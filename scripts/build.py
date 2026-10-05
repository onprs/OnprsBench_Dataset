"""发布构建工具。

流程：校验仓库 -> 生成 manifest -> 复制产物 -> 打包 tar.gz -> 生成 SHA256SUMS。
产物输出到 dist/（不入 git）。发布产物中的 manifest.yaml 即协议冻结版本。
"""
from __future__ import annotations

import argparse
import datetime
import shutil
import sys
import tarfile
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from common import (
    DATASET_ID,
    DATASET_NAME,
    PROTOCOL_VERSION,
    REPO_ROOT,
    VIS_JUDGE,
    VIS_META,
    VIS_SOLVER,
    bundle_sha256,
    collect_task_files,
    dump_yaml,
    git_revision,
    iter_task_dirs,
    load_schema,
    load_suites,
    load_yaml,
    sha256_file,
)
from validate import validate_repository

DATASET_DESCRIPTION = (
    "独立版本化的 LLM 基准数据集：外部坐标系 + 新鲜来源 + 衍生任务，"
    "关注模型面对新问题与新知识时的实际能力。"
)
DATASET_LICENSE = (
    "代码 MIT；本仓库原创任务内容 CC BY 4.0；"
    "外部来源内容以其 source 元数据为准（见 LICENSING.md）"
)


def build_manifest(root: Path, version: str, release_date: str) -> dict:
    """根据仓库当前内容生成 manifest 数据结构。"""
    suites = load_suites(root / "dataset" / "suites")

    # 任务 id -> 条目
    task_entries: dict[str, dict] = {}
    for suite_name, task_dir in iter_task_dirs(root / "dataset" / "tasks"):
        meta = load_yaml(task_dir / "meta.yaml")
        overrides = meta.get("visibility_overrides") or {}
        files = collect_task_files(task_dir, overrides)

        file_hashes = {rel: info["sha256"] for rel, info in files.items()}
        solver_visible = sorted(rel for rel, i in files.items() if i["visibility"] == VIS_SOLVER)
        judge_visible = sorted(rel for rel, i in files.items() if i["visibility"] == VIS_JUDGE)
        # VIS_META 文件（meta.yaml）只出现在 hashes 中，不进入两个可见性列表

        task_entries[meta["id"]] = {
            "id": meta["id"],
            "revision": meta["revision"],
            "title": meta["title"],
            "type": meta["type"],
            "tags": meta["tags"],
            "status": meta["lifecycle"]["status"],
            "path": f"dataset/tasks/{suite_name}/{task_dir.name}",
            "solver_visible": solver_visible,
            "judge_visible": judge_visible,
            "metadata": {
                "difficulty": meta["difficulty"]["author"],
                "freshness": meta["freshness"]["class"],
                "contamination": meta["contamination"]["risk"],
                "flagship": bool(meta.get("flagship", False)),
            },
            "hashes": {
                "bundle_sha256": bundle_sha256(file_hashes),
                "files": file_hashes,
            },
        }

    manifest_suites = []
    for sid in sorted(suites):
        sdata = suites[sid]
        manifest_suites.append(
            {
                "id": sdata["id"],
                "name": sdata["name"],
                "description": sdata["description"],
                "layer": sdata["layer"],
                "adapter": sdata.get("adapter"),
                "tasks": [task_entries[tid] for tid in sdata.get("tasks", []) if tid in task_entries],
            }
        )

    return {
        "protocol_version": PROTOCOL_VERSION,
        "dataset": {
            "id": DATASET_ID,
            "name": DATASET_NAME,
            "version": version,
            "release_date": release_date,
            "revision": git_revision(root),
            "description": DATASET_DESCRIPTION,
            "license": DATASET_LICENSE,
        },
        "suites": manifest_suites,
    }


def build_dataset(
    root: Path | None = None,
    out_root: Path | None = None,
    version: str | None = None,
    release_date: str | None = None,
) -> Path:
    """构建发布产物，返回 manifest.yaml 的路径。校验失败时抛出 RuntimeError。"""
    root = Path(root) if root else REPO_ROOT
    out_root = Path(out_root) if out_root else root / "dist"
    version = version or (root / "VERSION").read_text(encoding="utf-8").strip()
    release_date = release_date or datetime.date.today().isoformat()

    errors = validate_repository(root)
    if errors:
        raise RuntimeError("校验未通过，拒绝构建：\n" + "\n".join(f"  - {e}" for e in errors))

    manifest = build_manifest(root, version, release_date)

    # 产物 manifest 必须通过协议 schema
    validator = Draft202012Validator(load_schema("manifest.schema.json"), format_checker=FormatChecker())
    schema_errors = list(validator.iter_errors(manifest))
    if schema_errors:
        detail = "\n".join(f"  - {e.message}" for e in schema_errors)
        raise RuntimeError(f"生成的 manifest 未通过 schema 校验：\n{detail}")

    artifact_name = f"{DATASET_ID}-{version}"
    artifact_dir = out_root / artifact_name
    if artifact_dir.exists():
        shutil.rmtree(artifact_dir)
    artifact_dir.mkdir(parents=True)

    # 复制数据与许可文件
    shutil.copytree(root / "dataset", artifact_dir / "dataset")
    shutil.copy2(root / "LICENSE", artifact_dir / "LICENSE")

    manifest_path = artifact_dir / "manifest.yaml"
    manifest_path.write_text(dump_yaml(manifest), encoding="utf-8")

    # 打包与校验和
    tarball_path = out_root / f"{artifact_name}.tar.gz"
    if tarball_path.exists():
        tarball_path.unlink()
    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(artifact_dir, arcname=artifact_name)

    sums_path = out_root / "SHA256SUMS"
    manifest_sha = sha256_file(manifest_path)
    tarball_sha = sha256_file(tarball_path)
    sums_path.write_text(
        f"{manifest_sha}  {artifact_name}/manifest.yaml\n"
        f"{tarball_sha}  {artifact_name}.tar.gz\n",
        encoding="utf-8",
    )
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 OnprsBench Dataset 发布产物")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="仓库根目录")
    parser.add_argument("--out", type=Path, default=None, help="产物输出目录（默认 dist/）")
    parser.add_argument("--version", default=None, help="覆盖 VERSION 文件中的版本号")
    parser.add_argument("--date", default=None, help="覆盖发布日期（YYYY-MM-DD）")
    args = parser.parse_args()

    try:
        manifest_path = build_dataset(args.root, args.out, args.version, args.date)
    except RuntimeError as exc:
        print(str(exc))
        return 1

    from common import sha256_file as _sha

    task_count = sum(1 for _ in iter_task_dirs((args.root or REPO_ROOT) / "dataset" / "tasks"))
    print(f"构建完成：{manifest_path.parent}")
    print(f"任务数：{task_count}")
    print(f"manifest sha256：{_sha(manifest_path)}")
    print(f"SHA256SUMS：{manifest_path.parent.parent / 'SHA256SUMS'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

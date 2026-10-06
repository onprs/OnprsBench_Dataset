"""发布构建工具。

流程：校验仓库 -> 生成 manifest -> 复制产物 -> 打包 tar.gz -> 生成 SHA256SUMS。
产物输出到 dist/（不入 git）。发布产物中的 manifest.yaml 即协议冻结版本。
"""
from __future__ import annotations

import argparse
import datetime
import gzip
import re
import shutil
import subprocess
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


def build_manifest(
    root: Path,
    version: str,
    release_date: str,
    distribution: str = "standard",
    resources: list[dict] | None = None,
) -> dict:
    """根据仓库当前内容生成 manifest 数据结构。

    distribution 为 standard 时不附带 resources；full 时 resources 由
    materialize_resources 生成，包含可离线使用的判定资源与许可信息。
    """
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
        "distribution": distribution,
        "dataset": {
            "id": DATASET_ID,
            "name": DATASET_NAME,
            "version": version,
            "release_date": release_date,
            "revision": git_revision(root),
            "description": DATASET_DESCRIPTION,
            "license": DATASET_LICENSE,
        },
        "resources": resources or [],
        "suites": manifest_suites,
    }


_GITHUB_URL_RE = re.compile(
    r"github\.com[:/](?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)
_LICENSE_NAMES = (
    "LICENSE",
    "LICENSE.txt",
    "LICENSE.md",
    "LICENSE.rst",
    "LICENSE-MIT",
    "LICENSE-APACHE",
    "COPYING",
    "COPYING.txt",
)


def collect_repo_contracts(root: Path) -> dict[tuple[str, str], dict]:
    """扫描任务 verify.yaml，汇总 full 形态需要分发的仓库快照契约。

    返回 {(repo_url, commit): {owner, repo, url, commit, license, attribution}}。
    """
    contracts: dict[tuple[str, str], dict] = {}
    for _suite, task_dir in iter_task_dirs(root / "dataset" / "tasks"):
        verify_path = task_dir / "judge_assets" / "verify.yaml"
        if not verify_path.is_file():
            continue
        verify = load_yaml(verify_path) or {}
        commit = verify.get("base_commit")
        url = verify.get("repo_url") or (
            f"https://github.com/{verify['repo']}" if verify.get("repo") else None
        )
        if not commit or not url:
            continue
        meta = load_yaml(task_dir / "meta.yaml") or {}
        source = meta.get("source") or {}
        key = (str(url), str(commit))
        entry = contracts.setdefault(
            key,
            {"url": str(url), "commit": str(commit), "license": None, "attribution": None},
        )
        entry["license"] = entry["license"] or source.get("license")
        entry["attribution"] = entry["attribution"] or source.get("attribution")

    for (url, _commit), entry in contracts.items():
        match = _GITHUB_URL_RE.search(url)
        if match is None:
            raise RuntimeError(f"full 形态仅支持 GitHub 仓库资源，无法解析: {url}")
        owner, repo = match.group("owner"), match.group("repo")
        entry["owner"] = owner
        entry["repo"] = repo
        entry["repo_slug"] = f"{owner}/{repo}"
    return contracts


def _find_local_clone(root: Path, owner: str, repo: str, commit: str) -> Path | None:
    """在 imported/repos 中查找包含指定 commit 的本地 clone（离线打包用）。"""
    repos_root = root / "imported" / "repos"
    if not repos_root.is_dir():
        return None
    for clone in sorted(p for p in repos_root.iterdir() if p.is_dir()):
        if not (clone / ".git").exists():
            continue
        exists = subprocess.run(
            ["git", "-C", str(clone), "cat-file", "-e", f"{commit}^{{commit}}"],
            capture_output=True,
        )
        if exists.returncode != 0:
            continue
        remote = subprocess.run(
            ["git", "-C", str(clone), "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
        ).stdout.strip()
        match = _GITHUB_URL_RE.search(remote) if remote else None
        if match is not None:
            if match.group("owner").lower() == owner.lower() and match.group("repo").lower() == repo.lower():
                return clone
            continue
        # 无 remote 信息时按目录名兜底（imported/ 属维护者本地目录）
        if repo.lower() in clone.name.lower():
            return clone
    return None


def _export_snapshot(clone: Path, commit: str, dest: Path, prefix: str) -> None:
    """用 git archive 导出提交快照。

    gzip 固定 mtime=0，保证同一 commit 重复构建得到相同字节
    （资源的 sha256 因此可复现）。
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        ["git", "-C", str(clone), "archive", "--format=tar", f"--prefix={prefix}/", commit],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    with dest.open("wb") as fh, gzip.GzipFile(fileobj=fh, mode="wb", mtime=0) as gz:
        shutil.copyfileobj(proc.stdout, gz)
        _, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(
            f"git archive 导出失败: {commit}: {stderr.decode('utf-8', 'replace')[:300]}"
        )


def _download_snapshot(owner: str, repo: str, commit: str, dest: Path) -> None:
    """本地 clone 不可用时从 GitHub 归档下载（codeload，与框架缓存同源）。"""
    import urllib.request

    url = f"https://codeload.github.com/{owner}/{repo}/tar.gz/{commit}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    try:
        urllib.request.urlretrieve(url, tmp)
    except OSError as exc:
        raise RuntimeError(f"下载仓库快照失败: {url}: {exc}") from exc
    tmp.replace(dest)


def _extract_license(clone: Path, commit: str, dest: Path) -> str | None:
    """从提交快照中提取许可文件（保留原字节，供产物署名与再分发合规）。"""
    for name in _LICENSE_NAMES:
        proc = subprocess.run(
            ["git", "-C", str(clone), "show", f"{commit}:{name}"],
            capture_output=True,
        )
        if proc.returncode == 0 and proc.stdout:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(proc.stdout)
            return name
    return None


def materialize_resources(root: Path, artifact_dir: Path) -> list[dict]:
    """把 full 形态所需的仓库快照与许可文件写入产物目录，返回 manifest.resources 条目。"""
    resources: list[dict] = []
    for (_url, _commit), entry in sorted(collect_repo_contracts(root).items()):
        owner, repo, commit = entry["owner"], entry["repo"], entry["commit"]
        rel = f"resources/repos/{owner}-{repo}-{commit}.tar.gz"
        dest = artifact_dir / rel
        clone = _find_local_clone(root, owner, repo, commit)
        if clone is not None:
            _export_snapshot(clone, commit, dest, f"{repo}-{commit}")
        else:
            _download_snapshot(owner, repo, commit, dest)

        license_file_rel = None
        if clone is not None:
            license_dest = artifact_dir / "resources" / "licenses" / f"{owner}-{repo}-LICENSE.txt"
            if _extract_license(clone, commit, license_dest):
                license_file_rel = license_dest.relative_to(artifact_dir).as_posix()

        resources.append(
            {
                "id": f"repo-snapshot:{owner}/{repo}@{commit}",
                "kind": "repo_snapshot",
                "path": rel,
                "sha256": sha256_file(dest),
                "bytes": dest.stat().st_size,
                "source": {
                    "repo": f"{owner}/{repo}",
                    "url": entry["url"],
                    "commit": commit,
                    "license": entry["license"] or "上游仓库 LICENSE（见 license_file）",
                    "attribution": entry["attribution"] or f"{owner}/{repo}",
                    "license_file": license_file_rel,
                },
            }
        )
    return resources


def validate_artifact_resources(artifact_dir: Path, manifest: dict) -> None:
    """产物自检：resources 文件必须存在、大小与 sha256 与 manifest 一致。"""
    for res in manifest.get("resources") or []:
        path = artifact_dir / res["path"]
        if not path.is_file():
            raise RuntimeError(f"resources 文件缺失: {res['path']}")
        if path.stat().st_size != res["bytes"]:
            raise RuntimeError(f"resources 大小不匹配: {res['path']}")
        if sha256_file(path) != res["sha256"]:
            raise RuntimeError(f"resources sha256 不匹配: {res['path']}")
        license_file = (res.get("source") or {}).get("license_file")
        if license_file and not (artifact_dir / license_file).is_file():
            raise RuntimeError(f"resources 许可文件缺失: {license_file}")


def _update_sums(out_root: Path, entries: dict[str, str]) -> None:
    """合并写入 SHA256SUMS（保留另一套分发形态的条目）。"""
    sums_path = out_root / "SHA256SUMS"
    existing: dict[str, str] = {}
    if sums_path.is_file():
        for line in sums_path.read_text(encoding="utf-8").splitlines():
            if "  " in line:
                digest, rel = line.split("  ", 1)
                existing[rel.strip()] = digest.strip()
    existing.update(entries)
    sums_path.write_text(
        "".join(f"{digest}  {rel}\n" for rel, digest in sorted(existing.items())),
        encoding="utf-8",
        newline="\n",
    )


def build_dataset(
    root: Path | None = None,
    out_root: Path | None = None,
    version: str | None = None,
    release_date: str | None = None,
    distribution: str = "standard",
) -> Path:
    """构建一套发布产物，返回 manifest.yaml 的路径。校验失败时抛出 RuntimeError。

    distribution=standard：仅任务内容；full：同时打包 resources（仓库快照 + 许可）。
    """
    root = Path(root) if root else REPO_ROOT
    out_root = Path(out_root) if out_root else root / "dist"
    version = version or (root / "VERSION").read_text(encoding="utf-8").strip()
    release_date = release_date or datetime.date.today().isoformat()
    if distribution not in ("standard", "full"):
        raise RuntimeError(f"未知分发形态: {distribution}")

    errors = validate_repository(root)
    if errors:
        raise RuntimeError("校验未通过，拒绝构建：\n" + "\n".join(f"  - {e}" for e in errors))

    artifact_name = f"{DATASET_ID}-{version}" + ("-full" if distribution == "full" else "")
    artifact_dir = out_root / artifact_name
    if artifact_dir.exists():
        shutil.rmtree(artifact_dir)
    artifact_dir.mkdir(parents=True)

    # 复制数据与许可文件
    shutil.copytree(root / "dataset", artifact_dir / "dataset")
    shutil.copy2(root / "LICENSE", artifact_dir / "LICENSE")

    # full 形态：附带判定资源（仓库快照 + 上游许可）
    resources = materialize_resources(root, artifact_dir) if distribution == "full" else []

    manifest = build_manifest(root, version, release_date, distribution, resources)

    # 产物 manifest 必须通过协议 schema
    validator = Draft202012Validator(load_schema("manifest.schema.json"), format_checker=FormatChecker())
    schema_errors = list(validator.iter_errors(manifest))
    if schema_errors:
        detail = "\n".join(f"  - {e.message}" for e in schema_errors)
        raise RuntimeError(f"生成的 manifest 未通过 schema 校验：\n{detail}")

    validate_artifact_resources(artifact_dir, manifest)

    manifest_path = artifact_dir / "manifest.yaml"
    # manifest.yaml 的字节是 manifest hash 的依据：固定 LF 换行，保证跨平台可复现
    manifest_path.write_text(dump_yaml(manifest), encoding="utf-8", newline="\n")

    # 打包与校验和
    tarball_path = out_root / f"{artifact_name}.tar.gz"
    if tarball_path.exists():
        tarball_path.unlink()
    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(artifact_dir, arcname=artifact_name)

    _update_sums(
        out_root,
        {
            f"{artifact_name}/manifest.yaml": sha256_file(manifest_path),
            f"{artifact_name}.tar.gz": sha256_file(tarball_path),
        },
    )
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 OnprsBench Dataset 发布产物")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="仓库根目录")
    parser.add_argument("--out", type=Path, default=None, help="产物输出目录（默认 dist/）")
    parser.add_argument("--version", default=None, help="覆盖 VERSION 文件中的版本号")
    parser.add_argument("--date", default=None, help="覆盖发布日期（YYYY-MM-DD）")
    parser.add_argument(
        "--distribution",
        choices=["standard", "full", "both"],
        default="both",
        help="standard = 仅任务内容；full = 附带仓库快照等判定资源；both = 同时构建（默认）",
    )
    args = parser.parse_args()

    forms = ["standard", "full"] if args.distribution == "both" else [args.distribution]
    task_count = sum(1 for _ in iter_task_dirs((args.root or REPO_ROOT) / "dataset" / "tasks"))
    try:
        manifests = [
            build_dataset(args.root, args.out, args.version, args.date, distribution=form)
            for form in forms
        ]
    except RuntimeError as exc:
        print(str(exc))
        return 1

    from common import sha256_file as _sha

    for manifest_path in manifests:
        manifest = load_yaml(manifest_path)
        print(f"构建完成：{manifest_path.parent}")
        print(
            f"  形态：{manifest['distribution']} | 任务数：{task_count}"
            f" | 资源数：{len(manifest.get('resources') or [])}"
        )
        print(f"  manifest sha256：{_sha(manifest_path)}")
    print(f"SHA256SUMS：{manifests[-1].parent.parent / 'SHA256SUMS'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

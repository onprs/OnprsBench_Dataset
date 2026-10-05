"""数据集校验器。

CI 与发布前必须通过。检查项：
- 全部 YAML 符合对应 JSON Schema
- suite 与 task 的双向引用一致、id 唯一
- revision / 生命周期 / errata 合法
- 许可与污染风险元数据完备（schema 强制）
- 新鲜度分级与日期一致
- 可见性映射完整（无无法分类的文件）
- rubric 权重和为 1.0、维度 id 唯一
- flagship 任务的 anchor 文件齐备

退出码：0 通过；1 存在错误。
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from common import (
    REPO_ROOT,
    collect_task_files,
    iter_task_dirs,
    load_schema,
    load_yaml,
)

# 与 DATASET_POLICY.md 第 1 节保持一致的政策边界
FRESHNESS_BOUNDARIES = ((7, "F0"), (30, "F1"), (180, "F2"))

FLAGSHIP_ANCHORS = [
    "score-000.md",
    "score-025.md",
    "score-050.md",
    "score-075.md",
    "score-100.md",
]


def freshness_class(days: int) -> str:
    """按政策边界把天数映射为新鲜度级别。"""
    for upper, label in FRESHNESS_BOUNDARIES:
        if days <= upper:
            return label
    return "legacy"


def validate_repository(root: Path | None = None) -> list[str]:
    """校验整个仓库的数据目录，返回错误信息列表（空列表表示通过）。"""
    root = Path(root) if root else REPO_ROOT
    errors: list[str] = []
    fmt = FormatChecker()
    suite_schema = load_schema("suite.schema.json")
    task_schema = load_schema("task.schema.json")
    rubric_schema = load_schema("rubric.schema.json")

    def check_schema(schema: dict, data, label: str) -> None:
        validator = Draft202012Validator(schema, format_checker=fmt)
        for err in validator.iter_errors(data):
            where = "/".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{label}: 字段 {where}: {err.message}")

    # ---------- suite ----------
    suites_root = root / "dataset" / "suites"
    suites: dict[str, dict] = {}
    for suite_dir in sorted(p for p in suites_root.iterdir() if p.is_dir()):
        suite_path = suite_dir / "suite.yaml"
        if not suite_path.exists():
            errors.append(f"suites/{suite_dir.name}: 缺少 suite.yaml")
            continue
        data = load_yaml(suite_path)
        check_schema(suite_schema, data, f"suites/{suite_dir.name}/suite.yaml")
        sid = data.get("id", suite_dir.name)
        if sid != suite_dir.name:
            errors.append(f"suites/{suite_dir.name}: 目录名与 id {sid} 不一致")
        if sid in suites:
            errors.append(f"suite id 重复: {sid}")
        suites[sid] = data

    # 任务 id -> 所属 suite（来自 suite.yaml 收录列表）
    membership: dict[str, str] = {}
    for sid, sdata in suites.items():
        for tid in sdata.get("tasks", []):
            if tid in membership:
                errors.append(f"任务 {tid} 被多个 suite 收录: {membership[tid]} 与 {sid}")
            membership[tid] = sid

    # ---------- task ----------
    tasks_root = root / "dataset" / "tasks"
    seen_ids: set[str] = set()
    for suite_name, task_dir in iter_task_dirs(tasks_root):
        label = f"tasks/{suite_name}/{task_dir.name}"

        meta_path = task_dir / "meta.yaml"
        if not meta_path.exists():
            errors.append(f"{label}: 缺少 meta.yaml")
            continue
        meta = load_yaml(meta_path)
        check_schema(task_schema, meta, f"{label}/meta.yaml")

        tid = meta.get("id", task_dir.name)
        if tid in seen_ids:
            errors.append(f"任务 id 重复: {tid}")
        seen_ids.add(tid)

        if meta.get("suite") != suite_name:
            errors.append(f"{label}: meta.suite={meta.get('suite')} 与所在目录 {suite_name} 不一致")
        if membership.get(tid) != suite_name:
            errors.append(f"{label}: 未被 suites/{suite_name}/suite.yaml 收录")
        if suite_name not in suites:
            errors.append(f"{label}: 未知 suite 目录 {suite_name}")

        if not (task_dir / "problem.md").exists():
            errors.append(f"{label}: 缺少 problem.md（solver 题面）")

        rubric_path = task_dir / "rubric.yaml"
        if not rubric_path.exists():
            errors.append(f"{label}: 缺少 rubric.yaml")
        else:
            rubric = load_yaml(rubric_path)
            check_schema(rubric_schema, rubric, f"{label}/rubric.yaml")
            dims = rubric.get("dimensions", [])
            total = sum(d.get("weight", 0) for d in dims)
            if abs(total - 1.0) > 1e-9:
                errors.append(f"{label}/rubric.yaml: 维度权重之和为 {total}，应为 1.0")
            dim_ids = [d.get("id") for d in dims]
            if len(set(dim_ids)) != len(dim_ids):
                errors.append(f"{label}/rubric.yaml: 维度 id 重复")

        lifecycle = meta.get("lifecycle", {})
        if lifecycle.get("status") == "superseded" and not lifecycle.get("superseded_by"):
            errors.append(f"{label}: status 为 superseded 但未填写 superseded_by")
        for errata in lifecycle.get("errata", []):
            if errata.get("revision", 1) > meta.get("revision", 1):
                errors.append(f"{label}: errata 指向高于当前 revision 的版本")

        freshness = meta.get("freshness", {})
        base = freshness.get("source_published_at") or freshness.get("created_at")
        released = freshness.get("dataset_release_at")
        if base and released:
            days = (date.fromisoformat(str(released)) - date.fromisoformat(str(base))).days
            expected = freshness_class(days)
            if expected != freshness.get("class"):
                errors.append(
                    f"{label}: freshness.class={freshness.get('class')} 与日期差 {days} 天应有的 {expected} 不一致"
                )

        if meta.get("flagship"):
            for name in FLAGSHIP_ANCHORS:
                if not (task_dir / "anchors" / name).exists():
                    errors.append(f"{label}: flagship 任务缺少 anchor 文件 anchors/{name}")

        overrides = meta.get("visibility_overrides") or {}
        files = collect_task_files(task_dir, overrides)
        for rel, info in files.items():
            if info["visibility"] is None:
                errors.append(f"{label}: 文件 {rel} 无法识别可见性，请在 visibility_overrides 中声明")
        for rel in overrides:
            if rel not in files:
                errors.append(f"{label}: visibility_overrides 指向不存在的文件 {rel}")

    # suite 收录了不存在的任务
    for tid, sid in membership.items():
        if tid not in seen_ids:
            errors.append(f"suite {sid} 收录的任务 {tid} 不存在对应目录")

    return errors


def count_tasks(root: Path) -> int:
    return sum(1 for _ in iter_task_dirs(root / "dataset" / "tasks"))


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 OnprsBench Dataset 仓库")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="仓库根目录")
    args = parser.parse_args()

    errors = validate_repository(args.root)
    if errors:
        print(f"校验失败，共 {len(errors)} 处问题：")
        for line in errors:
            print(f"  - {line}")
        return 1
    print(f"校验通过：{count_tasks(args.root)} 个任务。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

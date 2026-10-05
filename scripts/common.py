"""共享工具：路径常量、YAML 读写、SHA-256 计算与可见性推导。

协议层面的规则以 PROTOCOL.md 与 DATASET_POLICY.md 为准，本文件是其实现。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"

DATASET_ID = "onprsbench-dataset"
DATASET_NAME = "OnprsBench Dataset"
PROTOCOL_VERSION = "1"

VIS_SOLVER = "solver"
VIS_JUDGE = "judge"
VIS_META = "meta"


def load_yaml(path: Path):
    """读取 YAML，并把日期对象统一转成 ISO 字符串（保证 schema 校验稳定）。"""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return _normalize_dates(data)


def _normalize_dates(value):
    if isinstance(value, datetime.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_dates(v) for v in value]
    return value


def dump_yaml(data) -> str:
    """以稳定格式序列化 YAML（manifest 等构建产物使用）。"""
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / name).read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def bundle_sha256(file_hashes: dict) -> str:
    """协议定义的 bundle hash：路径字典序拼接 "<path>  <sha256>" 后再取 SHA-256。"""
    lines = "".join(f"{rel}  {digest}\n" for rel, digest in sorted(file_hashes.items()))
    return sha256_bytes(lines.encode("utf-8"))


def default_visibility(relpath: str) -> str | None:
    """按仓库惯例推导可见性；无法识别时返回 None（由校验器要求显式声明）。"""
    if relpath == "problem.md" or relpath.startswith("assets/"):
        return VIS_SOLVER
    if (
        relpath == "rubric.yaml"
        or relpath.startswith("reference/")
        or relpath.startswith("anchors/")
        or relpath.startswith("judge_assets/")
    ):
        return VIS_JUDGE
    if relpath == "meta.yaml":
        return VIS_META
    return None


def iter_task_dirs(tasks_root: Path):
    """产出 (suite目录名, 任务目录)，按名称排序保证确定性。"""
    if not tasks_root.is_dir():
        return
    for suite_dir in sorted(tasks_root.iterdir()):
        if not suite_dir.is_dir():
            continue
        for task_dir in sorted(suite_dir.iterdir()):
            if task_dir.is_dir():
                yield suite_dir.name, task_dir


def collect_task_files(task_dir: Path, overrides: dict | None = None) -> dict:
    """收集任务目录全部文件，返回 {相对路径: {"sha256": ..., "visibility": ...}}。"""
    overrides = overrides or {}
    files = {}
    for path in sorted(task_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(task_dir).as_posix()
        files[rel] = {
            "sha256": sha256_file(path),
            "visibility": overrides.get(rel) or default_visibility(rel),
        }
    return files


def load_suites(suites_root: Path) -> dict:
    """读取全部 suite，返回 {suite_id: suite 数据}。"""
    suites = {}
    if not suites_root.is_dir():
        return suites
    for path in sorted(suites_root.glob("*/suite.yaml")):
        data = load_yaml(path)
        suites[data["id"]] = data
    return suites


def git_revision(root: Path) -> str:
    """返回构建时的 git commit；不在 git 仓库中时返回 uncommitted。"""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "uncommitted"

"""LiveCodeBench -> Dataset Protocol 转换器（原型，metadata_only 模式）。

输入：用户本地合法获取的 code_generation JSONL（每行一条记录，字段对应
livecodebench/code_generation_lite，如 question_content / platform /
question_id / contest_id / contest_date / difficulty）。

输出：协议任务骨架目录（meta.yaml + problem.md 占位 + 默认 rubric.yaml）。
题面与测试数据不入库，只在 import-report.yaml 中记录来源元数据与内容 hash。

用法：
    python adapter.py --input <本地.jsonl> --out <输出目录> [--upstream-version release_v6]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ADAPTER_ID = "livecodebench"
ADAPTER_VERSION = "0.1.0"
DEFAULT_UPSTREAM_VERSION = "release_v6"

DATASET_REPO = "https://huggingface.co/datasets/livecodebench/code_generation_lite"


def slugify(text: str) -> str:
    """把上游 question_id 转成协议允许的任务 id 片段。"""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "unknown"


def task_id_for(record: dict) -> str:
    platform = slugify(str(record.get("platform", "unknown")))
    qid = slugify(str(record.get("question_id", "unknown")))
    return f"lc-{platform}-{qid}"


def content_sha256(record: dict) -> str:
    """对上游记录的关键内容取 hash，用于溯源与变更检测（不保存内容本体）。"""
    payload = json.dumps(
        {
            "question_content": record.get("question_content", ""),
            "public_test_cases": record.get("public_test_cases", ""),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def convert_record(record: dict, upstream_version: str) -> tuple[str, dict, str, str]:
    """转换单条记录，返回 (任务id, meta, problem_md, rubric_yaml)。"""
    tid = task_id_for(record)
    contest_date = record.get("contest_date") or None

    meta = {
        "id": tid,
        "revision": 1,
        "title": f"LiveCodeBench {record.get('platform', '')} {record.get('question_id', '')}".strip(),
        "suite": "coding",
        "type": "code_generation",
        "tags": ["external", "code-generation", slugify(str(record.get("difficulty", "unknown")))],
        "lifecycle": {"status": "draft", "stage": "legacy", "superseded_by": None, "errata": []},
        "freshness": {
            "class": "legacy",
            "created_at": contest_date,
            "source_published_at": contest_date,
            "dataset_release_at": None,
        },
        "difficulty": {"author": _map_difficulty(record.get("difficulty"))},
        "source": {
            "kind": "external_benchmark",
            "name": "LiveCodeBench",
            "url": DATASET_REPO,
            "published_at": contest_date,
            "license": "代码 MIT；HF 数据集卡标注 license: cc",
            "redistribution": "metadata_only",
            "attribution": "LiveCodeBench authors (N. Jain et al.)",
            "upstream_version": upstream_version,
            "upstream_commit": None,
            "adapter": f"{ADAPTER_ID}@{ADAPTER_VERSION}",
        },
        "contamination": {
            "risk": "medium",
            "source_publication_date": contest_date,
            "exact_problem_public": True,
            "reference_public": False,
            "transformation": [],
            "notes": "题面在原竞赛平台公开；按 contest_date 做时间切片可降低污染。",
        },
        "license": "上游内容适用其原始许可；本骨架文件 CC BY 4.0",
        "authors": [f"adapter:{ADAPTER_ID}@{ADAPTER_VERSION}"],
        "flagship": False,
    }

    problem_md = (
        f"# {meta['title']}\n\n"
        "本任务以 metadata_only 方式接入，题面与测试数据不入库。\n\n"
        "本地导入方式（用户自行获取）：\n\n"
        "```python\n"
        "from datasets import load_dataset\n"
        f"ds = load_dataset(\"livecodebench/code_generation_lite\", version_tag=\"{upstream_version}\")\n"
        f"# 定位 platform={record.get('platform')}, question_id={record.get('question_id')} 的记录\n"
        "```\n"
    )

    rubric = {
        "rubric_version": 1,
        "dimensions": [
            {
                "id": "correctness",
                "weight": 1.0,
                "description": "生成的代码通过上游全部测试（公开 + 私有），由程序 verifier 判定。",
                "anchors": [
                    {"score": 0.0, "description": "未通过全部公开测试。"},
                    {"score": 0.5, "description": "通过全部公开测试，但私有测试存在失败。"},
                    {"score": 1.0, "description": "通过全部测试。"},
                ],
            }
        ],
    }
    return tid, meta, problem_md, yaml.safe_dump(rubric, allow_unicode=True, sort_keys=False)


def _map_difficulty(raw) -> str:
    """把上游 difficulty 映射到协议的人工预测难度枚举。"""
    return {"easy": "easy", "medium": "medium", "hard": "hard"}.get(
        str(raw or "").lower(), "medium"
    )


def convert_file(input_path: Path, out_dir: Path, upstream_version: str) -> list[dict]:
    """转换整个 JSONL，写出任务骨架与 import-report.yaml，返回报告条目。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for lineno, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        tid, meta, problem_md, rubric_yaml = convert_record(record, upstream_version)

        task_dir = out_dir / tid
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "meta.yaml").write_text(
            yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8"
        )
        (task_dir / "problem.md").write_text(problem_md, encoding="utf-8")
        (task_dir / "rubric.yaml").write_text(rubric_yaml, encoding="utf-8")

        report.append(
            {
                "id": tid,
                "platform": record.get("platform"),
                "question_id": record.get("question_id"),
                "contest_id": record.get("contest_id"),
                "contest_date": record.get("contest_date"),
                "content_sha256": content_sha256(record),
            }
        )

    (out_dir / "import-report.yaml").write_text(
        yaml.safe_dump(
            {
                "adapter": f"{ADAPTER_ID}@{ADAPTER_VERSION}",
                "upstream_version": upstream_version,
                "source": str(input_path),
                "count": len(report),
                "records": report,
            },
            allow_unicode=True,
            sort_keys=False,
            width=120,
        ),
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="LiveCodeBench 本地导入转换器（metadata_only）")
    parser.add_argument("--input", type=Path, required=True, help="本地 code_generation JSONL")
    parser.add_argument("--out", type=Path, required=True, help="骨架输出目录（建议 imported/coding/）")
    parser.add_argument("--upstream-version", default=DEFAULT_UPSTREAM_VERSION)
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"输入文件不存在：{args.input}")
        return 1
    report = convert_file(args.input, args.out, args.upstream_version)
    print(f"转换完成：{len(report)} 条 -> {args.out}")
    print("提示：骨架处于 draft 状态，需人工补全评审后方可移入 dataset/。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

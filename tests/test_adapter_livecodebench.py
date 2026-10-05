"""LiveCodeBench 适配器原型测试：转换产物必须符合协议 schema，且不复制题面。"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from common import load_schema, load_yaml  # noqa: E402

# 按路径加载适配器模块（适配器目录不是 Python 包）
_spec = importlib.util.spec_from_file_location(
    "lcb_adapter", ROOT / "adapters" / "livecodebench" / "adapter.py"
)
lcb_adapter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lcb_adapter)

SAMPLE = ROOT / "adapters" / "livecodebench" / "examples" / "sample.jsonl"


class LiveCodeBenchAdapterTest(unittest.TestCase):
    def test_convert_sample(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            report = lcb_adapter.convert_file(SAMPLE, out, "release_v6")
            self.assertEqual(len(report), 1)

            tid = report[0]["id"]
            self.assertRegex(tid, r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

            task_dir = out / tid
            meta = load_yaml(task_dir / "meta.yaml")

            # 任务元数据必须通过协议 schema
            validator = Draft202012Validator(
                load_schema("task.schema.json"), format_checker=FormatChecker()
            )
            self.assertEqual(list(validator.iter_errors(meta)), [])

            # metadata_only：题面占位文件不得包含上游题面内容
            problem = (task_dir / "problem.md").read_text(encoding="utf-8")
            self.assertNotIn("中位数", problem)
            self.assertIn("metadata_only", problem)

            # 导入报告记录内容 hash 而非内容本体
            import_report = yaml.safe_load((out / "import-report.yaml").read_text(encoding="utf-8"))
            self.assertEqual(import_report["count"], 1)
            self.assertRegex(report[0]["content_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(meta["source"]["redistribution"], "metadata_only")


if __name__ == "__main__":
    unittest.main()

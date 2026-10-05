"""构建工具测试：产物 manifest 必须通过协议 schema，且 hash 可复算一致。"""
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
from common import bundle_sha256, load_schema, sha256_file  # noqa: E402


class BuildTest(unittest.TestCase):
    def test_build_produces_consistent_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            manifest_path = build.build_dataset(
                ROOT, out_root=out, version="0.0.0", release_date="2026-10-05"
            )

            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

            # 协议 schema 校验
            validator = Draft202012Validator(
                load_schema("manifest.schema.json"), format_checker=FormatChecker()
            )
            self.assertEqual(list(validator.iter_errors(manifest)), [])

            self.assertEqual(manifest["protocol_version"], "1")
            self.assertEqual(manifest["dataset"]["version"], "0.0.0")

            # 每个任务的 bundle hash 可由文件 hash 复算
            task_total = 0
            for suite in manifest["suites"]:
                for task in suite["tasks"]:
                    task_total += 1
                    recomputed = bundle_sha256(task["hashes"]["files"])
                    self.assertEqual(task["hashes"]["bundle_sha256"], recomputed)
                    self.assertTrue(task["solver_visible"], "任务缺少 solver 可见文件")
                    self.assertTrue(task["judge_visible"], "任务缺少 judge 可见文件")
            self.assertGreaterEqual(task_total, 1)

            # 校验和文件存在且记录 manifest hash
            sums = (out / "SHA256SUMS").read_text(encoding="utf-8")
            self.assertIn(sha256_file(manifest_path), sums)

    def test_visibility_separation(self):
        """manifest 中 solver 列表不得包含任何 judge 路径。"""
        with tempfile.TemporaryDirectory() as td:
            manifest_path = build.build_dataset(
                ROOT, out_root=Path(td), version="0.0.0", release_date="2026-10-05"
            )
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            for suite in manifest["suites"]:
                for task in suite["tasks"]:
                    overlap = set(task["solver_visible"]) & set(task["judge_visible"])
                    self.assertEqual(overlap, set())
                    for rel in task["solver_visible"]:
                        self.assertFalse(
                            rel.startswith(("reference/", "anchors/", "judge_assets/"))
                            or rel == "rubric.yaml",
                            f"judge 材料泄露到 solver_visible: {rel}",
                        )


if __name__ == "__main__":
    unittest.main()

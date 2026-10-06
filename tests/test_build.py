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
            self.assertEqual(manifest["distribution"], "standard")
            self.assertEqual(manifest.get("resources"), [])

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

    def test_full_distribution_bundles_resources(self):
        """完整形态附带仓库快照与许可，资源 hash 可复算，两套产物 manifest hash 不同。"""
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            full_manifest_path = build.build_dataset(
                ROOT,
                out_root=out,
                version="0.0.0",
                release_date="2026-10-05",
                distribution="full",
            )
            manifest = yaml.safe_load(full_manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["distribution"], "full")
            self.assertTrue(manifest["resources"], "完整形态必须附带资源")

            artifact_dir = full_manifest_path.parent
            for res in manifest["resources"]:
                path = artifact_dir / res["path"]
                self.assertTrue(path.is_file(), res["path"])
                self.assertEqual(path.stat().st_size, res["bytes"])
                self.assertEqual(sha256_file(path), res["sha256"])
                source = res["source"]
                self.assertTrue(source["repo"])
                self.assertTrue(source["commit"])
                self.assertTrue(source["license"])
                self.assertTrue(source["attribution"])
                if source["license_file"]:
                    self.assertTrue((artifact_dir / source["license_file"]).is_file())

            # 同一版本号的两套产物：manifest hash 不同，SHA256SUMS 同时记录
            standard_manifest_path = build.build_dataset(
                ROOT,
                out_root=out,
                version="0.0.0",
                release_date="2026-10-05",
                distribution="standard",
            )
            self.assertNotEqual(sha256_file(full_manifest_path), sha256_file(standard_manifest_path))
            sums = (out / "SHA256SUMS").read_text(encoding="utf-8")
            self.assertIn("onprsbench-dataset-0.0.0-full/manifest.yaml", sums)
            self.assertIn("onprsbench-dataset-0.0.0-full.tar.gz", sums)
            self.assertIn("onprsbench-dataset-0.0.0/manifest.yaml", sums)
            self.assertIn("onprsbench-dataset-0.0.0.tar.gz", sums)

            # 资源被篡改时构建自检必须拒绝
            tampered = artifact_dir / manifest["resources"][0]["path"]
            tampered.write_bytes(tampered.read_bytes() + b"tampered")
            with self.assertRaises(RuntimeError):
                build.validate_artifact_resources(artifact_dir, manifest)

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

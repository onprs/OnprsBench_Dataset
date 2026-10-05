"""校验器测试：真实仓库必须通过；损坏的最小仓库必须报错。"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402
from common import bundle_sha256  # noqa: E402


class ValidateRepoTest(unittest.TestCase):
    def test_repository_passes(self):
        errors = validate.validate_repository(ROOT)
        self.assertEqual(errors, [])

    def test_freshness_boundaries(self):
        # 与 DATASET_POLICY.md 一致：F0 ≤7，F1 8–30，F2 31–180，其余 legacy
        self.assertEqual(validate.freshness_class(0), "F0")
        self.assertEqual(validate.freshness_class(7), "F0")
        self.assertEqual(validate.freshness_class(8), "F1")
        self.assertEqual(validate.freshness_class(30), "F1")
        self.assertEqual(validate.freshness_class(31), "F2")
        self.assertEqual(validate.freshness_class(180), "F2")
        self.assertEqual(validate.freshness_class(181), "legacy")

    def test_bundle_hash_deterministic(self):
        hashes = {"a.txt": "0" * 64, "b.txt": "1" * 64}
        self.assertEqual(bundle_sha256(hashes), bundle_sha256(dict(reversed(list(hashes.items())))))
        self.assertNotEqual(bundle_sha256(hashes), bundle_sha256({"a.txt": "0" * 64}))


class BrokenRepoTest(unittest.TestCase):
    """在临时目录构造损坏仓库，校验器必须检出错误。"""

    def _make_broken_repo(self, tmp: Path) -> Path:
        suite_dir = tmp / "dataset" / "suites" / "demo"
        task_dir = tmp / "dataset" / "tasks" / "demo" / "bad-task"
        suite_dir.mkdir(parents=True)
        task_dir.mkdir(parents=True)
        # suite 收录了任务，但任务 meta 缺少 license / contamination 等必填字段
        (suite_dir / "suite.yaml").write_text(
            "id: demo\nname: Demo\ndescription: 测试\nlayer: derived\nadapter: null\ntasks:\n  - bad-task\n",
            encoding="utf-8",
        )
        (task_dir / "meta.yaml").write_text(
            "id: bad-task\nrevision: 1\ntitle: 坏任务\n",
            encoding="utf-8",
        )
        (task_dir / "problem.md").write_text("# 题面\n", encoding="utf-8")
        (task_dir / "stray.txt").write_text("无法识别可见性的文件\n", encoding="utf-8")
        return tmp

    def test_broken_repo_detected(self):
        with tempfile.TemporaryDirectory() as td:
            repo = self._make_broken_repo(Path(td))
            errors = validate.validate_repository(repo)
        self.assertTrue(errors, "损坏仓库未被检出")
        joined = "\n".join(errors)
        self.assertIn("meta.yaml", joined)  # schema 必填字段缺失
        self.assertIn("stray.txt", joined)  # 可见性无法识别
        self.assertIn("rubric.yaml", joined)  # 缺少 rubric


if __name__ == "__main__":
    unittest.main()

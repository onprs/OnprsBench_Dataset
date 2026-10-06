"""Fresh SWE 候选采集器。

从 GitHub 采集"真实 issue + 已合并修复 PR + 含测试"的任务候选，
输出到 imported/fresh-swe/ 暂存区（不入库）。候选经本地复现验证后，
由维护者按 CURATION_GUIDE 移入 dataset/tasks/frontier-swe/。

依赖：gh CLI（已认证）。用法：
    python scripts/collect_fresh_swe.py --repo pallets/click --days 240 --max-pr 40
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING = REPO_ROOT / "imported" / "fresh-swe"

GRAPHQL = """
query($owner:String!, $name:String!, $n:Int!) {
  repository(owner:$owner, name:$name) {
    licenseInfo { spdxId }
    defaultBranchRef { name }
    pullRequests(first: $n, states: MERGED, orderBy:{field:UPDATED_AT, direction:DESC}) {
      nodes {
        number title mergedAt url additions deletions
        baseRefOid mergeCommit { oid }
        closingIssuesReferences(first: 3) { nodes { number title url createdAt } }
        files(first: 60) { nodes { path } }
      }
    }
  }
}
"""

TEST_HINT = ("test", "spec", "conftest")


def gh_graphql(owner: str, name: str, n: int) -> dict:
    out = subprocess.run(
        ["gh", "api", "graphql", "-F", f"owner={owner}", "-F", f"name={name}",
         "-F", f"n={n}", "-f", f"query={GRAPHQL}"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)["data"]["repository"]


def gh_rest(path: str, accept: str = "application/vnd.github+json") -> str:
    out = subprocess.run(
        ["gh", "api", path, "-H", f"Accept: {accept}"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout


def is_test_file(path: str) -> bool:
    name = path.rsplit("/", 1)[-1].lower()
    return any(h in path.lower() for h in TEST_HINT) and name.endswith((".py", ".pyx", ".js", ".ts"))


def is_source_file(path: str) -> bool:
    name = path.rsplit("/", 1)[-1].lower()
    return name.endswith((".py", ".pyx")) and not is_test_file(path)


def collect(repo: str, days: int, max_pr: int, max_changed: int) -> list[dict]:
    owner, name = repo.split("/")
    repo_data = gh_graphql(owner, name, max_pr)
    license_id = (repo_data.get("licenseInfo") or {}).get("spdxId") or "UNKNOWN"
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    candidates = []
    for pr in repo_data["pullRequests"]["nodes"]:
        issues = pr["closingIssuesReferences"]["nodes"]
        if not issues:
            continue
        merged_at = datetime.fromisoformat(pr["mergedAt"].replace("Z", "+00:00"))
        if merged_at < cutoff:
            continue
        files = [f["path"] for f in pr["files"]["nodes"]]
        tests = [f for f in files if is_test_file(f)]
        sources = [f for f in files if is_source_file(f)]
        if not tests or not sources:
            continue
        if pr["additions"] + pr["deletions"] > max_changed:
            continue
        candidates.append(
            {
                "repo": repo,
                "license": license_id,
                "pr": pr["number"],
                "title": pr["title"],
                "url": pr["url"],
                "merged_at": pr["mergedAt"],
                "base_commit": pr["baseRefOid"],
                "merge_commit": pr["mergeCommit"]["oid"],
                "issues": [{"number": i["number"], "title": i["title"], "url": i["url"],
                            "created_at": i["createdAt"]} for i in issues],
                "test_files": tests,
                "source_files": sources,
                "changed": f"+{pr['additions']}-{pr['deletions']}",
            }
        )
    return candidates


def stage(candidate: dict, staging: Path) -> Path:
    """抓取 issue 正文与 PR diff，写入暂存区。"""
    repo = candidate["repo"]
    dest = staging / f"{repo.replace('/', '__')}__pr{candidate['pr']}"
    dest.mkdir(parents=True, exist_ok=True)

    issue = candidate["issues"][0]
    issue_detail = json.loads(gh_rest(f"repos/{repo}/issues/{issue['number']}"))
    (dest / "issue.md").write_text(
        f"# {issue_detail['title']}\n\n来源：{issue['url']}\n\n"
        + (issue_detail.get("body") or "（无正文）"),
        encoding="utf-8",
        newline="\n",
    )

    diff = gh_rest(f"repos/{repo}/pulls/{candidate['pr']}", accept="application/vnd.github.v3.diff")
    (dest / "fix.diff").write_text(diff, encoding="utf-8", newline="\n")

    (dest / "candidate.yaml").write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    return dest


def main() -> int:
    parser = argparse.ArgumentParser(description="采集 Fresh SWE 候选")
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--days", type=int, default=240, help="合并时间窗口（天）")
    parser.add_argument("--max-pr", type=int, default=40)
    parser.add_argument("--max-changed", type=int, default=400, help="变更行数上限（保证可复现性）")
    parser.add_argument("--fetch", action="store_true", help="抓取 issue 正文与 diff 到暂存区")
    args = parser.parse_args()

    candidates = collect(args.repo, args.days, args.max_pr, args.max_changed)
    print(f"{args.repo}: {len(candidates)} 个候选")
    for c in candidates:
        print(f"  PR#{c['pr']} {c['merged_at'][:10]} {c['changed']} "
              f"issue#{c['issues'][0]['number']} tests={len(c['test_files'])} {c['title'][:50]}")

    if args.fetch:
        for c in candidates:
            dest = stage(c, STAGING)
            print(f"  已暂存 {dest.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

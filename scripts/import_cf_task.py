"""Codeforces 任务本地导入器（metadata_only 模式）。

在维护者本机运行：抓取指定题目的题面与官方题解（含官方参考代码），
写入 imported/cf/<contest><index>/ 暂存区，并打印各文件 sha256。
题库内容按 research_archive 政策归档入库（署名 + 上游 hash，见 LICENSING.md）；
本工具用于首次获取与后续核对上游内容是否变动。

用法：
    python scripts/import_cf_task.py --contest 2269 --index C
    python scripts/import_cf_task.py --contest 2269 --index C --tutorial 157140
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGING = REPO_ROOT / "imported" / "cf"

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
)


def fetch(url: str) -> str:
    """以浏览器 UA 抓取公开页面（匿名抓取会被反爬拦截）。"""
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_block(fragment: str) -> str:
    """把 Codeforces 的 HTML 片段转成纯文本（保留行结构）。"""
    t = re.sub(r"</div>\s*", "\n", fragment)
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    lines = [ln.strip() for ln in t.splitlines()]
    return "\n".join(ln for ln in lines if ln).strip()


def extract_statement(page: str) -> dict:
    """从题目页提取题面信息。"""
    def grab(pattern: str, default: str = "") -> str:
        m = re.search(pattern, page, re.S)
        return clean_block(m.group(1)) if m else default

    samples = []
    for inp, ans in re.findall(
        r'<div class="input"><div class="title">Input</div><pre>(.*?)</pre></div>'
        r'<div class="output"><div class="title">Output</div><pre>(.*?)</pre></div>',
        page, re.S,
    ):
        samples.append({"input": clean_block(inp), "output": clean_block(ans)})

    return {
        "title": grab(r'<div class="title">([^<]+)</div>'),
        "time_limit": grab(r'<div class="time-limit">(.*?)</div>'),
        "memory_limit": grab(r'<div class="memory-limit">(.*?)</div>'),
        "statement": grab(r'<div class="problem-statement">(.*?)<div class="input-specification">'),
        "input_spec": grab(r'<div class="input-specification">(.*?)<div class="output-specification">'),
        "output_spec": grab(r'<div class="output-specification">(.*?)<div class="sample-tests">'),
        "samples": samples,
    }


def find_tutorial_entry(contest: int) -> str | None:
    """从比赛页侧栏找官方题解 blog entry id。"""
    page = fetch(f"https://codeforces.com/contest/{contest}")
    m = re.search(r'href="(/blog/entry/(\d+))"[^>]*>\s*Tutorial', page)
    return m.group(2) if m else None


def extract_editorial(tutorial_page: str, contest: int, index: str) -> dict:
    """从官方题解页提取指定题目的小节与首个代码块（官方参考实现）。"""
    start = tutorial_page.find(f"{contest}{index} - ")
    if start < 0:
        raise RuntimeError(f"题解页中未找到 {contest}{index} 小节")
    m = re.search(rf"{contest}[A-Z]{1,2} - ", tutorial_page[start + 10:])
    end = start + 10 + m.start() if m else len(tutorial_page)
    seg = tutorial_page[start:end]

    codes = re.findall(r"<pre[^>]*>(.*?)</pre>", seg, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", codes[0])).strip() if codes else ""
    text = clean_block(re.sub(r"<pre[^>]*>.*?</pre>", "\n[代码]\n", seg, flags=re.S))
    return {"text": text, "official_code": code}


def main() -> int:
    parser = argparse.ArgumentParser(description="Codeforces 任务本地导入器（metadata_only）")
    parser.add_argument("--contest", type=int, required=True)
    parser.add_argument("--index", required=True, help="题目序号，如 C / F1")
    parser.add_argument("--tutorial", default=None, help="官方题解 blog entry id；缺省自动探测")
    args = parser.parse_args()

    dest = STAGING / f"{args.contest}{args.index.lower()}"
    dest.mkdir(parents=True, exist_ok=True)

    statement = extract_statement(fetch(f"https://codeforces.com/contest/{args.contest}/problem/{args.index}"))
    (dest / "statement.txt").write_text(
        f"# {statement['title']}\n\n{statement['time_limit']} / {statement['memory_limit']}\n\n"
        f"{statement['statement']}\n\n## 输入\n{statement['input_spec']}\n\n"
        f"## 输出\n{statement['output_spec']}\n",
        encoding="utf-8",
    )
    (dest / "samples.json").write_text(
        json.dumps(statement["samples"], ensure_ascii=False, indent=2), encoding="utf-8"
    )

    tutorial = args.tutorial or find_tutorial_entry(args.contest)
    if not tutorial:
        print("未找到官方题解链接", file=sys.stderr)
        return 1
    editorial = extract_editorial(fetch(f"https://codeforces.com/blog/entry/{tutorial}"), args.contest, args.index)
    (dest / "editorial.txt").write_text(editorial["text"], encoding="utf-8")
    if editorial["official_code"]:
        (dest / "official.cpp").write_text(editorial["official_code"], encoding="utf-8")

    print(f"导入完成：{dest.relative_to(REPO_ROOT)}（tutorial entry {tutorial}）")
    for name in ("statement.txt", "samples.json", "editorial.txt", "official.cpp"):
        f = dest / name
        if f.exists():
            print(f"  {name}  sha256={sha256_text(f.read_text(encoding='utf-8'))[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""暴力求解器（对拍基准）。

枚举全部子集，检查容量与颜色可行性（max_c |S_c| <= |S| - max_c |S_c| + 1），
取最大收益。仅用于小规模用例。从 stdin 读入题目格式输入。
"""
import sys


def brute(n: int, b: int, items: list[tuple[int, int, int]]) -> int:
    best = 0
    for mask in range(1 << n):
        weight = 0
        profit = 0
        counts: dict[int, int] = {}
        ok = True
        for i in range(n):
            if mask >> i & 1:
                w, p, c = items[i]
                weight += w
                if weight > b:
                    ok = False
                    break
                profit += p
                counts[c] = counts.get(c, 0) + 1
        if not ok:
            continue
        total = bin(mask).count('1')
        mx = max(counts.values()) if counts else 0
        if 2 * mx <= total + 1 and profit > best:
            best = profit
    return best


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); b = int(data[idx + 1]); idx += 2
        if n > 18:
            raise SystemExit("暴力解法仅支持 n <= 18 的用例")
        items = []
        for _ in range(n):
            w = int(data[idx]); p = int(data[idx + 1]); c = int(data[idx + 2]); idx += 3
            items.append((w, p, c))
        out.append(str(brute(n, b, items)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

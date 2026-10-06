"""暴力求解器（对拍基准）。

从 stdin 读入题目格式的输入，对每个用例枚举所有含 A 个 a、B 个 b 的词，
按 |w|_ab 分组后取普遍性指数的最大值与最小值（即存在指数与全称指数）。
仅适用于 A + B <= 17 的小规模用例；用于与参考解对拍。
"""
import sys
from itertools import combinations


def iota(word: str) -> int:
    """词的普遍性指数：贪心 arch 分解中完整 arch 的个数。"""
    seen = set()
    k = 0
    for ch in word:
        seen.add(ch)
        if len(seen) == 2:
            k += 1
            seen.clear()
    return k


def brute(a: int, b: int, c: int) -> tuple[int, int]:
    n = a + b
    if n == 0:
        return 0, 0
    best_max = -1
    best_min = 10 ** 9
    for pos in combinations(range(n), a):
        s = ["b"] * n
        for i in pos:
            s[i] = "a"
        word = "".join(s)
        ab = 0
        seen_a = 0
        for ch in word:
            if ch == "a":
                seen_a += 1
            else:
                ab += seen_a
        if ab != c:
            continue
        v = iota(word)
        best_max = max(best_max, v)
        best_min = min(best_min, v)
    if best_max < 0:
        raise ValueError(f"参数非法：C={c} 在 A={a}, B={b} 下不可达")
    return best_max, best_min


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        a = int(data[idx])
        b = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        if a + b > 17:
            raise SystemExit("暴力解法仅支持 A + B <= 17 的用例")
        e, f = brute(a, b, c)
        out.append(f"{e} {f}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

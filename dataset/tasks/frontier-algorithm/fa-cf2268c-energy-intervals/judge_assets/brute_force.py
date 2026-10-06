"""2268C 暴力求解器（对拍基准）。

直接枚举全部区间 (l, r)（l < r），按定义计算
XOR_{k=l..r} (a_k & max(a_l..a_r))，取最大值。
仅用于小规模应力测试；从 stdin 读入题目输入，每行一个答案。
"""
import sys


def solve(a: list[int]) -> int:
    n = len(a)
    best = 0
    for l in range(n):
        m = 0
        for r in range(l, n):
            m = max(m, a[r])
            if r == l:
                continue
            value = 0
            for k in range(l, r + 1):
                value ^= a[k] & m
            best = max(best, value)
    return best


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx: idx + n]]; idx += n
        out.append(str(solve(a)))
    print("\n".join(out))


if __name__ == "__main__":
    main()

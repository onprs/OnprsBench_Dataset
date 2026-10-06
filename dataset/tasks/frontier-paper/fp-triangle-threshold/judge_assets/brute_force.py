"""暴力求解器（对拍基准）。

按定义逐步模拟：每次插入前枚举已插入邻居求公共邻居数；仅用于小规模用例。
从 stdin 读入题目格式输入，输出格式与参考解一致。
"""
import sys
from math import gcd


def simulate(m: int, q: int, edges: list[tuple[int, int]]) -> tuple[int, int, int]:
    adj: dict[int, set[int]] = {}
    cnt = 0
    s = 0
    stopped = False
    for u, v in edges:
        if not stopped:
            au = adj.get(u, set())
            av = adj.get(v, set())
            cnt += len(au & av)
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
            s += 1
            if cnt >= q:
                stopped = True
    p = q * m ** 3
    r = s ** 3
    g = gcd(p, r)
    return s, p // g, r // g


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        m = int(data[idx]); q = int(data[idx + 1]); idx += 2
        if m > 2000:
            raise SystemExit("暴力解法仅支持 m <= 2000 的用例")
        edges = []
        for _ in range(m):
            u = int(data[idx]); v = int(data[idx + 1]); idx += 2
            edges.append((u, v))
        s, p, r = simulate(m, q, edges)
        out.append(f"{s} {p} {r}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

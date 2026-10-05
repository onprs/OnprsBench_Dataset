"""2269D 暴力求解器（对拍基准）。

操作是可逆的（同一掩码作用两次即还原），可达状态构成无向图的连通分量。
对每个连通分量求"3 的倍数元素个数"的最大值；每次查询把数组映射到
其所在分量的最大值。仅用于小规模应力测试（n <= 3）。
输入输出格式与题目一致。
"""
import sys
from collections import deque

MASKS = [3 * k for k in range(1, 6)]  # 3,6,9,12,15


def neighbors(state: tuple):
    n = len(state)
    for i in range(n - 1):
        for m in MASKS:
            nxt = list(state)
            nxt[i] ^= m
            nxt[i + 1] ^= m
            yield tuple(nxt)


def good_count(state: tuple) -> int:
    return sum(1 for x in state if x % 3 == 0)


class ComponentTable:
    """按 n 惰性构建连通分量表：state -> 分量内最大 good_count。"""

    def __init__(self) -> None:
        self._best: dict[int, dict[tuple, int]] = {}

    def _build(self, n: int) -> None:
        best: dict[tuple, int] = {}
        for top in range(16 ** n):
            state = tuple((top >> (4 * i)) & 15 for i in range(n))
            if state in best:
                continue
            comp = [state]
            seen = {state}
            q = deque([state])
            mx = good_count(state)
            while q:
                cur = q.popleft()
                for nxt in neighbors(cur):
                    if nxt not in seen:
                        seen.add(nxt)
                        mx = max(mx, good_count(nxt))
                        comp.append(nxt)
                        q.append(nxt)
            for s in comp:
                best[s] = mx
        self._best[n] = best

    def query(self, state: tuple) -> int:
        n = len(state)
        if n not in self._best:
            self._build(n)
        return self._best[n][tuple(state)]


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    table = ComponentTable()
    out_lines = []
    for _ in range(t):
        n, q = int(data[idx]), int(data[idx + 1]); idx += 2
        a = [int(x) for x in data[idx: idx + n]]; idx += n
        answers = [str(table.query(tuple(a)))]
        for _ in range(q):
            p, x = int(data[idx]), int(data[idx + 1]); idx += 2
            a[p - 1] = x
            answers.append(str(table.query(tuple(a))))
        out_lines.append(" ".join(answers))
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()

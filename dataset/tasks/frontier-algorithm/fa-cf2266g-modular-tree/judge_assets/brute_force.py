"""2266G 暴力求解器（对拍基准）。

在小规模、小模数下直接 BFS 全部可达状态：每个节点的取值落在 [0, b_i)，
状态数上界为 ∏b_i。对每个可达状态统计节点值总和，取最大值。
仅用于小规模应力测试。
"""
import sys
from collections import deque


def solve(n: int, a: list[int], b: list[int], edges: list[tuple[int, int]]) -> int:
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    children = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    order = [1]
    parent[1] = -1
    for u in order:
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                children[u].append(v)
                order.append(v)

    start = tuple(a)
    seen = {start}
    queue = deque([start])
    best = sum(start)
    while queue:
        state = queue.popleft()
        for u in range(1, n + 1):
            s = sum(state[v - 1] for v in children[u])
            nxt = list(state)
            nxt[u - 1] = (nxt[u - 1] + s) % b[u - 1]
            nxt = tuple(nxt)
            if nxt not in seen:
                seen.add(nxt)
                best = max(best, sum(nxt))
                queue.append(nxt)
    return best


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx: idx + n]]; idx += n
        b = [int(x) for x in data[idx: idx + n]]; idx += n
        edges = []
        for _ in range(n - 1):
            u, v = int(data[idx]), int(data[idx + 1]); idx += 2
            edges.append((u, v))
        out.append(str(solve(n, a, b, edges)))
    print("\n".join(out))


if __name__ == "__main__":
    main()

"""2268D 暴力求解器（对拍基准）。

按定义建图：i 可以走到任意 j < i，以及右侧第一个满足 p_j > p_i 的 j。
对每个起点 BFS 求到所有点的最短路，累加距离（不可达记 0）。
仅用于小规模应力测试。
"""
import sys
from collections import deque


def solve(p: list[int]) -> int:
    n = len(p)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i - 1, -1, -1):
            adj[i].append(j)
        nxt = n
        for j in range(i + 1, n):
            if p[j] > p[i]:
                nxt = j
                break
        if nxt < n:
            adj[i].append(nxt)

    total = 0
    for src in range(n):
        dist = [-1] * n
        dist[src] = 0
        queue = deque([src])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        total += sum(d if d > 0 else 0 for d in dist)
    return total


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        p = [int(x) for x in data[idx: idx + n]]; idx += n
        out.append(str(solve(p)))
    print("\n".join(out))


if __name__ == "__main__":
    main()

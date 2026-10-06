"""随机测试生成器（应力测试用）。

用法：python generator.py <种子> <用例数>

生成随机简单图及其边的随机顺序，覆盖：无三角形图（永不触发阈值）、
小 Q 提前停止、大 Q 全流过、稠密小图与稀疏大图。输出格式与 problem.md 一致。
"""
import random
import sys


def gen_case(rng: random.Random) -> tuple[int, int, list[tuple[int, int]]]:
    kind = rng.random()
    if kind < 0.20:
        # 二部图：没有三角形，永远不会达到阈值（Q >= 1）
        n = rng.randint(2, 30)
        side = n // 2
        edges = []
        for u in range(side):
            for v in range(side, n):
                edges.append((u, v))
        rng.shuffle(edges)
        m = min(len(edges), rng.randint(1, 200))
        edges = edges[:m]
        q = rng.choice([1, 2, rng.randint(1, 10)])
        return m, q, edges
    if kind < 0.45:
        # 稠密小图：三角形多，阈值小，提前停止
        n = rng.randint(5, 60)
        all_edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
        rng.shuffle(all_edges)
        m = rng.randint(1, min(len(all_edges), 300))
        edges = all_edges[:m]
        q = rng.choice([1, 2, 3, rng.randint(1, 50)])
        return m, q, edges
    if kind < 0.75:
        # 稀疏大图：m 较大，阈值中等
        n = rng.randint(50, 4000)
        m = rng.randint(10, 4000)
        m = min(m, n * (n - 1) // 2)
        seen = set()
        edges = []
        while len(edges) < m:
            u = rng.randrange(n)
            v = rng.randrange(n)
            if u == v:
                continue
            if u > v:
                u, v = v, u
            if (u, v) in seen:
                continue
            seen.add((u, v))
            edges.append((u, v))
        rng.shuffle(edges)
        q = rng.choice([rng.randint(1, 20), rng.randint(1, 1000), 10 ** 12, 10 ** 18])
        return m, q, edges
    # 带明显团块的图：三角形集中
    n = rng.randint(10, 120)
    m = rng.randint(5, 400)
    m = min(m, n * (n - 1) // 2)
    seen = set()
    edges = []
    while len(edges) < m:
        u = rng.randrange(n)
        v = rng.randrange(n)
        if u == v:
            continue
        if u > v:
            u, v = v, u
        if (u, v) in seen:
            continue
        seen.add((u, v))
        edges.append((u, v))
    rng.shuffle(edges)
    q = rng.choice([1, 2, rng.randint(1, 200)])
    return m, q, edges


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    rng = random.Random(seed)
    print(cases)
    for _ in range(cases):
        m, q, edges = gen_case(rng)
        print(m, q)
        for u, v in edges:
            print(u, v)


if __name__ == "__main__":
    main()

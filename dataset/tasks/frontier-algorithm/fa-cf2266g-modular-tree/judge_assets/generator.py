"""2266G 随机测试生成器（应力测试用）。

生成小规模随机树（节点标签随机置换），使节点 1 为随机根。
用法：python generator.py <种子> <用例数>
"""
import random
import sys


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)

    print(cases)
    for _ in range(cases):
        n = rng.randint(1, 5)
        perm = list(range(1, n + 1))
        rng.shuffle(perm)  # perm[old] = new label
        a = []
        b = []
        for _ in range(n):
            mod = rng.randint(1, 8)
            b.append(mod)
            a.append(rng.randrange(mod))
        a2 = [0] * n
        b2 = [0] * n
        for old in range(1, n + 1):
            new = perm[old - 1]
            a2[new - 1] = a[old - 1]
            b2[new - 1] = b[old - 1]
        edges = []
        for old in range(2, n + 1):
            parent_old = rng.randint(1, old - 1)
            edges.append((perm[old - 1], perm[parent_old - 1]))
        print(n)
        print(*a2)
        print(*b2)
        for u, v in edges:
            if rng.random() < 0.5:
                u, v = v, u
            print(u, v)


if __name__ == "__main__":
    main()

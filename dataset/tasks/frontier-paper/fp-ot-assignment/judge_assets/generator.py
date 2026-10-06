"""随机测试生成器（应力测试用）。

用法：python generator.py <种子> <用例数>

覆盖均匀随机、带植入排列、对角便宜、低秩结构与不同规模（n 至 400）。
输出格式与 problem.md 一致。
"""
import random
import sys

MAXC = 10 ** 6


def gen_matrix(rng: random.Random, n: int) -> list[list[int]]:
    kind = rng.random()
    if kind < 0.40:
        return [[rng.randint(0, MAXC) for _ in range(n)] for _ in range(n)]
    if kind < 0.65:
        # 植入一个随机排列并小幅扰动，最优解接近植入排列
        base = list(range(n))
        rng.shuffle(base)
        m = [[rng.randint(0, MAXC) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            j = base[i]
            m[i][j] = rng.randint(0, 100)
        return m
    if kind < 0.85:
        # 对角便宜
        m = [[rng.randint(0, MAXC) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            m[i][i] = rng.randint(0, 50)
        return m
    # 低秩（度量式）结构：C[i][j] = |x_i - y_j| 的小扰动
    xs = [rng.randint(0, n) for _ in range(n)]
    ys = [rng.randint(0, n) for _ in range(n)]
    return [[abs(xs[i] - ys[j]) + rng.randint(0, 20) for j in range(n)] for i in range(n)]


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    rng = random.Random(seed)
    print(cases)
    for _ in range(cases):
        r = rng.random()
        if r < 0.35:
            n = rng.randint(1, 8)
        elif r < 0.65:
            n = rng.randint(9, 60)
        elif r < 0.85:
            n = rng.randint(60, 200)
        else:
            n = rng.randint(200, 400)
        m = gen_matrix(rng, n)
        print(n)
        for row in m:
            print(*row)


if __name__ == "__main__":
    main()

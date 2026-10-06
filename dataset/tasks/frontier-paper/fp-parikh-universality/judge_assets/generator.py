"""随机测试生成器（应力测试用）。

用法：python generator.py <种子> <用例数>

覆盖小参数、全枚举边界（C = 0、C = A*B、k(k-1)/2 阈值附近、A 的倍数）
与大参数（A, B 达 1e18）。输出格式与 problem.md 一致。
"""
import random
import sys

MAXV = 10 ** 18


def make_c(rng: random.Random, a: int, b: int) -> int:
    ab = a * b
    if ab == 0:
        return 0
    r = rng.random()
    if r < 0.12:
        return 0
    if r < 0.24:
        return ab
    if r < 0.45:
        k = rng.randint(0, min(a, b))
        return min(ab, k * (k - 1) // 2)
    if r < 0.60:
        k = rng.randint(0, min(a, b))
        return max(0, ab - k * (k - 1) // 2)
    if r < 0.72 and a > 0:
        q = rng.randint(1, max(1, ab // a))
        return min(ab, a * q)
    if r < 0.84 and b > 0:
        q = rng.randint(1, max(1, ab // b))
        return min(ab, b * q)
    return rng.randint(0, ab)


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    rng = random.Random(seed)

    print(cases)
    for _ in range(cases):
        r = rng.random()
        if r < 0.35:
            a = rng.randint(0, 6)
            b = rng.randint(0, 6)
        elif r < 0.60:
            a = rng.randint(0, 300)
            b = rng.randint(0, 300)
        elif r < 0.80:
            a = rng.randint(0, 10 ** 6)
            b = rng.randint(0, 10 ** 6)
        else:
            a = rng.randint(0, MAXV)
            b = rng.randint(0, MAXV)
        print(a, b, make_c(rng, a, b))


if __name__ == "__main__":
    main()

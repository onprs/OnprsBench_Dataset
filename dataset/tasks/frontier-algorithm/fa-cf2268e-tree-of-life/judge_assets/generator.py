"""2268E 随机测试生成器（应力测试用）。

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
        n = rng.randint(1, 6)
        bits = rng.choice([2, 3, 4, 18])
        hi = 1 << bits
        a = [rng.randrange(hi) for _ in range(n)]
        print(n)
        print(*a)


if __name__ == "__main__":
    main()

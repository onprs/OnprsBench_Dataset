"""2264E1 随机测试生成器（应力测试用）。

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
        n = rng.randint(1, 8)
        print(n)
        if rng.random() < 0.5:
            a = [rng.randint(1, n) for _ in range(n)]
        else:
            a = [rng.randint(1, min(n, 4)) for _ in range(n)]
        print(*a)


if __name__ == "__main__":
    main()

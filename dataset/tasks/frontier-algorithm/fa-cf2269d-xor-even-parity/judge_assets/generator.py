"""2269D 随机测试生成器（应力测试用，小规模以便暴力核验）。

用法：python generator.py <种子> <用例数>
输出到 stdout，格式与题目输入一致。
"""
import random
import sys


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    rng = random.Random(seed)

    print(cases)
    for _ in range(cases):
        n = rng.randint(2, 3)
        q = rng.randint(0, 3)
        a = [rng.randint(0, 15) for _ in range(n)]
        print(n, q)
        print(*a)
        for _ in range(q):
            p = rng.randint(1, n)
            x = rng.randint(0, 15)
            print(p, x)


if __name__ == "__main__":
    main()

"""随机测试生成器（应力测试用）。

用法：python generator.py <种子> <用例数>

覆盖不同字母表大小、全字母出现/缺失、高度重复、de Bruijn 式覆盖与随机串。
输出格式与 problem.md 一致。
"""
import random
import sys


def random_string(rng: random.Random, n: int, sigma: int) -> str:
    kind = rng.random()
    if kind < 0.20:
        # 保证每个字母至少出现一次：先放一轮全字母，再随机填充
        if n < sigma:
            return ''.join(chr(ord('a') + i % sigma) for i in range(n))
        letters = [chr(ord('a') + i) for i in range(sigma)]
        rng.shuffle(letters)
        rest = [chr(ord('a') + rng.randrange(sigma)) for _ in range(n - sigma)]
        chars = letters + rest
        rng.shuffle(chars)
        return ''.join(chars)
    if kind < 0.40:
        # 高度周期
        period = rng.randint(1, max(1, min(8, n)))
        base = ''.join(chr(ord('a') + rng.randrange(sigma)) for _ in range(period))
        return (base * (n // period + 1))[:n]
    if kind < 0.55:
        # 单字母
        return chr(ord('a') + rng.randrange(sigma)) * n
    if kind < 0.70:
        # 两个固定字母交替
        a = chr(ord('a') + rng.randrange(sigma))
        b = chr(ord('a') + rng.randrange(sigma))
        return ''.join(a if i % 2 == 0 else b for i in range(n))
    return ''.join(chr(ord('a') + rng.randrange(sigma)) for _ in range(n))


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    rng = random.Random(seed)
    print(cases)
    for _ in range(cases):
        r = rng.random()
        if r < 0.35:
            sigma = rng.randint(1, 4)
            n = rng.randint(1, 120)
        elif r < 0.65:
            sigma = rng.randint(2, 8)
            n = rng.randint(50, 3000)
        elif r < 0.85:
            sigma = rng.randint(2, 26)
            n = rng.randint(500, 20000)
        else:
            sigma = 26
            n = rng.randint(10000, 200000)
        s = random_string(rng, n, sigma)
        print(n, sigma)
        print(s)


if __name__ == "__main__":
    main()

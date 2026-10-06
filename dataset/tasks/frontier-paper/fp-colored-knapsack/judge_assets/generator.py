"""随机测试生成器（应力测试用）。

用法：python generator.py <种子> <用例数>

覆盖小规模可暴力对拍用例与接近上限的用例（n = 28、b = 300）、
负收益物品、单色、多色、容量紧/松等结构。输出格式与 problem.md 一致。
"""
import random
import sys


def gen_case(rng: random.Random) -> tuple[int, int, list[tuple[int, int, int]]]:
    kind = rng.random()
    if kind < 0.35:
        # 小规模：供暴力对拍
        n = rng.randint(1, 12)
        b = rng.randint(0, 30)
    elif kind < 0.60:
        n = rng.randint(10, 20)
        b = rng.randint(1, 80)
    else:
        n = rng.randint(20, 28)
        b = rng.randint(1, 300)

    ncolors = rng.choice([1, 2, 3, rng.randint(1, min(n, 8))])
    style = rng.random()
    items = []
    for _ in range(n):
        c = rng.randrange(ncolors)
        if style < 0.15:
            # 大量负收益物品充当分隔符
            p = rng.randint(-30, 5)
        elif style < 0.30:
            # 全部非负
            p = rng.randint(0, 60)
        else:
            p = rng.randint(-20, 60)
        w = rng.randint(1, max(1, min(b, 50) if b > 0 else 1))
        items.append((w, p, c))
    rng.shuffle(items)
    return n, b, items


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    rng = random.Random(seed)
    print(cases)
    for _ in range(cases):
        n, b, items = gen_case(rng)
        print(n, b)
        for w, p, c in items:
            print(w, p, c)


if __name__ == "__main__":
    main()

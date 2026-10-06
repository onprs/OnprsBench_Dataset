"""参考解：二进制 Parikh 矩阵语言的普遍性指数。

闭式刻画见 reference/algorithm.md（对应来源论文 arXiv:2610.06717 的
定理 3.3 与定理 4.5）。从 stdin 读入题目格式的输入，逐用例输出存在指数
与全称指数。
"""
import sys
from math import isqrt


def exists_index(a: int, b: int, c: int) -> int:
    """最大的 k <= min(A,B)，使 k(k-1)/2 <= min(C, A*B-C)。"""
    m = min(c, a * b - c)
    k = isqrt(2 * m) + 1
    while k * (k - 1) // 2 > m:
        k -= 1
    return min(a, b, k)


def forall_index(a: int, b: int, c: int) -> int:
    """按论文定理 4.5 的分类计算全称指数。"""
    m = min(c, a * b - c)
    if a >= 3 and b >= 3 and m > max(a, b) and c % a != 0 and c % b != 0:
        return 3
    if a >= 2 and b >= 2 and m > 0:
        return 2
    if a >= 1 and b >= 1:
        return 1
    return 0


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    out = []
    idx = 1
    for _ in range(t):
        a = int(data[idx])
        b = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        out.append(f"{exists_index(a, b, c)} {forall_index(a, b, c)}")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

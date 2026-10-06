"""2268E 暴力求解器（对拍基准）。

枚举所有中序遍历为 1..n 的二叉树（Catalan 枚举），对每棵树按定义累加：
断开每条边后两侧 XOR 之和（整数加法），最后对所有树求和取模。
仅用于小规模应力测试。
"""
import sys

MOD = 998244353


def solve(a: list[int]) -> int:
    n = len(a)
    total_xor = 0
    for v in a:
        total_xor ^= v

    def enumerate_trees(l: int, r: int):
        """产出 (子树 XOR, 子树内部所有边的贡献之和, 子树是否为空)。"""
        if l > r:
            yield 0, 0, True
            return
        for root in range(l, r + 1):
            for lx, lc, lemp in enumerate_trees(l, root - 1):
                for rx, rc, remp in enumerate_trees(root + 1, r):
                    x = a[root - 1] ^ lx ^ rx
                    inner = lc + rc
                    if not lemp:
                        inner += lx + (total_xor ^ lx)
                    if not remp:
                        inner += rx + (total_xor ^ rx)
                    yield x, inner, False

    answer = 0
    for _, contribution, _ in enumerate_trees(1, n):
        answer = (answer + contribution) % MOD
    return answer


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx: idx + n]]; idx += n
        out.append(str(solve(a)))
    print("\n".join(out))


if __name__ == "__main__":
    main()

"""2269C 暴力求解器（对拍基准）。

直接在操作序列状态空间上搜索：每步删除左起第 k 个或右起第 k 个元素，
用记忆化搜索枚举全部决策。仅用于小规模应力测试。
从 stdin 读入与题目一致的输入，输出每个测试用例的最大得分（每行一个）。
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def max_score(arr: tuple, k: int) -> int:
    @lru_cache(maxsize=None)
    def dp(state: tuple) -> int:
        m = len(state)
        if m < k:
            return 0
        # 删除左起第 k 个
        left = state[: k - 1] + state[k:]
        # 删除右起第 k 个
        right = state[: m - k] + state[m - k + 1:]
        return max(state[k - 1] + dp(left), state[m - k] + dp(right))

    return dp(tuple(arr))


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, k = int(data[idx]), int(data[idx + 1]); idx += 2
        a = [int(x) for x in data[idx: idx + n]]; idx += n
        out.append(str(max_score(tuple(a), k)))
    print("\n".join(out))


if __name__ == "__main__":
    main()

"""暴力求解器（对拍基准）。

枚举全部排列求最小总费用。仅用于 n <= 8 的小规模用例。
从 stdin 读入题目格式输入，每行输出一个最优费用。
"""
import sys
from itertools import permutations


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        if n > 8:
            raise SystemExit("暴力解法仅支持 n <= 8 的用例")
        c = []
        for _ in range(n):
            row = [int(x) for x in data[idx:idx + n]]
            idx += n
            c.append(row)
        best = min(sum(c[i][perm[i]] for i in range(n)) for perm in permutations(range(n)))
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

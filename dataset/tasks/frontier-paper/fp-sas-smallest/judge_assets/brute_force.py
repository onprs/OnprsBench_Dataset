"""暴力求解器（对拍基准）。

按定义枚举长度 1,2,... 的全部词（字典序），返回第一个不出现在 S 中的词。
仅用于小字母表、小规模用例。从 stdin 读入题目格式输入，输出每行一个缺失词。
"""
import sys
from itertools import product


def smallest_absent(s: str, sigma: int) -> str:
    letters = [chr(ord('a') + i) for i in range(sigma)]
    length = 0
    while True:
        length += 1
        for tup in product(letters, repeat=length):
            w = ''.join(tup)
            if w not in s:
                return w


def main() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        n = int(data[idx]); sigma = int(data[idx + 1]); idx += 2
        s = data[idx].decode(); idx += 1
        if n > 600 or sigma > 4:
            raise SystemExit("暴力解法仅支持 n <= 600 且 sigma <= 4 的用例")
        out.append(smallest_absent(s, sigma))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

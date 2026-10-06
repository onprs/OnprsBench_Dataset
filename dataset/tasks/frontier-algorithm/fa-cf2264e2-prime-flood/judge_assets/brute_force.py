"""2264E1 暴力求解器（对拍基准）。

按定义枚举所有非空子序列（下标掩码），对每个子序列用状态搜索求
f(b)：选择质数 p，把所有能被 p 整除的元素同时减 1，问所有元素相等的
最大可达值。子序列按掩码计数（下标不同即不同），求和取模。
仅用于小规模应力测试。
"""
import sys
from math import isqrt

MOD = 998244353


def primes_upto(n: int) -> list[int]:
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
    return [i for i in range(2, n + 1) if sieve[i]]


def max_equal_value(values: list[int]) -> int:
    primes = primes_upto(max(values))
    start = tuple(sorted(values))
    seen = {start}
    stack = [start]
    best = -1
    while stack:
        state = stack.pop()
        if state[0] == state[-1]:
            best = max(best, state[0])
            continue
        for p in primes:
            nxt = tuple(sorted(x - 1 if x % p == 0 else x for x in state))
            if nxt != state and nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return best


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx: idx + n]]; idx += n
        total = 0
        for mask in range(1, 1 << n):
            chosen = [a[i] for i in range(n) if mask >> i & 1]
            total = (total + max_equal_value(chosen)) % MOD
        out.append(str(total))
    print("\n".join(out))


if __name__ == "__main__":
    main()

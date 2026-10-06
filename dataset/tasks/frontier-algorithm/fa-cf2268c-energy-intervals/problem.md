# KiaKio and Energy Intervals

> 来源：Codeforces Round 1124 (Div. 1) Problem C（2026-09-26），https://codeforces.com/contest/2268/problem/C
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：2 秒 / 256 MB；rating 2300。

## 题面

Kia and Kio found a glowing array $a_1, a_2, \ldots, a_n$ inside a crystal terminal in the ruins of an ancient digital kingdom.

The terminal works like this. Kia picks a segment of the array: any two indices $l$ and $r$ with $l \lt r$ (so the segment always has at least two elements). Kio then finds the strongest energy in that segment, $m = \max\left(a_l, a_{l+1}, \ldots, a_r\right)$, and the terminal masks every element of the segment with $m$ (bitwise AND), then fuses the results together (bitwise XOR):

$$ (a_l \,\&\, m)\oplus(a_{l+1} \,\&\, m)\oplus\cdots\oplus(a_r \,\&\, m). $$

That number is the energy released.

Kia wants the strongest possible blast. Over all valid segments $(l, r)$, what is the largest energy the terminal can produce?

Here, $\&$ denotes the bitwise AND operation, and $\oplus$ denotes the bitwise XOR operation.

## 输入

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows.

The first line of each test case contains a single integer $n$ ($2 \le n \le 2\cdot10^5$) — the size of the array.

The second line contains $n$ integers $a_1,a_2,\ldots,a_n$ ($0 \le a_i \lt 2^{18}$).

It is guaranteed that the sum of $n$ over all test cases does not exceed $2\cdot10^5$.

## 输出

For each test case, print a single integer — the maximum possible value of

$$ (a_l \,\&\, m)\oplus(a_{l+1} \,\&\, m)\oplus\cdots\oplus(a_r \,\&\, m) $$

among all pairs $(l,r)$ satisfying $l \lt r$.

## 样例

输入：

```text
4
5
1 7 3 7 2
3
3 1 2
5
1 5 2 3 4
4
3 5 2 6
```

输出：

```text
6
2
5
5
```

# A Prime Flood (Hard Version)

> 来源：Codeforces Round 1121 (Div. 2) Problem E2（2026-09-13），https://codeforces.com/contest/2264/problem/E2
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：3 秒 / 256 MB；rating 2700。

## 题面

This is the Hard version of the problem. The difference between the versions is that in this version, $n \le 3\cdot 10^5$. You can hack only if you solved all versions of this problem.

Antigun and Lamus have flooded Madamant's house. She wants them to make the water levels equal while removing as little water as possible.

Formally, the initial water levels are given by an array $a = [a_1, a_2, \ldots, a_n]$. For each hypothetical cleanup, Antigun and Lamus select a non-empty subsequence$^{\text{∗}}$ $b$ of $a$. They may perform the following operation on $b$ any number of times, possibly zero:

- choose a prime number $p$;
- simultaneously decrease every element $b_i$ whose current value is divisible by $p$ by $1$. All other elements remain unchanged.

Let $f(b)$ be the maximum integer $x$ such that, after some sequence of operations, every element of $b$ is equal to $x$.

Find the sum of $f(b)$ over all non-empty subsequences $b$ of $a$, modulo $998\,244\,353$. Subsequences formed by different choices of indices are counted separately, even if their values are equal.

Each subsequence is considered independently, starting from its original values.

$^{\text{∗}}$A sequence $a$ is a subsequence of a sequence $b$ if $a$ can be obtained from $b$ by the deletion of several (possibly, zero or all) elements from arbitrary positions.

## 输入

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows.

The first line of each test case contains a single integer $n$ ($1 \le n \le 300\,000$) — the length of the array $a$.

The second line contains $n$ integers $a_1, a_2, \ldots, a_n$ ($1 \le a_i \le n$) — the elements of $a$.

It is guaranteed that the sum of $n$ over all test cases does not exceed $300\,000$.

## 输出

For each test case, print one integer — the sum of $f(b)$ over all non-empty subsequences $b$ of $a$, modulo $998\,244\,353$.

## 样例

输入：

```text
4
1
1
4
2 4 4 4
4
2 3 4 4
6
3 6 1 1 1 1
```

输出：

```text
1
37
34
72
```

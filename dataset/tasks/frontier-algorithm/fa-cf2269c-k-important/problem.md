# K Is Important

> 来源：Codeforces Round 1124 (Div. 2) Problem C（2026-09-26），https://codeforces.com/contest/2269/problem/C
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：2 秒 / 256 MB；rating 1200。

## 题面

You are given an array $a$ consisting of $n$ positive integers, as well as an integer parameter $k$.

While the array has at least $k$ elements, you need to perform one of the following two types of operations on $a$:

- Remove $a_k$ and add its value to your score, or
- Remove $a_{m-k+1}$ and add its value to your score, where $m$ is the length of $a$ before this operation.

After removing an element, the remaining elements keep their relative order.

Your task is to determine the maximum possible score that can be obtained.

## 输入

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows.

The first line of each test case contains two integers $n$ and $k$ ($1 \le k \le n \le 10^5$) — the length of $a$ and the parameter.

The second line contains $n$ integers $a_i$ ($1 \le a_i \le 10^9$) — the elements of $a$.

It is guaranteed that the sum of $n$ over all test cases does not exceed $10^5$.

## 输出

For each test case, output a single integer — the maximum score that can be obtained.

## 样例

输入：

```text
4
4 2
1 2 3 4
4 4
3 4 1 2
1 1
1
6 3
1 4 8 2 6 3
```

输出：

```text
9
3
1
19
```

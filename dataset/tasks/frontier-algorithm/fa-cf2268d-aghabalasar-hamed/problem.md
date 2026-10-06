# AghaBalaSar and Hamed

> 来源：Codeforces Round 1124 (Div. 1) Problem D（2026-09-26），https://codeforces.com/contest/2268/problem/D
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：2 秒 / 256 MB；rating 2600。

## 题面

You are given a permutation$^{\text{∗}}$ $p$ of length $n$.

For each index $i$, you may move in one step to:

- any index $j \lt i$, or
- the first index $j \gt i$ such that $p_j \gt p_i$ (if such an index exists),

In other words:

- You can always move to any position on the left.
- On the right, you can move only to the nearest position whose value is strictly greater than the current one.

For every pair of indices $(i,j)$, let $f(i,j)$ be the minimum number of steps needed to move from $i$ to $j$. Note that if we cannot reach $j$ from $i$, then $f(i,j)=0$. Your task is to compute:

$$\sum_{1 \le i,j \le n} f(i,j).$$

$^{\text{∗}}$A permutation of length $n$ is an array consisting of $n$ distinct integers from $1$ to $n$ in arbitrary order. For example, $[2,3,1,5,4]$ is a permutation, but $[1,2,2]$ is not a permutation ($2$ appears twice in the array), and $[1,3,4]$ is also not a permutation ($n=3$ but there is $4$ in the array).

## 输入

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows.

The first line of each test case contains a single integer $n$ ($1 \leq n \leq 10^6$) — the length of $p$.

The second line of each test case contains $n$ distinct integers $p_1,p_2,\ldots,p_n$ ($1\le p_i\le n$) — the elements of $p$.

It is guaranteed that the sum of $n$ over all test cases does not exceed $10^6$.

## 输出

For each test case, print a single integer — the value of $\sum\limits_{1 \le i,j \le n} f(i,j)$.

## 样例

输入：

```text
6
2
1 2
2
2 1
3
1 3 2
3
1 2 3
5
1 3 5 2 4
7
6 2 4 3 7 5 1
```

输出：

```text
2
1
4
7
15
38
```

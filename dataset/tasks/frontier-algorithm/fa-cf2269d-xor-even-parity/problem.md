# What a SauSaGe! It's All Meat

> 来源：Codeforces Round 1124 (Div. 2) Problem D（2026-09-26），https://codeforces.com/contest/2269/problem/D
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：2 秒 / 256 MB；rating 1500。

## 题面

In SauSaGe City, there are $n$ different flavors of sausages. Reyhaneh, the Queen of SauSaGe City, keeps $a_i$ ($a_i < 16$) sausages of flavor $i$ in the royal warehouse.

Over time, the royal inventory undergoes $q$ updates. Each update is given in the form $(p, x)$, which means the number of sausages of flavor $p$ in the warehouse is changed to $x$ (i.e., $a_p := x$).

Reyhaneh can perform the following operation on the sausages any number of times (possibly zero):

- Choose an index $1 \leq i < n$ and an integer $1 \leq k \leq 5$, then replace $a_i$ and $a_{i+1}$ with $a_i \oplus (3 \cdot k)$ and $a_{i+1} \oplus (3 \cdot k)$, respectively, where $\oplus$ denotes the bitwise XOR.

In SauSaGe City, a sausage flavor is called **All-Meat** if its quantity is divisible by $3$. Three famous sausage critics — Shafi, Shafaghi, and Ghaffari — only like flavors that are All-Meat.

Before processing any updates, and after each of the $q$ updates, you need to answer the following question: If Reyhaneh performs an arbitrary number of operations optimally, what is the maximum possible number of sausage flavors that the three critics would like?

Note: The operations you perform to find the answer for each state are hypothetical and do not affect the array for subsequent queries. However, the $q$ inventory updates ($a_p := x$) are permanent.

## 输入

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows.

The first line of each test case contains two integers $n$ and $q$ ($2 \leq n \leq 2 \cdot 10^5$, $0 \leq q \leq 2 \cdot 10^5$) — the number of sausage flavors and the number of updates, respectively.

The second line contains $n$ integers $a_1, a_2, \ldots, a_n$ ($0 \leq a_i < 16$) — the initial numbers of sausages of each flavor.

Then $q$ lines follow, each containing two integers $p$ and $x$ ($1 \leq p \leq n$, $0 \leq x < 16$), meaning that $a_p$ is replaced with $x$.

It is guaranteed that the sum of $n$ and the sum of $q$ over all test cases each do not exceed $2 \cdot 10^5$.

## 输出

For each test case, output $q + 1$ integers. The first integer denotes the answer for the initial array. The next $q$ integers denote the answer for each update.

## 样例

输入：

```text
3
2 1
10 3
1 0
3 3
15 1 5
3 0
1 10
2 0
4 0
1 2 3 4
```

输出：

```text
2 2
2 2 2 3
1
```

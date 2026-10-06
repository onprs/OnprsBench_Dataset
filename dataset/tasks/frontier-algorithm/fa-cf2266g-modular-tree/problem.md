# Modular Tree

> 来源：Codeforces Round 1122 (Div. 3) Problem G（2026-09-21），https://codeforces.com/contest/2266/problem/G
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：3 秒 / 256 MB；rating 2200。

## 题面

Vihaan has a rooted tree$^{\text{∗}}$ with $n$ nodes. The tree is rooted at node $1$.

Each node $i$ has an initial value $a_i$ and a modulus $b_i$. Let $x_i$ denote the current value of node $i$. Initially, $x_i=a_i$.

Vihaan may perform the following operation any number of times:

- Choose a node $u$. Let $s$ be the sum of the current values of all direct children of $u$, then replace $x_u$ with $(x_u+s)\bmod b_u$.

After performing any number of operations, Vihaan wants to maximize the sum of the values of all nodes.

Determine the maximum possible sum.

$^{\text{∗}}$A tree is an undirected connected graph in which there are no cycles.

## 输入

The first line contains an integer $t$ ($1 \le t \le 10^4$) — the number of test cases.

The first line of each test case contains an integer $n$ ($1 \le n \le 2 \cdot 10^5$) — the number of nodes in the tree.

The second line contains $n$ integers $a_1,a_2,\ldots,a_n$ ($0 \le a_i \lt b_i$) — the initial values of the nodes.

The third line contains $n$ integers $b_1,b_2,\ldots,b_n$ ($1 \le b_i \le 10^9$) — the moduli of the nodes.

Each of the next $n-1$ lines contains two integers $u$ and $v$ ($1 \le u,v \le n$) — an edge between nodes $u$ and $v$.

It is guaranteed that the given edges form a tree.

It is guaranteed that the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$.

## 输出

For each test case, print one integer — the maximum possible sum of the values of all nodes after performing any number of operations.

## 样例

输入：

```text
8
1
3
7
2
0 3
5 4
1 2
3
0 2 3
7 3 4
1 2
2 3
3
0 0 1
5 2 2
1 2
2 3
4
1 2 3 4
10 3 4 5
1 2
1 3
1 4
3
0 1 3
10 2 4
1 2
1 3
5
0 0 1 2 3
12 6 9 3 4
1 2
1 3
2 4
3 5
4
0 999999999 999999999 999999999
1000000000 1000000000 1000000000 1000000000
1 2
1 3
1 4
```

输出：

```text
3
7
11
6
18
12
27
3999999996
```

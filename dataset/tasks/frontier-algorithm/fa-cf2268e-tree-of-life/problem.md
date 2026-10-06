# Kia Kio and Tree of Life

> 来源：Codeforces Round 1124 (Div. 1) Problem E（2026-09-26），https://codeforces.com/contest/2268/problem/E
> 权利归 Codeforces 与原作者所有；按研究基准惯例收录并署名（见 LICENSING.md "research_archive"）。
> 限制：3 秒 / 256 MB；rating 2700。

## 题面

After unlocking the crystal terminal, Kia and Kio discovered the blueprint for the kingdom's forgotten heart: a digital Tree of Life, seeded by the array $a_1, a_2, \ldots, a_n$.

To restore its pulse, they had to weave every possible incarnation of the Tree together. For any continuous segment, Kia would gently select an index $i$ to plant the root. Trusting her vision, Kio would carefully weave the branches of life — crafting the left subtree from the preceding segment $[1, i-1]$ and the right subtree from the succeeding segment $[i+1, n]$.

Once a Tree of Life bloomed, its vital resonance, $f(\text{tree})$, was defined by its bonds. If one were to sever any of the $n-1$ delicate branches, the Tree would split into two disconnected halves, releasing an energy of $X+Y$, where $X$ and $Y$ are the bitwise XOR sums of the array elements remaining in the first and second halves, respectively.

The total power of the Tree, $f(\text{tree})$, is the sum of these released energies across all $n-1$ branches.

Kia wanted to know the ultimate vital force they could awaken. Help them compute the total sum of $f(\text{tree})$ across every valid Tree of Life born from their shared bond, modulo $998\,244\,353$.

## 输入

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows.

The first line of each test case contains a single integer $n$ ($1 \le n \le 2\cdot10^5$) — the size of the array.

The second line contains $n$ integers $a_1,a_2,\ldots,a_n$ ($0 \le a_i \lt 2^{18}$).

It is guaranteed that the sum of $n$ over all test cases does not exceed $2\cdot10^5$.

## 输出

For each test case, print a single integer — the total sum of $f(\text{tree})$ across all valid Trees of Life, modulo $998\,244\,353$.

## 样例

输入：

```text
5
2
1 2
3
1 1 1
3
1 2 3
4
2 1 4 7
5
5 12 9 14 1
```

输出：

```text
6
10
40
318
2520
```

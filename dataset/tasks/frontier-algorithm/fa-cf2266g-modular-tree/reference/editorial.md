# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/156984 （2266G 小节）
> 题解：Codeforces Round 1122 (Div. 3) 官方题解（作者未单独标注）
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。


**Hint 1** —

Process the tree from the leaves upward.

**Hint 2** —

A node can always be brought back to its original value after changing it.

**Hint 3** —

For every node $i$, its reachable values have the form $(a_i+g_ix)\bmod b_i$ for some integer $x$. Find $g_i$.

## Solution

For every node $u$, let $g_u$ be such that its reachable values are exactly $(a_u+g_ux)\bmod b_u$. We compute $g_u$ from the leaves upward.

Suppose $v$ is a child of $u$. If $g_v=b_v$, then $v$ is fixed at $a_v$. Otherwise, its value can change from $a_v$ by multiples of $g_v$. Let $S_u$ be the sum of the initial values of all direct children of $u$. We can add $S_u$ to $u$ by leaving all children at their initial values, and every non-fixed child $v$ lets us vary this amount by multiples of $g_v$. Therefore, $g_u=\gcd(b_u,S_u,g_v\text{ for all non-fixed children }v)$.

For a leaf, this gives $g_u=b_u$, as expected. Once we know $g_u$, the largest reachable value is $a_u+\left\lfloor\frac{b_u-1-a_u}{g_u}\right\rfloor g_u$.

These maxima can all be achieved together. We can first set a node to its maximum, then continue working strictly inside its children's subtrees without changing that node. So after computing all $g_u$ bottom-up, we simply sum the maximum reachable value of every node.

The complexity is $O(n\log 10^9)$ per test case.

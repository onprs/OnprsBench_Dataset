# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/157140 （2269C 小节）
> Idea / Preparation：eren__
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。

## Hints

**Hint 1** — Consider the special case where $2k = n$. Which elements are competing against each other to be deleted?

**Hint 2** — You can prove that for a specific index $i$, we are forced to delete exactly one element from the symmetric pair $(a_i, a_{n-i+1})$. Therefore, to maximize the sum, we should greedily take $\max(a_i, a_{n-i+1})$.

## Solution

We can analyze the problem by splitting it into two cases based on the relationship between $2k$ and $n$:

**Case 1: $2k \le n$**

The elements in the middle, where $k \le i \le n - k + 1$, are inevitably going to be deleted. No matter what sequence of operations we choose, these elements will eventually land on the $k$-th position from either the left or the right side. Thus, we unconditionally add all of them to our total sum.

After removing the middle section, we are left with a prefix of length $k-1$ and a suffix of length $k-1$.

*Proof of the pairing relation:* Notice that when the remaining array shrinks to exactly length $k + i - 1$ (for $1 \le i \le k - 1$), the $k$-th element from the left and the $k$-th element from the right correspond exactly to the original elements $a_{n-i+1}$ and $a_i$ (or what remains of their relative positions). At this specific length, the operation forces us to delete exactly one of them.

Therefore, for each $1 \le i \le k - 1$, we must choose exactly one element from the pair $(a_i, a_{n-i+1})$. To maximize our score, we greedily add $\max(a_i, a_{n-i+1})$ to our answer.

**Case 2: $2k > n$**

This case is very similar, but the roles are inverted. The elements in the middle, where $n - k + 2 \le i \le k - 1$, are completely fixed and safe. The total length of the array will drop below $k$ before these elements can ever reach the $k$-th position from either boundary. Thus, they can never be deleted.

For the remaining valid elements on the two boundaries, the exact same symmetric relationship holds. We form pairs from the two ends: $(a_i, a_{n-i+1})$ for $1 \le i \le n - k + 1$. Just like in the first case, we can delete exactly one element from each pair, so we greedily add $\max(a_i, a_{n-i+1})$ to our sum.

Using two pointers (`l` and `r`) allows us to implement both cases cleanly in $\mathcal{O}(n)$.

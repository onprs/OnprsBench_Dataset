# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/157140 （2268E 小节）
> Idea：sweetweasel；Preparation：Hamed_Ghaffari and _R00T
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。


Idea: sweetweasel
Preparation: Hamed_Ghaffari and _R00T

## Hints

**Hint 1** —

The number of valid trees that can be constructed from a segment of length $m$ is the $m$-th Catalan number.

**Hint 2** —

The vertices inside every subtree form a continuous subarray. Fix a subarray of length $l$. In how many trees does it appear as the subtree below some edge?

**Answer**

Exactly $C_lC_{n-l}$, where $C_i$ is the $i$-th Catalan number.

**Hint 3** —

Consider every bit independently. If the XOR of the entire array has this bit set, exactly one of the two components created by cutting any edge has this bit set.

**Hint 4** —

Suppose the bit is not set in the XOR of the entire array. We need, for every length $l$, the number of subarrays of length $l$ whose XOR has this bit set.

**Hint 5** —

Let $p_i=a_1\oplus a_2\oplus\cdots\oplus a_i$. Encode the corresponding bit of each $p_i$ as either $1$ or $-1$. The number of pairs with different signs can be found from their autocorrelation.

**Hint 6** —

We only need a weighted sum of the autocorrelation values. Using Parseval's identity, this weighted sum can be calculated without performing an inverse NTT for every bit.

## Solution

Let $C_m$ be the $m$-th Catalan number:

$ C_m=\frac{1}{m+1}\binom{2m}{m}. $

The recursive construction in the statement generates exactly the binary trees whose inorder traversal is:

$ 1,2,\ldots,n. $

Therefore, there are $C_n$ valid trees.

Consider an edge between a parent and one of its children. The component containing the child after removing this edge is exactly the child's subtree. Since the inorder traversal is fixed, the vertices of this subtree form a continuous subarray.

Now fix a proper subarray $[L,R]$ of length $l$.

There are $C_l$ possible trees inside this subarray. After deleting this subtree, the remaining $n-l$ vertices can form any valid tree, giving $C_{n-l}$ possibilities.

The location of $[L,R]$ determines one gap in the inorder traversal of the remaining tree. This gap corresponds to a unique empty child position, so the chosen subtree can be attached there in exactly one way.

Therefore, a fixed subarray of length $l$ appears as the child subtree of an edge in exactly:

$ C_lC_{n-l} $

valid trees.

Let:

$ S=a_1\oplus a_2\oplus\cdots\oplus a_n. $

For a subarray $I$, let its XOR be $X_I$. Cutting the edge above this subtree produces two components with XOR values:

$ X_I \qquad\text{and}\qquad S\oplus X_I. $

Thus, the whole answer can be written as:

$ \sum_{\substack{I\text{ is a subarray}\\|I| \lt n}} C_{|I|}C_{n-|I|} \left(X_I+(S\oplus X_I)\right). $

We calculate this sum bit by bit.

Fix a bit $b$.

Case 1: Bit $b$ of $S$ is set.

At this bit, $X_I$ and $S\oplus X_I$ are different. Therefore, exactly one of the two components has this bit set for every tree and every edge.

There are $C_n$ trees, and every tree has $n-1$ edges. Hence, before multiplying by $2^b$, the contribution is:

$ (n-1)C_n. $

Case 2: Bit $b$ of $S$ is not set.

In this case, the two component XORs have the same value at bit $b$.

- If bit $b$ of $X_I$ is zero, the edge contributes zero.
- If bit $b$ of $X_I$ is one, both components contribute this bit, so the edge contributes twice.

For every length $l$, let $D_l$ be the number of subarrays of length $l$ whose XOR has bit $b$ set. The contribution of this bit is:

$ 2\sum_{l=1}^{n-1}D_lC_lC_{n-l}. $

It remains to calculate every $D_l$.

Define the prefix XORs:

$ p_0=0,\qquad p_i=a_1\oplus a_2\oplus\cdots\oplus a_i. $

The XOR of a subarray of length $l$ starting after position $i$ is:

$ p_i\oplus p_{i+l}. $

Define:

$ s_i= \begin{cases} 1,&\text{if bit }b\text{ of }p_i\text{ is zero},\\ -1,&\text{if bit }b\text{ of }p_i\text{ is one}. \end{cases} $

The required subarray has bit $b$ set exactly when $s_i$ and $s_{i+l}$ are different.

Consider:

$ R_l=\sum_{i=0}^{n-l}s_is_{i+l}. $

Equal pairs contribute $1$, while different pairs contribute $-1$. Since there are $n+1-l$ pairs in total:

$ R_l=(n+1-l)-2D_l. $

Therefore:

$ D_l=\frac{n+1-l-R_l}{2}. $

The values $R_l$ form the autocorrelation of the sequence $s$. After padding the sequence with enough zeros, let $F_k$ be its NTT. The NTT representation of the autocorrelation is:

$ P_k=F_kF_{-k}. $

With a transform of size $N$, the index $-k$ is represented by $(N-k)\bmod N$.

A direct implementation could perform an inverse NTT and obtain every $R_l$. However, we only need their weighted sum.

Let:

$ w_l=C_lC_{n-l} $

for $1\leq l \lt n$, and let $W_k$ be the NTT of $w$. Using Parseval's identity:

$ \sum_{l=1}^{n-1}w_lR_l = \frac{1}{N} \sum_{k=0}^{N-1}P_kW_{-k}. $

Also:

$ 2\sum_{l=1}^{n-1}D_lw_l = \sum_{l=1}^{n-1}(n+1-l)w_l - \sum_{l=1}^{n-1}R_lw_l. $

The first sum is independent of the bit and can be precomputed. The second sum is calculated using one forward NTT and Parseval's identity.

Therefore, we need one NTT for the weights and at most one NTT for each of the $18$ bits.

The total time complexity is:

$ \mathcal{O}(18n\log n), $

and the memory complexity is $\mathcal{O}(n)$.

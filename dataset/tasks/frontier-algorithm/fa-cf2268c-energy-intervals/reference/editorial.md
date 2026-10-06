# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/157140 （2268C 小节）
> Idea / Preparation：sweetweasel
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。


Idea: sweetweasel
Preparation: sweetweasel

## Hints

**Hint 1** —

Let:

$ p_0=0,\qquad p_i=a_1\oplus a_2\oplus\cdots\oplus a_i. $

If $m=\max(a_l,a_{l+1},\ldots,a_r)$, show that the value of the interval is:

$ (p_{l-1}\oplus p_r)\mathbin{\&}m. $

**Hint 2** —

Build the maximum Cartesian tree of the original array.

What is the relation between $\operatorname{LCA}(l,r)$ and the maximum element of $a_l,a_{l+1},\ldots,a_r$?

**Hint 3** —

Construct the answer greedily from the highest bit to the lowest bit.

For a candidate mask $M$, we only need to determine whether there exists an interval whose value contains every bit of $M$.

**Hint 4** —

For a fixed candidate $M$, define:

$ b_i=a_i\mathbin{\&}M $

and let $s_i$ be the prefix XOR of $b$.

An interval represented by a Cartesian-tree vertex $v$ is valid for $M$ if:

$ (a_v\mathbin{\&}M)=M $

and:

$ s_{l-1}\oplus s_r=M. $

**Hint 5** —

Suppose the subtree of $v$ represents the segment $[L,R]$.

For an interval whose Cartesian-tree LCA is $v$, its two prefix endpoints satisfy:

$ l-1\in[L-1,v-1],\qquad r\in[v,R]. $

Be careful with the pair $(v-1,v)$: it represents the forbidden one-element interval $[v,v]$.

**Hint 6** —

Process the smaller child first, remove its prefix XORs from the frequency array, and then process the larger child.

Keep the larger side in the frequency array, iterate over the smaller side, and search for the required complementary prefix XOR.

## Solution

Define the prefix XORs of the original array as:

$ p_0=0,\qquad p_i=a_1\oplus a_2\oplus\cdots\oplus a_i. $

Suppose we choose an interval $[l,r]$, and let:

$ m=\max(a_l,a_{l+1},\ldots,a_r). $

Bitwise AND distributes over XOR, so:

$ \begin{aligned} &(a_l\mathbin{\&}m)\oplus (a_{l+1}\mathbin{\&}m)\oplus\cdots\oplus (a_r\mathbin{\&}m)\\ &= (a_l\oplus a_{l+1}\oplus\cdots\oplus a_r) \mathbin{\&}m\\ &= (p_{l-1}\oplus p_r)\mathbin{\&}m. \end{aligned} $

Therefore, the answer depends only on the XOR of two prefix endpoints and the maximum of the interval.

Cartesian tree

Build the maximum Cartesian tree of the original array $a$. Ties may be handled in any consistent way.

This tree has two useful properties:

- The subtree of every vertex $v$ corresponds to a continuous segment $[L_v,R_v]$.
- For every interval $[l,r]$:

$ a_{\operatorname{LCA}(l,r)} = \max(a_l,a_{l+1},\ldots,a_r). $

Thus, if $v=\operatorname{LCA}(l,r)$, the value of the interval is:

$ (p_{l-1}\oplus p_r)\mathbin{\&}a_v. $

Constructing the answer bit by bit

Suppose some higher bits of the answer have already been fixed, and we want to test a candidate mask $M$.

The candidate is feasible if there exists an interval whose value contains every bit of $M$.

For this check, define:

$ b_i=a_i\mathbin{\&}M $

and its prefix XORs:

$ s_0=0,\qquad s_i=b_1\oplus b_2\oplus\cdots\oplus b_i. $

Equivalently:

$ s_i=p_i\mathbin{\&}M. $

For an interval whose Cartesian-tree LCA is $v$, all bits of $M$ occur in its value if and only if:

$ (a_v\mathbin{\&}M)=M $

and:

$ s_{l-1}\oplus s_r=M. $

The second condition can be rewritten as:

$ s_r=s_{l-1}\oplus M. $

Therefore, after fixing one endpoint, we only need a frequency array to determine whether the required other endpoint exists.

Notice that the Cartesian tree is always built from the original values. Only the prefix XORs are masked during a feasibility check.

Processing one Cartesian-tree vertex

Suppose the subtree of $v$ corresponds to $[L,R]$.

Every interval whose LCA is exactly $v$ can be represented by two prefix endpoints:

$ x=l-1\in[L-1,v-1], $

$ y=r\in[v,R]. $

We need to find a pair satisfying:

$ s_x\oplus s_y=M. $

There is one important exception. The pair:

$ (x,y)=(v-1,v) $

represents the interval $[v,v]$, which is forbidden because the statement requires $l \lt r$.

Moreover, whenever $a_v & M=M$, this pair automatically satisfies:

$ s_{v-1}\oplus s_v=a_v\mathbin{\&}M=M. $

So failing to exclude this exact pair would produce a false positive at every suitable vertex.

Small-to-large traversal

For every processed subtree $[L,R]$, we maintain the following invariant:

The frequency array contains $s_L,s_{L+1},\ldots,s_R$.

At a vertex $v$:

- Recursively check both child subtrees.
- Keep the prefix XORs of the larger child in the frequency array.
- Iterate over the endpoints belonging to the smaller side.
- For every value $s_x$, check whether $s_x\oplus M$ exists on the other side.
- Merge the smaller side into the frequency array.

The boundary prefix $s_{L-1}$ is inserted temporarily when needed.

The pair $(v-1,v)$ is excluded by checking one boundary endpoint before inserting the other one. Since the frequency array stores counts rather than only presence, equal prefix XOR values at different indices are still handled correctly.

Whenever an index is scanned as part of the smaller side, the size of the subtree containing it at least doubles before it can be scanned again. Hence, every index is scanned at most $\mathcal{O}(\log n)$ times.

One feasibility check takes:

$ \mathcal{O}(n\log n). $

There are $18$ bits, so the total time complexity is:

$ \mathcal{O}(18n\log n). $

The memory complexity is:

$ \mathcal{O}(n+2^{18}). $

The implementation below uses an explicit stack because a Cartesian tree can have depth $n$ for a sorted array.

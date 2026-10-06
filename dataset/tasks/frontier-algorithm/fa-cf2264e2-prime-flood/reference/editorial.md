# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/156680 （2264E2 小节）
> Problem by qwexd；Hard Version 由 jeroenodb 求解
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。


Problem by qwexd and solved for bigger constraints by jeroenodb.

**Hint 1** —

Let $dp[x][y]$ be the answer for minimum $x$ and maximum $y$. E1 builds and sums over every pair. Fix $x$ and scan larger values of $y$. When can $dp[x][y]$ differ from $dp[x][y-1]$?

**Hint 2** —

Let $r(y)$ be the product of the distinct prime divisors of $y$. The row for $x$ can change only at positions where $r(y)\mid x$. Generate these positions by fixing $y$ and visiting the smaller multiples of $r(y)$.

**Hint 3** —

For fixed $x$, separate the number of subsequences with endpoints $(x,y)$ into an $x$-only factor and a $y$-only factor. Prefix sums of the $y$-only factors can add a whole constant part of the row at once.

## Solution

The easy solution builds the full DP table and then loops over every minimum and maximum. We need to compress both quadratic parts.

Let $r(y)$ be the product of the distinct prime divisors of $y$. The transition from E1 is

$ dp[x][y]= \begin{cases} dp[x-1][y-1],&r(y)\mid x,\\ dp[x][y-1],&r(y)\nmid x. \end{cases} $

Fix $x$ and read the row from left to right. Unless $r(y)$ divides $x$, the value is copied from the previous position. Thus, the row can change only at positions satisfying $r(y)\mid x$; call them blockers.

For example, the blockers of row $2$ are $4,8,16,\ldots$. At $y=4$, the row changes from $2$ to $dp[1][3]=1$. Every later blocker also reads $1$ from row $1$, so the whole row is stored as only $(2,2)$ and $(4,1)$.

We can generate all blockers without checking every pair. For each $y$, visit

$ x=r(y),2r(y),3r(y),\ldots\qquad(x \lt y) $

and add $y$ to the blocker list of each visited $x$. Processing $y$ in increasing order keeps every list sorted.

Now build the rows in increasing order of $x$. Store a row as breakpoints $(s,z)$: its value becomes $z$ starting at position $s$. Begin row $x$ with $(x,x)$. At a blocker $y$, advance a pointer in row $x-1$ while the next breakpoint starts at or before $y-1$. Its current value is $dp[x-1][y-1]$. Add a new breakpoint only when this value differs from the previous one.

For the fixed limit $M=300\,000$, generating the blocker lists visits $5\,970\,168$ pairs. Unfortunately, a bound on the number of generated pairs is not easy to calculate for general $n$, so the best way to solve the problem in-contest is to experimentally verify that the number of pairs is small enough for the given $n$. After equal neighboring parts are merged, all rows together contain $640\,704$ breakpoints, and no row contains more than eight.

We still need to avoid iterating over every pair of endpoints. Let $c_v$ be the frequency of $v$, and write

$ C_v=2^{c_v}-1,\qquad S(v)=\sum\limits_{u\le v}c_u. $

For $x \lt y$, the number of subsequences with minimum $x$ and maximum $y$ is

$ C_xC_y2^{S(y-1)-S(x)} =\left(C_x2^{-S(x)}\right) \left(C_y2^{S(y-1)}\right). $

Call the two factors $L_x$ and $R_y$. Build prefix sums of $R_y$. Intersect each compressed part with $x \lt y\le n$. If the remaining interval is $u\le y\le v$ and the row value there is $z$, its whole contribution is

$ L_xz\sum\limits_{y=u}^{v}R_y, $

which is one prefix-sum query. Skip values with $c_x=0$. The case $x=y$ contributes $xC_x$ separately.

The radical sieve takes $O(M\log\log M)$ time. The remaining preprocessing is linear in the $5\,970\,168$ generated pairs and $640\,704$ stored breakpoints. Afterward, each present minimum scans at most eight parts, so the additional work is virtually linear in the total input size. The blocker lists and compressed rows have the sizes given above; together with the $O(M)$ arrays, they fit comfortably in memory.

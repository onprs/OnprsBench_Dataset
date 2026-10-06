# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/157140 （2268D 小节）
> Idea / Preparation：Hamed_Ghaffari
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。


Idea: Hamed_Ghaffari
Preparation: Hamed_Ghaffari

**What is AghaBalaSar?**

AghaBalaSar (آقابالاسر) is a term commonly used in the Iranian CP community for the nearest greater/smaller element on either side.

I also used it in a previous contest as well :D 2127F - Hamed and AghaBalaSar

## Hints

**Hint 1** —

For a fixed $i$, try to describe the shape of a shortest path. In particular, how many times do we really need to move left?

**Hint 2** —

For a fixed $i$, what can we say about the positions $j$ whose $f(i, j)$ are $1$, $2$, or greater than $2$?

## Solution

The important observation is that a shortest path has the form

$L,R,R,\ldots,R,L$

So after at most one initial left move, all right moves are forced.

Let $R_i=\text{the first }j \gt i\text{ such that }p_j \gt p_i$ or $n+1$ if it does not exist.

We split the permutation into blocks ending at positions $r$ with $R_r=n+1$, because we cannot move from one block to any of the blocks to its right.

Let $dp_i$ be the sum of distances from $i$ to all positions in the current block.

Let $x$ be the rightmost position reachable from $i$ in at most two moves.

There are two cases.

Case 1: ($x=R[i]$)

Then there is no way to reach anything beyond $R_i$ in two moves.

Therefore, for every $j \gt R_i$, every shortest path starts with $i\to R_i$, hence $f(i,j)=1+f(R_i,j)$.

Now compare the contributions of $i$ and $R_i$.

- For $j \lt i$, both distances are $1$.
- For $j=i$, we gain $-1$.
- For $j \gt i$, the distance from (i) is exactly one larger than the corresponding distance from $R_i$.

The total difference simplifies to $dp_i-dp_{R_i}=r-i-1$. Thus

$dp_i=dp_{R_i}+r-i-1$

Where $r$ is the end of the current block.

Case 2: ($x \gt R_i$)

Now $x$ is reachable in two moves, and $x$ is the furthest position with this property.

For every $j \gt x$, $f(i,j)=2+f(x,j)$.

Why? We can reach $x$ in two moves and then follow an optimal path from $x$. Also, by definition of $x$, no position farther right can be reached from $i$ in two moves, so we cannot do better.

Thus, for everything after $x$, we can simply use $dp_x$.

It remains to handle the positions between $i$ and $x$.

Since $x$ is reachable in at most two moves, every position $j\in(i,x]$ has distance either $2$ or $3$ from $i$.

Let $c_2$ be the number of $j \in (i,x]$ such that $f(i,j)=2$.

There are $x-i-1$ positions strictly between $i$ and $x$. Among them, $c_2-1$ have distance $2$, because $x$ itself is also counted by $c_2$. Therefore the remaining $x-i-c_2$ positions have distance $3$. Comparing their contributions with $dp_x$, we get

$dp_i=dp_x+2(r-i)-2-c_2$

So the only remaining problem is computing $x$ and $c_2$ efficiently.

Finding the positions reachable in two moves

A position $j \gt i$ can be reached in two moves in exactly these ways:

- $i \lt j \lt R_i$, by $i\to R_i\to j$;
- $j=R_{R_i}$;
- There is some $k\le i$ such that $R_k=j$, because we can do $i\to k\to j$.

Let $L_j$ be the minimum $k$ such that $R_k = j$, then third case is simply $L_j\le i$.

We process $i$ from right to left and maintain all positions $j$ satisfying $L_j\le i$. The rightmost marked position is exactly $x$.

Computing $c_2$

Among the distance-$2$ positions we have:

- $R_i-i-1$ positions between $i$ and $R_i$;
- $R_{R_i}$, if it exists;
- all currently marked positions except $R_i$.

There is one possible double count: $R_{R_i}$ may itself already be marked.

So we can compute $c_2$ by processing $i$ from right to left and maintaining all marked positions.

Complexity: $\mathcal{O}(n)$

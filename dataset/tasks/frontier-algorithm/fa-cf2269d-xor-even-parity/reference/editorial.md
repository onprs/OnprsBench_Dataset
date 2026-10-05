# 官方题解（原文归档）

> 来源：https://codeforces.com/blog/entry/157140 （2269D 小节）
> Idea / Preparation：_R00T
> 权利归 Codeforces 与作者所有；按研究基准惯例收录并署名（LICENSING.md "research_archive"）。
> 官方参考代码见 `../judge_assets/reference_solution.cpp`；判题以程序 verifier 为准。

## Hints

**Hint 1** — Write all possible values of $3k$ in binary. What property of each $a_i$ is preserved after every operation?

**Hint 2** — Show that instead of two adjacent elements, we can apply the same XOR mask to any pair $a_i, a_j$.

**Hint 3** — By combining several operations, we can XOR two chosen elements by any four-bit number with an even number of set bits.

**Hint 4** — An element with an odd number of set bits can never become All-Meat. To prove that every other element can become All-Meat, consider these two cases separately: (1) there is an element with odd popcount; (2) all elements have even popcount.

## Solution

The possible XOR masks in one operation are $3, 6, 9, 12, 15$; in binary: $0011, 0110, 1001, 1100, 1111$. All these masks have an even number of set bits. XORing a number with such a mask flips an even number of its bits, so the parity of its popcount does not change.

The All-Meat values smaller than $16$ are $0, 3, 6, 9, 12, 15$; in binary: $0000, 0011, 0110, 1001, 1100, 1111$. They all have even popcount. Therefore, an element with odd popcount can never become All-Meat. This gives the upper bound:

$$\text{answer} \leq \#\{i \mid \operatorname{popcount}(a_i)\text{ is even}\}.$$

Now we prove that this upper bound can always be achieved.

First, we can apply the same mask to any two elements, not necessarily adjacent ones. Suppose we want to apply a mask to $a_i$ and $a_j$ ($i < j$): apply it to every adjacent pair $(i,i+1), (i+1,i+2), \ldots, (j-1,j)$. Every element strictly between $i$ and $j$ is XORed twice, so it remains unchanged. Only $a_i$ and $a_j$ are XORed once.

We can also combine multiple operations on the same pair. The set of all four-bit values with even popcount is $E = \{0, 3, 5, 6, 9, 10, 12, 15\}$. All of them are already valid masks except $5$ and $10$, and $5 = 3 \oplus 6$, $10 = 3 \oplus 9$. Thus, we can XOR any two chosen elements by any mask with even popcount.

Equivalently, if we write the array as an $n \times 4$ grid of bits, we may choose any two rows and any two columns and flip the four corner bits.

**Case 1: There is an element with odd popcount.** Choose one such element as a buffer. For every element $a_i$ with even popcount, XOR both $a_i$ and the buffer by $a_i$ (possible because $a_i$ itself has even popcount). After this operation $a_i \oplus a_i = 0$, so $a_i$ becomes All-Meat. The buffer still has odd popcount because we only XOR it with even-popcount masks. Therefore, every element with even popcount becomes All-Meat, while the elements with odd popcount cannot contribute to the answer anyway.

**Case 2: All elements have even popcount.** Use $a_1$ as a buffer. For every $2 \leq i \leq n$, XOR $a_1$ and $a_i$ by $a_i$. This makes every $a_i$ ($i \geq 2$) equal to zero. After these operations, the array has the form $[x, 0, 0, \ldots, 0]$, where $x = a_1 \oplus a_2 \oplus \cdots \oplus a_n$. Since all original elements have even popcount, $x$ also has even popcount. If $x \in \{0, 3, 6, 9, 12, 15\}$, every element is already All-Meat. The only remaining possibilities are $x = 5$ and $x = 10$; in both cases, apply XOR with $3$ to the first two elements: $(5, 0) \to (6, 3)$, $(10, 0) \to (9, 3)$. Again, every element becomes All-Meat.

Therefore, the upper bound is always achievable, and the answer is exactly $\#\{i \mid \operatorname{popcount}(a_i)\text{ is even}\}$. For each update, we only need to remove the contribution of the old value and add the contribution of the new value. The initial array is processed in $\mathcal{O}(n)$, and every update in $\mathcal{O}(1)$; total $\mathcal{O}(n + q)$.

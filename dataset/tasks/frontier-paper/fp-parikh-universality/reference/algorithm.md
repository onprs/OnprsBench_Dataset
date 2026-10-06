# 参考解与答案锚点

## 来源结论（锚点）

来源论文：*Subsequence Analysis Problems for Binary Parikh Matrices*（arXiv:2610.06717，2026-10-05）。

- **定理 3.3**：语言 $L(A,B,C)$ 是 $k$-$\exists$-universal 当且仅当 $A \ge k$、$B \ge k$、$C \ge \binom{k}{2}$ 且 $AB-C \ge \binom{k}{2}$。
- **命题 4.2**：非空 $L(A,B,C)$ 是 $2$-$\forall$-universal 当且仅当 $A,B \ge 2$ 且 $\min(C, AB-C) > 0$。
- **定理 4.4**：非空 $L(A,B,C)$ 是 $3$-$\forall$-universal 当且仅当 $A,B \ge 3$、$\min(C,AB-C) > \max(A,B)$、$A \nmid C$ 且 $B \nmid C$。
- **定理 4.5**：$\iota_{\forall}(L(A,B,C))$ 的完整分类（3 / 2 / 1 / 0 四档）。
- **引理 4.1**：非空 $L(A,B,C)$ 的全称指数至多为 3。

## 由结论得到的计算式

记 $m = \min(C,\ AB-C)$。

- **存在指数**：$\iota_{\exists} = \max\{\, k \le \min(A,B) : \frac{k(k-1)}{2} \le m \,\}$。因为 $\binom{k}{2}$ 关于 $k$ 单调，可直接解二次不等式 $k(k-1)/2 \le m$ 得到上界，再与 $\min(A,B)$ 取小。
- **全称指数**：按定理 4.5 依次判定：
  1. 若 $A,B \ge 3$、$m > \max(A,B)$、$A \nmid C$、$B \nmid C$，则为 3；
  2. 否则若 $A,B \ge 2$ 且 $m > 0$，则为 2；
  3. 否则若 $A,B \ge 1$，则为 1；
  4. 否则为 0。

参考实现 `judge_assets/reference_solution.py` 即按上述两式编写。

## 为什么答案不是 AI 自证

- 两个指数的闭式刻画来自论文中已发表、可复核的定理（编号如上），参考实现只是形式转换。
- 参考实现在 $A,B \in [0,8]$、$0 \le C \le AB$ 的全部 1377 组参数上与暴力枚举逐字比对一致；暴力枚举独立实现定义（枚举全部词、按 $|w|_{ab}$ 分组、计算 $\iota$）。
- 题目对输入大参数（$A,B \le 10^{18}$）的要求使枚举不可行，区分度来自是否正确落实闭式刻画。

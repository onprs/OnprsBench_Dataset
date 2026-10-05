# 参考修复分析（基于上游 PR #30530，已合并）

## 根因

`sympy/solvers/inequalities.py` 中两条路径的奇点处理不一致：

- `_solve_inequality(relational, s)` 在求解单条关系式时会识别分母零点并给出 `!= 0` 约束；
- `_reduce_inequalities`（`reduce_inequalities` 内部）先把关系式左右相减得到 `expr`，再送入 `_solve_inequality`。这一步相减可能把分母的零点约掉：`1/x <= 1/x` 相减后恒为 `0`，`x = 0` 的失效点消失，结果退化为 `True`。
- `reduce_rational_inequalities` 同样在归约前做相减，存在同样的丢失。

## 修复要点（上游实际做法）

1. `reduce_rational_inequalities` 直接接收完整的 `Relational`：在左右相减之前，检查分母多项式因子是否会在相减中丢失，并把它们作为 `!= 0` 条件保留；之后才归一为 `(expr, rel)` 交给既有有理不等式机器。
2. `_solve_inequality` 改为接收已归一的 `(expr, rel)` 元组；`reduce_abs_inequality` 内部生成的零相对条件也使用同一形态，避免重复求解。
3. 分母约束不再局限于"能解成生成元的单个值"的情形：`d = 0` 解不出单点时直接保留 `Ne(d, 0)`，从而支持 `sin(x)` 一类非多项式分母。
4. 把 `1/x <= 1/x` 这类"相减后为 0、`rv` 不为 `None`"的分支也纳入同一处理流程（原实现的约束块只在 `rv is None` 路径执行）。
5. `solve_univariate_inequality` 对非 `Symbol` 生成元（如 `RandomSymbol`）先转换为实 `Dummy` 再求解，避免退化成 `ConditionSet`。

## 验证

- FAIL_TO_PASS：`test_issue_30529`、`test_solve_univariate_inequality_random_symbol`
- PASS_TO_PASS：`sympy/solvers/tests/test_inequalities.py` 全量（修复后 30 项通过、2 项 xfail）

# 修复 `reduce_inequalities` 在求解过程中消去不等式奇点的问题

## 任务

仓库 `sympy/sympy` 当前处于 commit `31e03dc7ed8114117274ea679be1835044cec9c9`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/sympy/sympy
cd sympy && git checkout 31e03dc7ed8114117274ea679be1835044cec9c9
pip install -e . pytest hypothesis
```

## 原始 issue

> 来源：https://github.com/sympy/sympy/issues/30529 （BSD-3-Clause，© SymPy contributors）
>
> **improve singularity handling in `inequalities.py`**
>
> While `_solve_inequality` eliminates singularities from the solution, the higher level `reduce_inequalities` can eliminate singularities before that function gets solved:
>
> <img width="412" height="157" alt="Image" src="https://github.com/user-attachments/assets/5ddeb305-73aa-4ee9-956b-903a0cc81741" />

## 问题复现

旧版实现中，单条关系式经 `_solve_inequality` 时会保留分母零点约束；但 `reduce_inequalities` / `reduce_rational_inequalities` 会在交给 `_solve_inequality` 之前先把关系式左右相减，分母的零点可能在这一步被约掉。修复前的实际输出：

```python
>>> from sympy import Symbol, sin
>>> from sympy.solvers.inequalities import reduce_inequalities, reduce_rational_inequalities
>>> x = Symbol("x", real=True)
>>> reduce_inequalities(1/x <= 1/x, x)
True                     # 1/x 在 x = 0 处无定义，应保留 Ne(x, 0)
>>> reduce_inequalities(1/sin(x) <= 1/sin(x), x)
True                     # 应保留 Ne(sin(x), 0)
>>> reduce_rational_inequalities([[1/x <= 1/x]], x)
True                     # 应保留 Ne(x, 0)
```

期望：求解结果必须保留因分母为零而失效的点；对无法解出单点零点的分母（如 `sin(x)`），直接保留 `d != 0` 形式的约束。

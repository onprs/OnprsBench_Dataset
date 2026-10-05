# 修复数组打印机把纯标量赋值打印为数组运算的问题

## 任务

仓库 `sympy/sympy` 当前处于 commit `e0e25c8eaab46155ee7c35c783e3f6f41e147b9b`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/sympy/sympy
cd sympy && git checkout e0e25c8eaab46155ee7c35c783e3f6f41e147b9b
pip install -e . pytest hypothesis numpy
```

## 原始 issue

> 来源：https://github.com/sympy/sympy/issues/30395 （BSD-3-Clause，© SymPy contributors）
>
> **[Printing] JaxPrinter/NumPyPrinter: scalar assignments print as array ops (`add`) or crash with `PrintMethodNotImplementedError`**
>
> **Cross-reference:** Regressed in #30132 (specifically commit `87bd37a8512aacabb4ef3f00d3e0e8b2c92416fe`) / cc @Upabjojr
>
> ## Summary
>
> When printing assignments (`doprint(expr, assign_to)` or `Assignment(assign_to, expr)`) using `JaxPrinter` or `NumPyPrinter` (via `ArrayPrinter._print_Assignment`), pure-scalar expressions with no `Indexed`, `Matrix`, or `Array` nodes are now erroneously converted into array expressions on `sympy-dev` (as of 09-02-2026).
>
> This causes two distinct regressions:
>
> 1. **Scalar addition degrades from infix `+` to nested binary `add(...)`:**
>    `x + y + z` prints as `jax.numpy.add(jax.numpy.add(x, y), z)` (or `numpy.add(...)`) instead of `x + y + z`.
> 2. **Crash on scalar expressions with functions:**
>    Expressions with scalar functions such as `x**2 + sqrt(y) - sin(x*z)` convert to `ArrayAdd` containing `ArrayElementwiseApplyFunc`. Because neither `JaxPrinter` nor `NumPyPrinter` implements `_print_ArrayElementwiseApplyFunc`, `doprint(expr, 'blah')` crashes with `PrintMethodNotImplementedError`.
>    In contrast, `doprint(expr)` without `assign_to` prints cleanly with normal infix arithmetic.
>
> ## Minimal Reproducer
>
> ```python
> import sympy as sp
> from sympy.printing.numpy import JaxPrinter, NumPyPrinter
>
> x, y, z = sp.symbols('x y z')
>
> # -------------------------------------------------------------
> # Case 1: Pure scalar Add degraded to binary add(...)
> # -------------------------------------------------------------
> print("Case 1 (x + y + z):")
> print(repr(JaxPrinter().doprint(x + y + z, 'blah')))
> print(repr(NumPyPrinter().doprint(x + y + z, 'blah')))
>
> # -------------------------------------------------------------
> # Case 2: Inconsistency and crash on expressions with functions
> # -------------------------------------------------------------
> expr = x**2 + sp.sqrt(y) - sp.sin(x*z)
>
> print("\nCase 2 without assign_to (works):")
> print(repr(JaxPrinter().doprint(expr)))
>
> print("\nCase 2 with assign_to (crashes on sympy-dev):")
> try:
>     print(repr(JaxPrinter().doprint(expr, 'blah')))
> except Exception as e:
>     print(f"{type(e).__name__}: {e}")
> ```
>
> ## Expected Behavior (SymPy 1.14.0)
>
> ```python
> # Case 1:
> 'blah = x + y + z'
> 'blah = x + y + z'
>
> # Case 2 without assign_to:
> 'x**2 + jax.numpy.sqrt(y) - jax.numpy.sin(x*z)'
>
> # Case 2 with assign_to:
> 'blah = x**2 + jax.numpy.sqrt(y) - jax.numpy.sin(x*z)'
> ```
>
> ## Actual Behavior (sympy-dev as of 09-02-2026)
>
> ```python
> # Case 1:
> 'blah = jax.numpy.add(jax.numpy.add(x, y), z)'
> 'blah = numpy.add(numpy.add(x, y), z)'
>
> # Case 2 without assign_to:
> 'x**2 + jax.numpy.sqrt(y) - jax.numpy.sin(x*z)'
>
> # Case 2 with assign_to:
> PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.numpy.JaxPrinter'>: <class 'sympy.tensor.array.expressions.array_expressions.ArrayElementwiseApplyFunc'>
> Set the printer option 'strict' to False in order to generate partially printed code.
> ```
>
> ## Printing path
>
> `ArrayPrinter._print_Assignment` in `sympy/printing/pycode.py` arrayifies both sides:
>
> ```python
> lhs = self._print(self._arrayify(expr.lhs))
> rhs = self._print(self._arrayify(expr.rhs))
> ```
>
> `_arrayify` is `convert_indexed_to_array` with an `except Exception: return indexed` fallback.
>
> `_print_ArrayAdd` then unconditionally folds to `jax.numpy.add` / `numpy.add`, and `_print_ArrayTensorProduct` to `einsum`.
>
> ## Why scalar exprs used to survive this path (1.14.0 behavior)
>
> On `1.14.0`, `convert_indexed_to_array` raises on these scalar inputs, so `_arrayify` falls back to the original scalar expression:
>
> * `x**2 + sqrt(y) - sin(x*z)` -> `ValueError: index is larger than expression shape` (from the `Pow` branch via `ArrayDiagonal` validation).
> * `x*z + y`, `y + sin(x*z)` -> `AttributeError: 'Symbol' object has no attribute 'shape'` (from `_array_add` / `ArrayAdd.__new__` doing `arg.shape` directly).
>
> Meanwhile `convert_indexed_to_array(x*z)` already succeeds on `1.14.0` as `ArrayTensorProduct(x, z)`, which is why scalar `Mul` already printed as `einsum`.
>
> ## What changed on master
>
> Recent merges made array-expression handling and `convert_indexed_to_array` permissive for rank-0 expressions:
>
> 1. **Merged PR #30132:** [Claude Opus 4.8 bug fixes in array expressions module](https://github.com/sympy/sympy/pull/30132)
>    Merged on 2026-09-02T20:00:45Z by **Francesco Bonazzi ([`@Upabjojr`](https://github.com/Upabjojr))**.
>    Specifically, commit [`87bd37a8512aacabb4ef3f00d3e0e8b2c92416fe`](https://github.com/sympy/sympy/commit/87bd37a8512aacabb4ef3f00d3e0e8b2c92416fe) modified `sympy/tensor/array/expressions/from_indexed_to_array.py`:
>    ```python
>    if isinstance(expr, Pow):
>        subexpr, subindices = _convert_indexed_to_array(expr.base)
>    +   if not subindices:
>    +       # Scalar base, no array axes involved:
>    +       return expr, ()
>    ```
>    Scalar powers no longer raise `ValueError`, and unary functions wrap into `ArrayElementwiseApplyFunc`.
> 2. **Merged PR #30276:** [ArrayAdd: collect proportional terms and add collect_tensor_products()](https://github.com/sympy/sympy/pull/30276)
>    Merged on 2026-09-02T10:21:59Z by **Francesco Bonazzi ([`@Upabjojr`](https://github.com/Upabjojr))**.
>    Commit [`e791b61374549ee88e9b62b92e8d187171ed576d`](https://github.com/sympy/sympy/commit/e791b61374549ee88e9b62b92e8d187171ed576d) formalized that rank-0 scalar addends remain an `ArrayAdd` rather than raising or collapsing to scalar sums.
>
> Because `convert_indexed_to_array` no longer raises on these scalar expressions:
> * `x + y + z` converts to `ArrayAdd(x, y, z)`, which `ArrayPrinter._print_ArrayAdd` prints via binary folds to `add(...)`.
> * `x**2 + sqrt(y) - sin(x*z)` converts to `ArrayAdd(..., ArrayElementwiseApplyFunc(sin, ...))`, which crashes in `JaxPrinter`/`NumPyPrinter` because `_print_ArrayElementwiseApplyFunc` is unimplemented.
>
> ## Suggested Fix
>
> The root issue is that `ArrayPrinter._arrayify` blindly passes all expressions—including pure scalars—to `convert_indexed_to_array`, previously relying on exceptions to leave scalars untouched.
>
> `ArrayPrinter._arrayify` in `sympy/printing/pycode.py` should check whether `indexed` actually contains array, matrix, or indexed nodes before invoking `convert_indexed_to_array`:
>
> ```diff
> diff --git a/sympy/printing/pycode.py b/sympy/printing/pycode.py
> --- a/sympy/printing/pycode.py
> +++ b/sympy/printing/pycode.py
> @@ -416,6 +416,12 @@ class ArrayPrinter:
>
>      def _arrayify(self, indexed):
> +        from sympy.tensor.indexed import IndexedBase, Indexed
> +        from sympy.tensor.array.ndim_array import NDimArray
> +        from sympy.tensor.array.expressions.array_expressions import _CodegenArrayAbstract
> +        from sympy.matrices.expressions.matexpr import MatrixExpr
> +        if not (isinstance(indexed, NDimArray) or indexed.has(IndexedBase, Indexed, _CodegenArrayAbstract, MatrixExpr)):
> +            return indexed
>          from sympy.tensor.array.expressions.from_indexed_to_array import convert_indexed_to_array
>          try:
>              return convert_indexed_to_array(indexed)
> ```
>
> Additionally, `JaxPrinter` and `NumPyPrinter` should implement `_print_ArrayElementwiseApplyFunc` so that when legitimate array expressions use elementwise functions, code generation does not fail.
>
> ### Proposed Test Case (for `sympy/printing/tests/test_numpy.py`)
>
> ```python
> def test_numpy_scalar_assignment_printing():
>     x, y, z = symbols('x y z')
>     np_p = NumPyPrinter()
>     jp = JaxPrinter()
>
>     # 1. Pure scalar Add preserves infix arithmetic in assignments:
>     assert np_p.doprint(x + y + z, 'out') == 'out = x + y + z'
>     assert jp.doprint(x + y + z, 'out') == 'out = x + y + z'
>
>     # 2. Pure scalar expressions with functions print without crashing:
>     expr = x**2 + sqrt(y) - sin(x*z)
>     assert np_p.doprint(expr, 'out') == 'out = x**2 + numpy.sqrt(y) - numpy.sin(x*z)'
>     assert jp.doprint(expr, 'out') == 'out = x**2 + jax.numpy.sqrt(y) - jax.numpy.sin(x*z)'
> ```
>
> ## Environment
>
> * **Failing:** SymPy `master` / `1.15.0.dev` as of 2026-09-02 (commit `e0e25c8eaa`), Python 3.12.
> * **Passing:** SymPy `1.14.0`.

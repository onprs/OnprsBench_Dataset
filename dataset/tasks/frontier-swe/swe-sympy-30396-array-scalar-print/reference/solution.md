# 参考修复分析（基于上游 PR #30396，已合并）

## 根因

`ArrayPrinter._print_Assignment` 对赋值两侧调用 `_arrayify`，而 `_arrayify` 无条件调用 `convert_indexed_to_array`，只依赖异常回退到原始表达式：

- `convert_indexed_to_array` 此前对纯标量会抛错（如 `ValueError` / `AttributeError`），因此标量得以原样打印；
- 上游对 rank-0 表达式的处理放宽后，`x + y + z` 变成 `ArrayAdd(x, y, z)`，经 `_print_ArrayAdd` 打印为嵌套 `add(...)`；
- `x**2 + sqrt(y) - sin(x*z)` 中的一元函数变成 `ArrayElementwiseApplyFunc`，而 `JaxPrinter` / `NumPyPrinter` 没有对应的打印方法，赋值时抛出 `PrintMethodNotImplementedError`。

## 修复要点（上游实际做法）

1. `sympy/printing/pycode.py` 的 `ArrayPrinter` 增加 `_print_ArrayElementwiseApplyFunc` 与 `_elementwise_body`：
   - 生成一个"打印为操作数代码"的 `Dummy` 子类 `_ElementwiseOperand` 占位符，占用操作数打印结果的优先级；
   - 把函数体（`Lambda` 或函数对象）中的变量替换为占位符后交给常规打印逻辑，使 `sin(A)` 打印为 `numpy.sin(A)`、`Lambda(d, 2*d + 1)` 在 `M + N` 上打印为 `2*(M + N) + 1`；
   - 用 `_is_atomic_code` 判断操作数打印结果是否为标识符或单个调用，决定是否需要括号。
2. `sympy/tensor/array/expressions/from_indexed_to_array.py` 对纯标量（无数组轴）保持标量形态，不再包装为数组表达式，使赋值路径回落为中缀打印。
3. `_ElementwiseOperand` 的 `sort_key` 保证占位符在求和/乘积中排在前面，输出稳定。

## 验证

- FAIL_TO_PASS：`test_issue_30395_scalar_assignment`、`test_array_printer`、`test_tensorflow_elementwise_apply_func`、`test_convert_indexed_to_array_scalars_stay_scalars`
- PASS_TO_PASS：`sympy/printing/tests/test_numpy.py`、`sympy/printing/tests/test_pycode.py`、`sympy/printing/tests/test_tensorflow.py`、`sympy/tensor/array/expressions/tests/test_convert_indexed_to_array.py`
- 修复后：70 项通过、7 项跳过

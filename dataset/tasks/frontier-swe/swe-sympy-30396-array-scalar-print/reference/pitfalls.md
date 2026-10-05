# 常见错误

1. **照搬 issue 中的建议方案**：只在 `_arrayify` 前判断是否包含数组节点，能修复纯标量场景，但数组表达式上的 `ArrayElementwiseApplyFunc` 仍无法打印，相关测试仍失败。
2. **直接在函数体上替换变量**：把操作数符号代入函数表达式会把 `d**2` 变成矩阵幂等错误语义；必须用"打印为操作数代码"的占位符保持逐元素语义。
3. **忽略括号**：操作数是复合表达式（如 `M + N`）时必须按优先级加括号，`2*M + N + 1` 与 `2*(M + N) + 1` 不同。
4. **把非原子代码当作原子**：只有标识符或单个函数调用可以不加括号；`a + b`、`f(x) + 1` 都需要括号。
5. **改变既有数组输出**：`ArrayAdd`、`ArrayTensorProduct`、`ArrayContraction`、`PermuteDims`、`Assignment` 的既有打印结果不得变化。
6. **破坏张量打印路径**：`from_indexed_to_array` 的标量处理同时影响张量打印与 `test_convert_indexed_to_array` 的既有断言，修改后需同时回归两个测试文件。

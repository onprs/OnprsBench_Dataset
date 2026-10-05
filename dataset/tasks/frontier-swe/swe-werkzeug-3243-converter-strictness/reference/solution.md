# 参考修复分析（基于上游 PR #3243，已合并）

## 根因

`src/werkzeug/routing/converters.py` 中 `NumberConverter` 作为 `IntegerConverter` 与 `FloatConverter` 的私有基类，把两类转换器的差异交给了 `num_convert` 与类级正则：

- `IntegerConverter.regex = r"\d+"`、`FloatConverter.regex = r"\d+\.\d+"`：`\d` 在 Python 正则中匹配任意 Unicode 十进制数字，`١٢٣` 这类非 ASCII 数字被接受。
- `to_python` 在 `fixed_digits` 用 `len(value)` 计数，`-0123` 的负号被计入位数。
- `FloatConverter.to_url` 用 `f"{value:f}".rstrip("0")` 格式化：`inf`/`nan` 不报错，而 6 位小数的截断又排除了大量合法取值。
- `to_url` 只在最后格式化，不校验负数（`signed=False`）与 `min`/`max` 范围，构建阶段可以生成无法被自身匹配的 URL。

## 修复要点（上游实际做法）

1. 删除 `NumberConverter`，两个转换器各自显式实现，去掉共享基类带来的隐式耦合。
2. 正则改为 `[0-9]+` / `[0-9]+\.[0-9]+`，只接受 ASCII 数字。
3. `fixed_digits` 用 `len(value.removeprefix("-"))` 计数。
4. `FloatConverter.to_python` 对 `math.isinf` 的结果抛出 `ValidationError`。
5. `to_url` 变成带校验的构建入口：未开启 `signed` 时拒绝负数，越界拒绝，`float` 的 `inf`/`nan` 拒绝；`int` 的 `fixed_digits` 溢出拒绝。
6. `to_url` 不再截断小数位：先用 `str(value)`，若含科学计数法则按指数展开（大数补零、小数补前导零），保留完整精度同时避免科学计数法。

## 验证

- FAIL_TO_PASS：`tests/test_routing.py::test_converter`（11 个参数化用例在修复前失败）
- PASS_TO_PASS：`tests/test_routing.py` 全量（修复后 186 项通过）

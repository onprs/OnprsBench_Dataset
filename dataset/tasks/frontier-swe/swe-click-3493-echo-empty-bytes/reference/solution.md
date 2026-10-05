# 参考修复分析（基于上游 PR #3493，已合并）

## 根因

`src/click/utils.py` 的 `echo()` 中：

```python
if nl:
    out = out or ""
```

`b""` 与 `bytearray(b"")` 是假值（falsy），`out or ""` 把空 bytes 替换成空 **str**。随后 `isinstance(out, str)` 分支追加 `"\n"`，最终向二进制流写入 str，抛出 `TypeError: a bytes-like object is required, not 'str'`。

## 修复要点

上游把"类型归一化"重写为显式分支（实际提交采用 `match` 语句）：

- `str / bytes / bytearray`：原样保留（空 bytes 不再被吞掉类型）；
- `None`：转为 `""`；
- 其他对象：`str(message)`。

等价的最小修复是 issue 中建议的 `out = "" if out is None else out`。关键是区分 `None` 与"空但类型合法"的输入，不能再用真值判断。

## 验证

- FAIL_TO_PASS：`tests/test_utils.py::test_echo_custom_file`（新增断言：`click.echo(b"", BytesIO())` 应写入 `b"\n"`）
- PASS_TO_PASS：`tests/test_utils.py` 全量（修复后 76 项通过、71 项跳过）

# 参考修复分析（基于上游 PR #1593，已合并）

## 根因

`src/attr/_make.py` 的 `_is_class_var(annot)` 用于判断某个注解是否为 `ClassVar`：它把注解 `str()` 化后做前缀/子串检查（`ClassVar[...]`、`typing.ClassVar`、`t.ClassVar` 等）。

Python 3.14 的注解延迟求值（PEP 649）下，`if TYPE_CHECKING` 中才导入的名字在类体执行时并未求值，`ClassVar[str]` 保持为 `ForwardRef('ClassVar[str]', is_class=True, owner=T)`。`str(ForwardRef(...))` 得到的是 `"ForwardRef('ClassVar[str]', ...)"`，与既有前缀检查不匹配，于是该字段被当作普通实例字段，`__init__` 因而多出一个必填参数。

## 修复要点（上游实际做法）

```python
def _is_class_var(annot):
    annot = getattr(annot, "__forward_arg__", annot)
    annot = str(annot)
    ...
```

在字符串化之前解包 `ForwardRef.__forward_arg__`，使 `ForwardRef("ClassVar[str]")` 复现原始注解文本，从而被既有的 `ClassVar` 判定路径识别；其他注解形态不受影响。

## 验证

- FAIL_TO_PASS：`tests/test_annotations.py::TestAnnotations::test_missing_classvar_import`（`slots` 两种参数）、`tests/test_annotations.py::test_is_class_var[annot4]`
- PASS_TO_PASS：`tests/test_annotations.py`
- 修复后：50 项全部通过

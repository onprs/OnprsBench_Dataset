# 常见错误

1. **只匹配 `ForwardRef` 的完整 repr**：`str(ForwardRef("ClassVar[str]"))` 是 `"ForwardRef('ClassVar[str]')"`，靠 `startswith("ClassVar")` 之类的判断永远不会命中，必须取出 `__forward_arg__`。
2. **把任意 `ForwardRef` 都当作 ClassVar**：只有注解文本本身是 `ClassVar[...]` 形态（或 `typing.ClassVar` / `t.ClassVar`）时才应判定，解包后仍需走既有检查。
3. **在 `attr.s`/`attrs.define` 侧捕获 `NameError`**：问题发生在注解的表示形态，不是抛错；在调用侧掩盖异常会漏掉其他字段。
4. **只在 Python 3.14 分支修补**：解包 `__forward_arg__` 对低版本无害，按版本分叉反而容易让测试在不同解释器下行为不一致。
5. **改动 `_is_class_var` 的字符串化顺序**：先解包再 `str()`；如果先 `str()` 再尝试解包，`ForwardRef` 信息已经丢失。

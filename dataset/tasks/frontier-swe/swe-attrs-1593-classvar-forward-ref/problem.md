# 修复 attrs 在 Python 3.14 下无法识别未导入 `ClassVar` 注解的问题

## 任务

仓库 `python-attrs/attrs` 当前处于 commit `6851ab593cd25f3c14393e9355d57d22bec2a074`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/python-attrs/attrs
cd attrs && git checkout 6851ab593cd25f3c14393e9355d57d22bec2a074
pip install -e . pytest hypothesis
```

注意：相关测试只在 Python 3.14 及以上执行。

## 原始 issue

> 来源：https://github.com/python-attrs/attrs/issues/1575 （MIT，© attrs contributors）
>
> **attrs doesn't recognize ClassVar if not imported in Python 3.14**
>
> The following code
>
> ```python
> from typing import TYPE_CHECKING
>
> import attrs
>
> if TYPE_CHECKING:
>     from typing import ClassVar
>
> @attrs.define
> class T:
>     t: ClassVar[str]
>
> T()
> ```
>
> results in:
>
> ```python
> Traceback (most recent call last):
>   File "/tmp/test.py", line 12, in <module>
>     T()
>     ~^^
> TypeError: T.__init__() missing 1 required positional argument: 't'
> ```
>
> Since the `if TYPE_CHECKING` block doesn't run, `ClassVar` isn't defined and attrs can't evaluate the ForwardRef or doesn't recognize `ClassVar`:
>
> ```python
> >>> attrs.fields_dict(T)["t"]
> Attribute(name='t', default=NOTHING, validator=None, repr=True, eq=True, eq_key=None, order=True, order_key=None, hash=None, init=True, metadata=mappingproxy({}), type=ForwardRef('ClassVar[str]', is_class=True, owner=<class '__main__.T'>), converter=None, kw_only=False, inherited=False, on_setattr=None, alias='t')
> ```
>
> Before Python 3.14, `T`'s definition would only run if you used a string annotation or `from __future__ import annotations` (which if used with 3.14, the above code runs fine), but with the new annotations behavior the class definition runs fine and this error appears. This is actually issue for dataclasses too, as I get the same error with them.
>
> I'm not sure if this is fixable, but decided to report it, because it catches you by surprise

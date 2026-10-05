# 修复 `click.echo` 输出空字节串时的 TypeError

## 任务

仓库 `pallets/click` 当前处于 commit `d42f15b71757de791a5781fb179fd972da9169f5`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/pallets/click
cd click && git checkout d42f15b71757de791a5781fb179fd972da9169f5
pip install -e . pytest
```

## 原始 issue

> 来源：https://github.com/pallets/click/issues/3487 （BSD-3-Clause，© Pallets）
>
> **Echoing empty bytes or bytearray raises TypeError**
>
> Hopefully this isn't too frivolous but I think it's an easy fix: echoing an empty byte string will cause a crash if `nl=True`.
>
> To replicate:
>
> ```shell
> $ python -c "import io; import click; click.echo(b'', io.BytesIO(), nl=True)"
>
> Traceback (most recent call last):
>   File "<string>", line 1, in <module>
>   File "/myproject/click/src/click/utils.py", line 337, in echo
>     file.write(out)  # type: ignore
>     ^^^^^^^^^^^^^^^
> TypeError: a bytes-like object is required, not 'str'
> ```
>
> Expected behaviour:
>
> We expect `b"\n"` to be written to the stream and for `TypeError` not to be thrown.
>
> Environment:
>
> - Python version: 3.11.2
> - Click version: 8.5.0.dev0

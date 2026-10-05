# 修复 click.progressbar 结束时位置显示不回满的问题

## 任务

仓库 `pallets/click` 当前处于 commit `8b44edfff7d9a6c895fa804148c16b3a0bc9efb5`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/pallets/click
cd click && git checkout 8b44edfff7d9a6c895fa804148c16b3a0bc9efb5
pip install -e . pytest
```

## 原始 issue

> 来源：https://github.com/pallets/click/issues/3571 （BSD-3-Clause，© Pallets）
>
> **`click.progressbar` doesn't show full completion when using `show_pos=True` combined with `update_min_steps`**
>
> Using a `click.progressbar` with:
> - `update_min_steps` which isn't a divisor of `length`
> - `show_pos=True`
>
> won't show full completion at the end. This can be reproduced as follows:
>
> ```python
> import time
>
> import click
>
> with click.progressbar(
>     range(20),
>     show_pos=True,
>     update_min_steps=7,
> ) as bar:
>     for i in bar:
>         time.sleep(0.1)
> ```
>
> with (final) output in the terminal
>
> ```text
>   [####################################]  14/20
> ```
>
> **Expected behaviour**: I had expected the output to show `20/20` at the end.
> This would be consistent with the default percentage formatting, as can be seen by commenting the line `show_pos=True` and re-running the reproduction:
>
> ```text
>   [####################################]  100%
> ```
>
> Environment:
>
> - Python version: tested with 3.12.3 and 3.14.3
> - Click version: 8.4.1

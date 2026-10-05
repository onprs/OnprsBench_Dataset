# 修复 Werkzeug 的 `int` / `float` URL 转换器接受非法取值的问题

## 任务

仓库 `pallets/werkzeug` 当前处于 commit `ef518e429b67a91a307de37a1845c93110180371`（修复合入前的状态）。下面的真实 issue 报告了 URL 转换器的缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/pallets/werkzeug
cd werkzeug && git checkout ef518e429b67a91a307de37a1845c93110180371
pip install -e . pytest ephemeral-port-reserve
```

## 原始 issue

> 来源：https://github.com/pallets/werkzeug/issues/3242 （BSD-3-Clause，© Pallets）
>
> **`int` and `float` converter issues**
>
> This is a more conservative version of #3237 that only fixes bugs/unintended behavior and otherwise doesn't break existing URLs. I'll target this at 3.2 since it does change what's accept a bit still.
>
> - Non-ASCII digits are accepted.
> - `int(fixed_digits=4, signed=True)` counts the negative sign as a digit.
> - `float` overflow values (too large to fit in float) become `inf`, which is a special, unexpected value that can cause problems when used later on.
>   - Underflow values become `0.0`, which is a "normal" value.
>   - Binary float cannot represent all values, but that's a very abstract concept for users to understand and ensure in URLs.
> - #3147 prevented scientific notation by limiting to 6 decimal places, which excludes many legitimate values.
>
> A 1-to-1 mapping of URLs to parsed values is not a goal. This will be documented for these converters. However, `.4` and `4.` will remain disallowed, I want to keep the more obvious `left.right` syntax only. And `4.` would cause issues with Markdown URL detection.
>
> The private `NumberConverter` base seems to be more trouble than the small amount of duplication it removes, especially if we also tried to extend it to `decimal` later, so I'll remove it.

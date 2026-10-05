# 修复 Flask 对 IPv6 地址的错误解析

## 任务

仓库 `pallets/flask` 当前处于 commit `514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/pallets/flask
cd flask && git checkout 514fc6b3e8402e4c646d5284e97a4f0ab50a7c4b
pip install -e . pytest
```

## 原始 issue

> 来源：https://github.com/pallets/flask/issues/6093 （BSD-3-Clause，© Pallets）
>
> **IPv6 addresses parsed incorrectly because of `.partition(":")`?**
>
> Hi, I checked the code and saw that two places use `.partition(":")` on addresses, and IPv6 addresses contain ":".
>
> This breaks 1. `session_transaction` value setting, and 2. `Flask.run()` if `SERVER_NAME` is set. I've already prepared two tests that fail, you can use them to reproduce:
>
> 1. In `test_testing.py`
>
> ```python
> def test_session_transaction_ipv6(app):
>     base_url = "http://[::1]:8000/"
>     client = app.test_client()
>
>     @app.get("/")
>     def index():
>         return str(flask.session.get("value"))
>
>     with client.session_transaction(base_url=base_url) as sess:
>         sess["value"] = 42
>
>     assert client.get("/", base_url=base_url).text == "42"
> ```
>
> 2. Add one case to `test_run_from_config`
>
> ```python
> (None, None, "[::1]:8080", "::1", 8080),
> ```
>
> Is this known and intended? I could send the patches for these two places.

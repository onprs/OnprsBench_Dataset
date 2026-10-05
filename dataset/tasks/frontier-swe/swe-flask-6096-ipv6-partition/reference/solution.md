# 参考修复分析（基于上游 PR #6096，已合并）

## 根因

两处代码用 `str.partition(":")` 从地址中拆出 host / port：

1. `src/flask/app.py` 的 `Flask.run()`：`sn_host, _, sn_port = server_name.partition(":")`
2. `src/flask/testing.py` 的 `session_transaction()`：`ctx.request.host.partition(":")[0]`

`partition(":")` 按第一个冒号截断。IPv6 地址本身含多个冒号（如 `[::1]:8080`），被截成 `"["` 之类的碎片，导致 host/port 解析错误。

## 修复要点

改用结构化 URL 解析：

- `app.py`：`urlsplit(f"//{server_name}")`，取 `.hostname` 与 `.port`。注意 `.port` 返回 `int | None`，因此后续判断从 `elif sn_port:` 改为 `elif sn_port is not None:`，并去掉冗余的 `int()` 转换；`run_simple` 的 `host` 不再需要 `t.cast(str, ...)`。
- `testing.py`：`urlsplit(ctx.request.host_url).hostname or "localhost"`（保留无地址时的回退行为）。

## 验证

- FAIL_TO_PASS：`tests/test_testing.py::test_session_transaction_ipv6`；`tests/test_basic.py::test_run_from_config[None-None-[::1]:8080-::1-8080]`
- PASS_TO_PASS：`tests/test_testing.py` 与 `tests/test_basic.py` 全量（修复后 159 项全过）

详细复现记录见 `judge_assets/verify.yaml`。

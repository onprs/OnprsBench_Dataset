# 常见错误

1. **只修一处**：issue 明确给出两处出错点（`Flask.run()` 与 `session_transaction()`）。只修 `app.py` 会让 `test_session_transaction_ipv6` 继续失败。
2. **继续用字符串处理**：用 `rsplit(":", 1)` 之类的方法处理 `[::1]:8080` 仍要手工剥离方括号，容易漏掉无端口 IPv6（`[::1]`）与 IPv4 的兼容。上游采用 `urlsplit("//...")` 正是为了复用标准解析。
3. **忽略 `.port` 的类型**：`urlsplit(...).port` 返回 `int | None`，且端口非法时会抛 `ValueError`；沿用旧的 `elif sn_port:`（真值判断）在语义上不等价（`0` 端口的处理差异）。
4. **改动测试而非源码**：任务要求修复库代码；修改测试断言以迁就错误行为属于伪装通过，在 root_cause 维度记 0 分。

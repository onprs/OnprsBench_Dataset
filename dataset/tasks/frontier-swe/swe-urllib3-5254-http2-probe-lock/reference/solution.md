# 参考修复分析（基于上游 PR #5254，已合并）

## 根因

`src/urllib3/http2/probe.py` 的 `_HTTP2ProbeCache.acquire_and_get()` 用 per-origin `RLock` 协调"谁负责探测"：

```python
with self._lock:                     # 缓存级锁
    value = self._cache_values[key]  # 已有结果则直接返回（尚未碰 per-origin 锁）
    ...
    key_lock = self._cache_locks[key]

key_lock.acquire()                   # 所有等待者都拿 per-origin 锁
try:
    value = self._cache_values[key]
except BaseException:
    key_lock.release()
    raise
return value                         # 等待者拿到缓存值后直接返回，未释放
```

约定是"拿到 `None` 的调用者负责探测，探测完成后调用 `set_and_release()` 释放"。当探测者写入结果并释放锁后，等待者被唤醒、读到非 `None` 的缓存值，却沿 `return value` 直接返回，锁被永久留在等待者线程名下；剩余等待者永远阻塞。

## 修复要点（上游实际做法）

```python
if value is not None:
    key_lock.release()

return value
```

- 只有拿到 `None`（负责探测）的调用者保留锁，直到 `set_and_release()`；
- 读到已缓存布尔值的等待者立即释放锁；
- 异常路径的释放逻辑保持不变。

## 验证

- FAIL_TO_PASS：`test/test_http2_probe.py::test_waiter_releases_lock_when_probe_result_is_available`（用 `MagicMock` 断言 `release` 恰好调用一次）
- PASS_TO_PASS：`test/test_http2_probe.py`、`test/test_http2_connection.py`、`test/test_poolmanager.py`

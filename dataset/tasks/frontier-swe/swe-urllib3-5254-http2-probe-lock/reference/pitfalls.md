# 常见错误

1. **在快速路径释放缓存级锁**：已缓存结果的新调用在 `with self._lock` 内提前返回，此时 per-origin 锁从未获取，误释放会抛 `RuntimeError`。
2. **让所有调用者都释放**：探测者拿到 `None` 后必须继续持有锁直到 `set_and_release()`，提前释放会让并发连接重复发起探测。
3. **用 try/finally 包住整个函数**：等待者与探测者的锁所有权不同，统一 finally 释放同样会破坏探测路径。
4. **改掉异常路径的释放**：`except BaseException: key_lock.release(); raise` 是既有语义，重构时不要遗漏或重复释放。
5. **只修等待者而不管缓存值判断**：必须按"返回值是否为 `None`"区分角色，不能用 `_cache_values` 再次查找（会引入新的竞态窗口）。

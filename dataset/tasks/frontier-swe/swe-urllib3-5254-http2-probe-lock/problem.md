# 修复 HTTP/2 探测缓存中等待线程返回后不释放锁的问题

## 任务

仓库 `urllib3/urllib3` 当前处于 commit `bcf84e6815f623521e1ffe3e6ab0224d778929c0`（修复合入前的状态）。下面的真实 issue 报告了一个缺陷。请在仓库中定位并修复该缺陷，使你的修改通过相关测试。

环境准备（供参考）：

```bash
git clone https://github.com/urllib3/urllib3
cd urllib3 && git checkout bcf84e6815f623521e1ffe3e6ab0224d778929c0
pip install -e . pytest trustme "anyio[trio]" h2 httpx hypercorn cryptography quart quart-trio
```

## 原始 issue

> 来源：https://github.com/urllib3/urllib3/issues/5206 （MIT，© urllib3 contributors）
>
> **Concurrent HTTP/2 probes can leave threads blocked in `acquire_and_get`**
>
> ### Subject
>
> When HTTP/2 support is enabled, concurrent first connections to the same origin can leave some threads blocked indefinitely in `_HTTP2ProbeCache.acquire_and_get()`.
>
> The first thread for an unknown origin acquires the per-origin lock and performs the probe. Other threads that reach the cache before the result is published wait on that lock. Once the first thread stores the result and releases the lock, one waiter wakes and reads the resulting `True` or `False`, but returns without releasing the lock. Any remaining waiters stay blocked.
>
> Connections that arrive after the result has been cached are unaffected because they return while holding the cache-wide lock, before acquiring the per-origin lock. The problem only affects threads that were already waiting for the initial probe.
>
> ### Environment
>
> ```
> OS Linux-7.0.0-30-generic-x86_64-with-glibc2.39
> Python 3.12.3
> OpenSSL 3.0.13 30 Jan 2024
> urllib3 2.7.1.dev42
> ```
>
> ### Steps to Reproduce
>
> ```python
> # test.py
> import threading
> import time
> from urllib3.http2.probe import _HTTP2ProbeCache
>
> cache = _HTTP2ProbeCache()
> host, port = "example.test", 443
> # This thread owns the initial probe.
> assert cache.acquire_and_get(host, port) is None
> barrier = threading.Barrier(3)
> results = []
>
> def wait_for_probe(index):
>     barrier.wait()
>     results.append((index, cache.acquire_and_get(host, port)))
>
> threads = [
>     threading.Thread(target=wait_for_probe, args=(index,), daemon=True)
>     for index in range(2)
> ]
> for thread in threads:
>     thread.start()
> barrier.wait()
> time.sleep(0.1)  # allow both threads to wait on the per-origin lock
> cache.set_and_release(host, port, False)
> for thread in threads:
>     thread.join(timeout=0.5)
> print("results", results)
> print("alive", [thread.is_alive() for thread in threads])
> print("lock", cache._cache_locks[(host, port)])
> ```
>
> ### Expected Behavior
>
> After the probe result is published, every waiting connection should continue.
> The per-origin lock should not remain owned by a waiter that has already returned from `acquire_and_get()`.
>
> ```
> results [(0, False), (1, False)]
> alive [False, False]
> lock <unlocked _thread.RLock object ... count=0>
> ```
>
> ### Actual Behavior
>
> ```
> results [(0, False)]
> alive [False, True]
> lock <locked _thread.RLock object owner=131377442428608 count=1 at 0x777cb286b600>
> ```
>
> ### Relevant code
>
> The following might be the reasons for this bug to occur.
>
> ```python
> # src/urllib3/http2/probe.py
> key_lock.acquire()
> try:
>     value = self._cache_values[key]
> except BaseException:
>     key_lock.release()
>     raise
> return value
> ```
>
> Only a caller that receives `None` later calls `set_and_release()` from `HTTPSConnection.connect()`.
> A waiter that receives a cached boolean has no corresponding release.

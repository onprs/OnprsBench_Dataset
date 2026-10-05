# 参考修复分析（基于上游 PR #3818，已合并）

## 根因

`src/click/core.py` 的 `Command.main()` 在旧实现中把"处理异常"与"输出消息、退出进程"写在同一个 `except` 块里：

```python
except (EOFError, KeyboardInterrupt) as e:
    echo(file=sys.stderr)
    raise Abort() from e
...
except ClickException as e:
    e.show()
    sys.exit(e.exit_code)
...
except Abort:
    echo(_("Aborted!"), file=sys.stderr)
    sys.exit(1)
```

这些块位于最外层 `try` 之外（或之后），`echo`、`show`、`sys.exit` 执行期间若再收到一次 `KeyboardInterrupt`（例如 Ctrl-C 在终端回显/刷新时到达），没有兜底处理器，异常直接冒泡为用户可见的 traceback，并在部分场景丢掉原本的退出码。

## 修复要点（上游实际做法）

1. 增加 `report`（延迟执行的消息输出）与 `exit_code` 两个局部变量，所有 `except` 分支只负责：
   - `standalone_mode=False` 时按既有契约重新抛出或返回；
   - 否则登记消息与退出码，不立即输出。
2. 在最外层 `try` 的收尾处统一执行 `report()` 与 `sys.exit(exit_code)`；最外层再补一个 `except (EOFError, KeyboardInterrupt)` 兜底，保证迟到的中断不会替换预期结果。
3. 空白行回显、`Aborted!` 消息、`ClickException.exit_code`、EPIPE 的静默包装等既有行为保持不变。

## 验证

- FAIL_TO_PASS：`tests/test_abort_interrupt.py` 中 3 个场景（报告中止、报告错误、成功退出时收到中断）
- PASS_TO_PASS：`tests/test_abort_interrupt.py`、`tests/test_termui.py`、`tests/test_basic.py`
- 修复后：`tests/test_abort_interrupt.py` 8 项通过；`tests/test_termui.py` 264 项通过、18 项跳过；`tests/test_basic.py` 102 项通过

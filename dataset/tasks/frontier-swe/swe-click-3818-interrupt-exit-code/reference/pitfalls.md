# 常见错误

1. **就地给 `echo` 加 try/except**：只保护消息输出，`sys.exit` 与 `e.show()` 期间的窗口仍在，测试的 `interrupt_at=2` 场景会失败。
2. **吞掉所有 `KeyboardInterrupt`**：非 standalone 模式下首个中断必须到达调用者（`Abort`，并以原中断为 `__cause__`），全盘捕获会破坏该契约。
3. **改变退出码**：迟到的中断不能改变原本的退出码（成功为 0，`ClickException` 为其 `exit_code`，中止为 1）。
4. **忽略 `EOFError`**：`Ctrl-D` 与 `Ctrl-C` 在 standalone 模式下走同一条路径，统一处理时不要区别对待成不一致的退出码。
5. **破坏 EPIPE 处理**：`OSError` 且 `errno == errno.EPIPE` 时只做 flush 包装并保持退出码 1，重构 `except` 顺序时容易误伤。
6. **只在测试覆盖的窗口修补**：新测试通过 `isatty` 调用计数选择中断时机，针对计数特判而不解决结构问题会在其他窗口复现。

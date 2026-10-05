# 参考修复分析（基于上游 PR #3769，已合并）

## 根因

`src/click/_termui_impl.py` 的 `ProgressBar` 用 `update_min_steps` 做渲染节流：迭代步进先累积进 `self._completed_intervals`，凑满一个步距才通过 `make_step()` 计入 `pos` 并渲染。

当 `length` 不是 `update_min_steps` 的整数倍时，迭代结束后 `_completed_intervals` 中仍滞留一个不足步距的余量（如 length=20、步距 7：20 = 7+7+6，最后余 6）。`render_finish()` 直接输出收尾，从不结算该余量，于是 `show_pos=True` 时最终显示 `14/20`（只计入了两个完整步距）。

## 修复要点

在 `render_finish()` 开头结算滞留余量：

```python
if self._completed_intervals:
    self.make_step(self._completed_intervals)
    self._completed_intervals = 0
    self.render_progress()
```

结算发生在收尾输出之前，且只在有余量时触发，不影响正常运行期的节流行为，也不触碰 hidden / 非 tty 等分支（它们在结算之后才判断）。

## 验证

- FAIL_TO_PASS：`tests/test_termui.py::test_progressbar_lands_on_final_position`（参数化共 12 例，base 上 6 例失败）
- PASS_TO_PASS：`tests/test_termui.py` 全量（修复后 249 项通过、11 项跳过）

# 外部基准适配器

适配器把外部基准转换为 Dataset Protocol 的任务描述。原则：

- **不 fork 上游数据集**：仓库内只保存上游元数据与转换代码。
- **显式版本固定**：`adapter.yaml` 记录上游版本 / commit 与 adapter 自身版本；上游更新时升级 adapter 并重放转换。
- **许可优先**：按 LICENSING.md 的分级执行。`metadata_only` 与 `local_import` 级别的内容不进 `dataset/`，转换产物先输出到本地暂存区（`imported/`，不入 git），经人工补全与评审后再入库。

## 适配器清单

| 适配器 | 上游 | 再分发分级 | 状态 |
| --- | --- | --- | --- |
| `livecodebench/` | LiveCodeBench | metadata_only | 原型（adapter.py 可用） |
| `hle/` | HLE / HLE-Diamond | metadata_only | 已登记元数据，转换器待实现 |
| `swebench/` | SWE-bench Verified | local_import | 已登记元数据，转换器待实现 |

## 适配器约定

- `adapter.yaml`：上游元数据（名称、主页、许可、再分发分级、版本固定方式）与适配器版本。
- `adapter.py`（可选）：转换器。输入为用户本地合法获取的上游数据，输出为协议任务骨架（meta.yaml + problem.md 占位 + 默认 rubric）。
- 转换器输出必须能通过 `schemas/task.schema.json` 校验。

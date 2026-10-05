# 许可与再分发策略

版权是一级设计约束。公开可访问（Publicly Accessible）的内容不一定允许重新分发（Redistributable），每个来源与任务都必须显式记录其许可状态。

## 1. 本仓库自身的许可

| 部分 | 许可 |
| --- | --- |
| 代码（scripts/、adapters/、schemas/、tests/） | MIT（见 LICENSE） |
| 本仓库原创任务内容（dataset/ 下原创 task bundle） | CC BY 4.0 |
| 外部来源内容 | 以该来源的许可与本文件的再分发分级为准 |

## 2. 再分发分级（redistribution）

每个 `source`（以及由适配器引入的任务）必须标注以下三档之一：

| 级别 | 含义 | 仓库内允许存放的内容 |
| --- | --- | --- |
| `redistributable` | 许可明确允许再分发 | 内容本体 + 署名信息 |
| `metadata_only` | 上游要求不公开再分发，或许可不明确 | 仅 source 元数据、URL、ID、日期、内容 hash |
| `local_import` | 内容可由用户自行合法获取，但仓库不分发 | 元数据 + importer；用户本地执行导入 |

## 3. 当前外部来源的核实结论

以下来自对上游页面的实际核查（核查日期 2026-10-05），后续变动以 `sources/registry.yaml` 的更新为准：

- **HLE / HLE-Diamond**（`cais/hle`，MIT）：上游明确要求不要公开分享、转传或分发数据集内容，以保护基准完整性。尽管许可为 MIT，本仓库按 `metadata_only` 处理。
- **LiveCodeBench**（代码 MIT；HF 数据集卡标注 `license: cc`）：题面聚合自 LeetCode / AtCoder / Codeforces，平台题面的再分发权利不清晰。按 `metadata_only` 处理，题面由用户本地导入。
- **SWE-bench Verified**（`princeton-nlp/SWE-bench_Verified`）：数据集卡未声明许可；记录内容派生自各开源仓库，适用各仓库自身许可。按 `local_import` 处理。
- **Codeforces**：API 不提供题面正文；公开网页在浏览器 UA 下可读（2026-10-05 实测），但未见任何再分发授权。题面、官方题解与官方代码一律按 `metadata_only` 处理：仓库存元数据、hash 与导入器，内容由用户本地获取。
- **Fresh SWE 自采内容**（frontier-swe）：issue 正文与补丁文本来自许可宽松的仓库（当前为 BSD-3-Clause 的 pallets 系列），适用仓库许可、允许再分发。按 `redistributable` 处理并署名；仅对许可明确的仓库开放此通道，其余仍按 `local_import`。

## 4. 每个来源 / 任务必须记录

- `license`：许可标识
- `redistribution`：上述三档之一
- `attribution`：署名文本
- `url`：来源地址
- 适配器引入时另需 `upstream_version` / `upstream_commit` / `adapter`

## 5. 行为准则

- 未经许可确认，不复制第三方完整题面、官方解答或测试数据进仓库。
- 不因为某内容可以从公开网页访问就将其重新发布。
- 校验工具（`scripts/validate.py`）强制检查许可元数据的存在性，缺失即构建失败。

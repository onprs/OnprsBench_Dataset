# 全量评审记录（22 任务，0.5.0 发布前）

- 日期：2026-10-06
- 评审人：AI 代理（未参与任何任务的生产；任务由维护者与其他代理会话生产）
- 范围：`dataset/tasks/` 全部 22 个任务（7 竞赛 + 6 论文 + 9 SWE）
- 依据：`curation/templates/review-checklist.md`、`DATASET_POLICY.md`、`CURATION_GUIDE.md` 第 0 节

## 机械核查项（全量，工具执行）

| 检查项 | 方法 | 结果 |
| --- | --- | --- |
| schema 完备（meta/rubric/suite/verify） | `python scripts/validate.py` | 22/22 通过 |
| 权重和为 1.0、维度 id 唯一 | 同上 | 22/22 通过 |
| 可见性映射无串漏、无未分类文件 | 同上 | 22/22 通过 |
| freshness 分级与日期一致 | 同上 | 22/22 通过 |
| 生命周期/errata 合法 | 同上 | 22/22 通过 |
| verify 契约引用文件存在 | 同上 | 21/21 通过（fp-ski-rental-discount 无契约，属设计） |
| 工具链与数据完整性单测 | `python -m unittest discover tests` | 8/8 通过 |

## 程序判定实测（全量真实执行，非抽样）

使用 OnprsBench_Core 框架（main@94ce233）对每个带 verify 契约的任务，以任务自带参考解
（`reference_solution.*`）或参考修复补丁（`fix.patch`）作为 solver 回答真实执行判定：

| Suite | 实测 | 结果 |
| --- | --- | --- |
| frontier-algorithm（7） | g++ 编译参考解 + 官方样例 + 生成器应力对拍（3 批次 × 100 用例） | 7/7 全过 |
| frontier-paper 实现题（5） | Python 参考解 + 样例 + 应力对拍 | 5/5 全过 |
| frontier-swe（9） | 下载上游仓库快照 + 独立 venv + 应用测试补丁与参考修复 + pytest F2P/P2P | 9/9 全过（目标测试通过且无回归） |

结论：全部 21 个程序判定任务的"答案锚点"可被机械 verifier 独立复核，满足第 0 节红线
（答案锚定官方参考实现 / 上游测试，非 AI 自证）。

## 内容抽查（逐题细读子集）

- `fa-cf2266g-modular-tree`：题面约束（n 总和、取值范围）完整；来源署名与版权标注规范；
  官方参考代码经对拍验证。
- `fp-ot-assignment`：题面输入输出格式、约束（n ≤ 400、费用范围）明确；参考实现锚定
  论文算法并与暴力对拍；rubric 维度（正确性/复杂度）可由第三方客观判定。
- `fp-ski-rental-discount`：旗舰题，anchors 五档齐备；按 CURATION_GUIDE 第 0 节标注为
  协议结构示例任务，其参考解答为人工编写的经典模型变体推导（无机械 verifier），
  维持 active 依赖既有评审记录。

## 未执行项与残留风险（如实记录）

- 未对 22 个任务逐题做人工复算/复证（清单"canonical 结论正确"项以机械 verifier
  全量实测替代；纯文本旗舰题维持既有评审结论）。
- 各任务尚未完成基线模型运行，故本次仅推进 `lifecycle.status: review → active`；
  `lifecycle.stage` 保持 `fresh`（按政策，stage 转 mature 需完成基线运行）。
- 建议维护者对抽查外的任务做抽复审。

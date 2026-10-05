# Curation Guide

本指南规范自有任务（重点是 frontier-paper suite）的生产流程与质量标准。目标能力是"新任务适应能力"：即使模型读过来源论文，也无法靠背答案得分。

## 1. frontier-paper 标准流程

```
Source Discovery
  → Paper Selection
  → Core Contribution Extraction
  → Task Design
  → Reference Construction
  → Rubric
  → Independent Review
  → Baseline Testing
  → active
```

1. **Source Discovery**：从 OpenReview 等允许合法使用的公开科研来源发现近期论文，登记进 `sources/registry.yaml`（缺失时新增条目）。
2. **Paper Selection**：优先选择提出新方法 / 新算法 / 新界限、且核心思想可被改造成新问题的论文。记录选稿理由。
3. **Core Contribution Extraction**：用 2–3 句话写下论文的核心机制与关键假设，作为改造起点。该摘要是内部工作文档。
4. **Task Design**：对核心思想做变换，见第 2 节。
5. **Reference Construction**：独立完成参考解答（canonical + alternatives + proof + pitfalls），参考解答必须可独立验证。
6. **Rubric**：按任务类型设计维度与锚点，见第 3 节。
7. **Independent Review**：由未参与出题的人按 `curation/templates/review-checklist.md` 独立解题并评审。
8. **Baseline Testing**：交由框架对若干基线模型试跑，确认题目可解、rubric 可区分；结果作为 analysis artifact 回流，不写入 meta.yaml。
9. **Active**：合并并在下一次发布进入 active。

## 2. 任务设计模式（论文只是知识来源）

- **条件变换**："如果改变条件 X，该方法是否仍然成立？"要求论证或给出反例。
- **反例构造**："构造一个导致 naive 方法失败的实例。"
- **受限重设计**："在新的资源/信息限制下重新设计算法并分析代价。"
- **证明任务**："证明该方法在该设定下的复杂度下界/收敛率。"
- **迁移失败分析**："指出论文方法不可直接迁移到场景 Y 的原因。"
- **实现任务**："依据论文给出的核心 primitive 实现算法，通过给定测试。"
- **新问题解决**："给定论文的核心 primitive，解决一个新的问题。"

禁止直接搬运"这篇论文说了什么"式的总结题。

## 3. Rubric 设计

- 维度 3–6 个，权重和 1.0，每维至少 0 / 0.5 / 1.0 三档锚点。
- 维度描述必须可判分：写清"满足什么条件给满分"，避免"较好/较差"式措辞。
- 同一 suite 内允许复用维度骨架，每题必须按自身参考答案核对锚点。

## 4. 质量关卡

高价值任务入库前尽可能完成：来源核实 → 题面评审 → 参考解答评审 → rubric 评审 → 独立可解性评审 → judge 行为测试 → 基线模型运行。每关记录在任务提案（`curation/templates/task-proposal.md`）的对应栏目。

## 5. 数量纪律

不追求任务数量。单道经过完整流程的 frontier 任务价值高于批量生成的低质量任务。禁止使用未经人工审核的批量 LLM 生成题。

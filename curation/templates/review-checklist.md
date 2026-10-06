# 独立评审清单

评审人必须是未参与该题生产的人。逐项确认后在提案中勾选。

## 题面

- [ ] 仅凭 solver_visible 内容即可理解题意，无歧义
- [ ] 题面不含答案、提示或指向 reference 内容的线索
- [ ] 所有假设（输入范围、边界、判定规则）写明

## 参考解答

- [ ] 答案锚点在来源中可复核（记录编号/位置/hash），非 AI 自证；来源未覆盖的新推导已有独立复核机制
- [ ] canonical 结论正确，且评审人已独立复算/复证
- [ ] proof 无跳步，分类讨论无遗漏
- [ ] alternatives 中列出的其他解法确实存在且结论正确
- [ ] pitfalls 覆盖了评审人自己差点犯的错误

## Rubric 与 anchor

- [ ] 每个维度的满分条件可被第三方客观判定
- [ ] 权重之和为 1.0，权重分配与题目重心一致
- [ ] anchor 各档与 rubric 维度得分可以对应复算
- [ ] 用 anchor 答案试评一次，judge（或模拟 judge）打分落在预期区间

## 元数据

- [ ] source 许可与再分发分级如实填写
- [ ] contamination 各字段如实填写，transformation 与实际变换一致
- [ ] freshness 日期与分级一致（见 DATASET_POLICY.md）
- [ ] difficulty.author 有填写依据

## 隔离

- [ ] solver_visible 与 judge_visible 无串漏
- [ ] 未引入任何框架内部代码或运行环境依赖

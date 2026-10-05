# 参考解答说明（metadata_only）

本任务的 canonical reference 是 Codeforces 官方题解（思路 + 官方参考代码）：

- 题解：https://codeforces.com/blog/entry/157140 （2269C 小节，Idea: eren__）
- 本地获取：`python scripts/import_cf_task.py --contest 2269 --index C`
- 完整性核对：hash 见 `judge_assets/verify.yaml`

题解内容（文字与代码）权利归 Codeforces 与作者，不复制进本仓库。

## 官方思路要点摘要

官方题解的核心观察：删除过程使中段元素必然入分；剩余前后缀构成对称配对，每对被迫二选一，取较大者贪心最优。详细推导与证明以官方题解原文为准。

## 出题人备注

该题的高区分点在于"证明配对关系"而非代码实现；评判代码正确性由 verifier 承担，judge 如需评估文字说明可对照官方题解。

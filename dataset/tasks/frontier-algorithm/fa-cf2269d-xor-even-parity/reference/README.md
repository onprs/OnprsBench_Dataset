# 参考解答说明（metadata_only）

本任务的 canonical reference 是 Codeforces 官方题解（思路 + 官方参考代码）：

- 题解：https://codeforces.com/blog/entry/157140 （2269D 小节，Idea: _R00T）
- 本地获取：`python scripts/import_cf_task.py --contest 2269 --index D`
- 完整性核对：hash 见 `judge_assets/verify.yaml`

题解内容（文字与代码）权利归 Codeforces 与作者，不复制进本仓库。

## 官方思路要点摘要

官方题解的关键在于发现异或掩码集合 {3,6,9,12,15} 的共同性质（置位数均为偶数）所诱导的奇偶不变量，并证明"偶置位数"恰好刻画了可达成集合；此后每次更新可 O(1) 维护答案。详细推导以官方题解原文为准。

## 出题人备注

该题的高区分点在于不变量发现与可达性证明；代码本身很短，评判由 verifier 承担。

# Roadmap

## 现状（v0.1.0 目标）

- 协议 v1、schema、校验与构建工具、CI
- 1 个完整示例任务（frontier-paper，演示 bundle 结构）
- LiveCodeBench 适配器原型（metadata_only 模式）
- HLE / HLE-Diamond、SWE-bench Verified 的适配器元数据与接入方案

## 第一阶段：MVP 数据集

1. **frontier-paper 首批 10–20 题**（核心投入）
   - 从 OpenReview 等来源选近期论文，按 CURATION_GUIDE 流程生产
   - 每题完成独立评审与基线模型试跑后转 active
2. **外部坐标系接入**
   - HLE / HLE-Diamond adapter：metadata_only，建立 academic suite 的 baseline
   - SWE-bench Verified adapter：local_import，建立 software-engineering suite 的 baseline
   - LiveCodeBench adapter：补全 release_v6 版本固定与本地导入流程
3. **发布机制演练**：完成一次完整 release（构建 → hash → GitHub Release → 框架联调）

## 第二阶段：Fresh SWE

- 从活跃开源项目采集"真实 issue + 已合并修复 PR"配对
- 冻结修复前 repo 状态（base_commit + 环境描述），judge 侧持有 merged patch 与测试
- 优先满足：有测试、有真实修复、可复现、可自动验证
- 形成 frontier-swe 任务生产线

## 第三阶段：Derived 资产规模化

- paper-derived / contest-derived / software-derived 任务流水线半自动化
- procedural 任务生成器（参数化实例 + 程序 verifier）
- 引入 Low-Contamination / Fresh / Derived 切片的报表约定（与框架对齐）

## 持续运营

- 定期核查 sources/registry.yaml 中各来源的许可与 API 变动
- 每季度评估新鲜度结构，维持 F0/F1 任务的稳定供给
- 接收框架回流的 analysis artifact（经验难度、区分度、judge 一致性），指导选题

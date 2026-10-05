# Roadmap

## 现状（v0.2.0）

- 协议 v1、schema、校验与构建工具、CI
- frontier-paper：协议示例任务 1 个（fp-ski-rental-discount）
- frontier-swe：首批 3 个真实任务，全部经本地复现验证（采集器：scripts/collect_fresh_swe.py）
- LiveCodeBench 适配器原型（metadata_only 模式）
- HLE / HLE-Diamond、SWE-bench Verified 的适配器元数据与接入方案

## 第一阶段：MVP 数据集

1. **frontier-swe 扩量**（当前主力，真实来源 + 程序验证）
   - 扩展目标仓库清单（许可宽松、测试完善的活跃项目）
   - 每个任务保持"本地复现验证"门槛
2. **frontier-paper 首批 10–20 题**（人工生产，AI 只能做素材整理与提案草稿）
   - 从 OpenReview / arXiv 选近期论文，按 CURATION_GUIDE 流程由人完成出题与独立评审
   - 候选论文素材库已建立检索通道（近期在线算法 / 流算法 / 学习增强算法论文已核实）
3. **frontier-algorithm 通道**
   - Codeforces 题面无法自动抓取（2026-10-05 实测 403）；改为人工选题 + 衍生改写，或寻找提供合法题面 API 的竞赛源
4. **外部坐标系接入**
   - HLE / HLE-Diamond adapter：metadata_only，建立 academic suite 的 baseline
   - SWE-bench Verified adapter：local_import，建立 software-engineering suite 的 baseline
5. **发布机制演练**：v0.2.0 已构建产物；待框架联调后打 tag 与 GitHub Release

## 第二阶段：Fresh SWE 规模化

- 扩大仓库覆盖与采集频率，形成周期性采集-验证-入库流水线
- 环境复现从本机验证走向容器化（统一 Python/系统依赖）

## 第三阶段：Derived 资产规模化

- paper-derived / contest-derived / software-derived 任务流水线半自动化
- procedural 任务生成器（参数化实例 + 程序 verifier）
- 引入 Low-Contamination / Fresh / Derived 切片的报表约定（与框架对齐）

## 持续运营

- 定期核查 sources/registry.yaml 中各来源的许可与 API 变动
- 每季度评估新鲜度结构，维持 F0/F1 任务的稳定供给
- 接收框架回流的 analysis artifact（经验难度、区分度、judge 一致性），指导选题

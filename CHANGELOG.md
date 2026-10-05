# Changelog

格式遵循 Keep a Changelog；版本号遵循语义化版本。

## [Unreleased]

## [0.2.0] - 2026-10-05

### 新增

- 新 suite `frontier-swe`（layer: fresh）：真实 GitHub issue + 已合并修复 PR 构成的工程任务
- 首批 3 个 Fresh SWE 任务，全部经本地完整复现验证（base 上目标测试失败、应用上游修复后通过、相关测试文件无回归）：
  - `swe-flask-6096-ipv6-partition`（pallets/flask#6093，IPv6 地址解析）
  - `swe-click-3493-echo-empty-bytes`（pallets/click#3487，空字节串 TypeError）
  - `swe-click-3769-progressbar-settle`（pallets/click#3571，进度条余量结算）
- Fresh SWE 采集器 `scripts/collect_fresh_swe.py`（GraphQL 检索 merged PR + 关联 issue + 测试文件，输出暂存区）
- SWE 任务的程序验证契约 `judge_assets/verify.yaml`（环境、FAIL_TO_PASS、PASS_TO_PASS、复现记录）
- 许可政策补充：宽松许可仓库（MIT/BSD/Apache）的 issue 与补丁按 redistributable 入库并署名
- CURATION_GUIDE 增加 Fresh SWE 生产线章节

## [0.1.0] - 2026-10-05

### 新增

- Dataset Protocol v1 文档与 JSON Schema（manifest / suite / task / rubric）
- 数据校验工具 `scripts/validate.py` 与发布构建工具 `scripts/build.py`
- 示例任务 `fp-ski-rental-discount`（frontier-paper，完整 bundle + 五档 anchor）
- LiveCodeBench 适配器原型（metadata_only 模式）
- HLE / HLE-Diamond、SWE-bench Verified 适配器元数据
- 数据来源注册表 `sources/registry.yaml`
- 数据政策（新鲜度分级、生命周期、污染风险）与许可政策文档
- frontier-paper 生产流程文档与提案 / 评审模板
- CI：schema 校验、引用完整性、许可元数据、hash 一致性、单元测试

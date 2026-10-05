# Changelog

格式遵循 Keep a Changelog；版本号遵循语义化版本。

## [Unreleased]

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

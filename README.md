# OnprsBench Dataset

独立、版本化的 LLM 基准数据集。本仓库只负责"测什么"：任务、参考资料、评分标准与元数据。运行评测、调用模型、Judge、存储历史结果与展示由完全独立的 Benchmark Framework 负责，双方仅通过 [Dataset Protocol](PROTOCOL.md) 交互。

## 特点

- 三层数据来源：外部基准（坐标系）、新鲜来源（近期论文 / 竞赛 / GitHub 工程）、衍生任务（核心资产）
- 每道任务是一个完整 bundle：题面 + 参考解答包 + rubric + 元数据，solver 与 judge 可见内容严格分离
- 每题记录新鲜度（F0/F1/F2/Legacy）与污染风险（low/medium/high）
- 任务级 revision、数据集级语义化版本，发布冻结，历史版本长期可获取
- 版权一级约束：逐来源记录许可与再分发策略，不支持再分发的内容以 metadata-only 适配器接入

## 仓库结构

```
dataset/            数据内容（suites + tasks，构建产物 manifest 描述全部数据）
schemas/            Dataset Protocol 的 JSON Schema
scripts/            校验（validate.py）、构建（build.py）与 Fresh SWE 采集（collect_fresh_swe.py）
adapters/           外部基准适配器（上游元数据 + 转换原型）
sources/            数据来源注册表（许可与再分发策略）
curation/           任务提案、生产模板与评审清单
tests/              工具链与数据完整性测试
```

## 快速开始

要求 Python 3.10+。

```bash
pip install -r requirements.txt

# 校验整个数据集（schema、引用、许可元数据、hash 一致性等）
python scripts/validate.py

# 构建发布产物（默认同时生成标准与完整两套，输出到 dist/）
python scripts/build.py --distribution both

# 运行测试
python -m unittest discover tests
```

## 文档

| 文档 | 内容 |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | Dataset Protocol v1：数据集与框架之间的约定 |
| [DATASET_POLICY.md](DATASET_POLICY.md) | 新鲜度分级、生命周期、revision 与污染风险政策 |
| [LICENSING.md](LICENSING.md) | 许可与再分发策略 |
| [CURATION_GUIDE.md](CURATION_GUIDE.md) | frontier-paper 任务生产流程与质量标准 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献方式 |
| [ROADMAP.md](ROADMAP.md) | 数据采集路线图 |
| [CHANGELOG.md](CHANGELOG.md) | 版本变更记录 |

## 版本与发布

数据集使用语义化版本（见 `VERSION`）。每次发布生成带完整 hash 清单的冻结产物，通过 `dataset id + dataset version + dataset commit + manifest hash` 唯一引用。已发布的内容只做 errata 记录，修改以新 revision / 新版本发布。

## 分发形态

同一版本号发布两套产物，任务内容一致：

| 产物 | 内容 | 适用场景 |
| --- | --- | --- |
| `onprsbench-dataset-<version>` | 任务内容（题面、参考解、rubric、判定资产） | 判定资源按需下载；体积小，网络可用时更轻量 |
| `onprsbench-dataset-<version>-full` | 任务内容 + 仓库快照与上游许可（`resources/`） | 安装后判定不联网，适合网络受限或要求判定环境完整复现的场景 |

两套产物的 dataset id、版本号与 commit 相同，框架以 manifest hash 区分并追溯；完整形态的资源随产物给出许可文本与署名。

## 许可

- 代码：MIT（见 [LICENSE](LICENSE)）
- 本仓库原创任务内容：CC BY 4.0
- 外部来源内容：以其 source 元数据中的许可与再分发策略为准，详见 [LICENSING.md](LICENSING.md)

## 贡献

欢迎提交任务提案、评审与适配器改进，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [CURATION_GUIDE.md](CURATION_GUIDE.md)。

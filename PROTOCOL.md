# Dataset Protocol v1

本文档定义数据集仓库与 Benchmark Framework 之间的唯一约定。数据集只描述"测什么"；运行、调用模型、Judge、存储与展示全部属于框架职责。框架通过发布产物中的 `manifest.yaml` 了解数据，不依赖目录结构。

`protocol_version: "1"`

## 1. 版本模型

| 层级 | 标识 | 规则 |
| --- | --- | --- |
| 协议 | `protocol_version` | 不兼容变更时递增 |
| 数据集 | `dataset.version`（语义化版本）+ git commit + manifest hash | 每次发布递增并冻结 |
| 任务 | `task.revision`（整数，从 1 开始） | 已发布任务的任何内容变更必须 +1 |

一次 Run 的完整引用为：`dataset.id + dataset.version + dataset commit + manifest hash`。禁止使用 `latest` 作为历史 Run 的唯一标识。

## 2. 数据集描述（manifest）

`manifest.yaml` 是构建产物（由 `scripts/build.py` 生成），发布时冻结：

```yaml
protocol_version: "1"
dataset:
  id: onprsbench-dataset
  name: OnprsBench Dataset
  version: 0.1.0            # 语义化版本
  release_date: "2026-10-05"
  revision: <git commit sha>
  description: ...
  license: ...              # 汇总说明，细则见 LICENSING.md
suites:
  - id: ...
    name: ...
    description: ...
    layer: external | fresh | derived
    tasks:
      - id: ...
        revision: 1
        title: ...
        type: ...
        tags: [...]
        status: active
        path: tasks/<suite>/<slug>/     # 相对 manifest 的路径
        solver_visible: [ ...相对 task 根的路径... ]
        judge_visible:  [ ... ]
        metadata: { difficulty, freshness, contamination 摘要 }
        hashes:
          bundle_sha256: ...
          files: { "<path>": "<sha256>" }
```

框架只能信任 manifest 中列出的内容；目录结构属于本仓库内部实现，可随时调整（调整不产生协议变更）。

## 3. Task Bundle

逻辑结构：

```
solver_visible:
  problem            # 题面
  assets             # solver 可用的附件
judge_visible:
  canonical_reference
  alternatives
  proof
  pitfalls
  rubric
  judge_assets
  anchors            # judge 校准答案（flagship/canary 任务）
meta:
  meta.yaml          # 生命周期、来源、污染风险、许可等（框架读取，不给 solver）
```

可见性取值：`solver` / `judge` / `meta`。

- 框架必须把 `solver_visible` 以外的内容对 solver 完全隔离。
- `judge_visible` 仅在评分阶段提供给 judge。
- `meta` 用于任务筛选、统计与溯源，不进入 solver 或 judge 的提示词。

本仓库采用的默认布局（构建工具据此推导可见性；仅为仓库内部惯例）：

| 路径 | 可见性 |
| --- | --- |
| `problem.md`、`assets/**` | solver |
| `rubric.yaml`、`reference/**`、`anchors/**`、`judge_assets/**` | judge |
| `meta.yaml` | meta |

任务可以覆盖默认映射：在 `meta.yaml` 的 `visibility_overrides` 中逐路径声明。

## 4. 标识与命名

- `task.id`：全数据集唯一，匹配 `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`，推荐 `<suite前缀>-<语义slug>`。首次进入任一发布后永久不变。
- `suite.id`：同一命名规则。
- 目录名与 id 可以不同，以 manifest 的 `path` 为准。

## 5. Hash 规则

- 文件 hash：对文件原始字节取 SHA-256。
- bundle hash：将 task 内所有文件按 POSIX 风格相对路径（`/` 分隔、UTF-8）字典序排序，逐行拼接 `<relpath>  <sha256>\n`（两个空格分隔），对拼接结果的 UTF-8 字节再取 SHA-256。
- manifest hash：发布产物中 `manifest.yaml` 文件字节的 SHA-256，记录于同目录 `SHA256SUMS` 与 Release 说明。

## 6. 评分 Rubric

每道任务自带 `rubric.yaml`，不同任务类型使用不同维度。rubric 必须给出：维度 id、权重（总和 1.0）、维度说明、评分锚点（至少 0 / 0.5 / 1.0 三档）。总分为各维度加权后的派生结果，数据集不存储"总分"字段。

```yaml
rubric_version: 1
dimensions:
  - id: correctness
    weight: 0.30
    description: ...
    anchors:
      - { score: 0.0, description: ... }
      - { score: 0.5, description: ... }
      - { score: 1.0, description: ... }
```

常用维度建议（各任务可增删）：算法题 `correctness / core_insight / complexity / proof / completeness`；论文任务 `understanding / reasoning / transfer / criticism / counterexample`；Debug 任务 `bug_identification / root_cause / patch_correctness / minimality / regression_risk`。

## 7. Anchor Answer

flagship / canary 任务必须提供 anchor answers（建议 0 / 25 / 50 / 75 / 100 五档），存放于 `anchors/`（judge 可见），用于 judge 校准、judge 一致性测试与 rubric 验证。普通任务可选。

## 8. 元数据（meta.yaml）

必填字段由 `schemas/task.schema.json` 定义，核心包括：

- `lifecycle.status`：`draft | review | active | deprecated | superseded`
- `lifecycle.stage`：`fresh | mature | legacy`（映射规则见 DATASET_POLICY.md）
- `freshness`：`created_at` / `source_published_at` / `dataset_release_at` / `class`（F0/F1/F2/legacy）
- `contamination`：`risk`、`source_publication_date`、`exact_problem_public`、`reference_public`、`transformation[]`、`notes`
- `source`：`kind`、`name`、`url`、`published_at`、`license`、`redistribution`、`attribution`、`upstream_version`、`upstream_commit`、`adapter`
- `difficulty.author`：人工预测难度（`easy | medium | hard | very_hard | frontier`）
- `license`：该任务内容本身的许可

经验难度与区分度由框架根据真实运行结果计算，作为独立 analysis artifact 回流；数据集仓库接收此类产物时单独存放，不覆盖 `meta.yaml`。

## 9. 外部任务接入

外部基准通过 `adapters/` 接入，adapter 负责把上游格式转换为本协议。adapter 元数据记录 `upstream`（名称、主页、许可、再分发策略、版本/commit 固定方式）与 `adapter.version`。上游更新时升级 adapter 并重放转换，禁止 fork 整个外部数据集进本仓库。再分发策略分级见 LICENSING.md。

## 10. 稳定性承诺

- 已发布（进入任一 release）的任务内容不可原地修改；修正错误通过 errata 记录 + `revision + 1` + 新数据集版本发布。
- 被替代的任务标记 `status: superseded` 并填写 `superseded_by`。
- 协议新增可选字段不递增 `protocol_version`；删除或改变既有字段语义才递增。

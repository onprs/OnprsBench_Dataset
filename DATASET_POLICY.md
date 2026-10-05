# Dataset Policy

本文件是数据政策的唯一权威来源。以下边界与规则以文档为准，代码中的常量仅为便于校验的镜像。

## 1. 新鲜度分级

以 `source_published_at → dataset_release_at` 的时间差计算：

| 级别 | 时间差 |
| --- | --- |
| F0 | ≤ 7 天 |
| F1 | 8–30 天 |
| F2 | 31–180 天 |
| Legacy | > 180 天 |

无外部来源的任务（如人工原创），以 `created_at → dataset_release_at` 计算。

## 2. 生命周期

任务状态（`lifecycle.status`）：

```
draft → review → active → deprecated
                         → superseded（须填写 superseded_by）
```

新鲜内容的成熟阶段（`lifecycle.stage`，按发布后的时间与验证进度推进）：

- `fresh`：新入库，尚未完成基线模型运行
- `mature`：完成全部评审与基线运行
- `legacy`：进入 Legacy 新鲜度区间

## 3. 修改与勘误

- 已发布任务的任何内容变更：`task.revision + 1`，并随新数据集版本发布。
- 发现的错误先记录 `errata`（meta.yaml 内），再修订。
- 禁止在不 bump revision / version 的情况下改动已发布内容。

## 4. 污染风险分级

`contamination.risk` 判定标准：

| 级别 | 含义 |
| --- | --- |
| low | 题目为衍生/原创，且来源内容在公开渠道不易被逐字检索到 |
| medium | 来源公开可检索，但题目经过实质变换（条件、目标、约束等） |
| high | 题面或参考解答与公开内容高度重合，模型可能在训练数据中见过 |

每题必须如实填写 `exact_problem_public`、`reference_public` 与 `transformation` 列表。

## 5. 难度

`difficulty.author` 仅为作者预测，取值 `easy | medium | hard | very_hard | frontier`。经验难度与区分度由框架基于真实运行计算，数据集不预填、不伪造统计值。

## 6. 评分

- 每题自带 rubric，维度权重总和必须为 1.0。
- 有确定答案的任务优先提供程序化 verifier（`judge_assets/`）。
- 开放式任务以 reference pack + rubric + anchors 支撑 judge。
- 总分是维度加权的派生结果，由框架计算。

## 7. 统计维度建议

框架可按以下切片汇报：Overall、Low-Contamination、Fresh（F0+F1）、Derived、Procedural。切片定义由框架实现，数据集保证 `contamination`、`freshness`、`source.kind` 字段完备以支持切片。

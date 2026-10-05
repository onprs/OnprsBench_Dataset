# 贡献指南

## 环境准备

```bash
pip install -r requirements.txt
python scripts/validate.py    # 提交前必须通过
```

## 贡献方式

1. **提交任务提案**：复制 `curation/templates/task-proposal.md` 填写，先发提案再写完整任务。
2. **提交任务**：按 `CURATION_GUIDE.md` 的流程生产，放入 `dataset/tasks/<suite>/<slug>/`。
3. **改进适配器**：见 `adapters/README.md`。
4. **修复数据错误**：修改已发布任务时必须 `revision + 1` 并在 meta.yaml 记录 `errata`。

## PR 检查清单

- [ ] `python scripts/validate.py` 通过
- [ ] `python -m unittest discover tests` 通过
- [ ] 每个新任务的 source 许可与再分发分级填写完整（见 LICENSING.md）
- [ ] solver_visible 与 judge_visible 无串漏（题面不含答案线索，参考包不含对 solver 的暗示性描述）
- [ ] 新任务初始 `revision: 1`、`status: draft` 或 `review`
- [ ] 未提交任何 API key、运行结果、个人配置
- [ ] CHANGELOG.md 的 Unreleased 段落已更新

## 目录约定速查

- 题面与 solver 附件：`problem.md`、`assets/`
- 评判材料：`reference/`、`rubric.yaml`、`anchors/`、`judge_assets/`
- 元数据：`meta.yaml`

详细协议见 [PROTOCOL.md](PROTOCOL.md)。

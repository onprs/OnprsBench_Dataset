# Changelog

格式遵循 Keep a Changelog；版本号遵循语义化版本。

## [Unreleased]

### 修复

- 新增 `.gitattributes`（`dataset/** -text`）：禁止 git 换行符转换，保证工作区文件字节与仓库对象一致（bundle hash 按原始字节计算，Windows 上 core.autocrlf=true 的 checkout 会破坏 hash 稳定性）
- `build.py` 写出 manifest.yaml 与 SHA256SUMS 时固定 LF 换行，保证同一内容跨平台构建出相同的 manifest hash（0.4.0 及之前版本的 manifest.yaml 为 CRLF 字节，发布产物自洽不受影响；本修复对后续版本生效）

### 改进

- PROTOCOL.md 框架环境义务补充：安装数据集时预取判定契约所需的仓库快照，Run 判定时缓存未命中再重试

### 新增

- frontier-swe 新增 6 个高难真实工程任务，均完成本地完整复现验证（base 上目标测试失败、应用上游修复后通过、相关测试文件无回归）：
  - `swe-werkzeug-3243-converter-strictness`（pallets/werkzeug#3242，`int`/`float` URL 转换器的取值校验与构建语义）
  - `swe-click-3818-interrupt-exit-code`（pallets/click#3802，报告中止/错误期间的迟到 `KeyboardInterrupt` 不再逃逸）
  - `swe-urllib3-5254-http2-probe-lock`（urllib3/urllib3#5206，HTTP/2 探测缓存等待线程的锁释放）
  - `swe-attrs-1593-classvar-forward-ref`（python-attrs/attrs#1575，Python 3.14 下未导入 `ClassVar` 的 ForwardRef 判定）
  - `swe-sympy-30530-inequality-singularities`（sympy/sympy#30529，`reduce_inequalities` 保留分母奇点）
  - `swe-sympy-30396-array-scalar-print`（sympy/sympy#30395，纯标量赋值与逐元素函数打印）
- `sources/registry.yaml` 新增 urllib3（MIT）、attrs（MIT）、sympy（BSD-3-Clause）来源条目
- frontier-algorithm 新增 5 个高难题（Codeforces Round 1121/1122/1124，rating 2200–2700），全部经官方参考代码与暴力对拍验证：
  - `fa-cf2268c-energy-intervals`（Round 1124 Div.1 C，rating 2300）
  - `fa-cf2268d-aghabalasar-hamed`（Round 1124 Div.1 D，rating 2600）
  - `fa-cf2268e-tree-of-life`（Round 1124 Div.1 E，rating 2700）
  - `fa-cf2266g-modular-tree`（Round 1122 Div.3 G，rating 2200）
  - `fa-cf2264e2-prime-flood`（Round 1121 Div.2 E2，rating 2700）

## [0.4.0] - 2026-10-06

### 修复

- frontier-algorithm 两个竞赛任务（`fa-cf2269c-k-important`、`fa-cf2269d-xor-even-parity`）的 verify.yaml：`evaluation.reference_solution` 由描述文本修正为机器可读路径，并显式声明 `samples` 路径；判定语义不变（revision 2）

### 新增

- `schemas/verify.schema.json`：程序判定契约（verify.yaml）的 JSON Schema，覆盖工程修复与竞赛代码两类契约；`scripts/validate.py` 对 verify.yaml 做 schema 校验并检查契约引用文件存在
- PROTOCOL.md 新增程序判定契约（第 8 节）、Solver 输出契约（第 9 节）与框架环境义务（第 10 节）


## [0.3.0] - 2026-10-05

### 新增

- frontier-algorithm 首批 2 个真实竞赛任务（Codeforces Round 1124 Div.2，2026-09-26，新鲜度 F1）
  - `fa-cf2269c-k-important`（rating 1200）
  - `fa-cf2269d-xor-even-parity`（rating 1500）
- Codeforces 本地导入器 `scripts/import_cf_task.py`（题面 / 官方题解 / 官方参考代码的本地下载与 hash 核对）
- 竞赛任务内容按 research_archive 政策归档入库：题面（problem.md）、官方题解（reference/editorial.md）、官方参考代码（judge_assets/reference_solution.cpp）、官方样例（judge_assets/samples.json），均署名并记录上游 hash
- 竞赛任务对拍验证工具（生成器 + 暴力基准，judge_assets/）：官方参考代码已与暴力完成对拍（C 题 500 例、D 题 300 例，另均通过官方样例）

### 改进

- frontier-algorithm suite 调整为 fresh 层：真实新题按 metadata_only 接入，judge 锚定官方题解而非衍生改写
- 文档更新 Codeforces 通道的可用获取方式（浏览器 UA 可读公开页，内容仍不入库）

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

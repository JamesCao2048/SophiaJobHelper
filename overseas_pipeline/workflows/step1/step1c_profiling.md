# Phase C: 分类与画像

> **子步骤文件** — 由 `workflows/step1_research.md` 分派，不可独立执行。

---

## 并行执行策略

Phase B 完成（B4 `faculty_data.json` 写入后），**立即并行启动以下任务**：

```
B4 完成
  ├─► C1（规则卡初始化）
  ├─► C2（HCI 密度分级）       ← 运行分类器脚本
  ├─► C3（院系四维画像·初步）   ← 用已有信号先评估，后续可更新
  ├─► C4（战略情报·A/B/C 并行） ← 内部三子任务开 subagent
  └─► C5（课程目录抓取）

C4-B 完成 → 触发 C3 维度二次更新（cluster 数据写入后修正维度评分）
C5 完成   → 触发 C3 课程维度更新（课程设置信号写入后修正）
C1/C2/C3/C4/C5 全部完成 → C6（数据审查与补全）
```

> **实现方式**：每个并行任务使用 Task 工具开独立 subagent（`subagent_type: Bash`），主 agent 等待所有子任务返回后执行 C6。

---

### C1. 生成并同步院系规则卡（强制）

- 规则卡主路径：`region_knowledge/schools/{school_id}/{dept_id}.md`
- 运行期副本路径：`output/{school_id}/{dept_id}/knowledge/{dept_id}.md`
- 若主路径不存在：按 `templates/knowledge/department_rule_card_template.md` 创建
- 若主路径已存在：在其基础上增量更新，不覆盖手工补充内容
- Step 1 完成后执行双写入同步：
  1. 先写入 `output/{school_id}/{dept_id}/knowledge/{dept_id}.md`
  2. 再同步到 `region_knowledge/schools/{school_id}/{dept_id}.md`
- `step1_summary.md` 需记录：
  - 本次是否复用了同校其他院系规则卡
  - 复用了哪些字段
  - 双写入同步是否成功

### C2. HCI 密度分级

读取策略文件：`overseas_pipeline/strategies/hci_density_strategy.md`（理解各策略标签的内涵，用于后续撰写 `strategy_rationale`）

```bash
python overseas_pipeline/src/hci_density_classifier.py \
  --input output/{school_id}/{dept_id}/faculty_data.json \
  [--target-dept "{目标系名称}"]
```

自动推断双层密度（target_dept + faculty_wide）和策略标签，写入 `faculty_data.json` 的 `hci_density` 字段。**agent 随后补充 `strategy_rationale`**（自然语言解释，检查边界情况）。

### C3. 生成院系四维画像（dept_profile）

读取策略文件：`overseas_pipeline/strategies/dept_type_strategy.md §一`

1. **官方分类**：从院系名称关键词匹配 `official_category`（cs/ischool/ds/aix/other）
2. **建院背景**：爬取院系 About / History 页面，提取 `founding_year` / `founding_method` / `founding_motivation`
3. **四维评估**：综合以下信号，对每个维度评定 high/medium/low：
   - JD 内容（关键词、研究要求）
   - 院系名称 + 建院背景
   - Faculty background 分布（Phase B 已统计的 major/minor 结果）
   - Research cluster 方向（C4 完成后可更新）
   - 课程设置（C5 完成后可更新）
4. **用户审核触发**：若维度存在不确定性（信号矛盾或置信度低），在 `step1_summary.md` 生成 `⚠ 院系维度需确认` 区块

写入 `faculty_data.json → dept_profile`（格式见 `../references/faculty_data_schema.md`）

**step1_summary.md 中的院系画像报告格式：**

```
📋 院系画像：{官方院系名称} ({大学名称})

官方分类：{official_category}
建院背景：{年份} / {founding_method} / {founding_motivation 摘要}

维度评估：
  定量严谨性偏好(QR)：  [low/medium/high]（依据：{2-3 条证据}）
  跨学科开放度(IO)：    [low/medium/high]（依据：{2-3 条证据}）
  系统构建偏好(SB)：    [low/medium/high]（依据：{2-3 条证据}）
  社会影响关注度(SI)：  [low/medium/high]（依据：{2-3 条证据}）

⚠ 如需修正，回复：维度名 新等级（如 "QR medium"）
```

### C4. 采集院系战略情报

读取策略文件：`overseas_pipeline/strategies/dept_type_strategy.md §一`

**可并行执行**：A/B/C 三个子任务各开 subagent，主 Agent 等待汇总后写入 `faculty_data.json → strategic_intelligence`。

#### A. 学院级战略方向（始终执行）

- 从院系主页找 About / Strategic Plan / Vision / Research Themes 链接
- 爬取并提取：愿景声明、战略优先级、近期大额资助（NSF Institute、重大合作等）
- 原始内容保存到 `raw/strategic_plan.md`

#### B. Research Cluster 深度分析（始终执行）

- 从院系页面识别所有 research cluster / group / lab / center
- 对每个 cluster 爬取子页面（`python src/web_fetch_utils.py "cluster URL"`），提取：
  - 最新项目（近 2 年）及研究方向
  - 成员列表（与 Phase B faculty 数据交叉对应）
- 识别与 Sophia 最相关的 2-3 个 cluster，标记 `alignment_with_sophia`（high/medium/low）及原因
- 原始内容保存到 `raw/cluster_{cluster_name}.md`
- **C3 更新**：cluster 方向信息写入后，可修正对应维度评分（如 cluster 含 ethics/social center → SI 可能上调）

#### C. 跨学院扫描（条件触发）

**触发条件**：`dept_profile.dimensions.interdisciplinary_openness == "high"` 且 JD 含关键词 `"interdisciplinary"` / `"cross-faculty"` / `"collaboration across schools"` / `"joint appointment"`

- 从目标大学官网找 2-3 个最相关的其他学院（优先级：医学院/公共卫生 > 教育 > 公共政策 > 商学院）
- 爬取各学院 faculty 页面，找与 Sophia 研究有交集的教授
- 记录合作角度（如"临床对话分析"、"教育技术评估"）

**汇总后写入** `faculty_data.json → strategic_intelligence`（格式见 `../references/faculty_data_schema.md`）

### C5. 抓取课程目录

```bash
python overseas_pipeline/src/course_catalog_scraper.py \
  --url "{目标系课程页面URL}" \
  --output output/{school_id}/{dept_id}/faculty_data.json \
  --school "{学校名}"
```

五层 fallback 抓取课程列表：
- 原始内容**始终保存**到 `output/{school_id}/{dept_id}/raw/course_catalog_raw.md`
- 正则提取结果写入 `faculty_data.json` 的 `department_courses` 字段
- 如课程页面 URL 未知，用 Tavily 搜索 `site:{domain} course catalog`

**⚠ 如果五层 fallback 全部失败（如 JS 渲染 + SSO 登录），必须使用 WebSearch 兜底：**
```
WebSearch: "{学校名} {院系名} course COMPSCI HCI AI 2025 2026"
WebSearch: "{学校名} DATASCI courses"
```
将 WebSearch 返回的课程编号记录到 `raw/course_catalog_search.md`，并标注 `verified: true`。
**禁止**使用"近似"课程编号——必须通过至少一种方式验证课程编号的真实存在性。

**agent 随后审查**（参照 `overseas_pipeline/strategies/hci_density_strategy.md` 中的课程优先级逻辑）：
- 若 `department_courses` 为空（正则提取失败），读取 `raw/course_catalog_raw.md` 直接识别课程
- 识别 Sophia 能教的课，按 `hci_density.strategy` 对应的密度策略排序（density_strategy_priority 字段）
- 将识别结果写回 `faculty_data.json` 的 `department_courses` 字段

### C6. 数据审查与补全

- 检查密度分类是否有边界遗漏
- 补充 `hci_density.strategy_rationale` 自然语言解释
- 将密度判断 + 课程匹配概览写入 `step1_summary.md`
- 生成 `data_quality.json`（规范见 `../references/data_quality_spec.md`）

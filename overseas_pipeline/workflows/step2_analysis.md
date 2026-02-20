# Step 2: Fit Analysis（分析匹配度）

## 前提

Step 1 已完成（`output/{school_id}/{dept_id}/faculty_data.json` 存在）

---

## 执行步骤

1. 读取 `output/{school_id}/{dept_id}/faculty_data.json`（含 `hci_density` 和 `department_courses` 字段）
2. 确定 region → 读取 `region_knowledge/regions/{region}.md`
3. 读取院系规则卡（用于覆盖地区卡差异）：
   - 主路径：`region_knowledge/schools/{school_id}/{dept_id}.md`
   - 副本路径：`output/{school_id}/{dept_id}/knowledge/{dept_id}.md`
   - 若主路径不存在但副本存在，读取副本并在 `step2_summary.md` 标注 "using_output_copy"
   - 若两者都不存在，按 "无院系覆盖规则" 继续并在 `step2_summary.md` 标注缺失
4. 读取策略文件：
   - `overseas_pipeline/strategies/hci_density_strategy.md`（所有地区）
     - 根据 `hci_density.strategy` 确定点名优先级和课程匹配顺序
   - `overseas_pipeline/strategies/nz_te_tiriti_strategy.md`（仅 region=new_zealand）
5. 爬取职位 JD 原文：
   - `python overseas_pipeline/src/faculty_scraper.py --url "{job_url}" --output-type raw`
   - 或请用户提供 JD 文本
   - 保存到 `output/{school_id}/{dept_id}/raw/jd_*.md`
6. **⚠ 扫描 JD 页数限制（必须在生成 fit_report 前完成）：**

   在 JD 原文中搜索页数相关关键词（大小写不敏感）：
   - `"not exceeding"`, `"no more than"`, `"maximum"`, `"up to"`, `"limited to"`
   - `"X pages"`, `"X-page"`, `"within X pages"`
   - 常见组合：`"research statement of no more than 3 pages"`, `"2-page teaching statement"`

   **默认页数（JD 未指定时使用）：**

   | 材料 | 默认页数 |
   |------|---------|
   | Cover Letter | 2 页 |
   | Research Statement | 4 页（TT），2-3 页（NTT） |
   | Teaching Statement | 2 页 |
   | Diversity Statement | 1 页（JD 要求 2 页时扩展） |
   | Selection Criteria Response | 按 criteria 数量，通常 6-10 页 |

   **如 JD 指定了与默认不同的页数要求：**
   - 在 `fit_report.md` 各材料调整建议中标注：`⚠ JD 明确要求：X 页（覆盖默认 Y 页）`
   - 在 `step2_summary.md` 顶部生成**页数偏差警示区块**（格式见下）
   - Step 3 优先使用 JD 要求的页数，不使用默认值
6. 读取 Sophia 全套材料：
   - `overseas_pipeline/materials/Research_Statement.md`
   - `overseas_pipeline/materials/Teaching_Statement.md`
   - `overseas_pipeline/materials/cv_latest.md`
   - `overseas_pipeline/materials/Impact_Statement.md`（如存在）
7. **⚠ 规则冲突检查（关键）**：（原步骤编号顺延）
   - 比较 JD 要求与地区规则卡的规则
   - 如发现冲突，**立即暂停**，显示冲突详情和处理选项（见下）
8. **Te Tiriti 矩阵分析（仅 region=new_zealand）：**（原步骤编号顺延）

   a. 读取 `faculty_data.json → te_tiriti` 块（Step 1 已填充的 jd_signal、school_signal、strategy）
   b. 读取 Sophia 材料识别可 Claim 的经历锚点（`materials/Research_Statement.md`, `materials/Teaching_Statement.md`）
   c. 确认/调整策略标签：
      - 如需调整，在 `strategy_rationale` 中记录理由
      - 典型上调：JD 是 `boilerplate` 但已知该校（Auckland/VUW）面试必考条约题 → 上调一级
      - 典型维持：school_signal=`strong` 但 JD 无任何条约词 → 维持矩阵结果（不下调）
   d. 填充 `faculty_data.json → te_tiriti.strategy_rationale`
   e. 在 fit_report 中生成 **Te Tiriti 评估** 专节（格式见下）

9. 生成 `output/{school_id}/{dept_id}/fit_report.md`（见格式规范）
9. 生成 `output/{school_id}/{dept_id}/fit_report.sources.md`

---

## fit_report.md 格式

```markdown
# {学校} {院系} -- 匹配分析报告

## 基本信息
- 院系：
- 地区 / 规则卡：{region} / `region_knowledge/regions/{region}.md`
- 职级：
- 职位类型：TT / NTT / Teaching-track（影响 CV 变体选择）
- Deadline：
- 薪资：
- 职位链接：

## Fit Score: X/10

## 各维度评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 研究方向匹配 | X/10 | |
| 教学匹配 | X/10 | |
| 区域适配 | X/10 | |
| 职位类型适配 | X/10 | |
| HCI 密度策略 | X/10 | `{strategy}` |

## 匹配维度分析

### 研究方向匹配 (X/10)
...

### 教学匹配 (X/10)
...

### 区域适配 (X/10)
...

### HCI 密度策略分析 (`{strategy}`)

- 目标系 HCI 密度：{level}（{count} 人）
- 学院 HCI 密度：{level}（{count} 人）
- 推荐策略：`{strategy}`
- 策略要点：
  - 对目标系评委：{具体修辞建议}
  - 点名优先级：{目标系教授} → {跨系补充（如有）}

### Te Tiriti 评估（仅 region=new_zealand）

**JD 信号: `{level}`**
> "{原文摘录}" ({所在板块/bullet})
> "{原文摘录}" ({所在板块/bullet})
<!-- 若 no_mention：说明"实质性板块未发现条约相关关键词，仅有 EEO 样板" -->

**学校信号: `{level}`**（来源：学校卡，assessed {date}）
> "{原文摘录}" ([{文档名}]({URL}))
> "{原文摘录}" ([{文档名}]({URL}))
> 专有框架: {框架名} | 核心术语: {术语列表}
<!-- 若无框架：说明"未发现专有框架，仅有标准 acknowledgement" -->

**矩阵结果: `{strategy_label}`**
<!-- 如有上调/下调，注明理由 -->

**Sophia 经历锚点（Step 3 参考）：**
- Kāwanatanga 可 Claim：{参与式设计方法论 / 跨学科协作经历}（来自 Research_Statement.md）
- Tino Rangatiratanga 可 Claim：{trustworthy AI 研究 / MindCoder.ai/CollabCoder 人类控制权设计}
- Ōritetanga 可 Claim：{AI 风险批判性研究立场 / 多元背景学生指导经验}

**Per-document 建议（参照 strategies/nz_te_tiriti_strategy.md §五 `{strategy_label}` 节）：**
- **Cover Letter**: {具体指示，标注哪些用 Claim 框架，哪些用 Aspire 框架}
- **Research Statement**: {是否需要独立小节，节名，字数范围}
- **Teaching Statement**: {是否需要 Māori/Pasifika 段，字数范围}
- **该校术语提醒**: {如需引用专有术语，列出术语 + 来源 URL}

### 关键决策人分析（材料写给谁看）

| 阶段 | 决策人 | 看什么 |
|------|--------|--------|
| 初筛 | 搜寻委员会 | ... |
| 面试 | ... | ... |
| 最终 | 系主任 | ... |

### 各材料调整建议

#### Cover Letter
- **页数**：2 页（JD 未指定时默认）{如 JD 有要求加：⚠ JD 明确要求：X 页（覆盖默认 2 页）}
- **密度策略** [`{strategy}`]：{具体修辞建议}
- **点名建议**：
  - 目标系（优先）：{教授 + 合作点}
  - 跨系补充（如需）：{教授 + 合作点}
- 其他定制点：...

#### Research Statement / Research Interests
- **页数**：4 页 TT / 2-3 页 NTT（JD 未指定时默认）{如 JD 有要求加：⚠ JD 明确要求：X 页（覆盖默认 Y 页）}
- **密度策略** [`{strategy}`]：{硬化/愿景化程度}
- 具体修改点：...

#### Teaching Statement
- **页数**：2 页（JD 未指定时默认）{如 JD 有要求加：⚠ JD 明确要求：X 页（覆盖默认 2 页）}
- **密度策略** [`{strategy}`]：{课程呈现顺序}
- **课程匹配**（来自 department_courses）：
  - 可教现有课：{课程代码 + 名称}
  - 可开新课：{名称}
- 其他修改点：...

#### Diversity Statement
- 是否需要提交：{是 / 否（JD 未要求）}
- **页数**：1 页（JD 未指定时默认）{如 JD 有要求加：⚠ JD 明确要求：X 页（覆盖默认 1 页）}
- 定制方向：{提及该校具体 diversity 项目或学生构成}

#### CV
- 变体选择：`{base / ntt / metrics-first / cv-analytique / dach}`（见 workflows/cv_strategy.md）
- 触发原因：{职位类型 NTT / 地区 Italy 等}
- 如为 `base`：直接提交，无需修改

#### Selection Criteria Response（如为澳洲职位）
...（逐条列出 criterion + 回应框架）

### 规则冲突记录

| 冲突项 | 规则卡规定 | JD 要求 | 处理方式 |
|--------|-----------|---------|---------|
| ... | ... | ... | 以 JD 为准 |

### 风险提示
...

### 投递建议
- 是否建议投递：
- 优先级：my favorite / worth trying / low priority
- 理由：...
```

---

## step2_summary.md 页数偏差警示区块格式

**当 JD 指定与默认值不同的页数时，在 step2_summary.md 顶部插入此区块（让用户在开始 Step 3 之前看到）：**

```markdown
## ⚠ 页数要求偏差（JD 覆盖默认值）

| 材料 | 默认页数 | JD 要求 | 备注 |
|------|---------|---------|------|
| Research Statement | 4 页 | **3 页** | JD 原文："research statement of no more than 3 pages" |
| Teaching Statement | 2 页 | **1 页** | JD 原文："one-page teaching statement" |

> Step 3 将按 JD 要求的页数生成，不使用默认值。如对此有异议，请在开始 Step 3 前告知。
```

如无偏差，step2_summary.md 中不出现此区块。

---

## 规则冲突处理流程

```
⚠ 发现规则冲突，暂停流水线。

【地区卡规则】{具体规则内容}（来源：{source URL}）
【JD 实际要求】{JD 中的具体要求}（来源：{job URL}）

请选择处理方式：
A. 以该校 JD 为准（本次），记录到学校卡
B. 以该校 JD 为准，同时标记地区卡 needs_review
C. 忽略冲突，仍按地区卡执行

请回复 A、B 或 C。
```

# fit_report.md 完整模板

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step2_analysis.md` step 10

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

## 院系画像（来自 dept_profile）

| 维度 | 评级 | 置信度 | 关键证据 |
|------|------|--------|---------|
| 定量严谨性 (QR) | high/medium/low | high/medium/low | {证据摘要} |
| 跨学科开放度 (IO) | high/medium/low | high/medium/low | {证据摘要} |
| 系统构建偏好 (SB) | high/medium/low | high/medium/low | {证据摘要} |
| 社会影响关注 (SI) | high/medium/low | high/medium/low | {证据摘要} |

- **官方分类**：{cs / ischool / ds / aix / other}（仅作人类参考，策略由维度驱动）
- **建院背景**：{建院时间 + 方式 + 动机简述（如有）}
- **Faculty 背景分布**：{major 类别统计，如"hci_qual×3, hci_systems×2, nlp×1"}
- **维度说明**：{如有矛盾信号或边界情况，在此标注}
{如有不确定维度：> ⚠ 以下维度置信度低，请确认后进入 Step 3：QR=medium（信号矛盾：JD 要求 methodological rigor 但 faculty 以 qual 为主）}

## 各维度评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 研究方向匹配 | X/10 | |
| 教学匹配 | X/10 | |
| 区域适配 | X/10 | |
| 职位类型适配 | X/10 | |
| HCI 密度策略 | X/10 | `{strategy}` |
| 院系类型对齐 | X/10 | QR={level}, IO={level}, SB={level}, SI={level} |

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

### 院系类型策略分析（来自 dept_type_strategy.md）

**维度组合**：QR={level} / IO={level} / SB={level} / SI={level}

**技术伪装程度**（由 QR 驱动）：
- {high → 全面 CS 技术语言，系统架构/算法贡献优先 / medium → 技术为主，可保留部分用户研究叙述 / low → 可用社科语言，定性方法直接呈现}

**术语体系**（Cover Letter / Research Statement 使用）：
- 技术类术语：{如 agentic AI evaluation, computational approach to qualitative analysis}
- 跨学科术语：{如 human-centered design, participatory research}（IO=high 时使用）
- 社会影响术语：{如 AI governance, equity, trustworthy AI}（SI=high 时使用）

**主推论文排序**（参照 dept_type_strategy.md §四）：
1. {P1：首推论文 + 原因}
2. {P2：次推论文 + 原因}
3. {P3（可选）}

**经费叙事方向**（参照 dept_type_strategy.md §五）：
- {如 QR=high → 强调 NSF CISE/IIS 主线 / IO=high → 加入 NSF SBE / NIH / 基金会多元渠道}

**院系战略对齐**：
- 学校战略优先项：{如 AI for Health, Digital Futures}
- Sophia 研究对齐点：{如 MindCoder.ai ↔ AI for Health: clinical decision support integration}
- 最相关 Research Cluster：{名称 + 与 Sophia 的具体结合点}
- 跨学院合作机会（IO=high 时）：{合作院系 + 潜在合作教授 + 合作角度}

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

### AU Indigenous 评估（仅 region=australia）

**JD 信号: `{level}`**
> "{原文摘录}" ({所在板块/bullet})
> "{原文摘录}" ({所在板块/bullet})
<!-- 若 no_mention：说明"实质性板块未发现原住民相关关键词，仅有 EEO 样板" -->

**学校信号: `{level}`**（来源：学校卡，assessed {date}）
> "{原文摘录}" ([{文档名}]({URL}))
> "{原文摘录}" ([{文档名}]({URL}))
> RAP tier: {tier} | 原住民战略: {名称或N/A} | 学术支持中心: {名称或N/A}
<!-- 若 light：说明"仅发现标准 Acknowledgement of Country，无专门战略文件" -->

**矩阵结果: `{strategy_label}`**
<!-- 如有上调，注明理由；如为 strong/full_rap，显示升级门槛验证提示 -->

**Sophia 经历锚点（Step 3 参考，参照 strategies/au_indigenous_strategy.md §五）：**
- Relationships 可 Claim：{参与式设计长期合作 / 跨文化协作经历}（来自 Research_Statement.md）
- Respect 可 Claim：{trustworthy AI 研究 / MindCoder.ai/CollabCoder 人类控制权设计}
- Opportunities 可 Claim：{AI 偏见批判性研究立场 / 多元背景学生指导经验}

**Per-document 建议（参照 strategies/au_indigenous_strategy.md §六 `{strategy_label}` 节）：**
- **Cover Letter**: {具体指示，标注哪些用 Claim 框架，哪些用 Aspire 框架，字数范围}
- **Research Statement**: {是否需要独立小节，节名，字数范围}
- **Teaching Statement**: {是否需要 First Nations 学生支持段，字数范围}
- **KSC Response**: {如有原住民相关 criteria，推荐 STAR/CAR 结构 + 具体 Claim 锚点}

### 关键决策人分析（材料写给谁看）

| 阶段 | 决策人 | 看什么 |
|------|--------|--------|
| 初筛 | 搜寻委员会 | ... |
| 面试 | ... | ... |
| 最终 | 系主任 | ... |

### 各材料调整建议

#### Cover Letter
- **页数**：2 页（JD 未指定时默认）{如 JD 有要求加：⚠ JD 明确要求：X 页（覆盖默认 2 页）}
- **技术伪装程度**（QR={level}）：{具体修辞基调——全面技术语言 / 技术为主偶用社科 / 可直接呈现定性}
- **密度策略** [`{strategy}`]：{点名结构和顺序}
  - 目标系（优先）：{教授 + 合作点}
  - 跨系补充（如需）：{教授 + 合作点}
- **院系战略对齐段落**（IO=high 或 SB=high 时建议加入）：{与目标院系/学校最新战略方向的对齐叙述}
- **跨学院合作段落**（IO=high 时必须加入，medium 时酌情）：{跨系合作潜在对象 + 合作角度}
- **经费叙事**：{主要经费来源定位，如 NSF CISE + NIH}
- 其他定制点：...

#### Research Statement / Research Interests
- **页数**：4 页 TT / 2-3 页 NTT（JD 未指定时默认）{如 JD 有要求加：⚠ JD 明确要求：X 页（覆盖默认 Y 页）}
- **技术伪装程度**（QR={level}）：{硬化/愿景化程度，参照 dept_type_strategy.md §二 2.1}
- **密度策略** [`{strategy}`]：{如 pure_pioneer → 系统架构图优先，specialist → 理论贡献优先}
- **主推论文**：{P1 + P2 + 可选 P3，参照 dept_type_strategy.md §四}
- **方法论处理**（V5 原则）：{定性方法直接呈现 + 系统构建并举，不伪装为语义计算}
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
- 变体选择：`{base / ntt / metrics-first / cv-analytique / dach}`（见 strategies/cv_strategy.md）
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

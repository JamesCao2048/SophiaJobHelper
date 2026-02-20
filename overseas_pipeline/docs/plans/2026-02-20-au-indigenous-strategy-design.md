# 澳洲原住民文化胜任力策略系统设计文档

- **日期**: 2026-02-20
- **状态**: 设计完成，待实现
- **关联文件**:
  - 原始策略研究: `general/research_job_rules/澳洲教职原住民协议申请指南.md`
  - 参考范式: `overseas_pipeline/strategies/nz_te_tiriti_strategy.md`（NZ 实现）
  - NZ 设计文档: `overseas_pipeline/docs/plans/2026-02-20-nz-te-tiriti-strategy-design.md`
  - 现有地区卡: `region_knowledge/regions/australia.md`
  - Sophia 材料: `overseas_pipeline/materials/`
- **产出物**:
  - `overseas_pipeline/strategies/au_indigenous_strategy.md`（新增）
  - `overseas_pipeline/workflows/step1_research.md`（修改：增加 Step 10.6）
  - `overseas_pipeline/workflows/step2_analysis.md`（修改：增加 AU 分析段）
  - `overseas_pipeline/workflows/step3_materials.md`（修改：Humanizer 检查项）
  - `region_knowledge/regions/australia.md`（修改：§3.7 + §4）
  - 学校卡模板更新（增加 AU Indigenous 字段块）
  - **NZ 同步修改**（见 §十一）

---

## 一、目标与作用域

### 要解决的问题

澳洲教职申请中，原住民文化胜任力（Indigenous Cultural Competency）正从"加分项"演变为"实质性考核维度"。Universities Australia 的国家级最佳实践框架要求所有大学将文化胜任力纳入招聘评估，且越来越多的 JD 在 Essential Criteria 中明确要求 "Demonstrated understanding of Indigenous cultural competency"。当前 pipeline 在 `australia.md` 地区卡中仅有 KSC 格式指南，缺乏：

1. JD 中原住民/和解信号的系统化检测
2. 学校层面 RAP 执行深度的评估
3. 两维信号交叉产出的分级策略
4. 基于 Sophia 真实背景的修辞校准
5. 同校跨院系的学校信号复用机制
6. **AU 独有：** KSC 中原住民相关条目的 STAR/CAR 结构化应对

### 作用域

- **聚焦澳洲**：文件命名和内容专注 AU Indigenous
- **架构模式复用 NZ**：二维矩阵（JD signal × Institution signal → strategy label）的架构直接复用
- **内容完全独立**：关键词、修辞框架、学校种子表、Sophia 校准全部独立于 NZ

### 不做的事

- 不写 Python 自动化脚本（与 NZ 一致，学校战略文件结构差异大，agent 判断更可靠）
- 不修改 Step 3 workflow 基础结构

### 澳洲与新西兰的制度基础差异

| 维度 | NZ | AU |
|------|----|----|
| 制度基础 | 宪法级条约（Te Tiriti o Waitangi），法律硬约束 | 机构自愿政策（RAP）+ 联邦立法（Native Title Act 1993, Racial Discrimination Act 1975），无宪法条约。2023 年 Voice to Parliament 公投失败，原住民仍无宪法承认 |
| 原住民地位定性 | 条约缔约方，拥有独特宪法伙伴地位 | 世界上最古老持续文化（65,000+ 年）的第一民族，权利通过 UNDRIP 承诺、RAP 框架、Native Title 法案及机构性政策得到承认 |
| 核心支柱 | 条约三条款：Kāwanatanga / Tino Rangatiratanga / Ōritetanga | RAP 三支柱：Relationships / Respect / Opportunities |
| 申请材料话语锚点 | "条约义务"、"条约合规"、"双文化承诺" | "推进和解"、"文化胜任力"、"Closing the Gap" |
| 遴选委员会期望 | 证明理解条约三条款的法律含义 | 证明理解和解进程的历史与机构承诺 |
| 独有文档类型 | Bicultural Statement（部分学校） | KSC Response（几乎所有学校强制） |

---

## 二、架构总览

### 新增/修改文件

```
overseas_pipeline/strategies/
├── hci_density_strategy.md          # 已有，不变
├── nz_te_tiriti_strategy.md         # 已有，修改（增加升级门槛规则，见§十一）
└── au_indigenous_strategy.md        # 【新增】矩阵 + 策略标签 + 修辞指南 + KSC 应对

overseas_pipeline/workflows/
├── step1_research.md                # 【修改】增加 Step 10.6 (AU Indigenous 信号采集)
├── step2_analysis.md                # 【修改】增加 AU Indigenous 矩阵分析段
└── step3_materials.md               # 【修改】Humanizer 检查项增加 AU 版

region_knowledge/regions/
└── australia.md                     # 【修改】§3.7 原住民策略指向 + §4 评审重点更新

overseas_pipeline/templates/knowledge/
└── department_rule_card_template.md  # 【修改】增加 AU Indigenous 学校信号字段块
```

### 数据流（与 NZ 完全对称）

```
Step 1 (Step 10.6, AU only):
  JD 原文 ──关键词扫描──→ jd_signal: no_mention | boilerplate | explicit
                          （附：原文摘录 + 所在板块位置）

  学校 RAP/战略页 ──agent 评估──→ school_signal: light | moderate | strong
                                   （附：原文摘录 + 来源 URL + RAP tier）
  ↓
  写入 faculty_data.json → au_indigenous 块
  写入学校卡 → AU Indigenous 学校信号（跨院系复用）

  如矩阵初判 ≥ strong → step1_summary 标注中断警告
  全量模式下 pipeline 中断，等待用户审查

Step 2:
  读取 au_indigenous 块 + au_indigenous_strategy.md + Sophia materials
  → 矩阵查表 → strategy_label (skip → full_rap)
  → 写入 fit_report → per-document 修辞建议（含 KSC，标注 Claim vs Aspire）

Step 3:
  读取 fit_report 中的 AU Indigenous 修辞建议
  → 按策略指南生成各文档中的相应段落
  → Humanizer pass 增加 AU 特定校验项
```

### 与 NZ 的关键区别点

- `faculty_data.json` 中的 key 是 `au_indigenous`（非 `te_tiriti`）
- Step 10.6 而非 10.5（并行存在，region=australia 触发 10.6，region=new_zealand 触发 10.5）
- fit_report 专节标题为 `### AU Indigenous 评估`
- Per-document 建议多一列：KSC Response

---

## 三、二维矩阵与策略标签

### 3.1 JD 信号等级定义

| level | 判定条件 | 典型表现 |
|-------|---------|---------|
| `no_mention` | JD 实质性评估板块无原住民相关词汇，仅有 EEO 样板 | "We are an equal opportunity employer" |
| `boilerplate` | 出现关键词但位于 Desirable / About the University 区域 | "An understanding of Aboriginal and Torres Strait Islander cultures" 在 Desirable Criteria 末尾 |
| `explicit` | 关键词出现在 Essential Criteria / Key Responsibilities / Selection Criteria | "Demonstrated understanding of Indigenous cultural competency" 在 Essential Criteria |

#### 扫描关键词清单

**核心词（高权重）：**
Reconciliation Action Plan, RAP, Aboriginal and Torres Strait Islander, Indigenous Cultural Competency, First Nations, Cultural Safety, Closing the Gap, Traditional Custodians, Welcome to Country, Acknowledgement of Country

**辅助词（低权重，结合位置判断）：**
reconciliation, indigenous, cultural competency, First Peoples, CARE principles, Indigenous data sovereignty, decolonising, Country (大写), Elders, community engagement

#### 位置权重规则

- Essential Criteria / Key Responsibilities / Selection Criteria 中出现 → **`explicit`**
- Desirable / Nice-to-have / About the University 中出现 → **`boilerplate`**
- 仅在 EEO 声明 / 页脚 / 学校简介样板中出现 → **`no_mention`**

### 3.2 学校信号等级定义

| level | 判定条件 | 典型表现 |
|-------|---------|---------|
| `light` | 仅有标准 Acknowledgement of Country，无专门战略文件；RAP 为 Reflect 或无 RAP | 页脚 "We acknowledge the Traditional Custodians..." |
| `moderate` | 有正式 RAP（Innovate 或以上）但未深入到学院级行动计划，无专设原住民研究中心参与招聘 | ANU 的 Innovate RAP 2024-2026 |
| `strong` | 有高级 RAP（Stretch/Elevate）+ 学院级原住民战略 + 原住民学术支持中心（如 Murrup Barak / Nura Gili）+ 明确的原住民就业 KPI | Melbourne 的 Murmuk Djerring + Indigenous Employment Plan |

**RAP tier 与 school_signal 的参考映射（非硬性绑定）：**
- Reflect / 无 RAP → 通常 `light`
- Innovate → 通常 `moderate`
- Stretch / Elevate → 通常 `strong`
- 但 Agent 应根据实际执行深度而非仅凭 tier 标签判断（有些 Innovate RAP 执行力比 Stretch 还强）

**评估信号来源（优先级从高到低）：**
1. 学校 RAP 文件（含 tier 级别）
2. Indigenous Employment Plan / Strategy
3. 学院级 Indigenous Engagement Strategy
4. 原住民学术支持中心的存在与职权
5. DVC(Indigenous) / PVC(Indigenous) 的存在

### 3.3 策略矩阵

| JD signal \ School signal | `light` | `moderate` | `strong` |
|---------------------------|---------|-----------|----------|
| `no_mention` | **`skip`** | **`subtle`** | **`moderate`** |
| `boilerplate` | **`subtle`** | **`moderate`** | **`strong`** |
| `explicit` | **`moderate`** | **`strong`** | **`full_rap`** |

---

## 四、升级门槛规则（AU + NZ 通用）

**核心原则：** `moderate` 是默认天花板。升级到 `strong` 或 `full_rap`/`full_treaty` 必须满足明确的证据门槛，且系统必须向用户显式说明升级理由。

### `strong` 触发条件（必须同时满足）

1. JD 或 School signal 中至少有一个 ≥ `explicit` 或 `strong`（矩阵硬性要求）
2. fit_report 中必须列出触发升级的**具体原文证据**（不能是 agent 的推测）
3. Step 2 在 fit_report 中用醒目标记提示用户：

```
⚠ 策略升级: moderate → strong
触发证据:
  - JD Essential Criteria: "Demonstrated understanding of Indigenous
    cultural competency" (jd_main.md, bullet 5)
  - 学校 RAP: Stretch RAP 2024-2027, Indigenous Employment Plan 目标
    原住民教职占比 3.5%
建议: 材料中需要 RAP 三支柱结构化段落。请确认是否采纳。
```

### `full_rap` / `full_treaty` 触发条件（最严格）

1. JD signal = `explicit` **且** School signal = `strong`（矩阵唯一入口，不接受 agent 上调）
2. JD 中必须有**至少 2 条**独立的原住民相关要求出现在 Essential Criteria
3. fit_report 中必须**暂停并询问用户确认**后才写入最终策略标签：

```
⚠ 最高级策略触发: full_rap
触发证据:
  - JD Essential Criteria #3: "Demonstrated cultural competency..."
  - JD Essential Criteria #7: "Commitment to reconciliation..."
  - 学校: Stretch RAP + Murrup Barak 中心 + Indigenous Employment Plan
此级别将在 Cover Letter 中加入 200-250 词专门段落、Research Statement
中加入 300-400 词独立小节。
请确认: 采纳 full_rap / 降级为 strong / 用户自定
```

### Agent 上调限制

- Agent 可将矩阵结果上调**至多一级**，且仅限 skip→subtle 或 subtle→moderate
- **禁止** agent 自行上调到 strong 或 full_rap/full_treaty
- 所有上调必须在 `strategy_rationale` 中注明理由

### 全量模式中断规则

当 Step 10.5（NZ）或 Step 10.6（AU）的矩阵初判结果为 `strong` 或 `full_rap`/`full_treaty` 时：

1. Step 1 正常完成所有其他子步骤
2. 在 `step1_summary.md` 顶部醒目标注中断警告
3. **全量模式（一键/全流程）下**：pipeline 在 Step 1 完成后**自动中断**，不进入 Step 2，等待用户审查 step1_summary 后手动触发继续
4. **单步模式下**：Step 1 正常结束，用户自然会在触发 Step 2 前看到 summary 中的警告

---

## 五、通用禁忌（所有级别）

以下错误在任何级别都负面，级别越高后果越严重：

1. **把它写成美式 DEI Statement**：只谈 "underrepresented minorities"、"intersectionality" → 暴露不了解澳洲第一民族作为世界上最古老持续文化（65,000+ 年）的独特历史地位与先住民族固有权利。澳洲原住民不具有 NZ 毛利人那样的宪法条约地位，但其权利通过 UNDRIP 承诺、RAP 框架、Native Title 法案（1993）及各大学的机构性政策得到承认
2. **把原住民归为"少数族裔"之一**：Aboriginal and Torres Strait Islander peoples 是 First Nations，拥有 65,000+ 年的持续文化传承，不是 minority
3. **混淆 Welcome to Country 与 Acknowledgement of Country**：前者**只能**由 Traditional Custodians/Elders 主持，后者任何人可做。在材料中声称要做 Welcome to Country = 严重文化失仪
4. **使用缺陷视角（Deficit-based language）**：把原住民描绘为需要"拯救"或"帮助"的对象 → 必须用优势视角（Strengths-based），强调原住民是"澳洲的第一代科学家"（First Scientists），强调社区韧性与知识体系的复杂性
5. **不懂装懂**：伪装已有原住民社区合作经验 → 面试时被识破
6. **套用 NZ 条约框架**：澳洲无宪法条约，RAP 与 Te Tiriti 是完全不同的制度基础，不可混用术语（如不可说"treaty obligations"）
7. **大写规则违规**：Country（指传统土地时）、Elders、Traditional Custodians、First Nations、Dreaming 在原住民语境下必须首字母大写

来源: 原指南文档 §话语体系与遴选标准

---

## 六、Sophia 背景校准：Claim vs Aspire

基于 Sophia 的真实研究经历（`materials/Research_Statement.md`, `materials/Teaching_Statement.md`），按 RAP 三支柱重新映射。

| RAP 支柱 | **Claim**（有真实经历支撑） | **Aspire**（无经历，只能表达意愿+计划） |
|---------|--------------------------|----------------------------------------|
| **Relationships** (关系) | 参与式设计中与 domain experts 建立长期合作关系（JHU 医疗、SMART/NUS 教育）；跨文化环境协作经历（新加坡、美国、香港）；开源平台（MindCoder.ai, CollabCoder）建立的研究者社区 | 与 Aboriginal and Torres Strait Islander 社区建立研究伙伴关系；参与学校 RAP 的 Relationships 行动项 |
| **Respect** (尊重) | 对 trustworthy AI 的核心研究关注体现对人类 agency 的尊重；人类中心设计保障用户对数据分析过程的掌控；批判性审视 AI 自动化对人类判断的替代风险 | 原住民知识体系（Indigenous Knowledge Systems）的学术尊重；CARE 原则实施；文化安全（Cultural Safety）培训参与 |
| **Opportunities** (机会) | 指导多元背景学生的经验；课程设计中融入伦理与公平议题；算法偏见批判性研究为消除技术不平等奠定基础 | 参与 STEM 原住民学生管道建设（Pipeline Development）；在 CS 课程中融入原住民技术发展史与数据伦理 |

### 修辞天花板规则（Step 3 Humanizer 强制检查项）

1. **Claim 用具体经历，Aspire 用"学习意愿 + 具体计划"**
   - ✅ "My participatory design methodology provides a foundation I am eager to adapt for respectful community-engaged research with Aboriginal and Torres Strait Islander communities."
   - ❌ "I have experience working with Indigenous communities on data governance."

2. **引用 AU 本土概念时，用"已了解 + 希望深入"框架**
   - ✅ "I am familiar with the CARE Principles and their role in complementing FAIR data practices. I look forward to engaging with [University]'s RAP commitments to deepen this understanding."
   - ❌ "My work directly implements Indigenous Data Sovereignty."

3. **可以画平行线但必须声明不可简单类比**：新加坡跨文化经验可作适应力证据，但必须强调澳洲第一民族 65,000 年持续文化传承的独特性不可类比。

4. **技术落地点要诚实**：MindCoder.ai/CollabCoder 的人类控制权设计与 CARE 原则中的 "Authority to Control" 有概念共鸣，但不要夸大成"这就是 Indigenous Data Sovereignty 实践"。

来源: 原指南文档 §优先级判断规则, §CS/HCI 领域具象化表达

---

## 七、各策略标签修辞指南

### `skip`（JD=no_mention, School=light）

**场景：** JD 不提原住民议题，学校 RAP 层级也浅。强行插入挤占展示科研教学实力的空间。

| 文档 | 策略 |
|------|------|
| Cover Letter | 不加任何原住民内容 |
| Research Statement | 无特殊调整 |
| Teaching Statement | 无特殊调整 |
| KSC Response | 无相关 criteria 则不涉及 |

**fit_report 仍需展示：** JD 证据 + 学校证据 + "建议 skip" 的判断依据，让用户知情并可自行覆盖。

---

### `subtle`（JD=no_mention+School=moderate, 或 JD=boilerplate+School=light）

**场景：** 信号微弱但不为零。展示"做过功课 + 有文化敏感度"即可。

| 文档 | 策略 |
|------|------|
| Cover Letter | 末尾或学术价值观段落嵌入 1-2 句 |
| Research Statement | 不做专门调整 |
| Teaching Statement | 如篇幅允许，末尾加半句对 First Nations 学生的关注 |
| KSC Response | 如有 "demonstrated commitment to diversity" 类 criteria，嵌入一句文化敏感度表态 |

**Cover Letter 范式（Sophia 适用）：**

> "As an international scholar committed to inclusive and ethical research practice, I am strongly motivated to engage with Australia's reconciliation journey. I look forward to participating in cultural competency training to ensure my teaching and research respectfully support the success and wellbeing of Aboriginal and Torres Strait Islander students."

来源: 原指南文档 §中/低优先级应对策略

---

### `moderate`（矩阵中间三格）

**场景：** 有一定信号但不构成核心考核项。需展示理解，不必逐支柱展开。

| 文档 | 策略 |
|------|------|
| Cover Letter | 一段（100-150 词），概括性提及和解进程与自身研究/教学的关联 |
| Research Statement | 嵌入一句 CARE 原则 / Indigenous Data Sovereignty 意识，不单独成节 |
| Teaching Statement | 一句对 First Nations 学生学业成功的承诺，可提 culturally responsive pedagogy |
| KSC Response | 如有相关 criteria，用 CAR 法则写 150-200 词回应，引用跨文化协作经历作为可迁移能力 |

**Cover Letter 范式（Sophia 适用）：**

> "My research on human–AI collaboration is grounded in participatory methods that prioritise human agency and informed consent — values that resonate with the principles underpinning Australia's reconciliation commitments. I am committed to ensuring that the AI systems I develop contribute to equitable outcomes for all communities, and I look forward to deepening my understanding of how these principles apply within the Australian context, particularly through engagement with [University]'s Reconciliation Action Plan."

**Research Statement 嵌入句范式：**

> "In pursuing open and trustworthy AI research, I am mindful of frameworks such as the CARE Principles for Indigenous Data Governance, which complement FAIR principles by centring collective benefit, authority to control, responsibility, and ethics."

**Teaching Statement 嵌入句范式：**

> "I am committed to culturally responsive pedagogy that supports the academic success of all students, including Aboriginal and Torres Strait Islander learners whose success is a priority for Australia's higher education sector."

**KSC 回应范式（如 criteria 要求 "understanding of cultural competency"）：**

> "**Context:** At Johns Hopkins University and SMART Centre Singapore, I conducted participatory design research across culturally diverse teams, navigating different epistemological traditions and communication norms. **Action:** I developed co-design protocols that ensured all stakeholders retained meaningful control over how their domain knowledge was represented in AI systems, prioritising transparency and informed consent at every stage. **Result:** This approach produced research tools (MindCoder.ai, CollabCoder) adopted across multiple cultural contexts. I am committed to adapting this culturally responsive methodology to the Australian context, engaging with [University]'s RAP commitments and cultural competency training to build respectful relationships with Aboriginal and Torres Strait Islander communities."

**如果 school_signal=strong：** 引用该校 RAP 具体支柱或原住民战略名称。

来源: 原指南文档 §中/低优先级应对策略, §CS/HCI 领域具象化表达

---

### `strong`（JD=boilerplate+School=strong, 或 JD=explicit+School=moderate）

**场景：** 原住民文化胜任力是实质考核维度。需要结构化回应。**触发须满足§四升级门槛。**

| 文档 | 策略 |
|------|------|
| Cover Letter | 专门段落（200-250 词），RAP 三支柱结构化回应（Claim+Aspire 混合） |
| Research Statement | 单独小节 "Responsible AI & Indigenous Data Governance"（150-200 词） |
| Teaching Statement | First Nations 学生支持段（100-150 词） |
| KSC Response | 如有相关 criteria，用 STAR 法则写 300-400 词深度回应，三支柱分点论述 |

**Cover Letter 三支柱回应框架（Sophia 适用）：**

> **Relationships:** "My research methodology centres on participatory design, where domain experts are active collaborators rather than passive subjects. At JHU and SMART, I co-designed AI systems with healthcare professionals and educators, building sustained partnerships grounded in mutual trust and shared ownership. I see this collaborative ethos as a foundation I am eager to bring to respectful, reciprocal engagement with Aboriginal and Torres Strait Islander communities, guided by [University]'s RAP commitments." [Claim: 参与式设计长期合作; Aspire: 原住民社区合作]
>
> **Respect:** "A core conviction of my work is that humans must retain meaningful control over AI-driven analysis — reflected in platforms like MindCoder.ai and CollabCoder, which keep users in command of every analytical decision. This commitment to human agency resonates with the CARE Principles for Indigenous Data Governance, which centre collective benefit and community authority over data. I look forward to deepening my understanding of Indigenous Knowledge Systems and Cultural Safety through [University]'s professional development programs." [Claim: 人类控制权研究; Aspire: 原住民知识体系与文化安全]
>
> **Opportunities:** "My research critically examines the risks of unchecked AI automation, demonstrating that purely automated analysis can perpetuate existing biases. As a faculty member, I am committed to extending this critical lens to ensure AI tools serve equitable outcomes for all communities, and to contributing to STEM pipeline development for Aboriginal and Torres Strait Islander students through mentoring and inclusive curriculum design." [Claim: AI 偏见批判研究; Aspire: STEM 管道建设]

**Research Statement 小节范式：**

> "**Responsible AI & Indigenous Data Governance.** As AI systems increasingly process sensitive human data, questions of who controls data collection, analysis, and application become paramount. My human-centred approach — ensuring transparency, user control, and rigorous validation — provides a natural foundation for engaging with Indigenous data governance frameworks. I am particularly drawn to the CARE Principles, which complement FAIR data practices by centring collective benefit, authority to control, responsibility, and ethics. I look forward to exploring how my human–AI collaboration architectures can be designed to honour these principles, contributing to culturally safe and equitable AI research in Australia."

**Teaching Statement First Nations 段范式：**

> "I am committed to fostering an inclusive learning environment that supports the academic success of Aboriginal and Torres Strait Islander students. Drawing on my experience mentoring students from diverse cultural backgrounds across Singapore, the US, and Hong Kong, I recognise that effective teaching requires culturally responsive pedagogy. I look forward to engaging with [University]'s Indigenous student support services and to embedding ethical AI discussions — including Indigenous data sovereignty and algorithmic fairness — into my curriculum."

**如果 school_signal=strong：** 必须引用该校 RAP 具体支柱、原住民战略名称或学术支持中心名称。

来源: 原指南文档 §高优先级应对策略, §双层架构分析, §CS/HCI 领域具象化表达

---

### `full_rap`（JD=explicit, School=strong）

**场景：** 最高规格。文化胜任力是硬性 Essential Criteria，学校有深度 RAP 和原住民战略。**触发须满足§四最严格门槛。**

| 文档 | 策略 |
|------|------|
| Cover Letter | 三支柱深度回应 + 引用该校 RAP/Indigenous Strategy + 考虑 DVC(Indigenous) 受众 |
| Research Statement | 专门一节 "Responsible AI in the Australian Context"（300-400 词） |
| Teaching Statement | First Nations 学生支持段 + 课程去殖民化构想 |
| KSC Response | 原住民相关 criteria 用 STAR 法则 400-500 词，引用目标学校 RAP 具体行动项和 KPI |

**在 `strong` 基础上的升级点：**

**Cover Letter 升级：**
- 三支柱回应中加深技术细节（"具体如何做"而非"我会做"）
- 引用该校 RAP 具体行动项 + Indigenous Employment Plan 的 KPI
- 如该校有 DVC/PVC(Indigenous) 参与审查，措辞需额外审慎
- 自然融入 Acknowledgement of Country 意识（如："I am mindful that [University]'s main campus stands on the unceded lands of the [Nation] people..."）

**Research Statement 完整小节升级（在 `strong` 基础上增加）：**
- 引用 AU 本土 CS/HCI 研究案例作为未来合作方向（Aspire 框架）：
  - Melbourne CIS 的 Indigenous HCI 项目（#thismymob 数字土地权）
  - Aboriginal English ASR 系统设计中的 IDSov 实践
- 经费叙事指向 ARC 资助中的 Indigenous Research 优先领域
- FAIR vs CARE 平衡的具体技术设想（中介访问机制、训练语料审计、社区数据控制面板）

**Teaching Statement 升级（课程去殖民化构想，用 Aspire 框架）：**
- 在 CS 导论/软件工程课程中嵌入原住民技术发展史（"First Scientists" 叙事）
- 数据伦理课程中融入 IDSov 和 CARE 原则讨论
- 参与学校 STEM 原住民预科项目（如 UNSW Winter School Program）的指导工作

**KSC Response 升级范式：**

> "**Situation:** The increasing deployment of AI systems in healthcare and education raises critical questions about algorithmic fairness for historically marginalised communities. In Australia, Aboriginal and Torres Strait Islander peoples face documented disparities in health outcomes partly attributable to Western-centric diagnostic algorithms. **Task:** As a researcher in human–AI collaboration, I recognised the need to ensure AI tools preserve human agency and do not perpetuate systemic biases. **Action:** I developed MindCoder.ai and CollabCoder — platforms that embed human control at every analytical step, ensuring domain experts retain authority over how data is interpreted. I also conducted systematic studies demonstrating that fully automated AI analysis risks missing cultural and contextual nuance. I have since familiarised myself with the CARE Principles for Indigenous Data Governance and [University]'s [RAP名称], and I am committed to adapting my participatory methodology for respectful engagement with Aboriginal and Torres Strait Islander communities. **Result:** My platforms have been adopted across diverse research contexts, demonstrating the scalability of human-centred AI design. Upon joining [University], I plan to pursue ARC funding for research on culturally safe AI in collaboration with [University]'s [原住民学术中心], and to participate in cultural competency training as part of [University]'s RAP commitments."

**Sophia 诚实度校准（full_rap 特别重要）：**
1. **方法论桥接**：用参与式设计方法论作为"可迁移基础"
2. **学习路径具体化**：不只说"我愿意学习"，而是"入职后参加 [University] 的 [具体培训项目]，第一年寻求与 [学校原住民研究中心] 的合作"
3. **平行经验谨慎使用**：简短提及跨文化适应力后，立刻声明"我深刻理解澳洲第一民族 65,000 年持续文化传承的独特性，不可与其他多文化经验简单类比"

来源: 原指南文档 §高优先级应对策略, §CS/HCI 领域具象化表达, §综合应用蓝图

---

## 八、数据结构

### 8.1 faculty_data.json 中的 `au_indigenous` 块

```json
{
  "au_indigenous": {
    "jd_signal": {
      "level": "explicit | boilerplate | no_mention",
      "evidence": [
        {
          "text": "原文摘录（英文原文）",
          "location": "所在板块/bullet 编号，如 'Essential Criteria, bullet 5'",
          "source": "raw/jd_main.md"
        }
      ]
    },
    "school_signal": {
      "level": "strong | moderate | light",
      "evidence": [
        {
          "text": "原文摘录（英文原文）",
          "url": "来源 URL",
          "document_name": "文档名称，如 'Stretch RAP 2024-2027'"
        }
      ],
      "rap_tier": "Reflect | Innovate | Stretch | Elevate | none",
      "indigenous_strategy_name": "该校原住民战略名称（如有）",
      "indigenous_centre_name": "原住民学术支持中心名称（如有）"
    },
    "strategy": "skip | subtle | moderate | strong | full_rap",
    "strategy_rationale": "Step 2 填充：矩阵结果 + 升级门槛验证 + agent 补充判断"
  }
}
```

**与 NZ `te_tiriti` 块的区别：**
- 多了 `rap_tier` 字段（记录 RAP 官方层级，作为参考但不直接决定 signal level）
- 多了 `indigenous_centre_name`（AU 大学普遍设有独立的原住民学术中心）
- 无 `key_framework_name` / `key_values`（NZ 学校有专有毛利术语体系，AU 学校更多用通用 RAP 术语）

**证据要求：**
- `jd_signal.evidence`：至少 1 条（`no_mention` 时记录"未发现相关关键词"）
- `school_signal.evidence`：至少 2 条（`light` 时可为"仅发现页脚 Acknowledgement of Country"）
- 所有 evidence 保留英文原文，不翻译

### 8.2 学校卡中的 AU Indigenous 字段块

```markdown
## AU Indigenous 学校信号（仅 region=australia）

- **signal_level**: strong | moderate | light
- **assessed_date**: YYYY-MM-DD
- **rap_tier**: Stretch | Innovate | Reflect | Elevate | none
- **rap_document**: RAP 文档名称（如 "Innovate RAP 2024-2026"）
- **indigenous_strategy**: 原住民战略名称（如 "Murmuk Djerring"，无则填 N/A）
- **indigenous_centre**: 原住民学术支持中心（如 "Murrup Barak"，无则填 N/A）
- **evidence**:
  1. "原文摘录（英文原文）"
     - source: [文档名](URL)
  2. "原文摘录（英文原文）"
     - source: [文档名](URL)
- **notes**: 其他备注（如 DVC(Indigenous) 审查权限、特定 KPI 等）
```

**跨院系复用规则（与 NZ 一致）：**
- 同校新院系 Step 1 时，检测到学校卡已有此字段且 `assessed_date` 在 6 个月内 → 直接复用，跳过学校 RAP 页爬取
- 仅需对新院系做 JD 信号检测

### 8.3 fit_report 中的 AU Indigenous 专节

```markdown
### AU Indigenous 评估（仅 region=australia）

**JD 信号: [level]**
> "[原文摘录]" ([位置])
> "[原文摘录]" ([位置])

**学校信号: [level]** (来源: 学校卡, assessed [date])
> "[原文摘录]" ([文档名](URL))
> "[原文摘录]" ([文档名](URL))
> RAP tier: [tier] | 原住民战略: [名称] | 学术支持中心: [名称]

**矩阵结果: [strategy_label]**
⚠ [如为 strong/full_rap，显示升级门槛验证和用户确认提示]

**Sophia 经历锚点（Step 3 参考）：**
- Relationships 可 Claim: ...
- Respect 可 Claim: ...
- Opportunities 可 Claim: ...

**Per-document 建议:**
- **Cover Letter**: [具体建议，标注 Claim vs Aspire]
- **Research Statement**: [具体建议]
- **Teaching Statement**: [具体建议]
- **KSC Response**: [如有相关 criteria，具体建议 + 推荐 STAR/CAR 结构]
```

---

## 九、Pipeline Workflow 修改

### 9.1 Step 1 新增：Step 10.6 AU Indigenous Signal Assessment

在现有 Step 10（HCI density + course catalog）和 Step 10.5（NZ Te Tiriti，如有）之后，仅当 `region=australia` 时触发：

```
Step 10.6: AU Indigenous Signal Assessment (AU only)

A. JD 信号检测
   1. 读取已爬取的 raw/jd_*.md
   2. 扫描关键词清单（见策略文件 §3.1）
   3. 记录每个命中：原文文本 + 所在位置（哪个板块/bullet）
   4. 根据位置权重规则判定 jd_signal level
   5. 写入 faculty_data.json → au_indigenous.jd_signal（含 evidence 数组）

B. 学校信号检测
   1. 检查同校学校卡是否已有 AU Indigenous 学校信号
      - 如有且 assessed_date 在 6 个月内 → 直接读取复用，跳到 C
      - 如无或已过期 → 继续
   2. 查策略文件种子表（§十），获取该校已知 RAP/Indigenous Strategy URL
   3. 爬取种子 URL（五层 fallback）
   4. 如种子不足或种子全部失败，搜索补充：
      - "{school_name} Reconciliation Action Plan"
      - "{school_name} Indigenous strategy"
      - "{school_name} Aboriginal Torres Strait Islander employment"
   5. Agent 基于爬取内容评定 school_signal level
   6. 摘录原文证据（至少 2 条），记录来源 URL 和文档名
   7. 识别 RAP tier、原住民战略名称、学术支持中心名称
   8. 写入学校卡 → AU Indigenous 学校信号
      （双写：region_knowledge/schools/ + output/knowledge/）
   9. 写入 faculty_data.json → au_indigenous.school_signal

C. 预判策略标签
   1. 查矩阵表 → 初步 strategy label
   2. 如为 strong 或 full_rap → 在 step1_summary.md 顶部标注中断警告
   3. 写入 faculty_data.json → au_indigenous.strategy
   4. 留空 strategy_rationale（Step 2 填充）

D. Step 1 Summary 新增行
   - "AU Indigenous: JD=[level], School=[level] → [strategy_label]（初步）"
   - 如 strong/full_rap: "⚠ 高级别信号，需用户审查后继续 Step 2"

E. 全量模式中断判定
   - 如 strategy_label ∈ {strong, full_rap} → pipeline 中断，等待用户审查
```

### 9.2 Step 2 修改：AU Indigenous 矩阵分析

在 fit_report 生成流程中增加（AU only）：

```
AU Indigenous Analysis:

1. 读取 faculty_data.json → au_indigenous 块
2. 读取 strategies/au_indigenous_strategy.md
3. 读取 Sophia 的 materials/Research_Statement.md 和
   Teaching_Statement.md（识别可 Claim 的经历锚点）
4. 确认/调整策略标签
   - Agent 可上调至多一级，仅限 skip→subtle 或 subtle→moderate
   - 禁止 agent 上调到 strong 或 full_rap
   - 典型上调场景：JD 是 boilerplate 但该校已知面试考文化胜任力
5. 填充 strategy_rationale
6. 在 fit_report 中生成 AU Indigenous 专节（格式见 §8.3）
7. 标注 Sophia 可 Claim 的经历点 + 需要 Aspire 的部分
8. 如有原住民相关 KSC criteria，标注推荐的 STAR/CAR 结构和具体 Claim 锚点
```

### 9.3 Step 3 修改

无结构性修改。Humanizer 强制检查项新增 AU 版：

```
Humanizer Checklist 新增 (AU):
□ AU Indigenous 相关段落是否超出 Sophia 真实经历？
  - 检查是否有伪装已有原住民社区合作经验的表述
  - 检查是否混淆 Welcome to Country 与 Acknowledgement of Country
  - 检查是否使用了缺陷视角（deficit-based language）描述原住民
  - 检查 Aspire 部分是否有具体学习计划而非空洞承诺
  - 检查大写规则：Country, Elders, Traditional Custodians, First Nations
  - 检查是否把 NZ 条约术语错误套用到 AU 语境
```

---

## 十、学校种子表

从原始指南文档中提取的澳洲大学数据。Step 1 agent 先按 school_id 匹配种子表爬取，无种子或种子不足时搜索补充。

### 墨尔本大学 (University of Melbourne)

- **预判 school_signal**: strong
- **RAP tier**: 有 RAP（具体 tier 需验证）
- **原住民战略**: Murmuk Djerring
- **学术支持中心**: Murrup Barak
- **种子 URL**:
  - Indigenous Employment Plan 2023-2027: https://www.unimelb.edu.au/__data/assets/pdf_file/0006/4852221/UOM_IndigenousEmploymentPlan23-27_240423_online.pdf
  - Selection Criteria Guide: https://about.unimelb.edu.au/careers/selection-criteria
  - Indigenous HCI - CIS projects: https://cis.unimelb.edu.au/research/hci/projects/indigenous-knowledge
  - #thismymob 数字土地权: https://cis.unimelb.edu.au/research/hci/projects/thismymob-establishing-digital-land-rights
  - Indigenous Data Governance: https://pursuit.unimelb.edu.au/articles/indigenous-data-governance-for-the-21st-century
- **特殊备注**: CIS 学院有成熟的 Indigenous HCI 项目群，full_rap 级别可引用作为未来合作方向；Indigenous Employment Plan 设定 2025 年原住民教职 350 人目标
- **原指南位置**: §双层架构分析

### 蒙纳士大学 (Monash University)

- **预判 school_signal**: moderate
- **RAP tier**: Innovate (2023-2025)
- **原住民战略**: Indigenous Research Action Plan (William Cooper Institute)
- **学术支持中心**: William Cooper Institute
- **种子 URL**:
  - Innovate RAP 2023-2025: https://www.monash.edu/__data/assets/pdf_file/0004/3290665/Monash-University-Innovate-Reconciliation-Action-Plan-June-2023-to-June-2025-1.pdf
  - Indigenous Employment Procedure: https://www.monash.edu/__data/assets/pdf_file/0007/3247090/Indigenous-Employment-Procedure.pdf
  - Indigenous Research Action Plan: https://www.monash.edu/indigenous-students/research/indigenous-research-action-plan
  - Inclusive Teaching: https://www.monash.edu/learning-teaching/TeachHQ/Teaching-practices/inclusive-teaching-practices/how-to/embed-inclusive-teaching
- **特殊备注**: IT 学院要求定期文化能力培训；RAP 指导将原住民视角嵌入日常课程
- **原指南位置**: §双层架构分析, §学院微观架构

### 澳大利亚国立大学 (ANU)

- **预判 school_signal**: moderate
- **RAP tier**: Innovate (2024-2026)
- **学术支持中心**: Tjabal Aboriginal & Torres Strait Islander Higher Education Centre
- **种子 URL**:
  - RAP page: https://www.anu.edu.au/about/strategic-planning/reconciliation-action-plan
  - Innovate RAP PDF: https://d1zkbwgd2iyy9p.cloudfront.net/files/2024-07/2024%20Reconciliation%20Action%20Plan%202024-FINAL.pdf
  - Indigenous Education Statement: https://services.anu.edu.au/files/document-collection/2012%20Indigenous%20Education%20Statement.pdf
- **原指南位置**: §大学宏观架构

### 新南威尔士大学 (UNSW)

- **预判 school_signal**: strong
- **RAP tier**: 需验证
- **原住民战略**: Indigenous Strategy 2018-2025 ("Give Back")
- **学术支持中心**: Nura Gili
- **种子 URL**:
  - Indigenous Strategy PDF: https://www.indigenous.unsw.edu.au/sites/default/files/documents/UNSW%20Indigenous%20Strategy%202021_web.pdf
  - Acknowledgement of Country protocols: https://www.indigenous.unsw.edu.au/sites/default/files/documents/Protocols%20for%20Acknowledgement%20of%20Country%20and%20Welcome%20to%20Country_0.pdf
  - Engineering Indigenous Engagement: https://www.unsw.edu.au/engineering/student-life/indigenous-engagement
  - Business School Indigenous Engagement: https://www.unsw.edu.au/business/about-us/equity-diversity-inclusion/indigenous-engagement
- **特殊备注**: 工程学院有 "Grow Our Own" 计划和 Indigenous STEM Winter School；full_rap 级别可引用
- **原指南位置**: §大学宏观架构, §学院微观架构

### 昆士兰大学 (University of Queensland)

- **预判 school_signal**: strong
- **RAP tier**: Stretch
- **种子 URL**:
  - Stretch RAP: https://about.uq.edu.au/sites/default/files/2024-11/stretch-reconciliation-action-plan.pdf
  - Indigenous Data Sovereignty guide: https://research-support.uq.edu.au/indigenous-knowledge-and-indigenous-data-sovereignty
- **特殊备注**: Stretch RAP 意味着和解目标已嵌入运营 KPI
- **原指南位置**: §RAP 四级体系

### 西悉尼大学 (Western Sydney University)

- **预判 school_signal**: moderate
- **种子 URL**:
  - Engineering Indigenous Strategy: https://www.westernsydney.edu.au/schools/engineering/indigenous-strategy-for-school-of-engineering
  - EDBE Indigenous Strategy PDF: https://www.westernsydney.edu.au/schools/soedbe/.indigenous-strategy-for-school-of-engineering-design-and-built-environment/edbe0375-strategy-plan-2021.pdf
- **特殊备注**: 工程学院有七大原住民目标，特别关注原住民女性群体代表性
- **原指南位置**: §学院微观架构

### 悉尼大学 (University of Sydney)

- **预判 school_signal**: moderate（待验证）
- **种子 URL**: 无直接种子
- **备注**: 原指南未单独论述，Step 1 需搜索补充

### CSIRO（联邦科学与工业研究组织）

- **预判 school_signal**: strong（非大学但可能出现在合作研究职位中）
- **RAP tier**: Stretch
- **种子 URL**:
  - RAP page: https://www.csiro.au/en/research/indigenous-science/reconciliation-action-plan
- **备注**: 非标准学校，仅在合作职位或博后职位中可能涉及
- **原指南位置**: §RAP 四级体系

---

## 十一、NZ 同步修改

本次 AU 设计过程中发现 NZ 策略系统需要同步改进的三个方面：

### 11.1 增加升级门槛规则

**修改文件：** `strategies/nz_te_tiriti_strategy.md`

在 §二（策略矩阵）后增加升级门槛规则，内容与 §四 完全对称：

- `strong` 触发需明确原文证据 + fit_report 醒目提示用户
- `full_treaty` 触发需 JD signal=explicit 且 School signal=strong（矩阵唯一入口，不接受 agent 上调）+ JD 中至少 2 条独立条约相关要求在 Essential Criteria + fit_report 暂停询问用户确认
- Agent 上调限制：至多一级，仅限 skip→subtle 或 subtle→moderate，禁止上调到 strong/full_treaty

### 11.2 全量模式中断规则

**修改文件：** `workflows/step1_research.md` Step 10.5

在 Step 10.5 的 C（预判策略标签）步骤中增加：

```
如为 strong 或 full_treaty:
  → 在 step1_summary.md 顶部标注中断警告
  → 全量模式下 pipeline 在 Step 1 完成后自动中断
  → 等待用户审查 step1_summary 后手动触发继续
```

### 11.3 多文档修辞落地执行力度

**问题：** NZ 策略文件的设计已覆盖多文档（Cover Letter + Research Statement + Teaching Statement），但实际执行中可能只落在了 Cover Letter 上。

**修改文件：** `workflows/step2_analysis.md`, `workflows/step3_materials.md`

- Step 2 的 fit_report Te Tiriti 专节中，per-document 建议必须为**每个文档**提供具体的修辞指令（不能只写 Cover Letter 的建议而留空 Research Statement / Teaching Statement）
- Step 3 在生成每个文档时，必须**显式检查** fit_report 中对应文档的 Te Tiriti 建议是否已执行
- Humanizer checklist 增加验证项："所有被 fit_report 标记需要 Te Tiriti 调整的文档是否都已执行？"

---

## 十二、地区卡修改

### australia.md 修改方案

**在 §3.5（KSC 回应文档）之后新增 §3.7：**

```markdown
### 3.7 原住民文化胜任力策略
- **状态**: 取决于 JD 信号强度和学校信号强度的矩阵交叉结果
- **详细策略**: 见 `overseas_pipeline/strategies/au_indigenous_strategy.md`
- **核心原则**:
  - 不能写成美式 DEI Statement；必须基于 RAP 和解框架而非多元文化框架
  - 澳洲原住民不具有 NZ 毛利人的宪法条约地位，话语锚点是"推进和解"而非"条约合规"
  - Country / Elders / Traditional Custodians / First Nations 必须首字母大写
  - 区分 Acknowledgement of Country（任何人可做）与 Welcome to Country（仅 Traditional Custodians）
- **Pipeline 行为**: Step 1 自动检测 JD/学校信号，Step 2 产出策略标签和 per-document 建议
- **影响文档**: Cover Letter, Research Statement, Teaching Statement, KSC Response（按策略级别递进）
```

**在 §4（评审重点）的"最看重"列表后新增：**

```markdown
4. **文化胜任力**（越来越多职位将其列为 Essential Criteria）
   — 详见 `overseas_pipeline/strategies/au_indigenous_strategy.md`
```

---

## 十三、实现计划

### Phase 1: 策略文件（优先）
1. 创建 `strategies/au_indigenous_strategy.md`
   - 矩阵定义 + 关键词清单 + 各标签修辞指南（含 KSC）
   - Sophia 背景校准 + 升级门槛规则 + 学校种子表
   - 从原始指南文档蒸馏，保留所有引用链接

### Phase 2: Workflow 修改
2. 修改 `workflows/step1_research.md` — 增加 Step 10.6
3. 修改 `workflows/step2_analysis.md` — 增加 AU Indigenous 分析段
4. 修改 `workflows/step3_materials.md` — Humanizer 检查项

### Phase 3: 地区卡/模板更新
5. 修改 `region_knowledge/regions/australia.md` §3.7 + §4
6. 更新学校卡模板 — 增加 AU Indigenous 字段块

### Phase 4: NZ 同步修改
7. 回写 `strategies/nz_te_tiriti_strategy.md` — 增加升级门槛规则
8. 修改 `workflows/step1_research.md` Step 10.5 — 增加 strong/full_treaty 中断规则
9. 修改 `workflows/step2_analysis.md` + `step3_materials.md` — 增强多文档修辞落地

### 验证
10. 如有已完成的澳洲学校产出（如 Monash），进行回测：用新矩阵评估，对比原 fit_report 中的策略是否一致

---

## 十四、引用索引

本设计文档的引用来源于原始指南文档 `general/research_job_rules/澳洲教职原住民协议申请指南.md`。以下为关键来源：

| 来源简称 | URL | 用途 |
|---------|-----|------|
| Reconciliation Australia RAP | https://www.reconciliation.org.au/reconciliation-action-plans/ | RAP 四级体系定义 |
| ANU Innovate RAP | https://d1zkbwgd2iyy9p.cloudfront.net/files/2024-07/2024%20Reconciliation%20Action%20Plan%202024-FINAL.pdf | 学校信号评估 |
| Universities Australia Indigenous Strategy | https://universitiesaustralia.edu.au/wp-content/uploads/2022/03/UA-Indigenous-Strategy-2022-25.pdf | 国家级框架 |
| UQ Stretch RAP | https://about.uq.edu.au/sites/default/files/2024-11/stretch-reconciliation-action-plan.pdf | 学校信号评估 |
| UA Cultural Competency Guiding Principles | https://universitiesaustralia.edu.au/wp-content/uploads/2019/06/Guiding-Principles-for-Developing-Indigenous-Cultural-Competency-in-Australian-Universities.pdf | JD 信号解读 |
| UA Cultural Competency Best Practice Framework | https://universitiesaustralia.edu.au/wp-content/uploads/2019/06/National-Best-Practice-Framework-for-Indigenous-Cultural-Competency-in-Australian-Universities.pdf | 文化胜任力框架 |
| Melbourne Indigenous Employment Plan | https://www.unimelb.edu.au/__data/assets/pdf_file/0006/4852221/UOM_IndigenousEmploymentPlan23-27_240423_online.pdf | 学校信号+种子 |
| Monash Innovate RAP | https://www.monash.edu/__data/assets/pdf_file/0004/3290665/Monash-University-Innovate-Reconciliation-Action-Plan-June-2023-to-June-2025-1.pdf | 学校信号+种子 |
| Monash Indigenous Research Action Plan | https://www.monash.edu/indigenous-students/research/indigenous-research-action-plan | 学校信号+种子 |
| UNSW Indigenous Strategy | https://www.indigenous.unsw.edu.au/sites/default/files/documents/UNSW%20Indigenous%20Strategy%202021_web.pdf | 学校信号+种子 |
| UNSW Acknowledgement Protocols | https://www.indigenous.unsw.edu.au/sites/default/files/documents/Protocols%20for%20Acknowledgement%20of%20Country%20and%20Welcome%20to%20Country_0.pdf | 文化协议 |
| Melbourne CIS Indigenous HCI | https://cis.unimelb.edu.au/research/hci/projects/indigenous-knowledge | RS 引用案例 |
| Melbourne #thismymob | https://cis.unimelb.edu.au/research/hci/projects/thismymob-establishing-digital-land-rights | RS 引用案例 |
| GIDA CARE Principles | https://www.gida-global.org/care | 核心概念 |
| ARDC CARE Principles | https://ardc.edu.au/resource/the-care-principles/ | 核心概念 |
| UQ Indigenous Data Sovereignty | https://research-support.uq.edu.au/indigenous-knowledge-and-indigenous-data-sovereignty | IDSov 参考 |
| Aboriginal English ASR | https://arxiv.org/html/2503.03186v1 | RS 引用案例 |
| Melbourne Selection Criteria Guide | https://about.unimelb.edu.au/careers/selection-criteria | KSC 格式 |
| CSIRO RAP | https://www.csiro.au/en/research/indigenous-science/reconciliation-action-plan | 学校信号+种子 |
| WSU Engineering Indigenous Strategy | https://www.westernsydney.edu.au/schools/engineering/indigenous-strategy-for-school-of-engineering | 学院级战略 |
| Monash Inclusive Teaching | https://www.monash.edu/learning-teaching/TeachHQ/Teaching-practices/inclusive-teaching-practices/how-to/embed-inclusive-teaching | TS 参考 |
| AU Style Manual: ATSI peoples | https://www.stylemanual.gov.au/accessible-and-inclusive-content/inclusive-language/aboriginal-and-torres-strait-islander-peoples | 大写规则 |
| Melbourne Indigenous Data Governance | https://pursuit.unimelb.edu.au/articles/indigenous-data-governance-for-the-21st-century | IDSov 参考 |
| AI Bias in AU Healthcare | https://www1.racgp.org.au/ajgp/2023/july/making-decisions | 算法偏见 |
| Indigenous HCI OzCHI workshop | https://research.monash.edu/en/publications/indigenous-hci-workshop-at-ozchi-2019-perth/ | HCI 领域 |

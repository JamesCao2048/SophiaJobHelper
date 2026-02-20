# 新西兰 Te Tiriti 策略指南

本文件被 Step 1（信号采集）和 Step 2（材料策略）读取，根据 JD 信号和学校信号的矩阵交叉，指导新西兰教职申请材料中《怀唐伊条约》相关内容的修辞策略。

**设计文档**: `docs/plans/2026-02-20-nz-te-tiriti-strategy-design.md`
**原始策略研究**: `../general/research_job_rules/新西兰教职申请：Te Tiriti 策略.md`

---

## 一、信号等级定义

### 1.1 JD 信号等级

| level | 判定条件 | 典型表现 |
|-------|---------|---------|
| `no_mention` | JD 实质性评估板块无任何条约相关词汇，仅有页脚 EEO 样板 | "The University is an equal opportunity employer" |
| `boilerplate` | 出现关键词但位于通用要求/nice-to-have 区域，非核心考核项 | "An appreciation of bicultural values" 在 Desirable Attributes 末尾 |
| `explicit` | 关键词出现在 Key Responsibilities / Essential Criteria / Skills and Attributes 等硬性考核板块 | "Demonstrated understanding of Te Tiriti o Waitangi and its application to tertiary education" 在 Essential Skills |

#### 扫描关键词清单

**核心词（高权重）：**
Te Tiriti, Treaty of Waitangi, Māori, Pasifika, Bicultural competence, Bicultural capability, Tangata Whenua, Mātauranga Māori, Tikanga, Kaupapa Māori

**辅助词（低权重，结合位置判断）：**
Te Reo, iwi, hapū, whānau, data sovereignty, indigenous, kaitiakitanga, whanaungatanga, manaakitanga, tino rangatiratanga, oritetanga

#### 位置权重规则

- Essential Criteria / Key Responsibilities / Selection Criteria 中出现 → **`explicit`**
- Desirable / Nice-to-have / About the University 中出现 → **`boilerplate`**
- 仅在 EEO 声明 / 页脚 / 学校简介样板中出现 → **`no_mention`**

来源: [^8][^9][^21]

### 1.2 学校信号等级

| level | 判定条件 | 典型表现 |
|-------|---------|---------|
| `light` | 学校网站仅有标准条约致敬声明（acknowledgement），无专门战略文件或框架 | 页脚 "We acknowledge the Treaty of Waitangi" |
| `moderate` | 有正式条约政策或战略文件，但未深入到院系层面的具体实施框架，无专有术语体系 | Massey 的 Tiriti o Waitangi Policy [^54] |
| `strong` | 有深度条约战略框架 + 院系级实施机制 + 校级专有毛利价值观术语命名 | Auckland 的 Waipapa Taumata Rau [^95]；VUW 的 Te Tiriti Statute [^4]；Waikato 的 Treaty Statement [^56] |

**评估信号来源（优先级从高到低）：**
1. 学校官方 Treaty Statement / Te Tiriti Policy
2. 学校战略规划文件（如 Strategic Plan 2030）
3. Māori Strategic Framework（如有）
4. 招聘政策/流程中的条约相关条款
5. Pro-Vice-Chancellor (Māori) 的存在与职权范围

---

## 二、策略矩阵

| JD signal \ School signal | `light` | `moderate` | `strong` |
|---------------------------|---------|-----------|----------|
| `no_mention` | **`skip`** | **`subtle`** | **`moderate`** |
| `boilerplate` | **`subtle`** | **`moderate`** | **`strong`** |
| `explicit` | **`moderate`** | **`strong`** | **`full_treaty`** |

**Agent 上调/下调说明：**
- 典型上调场景：JD 虽是 `boilerplate` 但已知该校面试必考条约题（如 Auckland、VUW）→ 可上调一级，并在 `strategy_rationale` 中注明
- 典型下调场景：school_signal=`strong` 但该院系 JD 明确技术导向、无任何条约相关词汇 → 维持矩阵结果，不下调（学校信号仍构成背景风险）

---

## 二.五、升级门槛规则

**核心原则：** `moderate` 是默认天花板。升级到 `strong` 或 `full_treaty` 必须满足明确的证据门槛，且系统必须向用户显式说明升级理由。

### `strong` 触发条件（必须同时满足）

1. JD 或 School signal 中至少有一个 ≥ `explicit` 或 `strong`（矩阵硬性要求）
2. fit_report 中必须列出触发升级的**具体原文证据**（不能是 agent 的推测）
3. Step 2 在 fit_report 中用醒目标记提示用户：

```
⚠ 策略升级: moderate → strong
触发证据:
  - JD Essential Criteria: "Demonstrated understanding of Te Tiriti o Waitangi
    and its application to tertiary education" (jd_main.md, bullet 4)
  - 学校: VUW Te Tiriti Statute（校董会正式立法）
建议: 材料中需要三条款结构化段落。请确认是否采纳。
```

### `full_treaty` 触发条件（最严格）

1. JD signal = `explicit` **且** School signal = `strong`（矩阵唯一入口，不接受 agent 上调）
2. JD 中必须有**至少 2 条**独立的条约相关要求出现在 Essential Criteria
3. fit_report 中必须**暂停并询问用户确认**后才写入最终策略标签：

```
⚠ 最高级策略触发: full_treaty
触发证据:
  - JD Essential Criteria #3: "Demonstrated understanding of Te Tiriti o Waitangi..."
  - JD Essential Criteria #6: "Commitment to bicultural practice..."
  - 学校: Auckland Waipapa Taumata Rau 战略框架 + PVC(Māori) 参与审查
此级别将在 Cover Letter 中加入 200-250 词专门段落、Research Statement
中加入 300-400 词独立小节。
请确认: 采纳 full_treaty / 降级为 strong / 用户自定
```

### Agent 上调限制

- Agent 可将矩阵结果上调**至多一级**，且仅限 skip→subtle 或 subtle→moderate
- **禁止** agent 自行上调到 strong 或 full_treaty
- 所有上调必须在 `strategy_rationale` 中注明理由

### 全量模式中断规则

当 Step 10.5（NZ）的矩阵初判结果为 `strong` 或 `full_treaty` 时：

1. Step 1 正常完成所有其他子步骤
2. 在 `step1_summary.md` 顶部醒目标注中断警告
3. **全量模式（一键/全流程）下**：pipeline 在 Step 1 完成后**自动中断**，不进入 Step 2，等待用户审查 step1_summary 后手动触发继续
4. **单步模式下**：Step 1 正常结束，用户自然会在触发 Step 2 前看到 summary 中的警告

---

## 三、Sophia 背景校准：Claim vs Aspire

基于 Sophia 的真实研究经历（`materials/Research_Statement.md`, `materials/Teaching_Statement.md`）。
Step 2 读取 Sophia 材料时识别可 Claim 的具体锚点，Step 3 生成时严格遵守此映射。

| 条约条款 | **Claim**（有真实经历支撑） | **Aspire**（无经历，只能表达意愿+计划） |
|---------|--------------------------|----------------------------------------|
| **Kāwanatanga** (伙伴关系) | 参与式设计方法论（user studies, interviews, co-design）；跨学科跨文化协作（JHU, SMART/Singapore, NUS, Notre Dame）；开源平台建设（MindCoder.ai, CollabCoder）体现的共享精神 | 与 iwi/hapū 建立研究共治关系；Kaupapa Māori 研究框架的具体应用 |
| **Tino Rangatiratanga** (数据主权) | 对 trustworthy AI 的核心研究关注；"keep humans at the center"是核心研究主张；MindCoder.ai/CollabCoder 保障用户对分析过程的掌控 | Māori Data Sovereignty 具体技术实践；CARE 原则实施；数据本地化存储架构 |
| **Ōritetanga** (公平) | Human-AI 协作中对人类 agency 和信任的系统性研究；对纯 AI 自动化风险的批判性立场；指导多元背景学生的经验 | 针对毛利群体的算法审计；NZ 特定数字包容性设计 |

### 修辞天花板规则（Step 3 Humanizer 强制检查项）

1. **Claim 部分用具体经历支撑，Aspire 部分用"学习意愿 + 具体计划"框架**
   - ✅ "My participatory design methodology, demonstrated in [具体项目], provides a methodological foundation I am eager to adapt within a Kaupapa Māori framework upon joining [University]."
   - ❌ "I have extensive experience working with indigenous communities on data sovereignty."

2. **引用 NZ 本土概念时，用"已了解 + 希望深入"的框架**
   - ✅ "I have studied Te Mana Raraunga's principles and see clear alignment with my commitment to human control over AI processes. I look forward to engaging with [University]'s [专有框架] to deepen this understanding."
   - ❌ "My work directly implements Māori Data Sovereignty principles."

3. **可以画平行线但必须立刻收回** [^27]：新加坡的跨文化协作经验可作"适应力"证据，但必须强调 Te Tiriti 赋予毛利人的宪法伙伴地位是独一无二的，不可简单类比。

4. **具体技术落地点要诚实**：MindCoder.ai/CollabCoder 的人类控制权设计是 Tino Rangatiratanga 最真实的连接点，但不要夸大成"这就是 Data Sovereignty 实践"。

来源: [^8][^27]

---

## 四、通用禁忌（所有级别）

以下错误在任何级别都负面，级别越高后果越严重：[^13][^16][^23][^25][^27]

1. **把它写成美式 Diversity Statement**：只谈"包容少数族裔"、"intersectionality"、"underrepresented minorities" → 在 NZ 语境下暴露完全不了解该国宪政框架，直接低分
2. **把毛利人归为"少数族裔"之一**：毛利人是条约缔约方，拥有独特宪法地位
3. **泛泛说"我尊重多元文化"**：暴露未做功课，缺乏具体性
4. **不懂装懂**：伪装成已有毛利社区合作经验 → 面试时会被识破
5. **套用其他国家原住民经验**：北美印第安部落、澳洲 Aboriginal 经验不可直接类比

---

## 五、各策略标签修辞指南

### `skip`（JD=no_mention, School=light）

**场景：** JD 不提，学校承诺也浅。强行插入喧宾夺主。

| 文档 | 策略 |
|------|------|
| Cover Letter | 不加任何条约内容 |
| Research Statement | 无特殊调整 |
| Teaching Statement | 无特殊调整 |

**重要：** fit_report 中仍需展示两层证据（JD 原文扫描结果 + 学校页面内容），让用户知情并可自行覆盖决策。来源: [^49]

---

### `subtle`（JD=no_mention+School=moderate, 或 JD=boilerplate+School=light）

**场景：** 信号微弱但不为零。展示"做过功课 + 有学习意愿"即可。

| 文档 | 策略 |
|------|------|
| Cover Letter | 末尾或学术价值观段落嵌入 1-2 句，核心：学习意愿 + 文化敏感度 |
| Research Statement | 不做专门调整 |
| Teaching Statement | 如篇幅允许，末尾加半句对 Māori/Pasifika 学生的关注 |

**Cover Letter 范式（Sophia 适用）：**

> "As an international scholar committed to inclusive research practice, I am strongly motivated to engage with the bicultural environment of Aotearoa New Zealand. I look forward to participating in professional development on Te Tiriti o Waitangi to ensure my teaching and research respectfully support the success of Māori and Pasifika students."

来源: [^21][^49]

---

### `moderate`（矩阵中间三格）

**场景：** 有一定信号但不构成核心考核项。需展示理解，不必逐条款展开。

| 文档 | 策略 |
|------|------|
| Cover Letter | 一段（约 100-150 词），概括性提及条约精神与自身研究/教学的关联 |
| Research Statement | 嵌入一句 Data Sovereignty 意识，不单独成节 |
| Teaching Statement | 一句对 Māori/Pasifika 学生学业成功的承诺 |

**Cover Letter 范式（Sophia 适用）：**

> "My research vision aligns with the principles of Te Tiriti o Waitangi. My work on human–AI collaboration is grounded in participatory methods that prioritise human agency and control — values that resonate with the Treaty's emphasis on partnership and self-determination. I am committed to ensuring that AI systems I develop contribute to equitable outcomes, and I look forward to deepening my understanding of how these principles apply within Aotearoa's unique bicultural context."

**Research Statement 嵌入句范式：**

> "In pursuing open and trustworthy AI research, I am mindful of emerging frameworks such as the CARE Principles for Indigenous Data Governance, which complement FAIR principles by centring collective benefit, authority to control, responsibility, and ethics — principles I look forward to engaging with more deeply in the Aotearoa context."

**Teaching Statement 嵌入句范式：**

> "I am committed to culturally responsive pedagogy that supports the academic success of all students, including Māori and Pasifika learners whose success is a priority for New Zealand's tertiary sector."

**如果 school_signal=strong：** 引用该校专有框架名称（"aligning with [University]'s [框架名] commitment to..."）。

来源: [^37][^49]

---

### `strong`（JD=boilerplate+School=strong, 或 JD=explicit+School=moderate）

**场景：** 条约能力是实质考核维度。需要结构化三条款回应。

| 文档 | 策略 |
|------|------|
| Cover Letter | 专门段落（200-250 词），三条款结构化回应（Claim+Aspire 混合） |
| Research Statement | 单独小节 "Responsible AI & Data Sovereignty"（150-200 词） |
| Teaching Statement | Māori/Pasifika 支持段（100-150 词） |

**Cover Letter 三条款回应框架（Sophia 适用）：**

> **Kāwanatanga (Partnership):** "My research methodology centres on participatory design, where domain experts are active collaborators rather than passive subjects. At [JHU / SMART], I co-designed AI systems with [healthcare professionals / educators], building trust through shared ownership of the research process. I see this approach as a foundation I am eager to adapt within Kaupapa Māori research frameworks, learning to build authentic partnerships with Māori communities as I develop my understanding of local tikanga."
>
> **Tino Rangatiratanga (Self-determination):** "A core conviction of my work is that humans must retain meaningful control over AI-driven analysis — reflected in my platforms MindCoder.ai and CollabCoder, which keep users in command of every analytical decision. This commitment to human agency aligns with the spirit of Māori Data Sovereignty, and I am keen to engage with Te Mana Raraunga's principles to ensure my future research in Aotearoa respects indigenous data governance." [^43][^68]
>
> **Ōritetanga (Equity):** "My research critically examines the risks of unchecked AI automation, demonstrating that purely automated analysis can miss nuance and perpetuate existing biases. As a faculty member, I am committed to extending this critical lens to ensure AI tools do not exacerbate inequities for Māori and Pasifika communities, and to designing inclusive systems accessible across diverse user groups."

**Research Statement 小节范式：**

> "**Responsible AI & Data Sovereignty.** As AI systems increasingly process sensitive human data, questions of who controls data collection, analysis, and application become paramount. My human-centred approach — ensuring transparency, user control, and rigorous validation — provides a natural foundation for engaging with Indigenous data governance frameworks. In the Aotearoa New Zealand context, I am particularly drawn to the principles articulated by Te Mana Raraunga [^43][^68], which position data as a taonga (treasure) subject to Māori governance. I look forward to exploring how my human–AI collaboration architectures can be designed to honour these principles, balancing open-science mandates (FAIR) with indigenous data ethics (CARE)." [^37]

**Teaching Statement Māori/Pasifika 段范式：**

> "I am committed to supporting the academic success of Māori and Pasifika students. Drawing on my experience mentoring students from diverse cultural backgrounds across Singapore, the US, and Hong Kong, I recognise that effective teaching requires adapting to students' cultural contexts. I look forward to learning about pedagogical approaches such as Tuākana-Teina (senior-junior mentoring) and to fostering collaborative learning communities where all students can thrive." [^87]

**如果 school_signal=strong：** 必须引用该校专有框架术语（见§六学校种子表中的 key_values）。

来源: [^12][^37][^43][^58][^87]

---

### `full_treaty`（JD=explicit, School=strong）

**场景：** 最高规格。条约能力是硬性门槛，学校有深度框架。

| 文档 | 策略 |
|------|------|
| Cover Letter | 三条款深度回应 + 引用该校专有框架/术语 + 考虑 PVC(Māori) 受众 |
| Research Statement | 专门一节 "Responsible AI in Aotearoa"（300-400 词） |
| Teaching Statement | Māori/Pasifika 支持段 + Mātauranga Māori integration 构想 |

**在 `strong` 基础上的升级点：**

**Cover Letter 升级：**
- 三条款回应中加深技术细节（具体"如何做"而非"我会做"）
- 引用该校专有框架 + 核心毛利价值观术语（见§六种子表）
- 如该校有 Pro-Vice-Chancellor (Māori) 参与审查 [^96]，措辞需额外审慎

**Research Statement 完整小节升级（在 `strong` 基础上增加）：**
- 引用 NZ 本土 CS 研究案例作为未来合作方向（Aspire 框架）：
  - Hakituri IoT 项目：毛利工人共同定义数据收集和使用方式 [^62]
  - Mātauranga Māori in Computing [^85][^86]
- 经费叙事指向 Marsden Fund / MBIE 中的 Responsiveness to Māori 要求 [^23]
- FAIR vs CARE 平衡的具体技术设想（如中介访问机制、训练语料审计）[^37][^103]

**Teaching Statement 升级（Mātauranga Māori Integration 构想，用 Aspire 框架）：**
- Kaitiakitanga（守护责任）融入数据伦理/网络安全教学的设想 [^35]
- Whakapapa（宗谱/关系网络）启发关系型数据库/知识图谱教学的构想 [^35]
- Whanaungatanga（建立关系/归属感）学习社群 [^87]
- 具体化学习路径（"入职后我计划参加 [University] 的 [具体培训项目]，并在第一年寻求与 [学校毛利研究中心] 的合作机会"）

**Sophia 诚实度校准（full_treaty 特别重要）：**
此级别要求最深度，但 Sophia 没有 NZ 经验。处理方式：
1. 方法论桥接：用已有的参与式设计方法论作为"可迁移的方法论基础"
2. 学习路径具体化：不只说"我愿意学习"，而是有具体的第一步计划
3. 平行经验谨慎使用 [^27]：简短提及新加坡跨文化适应力后，立刻声明"我深刻理解 Te Tiriti 赋予毛利人的宪法伙伴地位是独一无二的，不可与其他多元文化经验简单类比"

来源: [^4][^8][^27][^35][^56][^87][^95][^96]

---

## 六、学校种子表

Step 1 agent 先按 school_id 匹配种子表爬取，无种子或种子失败时搜索补充。
所有 URL 来源于原策略文档 `general/research_job_rules/新西兰教职申请：Te Tiriti 策略.md` 的引用索引，可用现有验证流程检查。

### 奥克兰大学 (University of Auckland / Waipapa Taumata Rau)

- **预判 school_signal**: strong
- **框架名**: Waipapa Taumata Rau + Taumata Teitei 2030
- **核心术语**: Manaakitanga, Whanaungatanga, Kotahitanga, Kaitiakitanga
- **种子 URL**:
  - Strategic Plan: [^95] https://www.auckland.ac.nz/en/about-us/about-the-university/the-university/official-publications/strategic-plan/purpose-vision-principles-values.html
  - Tuākana Programme: [^87] https://www.auckland.ac.nz/en/students/student-support/academic-support/tuakana-learning-communities/what-is-tuakana.html
  - Academic Staff Recruitment Procedures: [^96] https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/academic-staff-recruitment-procedures.html
  - Recruitment Policy: [^39] https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/recruitment-selection-appointment-policy.html
  - Equity for Staff: [^25] https://www.auckland.ac.nz/en/about-us/about-the-university/equity-at-the-university/equity-information-for-staff.html
  - Equity Questions in Recruitment: [^102] https://www.auckland.ac.nz/assets/about-us/about-the-university/equity-at-the-university/equity-information-staff/Appendix%202%20Equity%20Questions%20in%20Recruitment%20and%20Selection.docx
- **特殊备注**: PVC(Māori) 参与高级职位的文化胜任力评估（具体否决权限待内部文件确认，[^96] §31 支持"咨询/协助"角色）；遴选末期同等实力候选人中，毛利裔或公平目标群体优先 [^96]
- **原策略文档位置**: §182-184

### 惠灵顿维多利亚大学 (Victoria University of Wellington / Te Herenga Waka)

- **预判 school_signal**: strong
- **框架名**: Te Tiriti o Waitangi Statute
- **核心术语**: Rite tahi (结果公平), Whai wāhi (决策层代表性)
- **种子 URL**:
  - Te Tiriti Statute PDF: [^4] https://www.wgtn.ac.nz/documents/policy/governance/te-tiriti-o-waitangi-statute.pdf
  - Principle of Rite tahi: [^76] https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-rite-tahi
  - Principle of Whai wāhi: [^98] https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-whai-wahi
  - Te Tiriti guide: [^97] https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi
- **特殊备注**: 校董会正式通过具有法律效力的 Te Tiriti Statute，是 NZ 大学中制度化程度最高的
- **原策略文档位置**: §186-192

### 奥塔哥大学 (University of Otago / Ōtākou Whakaihu Waka)

- **预判 school_signal**: strong
- **框架名**: Māori Strategic Framework 2030
- **核心术语**: Kāwanataka (领导力), Tauira Māori (毛利学生)
- **种子 URL**:
  - Māori Strategic Framework 2030: [^99] https://www.otago.ac.nz/maori/maori-strategic-framework
  - Humanities MSF: [^47] https://www.otago.ac.nz/humanities/maori-at-humanities/strategic-framework
  - Te Tiriti page: [^64] https://www.otago.ac.nz/maori/world/treaty
  - Academic Staff Recruitment Guidelines: [^9] https://www.otago.ac.nz/administration/policies/academic-staff-recruitment-process-guidelines
  - HR Legislative Framework: [^46] https://www.otago.ac.nz/humanresources/toolkit/recruiting/legislative-framework
- **特殊备注**: 与南岛 Ngāi Tahu 部落有深厚历史渊源；强调学生能"以毛利人的身份生活和学习"
- **原策略文档位置**: §194-199

### 怀卡托大学 (University of Waikato / Te Whare Wānanga o Waikato)

- **预判 school_signal**: strong
- **框架名**: Treaty Statement
- **核心术语**: Mana Māori Motuhake (原住民固有权利), Mana Mātauranga Māori (毛利知识权威性)
- **种子 URL**:
  - Treaty Statement: [^100] https://www.waikato.ac.nz/about/governance/docs/university-of-waikato-treaty-statement/
  - Critical Tiriti Analysis (学术): [^56] https://www.journalofglobalindigeneity.com/article/92446-a-critical-tiriti-analysis-of-the-treaty-statement-from-a-university-in-aotearoa-new-zealand
  - Māori Data Governance Model: [^70] https://www.waikato.ac.nz/assets/Uploads/Research/Research-institutes-centres-and-groups/Institutes/Te-Ngira-Institute-for-Population-Research/Maori_Data_Governance_Model.pdf
- **特殊备注**: NZ 最早一批正式发布独立 Treaty Statement 的大学，"advanced further down this path than many other universities and public sector institutions" [^100]
- **原策略文档位置**: §201-205

### 坎特伯雷大学 (University of Canterbury / UC)

- **预判 school_signal**: moderate
- **框架名**: Bicultural Competence & Confidence
- **核心术语**: Bicultural confidence
- **种子 URL**:
  - Bicultural confidence — Employers: [^17] https://www.canterbury.ac.nz/study/study-support-info/study-related-topics/graduate-profile/employers/bicultural-confidence---competence
  - Bicultural confidence — Academics: [^61] https://www.canterbury.ac.nz/study/study-support-info/study-related-topics/graduate-profile/academics/bicultural-confidence---competence

### 梅西大学 (Massey University)

- **预判 school_signal**: moderate
- **框架名**: Tiriti o Waitangi Policy
- **种子 URL**:
  - Policy PDF: [^54] https://www.massey.ac.nz/documents/1796/Treaty_of_Waitangi_Te_Tiriti_o_Waitangi_Policy.pdf
  - Te Tiriti meets HOP: [^55] https://www.massey.ac.nz/about/news/te-tiriti-o-waitangi-principles-meets-human-and-organisational-performance/

### 奥克兰理工大学 (AUT)

- **预判 school_signal**: moderate（待验证）
- **种子 URL**:
  - Academic Standards: [^92] https://www.aut.ac.nz/__data/assets/pdf_file/0010/288955/Academic-Standards-and-Expectations.pdf
- **备注**: 种子有限，Step 1 需搜索补充 "AUT Te Tiriti strategy" 或 "AUT Māori strategic plan"

### 林肯大学 (Lincoln University)

- **预判 school_signal**: 未知
- **种子 URL**: 无
- **备注**: 原策略文档未覆盖，Step 1 完全依赖搜索

---

## 七、引用索引

引用标号对应原策略文档 `general/research_job_rules/新西兰教职申请：Te Tiriti 策略.md` 引用列表，可用 `region_knowledge/src/web_fetch.py` 验证。

| 引用 | 来源简称 | URL |
|------|---------|-----|
| [^4] | VUW Te Tiriti Statute | https://www.wgtn.ac.nz/documents/policy/governance/te-tiriti-o-waitangi-statute.pdf |
| [^8] | Reddit: NZ Faculty Advice | https://www.reddit.com/r/AskAcademia/comments/1r0afcw/seeking_advice_from_new_zealand_faculty/ |
| [^9] | Otago Recruitment Guidelines | https://www.otago.ac.nz/administration/policies/academic-staff-recruitment-process-guidelines |
| [^10] | Mana Raraunga Data Sovereignty | https://knowledgeauckland.org.nz/publications/mana-raraunga-data-sovereignty-what-is-it-and-why-does-it-matter-in-aotearoa-new-zealand/ |
| [^12] | Te Tiriti practice in health promotion | https://nwo.org.nz/wp-content/uploads/2018/10/ToW-practice-in-HP-online.pdf |
| [^13] | Diversity Statement structure | https://universityaffairs.ca/career-advice/how-to-structure-your-diversity-statement-for-your-academic-job-search/ |
| [^16] | Māori representation in university strategy | https://www.tandfonline.com/doi/full/10.1080/13613324.2024.2306379 |
| [^17] | UC Bicultural confidence — Employers | https://www.canterbury.ac.nz/study/study-support-info/study-related-topics/graduate-profile/employers/bicultural-confidence---competence |
| [^21] | NZ Govt Job Example | https://jobs.govt.nz/jobtools/jncustomsearch.viewFullSingle?in_organid=16563&in_jnCounter=226465297&in_location=%22Canterbury%22 |
| [^23] | NEAC Research Ethics NZ | https://neac.health.govt.nz/national-ethical-standards/part-one/research-in-the-new-zealand-context/ |
| [^25] | UoA Equity for Staff | https://www.auckland.ac.nz/en/about-us/about-the-university/equity-at-the-university/equity-information-for-staff.html |
| [^27] | RANZCP Te Tiriti significance | https://www.ranzcp.org/clinical-guidelines-publications/clinical-guidelines-publications-library/recognising-the-significance-of-te-tiriti-o-waitangi |
| [^35] | NZ Curriculum: CS & Mātauranga | https://newzealandcurriculum.tahurangi.education.govt.nz/case-study---strategies-to-engage-girls-in-computer-science/5637203861.p |
| [^37] | Aotearoa Genomic Data Repository (FAIR vs CARE) | https://pmc.ncbi.nlm.nih.gov/articles/PMC11696480/ |
| [^39] | UoA Recruitment Policy | https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/recruitment-selection-appointment-policy.html |
| [^43] | Te Mana Raraunga Principles | https://www.otago.ac.nz/__data/assets/pdf_file/0014/321044/tmr-maori-data-sovereignty-principles-october-2018-832194.pdf |
| [^46] | Otago HR Legislative Framework | https://www.otago.ac.nz/humanresources/toolkit/recruiting/legislative-framework |
| [^47] | Otago Humanities MSF | https://www.otago.ac.nz/humanities/maori-at-humanities/strategic-framework |
| [^49] | NZCER: Securing a position | https://www.nzcer.org.nz/sites/default/files/downloads/Optimising%20your%20academic%20career_%20ch%202_0.pdf |
| [^54] | Massey Tiriti Policy | https://www.massey.ac.nz/documents/1796/Treaty_of_Waitangi_Te_Tiriti_o_Waitangi_Policy.pdf |
| [^55] | Massey Te Tiriti meets HOP | https://www.massey.ac.nz/about/news/te-tiriti-o-waitangi-principles-meets-human-and-organisational-performance/ |
| [^56] | Waikato Treaty Analysis | https://www.journalofglobalindigeneity.com/article/92446-a-critical-tiriti-analysis-of-the-treaty-statement-from-a-university-in-aotearoa-new-zealand |
| [^58] | Kaupapa Māori publications | https://www.researchgate.net/topic/Kaupapa-Maori/publications |
| [^61] | UC Bicultural confidence — Academics | https://www.canterbury.ac.nz/study/study-support-info/study-related-topics/graduate-profile/academics/bicultural-confidence---competence |
| [^62] | Hakituri IoT / Participatory Data Design | https://academic.oup.com/iwc/article/34/2/60/6759159 |
| [^64] | Otago Te Tiriti page | https://www.otago.ac.nz/maori/world/treaty |
| [^68] | Te Mana Raraunga official site | https://www.temanararaunga.maori.nz/ |
| [^70] | Waikato Māori Data Governance Model | https://www.waikato.ac.nz/assets/Uploads/Research/Research-institutes-centres-and-groups/Institutes/Te-Ngira-Institute-for-Population-Research/Maori_Data_Governance_Model.pdf |
| [^71] | UoA Māori Data Sovereignty | https://research-hub.auckland.ac.nz/article/maori-data-sovereignty |
| [^76] | VUW Rite tahi | https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-rite-tahi |
| [^78] | NZ Digital Inclusion | https://www.digital.govt.nz/dmsdocument/196~digital-inclusion-user-insightsformer-refugees-and-migrants-with-english-as-a-second-language/html |
| [^85] | Mātauranga Māori in Computing (Unitec) | https://www.unitec.ac.nz/epress/wp-content/uploads/2024/07/12-CITRENZ2023-Proceedings-Chitalia-et-al.pdf |
| [^86] | Mātauranga Māori in Computing (Unitec ePress) | https://www.unitec.ac.nz/epress/wp-content/uploads/2024/07/12-CITRENZ2023-Proceedings-Chitalia-et-al.pdf |
| [^87] | UoA Tuākana Programme (Tuākana-Tēina 官方专页) | https://www.auckland.ac.nz/en/students/student-support/academic-support/tuakana-learning-communities/what-is-tuakana.html |
| [^92] | AUT Academic Standards | https://www.aut.ac.nz/__data/assets/pdf_file/0010/288955/Academic-Standards-and-Expectations.pdf |
| [^95] | UoA Strategic Plan | https://www.auckland.ac.nz/en/about-us/about-the-university/the-university/official-publications/strategic-plan/purpose-vision-principles-values.html |
| [^96] | UoA Academic Recruitment Procedures | https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/academic-staff-recruitment-procedures.html |
| [^97] | VUW Te Tiriti guide | https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi |
| [^98] | VUW Whai wāhi | https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-whai-wahi |
| [^99] | Otago MSF 2030 | https://www.otago.ac.nz/maori/maori-strategic-framework |
| [^100] | Waikato Treaty Statement | https://www.waikato.ac.nz/about/governance/docs/university-of-waikato-treaty-statement/ |
| [^102] | UoA Equity Questions in Recruitment | https://www.auckland.ac.nz/assets/about-us/about-the-university/equity-at-the-university/equity-information-staff/Appendix%202%20Equity%20Questions%20in%20Recruitment%20and%20Selection.docx |
| [^103] | Royal Society Te Apārangi: GenAI 研究最佳实践指南（2025年6月，§2.3 + §3.2.1 直接论及未经授权抓取 te reo Māori / mātauranga Māori 语料库） | https://www.royalsociety.org.nz/assets/Guidelines-for-the-best-practice-use-of-GenAI-in-research_Royal-Society-Te-Aparangi_June-2025_English-.pdf |

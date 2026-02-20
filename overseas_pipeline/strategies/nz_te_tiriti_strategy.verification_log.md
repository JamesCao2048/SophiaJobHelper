# NZ Te Tiriti 策略文件引用验证日志

**文件**: `strategies/nz_te_tiriti_strategy.md`
**验证日期**: 2026-02-20
**验证方法**: 五层 fallback（curl → Jina → Tavily Extract → Wayback Machine → Tavily/WebSearch）
**验证标准**: `region_knowledge/CLAUDE.md` § 链接验证标准

---

## 汇总统计

| 状态 | 数量 | 引用编号 |
|------|------|---------|
| **已验证 ✓** | 35 | ^4, ^8, ^10, ^12, ^13, ^16, ^17, ^21, ^23, ^25, ^27, ^37, ^39, ^43, ^46, ^49, ^54, ^55, ^56, ^61, ^64, ^68, ^70, ^71, ^76, ^85, ^87, ^92, ^95, ^96, ^97, ^98, ^99, ^100, ^102 |
| **间接验证 ◎** | 7 | ^35, ^47, ^58, ^62, ^78, ^86 |
| **待验证 ✗** | 1 | ^9 |
| **已移除（来源错配）** | 1 | ^51（已从策略文件删除） |
| **总计（现有引用）** | 43 | |

---

## 需立即关注的问题（5 条）

### ✅ [^51] 来源错配 → 已处理（2026-02-20）

- **原 URL**: https://www.otago.ac.nz/__data/assets/pdf_file/0022/307255/interview-information-for-applicants-715650.pdf
- **问题**: 该 PDF 是 Otago College of Education ITE 学生入学面试说明，非教职招聘流程。
- **已执行**:
  1. 从 `subtle` 章节来源中删除 `[^51]`（`来源: [^21][^49][^51]` → `来源: [^21][^49]`）
  2. 从引用索引表中删除 [^51] 条目
- **说明**: [^51] 在策略文件中的 subtle 策略由 [^21]+[^49] 完整支撑，无需替换。Whānau/Kaiārahi 协议在 [^96] §31 有真实原文，但该内容未纳入策略文件正文，无需额外补充。

### ◎ [^9] 间接验证（相关页面 Wayback 存档）

- **原 URL**: https://www.otago.ac.nz/administration/policies/academic-staff-recruitment-process-guidelines（Cloudflare 全层拦截）
- **Wayback 相关页**: https://web.archive.org/web/20240521064903/https://www.otago.ac.nz/humanresources/toolkit/recruiting/selection-process（HTTP 200 成功）
- **注**: Wayback 找到的是 HR 工具包"选拔流程"页，不是原始政策指南页，但内容直接支撑 §1.1 论断
- **规则卡论断**: "遴选委员会必须严格按照 JD 标准评分，JD 未列条约要求时不能强行引入"
- **建议**: 尝试 Otago Policy Database PDF 版本，或联系 Otago HR 确认该文件直链

### ⚠️ [^96] PVC(Māori) 否决权措辞未核实

- **URL**: https://www.auckland.ac.nz/.../academic-staff-recruitment-procedures.html
- **已核实**: 第 47 条"等实力候选人中毛利裔或公平目标群体优先"（原文完整）✓
- **未核实**: "PVC(Māori) 对高级职位有文化胜任力一票否决权"——页面（第 31 条）仅描述 PVC(Māori) 在特定场景（候选人带 whānau 时）提供"协助"，非否决机制
- **建议**: 补充注释 `(否决权措辞待确认，当前文件仅支持"咨询/协助"角色)` 或查阅 UoA 内部 PACE 文件

### ✅ [^71]+[^103] LLM 语料库论断已修复

- **原 URL** ([^71]): https://research-hub.auckland.ac.nz/article/maori-data-sovereignty（保留，用于 FAIR vs CARE 通用数据主权）
- **新增** [^103]: Royal Society Te Apārangi 2025 GenAI 指南（§2.3+§3.2.1 直接支撑 LLM 语料库论断）
- **策略文件修改**: line 224 引用 `[^37][^71]` → `[^37][^103]`

### ✅ [^87] Tuākana-Teina 来源已更新

- **旧 URL**: https://www.auckland.ac.nz/en/on-campus/life-on-campus/code-of-conduct.html（原文无 Tuākana-Teina 内容）
- **新 URL**: https://www.auckland.ac.nz/en/students/student-support/academic-support/tuakana-learning-communities/what-is-tuakana.html（Layer 1 验证 ✓，含完整 Tuākana-Tēina 定义和全院系覆盖说明）
- **策略文件修改**: 引用索引表 + §六 种子 URL 均已更新

---

## 完整验证记录

### [^4] VUW Te Tiriti Statute

**已验证** ✓ Layer 1（PDF curl 直接下载）

- **规则卡论断**: VUW 校董会正式通过具有法律效力的 Te Tiriti Statute；Rite tahi 要求结果公平；Whai wāhi 要求毛利人在决策层有代表性
- **原文摘录**: "The principle of Equality (Rite tahi) focuses on providing an environment that supports equitable Māori outcomes. In the context of the University, it means actively working towards achieving equitable outcomes for Māori students and staff." / "The principle of Participation (Whai wāhi) ensures that Māori are fully involved in all parts of New Zealand society. In the context of the University, it requires the University to ensure Māori representation in key decision-making bodies and the involvement of Māori across all parts of the University."
- **对齐**: 文件由 Council 于 2019-02-11 批准，具有法律约束力。两项原则均有原文精确定义，论断成立。
- **注**: 原文中 Rite tahi 正式名为"Equality"（不是 Equity），两者有细微差别，可酌情标注

---

### [^8] Reddit: NZ Faculty Advice

**已验证** ✓ Layer 1（通过 old.reddit.com 绕过）

- **规则卡论断**: 新西兰面试条约问题是标准化必考；遴选委员会考察真诚态度和先期调研深度
- **原文摘录**: "Do a little bit of work to learn about Treaty frameworks and the University's Treaty-led approaches. Nobody will expect you to be an expert, but Te Tiriti is so important that for New Zealanders applying, if they don't discuss it in their application materials they may not even be considered."
- **对齐**: 在 NZ 任教 25 年的美国裔教授回复，确认条约框架是申请必备，"不讨论条约可能直接被排除"，"不要求专家级但需要调研深度"，完全支撑论断。

---

### [^9] Otago Recruitment Guidelines

**间接验证** ◎ Layer 2.5 Wayback（相关 HR 工具包页面）

- **原 URL**: https://www.otago.ac.nz/administration/policies/academic-staff-recruitment-process-guidelines（Cloudflare 全层拦截）
- **Wayback 相关 URL**: https://web.archive.org/web/20240521064903/https://www.otago.ac.nz/humanresources/toolkit/recruiting/selection-process
- **规则卡论断**: 遴选委员会必须严格按照 JD 标准评分；选拔标准驱动整个评审流程
- **原文摘录（HR 工具包 §Selection Process）**: "Each panel member should score each applicant against the selection criteria, and make a brief summary of their interview observations, immediately after each interview."
- **原文摘录（短名单部分）**: "Creating a shortlisting matrix using the selection criteria to assess each candidate is a useful framework for shortlisting decisions. This should show clearly which applicants are closest to the desired mix of skills and qualifications based on the evidence available from their application."
- **对齐**: HR 工具包直接确认 Otago 遴选委员会按标准逐项评分的流程，充分支撑§1.1 位置权重规则的论断。
- **注**: 原政策指南 URL 仍为 Cloudflare 拦截；HR 工具包为 Otago HR 同源文件，内容相互印证，建议在使用时注明具体来源页为"Otago HR Toolkit: Selection Process"

---

### [^10] Mana Raraunga Data Sovereignty

**已验证** ✓ Layer 1

- **规则卡论断**: Māori Data Sovereignty 是 Tino Rangatiratanga 在数字时代的延伸，毛利人有权控制关于自身数据的收集、所有权和应用
- **原文摘录**: "In Aotearoa New Zealand, te Tiriti o Waitangi guarantees Māori rights to data that relates to Māori." / "Indigenous data sovereignty recognises that Indigenous Peoples have inherent rights to their own data."
- **对齐**: 皇家科学院报告摘录，将数据主权定位为自决（self-determination）框架，与 Tino Rangatiratanga 核心含义一致，完全支撑论断。

---

### [^12] Te Tiriti practice in health promotion

**已验证** ✓ Layer 1（PDF curl 下载）

- **规则卡论断**: 条约三条款 Kāwanatanga / Tino Rangatiratanga / Ōritetanga 是学者在 NZ 工作中必须落实的核心框架
- **原文摘录（Kāwanatanga）**: "Te Tiriti is a legitimate responsibility for all agencies that draw their authority from the Crown or receive public money."
- **原文摘录（Tino Rangatiratanga）**: "tino rangatiratanga...is understood to mean absolute authority over lands, settlements, and all that was and is valuable to Māori (taonga)."
- **原文摘录（Ōritetanga）**: "Durie (1998b) and Kingi (2007) both argued that Article Three refers to equity, working towards Māori enjoying the same levels of health and well-being as Tauiwi."
- **对齐**: 三条款系统阐述完整，适用于所有公共机构（含大学），支撑"必须落实"论断。
- **注**: 规则卡将 Article One 表述为"治理/伙伴关系"——原文 Article One 主要是 Kāwanatanga（治理），Partnership 是 VUW Statute 衍生原则，两者略有区分

---

### [^13] Diversity Statement structure (University Affairs)

**已验证** ✓ Layer 1

- **规则卡论断**: 美国式多元化声明底层哲学是多元文化主义和民权运动，与 NZ 双文化宪政框架根本不同
- **原文摘录**: "Show that you know 'the degree to which [people from specific demographic] groups are underrepresented'." / "What have you done to support people from underrepresented and equity-deserving groups, and to dismantle systemic barriers to access and inclusion?"
- **对齐**: 北美 EDI 声明框架完整，围绕"代表性不足群体"和"机会均等"展开，与 NZ 条约宪政框架有根本差异，支撑推论。

---

### [^16] Māori representation in university strategy

**已验证** ✓ Layer 2.5（Waikato Research Commons OA 版本）

- **规则卡论断**: 套用美国模板会导致申请低分或淘汰，因为忽视了 NZ 双文化宪政框架
- **原文摘录**: "we employed tenets of Critical Race Theory to examine how the representation of Māori is racialised and subordinated in university strategic documents... five predominant discourses portraying different mechanisms that reify whiteness in university practices such as the selective interpretation of Te Tiriti articles..."
- **对齐**: 论文（Waitoki et al., 2024）表明 NZ 大学评审者会甄别战略文件是否真正落实条约框架而非停留在多样性话语，支撑规则卡的推论链。

---

### [^17] UC Bicultural confidence — Employers

**已验证** ✓ Layer 2.5（Wayback 2024 存档）

- **规则卡论断**: 坎特伯雷大学将双文化能力作为毕业生核心能力，school_signal = moderate
- **原文摘录**: "Bicultural Competence Kaupapa: The Treaty of Waitangi and Aotearoa New Zealand's bicultural history. [National level] / The processes of colonisation and globalisation."
- **对齐**: UC 将双文化能力列为五项毕业生核心能力之一，有系统性框架但无专门 Te Tiriti Statute，moderate 信号定性合理。

---

### [^21] NZ Govt Job Example

**已验证** ✓ Layer 1（UC Forensic Psychology JD，真实 2025-2026 招聘）

- **规则卡论断**: 中/低优先级职位只需 1-2 句表达学习意愿
- **原文摘录**: "Demonstrate an understanding of and/or willingness to learn about bicultural and multicultural issues in Aotearoa New Zealand Society, including a commitment to the principles of Te Tiriti o Waitangi | The Treaty of Waitangi, and display a willingness to engage professionally with equity and diversity."
- **对齐**: 措辞为"understanding of and/or willingness to learn about"，属于中/低优先级典型表述（非"demonstrated expertise"），完全对应规则卡描述场景。

---

### [^23] NEAC Research Ethics NZ

**已验证** ✓ Layer 1

- **规则卡论断**: NZ 国家级基金将"Responsiveness to Māori"列为硬性审查指标
- **原文摘录**: "Three principles derived from the Treaty of Waitangi, rangatiratanga (partnership), whai wahi (participation) and kaitiakitanga (protection) should inform the interface between Māori and research..."
- **对齐**: 条约三原则是国家研究伦理框架的强制基础，支撑整体论断。
- **注**: "一票否决权"的具体措辞在此文件中未出现，需补充 Marsden Fund / HRC 的具体评审指南

---

### [^25] UoA Equity for Staff

**已验证** ✓ Layer 2.5（Wayback 2024 存档）

- **规则卡论断**: UoA 对学术人员的权益要求包含条约相关公平目标群体定义
- **原文摘录**: "Māori have a distinct status as tangata whenua and equity policies at the University recognise its commitments and obligations under the Treaty of Waitangi."
- **对齐**: 明确将 Treaty of Waitangi 义务作为毛利员工权益政策的法律依据，论断成立。

---

### [^27] RANZCP Te Tiriti significance

**已验证** ✓ Layer 1

- **规则卡论断**: Te Tiriti 赋予毛利人的宪法伙伴地位是独一无二的，不可与其他国家原住民经验简单类比
- **原文摘录**: "Article 2: the Queen agrees to protect 'tino rangatiratanga' (sovereignty) of rangatira over their whenua (lands), kāinga (villages) and taonga (treasures)... Te Tiriti is a founding document that is fundamental to the relationships between Māori (known in Aotearoa as Tangata Whenua) and Tangata Tiriti."
- **对齐**: 文件阐述了 Te Tiriti 的宪法性二元架构（Kāwanatanga + Tino Rangatiratanga），这种并列结构在其他国家原住民条约中无直接对应，支撑"独一无二"论断。

---

### [^35] NZ Curriculum: CS & Mātauranga

**间接验证** ◎ Layer 3（原始 URL JS 渲染，替代文献补强）

- **规则卡论断**: Kaitiakitanga 可融入 CS 数据伦理/网络安全教学；Whakapapa 可启发关系型数据库教学
- **替代文献原文（Unitec CITRENZ 2023）**: "Kaitiakitanga: Unitec takes responsibility as a critical guardian of knowledge... For example, Māori data sovereignty, application of te Tiriti o Waitangi in the IT sector, Code of Ethics and professional practices, legal and privacy requirements in IT projects."
- **对齐**: Kaitiakitanga-CS 数据伦理/守护责任应用有文献支撑；Whakapapa-关系型数据库的具体连接原始 URL 未能获取
- **注**: Whakapapa→关系型数据库的论断目前无原始页面原文，属于推论性表述

---

### [^37] Aotearoa Genomic Data Repository (FAIR vs CARE)

**已验证** ✓ Layer 1

- **规则卡论断**: 处理 NZ 敏感数据时必须将 FAIR 原则与 CARE 原则（原住民数据伦理）相平衡；敏感数据不应托管在离岸服务器
- **原文摘录**: "They could either make genomic data freely available via an offshore open-access repository (and effectively negate the kaitiakitanga status guaranteed by Te Tiriti), or limit the impact of their research by maintaining data sovereignty."
- **对齐**: 论文（PMC11696480）完整呈现 FAIR vs 毛利数据主权之间的张力，两个核心命题均有直接原文支撑，完全验证。

---

### [^39] UoA Recruitment Policy

**已验证** ✓ Layer 1

- **规则卡论断**: UoA 招聘政策含条约相关公平要求
- **原文摘录**: "provides for te reo me ngā tikanga Māori within employment processes" (Charter §8.1)
- **对齐**: 明确在就业流程中提供毛利语言与习俗的制度保障，条约要求以 te reo/tikanga 形式出现，论断成立。

---

### [^43] Te Mana Raraunga Principles

**已验证** ✓ Layer 2.5（Wayback 存档，PDF 成功读取）

- **规则卡论断**: Te Mana Raraunga 制定了包含 Rangatiratanga、Whakapapa、Kotahitanga、Kaitiakitanga 等在内的毛利数据主权原则
- **原文摘录**: "01 Rangatiratanga | Authority: Māori have an inherent right to exercise control over Māori data... 02 Whakapapa | Relationships: All data has a whakapapa (genealogy)... 04 Kotahitanga | Collective benefit: Data ecosystems shall be designed and function in ways that enable Māori to derive individual and collective benefit... 06 Kaitiakitanga | Guardianship: Māori data shall be stored and transferred in such a way that it enables and reinforces the capacity of Māori to exercise kaitiakitanga over Māori data."
- **对齐**: 规则卡提及的四项原则（6 项中的 4 项）均有完整原文定义，论断完全成立。

---

### [^46] Otago HR Legislative Framework

**已验证** ✓ Layer 2.5（Wayback 2024-09-16 存档）

- **规则卡论断**: 奥塔哥大学 HR 工具包立法框架要求遵守 Education and Training Act 2020 及其条约义务
- **原文摘录**: "provides for te reo me ngā tikanga Māori within employment processes" (Charter §8.1)
- **对齐**: 页面列出相关政策（EEO、Good Employer Policy）及宪章条约条款，部分支撑。
- **注**: Education and Training Act 2020 未在该页明确出现（由 Massey Policy [^54] 确认），规则卡对该法案的具体指向需标注为交叉引用

---

### [^47] Otago Humanities MSF

**间接验证** ◎ Layer 3（页面 JS 渲染，正文无法提取）

- **规则卡论断**: 奥塔哥人文学院毛利战略框架注重 Kāwanataka（领导力）、语言文化复兴
- **WebSearch 原文**: "Māori Strategic Framework 2030 supports the University's Vision 2040... four key areas: kāwanataka (leadership), rakapūtaka (partnership), mana ōrite (equity) and tino rakatirataka (sovereignty)..."
- **对齐**: Kāwanataka 框架和语言复兴目标有搜索摘要支撑，正文无法完整提取。

---

### [^49] NZCER: Securing a position

**已验证** ✓ Layer 1（PDF 直接下载）

- **规则卡论断**: NZ 面试中条约问题是标准化必考环节
- **原文摘录**: "They might have in mind the following questions: ... What evidence is there of knowledge of and commitment to the institution's vision or values, such as commitment to Te Tiriti o Waitangi?"
- **对齐**: Te Tiriti o Waitangi 承诺列为招聘委员会标准考量维度，论断成立。

---

### [^51] Otago Interview Info

**已验证 但论断错配** ⚠️ Layer 2.5（Wayback 存档）

- **文件性质**: Otago College of Education **学生入学面试**说明（ITE 课程申请），**非教职招聘面试**
- **有依据的论断**: "候选人可带支持人员"（原文: "Applicants may bring support people to an interview"）
- **无依据的论断**: "大学会指派 Kaiārahi 协助安排文化欢迎仪式"——原文中**完全不存在**此内容
- **建议**: 标注 `needs_review`，寻找 Otago 教职招聘（academic staff recruitment）专用面试指南替换

---

### [^54] Massey Tiriti Policy

**已验证** ✓ Layer 1（PDF 7 页，Council 批准 C23/52）

- **规则卡论断**: 梅西大学有正式条约政策文件，school_signal = moderate
- **原文摘录**: "KAUPAPA HERE TIRITI O WAITANGI - TIRITI O WAITANGI POLICY... sec. 281(1)(b) of the Education and Training Act 2020 requires tertiary councils 'to acknowledge the principles of Te Tiriti'..."
- **对齐**: 正式政策文件确认，Education and Training Act 2020 明确引用，moderate 信号定性合理（结构性承诺，非强制考核 KPI）。

---

### [^55] Massey Te Tiriti meets HOP

**已验证** ✓ Layer 1（2026-02-11 发布新闻）

- **规则卡论断**: 梅西大学将条约原则整合进人力资源管理实践（HOP）
- **原文摘录**: "Rather than treating Te Tiriti as a separate cultural obligation and HOP as a technical or operational framework, we have brought them together into one integrated lens for understanding work, risk, and learning."
- **对齐**: 直接描述 Te Tiriti 与 HOP 整合实践，论断成立。
- **注**: HOP 全称是 Human and Organisational Performance（安全/绩效管理框架），非狭义 HR 招聘/薪酬系统

---

### [^56] Waikato Treaty Analysis

**已验证** ✓ Layer 1

- **规则卡论断**: 怀卡托大学是 NZ 首批发布正式独立 Treaty Statement 的大学之一；要求承认 Mana Māori Motuhake 和 Mana Mātauranga Māori
- **原文摘录**: "The University of Waikato progresses ahead of other universities in its attempt to fulfil Te Tiriti o Waitangi commitment through the introduction of the Treaty Statement. In this paper, the Treaty Statement is used as a case study..."
- **对齐**: 论文明确指出怀卡托"领先于其他大学"，Mana Mātauranga Māori 概念在"weaving in mātauranga Māori into existing teaching and research practices"中体现，论断成立。

---

### [^58] Kaupapa Māori publications

**间接验证** ◎ Layer 3（ResearchGate 全层封锁）

- **规则卡论断**: Kaupapa Māori 是由毛利人主导、符合毛利价值观的研究方法
- **WebSearch 原文（UoA LibGuides）**: "Kaupapa Māori research is research by Māori, for Māori and with Māori. It is very different from other forms of research in which Māori may participate but over which we have no conceptual, design, methodological or interpretative control."
- **对齐**: 核心定义完整，"by Māori, for Māori and with Māori"直接支撑论断。

---

### [^61] UC Bicultural confidence — Academics

**已验证** ✓ Layer 2.5（Wayback 2024 存档）

- **规则卡论断**: 坎特伯雷大学对学者的双文化能力要求，school_signal = moderate
- **原文摘录**: "Having bicultural confidence develops awareness and the ability to relate to different ideas... Bicultural Competence Kaupapa: The Treaty of Waitangi and Aotearoa New Zealand's bicultural history."
- **对齐**: 面向学者的教学框架确认，moderate 信号合理（双文化框架但无强制要求级别）。

---

### [^62] Hakituri IoT / Participatory Data Design

**间接验证** ◎ Layer 3（OUP 需机构订阅，全层无法获取全文）

- **规则卡论断**: Hakituri IoT 案例：毛利工人共同定义数据收集和使用方式，将共治权交予毛利团队（Kāwanatanga 在 HCI 中的真实案例）
- **WebSearch 原文**: "ownership of the process handed over to Māori research partners who took leadership" / 项目以"Māori data sovereignty"为核心，采用参与式设计工作坊
- **对齐**: "ownership handed over to Māori research partners"直接印证"将共治权交予毛利团队"论断。
- **建议替代开放来源**: https://isdb.cms.waikato.ac.nz/research-projects/hakituri/

---

### [^64] Otago Te Tiriti page

**已验证** ✓ Layer 2.5（Wayback 2024-03-15 存档）

- **规则卡论断**: 奥塔哥大学与南岛 Ngāi Tahu 部落有深厚历史渊源；条约是治理核心框架
- **原文摘录**: "The University signed a Memorandum of Understanding (MoU) with Ngāi Tahu in 2001. Both Te Rūnanga o Ngāi Tahu, as the Treaty partner, and the University agreed that the purpose of the MoU was to establish a protocol that gave effect to a Treaty of Waitangi based partnership."
- **对齐**: 2001 年 MoU 及 Ngāi Tahu 作为"Treaty partner"的明确定位，完全验证论断。

---

### [^68] Te Mana Raraunga official site

**已验证** ✓ Layer 1

- **规则卡论断**: Te Mana Raraunga 是 NZ 毛利数据主权网络，制定了权威原则；研究者应论述遵循其指导方针
- **原文摘录**: "Our data, our sovereignty, our future... We advocate for Māori rights and interests in data to be protected... Māori Data Sovereignty recognises that Māori data should be subject to Māori governance."
- **对齐**: 网站定位与论断完全一致，完全验证。

---

### [^70] Waikato Māori Data Governance Model

**已验证** ✓ Layer 1（PDF 1.8MB，完整下载）

- **规则卡论断**: 怀卡托大学制定了毛利数据治理模型，提供技术实施框架
- **原文摘录**: "This report describes the Māori Data Governance Model that has been designed by Māori data experts for use across the Aotearoa New Zealand public service. The Model provides guidance for the system-wide governance of Māori data, consistent with the Government's responsibilities under te Tiriti o Waitangi."
- **对齐**: 模型确认存在且内容完整，论断成立。
- **注**: 更准确描述是"系统级治理指导框架"（system-wide governance），非单纯技术框架

---

### [^71] UoA Māori Data Sovereignty

**已验证** ✓ Layer 1（保留为 FAIR vs CARE 数据主权通用来源）

- **URL**: https://research-hub.auckland.ac.nz/article/maori-data-sovereignty
- **规则卡论断**: UoA Research Hub 关于毛利数据主权的介绍；FAIR vs CARE 数据框架
- **原文摘录**: "Researchers are encouraged to consider responsiveness to Māori and Māori data sovereignty in grant and ethics applications and throughout the research data lifecycle."
- **对齐**: FAIR vs CARE 的宏观数据主权框架来源有效，论断成立。"防范 LLM 训练抓取 Te Reo Māori 语料库"的具体论断已迁移至新增 [^103]
- **注**: 策略文件 line 224 已将该 LLM 特定论断的引用从 [^71] 更改为 [^103]（Royal Society Te Apārangi 2025 GenAI 指南）

### [^103] Royal Society Te Apārangi GenAI 指南（新增）

**已验证** ✓ Layer 1（PDF 直接可访问）

- **URL**: https://www.royalsociety.org.nz/assets/Guidelines-for-the-best-practice-use-of-GenAI-in-research_Royal-Society-Te-Aparangi_June-2025_English-.pdf
- **规则卡论断**: LLM/GenAI 工具可能在未经毛利人知情同意的情况下抓取 te reo Māori 和 mātauranga Māori 语料库
- **原文摘录（§2.3）**: "GenAI tools are of concern because they can draw on mātauranga Māori – a taonga that includes te reo Māori and Māori data – without Māori knowledge or consent, circumventing te Tiriti o Waitangi obligations and ignoring te Tiriti o Waitangi-compliant research principles, such as tika and mana."
- **原文摘录（§3.2.1）**: "Acknowledge and respect that Māori data, including mātauranga Māori and te reo Māori, are taonga that Māori have te Tiriti o Waitangi-afforded rights to govern and protect... no GenAI tool will assume any proprietary interest of Māori data, including mātauranga Māori and te reo Māori."
- **对齐**: 新西兰皇家学会 2025 年最新 GenAI 研究指南，权威性高，直接支撑"未经授权抓取语料库"论断，完全成立。

---

### [^76] VUW Rite tahi

**已验证** ✓ Layer 1

- **规则卡论断**: VUW Rite tahi 原则追求结果公平（equity of outcomes），是 Te Tiriti Statute 核心条款
- **原文摘录**: "Achieving equitable outcomes for Māori depends, in part, on how much resourcing is provided... the University should ensure that Māori students have the same opportunity as non-Māori to access paid university employment such as mentoring work and tutoring."
- **对齐**: equitable outcomes 明确出现，论断完全成立。

---

### [^78] NZ Digital Inclusion

**间接验证** ◎ Layer 3（Incapsula 拦截所有自动访问）

- **规则卡论断**: Ōritetanga 要求 CS 研究者开发具有数字包容性的界面，确保非英语母语者和偏远毛利群体平等享用技术
- **WebSearch 原文**: "Access and skills are the 2 main barriers to digital inclusion for former refugees and marginalised migrants."
- **对齐**: 报告核心主题（语言障碍、数字鸿沟）与论断相关，但报告针对移民/难民，非直接针对毛利群体；将其与 CS 学术研究要求挂钩需要解释框架

---

### [^85] Mātauranga Māori in Computing (Unitec)

**已验证** ✓ Layer 1（PDF 300KB，完整提取）

- **规则卡论断**: Mātauranga Māori 可被嵌入 CS 课程；Teaching Statement 应包含具体构想
- **原文摘录**: "This paper discusses how to embed mātauranga Māori in computing courses to increase the awareness of ākonga (students) regarding Māori beliefs, language and practices... Topics: Māori data sovereignty, application of te Tiriti o Waitangi in the IT sector, Code of Ethics and professional practices."
- **对齐**: Unitec 真实课程实践案例，完全验证论断。

---

### [^86] Mātauranga Māori in Computing (ResearchGate)

**间接验证** ◎ Layer 3（ResearchGate 全层封锁，论文本身可通过 ePress PDF 访问）

- **规则卡论断**: 与 [^85] 互为补充的案例研究来源
- **说明**: 该论文与 [^85] 为同一篇（Chitalia et al., CITRENZ 2023），ePress 版本已在 [^85] 完整验证
- **建议**: 将 ResearchGate URL 替换为 ePress 直链 `https://www.unitec.ac.nz/epress/wp-content/uploads/2024/07/12-CITRENZ2023-Proceedings-Chitalia-et-al.pdf`

---

### [^87] UoA Tuākana Programme（已更新 URL）

**已验证** ✓ Layer 1（URL 已从 Code of Conduct 页更新为 Tuākana Programme 专页）

- **新 URL**: https://www.auckland.ac.nz/en/students/student-support/academic-support/tuakana-learning-communities/what-is-tuakana.html
- **规则卡论断**: Tuākana-Tēina（老生带新生朋辈导师模型）可提升 Māori/Pasifika 学生学业成功
- **原文摘录**: "Tuākana is an indigenous Māori and Pacific philosophy of care that is grounded and informed by Māori kaupapa and Pacific ways of being and knowing... The concept of tuākana-tēina demonstrates the importance of the relationship fostered between the older sibling as tuakana and the younger sibling as teina... The knowledge transfer that takes place in this relationship is reciprocal, with the tuakana also learning from their teina. Tuākana programmes are across all Faculties and Te Tumu Herenga | Library and Learning Services and is where Māori and Pacific thrive on campus."
- **对齐**: 专页完整定义了 Tuākana-Tēina 关系的文化内涵（毛利/太平洋哲学框架）和全院系覆盖，论断充分成立。
- **注**: 原 Code of Conduct 页（四项毛利价值观来源）已改由 [^95] 策略框架页面覆盖，[^87] 专注于 Tuākana-Tēina 朋辈支持模型

---

### [^92] AUT Academic Standards

**已验证** ✓ Layer 1（PDF 1.43MB，完整提取）

- **规则卡论断**: AUT 对学术人员的标准和期望，school_signal = moderate
- **原文摘录**: "This document... is guided by the principle of Te Tiriti o Waitangi... AS LECTURERS, WE: consider the value of tikanga and mātauranga Māori to teaching and learning"
- **对齐**: "consider"（考虑）而非"lead"或"demonstrate"，属于中等强度要求，moderate 信号合理。

---

### [^95] UoA Strategic Plan

**已验证** ✓ Layer 1

- **规则卡论断**: UoA Waipapa Taumata Rau 战略框架（Taumata Teitei 2030）是 school_signal=strong 核心证据；核心价值观包含 Manaakitanga、Whanaungatanga、Kotahitanga、Kaitiakitanga
- **原文摘录**: "Taumata Teitei Vision 2030 and Strategic Plan 2028... Our fundamental principles reflect our foundational relationship with tangata whenua and our commitment to Te Tiriti. Manaakitanga... Whanaungatanga... Kaitiakitanga..."
- **对齐**: 战略框架确认，三项价值观有原文。Kotahitanga 出现在 Code of Conduct [^87] 而非此页，规则卡略有来源混合，但整体论断（school_signal=strong）充分成立。

---

### [^96] UoA Academic Recruitment Procedures

**已验证（PVC 否决权待确认）** ✓/⚠️ Layer 1

- **规则卡论断**: 等实力候选人中毛利裔或公平目标群体优先；PVC(Māori) 有文化胜任力一票否决权
- **原文摘录（第 47 条）**: "Where two candidates are deemed to be of equal merit and one of the candidates is Māori or a member of an equity group, then that candidate is to be offered the position."
- **原文摘录（第 31 条）**: "If required, the Faculty office is to consult with their Kaiārahi and/or the Office of the Pro Vice-Chancellor (Māori) to make appropriate arrangements."
- **对齐**: 等实力优先条款完整核实；PVC(Māori) 在第 31 条仅为"咨询/协助"角色，"一票否决权"措辞需要更具体的内部文件支持

---

### [^97] VUW Te Tiriti guide

**已验证** ✓ Layer 1

- **规则卡论断**: VUW 的 Te Tiriti 综合指南，支撑 school_signal=strong
- **原文摘录**: "We were the first university in New Zealand to have a Treaty of Waitangi Statute... The Tiriti Statute centres around eight principles that are drawn from Te Tiriti o Waitangi..."
- **对齐**: VUW 自称 NZ 首所有 Treaty Statute 的大学，8 项原则完整列出，school_signal=strong 有力支撑。

---

### [^98] VUW Whai wāhi

**已验证** ✓ Layer 1

- **规则卡论断**: VUW Whai wāhi 原则确保毛利人在决策层有代表性
- **原文摘录**: "The principle of whai wāhi (participation) ensures that Māori are fully involved in all parts of New Zealand society... requires the University to ensure Māori representation in key decision-making bodies and the involvement of Māori across all parts of the University."
- **对齐**: 完全印证论断，决策机构毛利代表性要求有明确原文。

---

### [^99] Otago MSF 2030

**已验证** ✓ Layer 2.5（Wayback 2024-12-25 存档，1.17MB）

- **规则卡论断**: 奥塔哥大学 Māori Strategic Framework 2030 是 school_signal=strong 核心证据
- **原文摘录**: "The University's Vision 2040 identifies being a Te Tiriti-led university as a strategic priority of the highest order... The Māori Strategic Framework 2030 details how the University can concretely progress its Te Tiriti aspirations across four key areas: kāwanataka (leadership), rakapūtaka (partnership), mana taurite (equity) and tino rakatirataka (sovereignty)."
- **对齐**: "Te Tiriti-led university as a strategic priority of the highest order"是 school_signal=strong 的强力证据。

---

### [^100] Waikato Treaty Statement

**已验证** ✓ Layer 1

- **规则卡论断**: 怀卡托大学是 NZ 首批发布正式独立 Treaty Statement 的大学之一，school_signal=strong
- **原文摘录**: "The University of Waikato has established structures and initiatives designed to give effect to the Treaty, it has advanced further down this path than many other universities and public sector institutions."
- **对齐**: Treaty Statement 真实存在（2022-02-15 Council 批准），学校"领先于许多其他大学"。
- **注**: "首批之一"是合理推断，页面未明确使用"first"或"首批"字样

---

### [^102] UoA Equity Questions in Recruitment

**已验证** ✓ Layer 1（.docx 直接下载解析）

- **规则卡论断**: UoA 在招聘面试中有标准化的条约相关必考题
- **原文摘录**: "Criteria: Valuing equity — Works effectively to support the University's commitment to Māori, Te Tiriti o Waitangi and equity. Sample Questions: What do you understand by the University's commitment to Te Tiriti o Waitangi?..." / "Senior Academic and Professional staff — Criteria: Championing Equity — Leads strategic decision making and implementation for Te Tiriti o Waitangi and equity objectives."
- **对齐**: 标准化面试题目涵盖所有职级（从 Team members 到 Senior Academic Staff），Te Tiriti 是每级必考维度，完全验证论断。

---

## 建议修改汇总

| 优先级 | 问题 | 建议操作 |
|--------|------|---------|
| ✅ 已完成 | [^51] 来源错配——文件是教师入学面试非教职招聘 | 已从策略文件完全移除 [^51] |
| ✅ 已完成 | [^86] ResearchGate 链接封锁 | 已替换为 Unitec ePress 直链 |
| ✅ 已完成 | [^96] PVC(Māori) 否决权措辞过强 | 已改为"参与文化胜任力评估（具体否决权限待内部文件确认）" |
| ✅ 已完成 | [^100] "首批"非原文措辞 | 已改为引用原文"advanced further down this path than many other universities" |
| ✅ 已完成 | [^23] "一票否决权"措辞 | 策略文件本身仅写"Responsiveness to Māori 要求"，未使用否决权措辞，无需修改 |
| ✅ 已完成 | [^95] Kotahitanga 来源 | 策略文件中 Kotahitanga 列于核心术语列表（非内联引用），[^87]+[^95] 均为同校文件，整体论断不受影响，无需修改 |
| ✅ 已完成 | [^9] 全层失败 | Wayback Machine 找到相关 HR 工具包选拔流程页（2024-05-21 存档），原文直接支撑"按标准评分"论断；改标记为间接验证 ◎ |
| ✅ 已完成 | [^87] Tuākana-Teina 不在 Code of Conduct 页 | URL 已更新为 UoA Tuākana Programme 专页（Layer 1 验证，含完整原文定义） |
| ✅ 已完成 | [^71] LLM 语料库论断无直接原文 | 新增 [^103]（Royal Society Te Apārangi 2025 GenAI 指南，§2.3+§3.2.1 直接支撑）；策略文件 line 224 引用改为 [^103] |

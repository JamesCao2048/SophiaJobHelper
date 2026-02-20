# 新西兰 Te Tiriti 策略系统设计文档

- **日期**: 2026-02-20
- **状态**: 设计完成，待实现
- **关联文件**:
  - 原始策略研究: `general/research_job_rules/新西兰教职申请：Te Tiriti 策略.md`
  - 参考范式: `overseas_pipeline/strategies/hci_density_strategy.md`
  - 现有地区卡: `region_knowledge/regions/new_zealand.md`
  - Sophia 材料: `overseas_pipeline/materials/`
- **产出物**:
  - `overseas_pipeline/strategies/nz_te_tiriti_strategy.md`（新增）
  - `overseas_pipeline/workflows/step1_research.md`（修改）
  - `overseas_pipeline/workflows/step2_analysis.md`（修改）
  - `region_knowledge/regions/new_zealand.md`（修改）
  - 学校卡模板更新

---

## 一、目标与作用域

### 要解决的问题

新西兰教职申请中，《怀唐伊条约》(Te Tiriti o Waitangi) 理解是从"加分项"到"否决项"的硬性门槛。当前 pipeline 仅在 `new_zealand.md` 地区卡中有基础的优先级判断（高/中），缺乏：

1. JD 中条约信号的系统化检测
2. 学校层面条约承诺深度的评估
3. 两维信号交叉产出的分级策略
4. 基于 Sophia 真实背景的修辞校准
5. 同校跨院系的学校信号复用机制

### 作用域

- **聚焦新西兰**：文件命名和内容专注 NZ Te Tiriti
- **设计模式可迁移**：二维矩阵（JD signal × Institution signal → strategy label）的架构模式可未来独立应用于：
  - 加拿大 Indigenous reconciliation / EDI 策略
  - 澳洲 Aboriginal & Torres Strait Islander acknowledgement 策略
  - 但不做提前抽象，各地区独立建策略文件

### 不做的事

- 不写 Python 自动化脚本（与 HCI density 不同，学校战略文件结构差异大，agent 判断比硬编码规则更可靠）
- 不修改 Step 3 workflow 结构（Te Tiriti 修辞建议通过 fit_report 自然流入 Step 3）

---

## 二、架构总览

### 新增/修改文件

```
overseas_pipeline/strategies/
├── hci_density_strategy.md          # 已有，不变
└── nz_te_tiriti_strategy.md         # 【新增】矩阵 + 策略标签 + 修辞指南

overseas_pipeline/workflows/
├── step1_research.md                # 【修改】增加 Step 10.5 (NZ Te Tiriti 信号采集)
└── step2_analysis.md                # 【修改】增加 Te Tiriti 矩阵交叉分析

region_knowledge/regions/
└── new_zealand.md                   # 【修改】§3.4 精简，指向策略文件

region_knowledge/schools/{school_id}/
└── {dept_id}.md                     # 【修改模板】新增 te_tiriti 字段块
```

### 数据流

```
Step 1:
  JD 原文 ──关键词扫描──→ jd_signal: no_mention | boilerplate | explicit
                          （附：原文摘录 + 所在板块位置）

  学校战略页 ──agent 评估──→ school_signal: light | moderate | strong
                              （附：原文摘录 + 来源 URL + 文档名）
  ↓
  写入 faculty_data.json → te_tiriti 块
  写入学校卡 → te_tiriti_school_signal（跨院系复用）

Step 2:
  读取 te_tiriti 块 + nz_te_tiriti_strategy.md + Sophia materials
  → 矩阵查表 → strategy_label
  → 写入 fit_report → per-document 修辞建议（标注 Claim vs Aspire）

Step 3:
  读取 fit_report 中的 Te Tiriti 修辞建议
  → 按策略指南生成各文档中的相应段落
  → Humanizer pass 增加校验项："Te Tiriti 段落是否超出 Sophia 真实经历？"
```

---

## 三、二维矩阵与策略标签

### 3.1 JD 信号等级定义

| level | 判定条件 | 典型表现 |
|-------|---------|---------|
| `no_mention` | JD 实质性评估板块无任何条约相关词汇，仅有页脚 EEO 样板 | "The University is an equal opportunity employer" |
| `boilerplate` | 出现关键词但位于通用要求/nice-to-have 区域，非核心考核项 | "An appreciation of bicultural values" 在 Desirable Attributes 末尾 |
| `explicit` | 关键词出现在 Key Responsibilities / Essential Criteria / Skills and Attributes 等硬性考核板块 | "Demonstrated understanding of Te Tiriti o Waitangi and its application to tertiary education" 在 Essential Skills |

**扫描关键词清单：**

核心词（高权重）：Te Tiriti, Treaty of Waitangi, Māori, Pasifika, Bicultural competence, Tangata Whenua, Mātauranga Māori, Tikanga, Kaupapa Māori

辅助词（低权重，需结合上下文）：Te Reo, iwi, hapū, whānau, data sovereignty, indigenous, kaitiakitanga, whanaungatanga, manaakitanga

**位置权重规则：**
- Essential Criteria / Key Responsibilities / Selection Criteria 中出现 → explicit
- Desirable / Nice-to-have / About the University 中出现 → boilerplate
- 仅在 EEO 声明 / 页脚 / 学校简介样板中出现 → no_mention

来源: 原策略文档 §43-73 [^8][^9][^21]

### 3.2 学校信号等级定义

| level | 判定条件 | 典型表现 |
|-------|---------|---------|
| `light` | 学校网站仅有标准条约致敬声明（acknowledgement），无专门战略文件或框架 | 页脚 "We acknowledge the Treaty of Waitangi" |
| `moderate` | 有正式条约政策或战略文件，但未深入到院系层面的具体实施框架，无专有术语体系 | Massey 的 Tiriti o Waitangi Policy [^54] |
| `strong` | 有深度条约战略框架 + 院系级实施机制 + 校级专有毛利价值观术语命名 | Auckland 的 Waipapa Taumata Rau + Taumata Teitei [^87][^95]；VUW 的 Te Tiriti Statute + Rite tahi/Whai wāhi [^4][^76]；Waikato 的 Treaty Statement + Mana Māori Motuhake [^56] |

**评估信号来源（优先级从高到低）：**
1. 学校官方 Treaty Statement / Te Tiriti Policy
2. 学校战略规划文件（如 Strategic Plan 2030）
3. Māori Strategic Framework（如有）
4. 招聘政策/流程中的条约相关条款
5. Pro-Vice-Chancellor (Māori) 的存在与职权范围

### 3.3 策略矩阵

| JD signal \ School signal | `light` | `moderate` | `strong` |
|---------------------------|---------|-----------|----------|
| `no_mention` | **`skip`** | **`subtle`** | **`moderate`** |
| `boilerplate` | **`subtle`** | **`moderate`** | **`strong`** |
| `explicit` | **`moderate`** | **`strong`** | **`full_treaty`** |

---

## 四、策略标签修辞指南

### 通用禁忌（所有级别）

以下错误在任何级别都会导致负面评价，级别越高后果越严重：

1. **把它写成美式 Diversity Statement** [^13][^25]：只谈"包容少数族裔"、"intersectionality"、"underrepresented minorities" → 在 NZ 语境下暴露完全不了解该国宪政框架
2. **把毛利人归为"少数族裔"之一** [^23]：毛利人是条约缔约方，拥有独特宪法地位，不是 minority
3. **泛泛说"我尊重多元文化"** [^16]：暴露未做功课，缺乏具体性
4. **不懂装懂** [^27]：伪装成已有毛利社区合作经验 → 面试时会被识破

### Sophia 背景校准：Claim vs Aspire

基于 Sophia 的真实研究经历（`materials/Research_Statement.md`, `materials/Teaching_Statement.md`）：

| 条款 | **Claim**（有经历支撑，可具体论述） | **Aspire**（无经历，只能表达学习意愿和未来计划） |
|------|-------------------------------------|------------------------------------------------|
| **Kāwanatanga** (伙伴关系) | 参与式设计方法论（user studies, interviews, co-design with domain experts）；跨学科跨文化协作经历（JHU, SMART/Singapore, NUS, Notre Dame）；开源平台建设（MindCoder.ai, CollabCoder）体现的共享精神 | 与 iwi/hapū 建立研究共治关系；Kaupapa Māori 研究框架的应用 |
| **Tino Rangatiratanga** (数据主权) | 对 trustworthy AI 的核心研究关注；人类对 AI 过程的控制权是核心研究主张（"keep humans at the center"）；MindCoder.ai 的人类中心设计保障用户对数据分析过程的掌控 | Māori Data Sovereignty 的具体技术实践；CARE 原则实施；数据本地化存储架构设计 |
| **Ōritetanga** (公平) | Human-AI 协作中对人类 agency 和信任的系统性研究；对纯 AI 自动化风险的批判性学术立场（"AI often fails to capture the depth and nuance"）；指导多元背景学生的经验 | 针对毛利群体的算法审计；NZ 特定数字包容性设计 |

**修辞天花板规则（Step 3 Humanizer 强制检查项）：**

1. **Claim 部分用具体经历支撑，Aspire 部分用"学习意愿 + 具体计划"框架**
   - ✅ "My participatory design methodology, demonstrated in [具体项目], provides a methodological foundation I am eager to adapt within a Kaupapa Māori framework upon joining [University]."
   - ❌ "I have extensive experience working with indigenous communities on data sovereignty."

2. **引用 NZ 本土概念时，用"已了解 + 希望深入"的框架**
   - ✅ "I have studied Te Mana Raraunga's principles and see clear alignment with my commitment to human control over AI processes. I look forward to engaging with [University]'s [专有框架] to deepen this understanding."
   - ❌ "My work directly implements Māori Data Sovereignty principles."

3. **可以画平行线但必须立刻收回** [^27]：新加坡的跨文化协作经验可作"适应力"证据，但必须强调 Te Tiriti 赋予毛利人的宪法伙伴地位是独一无二的，不可简单类比。

4. **技术落地点要诚实**：MindCoder.ai 和 CollabCoder 的人类控制权设计是 Tino Rangatiratanga 最真实的连接点（人类对 AI 过程的控制权 ≈ 数据主权中的自治精神），但不要夸大成"这就是 Data Sovereignty 实践"。

---

### `skip`（JD=no_mention, School=light）

**场景：** JD 不提条约，学校本身条约承诺也浅。强行插入会喧宾夺主、挤占展示科研教学实力的空间。

| 文档 | 策略 |
|------|------|
| Cover Letter | 不加任何条约内容 |
| Research Statement | 无特殊调整 |
| Teaching Statement | 无特殊调整 |

**fit_report 中仍需展示：** JD 证据 + 学校证据 + "建议 skip" 的判断依据，让用户知情并可自行覆盖。

来源: 原策略文档 §63-73 [^49]

---

### `subtle`（JD=no_mention+School=moderate, 或 JD=boilerplate+School=light）

**场景：** 信号微弱但不为零。展示"做过功课 + 有学习意愿"即可。

| 文档 | 策略 |
|------|------|
| Cover Letter | 末尾或学术价值观段落中嵌入 1-2 句。核心：学习意愿 + 文化敏感度 |
| Research Statement | 不做专门调整 |
| Teaching Statement | 如篇幅允许，末尾加半句对 Māori/Pasifika 学生的关注 |

**Cover Letter 范式（Sophia 适用）：**

> "As an international scholar committed to inclusive research practice, I am strongly motivated to engage with the bicultural environment of Aotearoa New Zealand. I look forward to participating in professional development on Te Tiriti o Waitangi to ensure my teaching and research respectfully support the success of Māori and Pasifika students."

来源: 原策略文档 §63-73, §119-131 [^21][^49][^51]

---

### `moderate`（矩阵中间三格）

**场景：** 有一定信号但不构成核心考核项。需要展示理解但不必逐条款展开。

| 文档 | 策略 |
|------|------|
| Cover Letter | 一段（约 100-150 词），概括性提及条约精神与自身研究/教学的关联 |
| Research Statement | 嵌入一句 Data Sovereignty 意识（如 FAIR 与 CARE 原则的平衡），不单独成节 |
| Teaching Statement | 一句对 Māori/Pasifika 学生学业成功的承诺，可提 culturally responsive pedagogy |

**Cover Letter 范式（Sophia 适用）：**

> "My research vision aligns with the principles of Te Tiriti o Waitangi. My work on human–AI collaboration is grounded in participatory methods that prioritise human agency and control — values that resonate with the Treaty's emphasis on partnership and self-determination. I am committed to ensuring that AI systems I develop contribute to equitable outcomes, and I look forward to deepening my understanding of how these principles apply within Aotearoa's unique bicultural context."

**Research Statement 嵌入句范式：**

> "In pursuing open and trustworthy AI research, I am mindful of emerging frameworks such as the CARE Principles for Indigenous Data Governance, which complement FAIR principles by centring collective benefit, authority to control, responsibility, and ethics."

**如果 school_signal=strong：** 引用该校专有框架名称（如 "aligning with [University]'s [框架名] commitment to..."）。

来源: 原策略文档 §63-73, §96-110 [^37][^49]

---

### `strong`（JD=boilerplate+School=strong, 或 JD=explicit+School=moderate）

**场景：** 条约能力是实质考核维度。需要结构化回应。

| 文档 | 策略 |
|------|------|
| Cover Letter | 专门段落（200-250 词），三条款结构化回应 |
| Research Statement | 单独小节 "Responsible AI & Data Sovereignty"（150-200 词） |
| Teaching Statement | Māori/Pasifika 支持段（100-150 词） |

**Cover Letter 三条款回应框架（Sophia 适用，Claim + Aspire 混合）：**

> **Kāwanatanga (Partnership):** "My research methodology centres on participatory design, where domain experts are active collaborators rather than passive subjects. At JHU and SMART, I have co-designed AI systems with healthcare professionals and educators, building trust through shared ownership of the research process. I see this approach as a foundation I am eager to adapt within Kaupapa Māori research frameworks, learning to build authentic partnerships with Māori communities as I develop my understanding of local tikanga." [Claim: 参与式设计经历; Aspire: Kaupapa Māori 适配]
>
> **Tino Rangatiratanga (Self-determination):** "A core conviction of my work is that humans must retain meaningful control over AI-driven analysis — reflected in my platforms MindCoder.ai and CollabCoder, which keep users in command of every analytical decision. This commitment to human agency aligns with the spirit of Māori Data Sovereignty, and I am keen to engage with Te Mana Raraunga's principles to ensure my future research in Aotearoa respects indigenous data governance." [Claim: 人类控制权研究; Aspire: MDSov 具体实践]
>
> **Ōritetanga (Equity):** "My research critically examines the risks of unchecked AI automation, demonstrating that purely automated analysis can miss nuance and perpetuate existing biases. As a faculty member, I am committed to extending this critical lens to ensure AI tools do not exacerbate inequities for Māori and Pasifika communities, and to designing inclusive systems accessible across diverse user groups." [Claim: AI 风险批判研究; Aspire: NZ 特定公平性]

**Research Statement 小节范式：**

> "**Responsible AI & Data Sovereignty.** As AI systems increasingly process sensitive human data, questions of who controls data collection, analysis, and application become paramount. My human-centred approach — ensuring transparency, user control, and rigorous validation — provides a natural foundation for engaging with Indigenous data governance frameworks. In the Aotearoa New Zealand context, I am particularly drawn to the principles articulated by Te Mana Raraunga, which position data as a taonga (treasure) subject to Māori governance. I look forward to exploring how my human–AI collaboration architectures can be designed to honour these principles, balancing open-science mandates (FAIR) with indigenous data ethics (CARE)."

**Teaching Statement Māori/Pasifika 段范式：**

> "I am committed to supporting the academic success of Māori and Pasifika students. Drawing on my experience mentoring students from diverse cultural backgrounds across Singapore, the US, and Hong Kong, I recognise that effective teaching requires adapting to students' cultural contexts. I look forward to learning about pedagogical approaches such as Tuākana-Teina (senior-junior mentoring) and to fostering collaborative learning communities where all students can thrive."

**如果 school_signal=strong：** 必须引用该校专有框架术语。

来源: 原策略文档 §49-62, §76-110, §152-176 [^12][^37][^43][^58][^87]

---

### `full_treaty`（JD=explicit, School=strong）

**场景：** 最高规格。条约能力是硬性门槛，学校有深度框架。材料必须展现专业深度，同时保持诚实。

| 文档 | 策略 |
|------|------|
| Cover Letter | 三条款深度回应 + 引用该校专有框架/术语 + 考虑 PVC(Māori) 受众 |
| Research Statement | 专门一节 "Indigenizing Computing / Responsible AI in Aotearoa"（300-400 词） |
| Teaching Statement | Māori/Pasifika 支持段 + Mātauranga Māori integration 构想 |

**在 `strong` 基础上的升级点：**

**Cover Letter:**
- 三条款回应中加深技术细节（不只是"我会做"，而是"具体如何做"）
- 引用该校专有框架 + 校级毛利价值观术语
- 如该校有 Pro-Vice-Chancellor (Māori) 参与审查 [^96]，措辞需额外考虑此受众的专业敏感度

**Research Statement 升级为完整小节：**

在 `strong` 的基础上增加：
- 引用 NZ 本土 CS 研究案例作为未来合作方向（如 Hakituri IoT 项目 [^62]、Mātauranga Māori in Computing [^85][^86]）—— 注意是"受启发"而非"已参与"
- 经费叙事指向 Marsden Fund / MBIE 中的 Responsiveness to Māori 要求 [^23]
- 提及 FAIR vs CARE 平衡的具体技术实施设想（如中介访问机制、训练语料审计）[^37][^71]

**Teaching Statement 升级：**

在 `strong` 的基础上增加 Mātauranga Māori Integration 构想（注意用 Aspire 框架）：
- Kaitiakitanga（守护责任）融入数据伦理/网络安全教学的设想 [^35]
- Whakapapa（宗谱/关系网络）启发关系型数据库教学的构想 [^35]
- Whanaungatanga（建立关系/归属感）学习社群 [^87]

**Sophia 诚实度校准（full_treaty 特别重要）：**

此级别要求深度，但 Sophia 没有 NZ 经验。处理方式：
1. **方法论桥接**：用 Sophia 已有的参与式设计、人类中心 AI 方法论作为"可迁移的方法论基础"
2. **学习路径具体化**：不只说"我愿意学习"，而是"入职后我计划参加 [University] 的 [具体培训项目]，并在第一年寻求与 [学校 Māori 研究中心] 的合作机会"
3. **平行经验谨慎使用** [^27]：新加坡跨文化经验可以简短提及适应力，但必须立刻声明"我深刻理解 Te Tiriti 赋予毛利人的宪法伙伴地位是独一无二的，不可与其他多元文化经验简单类比"

来源: 原策略文档 §49-62, §76-110, §112-176, §207-237 [^4][^8][^27][^35][^56][^87][^95][^96]

---

## 五、数据结构

### 5.1 faculty_data.json 中的 `te_tiriti` 块

```json
{
  "te_tiriti": {
    "jd_signal": {
      "level": "explicit | boilerplate | no_mention",
      "evidence": [
        {
          "text": "原文摘录（英文原文）",
          "location": "所在板块/bullet 编号，如 'Key Responsibilities, bullet 7'",
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
          "document_name": "文档名称，如 'Taumata Teitei 2030 Strategic Plan'"
        }
      ],
      "key_framework_name": "该校专有框架名称（如有）",
      "key_values": ["该校专有毛利价值观术语列表（如有）"]
    },
    "strategy": "skip | subtle | moderate | strong | full_treaty",
    "strategy_rationale": "Step 2 填充：矩阵结果 + agent 对上下文的补充判断"
  }
}
```

**证据要求：**
- `jd_signal.evidence`：至少 1 条（`no_mention` 时记录"未发现相关关键词"即可）
- `school_signal.evidence`：至少 2 条（`light` 时可为"仅发现页脚 acknowledgement"）
- 所有 evidence 必须包含原文英文文本，不翻译

### 5.2 学校卡中的 Te Tiriti 字段块

```markdown
## Te Tiriti 学校信号

- **signal_level**: strong | moderate | light
- **assessed_date**: YYYY-MM-DD
- **key_framework**: 框架名称（如 Waipapa Taumata Rau）
- **key_values**: 术语1, 术语2, ...（如 Manaakitanga, Whanaungatanga）
- **evidence**:
  1. "原文摘录..."
     - source: [文档名](URL)
  2. "原文摘录..."
     - source: [文档名](URL)
- **notes**: 其他备注（如 PVC(Māori) 审查权限等）
```

**跨院系复用规则：**
- 同校新院系 Step 1 时，检测到学校卡已有此字段 → 直接读取复用，跳过学校战略页爬取
- 仅需对新院系做 JD 信号检测

### 5.3 fit_report 中的 Te Tiriti 专节

```markdown
### Te Tiriti 评估

**JD 信号: [level]**
> "[原文摘录]" ([位置])
> "[原文摘录]" ([位置])

**学校信号: [level]** (来源: 学校卡, assessed [date])
> "[原文摘录]" ([文档名](URL))
> "[原文摘录]" ([文档名](URL))
> 专有框架: [名称] | 核心术语: [术语列表]

**矩阵结果: [strategy_label]**

**Per-document 建议:**
- **Cover Letter**: [具体建议，标注 Claim vs Aspire 段落]
- **Research Statement**: [具体建议]
- **Teaching Statement**: [具体建议]
- **该校术语提醒**: 如需引用 [术语]，参考 [URL]
```

---

## 六、Pipeline Workflow 修改

### 6.1 Step 1 新增：Step 10.5 Te Tiriti Signal Assessment

在现有 Step 10（HCI density + course catalog）之后，仅当 `region=new_zealand` 时触发：

```
Step 10.5: Te Tiriti Signal Assessment (NZ only)

A. JD 信号检测
   1. 读取已爬取的 raw/jd_*.md
   2. 扫描关键词清单（见策略文件 §3.1 关键词清单）
   3. 记录每个命中：原文文本 + 所在位置（哪个板块/bullet）
   4. 根据位置权重规则判定 jd_signal level
   5. 写入 faculty_data.json → te_tiriti.jd_signal（含 evidence 数组）

B. 学校信号检测
   1. 检查同校学校卡是否已有 te_tiriti_school_signal
      - 如有且 assessed_date 在 6 个月内 → 直接读取复用，跳到 C
      - 如无或已过期 → 继续
   2. 查策略文件种子表（§八），获取该校已知条约页面 URL
   3. 爬取种子 URL（五层 fallback）
   4. 如种子不足或种子全部失败，搜索补充：
      - "{school_name} Te Tiriti strategy"
      - "{school_name} Māori strategic framework"
      - "{school_name} Treaty of Waitangi policy"
   5. Agent 基于爬取内容评定 school_signal level
   6. 摘录原文证据（至少 2 条），记录来源 URL 和文档名
   7. 识别该校专有框架名称和核心价值观术语
   8. 写入学校卡 → Te Tiriti 学校信号
      （双写：region_knowledge/schools/ + output/knowledge/）
   9. 写入 faculty_data.json → te_tiriti.school_signal

C. 预判策略标签
   1. 查矩阵表 → 初步 strategy label
   2. 写入 faculty_data.json → te_tiriti.strategy
   3. 留空 strategy_rationale（Step 2 填充）

D. Step 1 Summary 中新增 Te Tiriti 行
   - "Te Tiriti: JD=[level], School=[level] → [strategy_label]（初步）"
```

### 6.2 Step 2 修改：Te Tiriti 矩阵交叉分析

在 fit_report 生成流程中增加（NZ only）：

```
Te Tiriti Analysis:

1. 读取 faculty_data.json → te_tiriti 块
2. 读取 strategies/nz_te_tiriti_strategy.md
3. 读取 Sophia 的 materials/Research_Statement.md 和
   Teaching_Statement.md（识别可 Claim 的经历锚点）
4. 确认/调整策略标签
   - Agent 可根据上下文微调，需记录理由
   - 典型上调场景：JD 虽是 boilerplate 但已知该校面试必考条约题
   - 典型下调场景：school_signal=strong 但该院系明确技术导向
5. 填充 strategy_rationale
6. 在 fit_report 中生成 Te Tiriti 专节（格式见 §5.3）
7. 标注 Sophia 可 Claim 的经历点 + 需要 Aspire 的部分
```

### 6.3 Step 3 修改

无结构性修改。新增一条 Humanizer 强制检查项：

```
Humanizer Checklist 新增:
□ Te Tiriti 相关段落是否超出 Sophia 真实经历？
  - 检查是否有伪装已有毛利社区合作经验的表述
  - 检查是否有把跨文化经验直接等同于 Te Tiriti 理解的表述
  - 检查 Aspire 部分是否有具体的学习计划而非空洞承诺
```

---

## 七、new_zealand.md 地区卡修改

### 修改内容

**§3.4 "特色材料" 中的 Bicultural Statement 部分**精简为：

```markdown
#### Bicultural Statement / Te Tiriti Commitment Statement
- **状态**: 取决于 JD 信号强度和学校信号强度的矩阵交叉结果
- **详细策略**: 见 `overseas_pipeline/strategies/nz_te_tiriti_strategy.md`
- **核心原则**: 不能写成美式 Diversity Statement；必须基于条约框架而非多元文化框架
- **Pipeline 行为**: Step 1 自动检测 JD/学校信号，Step 2 产出策略标签和 per-document 建议
```

**保留 §3.4 中的优先级判断规则要点**（作为快速参考），但标注"详见策略文件"以避免重复维护。

---

## 八、学校种子表

从原策略文档（`general/research_job_rules/新西兰教职申请：Te Tiriti 策略.md`）的引用索引提取。Step 1 agent 先按 school_id 匹配种子表爬取，无种子或种子不足时搜索补充。

### 奥克兰大学 (University of Auckland / Waipapa Taumata Rau)

- **预判 school_signal**: strong
- **框架名**: Waipapa Taumata Rau + Taumata Teitei 2030
- **核心术语**: Manaakitanga, Whanaungatanga, Kotahitanga, Kaitiakitanga
- **种子 URL**:
  - [^95] Strategic Plan: Purpose, Vision, Principles, Values — https://www.auckland.ac.nz/en/about-us/about-the-university/the-university/official-publications/strategic-plan/purpose-vision-principles-values.html
  - [^87] Code of Conduct — https://www.auckland.ac.nz/en/on-campus/life-on-campus/code-of-conduct.html
  - [^96] Academic Staff Recruitment Procedures — https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/academic-staff-recruitment-procedures.html
  - [^39] Recruitment, Selection and Appointment Policy — https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/recruitment-selection-appointment-policy.html
  - [^25] Equity information for staff — https://www.auckland.ac.nz/en/about-us/about-the-university/equity-at-the-university/equity-information-for-staff.html
  - [^102] Equity Questions in Recruitment — https://www.auckland.ac.nz/assets/about-us/about-the-university/equity-at-the-university/equity-information-staff/Appendix%202%20Equity%20Questions%20in%20Recruitment%20and%20Selection.docx
- **特殊备注**: PVC(Māori) 对高级职位有文化胜任力一票否决权；遴选末期同等实力候选人中，毛利裔或公平目标群体身份候选人优先录用 [^96]
- **原策略文档位置**: §182-184

### 惠灵顿维多利亚大学 (Victoria University of Wellington / Te Herenga Waka)

- **预判 school_signal**: strong
- **框架名**: Te Tiriti o Waitangi Statute
- **核心术语**: Rite tahi (结果公平), Whai wāhi (决策层代表性)
- **种子 URL**:
  - [^4] Te Tiriti o Waitangi Statute PDF — https://www.wgtn.ac.nz/documents/policy/governance/te-tiriti-o-waitangi-statute.pdf
  - [^76] Principle of Rite tahi — https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-rite-tahi
  - [^98] Principle of Whai wāhi — https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-whai-wahi
  - [^97] Te Tiriti o Waitangi guide — https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi
- **特殊备注**: 校董会正式通过具有法律效力的 Te Tiriti Statute，是 NZ 大学中制度化程度最高的
- **原策略文档位置**: §186-192

### 奥塔哥大学 (University of Otago / Ōtākou Whakaihu Waka)

- **预判 school_signal**: strong
- **框架名**: Māori Strategic Framework 2030
- **核心术语**: Kāwanataka (领导力), Tauira Māori (毛利学生)
- **种子 URL**:
  - [^99] Māori Strategic Framework 2030 — https://www.otago.ac.nz/maori/maori-strategic-framework
  - [^47] Humanities Māori Strategic Framework — https://www.otago.ac.nz/humanities/maori-at-humanities/strategic-framework
  - [^64] Te Tiriti o Waitangi page — https://www.otago.ac.nz/maori/world/treaty
  - [^9] Academic Staff Recruitment Process Guidelines — https://www.otago.ac.nz/administration/policies/academic-staff-recruitment-process-guidelines
  - [^46] Legislative framework, Human Resources — https://www.otago.ac.nz/humanresources/toolkit/recruiting/legislative-framework
- **特殊备注**: 与南岛 Ngāi Tahu 部落有深厚历史渊源；强调学生能"以毛利人的身份生活和学习"
- **原策略文档位置**: §194-199

### 怀卡托大学 (University of Waikato / Te Whare Wānanga o Waikato)

- **预判 school_signal**: strong
- **框架名**: Treaty Statement
- **核心术语**: Mana Māori Motuhake (原住民固有权利), Mana Mātauranga Māori (毛利知识权威性)
- **种子 URL**:
  - [^100] University of Waikato Treaty Statement — https://www.waikato.ac.nz/about/governance/docs/university-of-waikato-treaty-statement/
  - [^56] Critical Tiriti Analysis (学术分析) — https://www.journalofglobalindigeneity.com/article/92446-a-critical-tiriti-analysis-of-the-treaty-statement-from-a-university-in-aotearoa-new-zealand
  - [^70] Māori Data Governance Model — https://www.waikato.ac.nz/assets/Uploads/Research/Research-institutes-centres-and-groups/Institutes/Te-Ngira-Institute-for-Population-Research/Maori_Data_Governance_Model.pdf
- **特殊备注**: NZ 首批发布正式独立 Treaty Statement 的大学之一；本土化进程走在全国前列
- **原策略文档位置**: §201-205

### 坎特伯雷大学 (University of Canterbury / UC)

- **预判 school_signal**: moderate
- **框架名**: Bicultural Competence & Confidence
- **核心术语**: Bicultural confidence
- **种子 URL**:
  - [^17] Bicultural confidence — Employers — https://www.canterbury.ac.nz/study/study-support-info/study-related-topics/graduate-profile/employers/bicultural-confidence---competence
  - [^61] Bicultural confidence — Academics — https://www.canterbury.ac.nz/study/study-support-info/study-related-topics/graduate-profile/academics/bicultural-confidence---competence
- **原策略文档位置**: 无专门段落，种子来自引用索引

### 梅西大学 (Massey University)

- **预判 school_signal**: moderate
- **框架名**: Tiriti o Waitangi Policy
- **种子 URL**:
  - [^54] Tiriti o Waitangi Policy PDF — https://www.massey.ac.nz/documents/1796/Treaty_of_Waitangi_Te_Tiriti_o_Waitangi_Policy.pdf
  - [^55] Te Tiriti meets HOP article — https://www.massey.ac.nz/about/news/te-tiriti-o-waitangi-principles-meets-human-and-organisational-performance/
- **原策略文档位置**: 无专门段落

### 奥克兰理工大学 (AUT)

- **预判 school_signal**: moderate（待验证）
- **种子 URL**:
  - [^92] Academic Standards and Expectations PDF — https://www.aut.ac.nz/__data/assets/pdf_file/0010/288955/Academic-Standards-and-Expectations.pdf
- **原策略文档位置**: 无专门段落，种子有限，需搜索补充

### 林肯大学 (Lincoln University)

- **预判 school_signal**: 未知
- **种子 URL**: 无
- **备注**: 原策略文档未覆盖，Step 1 需完全依赖搜索

---

## 九、引用索引

本设计文档的引用标号对应原策略文档 `general/research_job_rules/新西兰教职申请：Te Tiriti 策略.md` 的引用索引。以下为本文件中引用的关键来源：

| 引用 | 来源简称 | URL | 用途 |
|------|---------|-----|------|
| [^4] | VUW Te Tiriti Statute | https://www.wgtn.ac.nz/documents/policy/governance/te-tiriti-o-waitangi-statute.pdf | 学校信号判定 |
| [^8] | Reddit: NZ Faculty Advice | https://www.reddit.com/r/AskAcademia/comments/1r0afcw/ | JD 解读策略 |
| [^9] | Otago Recruitment Guidelines | https://www.otago.ac.nz/administration/policies/academic-staff-recruitment-process-guidelines | 招聘流程 |
| [^10] | Mana Raraunga Data Sovereignty | https://knowledgeauckland.org.nz/publications/mana-raraunga-data-sovereignty-what-is-it-and-why-does-it-matter-in-aotearoa-new-zealand/ | Tino Rangatiratanga 落地 |
| [^12] | Te Tiriti practice in health promotion | https://nwo.org.nz/wp-content/uploads/2018/10/ToW-practice-in-HP-online.pdf | 三条款框架 |
| [^13] | Diversity Statement structure (Canada) | https://universityaffairs.ca/career-advice/how-to-structure-your-diversity-statement-for-your-academic-job-search/ | 美式 vs NZ 对比 |
| [^16] | Māori representation in university strategy | https://www.tandfonline.com/doi/full/10.1080/13613324.2024.2306379 | 禁忌：泛泛而谈 |
| [^21] | NZ Govt Job Example (Forensic Psych) | https://jobs.govt.nz/jobtools/jncustomsearch.viewFullSingle?in_organid=16563&in_jnCounter=226465297 | JD 范例 |
| [^23] | NEAC Research Ethics NZ | https://neac.health.govt.nz/national-ethical-standards/part-one/research-in-the-new-zealand-context/ | Responsiveness to Māori |
| [^25] | UoA Equity for Staff | https://www.auckland.ac.nz/en/about-us/about-the-university/equity-at-the-university/equity-information-for-staff.html | 禁忌：美式 EDI |
| [^27] | RANZCP Te Tiriti significance | https://www.ranzcp.org/clinical-guidelines-publications/clinical-guidelines-publications-library/recognising-the-significance-of-te-tiriti-o-waitangi | 真诚定位 |
| [^35] | NZ Curriculum: CS strategies | https://newzealandcurriculum.tahurangi.education.govt.nz/case-study---strategies-to-engage-girls-in-computer-science/5637203861.p | Mātauranga 融入教学 |
| [^37] | Aotearoa Genomic Data Repository | https://pmc.ncbi.nlm.nih.gov/articles/PMC11696480/ | FAIR vs CARE |
| [^43] | Te Mana Raraunga Principles | https://www.otago.ac.nz/__data/assets/pdf_file/0014/321044/tmr-maori-data-sovereignty-principles-october-2018-832194.pdf | MDSov 原则 |
| [^47] | Otago Humanities MSF | https://www.otago.ac.nz/humanities/maori-at-humanities/strategic-framework | 学校信号 |
| [^49] | NZCER: Securing a position | https://www.nzcer.org.nz/sites/default/files/downloads/Optimising%20your%20academic%20career_%20ch%202_0.pdf | 面试策略 |
| [^51] | Otago Interview Info | https://www.otago.ac.nz/__data/assets/pdf_file/0022/307255/interview-information-for-applicants-715650.pdf | 学习意愿范式 |
| [^54] | Massey Tiriti Policy | https://www.massey.ac.nz/documents/1796/Treaty_of_Waitangi_Te_Tiriti_o_Waitangi_Policy.pdf | 学校信号 |
| [^56] | Waikato Treaty Analysis | https://www.journalofglobalindigeneity.com/article/92446 | 学校信号 |
| [^58] | Kaupapa Māori publications | https://www.researchgate.net/topic/Kaupapa-Maori/publications | Kāwanatanga 落地 |
| [^62] | Hakituri IoT project | https://academic.oup.com/iwc/article/34/2/60/6759159 | NZ 本土 CS 案例 |
| [^68] | Te Mana Raraunga official | https://www.temanararaunga.maori.nz/ | MDSov 官方 |
| [^71] | UoA Māori Data Sovereignty | https://research-hub.auckland.ac.nz/article/maori-data-sovereignty | LLM 语料保护 |
| [^76] | VUW Rite tahi | https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-rite-tahi | 学校术语 |
| [^78] | Digital inclusion NZ | https://www.digital.govt.nz/dmsdocument/196 | Ōritetanga 落地 |
| [^85] | Mātauranga Māori in Computing | https://www.unitec.ac.nz/epress/wp-content/uploads/2024/07/12-CITRENZ2023-Proceedings-Chitalia-et-al.pdf | 教学融合案例 |
| [^86] | Mātauranga Māori in Computing (RG) | https://www.researchgate.net/publication/384370602 | 教学融合案例 |
| [^87] | UoA Code of Conduct | https://www.auckland.ac.nz/en/on-campus/life-on-campus/code-of-conduct.html | 学校术语 |
| [^95] | UoA Strategic Plan | https://www.auckland.ac.nz/en/about-us/about-the-university/the-university/official-publications/strategic-plan/purpose-vision-principles-values.html | 学校信号 |
| [^96] | UoA Academic Recruitment Procedures | https://www.auckland.ac.nz/en/about-us/about-the-university/policy-hub/people-culture/recruitment-appointment-induction/academic-staff-recruitment-procedures.html | PVC(Māori) 否决权 |
| [^98] | VUW Whai wāhi | https://www.wgtn.ac.nz/maori-at-victoria/rauemi/te-tiriti-o-waitangi/principle-of-whai-wahi | 学校术语 |
| [^99] | Otago MSF 2030 | https://www.otago.ac.nz/maori/maori-strategic-framework | 学校信号 |
| [^100] | Waikato Treaty Statement | https://www.waikato.ac.nz/about/governance/docs/university-of-waikato-treaty-statement/ | 学校信号 |
| [^102] | UoA Equity Questions | https://www.auckland.ac.nz/assets/.../Appendix%202%20Equity%20Questions%20in%20Recruitment%20and%20Selection.docx | 面试题库 |

---

## 十、实现计划

### Phase 1: 策略文件（优先）
1. 创建 `strategies/nz_te_tiriti_strategy.md`
   - 矩阵定义 + 关键词清单 + 各标签修辞指南 + Sophia 背景校准 + 学校种子表
   - 从原策略文档蒸馏，保留所有引用链接

### Phase 2: Workflow 修改
2. 修改 `workflows/step1_research.md` — 增加 Step 10.5
3. 修改 `workflows/step2_analysis.md` — 增加 Te Tiriti 分析段
4. 修改 `workflows/step3_materials.md` — Humanizer 检查项

### Phase 3: 地区卡/模板更新
5. 修改 `region_knowledge/regions/new_zealand.md` §3.4 — 精简并指向策略文件
6. 更新学校卡模板 — 增加 Te Tiriti 字段块

### 验证
7. 对已有的 University of Auckland 产出（`output/university_of_auckland/cs/`）进行回测：用新矩阵重新评估，对比原 fit_report 中的 Te Tiriti 建议是否一致

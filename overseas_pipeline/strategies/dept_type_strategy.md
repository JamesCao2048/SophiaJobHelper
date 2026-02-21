# 院系画像与维度策略指南

本文件被 Step 1（院系画像生成）、Step 2（分析）和 Step 3（材料生成）读取。根据目标院系的四个信号维度，指导申请材料的修辞策略、术语选择、论文排序和经费叙事。

**与 `hci_density_strategy.md` 的协作**：本文件管"说什么"（定位、术语、论文、经费），密度策略管"对谁说"（点名、课程、Teaching 结构）。两者无冲突，Step 2/3 先读本文件确定基调，再读密度策略叠加细节。

---

## 一、院系画像生成（Step 1 Step 8.5 使用）

### 1.1 官方分类标签

仅供人类快速理解，**不驱动策略**。从院系名称关键词匹配：


| category_id | 典型名称关键词                                                                                             |
| ----------- | --------------------------------------------------------------------------------------------------- |
| `cs`        | "Computer Science", "EECS", "Computing Sciences", "Computer Engineering"                            |
| `ischool`   | "Information Science", "School of Information", "iSchool", "Informatics", "Library and Information" |
| `ds`        | "Data Science", "Data Analytics", "Computational Science", "Statistics and Data Science"            |
| `aix`       | "Artificial Intelligence", "AI", "Computing and X", "Connected Computing", "Responsible AI"         |
| `other`     | 不匹配以上任何 → 标注 `other` 并在 step1_summary 提示用户                                                          |


### 1.2 建院背景采集

从院系 About / History 页面提取以下信息，辅助维度判断：


| 字段                    | 说明                                                                               | 对维度判断的价值                                    |
| --------------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| `founding_year`       | 建院/更名年份                                                                          | ≤3 年的新院校评价文化可能尚未稳定；历史悠久的院系文化更固化             |
| `founding_method`     | `new_establishment` / `renamed_restructured` / `split_from_existing` / `unknown` | 更名重组继承原系文化；新建院校通常更灵活开放                      |
| `founding_motivation` | 建院动机（从 About 页面提取关键句）                                                            | 直接揭示价值取向（如"打破学科壁垒"→ 跨学科高，"迎合 AI 需求"→ 系统构建高） |


### 1.3 四个信号维度

#### 维度 1：定量严谨性偏好（quantitative_rigor）

衡量院系对定量方法/数学证明的看重程度。


| 等级       | 含义              | 判定信号                                                                                                                           |
| -------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `high`   | 强烈偏好统计/数学/形式化方法 | faculty 以统计学家/ML 理论家为主；JD 要求"mathematical foundations"；课程以统计/算法理论为主；院系前身为统计系                                                   |
| `medium` | 兼容定量与其他方法       | faculty 构成多元（含 HCI/设计/社科方向）；JD 未明确要求数学背景；课程涵盖多种方法论                                                                             |
| `low`    | 主动欢迎定性/混合方法     | JD 明确提"qualitative"/"mixed methods"/"ethnographic"；有 HCDS/设计方向的 faculty 或 cluster；院系使命声明提"diverse methodological perspectives" |


#### 维度 2：跨学科开放度（interdisciplinary_openness）

衡量院系对跨学科合作的重视程度。


| 等级       | 含义       | 判定信号                                                                                                                         |
| -------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `high`   | 跨学科是核心使命 | JD 含 "interdisciplinary"/"cross-faculty"/"collaboration across schools"；建院动机为打破学科壁垒；有 joint appointment 机制；cluster 涉及非 CS 领域 |
| `medium` | 鼓励但非必需   | JD 提及 collaboration 但不作为核心要求；院系有跨学科项目但非主打                                                                                    |
| `low`    | 纯学科导向    | JD 聚焦于单一学科贡献；faculty 同质化；无跨院合作机制                                                                                             |


#### 维度 3：系统构建偏好（system_building_preference）

衡量院系对可部署系统（vs 理论/方法论）的看重程度。


| 等级       | 含义           | 判定信号                                                                                                             |
| -------- | ------------ | ---------------------------------------------------------------------------------------------------------------- |
| `high`   | 重视可部署系统和工程能力 | JD 强调 "systems building"/"software development"/"deployed systems"；faculty 有大量系统论文（OSDI/SOSP/CHI systems）；课程侧重实践 |
| `medium` | 理论与系统并重      | faculty 兼有理论和系统研究者；JD 未明确偏好                                                                                      |
| `low`    | 重视理论/方法论贡献   | JD 强调 "theoretical foundations"/"methodological contributions"；faculty 以理论家为主                                    |


#### 维度 4：社会影响关注度（social_impact_focus）

衡量院系对社会/伦理影响的关注程度。


| 等级       | 含义             | 判定信号                                                                                                                   |
| -------- | -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `high`   | 社会/伦理影响是核心评价标准 | JD 含 "responsible AI"/"AI ethics"/"social impact"/"algorithmic accountability"；有专门的 ethics cluster/center；院系使命声明强调社会责任 |
| `medium` | 有关注但非主打        | 有 ethics 相关课程或教授但不是院系重点；JD 提及但不作为核心要求                                                                                  |
| `low`    | 纯技术评价          | JD 聚焦算法/系统性能；无 ethics/social impact 相关内容                                                                               |


### 1.3.5 Faculty 研究背景分析（major/minor）

仅凭 research interests 文字描述难以准确判断 faculty 的方法论偏好。需要通过其**发表论文的 venue** 推断背景类型，进而辅助四个维度的评级。

**Background 类别及 venue 对照：**

| background_id | 代表 Venue | 对维度的贡献 |
|--------------|------------|------------|
| `hci_qual` | CHI(qual)/CSCW/TOCHI/DIS/GROUP | QR↓, SI↑ |
| `hci_systems` | CHI(systems)/UIST/IMWUT/ASSETS/ITS | SB↑ |
| `ml_theory` | NeurIPS/ICML/ICLR/AISTATS/UAI | QR↑↑ |
| `ml_applied` | KDD/WWW/RecSys/WSDM/AAAI/IJCAI | QR↑, SB↑ |
| `nlp` | ACL/EMNLP/NAACL/COLING/EACL | QR↑ |
| `se` | ICSE/FSE/ASE/ISSTA/ICSME/MSR | QR↑, SB↑ |
| `systems` | OSDI/SOSP/EuroSys/NSDI/ATC/USENIX | QR↑, SB↑↑ |
| `theory_algo` | STOC/FOCS/SODA/ITCS/CCC | QR↑↑ |
| `stats_ds` | JASA/AoS/JRSS/Biometrics/统计学期刊 | QR↑↑ |
| `responsible_ai` | FAccT/AIES/ACM CSUR(ethics)/CHI bias | SI↑↑ |
| `interdisciplinary` | 3+ 类别 venue 均有分布，无主导方向 | IO↑ |

**Major/Minor 判定规则：**
- **major**：占该 faculty 近期发表（5 年内）的 ≥60%
- **minor**：占 20–40%（明显的次要方向，minor 可为 null）
- 若主页无发表列表，通过 Google Scholar 或 DBLP 补充

**对维度评估的影响（统计院系 faculty 的背景分布）：**
- 半数以上为 `ml_theory` / `stats_ds` → QR 倾向 **high**
- 多位 `hci_qual` / `responsible_ai` → QR 倾向 **low**，SI 倾向 **high**
- 多位 `hci_systems` / `se` / `systems` → SB 倾向 **high**
- 多位 `interdisciplinary` → IO 倾向 **high**

**faculty_data.json 记录格式（每位 faculty 新增字段）：**

```json
{
  "name": "Prof. Jane Smith",
  "research_background": {
    "major": "hci_systems",
    "minor": "nlp",
    "evidence_venues": ["CHI 2024 (systems)", "UIST 2023", "EMNLP 2023"]
  }
}
```

### 1.4 典型院系的维度画像参考

以下为基于验证数据的参考基线，**实际评估必须基于目标院系的具体信号**：


| 院系实例                       | QR  | IO  | SB  | SI  | 说明                |
| -------------------------- | --- | --- | --- | --- | ----------------- |
| 传统 CS 强校（如 CMU SCS）        | H   | L   | H   | L   | 算法+系统双强，学科导向      |
| UVA School of Data Science | M   | H   | M   | H   | 独立建制，主动招 HCI/伦理方向 |
| Cornell Statistics & DS    | H   | M   | L   | L   | 统计学转型，偏理论         |
| UW iSchool                 | L   | H   | M   | H   | 信息科学传统，欢迎定性方法     |
| Stanford HAI (affiliate)   | M   | H   | H   | H   | 跨学科旗舰，系统+影响并重     |
| Hopkins DSAI               | M   | H   | H   | M   | 150 教职大扩招，全学科覆盖   |


> ⚠ 以上仅为参考，不可直接套用。必须从目标院系的实际 JD、faculty、cluster、课程提取信号。

---

## 二、各维度策略规则（Step 2/3 使用）

### 通用规则（所有维度组合适用）

**始终主推的发表**：

- TOCHI 2023（CoAIcoder）— 100+ 引用，奠基性地位
- CHI 2024（CollabCoder）— 180+ 引用，端到端系统
- 这两篇在任何院系类型中都应出现在 Cover Letter 和 Research Statement 的核心位置

**方法论呈现原则**（基于验证 V5）：

- **清晰自信地解释定性方法本身**，而非伪装为其他东西
- 展示"定性洞察 → 系统设计 → 实证评估"的完整闭环
- 不要称 QDA 为"语义计算"或"降维"——懂 NLP 的评委会追问
- 正确做法：解释 formative study 是什么、为什么重要、它如何驱动了系统设计决策

### 2.1 定量严谨性偏好（quantitative_rigor）

#### high — 评委偏好定量/数学/形式化方法

**Cover Letter**：

- 方法论呈现：清晰解释定性方法的科学性，重点强调量化评估结果
  - ✅ "Through controlled experiments with N=XX participants, our system achieved XX% improvement in coding efficiency while maintaining inter-rater reliability of XX"
  - ✅ "Our evaluation framework incorporates both quantitative metrics (agreement rates, time-on-task) and qualitative validation"
  - ❌ 不要回避"qualitative"这个词，但要紧跟量化证据
- 额外强调：ICPC 2026（代码理解），用 1-2 句说明跨界到 Software Engineering 的价值
- 额外强调：ICSME 2023（ML 系统测试复杂度），展示对 SE 核心问题的贡献

**Research Statement**：

- 每个研究方向必须包含量化评估结果（效率提升百分比、准确率、用户满意度评分）
- 系统架构图与量化结果并重
- Future Work 中提及可度量的目标（"achieve XX% accuracy on benchmark Y"）

**术语体系**：

- 推荐：evaluation framework, controlled experiment, inter-rater reliability, scalable, benchmark, ablation study
- 谨慎使用：sensemaking, lived experience, narrative analysis（不禁止，但不放在显眼位置）

#### medium — 兼容多种方法

**Cover Letter**：

- 方法论呈现：平衡展示定性和定量贡献，无需刻意偏重
- 正常推出 TOCHI + CHI 主推论文

**Research Statement**：

- 混合呈现：用户研究洞察 + 系统贡献 + 量化评估

#### low — 欢迎定性/混合方法

**Cover Letter**：

- 可充分展开社科语言：sensemaking, grounded theory, thematic analysis
- 重点强调 CHI Workshop "LLMs as Research Tools" 的社区领导力
- Impact Statement 的社会价值论述可完整释放

**Research Statement**：

- 可包含用户引语、案例叙事
- 理论贡献（如 Human-LLM Interaction Taxonomy）可作为主线

### 2.2 跨学科开放度（interdisciplinary_openness）

#### high — 跨学科是核心使命

**Cover Letter**：

- 核心定位：**"桥梁型学者——连接计算技术与垂直领域"**
- 必须展示跨学科落地记录：
  - JHU Malone Center（医疗健康工程）— 将 QDA 工具应用于临床对话分析
  - SMART Singapore-MIT Alliance（跨学科合作）— 与 Thomas Malone 合作的人机协作分类学
- 跨学院合作段落（按 JD 跨学科信号强度）：
  - JD 信号 **high**：必须包含，详细点名目标大学具体学院和教授，说明合作方向
  - JD 信号 **medium**：包含，简要提及 1-2 个合作方向
  - JD 信号 **low**：不需要专门段落

**Research Statement**：

- Future Work 明确列出跨学科应用场景（医疗、教育、公共政策）
- 展示研究工具作为"基础设施"赋能其他领域的愿景

**经费叙事**：

- NSF AI Institutes / NIH R01（AI + 健康）/ NSF SBE-CISE 跨学科项目
- "我的加入将打开跨学科经费渠道，连接 CISE 与 SBE/医学/教育资助"

#### medium — 鼓励但非核心

**Cover Letter**：

- 提及跨学科能力但不作为主打卖点
- JHU/SMART 经历简要提及即可

**经费叙事**：

- 主打学科内资助（NSF CISE/IIS），跨学科作为补充

#### low — 纯学科导向

**Cover Letter**：

- 聚焦学科内贡献，跨学科经历作为背景而非卖点
- 不需要跨学院合作段落

**经费叙事**：

- NSF CISE Core / CAREER

### 2.3 系统构建偏好（system_building_preference）

#### high — 重视可部署系统

**Cover Letter**：

- 核心定位：**"构建下一代人机协作系统的系统工程者"**
- 重点强调：
  - MindCoder.ai — 公开部署的 trustworthy QDA 平台
  - CollabCoder — 开源端到端协作 QDA 工具
  - 克服的纯技术挑战：提示词工程稳定性、长上下文处理、多用户并发同步、多 Agent 架构

**Research Statement**：

- 系统架构图为主线
- 每个方向先讲系统设计，再讲用户研究验证
- 强调可复用性、开源社区、部署规模（用户数、GitHub stars）

**术语体系**：

- 推荐：end-to-end system, deployed platform, open-source, pipeline architecture, multi-agent framework
- 可用但非重点：user study, formative research

#### medium — 理论与系统并重

- 系统和理论均衡呈现
- 架构图和研究框架图交替使用

#### low — 重视理论/方法论

**Cover Letter**：

- 核心定位：**"人机协作领域的方法论创新者"**
- 重点强调：
  - Human-LLM Interaction Taxonomy（CHI EA 2024, 80+ 引用）— 理论框架贡献
  - CoAIcoder 的理论贡献（权衡空间定义）
  - Community Service：CHI Workshop organizer, reviewer

**Research Statement**：

- 理论贡献 > 系统贡献
- 强调"第二阶影响"：框架被多少后续工作引用、推动了哪些新研究方向
- Future Work 以研究问题驱动，而非系统目标驱动

### 2.4 社会影响关注度（social_impact_focus）

#### high — 社会/伦理影响是核心

**Cover Letter**：

- 充分释放 Impact Statement 中的社会价值论述
- 重点强调：
  - CollabCoder 如何解决团队协作中的权力不平衡
  - LLM 在关键任务中对人类认知的替代风险
  - Trustworthy AI — 透明共识机制防止 LLM hallucination

**术语体系**：

- 推荐：algorithmic accountability, responsible AI, human agency, power dynamics, trustworthy AI, sensemaking, digital equity
- 可充分使用社科术语

**额外材料**：

- Diversity/Impact Statement 篇幅可扩展
- Teaching Statement 可加入 AI Ethics 课程设计

#### medium — 有关注但非主打

- Impact 段落正常长度
- 提及 responsible AI 但不作为核心叙事

#### low — 纯技术评价

- Impact 段落精简
- 聚焦技术贡献和性能指标
- DEI/Impact Statement 按最低要求

---

## 三、关键维度组合的特殊规则

某些维度组合需要特殊处理，因为维度间可能产生张力：

### 3.1 quantitative_rigor=high + social_impact=high

**场景**：院系既重视定量严谨又关注社会影响（如某些 Responsible AI 项目）
**策略**："用数据证明社会影响"

- 量化 impact 指标：系统用户数、分析效率提升、数据标注质量改善百分比
- 展示 trustworthy AI 框架的可度量评估结果
- 避免纯叙事性的 impact 描述，每个 claim 附证据

### 3.2 interdisciplinary=high + system_building=low

**场景**：跨学科导向但偏理论（如某些 Science Studies / STS 相关院系）
**策略**："理论桥梁型学者"

- 强调方法论跨界贡献（而非系统工具）
- Taxonomy 论文和 CoAIcoder 理论框架作为主打
- 跨学科叙事聚焦"方法论输出"而非"工具输出"

### 3.3 quantitative_rigor=low + interdisciplinary=high

**场景**：完全拥抱多元方法的跨学科院校（如某些 iSchool）
**策略**：全面释放社科语言

- 可使用 grounded theory, thematic analysis 等术语作为研究方法描述
- 强调 community building：CHI Workshop、开源社区
- 经费叙事加入人文/社科资助来源（IMLS、NEH、基金会）

### 3.4 quantitative_rigor=high + system_building=high

**场景**：硬核工程型院系（如传统 CS 强校的系统方向）
**策略**：最大程度展示工程能力

- Research Statement 以系统为主线，用户研究作为"需求分析阶段"
- 强调：多 Agent 架构、LLM pipeline 工程、并发处理、部署规模
- ICPC 2026 + ICSME 2023 提到靠前位置
- 避免在显眼位置使用 "user study" 作为独立贡献——改为 "requirements engineering through empirical investigation"

### 3.5 interdisciplinary=high + social_impact=high + system_building=high

**场景**：AI+X 旗舰（如 Stanford HAI、Hopkins DSAI）
**策略**：全能型叙事

- 同时展示：系统构建能力 + 跨学科落地记录 + 社会影响愿景
- 这是 Sophia 最适合发挥的场景——全部材料充分展开
- 经费叙事最激进：NSF AI Institute + NIH + 跨学科大额联邦资助

---

## 四、主推论文完整排序表

所有维度组合共享的基础排序 + 各维度的调整：

### 4.1 核心论文池


| #   | 论文                     | 会议/期刊             | 引用   | 核心价值                      |
| --- | ---------------------- | ----------------- | ---- | ------------------------- |
| P1  | CoAIcoder              | TOCHI 2023        | 100+ | 奠基：定义 AI 辅助协作定性分析的权衡空间    |
| P2  | CollabCoder            | CHI 2024          | 180+ | 系统：首个端到端 LLM 驱动协作 QDA 工作流 |
| P3  | VISAR                  | UIST 2023         | 170+ | 系统：AI 辅助论证写作，视觉编程         |
| P4  | Code Comprehension     | ICPC 2026         | —    | 跨界：SE × HCI，代码理解          |
| P5  | Taxonomy               | CHI EA 2024       | 80+  | 理论：Human-LLM 交互模式分类学      |
| P6  | LLMs as Research Tools | CHI 2024 Workshop | —    | 社区：领导力，跨领域召集              |
| P7  | ML Testing Complexity  | ICSME 2023        | —    | 跨界：SE × ML，系统测试           |
| P8  | MindCoder (arXiv)      | In submission     | —    | 系统：最新，trustworthy QDA 平台  |
| P9  | Evaluation Framework   | In prep           | —    | 方法论：LLM 辅助 QDA 评估框架       |


### 4.2 维度驱动的排序调整


| 维度值                     | 提升                                       | 降低              |
| ----------------------- | ---------------------------------------- | --------------- |
| quantitative_rigor=high | P4(ICPC), P7(ICSME) 各+1 句说明              | P5(Taxonomy) 放后 |
| system_building=high    | P2(CollabCoder), P8(MindCoder) 靠前，展开技术细节 | P5 放后           |
| system_building=low     | P5(Taxonomy), P1(CoAIcoder 理论面) 靠前       | P8 简要提及         |
| social_impact=high      | P6(Workshop) 提前，展示社区领导力                  | —               |
| interdisciplinary=high  | 额外强调 JHU Malone + SMART 经历（非论文，但重要）      | —               |


---

## 五、经费叙事速查表


| 维度组合              | 主打经费来源                                     | 叙事角度                   |
| ----------------- | ------------------------------------------ | ---------------------- |
| IO=high           | NSF AI Institutes, NIH R01, 跨学科大额项目        | "我的加入将打开新的跨学科经费渠道"     |
| IO=low, QR=high   | NSF CISE Core, NSF CAREER                  | "聚焦 HCI/AI 核心方向的高质量项目" |
| IO=low, QR=low    | NSF CISE/IIS, NSF SBE                      | "连接技术与社会研究的桥梁"         |
| SI=high           | NSF Responsible AI, 基金会资助（Ford, MacArthur） | "负责任 AI 是国家级资助热点"      |
| SB=high           | NSF CISE/CNS（系统方向）, DARPA                  | "系统驱动的研究获得持续工业/国防关注"   |
| IO=high + SI=high | 最激进：NSF AI Institute + NIH + 跨部门           | "整合多资助来源的大型跨学科项目"      |


> 注：iSchool 的经费期望与 CS 系相当或略低，但接受更广泛的来源（IMLS、NEH、基金会），不必聚焦联邦资助。（验证 V3）

---

## 六、跨学院扫描触发条件

### 6.1 触发规则

当以下两个条件**同时满足**时，Step 1 Step 8.6C 执行跨学院扫描：

1. `interdisciplinary_openness == "high"`
2. JD 含跨学科信号关键词：`"interdisciplinary"` / `"cross-faculty"` / `"collaboration across schools"` / `"joint appointment"` / `"multi-departmental"`

### 6.2 扫描深度

- 从目标大学官网找到 2-3 个与 Sophia 研究最相关的其他学院
- 优先级：医学院/公共卫生 > 教育学院 > 公共政策 > 商学院
- 爬取各学院 faculty 页面，找与 Sophia 研究有交集的教授
- 记录合作角度（如"临床对话分析"、"教育技术评估"）

### 6.3 Cover Letter 使用规则


| JD 跨学科信号 | Cover Letter 跨学院合作段落 |
| -------- | -------------------- |
| high     | 必须包含，详细点名具体学院和教授     |
| medium   | 包含，简要提及合作方向（1-2 句）   |
| low      | 不需要                  |


---

## 七、与 HCI 密度策略的协作规则

### 7.1 读取顺序

1. **先读本文件** → 确定整体基调（定位、术语、论文、经费）
2. **再读 `hci_density_strategy.md`** → 在基调之上叠加点名/课程/Teaching 细节

### 7.2 无冲突保证

两个策略文件的职责完全不重叠：


| 决策项                        | 由谁决定               |
| -------------------------- | ------------------ |
| "Sophia 的核心定位怎么说？"         | 本文件（按维度组合）         |
| "点名哪些教授？"                  | hci_density（按密度等级） |
| "用什么术语体系？"                 | 本文件（按维度组合）         |
| "课程怎么排序？"                  | hci_density（按密度等级） |
| "主推哪些论文？"                  | 本文件（按维度组合）         |
| "Teaching Statement 什么结构？" | hci_density（按密度等级） |
| "经费怎么叙述？"                  | 本文件（按维度组合）         |


### 7.3 维度 × 密度的常见组合示例


| 维度画像                     | 密度策略         | 综合效果                                  |
| ------------------------ | ------------ | ------------------------------------- |
| QR=high, SB=high, IO=low | pure_pioneer | 全硬核模式：工程语言+量化证据+CS核心课优先+仅点名目标系教授      |
| QR=low, SI=high, IO=high | specialist   | 全社科模式：社会影响语言+跨学科经费+HCI高阶课优先+点名多系HCI教授 |
| QR=medium, IO=medium     | builder      | 均衡模式：混合语言+互补课程+点名现有HCI教授展示协同          |


---

## 八、参考资料与验证来源

### 验证报告（2026-02-20 完成）


| V#  | 论断                       | 结果     | 关键来源                                                                                                                                                                     |
| --- | ------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| V1  | CRA 2026: AI 占 CS 教职 29% | ✅ 已验证  | [CRA CRN Jan 2026](https://cra.org/crn/2026/01/what-advertised-faculty-searches-reveal-about-computer-science-hiring-in-2026/)                                           |
| V2  | DS 系话语 = 统计/A/B 测试       | ❌ 夸大   | UVA DS, Cornell Stats&DS, Hopkins DSAI 等实际 JD                                                                                                                            |
| V3  | iSchool 经费期望极高           | ❌ 夸大   | [UW iSchool Tenure Criteria](https://ischool.uw.edu/faculty-affairs/promotion-criteria-guidelines/tt-assistant-associate)                                                |
| V4  | AI+X Tenure 摸索中          | ✅ 部分验证 | MIT Schwarzman, Stanford HAI, UMD AIM                                                                                                                                    |
| V5  | QDA 被误解为主观               | ✅ 感知真实 | [Bigham 2018](https://jeffreybigham.com/blog/2018/only-hci-person-in-a-cs-department.html), [Correll 2024](https://mcorrell.medium.com/the-othering-of-hci-ab0a07edc69f) |


### 原始参考

- 院系申请策略：`general/research_job_rules/院系分析/院系申请策略.md`（Gemini 生成，已验证修正）
- 关键词列表：`general/research_job_rules/院系分析/院系申请与关键词列表.md`（Gemini 生成，已验证修正）
- 设计文档：`overseas_pipeline/docs/plans/2026-02-20-dept-type-strategy-design.md`


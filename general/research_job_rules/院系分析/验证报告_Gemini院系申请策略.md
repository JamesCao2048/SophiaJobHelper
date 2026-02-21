# 验证报告：Gemini 院系申请策略内容核查

**验证日期**：2026-02-20
**验证方法**：联网搜索 + 抓取原始来源文档
**被验证文件**：`院系申请策略.md`、`院系申请与关键词列表.md`

---

## 总体结论

Gemini 生成的院系申请策略框架**整体方向正确**，但存在若干被夸大、过度简化或由工业界认知混入的错误。核心建议（"战略变色龙"定位、不同院系类型需要不同修辞）经验证是合理的。

---

## V1：CS 教职市场 AI 占比 29%（CRA 2026 数据）

**结论：✅ 数据准确，但有若干措辞问题**

### 已验证内容

- AI/Data Mining/Machine Learning 占所有 CS 教职搜索的 **29%**，是 12 年研究史上历史最高 ✅
- 网络安全占 **21%**，AI + 安全合计 **50%** ✅
- CS 教职整体相比 2024 年下降 **33%** ✅
- 搜索机构数量下降约 **25%** ✅

### Gemini 的措辞问题

| Gemini 原文 | 实际情况 | 影响 |
|-----------|---------|------|
| "一半以上的教职资源" | 准确数字是 50%，不是"过半" | 措辞夸大，需修正 |
| "自2016年以来最低" | 原文有限定"不含2021 COVID年" | Gemini 遗漏了这个重要注脚 |
| 表述为"录用"情况 | CRA 研究统计的是**招聘搜索数**，不是实际录用 | 方法论区别，实际录用率可能不同 |

### 额外有价值的细节（Gemini 未提）

- 地区差异极大：太平洋西部降 65%，南部仅降 22%
- Theory/算法因量子计算崛起成为第三热门
- 研究窗口仅覆盖 2025 年 8 月至 11 月中旬的公开广告

### 来源

- 主来源：[CRA CRN Jan 2026](https://cra.org/crn/2026/01/what-advertised-faculty-searches-reveal-about-computer-science-hiring-in-2026/)
- 作者：Craig E. Wills, Worcester Polytechnic Institute

---

## V2：DS 系主流话语体系 = 统计显著性/模型参数量/A/B 测试

**结论：❌ 严重夸大，描述的是工业界 ML 文化，不是学术 DS 院系**

### 核心发现

查看了 7+ 所院校的 DS 教职 JD（UVA、UChicago、Cornell、San Jose State、Hopkins、Princeton、OldDominion）：
- **没有一份**提到 A/B 测试、模型参数量或统计显著性作为要求
- DS 系类型差异巨大，必须区分三类

### DS 系三类划分

| 类型 | 典型院校 | 实际评价文化 | Gemini 描述准确度 |
|------|---------|------------|----------------|
| **统计学转型 DS 系** | Cornell Statistics & DS | 偏定量/统计理论 | 部分准确 |
| **独立建制 DS 学院** | UVA School of DS, UNC Charlotte | 主动跨学科，招 HCI/设计/伦理 | 完全错误 |
| **DS 研究所** | Hopkins DSAI, Princeton DS | 覆盖人文/社科/工程 | 完全错误 |

### 反驳证据

- **UVA DS（2025 年录用）**：Hannah Bako（HCI+数据可视化）、Nur Yildirim（参与式 AI），还有社会学家和技术政策研究者
- **UC Berkeley iSchool** 专门发布 "Human-Centered Data Science" 教职，明确欢迎定性方法
- **UW Human-Centered Data Science Lab**：Cecilia Aragon 的实验室同时使用定量统计和民族志方法，其《Human-Centered Data Science》(MIT Press, 2022) 是该领域里程碑著作
- **Princeton DS**：明确覆盖"all science, engineering, social science, and humanities areas"

### 对策略文件的影响

**不可使用**"DS 系必须用 A/B 测试语言"的建议。

正确策略：
1. 必须先判断目标 DS 系属于哪种子类型（统计转型 vs 独立建制 vs 研究所）
2. 使用四维信号框架评估，不能因名字叫 Data Science 就套用固定策略

### 来源

- [UVA DS Faculty Jobs](https://datascience.virginia.edu/faculty-jobs)
- [UVA DS 2025 年新进教员](https://datascience.virginia.edu/news/school-data-science-welcomes-nine-new-faculty-2025)
- [UC Berkeley iSchool HCDS 职位](https://www.ischool.berkeley.edu/about/ischooljobs/human-centered-data-science)
- [UW HDSL Lab](https://depts.washington.edu/hdsl/)
- [Princeton 跨学科 DS 招聘](https://cdh.princeton.edu/opportunities/faculty-positions-in-interdisciplinary-data-science/)

---

## V3：iSchool 对跨学科联邦资金期望"极高"

**结论：❌ 夸大，且混淆了两个概念**

### 核心发现

Gemini 混淆了两件事：
- **iSchool 本身具有跨学科属性** → 正确
- **iSchool 期望教员专门去申跨学科联邦资助** → 不准确

### 实际情况

**UW iSchool Tenure 标准原文**：
> "Outside funding of research from prestigious foundations and institutes (in those disciplines where **it is available**) can be viewed as a significant part of the scholarly record, depending on the relative size of the grant..."

措辞极为温和，且有"在资助可获得的领域内"的限定——意味着图书馆学、数字人文方向的教员不受相同经费压力。

**Berkeley iSchool 的 HCI 教职 JD**：完全没有提到经费获取要求。

### iSchool 经费期望的准确描述

| 对比项 | 传统 CS R1 院校 | iSchool R1 院校 |
|-------|--------------|----------------|
| 对资助的要求措辞 | "establish externally funded research program"（强制性） | "pursue extramural funding as needed"（弹性） |
| 接受的资助来源 | 主要 NSF CISE/联邦 | NSF + IMLS + NEH + 基金会（更广泛） |
| 资助与论文的权重关系 | 资助是 tenure 关键条件 | 发表质量权重更高，资助是多个因素之一 |

### Gemini 的具体错误

iSchool 教员申请的主要经费是 **NSF CISE/IIS**（学科内，非跨学科），与 CS 系教员完全相同。"跨学科联邦资助"并非 iSchool 特别偏好。

### 来源

- [UW iSchool Tenure Criteria](https://ischool.uw.edu/faculty-affairs/promotion-criteria-guidelines/tt-assistant-associate)
- [Berkeley iSchool HCI 职位](https://www.ischool.berkeley.edu/about/ischooljobs/assistant-professor-hci)
- [CRA: Promotion and Tenure of Interdisciplinary Faculty](https://cra.org/resources/best-practice-memos/promotion-and-tenure-of-interdisciplinary-faculty/)

---

## V4：AI+X 新学院 Tenure Guidelines 尚在摸索

**结论：✅ 部分验证，双重汇报挑战属实，但各校应对方式有差异**

### 已验证内容

CRA、APA、Columbia、MSU 均有文献记录 joint appointment 的挑战：
- "双重考核"困境（Double Jeopardy）：两套评审、两套委员会 ✅
- "50-50 变 75-75"现象：两边都要求完整的服务/委员会参与 ✅
- 跨学科工作在两方都可能被认为"不够属于本学科" ✅

### 各校实际情况

| 院校 | 成立时间 | Tenure 状态 |
|------|---------|------------|
| MIT Schwarzman College | 2019 | 已有实际 tenure 案例（2025 年），但细则仍少公开 |
| Stanford HAI | — | **完全不做 tenure 授予单位**，faculty 在原系评 tenure |
| UMD AIM | 近年 | 承认问题，采用"一人一份 MOU"临时方案 |
| Vanderbilt Connected Computing | 2025 | 尚无院级评估细则，延用全校通用标准 |
| USF Bellini College | 2025 | 2025 建，首批 tenure 案例约在 2030-2031 |

### 对候选人的实际建议

申请 AI+X 机构时，建议在面试时主动询问：
1. 你的 tenure home（主要归属院系）是哪里？
2. 是否有明文的 joint appointment 备忘录（MOU）？
3. 谁来组成你的 tenure 评审委员会？

### 来源

- [MIT tenure 案例 2025](https://computing.mit.edu/news/the-tenured-engineers-of-2025/)
- [Stanford HAI: Affiliated Faculty](https://hai.stanford.edu/become-hai-affiliated-faculty)
- [UMD AIM 职位描述](https://umd.wd1.myworkdayjobs.com/en-US/UMCP/job/Senior-Tenure-Track-Faculty-at-the-Artificial-Intelligence-Interdisciplinary-Institute-at-Maryland--AIM-)
- [CRA: Interdisciplinary Faculty P&T](https://cra.org/resources/best-practice-memos/promotion-and-tenure-of-interdisciplinary-faculty/)
- [Columbia: Joint Appointments Best Practices](https://provost.columbia.edu/content/joint-and-interdisciplinary-appointments-best-practices-full-version)

---

## V5：QDA 在 CS/DS 中被误解为"主观/缺乏严谨性"

**结论：✅ 感知问题属实；但 Gemini 的"重新包装为语义计算"建议有风险，不应采用**

### 已验证内容：感知问题确实存在

**Jeffrey Bigham（CMU HCII，HCI 界知名教授）2018 文章**：
> "HCI people face the burden of truly not being seen by many Computer Scientists as a real part of their field."
> "If they aren't really sure that HCI is a valid research discipline, will they actually decide to tenure you?"

**2025 年 HCI 期刊论文**（记录"Positivism Creep"现象）：
> 定量范式的标准（如"需要控制偏差"、"需要可复现"）被强加于定性研究，在近几届 CHI/CSCW 已出现系统性的错误 review 标准。

### Gemini 建议的问题：不应将 QDA 伪装为"语义计算"

**风险**：
1. 真正懂 NLP 的评委会追问技术细节（你的 embedding 模型是什么？降维方法是 PCA 还是 t-SNE？）
2. 懂 HCI 的评委会觉得你在回避方法论，信任度下降
3. 方法论不诚实是学术界大忌

**正确策略**（来自 HCI 社区共识）：

> 清晰自信地解释定性方法本身。Bigham 描述的成功案例是：候选人清楚解释了"formative study 是什么、什么使它变好、它告诉了我们什么"——委员会正面回应，因为方法被严谨地定义了。

**Yisong Yue（Caltech）建议**：在 JD 对应的研究领域语言下诠释你的工作——但这是"调整描述方式"，不是"伪装方法论"。

### 实际可用的应对策略

1. **"定性洞察 → 系统设计 → 量化评估"三段式**：让定性研究成为工程决策的依据，而非孤立的研究贡献
2. **系统并举**：展示 QDA 研究直接产出了 MindCoder.ai 和 CollabCoder 等可部署系统
3. **量化验证**：每个定性发现后跟量化实验结果（inter-rater reliability、效率提升百分比）
4. **不回避，但要框定**：正面使用"qualitative"，但紧跟其科学定义和量化验证

### 来源

- [Bigham: Only HCI Person in a CS Dept (2018)](https://jeffreybigham.com/blog/2018/only-hci-person-in-a-cs-department.html)
- [Correll: The Othering of HCI (2024)](https://mcorrell.medium.com/the-othering-of-hci-ab0a07edc69f)
- [H is for Human: Evaluating Qualitative Research in HCI (2025)](https://www.tandfonline.com/doi/full/10.1080/07370024.2025.2475743)
- [Yue: Tips for CS Faculty Applications](https://yisongyue.medium.com/checklist-of-tips-for-computer-science-faculty-applications-9fd2480649cc)

---

## 对策略文件的总体修正指令

| Gemini 原始建议 | 修正后建议 |
|--------------|---------|
| DS 系 = 统计显著性话语体系 | 必须先判断 DS 系子类型；独立建制 DS 学院通常欢迎 HCI/定性方法 |
| iSchool 对跨学科经费期望极高 | iSchool 经费期望与 CS 相当或略低，来源更多元（含 IMLS/NEH/基金会） |
| QDA 应重新包装为"语义计算" | 清晰解释定性方法 + 系统构建并举；不伪装 |
| AI+X Tenure 完全不成熟 | 部分真实，但 Stanford HAI 等已有解决方案；面试时主动确认 tenure 归属 |
| "AI + 安全占过半数教职" | 准确数字是恰好 50%，不是"过半" |

---

*验证执行人：Claude Code (Opus 4.6)*
*对应策略文件：`overseas_pipeline/strategies/dept_type_strategy.md`*
*相关设计文档：`overseas_pipeline/docs/plans/2026-02-20-dept-type-strategy-design.md`*

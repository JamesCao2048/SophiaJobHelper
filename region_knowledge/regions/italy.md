# 意大利 教职申请规则卡 (CS/HCI)

## 元信息
- region_id: italy
- last_verified: 2026-02-19
- status: draft (待验证)
- source_documents:
  - `general/research_job_rules/美国欧洲CS_HCI教职申请指南.md` Section 5 (L161-188)
- needs_review: []

---

## 1. 体系特点：量化指标的森严壁垒

意大利是欧洲 **最量化、最刚性** 的学术招聘体系。候选人首先面对的不是面试官，而是**算法和指标**。

---

## 2. 第一关：国家科学资格认证（ASN）

**没有 ASN，不得申请意大利终身教职。**

### ASN 运作机制

| 维度 | 说明 | source |
|------|------|--------|
| 性质 | **对过往学术产出的量化审核**（非考试）| [R18](https://www.gennarovessio.com/asn) |
| CS/HCI 学科分类 | **01/B1 (Informatica)** 或工程学院下的 **09/H1** | [R18](https://www.gennarovessio.com/asn) |
| 有效期 | 6 年 | [R18](https://www.gennarovessio.com/asn) |

### 三大量化指标（必须满足 2/3）

| 指标 | 计算范围 | 来源数据库 | source |
|------|---------|---------|--------|
| 论文总数 | 过去 5/10 年 | Scopus 或 WoS | [R18](https://www.gennarovessio.com/asn) |
| 总引用数 | 全职业生涯 | Scopus 或 WoS | [R18](https://www.gennarovessio.com/asn) |
| H-index | 全职业生涯 | Scopus 或 WoS | [R18](https://www.gennarovessio.com/asn) |

每个指标与全国该学科的**中位数**比较，超过中位数即算达标。

### ⚠ HCI 的困境

- 意大利 CS 学科（01/B1）传统偏重**理论计算机和算法**
- CHI/CSCW 等顶级会议在老派委员会眼中**不如 SCI 期刊**（即使影响因子低）
- 近年会议论文地位有所提升，但需确认：
  1. 论文是否被 **Scopus 正确索引**（会议论文的索引状态参差不齐）
  2. 自查 Scopus Author Profile，确认所有论文已归入个人档案
- source: [R19](https://pmc.ncbi.nlm.nih.gov/articles/PMC10435642/)

---

## 3. 职级术语映射

| 意大利职称 | ≈ 美国等级 | 合同类型 | source |
|-----------|-----------|---------|--------|
| **RTT (Ricercatore Tenure Track)** | 助理教授 | **3 年**（初级）或 **6 年**（资深）合同，考核后转副教授 | [R20](https://www.unive.it/pag/28008/), [R21](https://academia.stackexchange.com/questions/46008/) |
| **Professore Associato (PA)** | 副教授 | 永久 + ASN 要求 | [R21](https://academia.stackexchange.com/questions/46008/) |
| **Professore Ordinario (PO)** | 正教授 | 永久 + ASN 要求 | -- |
| 旧体系 RTD-A/B | （已被 RTT 取代）| -- | [R21](https://academia.stackexchange.com/questions/46008/) |

**RTT 特点（2024 改革，取代 RTD-A/B）**：
- 合同时长：**3 年**（初级）或 **6 年**（资深），按候选人资历决定 [R21](https://academia.stackexchange.com/questions/46008/)
- 持有 ASN + 第 3 年考核通过 → 直接转 PA（副教授）[R20](https://www.unive.it/pag/28008/)
- 唯一申请前提：博士学位

---

## 4. 招聘渠道

### 4.1 标准公开招聘（RTT）

- 大学在 `universitaly.it` 或各校网站发布公告
- 面试通常较短（30–60 分钟，非美式 1–2 天）
- 委员会评审：科研指标 + 研究计划 + 简短面试

### 4.2 直接征召（Chiamata Diretta）——资深学者的捷径

| 条件 | 说明 | source |
|------|------|--------|
| 资格 | 在海外已拥有**永久教职**（或同等职位）**至少 3 年** | [R22](https://www.unimi.it/en/university/work-us/researcher-recruitment) |
| 机制 | 大学可直接发出邀请，**绕过 ASN 和公开招聘** | [R22](https://www.unimi.it/en/university/work-us/researcher-recruitment) |
| 适用场景 | 资深 HCI 学者"空降"意大利的最佳途径 | [R22](https://www.unimi.it/en/university/work-us/researcher-recruitment) |

> Sophia 目前不符合 Chiamata Diretta 资格（需永久教职 3 年以上），但可关注 RTT 路线。

---

## 5. HCI 重点机构

| 大学 | HCI 特点 |
|------|---------|
| **米兰理工大学（Politecnico di Milano）** | 设计学院与计算机系交叉，HCI 土壤极好 |
| **罗马第一大学（Sapienza）** | 庞大计算机系，有活跃 HCI 研究组 |
| **特伦托大学（University of Trento）** | 依托 FBK 基金会，普适计算（Ubicomp）和 HCI 世界级影响力 |

---

## 6. 申请材料优化策略

### 6.1 CV 的指标先行原则

**在 CV 首页醒目位置列出所有 Bibliometrics 指标，不要让委员会自己算：**

```
Bibliometrics (Scopus, as of YYYY-MM):
- Scopus Author ID: XXXXXXXX
- h-index: XX
- Total Citations: XXXX
- Total Publications (Scopus-indexed): XX
- Publications in last 5 years: XX
- Publications in last 10 years: XX
```

- source: [R19](https://pmc.ncbi.nlm.nih.gov/articles/PMC10435642/)

### 6.2 确保 Scopus 索引

- 登录 Scopus，确认所有会议论文（包括 CHI/CSCW）已被正确索引并归入个人 Author Profile
- 如有缺失，通过 Scopus Author Feedback Wizard 申请合并/补录
- CHI 论文通常已被 Scopus 索引（ACM DL 中的论文大多在 Scopus 中有记录）

### 6.3 研究计划

- 意大利不强调"整合计划"（unlike 法国），但需证明研究在意大利语境下的可行性
- 提及意大利国内合作者（如特伦托的 FBK、米兰理工的具体团队）是加分项

---

## 7. 决策逻辑

| 维度 | 说明 |
|------|------|
| 第一道门槛 | ASN 量化指标（算法决定，非人为）|
| 第二道门槛 | 委员会 + 量化评分（仍以指标为主）|
| 面试权重 | 相对较低（主要是确认没有硬伤）|
| 核心策略 | **指标先行**，确保 Scopus 档案完整 |

---

## 8. Sophia 特有优势/风险

### 优势
- **CHI 顶会发表**：如在 Scopus 中正确索引，引用数和 H-index 将受益
- **系统工具产出**：CollabCoder 等工具若发表于 Scopus 索引的会议/期刊，可直接计入 ASN 指标
- **意大利 HCI 生态**：特伦托/米兰理工有强 HCI 社区，可作为目标机构

### 风险
- **ASN 指标门槛**：早期职业学者（PhD + 1–2 年博后）的 H-index 可能尚未达到 01/B1 或 09/H1 的国家中位数
  - **缓解方案**：RTT 职位（助理教授级别）的指标要求低于 PA（副教授）级别；优先申请 RTT
- **HCI 会议论文认可度**：部分老派委员会可能不认可会议论文；需确保 Scopus 索引状态
- **意大利语**：非必须，但部分职位要求意大利语授课；申请前确认

---

## 引用索引

| ID | 来源 | URL | 验证状态 |
|----|------|-----|---------|
| R18 | Gennaro Vessio: ASN 申请指南 | https://www.gennarovessio.com/asn | **已验证** (2026-02-19, Layer 1): "ASN is a mandatory qualification for candidates seeking Full or Associate Professor positions" — 确认 ASN 为教职必要前提 |
| R19 | PMC: Scientific requisites for academic advancements in Italy | https://pmc.ncbi.nlm.nih.gov/articles/PMC10435642/ | **已验证** (2026-02-19, Layer 1): 确认三大指标（论文数、引用数、H-index）+ 5/10 年时间窗口；"commission consisting of 5 full professors" 评审 |
| R20 | Ca' Foscari: Working in Research (RTT) | https://www.unive.it/pag/28008/ | **已验证** (2026-02-19, Layer 1): "three-year non-renewable contract... evaluated by the University in the third year... upgraded to Associate Professor" — 确认 RTT 结构和晋升路径 |
| R21 | Academia SE: What are RTD-b/RTT positions in Italy? | https://academia.stackexchange.com/questions/46008/what-are-rtd-b-positions-in-italy | **已验证** (2026-02-19, Layer 2): 确认 2024 年 RTD-B → RTT 改革；"pre-tenure period is 3 or 6 years, according to the seniority" — 确认时长差异 |
| R22 | Università di Milano: Researcher Recruitment (RTT/RTDA) | https://www.unimi.it/en/university/work-us/researcher-recruitment | **已验证** (2026-02-19, Layer 2): 确认 RTDA（非终身轨）和 RTT（终身轨）双轨并存；PNRR 资金支持 |

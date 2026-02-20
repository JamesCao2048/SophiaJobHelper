# 新西兰 教职申请规则卡

## 元信息
- region_id: new_zealand
- last_verified: 2026-02-18
- status: draft (已验证, 2026-02-18)
- source_documents:
  - `general/research_job_rules/亚洲及中东教职招聘分析.md` Section 5.1 (L162-181)
- needs_review:
  - PBRF (Performance-Based Research Fund) 2026-27 评估周期
  - 各大学 Māori Data Sovereignty 政策具体要求
  - 奥克兰大学、维多利亚大学惠灵顿当前 HCI 职位

---

## 1. 职级术语映射

| 当地职称 | ≈ 美国等级 | 薪资范围 | 说明 | source |
|---------|-----------|---------|------|--------|
| Lecturer | Assistant Professor | NZD ~85-100k/年 (约 USD 50-65k) | 终身轨起点，Sophia 目标职级 | [R1](https://www.mbie.govt.nz/business-and-employment/employment-and-skills/employment-strategy/maori-employment-action-plan/te-tiriti-principles) |
| Senior Lecturer | 资深 Assistant Prof | NZD ~100-120k/年 | 资深讲师 | -- |
| Associate Professor | Associate Professor | NZD ~120-140k/年 | 副教授 | -- |
| Professor | Full Professor | NZD ~140k+/年 | 正教授 | -- |

**薪酬特点：**
- 6% 超级年金 (KiwiSaver)（养老金）
- 相比澳洲、香港、新加坡，薪资是该地区最低的
- 但新西兰工作生活质量极高，是追求平衡的选择
- 惠灵顿、奥克兰：生活成本高，但其他城市（基督城、达尼丁）合理

---

## 2. 关键决策人与招聘流程

### 机制类型：价值导向（双文化主义硬指标）
核心驱动力：《怀唐伊条约》(Te Tiriti o Waitangi) + PBRF 评估 ([亚洲教职分析](../general/research_job_rules/亚洲及中东教职招聘分析.md) L166)

### 决策链

| 阶段 | 决策人 | 看什么 | source |
|------|--------|--------|--------|
| 初审 | 招聘委员会 | 学术档案 + 条约声明合规性 | [R1](https://www.mbie.govt.nz/business-and-employment/employment-and-skills/employment-strategy/maori-employment-action-plan/te-tiriti-principles) |
| 面试 | 招聘委员会 | 研究实力 + 文化胜任力 (Cultural Competency) | [R2](https://www.massey.ac.nz/about/news/massey-university-sets-new-standard-for-te-tiriti-excellence/) |
| 录用批准 | Pro-Vice-Chancellor (Māori) | 文化胜任力一票否决权（高级职位）| [亚洲教职分析](../general/research_job_rules/亚洲及中东教职招聘分析.md) L181 |

### ⚠️ 隐形否决者
- **Pro-Vice-Chancellor (Māori)**：虽然可能不直接决定 CS 助理教授的录用，但在终身教职评审和高级职位招聘中，对候选人文化胜任力拥有**一票否决权** ([亚洲教职分析](../general/research_job_rules/亚洲及中东教职招聘分析.md) L181)
- 实际上，招聘委员会在短名单阶段就会评估条约理解，不符合的候选人不会进入面试

---

## 3. 申请材料要求

### 3.1 Cover Letter
- 提及对《怀唐伊条约》的理解，以及作为 Tangata Tiriti（条约伙伴）的责任
- 说明研究如何服务毛利社区或如何避免对毛利数据主权产生负面影响

### 3.2 CV
- 标准学术格式，新西兰与澳洲类似
- 包含 PBRF 相关研究产出（期刊、会议、外部经费）

### 3.3 Research Statement
- 专门开辟一节讨论"Indigenizing Computing"或"Data Sovereignty" ([亚洲教职分析](../general/research_job_rules/亚洲及中东教职招聘分析.md) L177)
- 引用毛利学者（如 Tahu Kukutai）关于 Māori Data Sovereignty 的研究，表明做了功课

### 3.4 特色材料

#### Bicultural Statement / Te Tiriti Commitment Statement
- **状态**: 取决于 JD 是否明确要求（见下方优先级判断）
- **优先级判断规则**（⚠️ 流水线必须遵守）：
  - **高优先级**：JD 明确提及 Te Tiriti / Māori / Pasifika / Bicultural / Treaty → 必须准备专门段落，三条款逐一回应
  - **中优先级**：JD 未提及上述关键词 → 在 Cover Letter 中用 1-2 句简要展示文化敏感度即可，不需大篇幅；如篇幅紧张可省略
  - 流水线 Step 2 分析时，**必须检查 JD 原文**是否包含关键词，并在 fit_report 中标注实际优先级，提示用户
- 参考来源：([亚洲教职分析](../general/research_job_rules/亚洲及中东教职招聘分析.md) L166)
- **⚠️ 错误写法**: 把它写成美国式的 Diversity Statement（多元化声明），只谈"包容少数族裔"= 直接低分出局
- **正确写法**: 必须具体引用条约的三个条款 ([亚洲教职分析](../general/research_job_rules/亚洲及中东教职招聘分析.md) L173):
  - **Kāwanatanga (Governance/Partnership)**：你如何在教学和科研管理中与毛利人建立伙伴关系？
  - **Tino Rangatiratanga (Chieftainship/Self-determination)**：你的 CS/HCI 研究如何赋能毛利数据主权（Māori Data Sovereignty）？
  - **Ōritetanga (Equity)**：你的算法或系统如何确保不加剧对毛利群体的不平等？

---

## 4. 评审重点

### 最看重
1. **Te Tiriti 理解**：**从"加分项"变为"否决项"**，所有八所公立大学强制要求
2. **PBRF 评级潜力**：影响政府对大学的研究拨款（类似英国 REF）
3. **学术质量**（期刊、会议、外部经费）

### HCI 会议论文认可度
- 新西兰 CS 社区整体认可 CHI/CSCW
- PBRF 评估体系偏向期刊，但顶会也被纳入计算
- 奥克兰大学有 HCI 研究组

### Grant 体系
- **MBIE (Ministry of Business, Innovation and Employment)**: 主要政府科研资助
- **Marsden Fund**: 新西兰版 NSERC/EPSRC，高度竞争但声望极高
- **Endeavour Fund**: 应用研究，与产业界连接
- **PBRF (Performance-Based Research Fund)**: 不是申请类经费，而是评估-分配机制

---

## 5. 条约声明写法示范

### 针对 HCI/AI 研究者的具体建议

**Tino Rangatiratanga 方向（赋能毛利数据主权）:**
```
我的人机交互研究采用参与式设计方法，这与《怀唐伊条约》
的 Tino Rangatiratanga 原则高度契合。我计划与毛利社区
合作，确保 AI 系统的训练数据和决策过程对毛利人保持透明
和可控，支持 Māori Data Sovereignty 目标。
```

**Ōritetanga 方向（算法公平性）:**
```
在我的 AI 系统评估框架中，我专门开发了针对原住民群体
的公平性指标，确保算法不加剧对毛利群体和太平洋岛民
群体的历史性不平等。
```

---

## 6. HCI 方向特殊注意

### 新西兰 HCI 生态
- **奥克兰大学 (University of Auckland)**: 有 HCI/可及性研究组
- **维多利亚大学惠灵顿 (Victoria University of Wellington)**: 较小但有社会技术研究
- **坎特伯雷大学 (University of Canterbury, UC)**: 强 HCI + 可视化
- **奥塔哥大学 (University of Otago)**: 以健康 HCI 和可及性见长

### 毛利数据主权与 HCI 的交叉
- 这是新西兰特有且高度重要的研究方向
- 如果 Sophia 的研究能与此交叉（如：AI 辅助工具如何保护原住民数据自主权），将获得极大竞争优势

---

## 7. Sophia 特有优势/风险

### 优势
- **可及性/参与式设计经验**：若有此类经历，可直接对接 Te Tiriti 承诺
- **CHI/CSCW 发表**：新西兰 CS 社区认可
- **工作生活平衡**：新西兰文化非常重视，Sophia 如果有此偏好，这是加分

### 风险
- **条约声明是真实门槛**：Sophia 来自中国/美国背景，对毛利文化可能不熟悉，需要专门研究
- **薪资偏低**：在该地区选项中薪资最低（约 USD 50-65k），与新加坡/香港差距极大
- **"色盲"Diversity Statement 会致命**：必须特别写作，不能套用美式格式
- **签证**: 工作签证，大学担保，通常顺利

---

## 引用索引

| ID | 来源 | URL | 验证状态 |
|----|------|-----|---------|
| R1 | MBIE: Te Tiriti principles | https://www.mbie.govt.nz/business-and-employment/employment-and-skills/employment-strategy/maori-employment-action-plan/te-tiriti-principles | 已验证 (2026-02-18) |
| R2 | Massey University: Te Tiriti excellence | https://www.massey.ac.nz/about/news/massey-university-sets-new-standard-for-te-tiriti-excellence/ | 已验证 (2026-02-18) |
| R3 | Karaitiana Taiuru: Treaty and Māori Ethics for AI | https://www.taiuru.co.nz/tiritiethicalguide/ | 已验证 (2026-02-18) |

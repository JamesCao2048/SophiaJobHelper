# HCI 密度策略融入 Pipeline 设计文档

> 日期：2026-02-19
> 状态：待实现
> 背景：基于 Gemini Deep Research 报告《大学教职申请：HCI研究者数量策略》，将目标院系 HCI 研究者密度作为新维度融入 overseas_pipeline 的 Step 1/2/3。

---

## 1. 核心概念：双层密度分类

目标院系与所在学院的 HCI 密度可能不同（如 Monash DSAI 系 HCI=0，但同学院 HCC 系 HCI=6+），因此采用**双层分类**：

- **target_dept**：目标系的 HCI 研究者人数
- **faculty_wide**：同校/同学院其他系的 HCI 研究者人数

### 密度等级

| level | 人数 | 含义 |
|:------|:-----|:-----|
| `none` | 0 | 无 HCI 研究者 |
| `few` | 1-3 | 小规模 HCI 集群 |
| `many` | >3 | 成熟 HCI 团队 |

### 组合策略矩阵

| target \ faculty | **none** | **few** | **many** |
|:-----------------|:---------|:--------|:---------|
| **none** | `pure_pioneer` | `pioneer_with_few_allies` | `pioneer_with_allies` |
| **few** | 罕见 | `builder` | `builder_in_rich_ecosystem` |
| **many** | 不可能 | 不可能 | `specialist` |

### 策略人设概要

| 策略 | 人设 | 核心修辞 |
|:-----|:-----|:---------|
| `pure_pioneer` | 开拓者 | 技术伪装，证明 HCI 是硬科学，CS 核心课能力，多元经费 |
| `pioneer_with_few_allies` | 开拓者+少量盟友 | 技术硬核 + 有限跨系合作 |
| `pioneer_with_allies` | 开拓者+强盟友 | 技术硬核基调 + 跨系合作叙事，论证为什么属于目标系 |
| `builder` | 建设者 | 点名现有 HCI 教授，互补定位，共建 HCI Track |
| `builder_in_rich_ecosystem` | 建设者+丰富生态 | 互补 + 提出更大规模的倡议（中心、项目） |
| `specialist` | 专家 | 愿景驱动，定义新子领域，学术领导力，跨院合作 |

---

## 2. 数据模型变更

### 2.1 faculty_data.json 新增字段

#### hci_density

```json
{
  "hci_density": {
    "target_dept": {
      "level": "none",
      "count": 0,
      "note": "DSAI 无 HCI 方向教职人员"
    },
    "faculty_wide": {
      "level": "many",
      "count": 6,
      "hci_members": ["Sharon Oviatt", "Joe Liu", "Matthew Butler"],
      "note": "HCC 系有 6 位 HCI 方向教职，含 ACM CHI Academy 成员"
    },
    "strategy": "pioneer_with_allies",
    "strategy_rationale": "目标系 DSAI 无 HCI（开拓者基调），但学院有成熟 HCC 团队（可强调跨系合作）。材料需对非 HCI 评委证明技术硬核度，同时对 HCC 教授展示互补合作潜力。"
  }
}
```

#### department_courses

```json
{
  "department_courses": [
    {
      "code": "FIT5145",
      "name": "Introduction to Data Science",
      "level": "postgrad",
      "hci_relevant": false
    },
    {
      "code": "FIT5047",
      "name": "Intelligent Systems",
      "level": "postgrad",
      "hci_relevant": false
    }
  ],
  "course_catalog_url": "https://www.monash.edu/it/dsai/courses",
  "course_catalog_scrape_date": "2026-02-19"
}
```

#### related_applications（可选）

```json
{
  "related_applications": [
    {
      "school_id": "monash_university_hcc",
      "department": "Human-Centred Computing",
      "strategy": "builder",
      "status": "step3_complete"
    }
  ]
}
```

---

## 3. 新增文件

### 3.1 `overseas_pipeline/strategies/hci_density_strategy.md`

独立策略文件，被 Step 2/3 读取。结构如下：

```
# HCI 密度策略指南

## 判定规则
- HCI 关键词表（可配置）
- 阈值定义
- 策略矩阵

## 各策略详细指南

### pure_pioneer（target=none, faculty=none）
#### Cover Letter
- 全面技术伪装
- 论证 HCI 对院系的增量价值
- 点名目标系教授的合作点（非 HCI 方向也可）
#### Research Statement
- "硬化"处理：系统架构图 > 用户引语
- 加入"方法论严谨性"段落
#### Teaching Statement
- 必须列 CS 核心课
- 从目标系 course catalog 选出能教的具体课程
- HCI 课作为"可开设的新课"
#### 经费叙事
- 强调跨学科经费源

### pioneer_with_allies（target=none, faculty=many）
#### Cover Letter
- 技术硬核基调打底
- 跨系合作段：优先目标系教授，不够补其他系
- 论证为什么属于目标系而非 HCI 系
#### Research Statement
- "硬化"语言为主
- 加 "Cross-departmental synergies" 段落
#### Teaching Statement
- CS 核心课能力 + 目标系 catalog 课程
- 提出与 HCI 系联合开课

### builder（target=few, faculty=few/many）
#### Cover Letter
- 明确提到现有 HCI 教授，阐述互补性
#### Research Statement
- 展示与现有研究的协同效应
#### Teaching Statement
- 展示课程如何拼成完整 HCI Track
- 从 catalog 找缺口课程，提出补全

### specialist（target=many, faculty=many）
#### Cover Letter
- 愿景驱动，提出新子领域
- 展示跨学院合作和学术领导力
#### Research Statement
- 理论贡献 > 系统贡献
#### Teaching Statement
- 工作室教学法、项目制学习
- 博士指导理念
- 从 catalog 选高阶/研究生课程

## 点名策略（通用规则）
1. 优先点名目标系内有研究交集的教授
2. 目标系匹配不足时，补充同校其他系 HCI 教授
3. 同校多系投递时：只点名该系 + 跨系合作对象，不提另一份申请

## 课程匹配规则
1. Step 2 须爬取目标系 course catalog（五层 fallback）
2. 从 catalog 识别 Sophia 能教的课程
3. 根据密度策略调整呈现顺序：
   - pioneer: CS 核心课在前，HCI 课在后
   - builder: 互补课程在前（填补 HCI Track 缺口）
   - specialist: 高阶/研究生 HCI 课在前
```

### 3.2 `overseas_pipeline/src/hci_density_classifier.py`

**职责**：从 faculty_data.json 自动推断 HCI 密度分类

```
输入：faculty_data.json
输出：更新 faculty_data.json 的 hci_density 字段

逻辑：
1. 加载 HCI 关键词表（内置默认 + 可配置扩展）
   默认关键词：HCI, human-computer interaction, CSCW,
   human-AI interaction, UX, accessibility, interaction design,
   user study, usability, participatory design, ...
2. 遍历 faculty，按 research_interests 匹配关键词
3. 按 department 分组统计 → target_dept count + faculty_wide count
4. 根据阈值推断 level (none=0 / few=1-3 / many=>3)
5. 根据两层 level 查矩阵 → strategy 标签
6. 写回 faculty_data.json 的 hci_density 字段
   （strategy_rationale 留空，由 agent 后续补充）
```

### 3.3 `overseas_pipeline/src/course_catalog_scraper.py`

**职责**：抓取目标系课程列表

```
输入：课程页面 URL（或从 faculty_data.json 读取 department_url）
输出：更新 faculty_data.json 的 department_courses 字段

逻辑：
1. 五层 fallback 抓取课程页面
   （Layer 1 → 1.5 Jina → 2 Tavily Extract → 2.5 Wayback → 3 Tavily Search）
2. 提取课程列表（code, name, level, description）
3. 用 HCI 关键词匹配标记 hci_relevant
4. 输出结构化 JSON
```

---

## 4. Pipeline 流程变更

### 4.1 Step 1（研究阶段）改动

在现有流程之后新增步骤，code 和 agent 分工：

```
现有步骤 1-5（不变）

新增步骤 6: HCI 密度分类（Code）
  python src/hci_density_classifier.py \
    --input output/{school}/faculty_data.json
  → 更新 faculty_data.json 的 hci_density 字段

新增步骤 7: 课程体系抓取（Code）
  python src/course_catalog_scraper.py \
    --url "{catalog_url}" \
    --output output/{school}/faculty_data.json
  → 更新 faculty_data.json 的 department_courses 字段

新增步骤 8: Agent 审查补充
  - 审查密度分类：检查边界情况（关键词未覆盖但实际 HCI 相关的教授）
  - 补充 strategy_rationale（自然语言解释）
  - 审查课程匹配：识别 Sophia 能教的课，按密度策略排序
  - 将密度判断 + 课程匹配写入 step1_summary.md，供 Sophia 异步审查
```

**Sophia 审查机制**：
- 密度判断和课程匹配写入 step1_summary.md
- Sophia 审查后如有异议，给出 comment 覆盖
- 无 comment 则默认使用自动判断
- 不阻塞流程

### 4.2 Step 2（分析阶段）改动

在 fit_report.md 中新增维度和调整建议：

```markdown
### HCI 密度策略分析 (X/10)
- 目标系 HCI 密度：{level} ({count}人)
- 学院 HCI 密度：{level} ({count}人，{dept}系)
- 推荐策略：{strategy}
- 策略要点：
  - 对目标系评委：{具体修辞建议}
  - 跨系合作叙事：{点名哪些教授}
  - 关键论证：{为什么属于目标系}
```

"各材料调整建议"中引用密度策略：

```markdown
#### Cover Letter
- 密度策略 [{strategy}]：{具体修辞建议}
- 点名建议：
  - 目标系：{教授列表}（优先）
  - 跨系补充：{教授列表}（目标系不够时）
- ⚠ 论证重点：{如为 pioneer_with_allies，需论证为什么不去 HCI 系}

#### Teaching Statement
- 密度策略 [{strategy}]：{课程呈现顺序建议}
- 目标系 catalog 匹配：
  - 能教的现有课：{课程列表}
  - 可开设新课：{课程列表}
  - 联合开课建议：{与哪个系合作}
```

### 4.3 Step 3（材料生成阶段）改动

```
1. 读取密度策略文件 strategies/hci_density_strategy.md
2. 根据 fit_report 中的密度策略建议生成材料
3. 各材料按对应策略调整修辞和结构：
   - Cover Letter: 点名策略（优先目标系 → 补充其他系）
   - Research Statement: 硬化/愿景化程度
   - Teaching Statement: 引用具体课程编号和名称
4. 如存在 related_applications：
   - 读取对方的 fit_report.md
   - 在 notes.md 中生成"同校多系一致性检查"段落
```

---

## 5. 同校多系投递支持

### 设计原则

- **假设委员会不互通材料，但可能非正式沟通**
- **针对每个系深度定制，但核心人设一致**
- **轻量支持：标记 + 一致性提醒，不阻塞流程**

### 数据标记

通过 `related_applications` 字段在 faculty_data.json 中标记同校其他投递。

### 一致性检查（Step 3 自动）

当检测到 related_applications 时，在 notes.md 的"给 Sophia 的审核重点"中自动生成：

```markdown
## 同校多系一致性检查
- 本校另一份申请：{department}（{strategy} 策略）
- 核心叙事一致性：✅/⚠ {描述}
- 侧重点差异：{本系版本特点} / {另一系版本特点}
- ⚠ 注意：{具体提醒事项}
```

### 策略约束

| 维度 | 约束 |
|:-----|:-----|
| 核心叙事 | 两份材料必须一致（如"human-AI collaboration 方法论创新"） |
| Research Statement | 同一套项目，不同侧面强调 |
| Cover Letter | 各自论证为什么适合该系，不提另一份申请 |
| Teaching Statement | 各自引用该系 course catalog |
| 点名策略 | 各份材料只点名该系 + 跨系合作对象 |

---

## 6. 其他同步更新

### 6.1 CLAUDE.md 网页抓取规则

将"三层 fallback 策略"更新为**五层 fallback 策略**：

1. **Layer 1**: curl + browser UA
2. **Layer 1.5**: Jina Reader（JS 渲染，免费无 key）
3. **Layer 2**: Tavily Extract API
4. **Layer 2.5**: Wayback Machine（历史快照，免费）
5. **Layer 3**: Tavily Search API

### 6.2 参考资源

- 策略报告原文：`general/research_job_rules/大学教职申请：HCI研究者数量策略.md`
- web-fetch-fallback skill：`~/.claude/skills/web-fetch-fallback/SKILL.md`

---

## 7. 实现优先级

| 优先级 | 任务 | 依赖 |
|:-------|:-----|:-----|
| P0 | 创建 `strategies/hci_density_strategy.md` | 无 |
| P0 | 更新 CLAUDE.md Step 1/2/3 流程 + 五层 fallback | 无 |
| P1 | 实现 `src/hci_density_classifier.py` | 策略文件 |
| P1 | 实现 `src/course_catalog_scraper.py` | 无 |
| P2 | 同校多系 related_applications 支持 | P0/P1 |

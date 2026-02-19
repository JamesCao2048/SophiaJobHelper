# Overseas Pipeline -- 海外教职申请流水线设计文档

> 日期: 2026-02-18
> 状态: Draft
> 作者: James + Claude Code brainstorm

---

## 一、背景与目标

### 问题
Sophia 正在全球投递教职（HCI / Human-AI Collaboration 方向）。美国市场行情差，正转向澳洲、加拿大、欧洲、中东、港新日韩。当前最大瓶颈是 **Cover Letter 及申请材料的个性化**，每个学校需要：
- 研究该校 faculty 的方向，找到 research overlap
- 根据不同地区的评审文化调整材料写法
- 每所学校耗时 1-2 小时，而她需要以每周 3-5 所的节奏投递

### 目标
构建一个 Claude Code 驱动的 4 步流水线，将每所学校的申请材料准备从 1-2 小时降至 15-20 分钟（生成初稿 + Sophia 审核修改）。

### 与现有工具的关系
```
faculty_monitor/       → Step 0: 发现新职位（已有，迁入本仓库）
job_hunting/           → 国内教职流水线（已有，继续维护）
overseas_pipeline/     → 海外教职流水线（本文档设计，新建）
job_filling/           → 表单自动填写（已有，下游使用）
google-sheets-sync/    → 申请状态追踪（已有，数据源）
overleaf-projects/     → 申请材料源文件（已有，被读取和参考）
```

---

## 二、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    Knowledge Layer                       │
│  region_profiles/        区域规则卡（可验证、可更新）       │
│  ├── uk.md              每张卡带 source links             │
│  ├── australia.md       + last_verified 日期              │
│  ├── dach.md            + needs_review 列表               │
│  ├── canada.md          当 Claude Code 发现规则过时时      │
│  ├── hk_singapore.md    → 自动追加 needs_review           │
│  ├── middle_east.md     → 空闲时验证并更新                │
│  ├── japan_korea.md                                      │
│  └── new_zealand.md                                      │
└─────────────────────────────────────────────────────────┘
         ↑ 被 Step 2, 3 引用

Step 0 [Discovery]     faculty_monitor/ (独立子模块，定期跑)
        ↓ 新职位 → Google Sheet
        ↓ Sophia 从列表中选择要分析的学校
Step 1 [Research]      faculty_scraper.py → faculty_data.json
        ↓
Step 2 [Fit Analysis]  Claude Code + 区域规则卡 → fit_report.md
        ↓
Step 3 [Materials]     Claude Code + fit_report → 全套材料初稿 + 修改说明
        ↓
[Existing] job_filling → 表单自动填写 → 提交
```

### 设计原则

1. **Claude Code 为主引擎**：Python 只做爬取/数据获取，Claude Code 做所有分析、匹配、写作。零额外 API 费用，跟 job_filling 模式一致。
2. **全链路可溯源**：每个产出物附带 sources 文件，严格标注参考的原始 URL、本地文件路径。
3. **所有材料生成初稿**：不只是修改建议，而是生成完整初稿 + 逐段修改说明（diff + 原因），Sophia 审核即可。
4. **区域知识可迭代**：规则卡从 DeepResearch 文档蒸馏而来，通过 needs_review 机制持续验证更新。

---

## 三、Knowledge Layer: 区域规则卡

### 来源
从以下 DeepResearch 文档蒸馏：
- `general/research_job_rules/海外教职申请机制与策略.md`（英/澳/DACH/荷/加）
- `general/research_job_rules/亚洲及中东教职招聘分析.md`（中/港/新/日/韩/中东/澳门/新西兰/马来）

### 每张卡的统一结构

```markdown
# {地区} 教职申请规则卡

## 元信息
- last_verified: YYYY-MM-DD
- sources: [URL1, URL2, ...]
- needs_review: []

## 职级术语映射
| 当地职称 | ≈ 美国等级 | 说明 |

## 关键决策人
- 初筛由谁做（HR / 系主任 / 委员会）
- 短名单由谁定
- 最终决策权在谁手上
- 外部评审的角色（如有）

## 申请材料要求
- Cover Letter 格式和写法（如英国逐条回应 Person Specification）
- CV 格式差异（如德国含照片、婚姻状况）
- Research Statement 侧重点
- Teaching Statement 侧重点
- 额外必须材料（如德国 Lehrkonzept、澳洲 Selection Criteria Response）

## 评审重点
- 评审者最看重什么
- HCI 会议论文的认可度
- Grant/资金期望（如英国 EPSRC、澳洲 ARC DECRA）
- Impact/社会影响的权重

## Cover Letter 策略
- 开头定调建议
- Faculty 提及方式
- 禁忌

## Sophia 特有优势/风险
- HCI + AI 交叉在该地区的定位
- CHI/TOCHI 在该评价体系下的认可度
- 开源工具部署经历的价值
```

### 更新机制
1. 初始版本：从 DeepResearch 文档蒸馏生成
2. 使用中发现不一致：Claude Code 自动追加 `needs_review` 条目
3. 定期验证：运行 "review region cards" workflow，Claude Code 逐条检查，查原始链接或搜新信息
4. 新地区：首次遇到未覆盖的地区时，Claude Code 搜索信息生成新规则卡

---

## 四、Step 0: Discovery（faculty_monitor/）

### 现状
`faculty_monitor.py` 已覆盖 7 个平台：jobs.ac.uk、HigherEdJobs、CRA、EURAXESS、Chronicle、THE Unijobs、Inside Higher Ed。偏北美，覆盖率约 50-60%。

### 迁入方案
- 从 `faculty-application_script/` 迁入为 `faculty_monitor/`
- 作为独立子模块维护，有自己的 CLAUDE.md
- 添加 `issues.md` 日志：使用中发现的问题（漏掉职位、某平台挂了、缺少地区源）随手记一条，积累后集中修

### 已知待改进项
- 缺少澳洲/新西兰源（SEEK Academic、universities.com.au）
- 缺少亚洲源（港/新/日/韩招聘平台）
- 缺少中东源
- AJO 和 SIGCHI Jobs 标注"手动"但是 HCI 最重要来源
- 关键词匹配精度有限

### 与流水线的对接
输出新职位 → 写入 Google Sheet 或 Excel → Sophia 从列表中选择学校 → 进入 Step 1

---

## 五、Step 1: Research（faculty_scraper.py）

### 触发方式
用户在 Claude Code 中说：**"研究 {学校名}"**

### 输入
- 学校名 + 院系名（或职位 URL，从中推断院系）
- Sophia 的 Research Statement + 代表作（用于 overlap 分析）

### 爬取策略

两层策略：
1. **Layer 1: Firecrawl / Jina Reader API** → 把院系 faculty 页面转成 markdown → Claude Code 从中提取结构化信息
2. **Layer 2: 兜底手动模式** → 如果反爬或结构太复杂 → Claude Code 提示用户手动 copy-paste faculty 列表

对于大院系（50+ faculty）：先爬 research group/cluster 页面，快速筛选相关组，再深入爬相关 faculty。

### 输出

`output/{school}/faculty_data.json`:
```json
{
  "school": "University of Melbourne",
  "department": "School of Computing and Information Systems",
  "department_url": "https://...",
  "region": "australia",
  "research_focus": ["AI", "HCI", "data science", "cybersecurity"],
  "faculty": [
    {
      "name": "Prof. Jane Smith",
      "title": "Professor",
      "research_interests": ["human-AI interaction", "CSCW", "social computing"],
      "homepage": "https://...",
      "google_scholar": "https://scholar.google.com/citations?user=xxxxx",
      "overlap_with_sophia": "high",
      "overlap_reason": "Both work on human-AI collaboration for data analysis",
      "overlapping_papers": [
        {
          "title": "Designing AI-Assisted Qualitative Coding Tools",
          "venue": "CHI 2025",
          "year": 2025,
          "url": "https://doi.org/10.1145/...",
          "local_path": "output/melbourne/papers/smith_chi2025.pdf",
          "relevance": "Direct overlap with CollabCoder/CoAIcoder line"
        }
      ]
    }
  ],
  "scrape_date": "2026-02-18",
  "scrape_method": "firecrawl"
}
```

关键点：
- `overlap_with_sophia` 由 Claude Code 分析填入
- 只对 overlap=high 的 3-5 人下载论文，每人 ≤5 篇最相关的
- 论文存在 `output/{school}/papers/`

`output/{school}/faculty_data.sources.md`: 标注每位 faculty 信息的来源 URL。

---

## 六、Step 2: Fit Analysis（fit_report.md）

### 触发方式
用户在 Claude Code 中说：**"分析 {学校名}"**（前提：Step 1 已完成）

### 输入
- `output/{school}/faculty_data.json`
- `output/{school}/papers/*.pdf`（overlap faculty 的论文）
- `region_profiles/{region}.md`（区域规则卡）
- Sophia 全套材料：Research Statement, CV, Teaching Statement, Impact Statement, 代表作
- 职位 JD 原文（从链接爬取）

### Claude Code 分析流程
1. 读取区域规则卡 → 了解该地区评审重点和决策人
2. 读取 faculty_data → 识别 research cluster 和 collaboration 机会
3. 读取下载的论文 → 找到具体研究结合点（引用具体章节）
4. 读取职位 JD → 提取 selection criteria 和关键要求
5. 综合评估 fit score

### 输出

`output/{school}/fit_report.md`:
```markdown
# {学校} -- 匹配分析报告

## 基本信息
- 院系 / 地区 / 职级 / Deadline / 职位链接

## Fit Score: X/10

## 匹配维度分析

### 研究方向匹配 (X/10)
- 院系有哪些相关研究组
- 高 overlap faculty 的具体结合点（引用其论文具体章节）

### 区域适配 (X/10)
- 材料格式要求是否有特殊调整
- HCI 会议论文认可度
- Grant 期望

### 关键决策人分析（材料写给谁看）
- 初筛: 谁做（HR / 系主任 / 委员会），看什么
- 短名单: 谁定，看什么
- 面试: panel 构成
- 外部评审: 如有，可能是谁

### 各材料调整建议

#### Cover Letter
- 格式要求（如逐条回应 Selection Criteria）
- Framing 建议
- 必须 name-drop 的 faculty + 结合点叙述
- 区域适配要点

#### Research Statement
- 当前版本可用度
- 需要调整的段落及方向（如加入当地 grant 计划）
- 需要强调/弱化的内容

#### Teaching Statement
- 当前版本可用度
- 需补充的学校课程名称
- 需要调整的表述

#### Impact / Diversity Statement
- 是否需要提交
- 当地语境下的表述调整（如新西兰 Treaty of Waitangi）

#### 特色材料（该地区/学校特有）
- 是否需要额外材料（如澳洲 Selection Criteria Response）
- 材料框架和关键点

### 风险提示
- 该职位/学校的潜在不利因素
- 需要特别注意的点

### 投递建议
- 是否建议投递
- 如投递，优先级（my favorite / worth trying / low priority）
```

`output/{school}/fit_report.sources.md`: 严格标注所有参考资料（区域规则卡、faculty 数据、论文、JD 原文、Sophia 材料）的链接。

---

## 七、Step 3: Application Materials Customization

### 触发方式
用户在 Claude Code 中说：**"生成材料 {学校名}"**（前提：Step 2 已完成）

### 输入
- `output/{school}/fit_report.md` 的"各材料调整建议"
- 现有材料（从 `overleaf-projects/` 读取）
- 区域规则卡
- Cover Letter LaTeX 模板

### 输出

对每份材料生成两个文件：

1. **完整初稿**：`output/{school}/materials/{material}.tex`
   - Cover Letter: 从模板生成全新版本
   - Research/Teaching/Impact Statement: 基于现有版本修改后的完整初稿
   - 特色材料（如 Selection Criteria Response）: 全新生成

2. **修改说明**：`output/{school}/materials/{material}.notes.md`
   ```markdown
   # {材料名} 修改说明 -- {学校}

   ## 生成日期

   ## 总体策略
   本材料采用什么写法，为什么，总体思路是什么。

   ## 参考资料清单
   | # | 类型 | 资料 | 链接 |
   |---|------|------|------|
   | R1 | 区域规则卡 | ... | region_profiles/australia.md |
   | R2 | Fit Report | ... | output/{school}/fit_report.md |
   | R3 | Faculty 论文 | ... | output/{school}/papers/xxx.pdf |
   | R4 | Sophia 材料 | ... | overleaf-projects/... |
   | R5 | 学校信息 | ... | https://... |
   ...

   ## 逐段修改说明

   ### 1. {段落标识}
   **原文：**
   > ...

   **修改为：**
   > ...

   **原因：**
   - 引用 [R1: 具体章节] ...
   - 引用 [R3: 论文 Section X] ...

   ### 2. {段落标识}
   ...
   ```

### 快捷命令

**"一键分析 {学校}"**：依次执行 Step 1 → Step 2 → Step 3，中间不暂停。适用于已确认要投的学校。

---

## 八、完整目录结构

```
SophiaJobHelper/
├── job_hunting/              # [已有] 国内教职流水线
├── job_filling/              # [已有] 表单自动填写
├── faculty_monitor/          # [迁入] 全球职位监控
│   ├── faculty_monitor.py
│   ├── .seen_jobs.json
│   ├── issues.md             # 问题日志
│   └── CLAUDE.md
├── google-sheets-sync/       # [已有] Google Sheet 同步
├── overleaf-projects/        # [已有] 申请材料源文件
├── overseas_pipeline/         # [新建] 海外申请流水线
│   ├── CLAUDE.md              # Workflow 定义
│   ├── src/
│   │   └── faculty_scraper.py
│   ├── region_profiles/       # 区域规则卡
│   │   ├── uk.md
│   │   ├── australia.md
│   │   ├── dach.md
│   │   ├── canada.md
│   │   ├── hk_singapore.md
│   │   ├── middle_east.md
│   │   ├── japan_korea.md
│   │   └── new_zealand.md
│   ├── templates/
│   │   └── cover_letter/      # LaTeX 模板
│   └── output/                # 每个学校的产出物（.gitignore）
│       └── {school}/
│           ├── faculty_data.json
│           ├── faculty_data.sources.md
│           ├── fit_report.md
│           ├── fit_report.sources.md
│           ├── papers/
│           └── materials/
│               ├── cover_letter.tex
│               ├── cover_letter.notes.md
│               ├── research_statement.tex
│               ├── research_statement.notes.md
│               └── ...
└── general/                   # [已有] 规划文档
    ├── plans/
    └── research_job_rules/    # DeepResearch 原始文档
```

---

## 九、实施优先级

### Phase 1（本周）
1. 迁移 `faculty_monitor.py` 到本仓库
2. 创建 `overseas_pipeline/` 目录结构
3. 从 DeepResearch 文档蒸馏 2-3 张最急需的区域规则卡（澳洲、英国、港新）
4. 搭建 `faculty_scraper.py` 基础版（Firecrawl/Jina Reader）
5. 写 `CLAUDE.md` workflow 定义

### Phase 2（第 2 周）
6. 用一所真实学校端到端测试全流程（建议选一所澳洲学校）
7. 根据测试结果迭代规则卡和 scraper
8. 补全剩余区域规则卡

### Phase 3（第 3 周+）
9. 完善 faculty_monitor 覆盖率（加澳洲/亚洲源）
10. 沉淀可复用模式，为 Academic Career Agent 产品化做准备

---

## 十、与第二职业计划的关系

| 给 Sophia 的功能 | 通用化后的产品 |
|------------------|---------------|
| faculty_scraper.py | → 通用学术院系研究工具 |
| region_profiles/ | → 全球教职申请知识库 |
| fit_report 生成 | → Academic Job Matching Service |
| 材料定制 + notes | → AI-Powered Application Suite |
| faculty_monitor | → Academic Job Aggregator |

使用过程中的数据（规则有效性、改动接受率）= paper 素材。

# 海外教职申请流水线 — 使用说明

> **目标**：每所学校的申请材料准备从 1-2 小时降至 15-20 分钟（AI 生成初稿 + 你审核修改）

---

## 目录

1. [项目是什么](#项目是什么)
2. [整体工作流程](#整体工作流程)
3. [文件目录结构](#文件目录结构)
4. [如何启动每一步](#如何启动每一步)
5. [每步完成后去哪里找产出](#每步完成后去哪里找产出)
6. [如何审阅产出文件](#如何审阅产出文件)
7. [如何给出调整意见](#如何给出调整意见)
8. [常见问题](#常见问题)

> **材料样式 / 模板相关内容** → 见 **[style.md](style.md)**

---

## 项目是什么

这是一个由 Claude Code（AI 助手）驱动的**申请材料自动化准备工具**。你只需要提供学校名称和职位链接，AI 会自动：

- 爬取该院系所有教授的研究方向
- 判断哪些教授与你的研究最接近
- 下载相关论文
- 分析职位要求与你的匹配程度
- 生成定制化的 Cover Letter、Research Statement、Teaching Statement 等材料初稿

整个过程你**不需要写任何代码**，只需要用自然语言告诉 Claude Code 做什么。

> **与表单填写工具的关系**：本模块（`overseas_pipeline`）负责**准备**定制化申请材料，配套的 `job_filling/` 工具负责**提交**申请（自动填写学校在线申请系统的网页表单）。完整申请流程：先用本模块生成材料 → 再用 `job_filling` 填写网页表单。

---

## 整体工作流程

```
你提供：学校名 + 职位链接
         ↓
[Step 1] 研究学校
  └→ AI 爬取院系教授信息，分析研究重叠，下载论文
         ↓
[Step 2] 分析匹配度
  └→ AI 读取职位 JD，与你的材料对比，生成 fit_report
         ↓
[Step 3] 生成材料
  └→ AI 生成 Cover Letter / Research Statement / Teaching Statement 等
         ↓
你审阅 .notes.md 文件，本地修改 .tex 文件并编译 PDF，提交申请
```

每步都可以单独运行，也可以一次性运行"一键分析"。

---

## 文件目录结构

### 本模块（overseas_pipeline/）

```
overseas_pipeline/
├── README.md                    ← 本文件
├── CLAUDE.md                    ← AI 指令（不需要手动修改）
├── workflows/                   ← 各步骤详细流程（AI 自动读取）
│   ├── step1_research.md        ← Step 1 总入口（Phase 概览 + 分派）
│   ├── step1/                   ← Step 1 子步骤（AI 按 Phase 按需读取）
│   │   ├── step1a_setup.md          ← Phase A: 初始化与数据准备
│   │   ├── step1b_scrape_analyze.md ← Phase B: 爬取与分析
│   │   ├── step1c_profiling.md      ← Phase C: 分类与画像
│   │   └── step1d_regional_signals.md ← Phase D: 地区信号（NZ/AU）
│   ├── step2_analysis.md        ← Step 2 执行规范
│   ├── step3_materials.md       ← Step 3 执行规范
│   └── references/              ← 参考文件（JSON schema、模板、检查清单）
│       ├── faculty_data_schema.md     ← faculty_data.json 完整格式
│       ├── data_quality_spec.md       ← 数据质量分级标准
│       ├── regional_signal_schemas.md ← Te Tiriti / AU Indigenous JSON 格式
│       ├── fit_report_template.md     ← fit_report.md 完整模板
│       ├── step2_message_templates.md ← 页数偏差 / 规则冲突对话模板
│       ├── humanizer_checklist.md     ← Humanizer 去 AI 化检查清单
│       ├── pdf_tuning_guide.md        ← PDF 排版微调策略
│       └── notes_and_output_spec.md   ← notes.md 格式 + 产出物清单
├── src/                         ← 爬取工具代码（AI 自动调用）
│   ├── page_scraper.py             ← 爬取院系页面 & JD 原文
│   ├── faculty_scraper.py          ← 教授个人信息抓取 & 论文下载
│   ├── web_fetch_utils.py          ← 五层 fallback 通用抓取工具
│   ├── paper_metadata.py           ← 论文元数据提取（DBLP / Semantic Scholar）
│   ├── course_catalog_scraper.py
│   └── hci_density_classifier.py
├── templates/                   ← LaTeX 格式模板（Caramel 配色，Step 3 使用）
│   ├── sophia-statement.sty         ← 共享样式包（颜色/字体/heading 格式）
│   ├── cover_letter/                ← Cover Letter 模板（OUCletter.cls + main_template.tex）
│   ├── research_statement/          ← Research Statement 模板（4 页）
│   ├── teaching_statement/          ← Teaching Statement 模板（2 页）
│   ├── diversity_statement/         ← Diversity Statement 模板（1 页默认）
│   ├── selection_criteria_response/ ← Selection Criteria 模板（澳洲用）
│   └── knowledge/
│       └── department_rule_card_template.md  ← 院系规则卡模板
├── strategies/
│   ├── hci_density_strategy.md  ← HCI 密度策略（AI 读取）
│   ├── dept_type_strategy.md    ← 院系类型四维策略（AI 读取）
│   ├── cv_strategy.md           ← CV 变体选择说明（AI 读取）
│   ├── nz_te_tiriti_strategy.md ← 新西兰 Te Tiriti 融入策略（AI 读取）
│   └── au_indigenous_strategy.md← 澳洲 Indigenous 融入策略（AI 读取）
└── output/                      ← ★ 所有产出物在这里（见下方）
    ├── university_of_auckland/
    │   └── cs/                  ← cs = Computer Science 院系
    ├── monash_university/
    │   └── dsai/                ← dsai = Data Science & AI 院系
    └── {school_id}/
        └── {dept_id}/
```

### LaTeX 资源分工

Step 3 生成材料时使用两类 LaTeX 资源，功能完全不同：

| 目录 | 作用 |
|------|------|
| `templates/` | **格式**：视觉样式（配色、字体、标题格式）|
| `overleaf-projects/Faculty Position/` | **内容**：Sophia 真实的申请材料文本 |

详细说明和样式修改方法见 **[style.md](style.md)**。

> **注意**：`region_knowledge/` 在项目根目录，路径为 `../region_knowledge/`，AI 会自动访问。

**你现有材料的路径：**
```
overseas_pipeline/materials/
├── cv_latest.md            ← 简历（Markdown 格式）
├── Research_Statement.md   ← 研究陈述
├── Teaching_Statement.md   ← 教学陈述
├── Impact_Statement.md     ← 影响力陈述
└── publication*.md         ← 发表论文列表
```

---

## 启动 Claude Code

**必须从 `overseas_pipeline/` 目录内启动 Claude Code**（确保相对路径正确，无需每次确认权限）：

```bash
# 在终端中进入 overseas_pipeline 目录
cd /path/to/SophiaJobHelper/overseas_pipeline

# 启动 Claude Code（跳过权限确认弹窗）
claude --dangerously-skip-permissions
```

启动后，Claude Code 的工作目录固定在 `overseas_pipeline/`，所有文件路径都基于此目录解析。

> **注意**：`--dangerously-skip-permissions` 允许 AI 自动执行文件读写、运行脚本等操作，无需逐一确认。这是本流水线的设计前提，在受信任的本地环境中使用是安全的。

### 推荐模型选择

不同步骤对模型的需求不同，合理切换可节省大量 token 费用：

| 步骤 | 推荐模型 | 原因 |
|------|----------|------|
| **Step 1** 院系研究 | **Sonnet** | 大量网页爬取，重复性任务，token 消耗大，Sonnet 性价比更高 |
| **Step 2** 匹配分析 | **Opus** | 需要深度推理，综合判断 JD 与你的材料的匹配度 |
| **Step 3** 材料生成 | **Opus** | 写作质量要求高，Opus 生成的英文更地道、论证更严密 |

**切换方法**：在 Claude Code 聊天界面输入 `/model`，然后从弹出的列表中选择目标模型。

---

## 如何启动每一步

打开 Claude Code，用**中文自然语言**说出你想做的事，不需要记忆精确命令。AI 会根据语义推断你要执行哪一步。

### Step 1：研究学校

**你可以这么说（任选其一）：**
```
研究一下 University of Auckland，链接：https://...
挖一下这个学校的院系 https://...
去调研一下 XXX 大学
启动 Auckland 的 Step 1
扫一下这个职位链接
```

**必须同时提供** 院系主页或职位 URL（AI 无法猜测）。

AI 完成后会展示教授重叠分析、课程匹配、数据质量评估摘要，等待你确认再继续。

---

### Step 2：分析匹配度

**Step 1 完成后，你可以这么说：**
```
分析一下 Auckland 的匹配度
继续（AI 会推断：继续 Auckland 的 Step 2）
值不值得投 Auckland？
下一步
打个分吧
```

AI 会生成 fit_report，包含综合评分和每份材料的定制建议。

---

### Step 3：生成材料

**Step 2 完成后，你可以这么说：**
```
给 Auckland 生成材料
出稿
继续，写材料
做 Cover Letter
下一步
```

AI 生成所有材料后，会逐一列出每份文件的位置和审阅重点。

---

### 一键全流程

```
一键分析 XXX 大学，链接：{URL}
从头开始做 Auckland
全部做一遍
```

AI 依次执行 Step 1 → Step 2 → Step 3。遇到需要你判断的问题（规则冲突、数据质量不足等）会自动暂停。

---

### 其他自然语言

你也可以直接描述目的，AI 会推断对应操作：

| 你说的 | AI 理解为 |
|--------|----------|
| "看看 Auckland 现在到哪一步了" | 列出已有产出文件 |
| "继续" | 当前学校 + 上一步后的下一步 |
| "Auckland 的教授列表给我看看" | 展示 Step 1 的 faculty 分析结果 |
| "重新分析一下，我觉得匹配度评分不对" | 重跑 Step 2 并询问具体异议 |

---

## 每步完成后去哪里找产出

所有产出文件都在 `output/{school_id}/{dept_id}/` 目录下。

**学校 ID 格式**：学校英文名的小写下划线格式，例如：
- University of Auckland → `university_of_auckland`
- Monash University → `monash_university`

**院系 ID 格式**：院系英文缩写，例如：
- School of Computer Science → `cs`
- Department of Data Science and AI → `dsai`

### Step 1 产出文件

```
output/{school_id}/{dept_id}/
├── step1_summary.md        ★ 主要阅读这个：研究摘要，包含教授重叠分析、课程匹配
├── faculty_data.json        AI 内部使用的结构化数据（一般不需要直接阅读）
├── faculty_data.sources.md  每位教授信息的来源 URL（可以核实）
├── data_quality.json        数据质量评估（high/medium/low）
├── knowledge/{dept_id}.md   院系规则卡（AI 研究发现的该院系特点）
└── raw/
    ├── faculty_page.md      爬取的院系页面原始内容
    ├── jd_*.md              爬取的职位 JD 原始内容
    └── course_catalog_raw.md 爬取的课程列表原始内容
└── papers/                  下载的高匹配教授论文 PDF
```

**你只需要读：** `step1_summary.md`

---

### Step 2 产出文件

```
output/{school_id}/{dept_id}/
├── step2_summary.md        ★ 主要阅读这个：匹配分析摘要，风险提示
├── fit_report.md           ★ 详细匹配报告（每份材料的具体调整建议）
└── fit_report.sources.md   分析依据的来源（规则卡条目、JD 原文）
```

**你主要读：** `fit_report.md`（它包含 Fit Score、各维度评分、每份材料的定制建议）

---

### Step 3 产出文件

```
output/{school_id}/{dept_id}/
├── step3_summary.md        ★ 主要阅读这个：材料生成摘要，告诉你哪些已生成
└── materials/
    ├── Cover Letter/
    │   ├── main.tex         ← 生成的 LaTeX 源文件（用于编译 PDF）
    │   ├── main.pdf         ← 编译好的 PDF（直接用于投递）
    │   └── cover_letter.notes.md  ★ 审阅重点：修改说明
    ├── Research Statement/
    │   ├── main.tex / main.pdf
    │   └── research_statement.notes.md  ★ 审阅重点
    ├── Teaching Statement/
    │   ├── Teaching_Statement.tex / .pdf
    │   └── teaching_statement.notes.md  ★ 审阅重点
    ├── Diversity Statement/        （JD 要求时才有）
    │   ├── main.tex / main.pdf
    │   └── diversity_statement.notes.md
    ├── CV/                         （需要定制时才有）
    │   ├── main.tex / main.pdf
    │   └── cv.notes.md
    └── Selection Criteria Response/ （仅澳洲职位）
        ├── selection_criteria_response.tex / .pdf
        └── selection_criteria_response.notes.md
```

---

## 如何审阅产出文件

### 审阅顺序建议

**Step 1 完成后：**
1. 打开 `step1_summary.md`，检查：
   - 识别的教授列表是否准确？有没有遗漏重要教授？
   - High Overlap 的教授判断是否合理？
   - 课程匹配列表是否实际？

**Step 2 完成后：**
1. 打开 `fit_report.md`，重点关注：
   - **Fit Score** 是否与你的直觉一致？
   - **规则冲突记录**：是否有地区规则与 JD 要求不一致的地方？
   - **各材料调整建议**：AI 给每份材料的定制建议是否合理？
   - **风险提示**：有无需要特别注意的申请风险？
   - **投递建议**：是否建议投递，优先级如何？

**Step 3 完成后：**
1. 打开每份材料的 `.notes.md` 文件（如 `cover_letter.notes.md`），这是**专门为你写的审阅说明**，包含：
   - **总体策略**：这份材料的整体定制方向
   - **逐段修改说明**：每段改了什么、为什么改
   - **给 Sophia 的审核重点**：3-5 条具体需要你检查的问题

2. 打开对应的 PDF 文件，阅读完整材料

3. 如需修改，用本地文本编辑器（VS Code、Cursor 等）打开对应的 `.tex` 文件编辑，编辑后重新编译 PDF

### `.notes.md` 文件阅读指南

每份材料的 `.notes.md` 文件结构如下：

```
# {材料名} 修改说明 -- {学校}

## 总体策略          ← 先读这里，理解整体定制思路

## 参考资料清单      ← 可追溯 AI 依据的具体来源

## 逐段修改说明      ← 了解每段改动，判断是否认同
  ### 1. 开头段 [NEW]
  原文：（无对应原文）
  修改为：> ...
  原因：...

## 给 Sophia 的审核重点  ← ★ 重点看这里，这是需要你判断的部分
  1. 第2段提到了 Danielle Lottridge 的研究...是否准确？
  2. Cover Letter 结尾是否体现了对 NZ 的兴趣...
```

---

## 如何给出调整意见

### 方式一：直接在 Claude Code 中口述修改（推荐）

审阅完 `.notes.md` 和 PDF 后，直接在 Claude Code 聊天窗口描述你的修改意见：

```
Cover Letter 第2段提到的合作方向不太准确，
我和 Lottridge 的合作点应该强调工具互补，
而不是方法论相同，请修改。
```

AI 会直接修改 `.tex` 文件并重新编译 PDF。

### 方式二：本地直接编辑 .tex 文件

如果你熟悉 LaTeX，可以用本地编辑器（VS Code、Cursor、TeXShop 等）直接打开 `.tex` 文件编辑，然后在终端运行编译命令生成 PDF。

**LaTeX 编译指令：**

```bash
# 进入对应材料目录（以 Cover Letter 为例）
cd output/university_of_auckland/cs/materials/Cover\ Letter/

# latexmk 自动处理（推荐，自动处理参考文献和多轮编译）
latexmk -pdf main.tex

# 编译完成后清理中间文件（可选）
latexmk -c
```

> **安装 LaTeX**：macOS 推荐 `brew install --cask mactex-no-gui`（命令行版，含 `pdflatex` / `latexmk`，约 4 GB）；或完整版 [MacTeX](https://www.tug.org/mactex/)。

### 意见反馈格式建议

| 类型 | 示例 |
|------|------|
| 内容不准确 | "第3段提到我在 CMU 发表了3篇 CHI，实际上是2篇，请更正" |
| 策略调整 | "我希望更突出 Data Science 方向，减少 HCI 的比重" |
| 语气调整 | "结尾感觉太生硬，能不能更自然一些？" |
| 增加内容 | "请在教学部分加入我在 JHU 担任 TA 的经历" |
| 删除内容 | "Research Statement 里提到的那个未发表项目先删掉" |

---

## 知识沉淀：让 AI 越用越聪明

**每次你纠正 AI，它可能在问你：这条经验要不要写进知识库？**

知识库分两类：
- **地区规则库** (`../region_knowledge/regions/`)：记录各国/地区的申请惯例（材料页数、面试流程、合同类型等）
- **学校规则卡** (`../region_knowledge/schools/`)：记录特定学校的特殊信息
- **流程文档** (`workflows/`)：记录这个流水线本身的操作步骤

### 什么情况下 AI 会主动询问你

当你的反馈涉及**规律性知识**（而不只是当前这所学校的个别情况）时，AI 会问：

> 我注意到你的反馈可能对其他学校也有参考价值：
> 【发现】新西兰 Lecturer 职位的 Cover Letter 通常比 2 页要短
> 【建议更新】`region_knowledge/regions/new_zealand.md`
>
> 需要将这条写入知识库吗？（Y 更新 / N 仅用于本次）

### 你也可以主动触发知识回写

直接告诉 AI：
```
把这条记录到新西兰规则卡里
这个发现对其他学校也适用，帮我存下来
把这条写进 workflow
```

AI 会在修改前告诉你具体改什么、改在哪里，由你最终确认。

---

## 常见问题

**Q: output/ 目录里的文件在 git 里看不到，这正常吗？**

A: 正常。`output/` 目录被 `.gitignore` 排除，不会提交到 git。这是保护你申请材料隐私的设计。文件都在本地，可以在 Finder 里直接找到。

---

**Q: AI 在 Step 1 爬取失败怎么办？**

A: AI 会先尝试5种不同的爬取方式，如果全部失败会告诉你，并请你手动复制粘贴院系页面内容。直接在浏览器打开院系页面，Ctrl+A 全选，Ctrl+C 复制，然后粘贴到 Claude Code 聊天窗口即可。

---

**Q: AI 发现"规则冲突"是什么意思？**

A: 地区申请规则库（比如新西兰的规定）和这所学校 JD 的具体要求有时会有差异（比如材料页数限制不同）。AI 会暂停并显示具体冲突内容，你选择 A/B/C 告诉 AI 怎么处理即可：
- **A**：以这所学校的 JD 为准
- **B**：以 JD 为准，同时标记地区规则库需要审查
- **C**：忽略冲突，按地区规则执行

---

**Q: Fit Score 多少分才值得申请？**

A: 一般建议：
- **7分以上**：强烈建议投递（my favorite）
- **5-7分**：值得尝试（worth trying）
- **5分以下**：低优先级，时间充裕再考虑

但最终判断还要结合你自己对这所学校的兴趣和地理偏好。

---

**Q: 澳洲申请为什么要额外生成 Selection Criteria Response？**

A: 澳洲大多数大学要求申请人逐条回应 JD 中列出的 Essential Criteria（必要条件）。这份文件不提交会直接被筛掉，AI 会自动识别澳洲职位并生成这份材料。

---

**Q: 生成的 PDF 在哪里？**

A: 在 `output/{school_id}/{dept_id}/materials/{材料名}/` 目录下，文件名通常是 `main.pdf` 或 `Teaching_Statement.pdf`。可以在 Finder 中导航到 `overseas_pipeline/output/` 找到对应学校目录。

---

**Q: 材料准备好了，怎么填写学校的在线申请系统？**

A: 使用配套的 `job_filling/` 工具，它专门负责自动填写网页表单：

```bash
cd ../job_filling
claude --dangerously-skip-permissions
```

启动后告诉 Claude Code："帮我填写表单"，AI 会读取你的个人资料和申请材料，自动填写当前打开的表单页面。详见 [`job_filling/README.md`](../job_filling/README.md)。

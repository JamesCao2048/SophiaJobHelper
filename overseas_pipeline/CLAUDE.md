# Overseas Pipeline -- 海外教职申请流水线

## 定位

Claude Code 驱动的海外教职申请材料准备流水线。目标：将每所学校的申请材料准备从 1-2 小时降至 15-20 分钟（生成初稿 + Sophia 审核修改）。

## 语言要求

**所有与用户的交互使用中文。** 代码注释和变量名保持英文。

## 网页抓取规则（强制）

**所有涉及 URL 抓取的步骤，必须使用 `web-fetch-fallback` skill 的三层 fallback 策略：**

1. **Layer 1**: WebFetch / Jina Reader / curl + browser UA
2. **Layer 2**: Tavily Extract API（`$TAVILY_API_KEY`）
3. **Layer 3**: Tavily Search API

**不允许在 Layer 1 失败后直接放弃**——必须依次尝试 Layer 2 和 Layer 3。大学网站普遍有 Cloudflare 保护，Layer 1 几乎必然失败，Layer 2/3 才是主力。

## 资源引用关系

```
overseas_pipeline/           ← 本模块
├── src/faculty_scraper.py   ← Step 1 爬取工具（Python 获取数据）
├── templates/cover_letter/  ← LaTeX 模板（OUCletter.cls + main_template.tex）
└── output/{school}/         ← 产出物（.gitignore，不提交）

region_knowledge/            ← 区域知识库（独立子模块）
├── regions/{region}.md      ← 地区规则卡（被 Step 2/3 读取）
└── schools/{school}.md      ← 学校知识卡（Step 1 处理后回写）

job_filling/materials/       ← Sophia 现有申请材料
├── cv_latest.md
├── Research_Statement.md
├── Teaching_Statement.md
├── Impact_Statement.md
└── publication*.md

overleaf-projects/           ← 申请材料 LaTeX 源文件（被 Step 3 读取）
```

## 产出物结构

```
output/{school_id}/
├── faculty_data.json          ← Step 1 产出：faculty 结构化数据
├── faculty_data.sources.md    ← Step 1 产出：数据来源标注
├── data_quality.json          ← Step 1 产出：数据质量评估（决定是否 warn 用户）
├── fit_report.md              ← Step 2 产出：匹配分析报告
├── fit_report.sources.md      ← Step 2 产出：参考资料清单
├── papers/                    ← Step 1 下载的相关论文（PDF）
└── materials/                 ← Step 3 产出
    ├── Cover Letter/              ← 从 overleaf-projects 复制的完整 LaTeX 项目
    │   ├── main.tex                   ← 定制后的 cover letter
    │   ├── main.pdf                   ← 编译后的 PDF
    │   ├── OUCletter.cls              ← 样式文件
    │   ├── signature*.pdf/png         ← 签名文件
    │   └── ...                        ← 其他依赖文件
    ├── Research Statement/        ← 从 overleaf-projects 复制的完整 LaTeX 项目
    │   ├── main.tex                   ← 定制后的 research statement
    │   ├── main.pdf                   ← 编译后的 PDF
    │   ├── figures/                   ← 图片文件夹
    │   └── reference.tex              ← 参考文献
    ├── Teaching Statement/        ← 从 overleaf-projects 复制的完整 LaTeX 项目
    │   ├── Teaching_Statement.tex     ← 定制后的 teaching statement
    │   └── Teaching_Statement.pdf     ← 编译后的 PDF
    ├── Selection Criteria Response/  ← 新建的 LaTeX 项目（澳洲特有）
    │   ├── selection_criteria_response.tex
    │   └── selection_criteria_response.pdf
    ├── cover_letter.notes.md      ← 修改说明（diff + 原因 + 参考来源）
    ├── research_statement.notes.md
    ├── teaching_statement.notes.md
    └── selection_criteria_response.notes.md  ← （澳洲特有）
```

### 材料输出格式规范

**最终产物（.tex）：**
- 必须是完整、干净、可直接编译的 LaTeX 文件
- 不包含任何标注（`[NEW]`、`[MODIFIED]`、编辑说明等）
- 用 `xelatex` 编译后可直接生成 PDF
- Sophia 审核时看 PDF，修改时编辑 .tex

**修改说明（.notes.md）：**
- Markdown 格式
- 包含：总体策略、参考资料清单、逐段 diff（原文 vs 修改、修改原因引用具体来源）
- 这是给 Sophia 审核用的"修改日志"，不是提交材料

---

## 用户命令

### "研究 {学校名}"（Step 1: Research）

**前提：** 需要学校名 + 院系 URL（或职位 URL）

**执行步骤：**
1. 确定学校 ID（snake_case，如 `monash_university`）
2. 爬取院系页面（三层 fallback 策略）：
   - **Layer 1**: 运行 `python overseas_pipeline/src/faculty_scraper.py`（Jina Reader API）
     ```
     python overseas_pipeline/src/faculty_scraper.py --school "{学校名}" --url "{院系页面URL}"
     ```
   - **Layer 2**: 如 Jina Reader 失败（403/Cloudflare），使用 `web-fetch-fallback` skill 的三层 fallback：
     1. `curl` + browser User-Agent
     2. Tavily Extract API（`$TAVILY_API_KEY`）
     3. Tavily Search API
   - **Layer 3**: 以上均失败时，提示用户手动 copy-paste
   - 输出原始 markdown 到 `output/{school_id}/raw/`
3. **Claude Code 分析**（从原始 markdown 中提取结构化数据）：
   - 读取爬取的 markdown 内容
   - 读取 `job_filling/materials/Research_Statement.md` 了解 Sophia 的研究方向
   - 识别 faculty 列表，对每人判断 `overlap_with_sophia`（high/medium/low/none）
   - 识别标准：Human-AI collaboration / HCI / CSCW / AI / NLP / qualitative methods 相关
   - 对 overlap=high 的 faculty（≤5人）记录详细的 `overlapping_papers` 信息
4. **下载高匹配 faculty 的相关论文**（必须执行，不可跳过）：
   - 对每位 overlap=high 的 faculty，通过 WebSearch 找到与 Sophia 研究方向最相关的 1-3 篇论文
   - 下载 PDF 到 `output/{school_id}/papers/`，命名格式：`{作者姓}_{年份}_{简短标题}.pdf`
   - 优先从 arXiv、ACL Anthology、Springer 等开放源下载
   - 在 `faculty_data.json` 的 `overlapping_papers` 中记录每篇论文的 `local_pdf` 路径
   - 论文是 Step 2 fit_report 中"具体研究结合点"分析的关键依据，不下载会导致分析空泛
5. 生成 `output/{school_id}/faculty_data.json`（见格式规范）
5. 生成 `output/{school_id}/faculty_data.sources.md`（标注每位 faculty 信息的来源 URL）
6. 检查 `region_knowledge/schools/{school_id}.md` 是否存在，如不存在则创建框架

**数据质量评估（Step 1 完成后必须执行）：**

生成 `output/{school_id}/data_quality.json`：
```json
{
  "overall_quality": "high | medium | low",
  "scrape_success": true/false,
  "data_source": "jina_reader | direct_html | web_search_summary | manual_paste",
  "faculty_count": 6,
  "high_overlap_count": 2,
  "papers_downloaded": 0,
  "issues": [
    "Cloudflare blocked: faculty page scraped via WebSearch summaries only",
    "No papers downloaded for high-overlap faculty"
  ]
}
```

**质量分级标准：**
| 质量 | 条件 | 行为 |
|------|------|------|
| **high** | Jina Reader/直接爬取成功 + faculty 页面完整 + high overlap faculty 论文已下载 | 静默继续 Step 2 |
| **medium** | 爬取成功但部分信息缺失（如缺论文下载），或来自 WebSearch 摘要但确认了 faculty 主页 | **⚠ Warning**：显示质量报告，询问用户是否继续 |
| **low** | 爬取完全失败 / faculty 数据来自搜索摘要且未验证 / high overlap faculty = 0 | **❌ 暂停**：必须等用户手动补充数据或确认跳过 |

**Warning 格式：**
```
⚠ Step 1 数据质量警告：{school_name}

数据来源：{data_source}（非直接爬取）
问题：
  - {issue_1}
  - {issue_2}

影响：
  - Faculty overlap 判断基于搜索摘要，可能不准确
  - 未下载高匹配 faculty 论文，fit_report 中的"具体研究结合点"将缺乏依据

选项：
A. 继续 Step 2（接受当前数据质量，分析结果标注为 [低置信度]）
B. 手动补充数据（在浏览器中访问 faculty 页面，copy-paste 到此处）
C. 中止（等后续改进 scraper 后重试）

请回复 A、B 或 C。
```

**"一键分析"模式下的行为：**
- 默认：数据质量 ≤ medium 时暂停（同上）
- 如果用户指定了 `--ignore-warnings`（如 "一键分析 {学校} 跳过警告"）：显示 warning 但不暂停，继续执行，所有产出物标注 `[低置信度]`

**如果爬取完全失败（反爬/结构复杂）：**
- 提示用户手动 copy-paste faculty 列表：
  ```
  ⚠ 自动爬取失败，请在浏览器中打开 {URL}，复制 faculty 列表内容后粘贴到此处。
  ```

**faculty_data.json 格式：**
```json
{
  "school": "Monash University",
  "school_id": "monash_university",
  "department": "Department of Data Science and AI",
  "department_url": "https://...",
  "job_url": "https://...",
  "region": "australia",
  "research_focus": ["AI", "HCI", "data science"],
  "faculty": [
    {
      "name": "Prof. Jane Smith",
      "title": "Professor",
      "research_interests": ["human-AI interaction", "CSCW"],
      "homepage": "https://...",
      "google_scholar": "https://scholar.google.com/citations?user=xxxxx",
      "overlap_with_sophia": "high",
      "overlap_reason": "Both work on human-AI collaboration for data analysis",
      "overlapping_papers": [
        {
          "title": "...",
          "venue": "CHI 2024",
          "year": 2024,
          "url": "https://doi.org/...",
          "relevance": "Direct overlap with CollabCoder line"
        }
      ]
    }
  ],
  "scrape_date": "YYYY-MM-DD",
  "scrape_method": "jina_reader"
}
```

---

### "分析 {学校名}"（Step 2: Fit Analysis）

**前提：** Step 1 已完成（`output/{school_id}/faculty_data.json` 存在）

**执行步骤：**
1. 读取 `output/{school_id}/faculty_data.json`
2. 确定 region → 读取 `region_knowledge/regions/{region}.md`
3. 检查 `region_knowledge/schools/{school_id}.md` 是否存在，如存在则读取（用于覆盖地区卡差异）
4. 爬取职位 JD 原文：
   - 用 `python overseas_pipeline/src/faculty_scraper.py --url "{job_url}" --output-type raw`
   - 或请用户提供 JD 文本
5. 读取 Sophia 全套材料：
   - `job_filling/materials/Research_Statement.md`
   - `job_filling/materials/Teaching_Statement.md`
   - `job_filling/materials/cv_latest.md`
   - `job_filling/materials/Impact_Statement.md`（如存在）
6. **⚠ 规则冲突检查（关键）**：
   - 比较 JD 要求与地区规则卡的规则
   - 如发现冲突，**立即暂停**，向用户显示：
     - 地区卡的规则（含 source 链接）
     - JD 的实际要求（含 URL）
     - 处理选项 A/B/C
7. 生成 `output/{school_id}/fit_report.md`（见格式规范）
8. 生成 `output/{school_id}/fit_report.sources.md`

**fit_report.md 格式：**
```markdown
# {学校} -- 匹配分析报告

## 基本信息
- 院系：
- 地区 / 规则卡：
- 职级：
- Deadline：
- 职位链接：

## Fit Score: X/10

## 匹配维度分析

### 研究方向匹配 (X/10)
...

### 区域适配 (X/10)
...

### 关键决策人分析（材料写给谁看）
...

### 各材料调整建议

#### Cover Letter
...

#### Research Statement
...

#### Teaching Statement
...

#### Selection Criteria Response（如为澳洲职位）
...（列出每条 criterion 的回应框架）

### 风险提示
...

### 投递建议
- 是否建议投递：
- 优先级：my favorite / worth trying / low priority
```

**规则冲突处理流程：**
```
⚠ 发现规则冲突，暂停流水线。

【地区卡规则】{具体规则内容}（来源：{source URL}）
【JD 实际要求】{JD 中的具体要求}（来源：{job URL}）

请选择处理方式：
A. 以该校 JD 为准（本次），记录到学校卡
B. 以该校 JD 为准，同时标记地区卡 needs_review
C. 忽略冲突，仍按地区卡执行

请回复 A、B 或 C。
```

---

### "生成材料 {学校名}"（Step 3: Materials Generation）

**前提：** Step 2 已完成（`output/{school_id}/fit_report.md` 存在）

**执行步骤：**
1. 读取 `output/{school_id}/fit_report.md` 中的"各材料调整建议"
2. 读取 Sophia 现有材料（`job_filling/materials/*.md`）
3. 读取区域规则卡（`region_knowledge/regions/{region}.md`）
4. 读取 overleaf 原始 LaTeX 源文件（`overleaf-projects/Faculty Position/`）
5. 为每份材料生成初稿 + notes（Step 3a）
6. 复制 overleaf 项目到学校输出目录 + 替换内容 + 编译 PDF（Step 3b）

#### Step 3a: 生成内容

**Cover Letter：**
- 读取 overleaf 中已有的该校 cover letter（如 `overleaf-projects/Cover Letter/Cover Letter- {学校名}/main.tex`），或读取模板 `overseas_pipeline/templates/cover_letter/main_template.tex`
- 基于 fit_report 建议定制内容
- 长度：1-2 页（澳洲规范），不要写成美式 5 页长文
- ⚠ **OUCletter.cls 注意：** cls 的 `\cvheader` 已自动渲染完整信息栏（JHU logo + 姓名 + 联系方式 + 地址）。**不要**添加任何 tikz overlay 或 eso-pic 来叠加地址，否则会导致重叠。只需定义 `\signature{\name}` 供 closing 使用。
- 同时生成 `cover_letter.notes.md`

**Research Statement：**
- 读取 `overleaf-projects/Faculty Position/Research Statement/Research Statement/main.tex`
- 基于原始 LaTeX 直接修改，保留完整格式和图片引用
- 修改点：加入 ARC grant 计划（必须具体提及 DECRA）、根据院系研究重点调整强调、加入院系合作段落
- 同时生成 `research_statement.notes.md`

**Teaching Statement：**
- 读取 `overleaf-projects/Faculty Position/Teaching Statement/Teaching Statement/Teaching_Statement.tex`
- 基于原始 LaTeX 直接修改
- 修改点：补充该校课程名称（从 JD/网站查取）、加入具体量化数据、加入澳洲 40/40/20 声明（如适用）
- 同时生成 `teaching_statement.notes.md`

**Selection Criteria Response（仅澳洲职位）：**
- 从 JD 中提取所有 Essential 和 Desirable criteria
- 全新生成 LaTeX 文件（使用与其他材料一致的样式）
- 格式：逐条用 STAR 法则回应（Situation → Task → Action → Result）
- 长度：6-10 页（澳洲规范）
- **这是澳洲申请的核心文件，不提交直接出局**
- 同时生成 `selection_criteria_response.notes.md`

#### Step 3b: 复制模板 + 编译 PDF（收尾步骤）

**执行流程：**
1. 从 `overleaf-projects/Faculty Position/` 复制完整 LaTeX 项目目录到 `output/{school_id}/materials/`：
   - `overleaf-projects/Cover Letter/Cover Letter- {学校名}/` → `output/{school_id}/materials/Cover Letter/`
     - 如 overleaf 中没有该校 cover letter，复制模板 `overseas_pipeline/templates/cover_letter/` 的内容
   - `Research Statement/Research Statement/` → `output/{school_id}/materials/Research Statement/`
   - `Teaching Statement/Teaching Statement/` → `output/{school_id}/materials/Teaching Statement/`
   - Selection Criteria Response 无需复制（新建目录即可）

2. 用 Step 3a 生成的 .tex 内容**替换**复制后目录中的对应 .tex 文件

3. **检查样式一致性**：
   - 对比 Step 3a 生成的 .tex 与原始模板的 preamble（包、颜色、页边距、字体等）
   - 如发现差异需要修改样式（如调整页边距适配更长内容），在 notes.md 中说明修改原因

4. **编译 PDF**：
   ```bash
   cd "output/{school_id}/materials/{文件夹}" && xelatex {主tex文件} && xelatex {主tex文件}
   ```
   - 执行两遍 xelatex 确保页码和引用正确
   - 如编译失败，检查错误并修复，记录到 notes.md

5. 验证 PDF 生成成功，检查页数是否合理

**每份 .notes.md 格式（强制要求，不可简化）：**

notes.md 是给 Sophia 审核的"修改日志"，必须包含足够的上下文让她无需打开 .tex 文件就能理解所有修改。**必须包含以下所有章节：**

```markdown
# {材料名} 修改说明 -- {学校}

## 生成日期

## 总体策略
<!-- 2-3 句话说明整体定制方向和关键定位决策 -->
<!-- 例：将 Sophia 的 human-AI collaboration 研究定位为 "human-centered evaluation for agentic AI" -->

## 参考资料清单
| # | 类型 | 资料 | 链接/路径 |
|---|------|------|-----------|
| R1 | 区域规则卡 | 澳洲规则卡 Section X（具体行号）| region_knowledge/regions/australia.md L58-138 |
| R2 | Fit Report | {学校} 匹配分析 | output/{school}/fit_report.md |
| R3 | Sophia 材料 | Research Statement | job_filling/materials/Research_Statement.md |
...
<!-- 参考资料必须标注具体章节/行号，不可泛泛引用 -->

## 逐段修改说明

### 1. {段落标识} [NEW/MODIFIED/UNCHANGED]
**原文：** > 引用原始文本（如为新增则标注"无对应原文"）
**修改为：** > 引用修改后的关键句子
**原因：**
- 引用 [R1: 具体章节/行号] ...
- 说明这个修改的设计意图

### N. 未修改部分
<!-- 必须列出所有未修改的主要段落，说明保留原因 -->
<!-- 例：教学哲学段（interactive + continuous refinement）完全保留，这是 Sophia 的核心教学理念 -->

## 样式说明与 Debug 记录
<!-- 记录编译器选择（pdflatex/xelatex）、字体、颜色方案等 -->
<!-- 如有编译问题的修复，必须记录 -->

## 给 Sophia 的审核重点
<!-- 3-5 条需要 Sophia 核实或决策的具体项目 -->
<!-- 每条必须是可操作的（如"核实 X 数字是否准确"），不是泛泛的"请审核" -->
```

**notes.md 质量检查标准（Step 3 完成前必须自检）：**
- [ ] 每个修改段落都有原文 vs 修改 的对比
- [ ] 每个修改原因都引用了具体的参考资料编号和章节
- [ ] 未修改的部分也有说明（为什么保留）
- [ ] 有编译/样式说明
- [ ] "给 Sophia 的审核重点"包含具体可操作的审核项

---

### "一键分析 {学校名}"

依次执行 Step 1 → Step 2 → Step 3，中间不暂停（规则冲突时除外）。

**用法：** 适用于已确认要投的学校，需同时提供：
- 院系 URL（或职位 URL）

**执行：**
1. 如果 `faculty_data.json` 不存在 → 先执行"研究 {学校名}"
2. 如果 `fit_report.md` 不存在 → 执行"分析 {学校名}"
3. 执行"生成材料 {学校名}"

---

## 质量要求

1. **全链路可溯源**：每个产出物必须有对应的 `.sources.md` 文件
2. **完整初稿**：生成完整可用的初稿，不只是修改建议
3. **冲突时必须暂停**：规则冲突不能静默处理，必须等用户判断
4. **澳洲 KSC 是重点**：Selection Criteria Response 是澳洲申请的核心，不能遗漏
5. **引用要具体**：notes 文件中引用规则卡时需注明章节，不能泛泛引用
6. **每步必须生成 step summary 文件**：每个 Step 完成后，除了在命令行向用户展示报告，**必须同时保存到文件**：
   - Step 1 → `output/{school_id}/step1_summary.md`（数据质量报告 + 适配度初判 + 高匹配 faculty 概览 + 论文下载情况）
   - Step 2 → `output/{school_id}/step2_summary.md`（fit score + 各维度评分 + 规则冲突记录 + 材料调整要点）
   - Step 3 → `output/{school_id}/step3_summary.md`（各材料生成状态 + PDF 编译结果 + 需要 Sophia 重点审核的内容）
   - 文件内容应与命令行展示的内容一致，方便跨 session 回溯和 Sophia 异步审阅

## 关于 .gitignore

`output/` 目录下的内容（学校分析数据、材料初稿）**不提交**到 git，已通过 `.gitignore` 排除。

# Step 1: Research（研究学校）

## 前提

需要学校名 + 院系 URL（或职位 URL）

---

## 执行步骤

### 1. 确定 ID

- `school_id`：snake_case，如 `monash_university`
- `dept_id`：目标院系英文缩写，snake_case，如 `dsai`、`hcc`、`cs`
- 输出目录：`output/{school_id}/{dept_id}/`（单系学校可省略 `dept_id` 层）

### 1b. 扫描同校已有院系产物（如 `output/{school_id}/` 已存在）

- 列出已有的 `{dept_id}/` 子目录
- 识别与当前院系 faculty 重叠的教授（joint appointment 或同校 HCI 教授）
- 将有价值的论文 PDF **复制**到当前院系的 `papers/` 目录（不是 symlink）
- 将已有院系的 `related_applications` 信息写入当前院系的 `faculty_data.json`
- 在 step1_summary.md 中列出：从哪个已有院系复用了哪些论文

**跨系 faculty 数据复用约定：**
- 已有院系的 `cross_department_collaborators` 往往正是当前院系的主体 faculty
- 预填充步骤：从已有院系的 `cross_department_collaborators` 中，找出 `department` 字段匹配当前院系的成员，将其基础信息作为当前院系 `faculty` 数组的**起点**
- 预填充只是起点，仍需：① 重新判断 `overlap_with_sophia`；② 重新搜索 `overlapping_papers`
- 已下载的论文 PDF 可直接复用（复制到当前 `papers/`），无需重新下载

### 2. 爬取院系页面（五层 fallback）

- **Layer 1**: `python overseas_pipeline/src/faculty_scraper.py --school "{学校名}" --url "{院系URL}"`
- **Layer 1.5～3**: 如 Jina Reader 失败，依次使用 `web-fetch-fallback` skill：
  1. curl + browser UA
  2. Tavily Extract API
  3. Wayback Machine
  4. Tavily Search API
- **全部失败时**: 提示用户手动 copy-paste

输出原始 markdown 到 `output/{school_id}/{dept_id}/raw/`

### 3. Claude Code 分析

- 读取爬取的 markdown 内容
- 读取 `job_filling/materials/Research_Statement.md` 了解 Sophia 的研究方向
- 识别 faculty 列表，对每人判断 `overlap_with_sophia`（high/medium/low/none）
- 识别标准：Human-AI collaboration / HCI / CSCW / AI / NLP / qualitative methods 相关
- 对 overlap=high 的 faculty（≤5人）记录详细的 `overlapping_papers` 信息

### 4. 下载高匹配 faculty 论文（必须执行，不可跳过）

- 对每位 overlap=high 的 faculty，通过 WebSearch 找到与 Sophia 研究方向最相关的 1-3 篇论文
- 下载 PDF 到 `output/{school_id}/{dept_id}/papers/`，命名：`{作者姓}_{年份}_{简短标题}.pdf`
- 优先从 arXiv、ACL Anthology、Springer 等开放源下载
- 在 `faculty_data.json` 的 `overlapping_papers` 中记录每篇论文的 `local_pdf` 路径
- 论文是 Step 2 fit_report "具体研究结合点"分析的关键依据，不下载会导致分析空泛

### 5. 生成 faculty_data.json（格式见下）

### 6. 生成 faculty_data.sources.md（标注每位 faculty 信息的来源 URL）

### 7. 检查 region_knowledge/schools/{school_id}.md，如不存在则创建框架

### 8. HCI 密度分类

```bash
python overseas_pipeline/src/hci_density_classifier.py \
  --input output/{school_id}/{dept_id}/faculty_data.json \
  [--target-dept "{目标系名称}"]
```

自动推断双层密度（target_dept + faculty_wide）和策略标签，写入 `faculty_data.json` 的 `hci_density` 字段。**agent 随后补充 `strategy_rationale`**（自然语言解释，检查边界情况）。

### 9. 课程体系抓取

```bash
python overseas_pipeline/src/course_catalog_scraper.py \
  --url "{目标系课程页面URL}" \
  --output output/{school_id}/{dept_id}/faculty_data.json \
  --school "{学校名}"
```

五层 fallback 抓取课程列表：
- 原始内容**始终保存**到 `output/{school_id}/{dept_id}/raw/course_catalog_raw.md`
- 正则提取结果写入 `faculty_data.json` 的 `department_courses` 字段
- 如课程页面 URL 未知，用 Tavily 搜索 `site:{domain} course catalog`

**agent 随后审查**：
- 若 `department_courses` 为空（正则提取失败），读取 `raw/course_catalog_raw.md` 直接识别课程
- 识别 Sophia 能教的课，按密度策略排序
- 将识别结果写回 `faculty_data.json` 的 `department_courses` 字段

### 10. Agent 审查补充

- 检查密度分类是否有边界遗漏
- 补充 `hci_density.strategy_rationale` 自然语言解释
- 将密度判断 + 课程匹配概览写入 `step1_summary.md`

---

## 数据质量评估（Step 1 完成后必须执行）

生成 `output/{school_id}/{dept_id}/data_quality.json`：

```json
{
  "overall_quality": "high | medium | low",
  "scrape_success": true,
  "data_source": "jina_reader | direct_html | web_search_summary | manual_paste",
  "faculty_count": 6,
  "high_overlap_count": 2,
  "papers_downloaded": 3,
  "issues": []
}
```

**质量分级标准：**

| 质量 | 条件 | 行为 |
|------|------|------|
| **high** | 直接爬取成功 + faculty 页面完整 + high overlap faculty 论文已下载 | 静默继续 Step 2 |
| **medium** | 爬取成功但部分信息缺失，或来自 WebSearch 摘要但确认了 faculty 主页 | **⚠ Warning**：询问用户是否继续 |
| **low** | 爬取完全失败 / faculty 数据未验证 / high overlap faculty = 0 | **❌ 暂停**：等用户手动补充 |

**Warning 格式：**
```
⚠ Step 1 数据质量警告：{school_name}

数据来源：{data_source}（非直接爬取）
问题：
  - {issue_1}

影响：
  - Faculty overlap 判断基于搜索摘要，可能不准确
  - 未下载高匹配 faculty 论文，fit_report 中的"具体研究结合点"将缺乏依据

选项：
A. 继续 Step 2（分析结果标注为 [低置信度]）
B. 手动补充数据（copy-paste 到此处）
C. 中止

请回复 A、B 或 C。
```

---

## faculty_data.json 格式

```json
{
  "school": "Monash University",
  "school_id": "monash_university",
  "department": "Department of Data Science and AI",
  "dept_id": "dsai",
  "department_url": "https://...",
  "job_url": "https://...",
  "region": "australia",
  "research_focus": ["AI", "HCI", "data science"],
  "hci_density": {
    "target_dept": "many | few | none",
    "faculty_wide": "many | few | none",
    "strategy": "specialist | builder | pioneer_with_allies | pioneer_with_few_allies | pure_pioneer",
    "strategy_rationale": "...",
    "target_dept_hci_faculty": ["Prof. X (HCI)", "Prof. Y (CSCW)"],
    "cross_department_collaborators": [
      {
        "name": "Prof. Z",
        "department": "School of Design",
        "research_interests": ["interaction design"],
        "overlap_reason": "User study methods overlap"
      }
    ]
  },
  "department_courses": [
    {
      "code": "FIT3170",
      "name": "Software Engineering Practice",
      "level": "undergraduate",
      "sophia_can_teach": true,
      "density_strategy_priority": "core"
    }
  ],
  "sophia_teachable_courses": {
    "can_teach_existing": [],
    "can_propose_new": []
  },
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
          "local_pdf": "papers/Smith_2024_title.pdf",
          "relevance": "Direct overlap with CollabCoder line"
        }
      ]
    }
  ],
  "scrape_date": "YYYY-MM-DD",
  "scrape_method": "jina_reader"
}
```

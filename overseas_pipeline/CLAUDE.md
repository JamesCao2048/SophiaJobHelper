# Overseas Pipeline -- 海外教职申请流水线

## 定位

Claude Code 驱动的海外教职申请材料准备流水线。目标：将每所学校的申请材料准备从 1-2 小时降至 15-20 分钟（生成初稿 + Sophia 审核修改）。

## 语言要求

**所有与用户的交互使用中文。** 代码注释和变量名保持英文。

## 网页抓取规则（强制）

**所有涉及 URL 抓取的步骤，必须使用 `web-fetch-fallback` skill 的五层 fallback 策略：**

1. **Layer 1**: curl + browser User-Agent
2. **Layer 1.5**: Jina Reader（`https://r.jina.ai/`，免费无 key，适合 Medium/Cloudflare 场景）
3. **Layer 2**: Tavily Extract API（`$TAVILY_API_KEY`）
4. **Layer 2.5**: Wayback Machine（`web.archive.org/web/{year}/原URL`，适合博客/个人网站）
5. **Layer 3**: Tavily Search API

**不允许在 Layer 1 失败后直接放弃**——必须依次尝试后续各层。详见 `web-fetch-fallback` skill。

## 资源引用关系

```
overseas_pipeline/           ← 本模块
├── src/faculty_scraper.py   ← Step 1 爬取工具
├── templates/cover_letter/  ← LaTeX 模板（OUCletter.cls + main_template.tex）
├── workflows/               ← 各步骤详细流程（按需读取）
│   ├── step1_research.md
│   ├── step2_analysis.md
│   ├── step3_materials.md
│   └── cv_strategy.md
└── output/{school}/         ← 产出物（.gitignore，不提交）

region_knowledge/            ← 区域知识库
├── regions/{region}.md      ← 地区规则卡（Step 2/3 读取）
└── schools/{school}.md      ← 学校知识卡

job_filling/materials/       ← Sophia 现有申请材料
├── cv_latest.md
├── Research_Statement.md
├── Teaching_Statement.md
├── Impact_Statement.md
└── publication*.md

overleaf-projects/Faculty Position/  ← LaTeX 源文件（Step 3 读取）
├── Cover Letter/                    ← 各校专属版
├── Research Statement/              ← 完整版（含图）
├── Teaching Statement/              ← 含 Zhiyao/Erika/Ruyuan 故事
├── DEI-structured-1p/               ← Diversity Statement 1 页（管道默认）
├── DEI-structured-2p/               ← Diversity Statement 2 页
├── DEI-prose-2p/                    ← 散文叙事版（备用参考）
├── CV_latest/                       ← CV 模块化源（Step 3 按需定制）
└── templates/cover_letter/          ← Cover Letter 模板
```

## 产出物结构

```
output/{school_id}/
├── {dept_id}/                         ← 院系级目录（必须存在，单系学校也需要此层）
│   ├── faculty_data.json              ← Step 1
│   ├── faculty_data.sources.md        ← Step 1
│   ├── data_quality.json              ← Step 1
│   ├── fit_report.md                  ← Step 2
│   ├── fit_report.sources.md          ← Step 2
│   ├── step1_summary.md
│   ├── step2_summary.md
│   ├── step3_summary.md
│   ├── raw/                           ← 原始抓取内容
│   │   ├── faculty_page.md
│   │   ├── jd_*.md
│   │   └── course_catalog_raw.md
│   ├── papers/                        ← 下载的相关论文 PDF
│   └── materials/                     ← Step 3 产出
│       ├── Cover Letter/
│       ├── Research Statement/        （或 Research Interests/）
│       ├── Teaching Statement/
│       ├── Diversity Statement/        （JD 要求时）
│       ├── CV/                         （变体≠base 时）
│       └── Selection Criteria Response/（仅澳洲）
└── {dept_id_2}/                       ← 同校另一院系（结构相同）
```

**材料格式规范：**
- `.tex`：完整、干净、可直接编译，不含任何 `[NEW]`/`[MODIFIED]` 标注
- `.notes.md`：修改日志（总体策略 + 参考资料清单 + 逐段 diff + 审核重点）

---

## 用户命令

### "研究 {学校名}"（Step 1: Research）

→ **执行前先读取 `overseas_pipeline/workflows/step1_research.md`**

**前提：** 学校名 + 院系 URL（或职位 URL）

核心步骤：确定 ID → 爬取院系页面（五层 fallback）→ 分析 faculty 重叠 → 下载高匹配论文 → HCI 密度分类 → 课程体系抓取 → 数据质量评估

### "分析 {学校名}"（Step 2: Fit Analysis）

→ **执行前先读取 `overseas_pipeline/workflows/step2_analysis.md`**

**前提：** Step 1 已完成

核心步骤：读取 faculty_data + 地区规则卡 → 爬取 JD → 规则冲突检查（冲突时必须暂停）→ 生成 fit_report.md

### "生成材料 {学校名}"（Step 3: Materials Generation）

→ **执行前先读取 `overseas_pipeline/workflows/step3_materials.md`**

**前提：** Step 2 已完成

核心步骤：按 fit_report 建议生成 Cover Letter / Research Statement / Teaching Statement / Diversity Statement（按需）/ CV（按需）/ Selection Criteria Response（澳洲）→ Humanizer 处理（强制）→ 编译 PDF

### "一键分析 {学校名}"

依次执行 Step 1 → Step 2 → Step 3，读取对应 workflow 文件。规则冲突或数据质量不足时暂停。

---

## 质量要求

1. **全链路可溯源**：每个产出物必须有对应的 `.sources.md` 文件
2. **完整初稿**：生成完整可用的初稿，不只是修改建议
3. **冲突时必须暂停**：规则冲突不能静默处理，必须等用户判断
4. **澳洲 KSC 是重点**：Selection Criteria Response 是澳洲申请的核心，不能遗漏
5. **引用要具体**：notes 文件中引用规则卡时需注明章节，不能泛泛引用
6. **每步必须生成 step summary 文件**（step1/2/3_summary.md），内容与命令行展示一致

## 关于 .gitignore

`output/` 目录下的内容（学校分析数据、材料初稿）**不提交**到 git，已通过 `.gitignore` 排除。

---

## 追踪数据库集成（ApplicationTracker）

overseas_pipeline 完成每个 Step 后，需要更新追踪数据库（`tracking/applications.db`）。

### 获取 app_id

```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd()))
from tracking.tracking_db import ApplicationTracker
tracker = ApplicationTracker()

all_apps = tracker.all_applications()
match = next((a for a in all_apps if school_id in (a.get("school_id") or "")), None)
if match:
    app_id = match["id"]
else:
    app_id = tracker.add_job(school=school_name, position=job_title, region=region)
```

或通过 CLI：
```bash
python -m tracking.cli add "University Name" "Position Title" --region australia
python -m tracking.cli list --status discovered
```

### Step 1 完成后

```python
tracker.mark_researched(
    app_id=app_id,
    pipeline_dir=f"overseas_pipeline/output/{school_id}",
    school_id=school_id,
    department=dept,
    hci_density_target=hci_target,
    hci_density_wide=hci_wide,
    hci_strategy=strategy,
    high_overlap_count=n,
    data_quality=quality,
)
```

### Step 2 完成后

```python
tracker.mark_analyzed(app_id=app_id, fit_score=fit_score)  # 1.0-10.0
```

### Step 3 完成后

```python
tracker.mark_materials_ready(app_id=app_id)
```

### 常用查询

```bash
python -m tracking.cli dashboard
python -m tracking.cli show <app_id>
python -m tracking.cli update <app_id> long_list
python -m tracking.cli update <app_id> rejected
```

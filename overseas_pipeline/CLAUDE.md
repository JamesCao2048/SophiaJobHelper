# Overseas Pipeline -- 海外教职申请流水线

## 定位

Claude Code 驱动的海外教职申请材料准备流水线。目标：将每所学校的申请材料准备从 1-2 小时降至 15-20 分钟（生成初稿 + Sophia 审核修改）。

## 启动方式（强制）

**Claude Code 必须从 `overseas_pipeline/` 目录内启动：**

```bash
cd overseas_pipeline
claude --dangerously-skip-permissions
```

从子项目目录启动可确保相对路径正确解析，且免去每次操作时确认权限弹窗。

## 路径规范（强制）

**所有文件路径必须使用相对路径，禁止使用任何含用户名的绝对路径（如 `/Users/junming/...`）。**

工作目录为 `overseas_pipeline/`，各关键路径的相对表示：

| 资源 | 相对路径 |
|------|---------|
| Sophia 现有材料 | `materials/` |
| LaTeX 模板 | `overleaf-projects/Faculty Position/` |
| 地区规则卡 | `../region_knowledge/regions/{region}.md` |
| 院系规则卡 | `../region_knowledge/schools/{school_id}/{dept_id}.md` |
| 产出物 | `output/{school_id}/{dept_id}/` |

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
overseas_pipeline/           ← 本模块（所有资源自包含）
├── src/faculty_scraper.py   ← Step 1 爬取工具
├── templates/cover_letter/  ← LaTeX 模板（OUCletter.cls + main_template.tex）
├── workflows/               ← 各步骤详细流程（按需读取）
│   ├── step1_research.md
│   ├── step2_analysis.md
│   ├── step3_materials.md
│   └── cv_strategy.md
├── materials/               ← Sophia 现有申请材料
│   ├── cv_latest.md
│   ├── Research_Statement.md
│   ├── Teaching_Statement.md
│   ├── Impact_Statement.md
│   └── publication*.md
├── overleaf-projects/Faculty Position/  ← LaTeX 源文件（Step 3 读取）
│   ├── Cover Letter/                    ← 各校专属版
│   ├── Research Statement/              ← 完整版（含图）
│   ├── Teaching Statement/              ← 含 Zhiyao/Erika/Ruyuan 故事
│   ├── DEI-structured-1p/               ← Diversity Statement 1 页（管道默认）
│   ├── DEI-structured-2p/               ← Diversity Statement 2 页
│   ├── DEI-prose-2p/                    ← 散文叙事版（备用参考）
│   ├── CV_latest/                       ← CV 模块化源（Step 3 按需定制）
│   └── templates/cover_letter/          ← Cover Letter 模板
└── output/{school}/         ← 产出物（.gitignore，不提交）

region_knowledge/                  ← 区域知识库（项目根目录）
├── regions/{region}.md            ← 地区规则卡（Step 2/3 读取）
└── schools/{school_id}/{dept_id}.md  ← 院系规则卡（同校多院系）
```

## 产出物结构

```
output/{school_id}/
├── {dept_id}/                         ← 院系级目录（必须存在，单系学校也需要此层）
│   ├── faculty_data.json              ← Step 1
│   ├── faculty_data.sources.md        ← Step 1
│   ├── data_quality.json              ← Step 1
│   ├── knowledge/
│   │   └── {dept_id}.md               ← 院系规则卡运行期副本（与 region_knowledge 双写入）
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

## 用户命令识别（模糊匹配）

用户不需要说出精确指令。根据语义推断目标步骤：

### Step 1 — 院系研究

**触发词**（含学校名或 URL 时）：研究、挖掘、爬取、调研、搜集、探索、扫描、看看这个学校、启动、开始、去查一下、先了解一下、Step 1、第一步

→ **执行前先读取 `workflows/step1_research.md`**

核心步骤：确定 ID → 爬取院系页面（五层 fallback）→ 分析 faculty 重叠 → 下载高匹配论文 → HCI 密度分类 → 课程体系抓取 → 数据质量评估

### Step 2 — 匹配分析

**触发词**（提及学校名，且 Step 1 已完成）：分析、评估、匹配、打分、fit、判断、看看匹配度、值不值得投、继续、下一步、Step 2、第二步

→ **执行前先读取 `workflows/step2_analysis.md`**

核心步骤：读取 faculty_data + 地区规则卡 → 爬取 JD → 规则冲突检查（冲突时必须暂停）→ 生成 fit_report.md

### Step 3 — 材料生成

**触发词**（提及学校名，且 Step 2 已完成）：生成材料、写材料、准备材料、出稿、做 Cover Letter、写申请、继续、下一步、Step 3、第三步

→ **执行前先读取 `workflows/step3_materials.md`**

核心步骤：按 fit_report 建议生成 Cover Letter / Research Statement / Teaching Statement / Diversity Statement（按需）/ CV（按需）/ Selection Criteria Response（澳洲）→ Humanizer 处理（强制）→ 编译 PDF

### 全流程一键

**触发词**：一键分析、全流程、从头开始、全部做、都做一遍 + 学校名/URL

依次执行 Step 1 → Step 2 → Step 3，读取对应 workflow 文件。规则冲突或数据质量不足时暂停询问用户。

### 歧义处理

- 如果无法确定目标步骤，列出当前学校的已完成步骤，询问用户意图
- "继续" 默认推断为：当前学校 + 上一步完成后的下一步
- 如果未提及学校名，询问："请问是哪所学校？"

---

## 知识回写规则

**每步执行完毕后，根据用户反馈判断是否需要更新共享知识库。** 这不仅仅是调整当前学校的产出，而是沉淀可复用的知识。

### 触发条件

以下情况应主动询问用户是否回写到知识库：

| 情况 | 可能需要更新的位置 |
|------|-------------------|
| 用户指出地区规则判断有误（如材料页数、面试流程） | `../region_knowledge/regions/{region}.md` |
| 用户反馈某类学校的申请策略与当前规则卡不符 | `../region_knowledge/regions/{region}.md` 或 `../region_knowledge/schools/{school}.md` |
| 用户对 HCI 密度策略的修辞建议有普遍性价值 | `strategies/hci_density_strategy.md` |
| 发现 Step 1/2/3 workflow 有结构性遗漏（如某类院校需额外步骤） | `workflows/step*.md` |
| 用户纠正了对某所学校的固定信息（如评审委员会结构、合同类型） | `../region_knowledge/schools/{school_id}/{dept_id}.md` |

### 询问方式

每次回写前必须询问确认，**不可静默修改共享知识库**：

```
我注意到你的反馈可能对其他学校也有参考价值：
【发现】{具体发现内容}
【建议更新】{目标文件} — {更新内容摘要}

请问需要将这条知识写入知识库吗？（Y 更新 / N 仅用于本次）
```

### 回写规范

- **增量写入**：不覆盖已有内容，在规则卡中追加或修改具体条目，并注明来源学校/日期
- **标注置信度**：如果是单一学校的数据，标注 `(单例，待更多数据验证)`
- **规则卡 needs_review**：如发现与已有规则冲突，在规则卡顶部标注 `needs_review`，不直接覆盖
- **workflow 更新**：改动 `workflows/` 文件时，在变更处加注释说明修改动机

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


<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

*No recent activity*
</claude-mem-context>

# 投递追踪系统 (Application Tracker)

SQLite-backed 申请全生命周期追踪，与 `faculty_monitor`、`overseas_pipeline`、`job_filling`、Google Sheets 联动。

---

## Quick Start

```bash
# 从项目根目录运行（替换为实际路径，或 cd 到该目录后运行）
# 查看当前全局状态（核心命令，每天打开看一眼）
python -m tracking.cli dashboard

# 分析现有 job list 现状（按状态查看）
python -m tracking.cli list --status discovered       # 尚未开始研究的
python -m tracking.cli list --status submitted        # 已投递
python -m tracking.cli list --priority favorite       # 标记为 favorite 的

# 查看快到期的 DDL
python -m tracking.cli upcoming 30

# 手动更新状态（收到学校邮件后）
python -m tracking.cli update 42 long_list
python -m tracking.cli update 42 rejected

# 查看单个申请详情 + 完整状态历史
python -m tracking.cli show 42
```

---

## 数据现状（截至 2026-02-19）

数据来源：从 Google Sheets 导入 184 条历史记录。

| 状态 | 数量 | 含义 |
|------|------|------|
| discovered | 101 | 发现但尚未开始分析 |
| submitted | 35 | 已提交申请 |
| rec_submitted | 20 | 推荐信已提交 |
| materials_ready | 8 | 材料已准备好，待填表 |
| filtered_out | 15 | 过滤掉（不匹配 / 已过期） |
| rec_requested | 4 | 学校已发出推荐信请求 |
| rejected | 1 | 已拒绝 |

---

## Pipeline 状态流

```
discovered ──► filtered_out  (不匹配/已过期，终止)
    │
    ▼
researched   (overseas_pipeline Step 1 完成)
    │
    ▼
analyzed     (overseas_pipeline Step 2 完成，有 fit_score)
    │
    ├──► decision_nogo  (主动放弃，终止)
    │
    ▼
materials_ready  (overseas_pipeline Step 3 完成)
    │
    ▼
form_filling     (job_filling 填表中)
    │
    ▼
submitted        (表单已提交)
    │
    ▼  (学校邮件通知推荐信——可选阶段)
rec_requested ──► rec_submitted
    │
    ▼
long_list ──► short_list ──► offer
    │
    └──► rejected  (终止)
```

---

## CLI 命令参考

```bash
# ── 查询 ──────────────────────────────────────────────
python -m tracking.cli dashboard              # 全局概览（推荐每日查看）
python -m tracking.cli upcoming [DAYS]        # N 天内到期（默认 7 天）
python -m tracking.cli list                   # 所有申请
python -m tracking.cli list --status submitted
python -m tracking.cli list --priority favorite
python -m tracking.cli show ID               # 单个申请详情+状态历史
python -m tracking.cli stale                  # 超期未推进（默认 submitted 30 天）
python -m tracking.cli stale --status long_list --days 21

# ── 写入 ──────────────────────────────────────────────
python -m tracking.cli add "学校名" "职位名" --region usa --deadline 2026-04-01
python -m tracking.cli update ID STATUS      # 手动更新状态
python -m tracking.cli priority ID favorite  # 设置优先级（favorite/high/low/none）

# ── 导出 ──────────────────────────────────────────────
python -m tracking.sheets_export             # 导出到 tracking/export_tracking.xlsx
python -m tracking.sheets_export --gsheets   # 上传到 Google Sheets（需配置 .env）

# ── 指定自定义 DB 路径 ────────────────────────────────
python -m tracking.cli --db /tmp/test.db dashboard
```

有效状态值：`discovered` `filtered_out` `researched` `analyzed` `decision_nogo` `materials_ready` `form_filling` `submitted` `rec_requested` `rec_submitted` `long_list` `short_list` `offer` `rejected`

有效优先级：`favorite` `high` `low`（`none` 清除标记）

---

## 与各子系统的联动

### 1. overseas_pipeline（Step 1/2/3）

每个 Step 完成后用 Python 更新状态：

```python
from tracking.tracking_db import ApplicationTracker
tracker = ApplicationTracker()

# 先找到 app_id（或新建）
all_apps = tracker.all_applications()
match = next((a for a in all_apps if "monash" in (a.get("school_id") or "").lower()), None)
if match:
    app_id = match["id"]
else:
    app_id = tracker.add_job(school="Monash University", position="Lecturer HCI", region="australia")

# Step 1 完成后
tracker.mark_researched(
    app_id=app_id,
    pipeline_dir="overseas_pipeline/output/monash_university",
    school_id="monash_university",
    department="Department of Data Science and AI",
    hci_density_target="many",   # none/few/many
    hci_density_wide="many",
    hci_strategy="specialist",
    high_overlap_count=3,
    data_quality="high",         # high/medium/low
)

# Step 2 完成后
tracker.mark_analyzed(app_id=app_id, fit_score=7.5)

# Step 3 完成后
tracker.mark_materials_ready(app_id=app_id)
```

也可通过 CLI 批量查找对应记录：
```bash
python -m tracking.cli list --status discovered | grep -i monash
```

### 2. job_filling（表单填写）

`form_filler.py apply` 支持 `--app-id` 参数，提交成功后自动回写：

```bash
cd job_filling
# 填表时带上 app_id，提交后自动变成 submitted 状态
python form_filler.py apply /tmp/instructions.json --app-id 42
```

如果忘记带参数，手动更新：
```bash
python -m tracking.cli update 42 submitted
```

### 3. faculty_monitor（自动发现新职位）

`faculty_monitor.py` 每次运行时会自动将推荐职位写入 tracker（`discovered` 状态）：

```bash
cd faculty-application_script
python faculty_monitor.py
# 运行后检查新增的 discovered 记录
cd ..
python -m tracking.cli list --status discovered | tail -5
```

### 4. Google Sheets 同步

**导出到 Excel（可用 Mac Excel 打开）：**
```bash
python -m tracking.sheets_export --output tracking/export_tracking.xlsx
```

**直接上传到 Google Sheets（需配置 `SPREADSHEET_ID`）：**
```bash
cd google-sheets-sync && python export_excel.py   # 原有方式，从云端拉
# 或反向推送：
python -m tracking.sheets_export --gsheets --spreadsheet-id <ID>
```

---

## Quick Start：将 faculty_monitor 的已知职位批量入库

`faculty_monitor.py` 在 `.seen_jobs.json` 中缓存了 90 个已抓取的职位，但这些**没有**自动进入 tracker。用以下脚本批量导入：

```python
# 在项目根目录运行：python tracking/import_seen_jobs.py
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tracking.tracking_db import ApplicationTracker

tracker = ApplicationTracker()
seen_path = Path("faculty-application_script/.seen_jobs.json")

with open(seen_path) as f:
    seen = json.load(f)

added = 0
for key, job in seen.items():
    title = job.get("title", "")
    url = job.get("url", "")
    first_seen = job.get("first_seen")
    if not title:
        continue
    # 粗略推断 region（可后续手动修正）
    region = "non_us_international"
    if any(k in title.lower() for k in ["university of", "carnegie", "mit", "stanford", "berkeley"]):
        region = "usa"
    app_id = tracker.add_job(
        school=title[:80],
        position=title,
        job_url=url,
        region=region,
        source="faculty_monitor_seen",
    )
    added += 1
    if added <= 3:
        print(f"  #{app_id}: {title[:60]}")

print(f"\n共导入 {added} 个职位")
```

运行后可继续精细化：
```bash
python -m tracking.cli list --status discovered | head -20
# 手动设置优先级
python -m tracking.cli priority 186 high
python -m tracking.cli priority 187 low
```

---

## Quick Start：分析现有 101 个 discovered 职位的现状

```bash
# 查看全部 discovered，按 DDL 排序
python -m tracking.cli list --status discovered

# 找 favorite 的（8 个）
python -m tracking.cli list --priority favorite

# 查看区域分布
python3 -c "
from tracking.tracking_db import ApplicationTracker
import collections
t = ApplicationTracker()
apps = t.all_applications()
by_region = collections.Counter(a.get('region','?') for a in apps)
by_status = collections.Counter(a.get('status','?') for a in apps)
print('=== 区域分布 ===')
for r, n in by_region.most_common():
    print(f'  {r}: {n}')
print()
print('=== 状态分布 ===')
for s, n in by_status.most_common():
    print(f'  {s}: {n}')
"

# 查看 submitted 里有没有超期未回音的
python -m tracking.cli stale --status submitted --days 60

# 查看 long_list 超 3 周没消息的
python -m tracking.cli stale --status long_list --days 21
```

---

## Quick Start：将 overseas_pipeline 中已分析的学校关联到 tracker

目前已有 2 所学校在 `overseas_pipeline/output/` 中有数据（Case Western、Monash）。将其与 tracker 中的记录关联：

```bash
# 1. 先找到对应的 app_id（按学校名搜索）
python -m tracking.cli list | grep -i "case western\|monash"

# 2. 找到 ID 后关联 pipeline 数据（以 Case Western 为例，假设 app_id=10）
python3 -c "
from tracking.tracking_db import ApplicationTracker
t = ApplicationTracker()

# Case Western
t.mark_researched(
    app_id=10,  # 替换为实际 ID
    pipeline_dir='overseas_pipeline/output/case_western_reserve_university',
    school_id='case_western_reserve_university',
    region='usa',
)
t.mark_analyzed(app_id=10, fit_score=5.0)   # 根据 fit_report.md 中的评分
print('Done')
"

# 3. 验证
python -m tracking.cli show 10
```

---

## Python API 快速参考

```python
from tracking.tracking_db import ApplicationTracker
tracker = ApplicationTracker()  # 默认 tracking/applications.db

# 写入
tracker.add_job(school, position, region, job_url, deadline, source, monitor_score, department)
tracker.mark_researched(app_id, pipeline_dir, school_id, department,
                        hci_density_target, hci_density_wide, hci_strategy,
                        high_overlap_count, data_quality)
tracker.mark_analyzed(app_id, fit_score)
tracker.mark_decision(app_id, go=False)        # go=False 设为 decision_nogo
tracker.mark_materials_ready(app_id)
tracker.mark_form_filling(app_id, form_url)
tracker.mark_submitted(app_id)
tracker.update_status(app_id, "long_list")     # 收邮件后手动更新
tracker.update_rec_letters(app_id, [{"name": "Ziang", "status": "submitted"}])
tracker.set_priority(app_id, "favorite")       # favorite/high/low/None

# 查询
tracker.get(app_id)                            # 单条详情
tracker.all_applications(status=None, priority_tag=None, region=None)
tracker.by_status("submitted")
tracker.upcoming_deadlines(days=7)
tracker.stale_applications("submitted", older_than_days=30)
tracker.dashboard_summary()                    # 全局概览 dict
tracker.status_history(app_id)                 # 状态变更日志
```

---

## 文件结构

```
tracking/
├── tracking_db.py      # 核心模块（ApplicationTracker 类）
├── cli.py              # CLI 工具（python -m tracking.cli ...）
├── migration.py        # 一次性：Google Sheet → SQLite
├── sheets_export.py    # SQLite → Excel / Google Sheets
├── applications.db     # 数据库（gitignored）
├── export_tracking.xlsx  # 导出文件（gitignored）
└── tests/
    ├── test_tracking_db.py
    └── test_migration.py
```

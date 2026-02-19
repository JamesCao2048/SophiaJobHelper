# 投递管理追踪系统 — 设计文档

**日期**: 2026-02-18
**状态**: Approved
**原始需求**: `general/plans/投递管理追踪系统.md`

---

## 1. 问题与目标

### 痛点
1. **缺乏 DDL/优先级管理** — Google Sheet 中 Deadline 只是文本字段，没有自动提醒，经常错过投递时间
2. **子系统无联动** — `faculty_monitor` 发现职位后手动录入 Sheet；`job_filling` 提交后手动更新状态；学校邮件反馈（reject/longlist/shortlist）也需手动维护

### 目标
- 建立以 **SQLite** 为核心的中央追踪数据库，**Google Sheets** 作为只读 dashboard
- 用 **pipeline-aware 状态模型** 替代 Google Sheet 的多列组合
- 各子系统通过 **共享 Python 库** 自动回写状态
- 提供 **CLI 查询** + **通知系统**（分阶段）

---

## 2. 数据模型

### 2.1 Pipeline 状态流

```
Discovered ── Filtered Out (not match / expired)
    │
    ▼
Researched (overseas_pipeline Step 1)
    │
    ▼
Analyzed (overseas_pipeline Step 2)
    │
    ▼
Decision ── NoGo (主动放弃)
    │
    ▼
Materials Ready (overseas_pipeline Step 3)
    │
    ▼
Form Filling (job_filling 填表中)
    │
    ▼
Submitted
    │
    ▼
Rec Requested → Rec Submitted (可选，学校通知推荐信)
    │
    ▼
Long List → Short List → Offer / Rejected
```

**状态 enum**:
```
discovered, filtered_out, researched, analyzed,
decision_nogo, materials_ready, form_filling, submitted,
rec_requested, rec_submitted,
long_list, short_list, offer, rejected
```

**正交维度**（不属于 pipeline 状态）:
- `priority_tag`: `favorite` / `high` / `low` / `NULL`
- DDL 是否超时: 计算字段 (`submitted_at` vs `deadline`)

### 2.2 SQLite Schema

```sql
CREATE TABLE applications (
    id                  INTEGER PRIMARY KEY,
    school              TEXT NOT NULL,           -- "University of Sydney"
    school_id           TEXT,                    -- "university_of_sydney" (overseas_pipeline key)
    department          TEXT,                    -- "School of Computer Science"
    region              TEXT,                    -- "australia", "usa", etc.
    position            TEXT,                    -- "Assistant Professor in HCI"
    job_url             TEXT,
    form_url            TEXT,                    -- job_filling 的表单 URL
    deadline            DATE,                   -- YYYY-MM-DD

    -- Pipeline 状态
    status              TEXT NOT NULL DEFAULT 'discovered',

    -- 关键时间戳
    discovered_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    researched_at       DATETIME,
    analyzed_at         DATETIME,
    materials_ready_at  DATETIME,
    form_filling_at     DATETIME,
    submitted_at        DATETIME,
    long_list_at        DATETIME,
    short_list_at       DATETIME,
    resolved_at         DATETIME,               -- offer/reject 时间

    -- 来源与优先级
    source              TEXT,                    -- "faculty_monitor", "manual", "google_sheet_import"
    priority_tag        TEXT,                    -- "favorite", "high", "low", NULL
    monitor_score       INTEGER,                -- faculty_monitor 关键词匹配评分

    -- overseas_pipeline 核心指标
    pipeline_dir        TEXT,                    -- "overseas_pipeline/output/university_of_sydney"
    fit_score           REAL,                    -- Step 2 fit score (1-10)
    hci_strategy        TEXT,                    -- "pioneer_with_allies" etc.
    hci_density_target  TEXT,                    -- none/few/many
    hci_density_wide    TEXT,                    -- none/few/many
    high_overlap_count  INTEGER,                -- 高匹配教授数
    data_quality        TEXT,                    -- high/medium/low

    -- 推荐信 (JSON array)
    rec_letters         TEXT,                   -- '[{"name":"Ziang","status":"submitted"}, ...]'

    notes               TEXT,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 状态变更日志
CREATE TABLE status_log (
    id              INTEGER PRIMARY KEY,
    application_id  INTEGER REFERENCES applications(id),
    old_status      TEXT,
    new_status      TEXT,
    changed_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    changed_by      TEXT                        -- "faculty_monitor", "job_filling", "manual", etc.
);
```

### 2.3 Google Sheet 状态映射

从现有 Google Sheet 导入时的映射规则：

| Google Sheet 状态 | → SQLite status |
|---|---|
| `Application Finalized` = 空 且有 University | `discovered` |
| `Application Finalized` = `not match` | `filtered_out` |
| `Application Finalized` = `expired/deadline passed` | `filtered_out` |
| `Application Finalized` = `Yes` 且 `Submission Date` 有值 | `submitted` |
| `Application Finalized` = `james_finish` 且 `Submission Date` 有值 | `submitted` |
| `Next Step` = `Rejection` | `rejected` |
| `Recommendation Letter Request` 有值 | `rec_requested` |
| `Recommendation Letter Submitted` = `Yes` | `rec_submitted` |

优先级映射：
- `My Followup` = `My favorite` / `my favoritate` → `priority_tag = 'favorite'`
- `My Followup` = `Low opportunities` → `priority_tag = 'low'`

---

## 3. Python API

### 3.1 模块位置

```
tracking/
├── __init__.py
├── tracking_db.py          -- 核心 DB 模块
├── cli.py                  -- CLI 入口
├── migration.py            -- Google Sheet → SQLite 导入
├── sheets_export.py        -- SQLite → Google Sheet 导出
└── applications.db         -- SQLite 数据库文件（gitignore）
```

### 3.2 API 设计

```python
# tracking/tracking_db.py

class ApplicationTracker:
    def __init__(self, db_path="tracking/applications.db"):
        """初始化数据库连接，自动创建表（如不存在）"""

    # === 写入 API ===

    def add_job(self, school, position, region=None, job_url=None,
                deadline=None, source="manual", monitor_score=None,
                department=None) -> int:
        """添加新职位，返回 app_id"""

    def mark_researched(self, app_id, pipeline_dir, school_id=None,
                        department=None, hci_density_target=None,
                        hci_density_wide=None, hci_strategy=None,
                        high_overlap_count=None, data_quality=None):
        """Step 1 完成"""

    def mark_analyzed(self, app_id, fit_score):
        """Step 2 完成"""

    def mark_decision(self, app_id, go: bool):
        """Go/NoGo 决策。go=False → status=decision_nogo"""

    def mark_materials_ready(self, app_id):
        """Step 3 完成"""

    def mark_form_filling(self, app_id, form_url=None):
        """开始填写表单"""

    def mark_submitted(self, app_id):
        """表单提交成功"""

    def update_status(self, app_id, new_status, changed_by="manual"):
        """通用状态更新（收到邮件后手动操作）"""

    def update_rec_letters(self, app_id, rec_letters: list):
        """更新推荐信状态。rec_letters: [{"name":"Ziang","status":"submitted"}, ...]"""

    def set_priority(self, app_id, priority_tag):
        """设置优先级: favorite/high/low/None"""

    # === 查询 API ===

    def get(self, app_id) -> dict:
        """获取单个申请详情"""

    def upcoming_deadlines(self, days=7) -> list:
        """返回 N 天内到期且未提交的申请"""

    def by_status(self, status) -> list:
        """按状态查询"""

    def stale_applications(self, status, older_than_days=14) -> list:
        """超过 N 天未推进的申请"""

    def dashboard_summary(self) -> dict:
        """总览：各状态计数 + 近期 DDL + stale 告警"""

    def all_applications(self, **filters) -> list:
        """查询所有申请，支持过滤"""

    def status_history(self, app_id) -> list:
        """查询状态变更日志"""
```

---

## 4. 子系统集成

### 4.1 faculty_monitor.py → 自动入库

```python
# 在 recommend_jobs() 末尾添加
from tracking.tracking_db import ApplicationTracker
tracker = ApplicationTracker()

for job in new_recommendations:
    tracker.add_job(
        school=job["title"],
        position=job["title"],
        region=job["region"],
        job_url=job["url"],
        source="faculty_monitor",
        monitor_score=job["score"]
    )
```

改动量：~10 行。

### 4.2 overseas_pipeline → Claude Code 指令

在 `overseas_pipeline/CLAUDE.md` 中添加约定：

- Step 1 完成后执行 `tracker.mark_researched(app_id, ...)`
- Step 2 完成后执行 `tracker.mark_analyzed(app_id, fit_score)`
- Step 3 完成后执行 `tracker.mark_materials_ready(app_id)`

Claude Code 通过 Bash 执行 Python 片段完成状态回写。

### 4.3 job_filling → 提交回写

`form_filler.py` 的 `apply` 命令成功后调用 `tracker.mark_submitted(app_id)`。

### 4.4 Google Sheets 同步

- **导出**：`sheets_export.py` 将 SQLite 数据按 region 分 sheet 导出
- **导入**（一次性）：`migration.py` 将现有 Google Sheet 数据导入 SQLite
- 导出后 Google Sheet 变为**只读 dashboard**，人工不再直接编辑 Sheet

---

## 5. CLI 命令

```bash
# 状态总览
python -m tracking.cli dashboard

# 查看近期 DDL
python -m tracking.cli upcoming 7

# 按状态查询
python -m tracking.cli list --status discovered
python -m tracking.cli list --status submitted --priority favorite

# 手动更新状态（收到邮件后）
python -m tracking.cli update 42 long_list
python -m tracking.cli update 42 rejected

# 设置优先级
python -m tracking.cli priority 42 favorite

# 查看单个申请详情 + 状态历史
python -m tracking.cli show 42

# 查看超期未推进的申请
python -m tracking.cli stale --days 14
```

---

## 6. 实施计划

### Phase 1：核心基建（最高优先级）
1. 创建 `tracking/` 目录
2. 实现 `tracking_db.py`（SQLite schema + Python API）
3. 实现 `tracking/cli.py`（dashboard, upcoming, list, update, show, stale）
4. 实现 `tracking/migration.py`（Google Sheet Excel → SQLite 导入）
5. 执行导入，验证数据完整性

### Phase 2：子系统集成
6. 改造 `faculty_monitor.py` — 新职位自动入库
7. 在 `overseas_pipeline/CLAUDE.md` 中添加状态回写指令
8. 改造 `job_filling/form_filler.py` — 提交后自动回写

### Phase 3：Google Sheets 双向同步
9. 实现 `tracking/sheets_export.py`（SQLite → Google Sheet 导出）
10. Google Sheet 转为只读 dashboard

### Phase 4：通知系统
11. DDL 提醒（cron + 邮件/微信通知）
12. Stale application 告警

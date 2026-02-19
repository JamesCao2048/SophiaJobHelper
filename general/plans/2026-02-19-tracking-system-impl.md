# 投递管理追踪系统 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a SQLite-backed application tracking system that integrates with faculty_monitor, overseas_pipeline, job_filling, and Google Sheets.

**Architecture:** Central `tracking/` Python package with `ApplicationTracker` class (SQLite), a `cli.py` CLI, a `migration.py` one-shot importer from the existing Google Sheet Excel, and a `sheets_export.py` exporter. Subsystems import and call `ApplicationTracker` directly.

**Tech Stack:** Python stdlib (sqlite3, argparse, json, datetime), openpyxl (already installed), gspread (already installed in google-sheets-sync)

**Design reference:** `general/plans/2026-02-18-tracking-system-design.md`

---

## Task 1: Scaffold tracking/ package + schema

**Files:**
- Create: `tracking/__init__.py`
- Create: `tracking/tracking_db.py`
- Create: `tracking/tests/__init__.py`
- Create: `tracking/tests/test_tracking_db.py`

**Step 1: Write failing tests for schema creation and add_job**

```python
# tracking/tests/test_tracking_db.py
import pytest
import sqlite3
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from tracking.tracking_db import ApplicationTracker

@pytest.fixture
def tracker(tmp_path):
    db_path = str(tmp_path / "test.db")
    return ApplicationTracker(db_path=db_path)

def test_tables_created(tracker):
    conn = sqlite3.connect(tracker.db_path)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    conn.close()
    assert "applications" in tables
    assert "status_log" in tables

def test_add_job_returns_id(tracker):
    app_id = tracker.add_job(school="MIT", position="Assistant Professor HCI")
    assert isinstance(app_id, int)
    assert app_id > 0

def test_add_job_default_status_is_discovered(tracker):
    app_id = tracker.add_job(school="MIT", position="Assistant Professor HCI")
    app = tracker.get(app_id)
    assert app["status"] == "discovered"

def test_add_job_stores_all_fields(tracker):
    app_id = tracker.add_job(
        school="Stanford", position="Assoc Prof", region="usa",
        job_url="https://example.com", deadline="2026-03-01",
        source="faculty_monitor", monitor_score=15, department="CS"
    )
    app = tracker.get(app_id)
    assert app["school"] == "Stanford"
    assert app["region"] == "usa"
    assert app["deadline"] == "2026-03-01"
    assert app["monitor_score"] == 15
    assert app["department"] == "CS"
```

**Step 2: Run test to verify fails**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m pytest tracking/tests/test_tracking_db.py -v 2>&1 | head -20
```
Expected: ImportError or ModuleNotFoundError

**Step 3: Create empty files**

```python
# tracking/__init__.py
# (empty)
```

```python
# tracking/tests/__init__.py
# (empty)
```

**Step 4: Implement tracking_db.py**

```python
# tracking/tracking_db.py
"""Central SQLite-backed application tracker."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List


VALID_STATUSES = {
    "discovered", "filtered_out", "researched", "analyzed",
    "decision_nogo", "materials_ready", "form_filling", "submitted",
    "rec_requested", "rec_submitted",
    "long_list", "short_list", "offer", "rejected",
}

VALID_PRIORITIES = {"favorite", "high", "low"}

STATUS_TIMESTAMPS = {
    "researched": "researched_at",
    "analyzed": "analyzed_at",
    "materials_ready": "materials_ready_at",
    "form_filling": "form_filling_at",
    "submitted": "submitted_at",
    "long_list": "long_list_at",
    "short_list": "short_list_at",
    "offer": "resolved_at",
    "rejected": "resolved_at",
}

_DEFAULT_DB = Path(__file__).parent / "applications.db"

CREATE_APPLICATIONS = """
CREATE TABLE IF NOT EXISTS applications (
    id                  INTEGER PRIMARY KEY,
    school              TEXT NOT NULL,
    school_id           TEXT,
    department          TEXT,
    region              TEXT,
    position            TEXT,
    job_url             TEXT,
    form_url            TEXT,
    deadline            DATE,
    status              TEXT NOT NULL DEFAULT 'discovered',
    discovered_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    researched_at       DATETIME,
    analyzed_at         DATETIME,
    materials_ready_at  DATETIME,
    form_filling_at     DATETIME,
    submitted_at        DATETIME,
    long_list_at        DATETIME,
    short_list_at       DATETIME,
    resolved_at         DATETIME,
    source              TEXT,
    priority_tag        TEXT,
    monitor_score       INTEGER,
    pipeline_dir        TEXT,
    fit_score           REAL,
    hci_strategy        TEXT,
    hci_density_target  TEXT,
    hci_density_wide    TEXT,
    high_overlap_count  INTEGER,
    data_quality        TEXT,
    rec_letters         TEXT,
    notes               TEXT,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_STATUS_LOG = """
CREATE TABLE IF NOT EXISTS status_log (
    id              INTEGER PRIMARY KEY,
    application_id  INTEGER REFERENCES applications(id),
    old_status      TEXT,
    new_status      TEXT,
    changed_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    changed_by      TEXT
)
"""


class ApplicationTracker:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = str(_DEFAULT_DB)
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._conn() as conn:
            conn.execute(CREATE_APPLICATIONS)
            conn.execute(CREATE_STATUS_LOG)

    def _now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log_status_change(self, conn, app_id: int, old_status: str, new_status: str, changed_by: str):
        conn.execute(
            "INSERT INTO status_log (application_id, old_status, new_status, changed_by) VALUES (?,?,?,?)",
            (app_id, old_status, new_status, changed_by),
        )

    # ── Write API ──────────────────────────────────────────────────────────

    def add_job(self, school: str, position: str, region: str = None,
                job_url: str = None, deadline: str = None,
                source: str = "manual", monitor_score: int = None,
                department: str = None) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """INSERT INTO applications
                   (school, position, region, job_url, deadline, source,
                    monitor_score, department, status, discovered_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,'discovered',?,?)""",
                (school, position, region, job_url, deadline, source,
                 monitor_score, department, self._now(), self._now()),
            )
            app_id = cur.lastrowid
            self._log_status_change(conn, app_id, None, "discovered", source or "manual")
            return app_id

    def mark_researched(self, app_id: int, pipeline_dir: str,
                        school_id: str = None, department: str = None,
                        hci_density_target: str = None, hci_density_wide: str = None,
                        hci_strategy: str = None, high_overlap_count: int = None,
                        data_quality: str = None):
        self._transition(app_id, "researched", "overseas_pipeline_step1",
                         pipeline_dir=pipeline_dir, school_id=school_id,
                         department=department, hci_density_target=hci_density_target,
                         hci_density_wide=hci_density_wide, hci_strategy=hci_strategy,
                         high_overlap_count=high_overlap_count, data_quality=data_quality)

    def mark_analyzed(self, app_id: int, fit_score: float):
        self._transition(app_id, "analyzed", "overseas_pipeline_step2",
                         fit_score=fit_score)

    def mark_decision(self, app_id: int, go: bool):
        new_status = "materials_ready" if go else "decision_nogo"
        # For Go we just set decision_nogo or leave at analyzed;
        # mark_materials_ready is called separately after Step 3
        if not go:
            self._transition(app_id, "decision_nogo", "manual")
        # go=True means proceed, caller then calls mark_materials_ready after Step 3

    def mark_materials_ready(self, app_id: int):
        self._transition(app_id, "materials_ready", "overseas_pipeline_step3")

    def mark_form_filling(self, app_id: int, form_url: str = None):
        kwargs = {}
        if form_url:
            kwargs["form_url"] = form_url
        self._transition(app_id, "form_filling", "job_filling", **kwargs)

    def mark_submitted(self, app_id: int):
        self._transition(app_id, "submitted", "job_filling")

    def update_status(self, app_id: int, new_status: str, changed_by: str = "manual"):
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}. Valid: {sorted(VALID_STATUSES)}")
        self._transition(app_id, new_status, changed_by)

    def update_rec_letters(self, app_id: int, rec_letters: list):
        now = self._now()
        with self._conn() as conn:
            conn.execute(
                "UPDATE applications SET rec_letters=?, updated_at=? WHERE id=?",
                (json.dumps(rec_letters), now, app_id),
            )

    def set_priority(self, app_id: int, priority_tag: Optional[str]):
        if priority_tag is not None and priority_tag not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority_tag}. Valid: {sorted(VALID_PRIORITIES)}")
        with self._conn() as conn:
            conn.execute(
                "UPDATE applications SET priority_tag=?, updated_at=? WHERE id=?",
                (priority_tag, self._now(), app_id),
            )

    def _transition(self, app_id: int, new_status: str, changed_by: str, **extra_fields):
        now = self._now()
        ts_col = STATUS_TIMESTAMPS.get(new_status)
        with self._conn() as conn:
            row = conn.execute("SELECT status FROM applications WHERE id=?", (app_id,)).fetchone()
            if row is None:
                raise ValueError(f"Application {app_id} not found")
            old_status = row["status"]

            # Build SET clause
            set_parts = ["status=?", "updated_at=?"]
            params = [new_status, now]
            if ts_col:
                set_parts.append(f"{ts_col}=?")
                params.append(now)
            for k, v in extra_fields.items():
                set_parts.append(f"{k}=?")
                params.append(v)
            params.append(app_id)

            conn.execute(
                f"UPDATE applications SET {', '.join(set_parts)} WHERE id=?",
                params,
            )
            self._log_status_change(conn, app_id, old_status, new_status, changed_by)

    # ── Query API ──────────────────────────────────────────────────────────

    def get(self, app_id: int) -> Optional[dict]:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM applications WHERE id=?", (app_id,)).fetchone()
            return dict(row) if row else None

    def upcoming_deadlines(self, days: int = 7) -> List[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT * FROM applications
                   WHERE deadline IS NOT NULL
                     AND deadline <= date('now', ?||' days')
                     AND deadline >= date('now')
                     AND status NOT IN ('submitted','rec_requested','rec_submitted',
                                        'long_list','short_list','offer','rejected',
                                        'filtered_out','decision_nogo')
                   ORDER BY deadline ASC""",
                (str(days),),
            ).fetchall()
            return [dict(r) for r in rows]

    def by_status(self, status: str) -> List[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM applications WHERE status=? ORDER BY deadline ASC NULLS LAST",
                (status,),
            ).fetchall()
            return [dict(r) for r in rows]

    def stale_applications(self, status: str, older_than_days: int = 14) -> List[dict]:
        ts_col = STATUS_TIMESTAMPS.get(status, "updated_at")
        with self._conn() as conn:
            rows = conn.execute(
                f"""SELECT * FROM applications
                    WHERE status=?
                      AND {ts_col} IS NOT NULL
                      AND {ts_col} < datetime('now', ?||' days')
                    ORDER BY {ts_col} ASC""",
                (status, f"-{older_than_days}"),
            ).fetchall()
            return [dict(r) for r in rows]

    def dashboard_summary(self) -> dict:
        with self._conn() as conn:
            counts = {}
            for row in conn.execute(
                "SELECT status, COUNT(*) as n FROM applications GROUP BY status"
            ).fetchall():
                counts[row["status"]] = row["n"]

            upcoming = self.upcoming_deadlines(7)
            stale_submitted = self.stale_applications("submitted", 30)
            stale_long_list = self.stale_applications("long_list", 21)

            return {
                "counts": counts,
                "total": sum(counts.values()),
                "upcoming_7d": upcoming,
                "stale_submitted_30d": stale_submitted,
                "stale_long_list_21d": stale_long_list,
            }

    def all_applications(self, status: str = None, priority_tag: str = None,
                         region: str = None) -> List[dict]:
        clauses, params = [], []
        if status:
            clauses.append("status=?")
            params.append(status)
        if priority_tag:
            clauses.append("priority_tag=?")
            params.append(priority_tag)
        if region:
            clauses.append("region=?")
            params.append(region)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._conn() as conn:
            rows = conn.execute(
                f"SELECT * FROM applications {where} ORDER BY deadline ASC NULLS LAST",
                params,
            ).fetchall()
            return [dict(r) for r in rows]

    def status_history(self, app_id: int) -> List[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM status_log WHERE application_id=? ORDER BY changed_at ASC",
                (app_id,),
            ).fetchall()
            return [dict(r) for r in rows]
```

**Step 5: Run tests**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m pytest tracking/tests/test_tracking_db.py -v
```
Expected: All 4 tests PASS

**Step 6: Commit**

```bash
cd /Users/junming/code/SophiaJobHelper
git add tracking/__init__.py tracking/tracking_db.py tracking/tests/__init__.py tracking/tests/test_tracking_db.py
git commit -m "feat: add ApplicationTracker core SQLite module"
```

---

## Task 2: Extend tests for write/query methods

**Files:**
- Modify: `tracking/tests/test_tracking_db.py`

**Step 1: Add tests for status transitions and query methods**

Append to `tracking/tests/test_tracking_db.py`:

```python
def test_mark_researched(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    tracker.mark_researched(app_id, pipeline_dir="overseas_pipeline/output/mit",
                            school_id="mit", hci_density_target="many",
                            hci_density_wide="many", data_quality="high")
    app = tracker.get(app_id)
    assert app["status"] == "researched"
    assert app["pipeline_dir"] == "overseas_pipeline/output/mit"
    assert app["hci_density_target"] == "many"
    assert app["researched_at"] is not None

def test_mark_analyzed(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    tracker.mark_researched(app_id, pipeline_dir="overseas_pipeline/output/mit")
    tracker.mark_analyzed(app_id, fit_score=8.5)
    app = tracker.get(app_id)
    assert app["status"] == "analyzed"
    assert app["fit_score"] == 8.5
    assert app["analyzed_at"] is not None

def test_mark_submitted(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    tracker.mark_submitted(app_id)
    app = tracker.get(app_id)
    assert app["status"] == "submitted"
    assert app["submitted_at"] is not None

def test_update_status_to_rejected(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    tracker.mark_submitted(app_id)
    tracker.update_status(app_id, "rejected")
    app = tracker.get(app_id)
    assert app["status"] == "rejected"
    assert app["resolved_at"] is not None

def test_update_status_invalid_raises(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    with pytest.raises(ValueError):
        tracker.update_status(app_id, "unicorn")

def test_status_history_logged(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    tracker.mark_submitted(app_id)
    tracker.update_status(app_id, "long_list")
    history = tracker.status_history(app_id)
    statuses = [h["new_status"] for h in history]
    assert "discovered" in statuses
    assert "submitted" in statuses
    assert "long_list" in statuses

def test_upcoming_deadlines(tracker):
    import datetime
    future = (datetime.date.today() + datetime.timedelta(days=3)).isoformat()
    app_id = tracker.add_job(school="MIT", position="Asst Prof", deadline=future)
    results = tracker.upcoming_deadlines(days=7)
    ids = [r["id"] for r in results]
    assert app_id in ids

def test_upcoming_deadlines_excludes_submitted(tracker):
    import datetime
    future = (datetime.date.today() + datetime.timedelta(days=3)).isoformat()
    app_id = tracker.add_job(school="Harvard", position="Prof", deadline=future)
    tracker.mark_submitted(app_id)
    results = tracker.upcoming_deadlines(days=7)
    ids = [r["id"] for r in results]
    assert app_id not in ids

def test_set_priority(tracker):
    app_id = tracker.add_job(school="MIT", position="Asst Prof")
    tracker.set_priority(app_id, "favorite")
    assert tracker.get(app_id)["priority_tag"] == "favorite"

def test_by_status(tracker):
    id1 = tracker.add_job(school="MIT", position="Asst Prof")
    id2 = tracker.add_job(school="Harvard", position="Prof")
    tracker.mark_submitted(id2)
    discovered = [r["id"] for r in tracker.by_status("discovered")]
    submitted = [r["id"] for r in tracker.by_status("submitted")]
    assert id1 in discovered
    assert id2 in submitted
    assert id2 not in discovered

def test_dashboard_summary(tracker):
    tracker.add_job(school="MIT", position="Asst Prof")
    tracker.add_job(school="Harvard", position="Prof")
    summary = tracker.dashboard_summary()
    assert summary["total"] == 2
    assert summary["counts"]["discovered"] == 2
```

**Step 2: Run tests**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m pytest tracking/tests/test_tracking_db.py -v
```
Expected: All 15 tests PASS

**Step 3: Commit**

```bash
git add tracking/tests/test_tracking_db.py
git commit -m "test: add comprehensive tests for ApplicationTracker write/query API"
```

---

## Task 3: Implement CLI

**Files:**
- Create: `tracking/cli.py`

**Step 1: Implement cli.py**

```python
# tracking/cli.py
"""CLI for application tracking.

Usage:
    python -m tracking.cli dashboard
    python -m tracking.cli upcoming [DAYS]
    python -m tracking.cli list [--status STATUS] [--priority PRIORITY]
    python -m tracking.cli update ID STATUS
    python -m tracking.cli priority ID TAG
    python -m tracking.cli show ID
    python -m tracking.cli stale [--status STATUS] [--days DAYS]
    python -m tracking.cli add SCHOOL POSITION [--region REGION] [--deadline DEADLINE]
"""

import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tracking.tracking_db import ApplicationTracker, VALID_STATUSES

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

STATUS_COLORS = {
    "discovered":     CYAN,
    "filtered_out":   "\033[90m",   # grey
    "researched":     CYAN,
    "analyzed":       CYAN,
    "decision_nogo":  "\033[90m",
    "materials_ready": YELLOW,
    "form_filling":   YELLOW,
    "submitted":      GREEN,
    "rec_requested":  YELLOW,
    "rec_submitted":  GREEN,
    "long_list":      GREEN,
    "short_list":     "\033[95m",   # magenta
    "offer":          "\033[95m",
    "rejected":       RED,
}

def colored_status(status: str) -> str:
    c = STATUS_COLORS.get(status, "")
    return f"{c}{status}{RESET}" if c else status

def fmt_app(a: dict, verbose=False) -> str:
    ddl = a.get("deadline") or "no DDL"
    priority = f"[{a['priority_tag']}]" if a.get("priority_tag") else ""
    fit = f" fit={a['fit_score']:.1f}" if a.get("fit_score") else ""
    school = a.get("school", "")[:40]
    pos = (a.get("position") or "")[:35]
    status = colored_status(a.get("status", ""))
    line = f"  #{a['id']:>4}  {school:<40}  {status:<25}  DDL:{ddl}  {priority}{fit}"
    if verbose and pos:
        line += f"\n         {pos}"
    return line


def cmd_dashboard(tracker: ApplicationTracker, _args):
    summary = tracker.dashboard_summary()
    print(f"\n{BOLD}=== Application Dashboard ==={RESET}")
    print(f"Total: {summary['total']}\n")

    print(f"{BOLD}By status:{RESET}")
    active_statuses = [
        "discovered", "researched", "analyzed", "materials_ready",
        "form_filling", "submitted", "rec_requested", "rec_submitted",
        "long_list", "short_list",
    ]
    for s in active_statuses:
        n = summary["counts"].get(s, 0)
        if n:
            print(f"  {colored_status(s):<35} {n}")
    closed = sum(summary["counts"].get(s, 0) for s in ["offer", "rejected", "filtered_out", "decision_nogo"])
    if closed:
        print(f"  {'(offer/rejected/filtered/nogo)':<35} {closed}")

    if summary["upcoming_7d"]:
        print(f"\n{BOLD}{YELLOW}⚠  Upcoming DDLs (7 days):{RESET}")
        for a in summary["upcoming_7d"]:
            print(fmt_app(a))

    if summary["stale_submitted_30d"]:
        print(f"\n{BOLD}Submitted 30+ days ago (no update):{RESET}")
        for a in summary["stale_submitted_30d"]:
            print(fmt_app(a))

    if summary["stale_long_list_21d"]:
        print(f"\n{BOLD}Long list 21+ days ago (no update):{RESET}")
        for a in summary["stale_long_list_21d"]:
            print(fmt_app(a))


def cmd_upcoming(tracker: ApplicationTracker, args):
    days = int(getattr(args, "days", 7) or 7)
    apps = tracker.upcoming_deadlines(days)
    print(f"\nUpcoming DDLs (next {days} days): {len(apps)}")
    for a in apps:
        print(fmt_app(a))


def cmd_list(tracker: ApplicationTracker, args):
    apps = tracker.all_applications(
        status=getattr(args, "status", None),
        priority_tag=getattr(args, "priority", None),
    )
    status_filter = getattr(args, "status", None) or "all"
    print(f"\nApplications [{status_filter}]: {len(apps)}")
    for a in apps:
        print(fmt_app(a))


def cmd_update(tracker: ApplicationTracker, args):
    app_id = int(args.id)
    new_status = args.new_status
    tracker.update_status(app_id, new_status, changed_by="manual")
    app = tracker.get(app_id)
    print(f"#{app_id} {app['school']} → {colored_status(new_status)}")


def cmd_priority(tracker: ApplicationTracker, args):
    app_id = int(args.id)
    tag = args.tag if args.tag != "none" else None
    tracker.set_priority(app_id, tag)
    print(f"#{app_id} priority → {tag}")


def cmd_show(tracker: ApplicationTracker, args):
    app_id = int(args.id)
    app = tracker.get(app_id)
    if not app:
        print(f"Application #{app_id} not found")
        sys.exit(1)
    print(f"\n{BOLD}#{app_id} — {app['school']}{RESET}")
    fields = [
        ("Position", "position"), ("Department", "department"),
        ("Region", "region"), ("Status", "status"),
        ("Deadline", "deadline"), ("Priority", "priority_tag"),
        ("Job URL", "job_url"), ("Form URL", "form_url"),
        ("Fit Score", "fit_score"), ("HCI Strategy", "hci_strategy"),
        ("HCI Density (dept/wide)", None),
        ("Data Quality", "data_quality"), ("Pipeline Dir", "pipeline_dir"),
        ("Source", "source"), ("Monitor Score", "monitor_score"),
        ("Discovered", "discovered_at"), ("Submitted", "submitted_at"),
        ("Long List", "long_list_at"), ("Notes", "notes"),
    ]
    for label, key in fields:
        if key is None:  # special
            val = f"{app.get('hci_density_target','?')} / {app.get('hci_density_wide','?')}"
        else:
            val = app.get(key)
        if val:
            print(f"  {label:<30} {val}")

    if app.get("rec_letters"):
        import json
        letters = json.loads(app["rec_letters"])
        print(f"  {'Rec Letters':<30}")
        for l in letters:
            print(f"    {l.get('name','?')}: {l.get('status','?')}")

    history = tracker.status_history(app_id)
    if history:
        print(f"\n  {BOLD}Status History:{RESET}")
        for h in history:
            print(f"    {h['changed_at']}  {h.get('old_status','–') or '–'} → {colored_status(h['new_status'])}  ({h.get('changed_by','')})")


def cmd_stale(tracker: ApplicationTracker, args):
    status = getattr(args, "status", None) or "submitted"
    days = int(getattr(args, "days", 14) or 14)
    apps = tracker.stale_applications(status, days)
    print(f"\nStale [{status}] >={days} days: {len(apps)}")
    for a in apps:
        print(fmt_app(a, verbose=True))


def cmd_add(tracker: ApplicationTracker, args):
    app_id = tracker.add_job(
        school=args.school,
        position=args.position,
        region=getattr(args, "region", None),
        deadline=getattr(args, "deadline", None),
        source="manual",
    )
    print(f"Added #{app_id}: {args.school}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Application tracker CLI")
    parser.add_argument("--db", default=None, help="Path to SQLite DB (default: tracking/applications.db)")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("dashboard", help="Show overall dashboard")

    p_upcoming = sub.add_parser("upcoming", help="Show upcoming DDLs")
    p_upcoming.add_argument("days", nargs="?", default=7, type=int)

    p_list = sub.add_parser("list", help="List applications")
    p_list.add_argument("--status", help="Filter by status")
    p_list.add_argument("--priority", help="Filter by priority tag")

    p_update = sub.add_parser("update", help="Update application status")
    p_update.add_argument("id", help="Application ID")
    p_update.add_argument("new_status", help="New status")

    p_priority = sub.add_parser("priority", help="Set priority tag")
    p_priority.add_argument("id", help="Application ID")
    p_priority.add_argument("tag", help="Priority tag (favorite/high/low/none)")

    p_show = sub.add_parser("show", help="Show application details + history")
    p_show.add_argument("id", help="Application ID")

    p_stale = sub.add_parser("stale", help="Show stale applications")
    p_stale.add_argument("--status", default="submitted")
    p_stale.add_argument("--days", default=14, type=int)

    p_add = sub.add_parser("add", help="Manually add an application")
    p_add.add_argument("school")
    p_add.add_argument("position")
    p_add.add_argument("--region")
    p_add.add_argument("--deadline")

    args = parser.parse_args(argv)
    tracker = ApplicationTracker(db_path=args.db)

    dispatch = {
        "dashboard": cmd_dashboard,
        "upcoming": cmd_upcoming,
        "list": cmd_list,
        "update": cmd_update,
        "priority": cmd_priority,
        "show": cmd_show,
        "stale": cmd_stale,
        "add": cmd_add,
    }

    if args.command not in dispatch:
        parser.print_help()
        sys.exit(1)

    dispatch[args.command](tracker, args)


if __name__ == "__main__":
    main()
```

**Step 2: Smoke-test CLI with a temp DB**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m tracking.cli --db /tmp/test_tracking.db dashboard
python -m tracking.cli --db /tmp/test_tracking.db add "Test University" "Asst Prof HCI" --region usa --deadline 2026-03-15
python -m tracking.cli --db /tmp/test_tracking.db dashboard
python -m tracking.cli --db /tmp/test_tracking.db show 1
python -m tracking.cli --db /tmp/test_tracking.db update 1 submitted
python -m tracking.cli --db /tmp/test_tracking.db show 1
```
Expected: No errors; dashboard shows 1 application; show displays details; update changes status.

**Step 3: Commit**

```bash
git add tracking/cli.py
git commit -m "feat: add CLI for application tracker (dashboard, list, update, show, stale)"
```

---

## Task 4: Implement migration.py (Google Sheet → SQLite)

**Files:**
- Create: `tracking/migration.py`
- Create: `tracking/tests/test_migration.py`

**Step 1: Write failing test for migration**

```python
# tracking/tests/test_migration.py
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from tracking.tracking_db import ApplicationTracker
from tracking.migration import migrate_from_excel

EXCEL_PATH = Path(__file__).parent.parent.parent / "google-sheets-sync" / "agent_sophia_job_list.xlsx"

@pytest.fixture
def tracker(tmp_path):
    return ApplicationTracker(db_path=str(tmp_path / "test.db"))

def test_migration_loads_data(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    stats = migrate_from_excel(str(EXCEL_PATH), tracker)
    assert stats["total_imported"] > 0
    apps = tracker.all_applications()
    assert len(apps) > 0

def test_migration_maps_submitted_status(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    migrate_from_excel(str(EXCEL_PATH), tracker)
    submitted = tracker.by_status("submitted")
    # Most rows in the sheet have Application Finalized = Yes + Submission Date
    assert len(submitted) > 50

def test_migration_maps_filtered_status(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    migrate_from_excel(str(EXCEL_PATH), tracker)
    filtered = tracker.by_status("filtered_out")
    # 'not match' and 'expired' rows
    assert len(filtered) > 0

def test_migration_maps_rejected_status(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    migrate_from_excel(str(EXCEL_PATH), tracker)
    rejected = tracker.by_status("rejected")
    assert len(rejected) > 0

def test_migration_maps_priority(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    migrate_from_excel(str(EXCEL_PATH), tracker)
    all_apps = tracker.all_applications()
    favorites = [a for a in all_apps if a.get("priority_tag") == "favorite"]
    assert len(favorites) > 0
```

**Step 2: Run to verify fails**

```bash
python -m pytest tracking/tests/test_migration.py -v 2>&1 | head -10
```
Expected: ImportError

**Step 3: Implement migration.py**

```python
# tracking/migration.py
"""One-shot migration: Google Sheet Excel → SQLite.

Column indices (0-based) for sheets US/NonUS/HKMacauSingapore/国内:
  0: Deadline
  1: University
  2: Positions
  3: Application Finalized
  4: Submission Date
  5: Whether on time?
  6: Recommendation Letter Request
  7: Recommendation Letter Submitted
  8: Submission Recheck
  9: Next Step
  10: My Followup  (国内 has Faculty contact at 10, Next Step at 11, Followup at 12)
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import openpyxl
from tracking.tracking_db import ApplicationTracker

# Sheet name → region
SHEET_REGIONS = {
    "US": "usa",
    "NonUS": "non_us_international",
    "HKMacauSingapore": "hk_macau_singapore",
    "国内": "china_mainland",
}

# For 国内 sheet, columns shift by 1 for Next Step / Followup
SHEET_COL_OFFSETS = {
    "国内": 1,  # Next Step at col 11, Followup at col 12
}


def _parse_deadline(raw) -> str:
    """Convert raw deadline like '12.1', '1.15' to ISO date string."""
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s.lower() in ("none", ""):
        return None
    # Handle "MM.DD" or "MM/DD" format; assume current or next year
    for sep in (".", "/", "-"):
        if sep in s:
            parts = s.split(sep)
            if len(parts) == 2:
                try:
                    m, d = int(parts[0]), int(parts[1])
                    # Application cycle: assume 2024/2025 season
                    # Months >= 8: assume 2024; months < 8: assume 2025
                    year = 2024 if m >= 8 else 2025
                    return f"{year}-{m:02d}-{d:02d}"
                except ValueError:
                    pass
    return None


def _map_status_and_priority(row, col_offset=0):
    """Return (status, priority_tag, rec_letters_info) from a sheet row."""
    app_finalized = str(row[3] or "").strip().lower()
    submission_date = row[4]
    rec_request = str(row[6] or "").strip()
    rec_submitted = str(row[7] or "").strip().lower()
    next_step_idx = 9 + col_offset
    followup_idx = 10 + col_offset
    next_step = str(row[next_step_idx] if len(row) > next_step_idx else "").strip().lower()
    followup = str(row[followup_idx] if len(row) > followup_idx else "").strip().lower()

    # Priority
    priority_tag = None
    if "favorite" in followup or "favourite" in followup:
        priority_tag = "favorite"
    elif "low" in followup:
        priority_tag = "low"

    # Status (most specific wins)
    status = "discovered"

    if app_finalized in ("not match", "not_match"):
        status = "filtered_out"
    elif "expired" in app_finalized or "deadline passed" in app_finalized:
        status = "filtered_out"
    elif app_finalized in ("yes", "james_finish") and submission_date:
        status = "submitted"
        # Override with more specific post-submission statuses
        if "rejection" in next_step:
            status = "rejected"
        elif rec_submitted in ("yes",):
            status = "rec_submitted"
        elif rec_request:
            status = "rec_requested"
    elif app_finalized in ("yes", "james_finish") and not submission_date:
        # Finalized but no submission date — treat as materials_ready
        status = "materials_ready"

    # Rec letters
    rec_letters = []
    if rec_request:
        rec_letters.append({"source": rec_request, "status": "requested"})
    if rec_submitted in ("yes",):
        if rec_letters:
            rec_letters[0]["status"] = "submitted"
        else:
            rec_letters.append({"source": "unknown", "status": "submitted"})

    return status, priority_tag, rec_letters


def migrate_from_excel(excel_path: str, tracker: ApplicationTracker,
                       dry_run: bool = False) -> dict:
    """Import all applications from the Google Sheet Excel file.

    Returns stats dict with counts.
    """
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    stats = {"total_imported": 0, "skipped_empty": 0, "by_sheet": {}}

    for sheet_name, region in SHEET_REGIONS.items():
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        col_offset = SHEET_COL_OFFSETS.get(sheet_name, 0)
        sheet_count = 0

        for row_cells in ws.iter_rows(min_row=2, values_only=True):
            # Skip empty rows
            school = str(row_cells[1] or "").strip()
            if not school:
                stats["skipped_empty"] += 1
                continue

            position = str(row_cells[2] or "").strip()
            deadline_raw = row_cells[0]
            deadline = _parse_deadline(deadline_raw)

            status, priority_tag, rec_letters = _map_status_and_priority(
                row_cells, col_offset
            )

            # submission_date for submitted_at timestamp
            submission_date_raw = row_cells[4]
            submission_date = _parse_deadline(submission_date_raw) if submission_date_raw else None

            if not dry_run:
                app_id = tracker.add_job(
                    school=school,
                    position=position,
                    region=region,
                    deadline=deadline,
                    source="google_sheet_import",
                )
                # Update to correct status if not discovered
                if status != "discovered":
                    tracker.update_status(app_id, status, changed_by="google_sheet_import")
                # Fix submitted_at if we have submission date
                if status in ("submitted", "rec_requested", "rec_submitted", "rejected") and submission_date:
                    from tracking.tracking_db import _DEFAULT_DB
                    import sqlite3
                    conn = sqlite3.connect(tracker.db_path)
                    conn.execute("UPDATE applications SET submitted_at=? WHERE id=?",
                                 (submission_date + " 00:00:00", app_id))
                    conn.commit()
                    conn.close()
                if priority_tag:
                    tracker.set_priority(app_id, priority_tag)
                if rec_letters:
                    tracker.update_rec_letters(app_id, rec_letters)

            sheet_count += 1
            stats["total_imported"] += 1

        stats["by_sheet"][sheet_name] = sheet_count

    return stats


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Migrate Google Sheet Excel → SQLite tracker")
    parser.add_argument("excel", nargs="?",
                        default="google-sheets-sync/agent_sophia_job_list.xlsx",
                        help="Path to Excel file")
    parser.add_argument("--db", default=None, help="Path to SQLite DB")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tracker = ApplicationTracker(db_path=args.db)
    print(f"Migrating from: {args.excel}")
    print(f"Target DB: {tracker.db_path}")
    if args.dry_run:
        print("DRY RUN — no data will be written")

    stats = migrate_from_excel(args.excel, tracker, dry_run=args.dry_run)
    print(f"\nDone!")
    print(f"  Total imported: {stats['total_imported']}")
    print(f"  Skipped empty rows: {stats['skipped_empty']}")
    print(f"  By sheet:")
    for sheet, n in stats["by_sheet"].items():
        print(f"    {sheet}: {n}")


if __name__ == "__main__":
    main()
```

**Step 4: Run migration tests**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m pytest tracking/tests/test_migration.py -v
```
Expected: All tests PASS (or SKIP if Excel not found)

**Step 5: Run actual migration on real data**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m tracking.migration google-sheets-sync/agent_sophia_job_list.xlsx
```
Expected: Print summary with total_imported > 100

**Step 6: Verify with dashboard**

```bash
python -m tracking.cli dashboard
```
Expected: Dashboard shows counts across multiple statuses

**Step 7: Spot-check a few records**

```bash
python -m tracking.cli list --status submitted | head -20
python -m tracking.cli list --status rejected | head -10
python -m tracking.cli list --status filtered_out | head -10
```

**Step 8: Commit**

```bash
git add tracking/migration.py tracking/tests/test_migration.py
git commit -m "feat: add Google Sheet → SQLite migration + import real data"
```

---

## Task 5: Integrate faculty_monitor.py

**Files:**
- Modify: `faculty-application_script/faculty_monitor.py`

**Step 1: Read the main() function in faculty_monitor.py**

Already done above — lines 789-829.

**Step 2: Add integration at the end of main()**

Edit `faculty-application_script/faculty_monitor.py`, append after line 815 (after `write_recommendations`):

```python
    # 6. 写入追踪数据库
    try:
        import sys, os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        from tracking.tracking_db import ApplicationTracker
        tracker = ApplicationTracker()
        added = 0
        for job in recommended:
            app_id = tracker.add_job(
                school=job.get("title", "")[:80],
                position=job.get("title", ""),
                region=job.get("region"),
                job_url=job.get("url"),
                source="faculty_monitor",
                monitor_score=job.get("score"),
            )
            added += 1
        log(f"📊 已将 {added} 个推荐职位写入追踪数据库 (ID 起始: {app_id - added + 1})")
    except Exception as e:
        log(f"⚠️  追踪数据库写入失败（不影响主功能）: {e}")
```

**Step 3: Smoke-test faculty_monitor integration**

```bash
cd /Users/junming/code/SophiaJobHelper/faculty-application_script
python faculty_monitor.py 2>&1 | tail -5
```
Expected: Last line includes "已将 N 个推荐职位写入追踪数据库" or "追踪数据库写入失败" if network issue

**Step 4: Commit**

```bash
git add faculty-application_script/faculty_monitor.py
git commit -m "feat: integrate faculty_monitor with ApplicationTracker (auto-add discovered jobs)"
```

---

## Task 6: Integrate job_filling/form_filler.py

**Files:**
- Modify: `job_filling/form_filler.py`

**Step 1: Read cmd_apply in form_filler.py**

```bash
grep -n "async def cmd_apply\|async def cmd_submit\|print.*submitted\|success" /Users/junming/code/SophiaJobHelper/job_filling/form_filler.py | head -20
```

**Step 2: Add --app-id argument and tracker callback to cmd_apply**

In `form_filler.py` main(), after the apply_parser definition (around line 545), add:
```python
apply_parser.add_argument("--app-id", type=int, default=None,
                          help="Tracking DB application ID to update on submit")
```

Then find `cmd_apply` and add at the end (after successful apply):
```python
    # Update tracker if app_id provided
    if hasattr(args, 'app_id') and args.app_id:
        try:
            import sys, os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
            from tracking.tracking_db import ApplicationTracker
            tracker = ApplicationTracker()
            tracker.mark_submitted(args.app_id)
            print(f"✓ Tracker updated: #{args.app_id} → submitted")
        except Exception as e:
            print(f"⚠  Tracker update failed (non-fatal): {e}")
```

**Step 3: Find exact location of cmd_apply**

```bash
grep -n "async def cmd_apply" /Users/junming/code/SophiaJobHelper/job_filling/form_filler.py
```

**Step 4: Read cmd_apply function body**

Read form_filler.py around the cmd_apply function to find exact insertion point.

**Step 5: Commit**

```bash
git add job_filling/form_filler.py
git commit -m "feat: integrate job_filling with ApplicationTracker (mark_submitted on apply)"
```

---

## Task 7: Update overseas_pipeline CLAUDE.md

**Files:**
- Modify: `overseas_pipeline/CLAUDE.md`

**Step 1: Read existing CLAUDE.md**

```bash
cat /Users/junming/code/SophiaJobHelper/overseas_pipeline/CLAUDE.md | head -50
```

**Step 2: Append tracking integration instructions**

Add a new section at the end of `overseas_pipeline/CLAUDE.md`:

```markdown
## 📊 追踪数据库集成（ApplicationTracker）

overseas_pipeline 完成每个 Step 后，需要更新追踪数据库。

### 获取 app_id
在开始研究某个学校前，先查找或创建 tracking 记录：
```python
from tracking.tracking_db import ApplicationTracker
tracker = ApplicationTracker()
# 查找已有记录
apps = tracker.all_applications()
match = next((a for a in apps if school_id in (a.get("school_id") or "")), None)
if match:
    app_id = match["id"]
else:
    app_id = tracker.add_job(school=school_name, position=job_title, region=region)
```

### Step 1 完成后
```python
tracker.mark_researched(
    app_id=app_id,
    pipeline_dir=f"overseas_pipeline/output/{school_id}",
    school_id=school_id,
    department=dept,                    # from faculty_data.json
    hci_density_target=hci_target,      # "none"/"few"/"many"
    hci_density_wide=hci_wide,
    hci_strategy=strategy,
    high_overlap_count=n,
    data_quality=quality,               # "high"/"medium"/"low"
)
```

### Step 2 完成后
```python
tracker.mark_analyzed(app_id=app_id, fit_score=fit_score)  # 1-10
```

### Step 3 完成后
```python
tracker.mark_materials_ready(app_id=app_id)
```

**注意**: 如果不确定 app_id，可以通过 `python -m tracking.cli list --status discovered` 查找对应记录，或用 `python -m tracking.cli add "School Name" "Position"` 手动创建。
```

**Step 3: Commit**

```bash
git add overseas_pipeline/CLAUDE.md
git commit -m "docs: add ApplicationTracker integration guide to overseas_pipeline CLAUDE.md"
```

---

## Task 8: Implement sheets_export.py (Phase 3)

**Files:**
- Create: `tracking/sheets_export.py`

**Step 1: Implement sheets_export.py**

```python
# tracking/sheets_export.py
"""Export SQLite tracking data back to Google Sheets format.

Creates/updates the same sheet structure as the original:
  US / NonUS / HKMacauSingapore / 国内

Run:
    python -m tracking.sheets_export
    python -m tracking.sheets_export --dry-run  # print instead of upload
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
from datetime import datetime
from tracking.tracking_db import ApplicationTracker

# Region → sheet name mapping
REGION_SHEETS = {
    "usa": "US",
    "non_us_international": "NonUS",
    "hk_macau_singapore": "HKMacauSingapore",
    "china_mainland": "国内",
}

# Status → Application Finalized column value
STATUS_TO_FINALIZED = {
    "submitted": "Yes",
    "rec_requested": "Yes",
    "rec_submitted": "Yes",
    "long_list": "Yes",
    "short_list": "Yes",
    "offer": "Yes",
    "rejected": "Yes",
    "materials_ready": "Yes",
    "filtered_out": "not match",
    "decision_nogo": "not match",
}

STATUS_TO_NEXT_STEP = {
    "rejected": "Rejection",
    "long_list": "Long List",
    "short_list": "Short List",
    "offer": "Offer",
    "rec_requested": "(Optional) Ask recommendation",
    "rec_submitted": "(Optional) Ask recommendation",
}


def _format_date(dt_str: str) -> str:
    """Convert YYYY-MM-DD or datetime string to M.D format for Google Sheet."""
    if not dt_str:
        return ""
    try:
        d = datetime.strptime(dt_str[:10], "%Y-%m-%d")
        return f"{d.month}.{d.day}"
    except ValueError:
        return ""


def build_row(app: dict) -> list:
    """Build a Google Sheet row from an application dict."""
    status = app.get("status", "discovered")
    deadline = _format_date(app.get("deadline"))
    school = app.get("school", "")
    position = app.get("position", "")
    app_finalized = STATUS_TO_FINALIZED.get(status, "")
    submission_date = _format_date(app.get("submitted_at")) if app.get("submitted_at") else ""
    on_time = "Yes" if (app.get("submitted_at") and app.get("deadline") and
                        app.get("submitted_at")[:10] <= app.get("deadline")) else ""

    # Rec letters
    import json
    rec_letters = []
    if app.get("rec_letters"):
        try:
            rec_letters = json.loads(app["rec_letters"])
        except Exception:
            pass
    rec_request = rec_letters[0].get("source", "") if rec_letters else ""
    rec_submitted = "Yes" if any(l.get("status") == "submitted" for l in rec_letters) else ""

    next_step = STATUS_TO_NEXT_STEP.get(status, "")

    # Priority → My Followup
    priority_map = {"favorite": "My favorite", "low": "Low opportunities"}
    followup = priority_map.get(app.get("priority_tag", ""), "")

    # Fit score in notes
    notes = ""
    if app.get("fit_score"):
        notes = f"fit={app['fit_score']:.1f}"
    if app.get("hci_strategy"):
        notes += f" strategy={app['hci_strategy']}"

    return [
        deadline, school, position, app_finalized,
        submission_date, on_time, rec_request, rec_submitted,
        "",  # Submission Recheck
        next_step, followup, notes,
    ]


def export_to_excel(tracker: ApplicationTracker, output_path: str):
    """Export all apps to an Excel file matching the Google Sheet structure."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, PatternFill

    HEADERS = [
        "Deadline", "University", "Positions", "Application Finalized",
        "Submission Date", "Whether on time?", "Recommendation Letter Request",
        "Recommendation Letter Submitted", "Submission Recheck",
        "Next Step", "My Followup", "Notes (auto)",
    ]

    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default sheet

    for region, sheet_name in REGION_SHEETS.items():
        apps = tracker.all_applications(region=region)
        if not apps:
            continue
        ws = wb.create_sheet(sheet_name)
        ws.append(HEADERS)
        for app in apps:
            ws.append(build_row(app))

    wb.save(output_path)
    print(f"Exported {sum(len(tracker.all_applications(region=r)) for r in REGION_SHEETS)} apps to {output_path}")


def export_to_gsheets(tracker: ApplicationTracker, credentials_path: str,
                      spreadsheet_id: str):
    """Upload to Google Sheets via gspread."""
    import gspread
    from google.oauth2.service_account import Credentials

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)

    HEADERS = [
        "Deadline", "University", "Positions", "Application Finalized",
        "Submission Date", "Whether on time?", "Recommendation Letter Request",
        "Recommendation Letter Submitted", "Submission Recheck",
        "Next Step", "My Followup", "Notes (auto)",
    ]

    for region, sheet_name in REGION_SHEETS.items():
        apps = tracker.all_applications(region=region)
        if not apps:
            continue
        try:
            ws = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=20)

        rows = [HEADERS] + [build_row(a) for a in apps]
        ws.clear()
        ws.update(rows)
        print(f"  {sheet_name}: {len(apps)} rows uploaded")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=None)
    parser.add_argument("--output", default="tracking/export_tracking.xlsx",
                        help="Output Excel path (local export)")
    parser.add_argument("--gsheets", action="store_true",
                        help="Upload to Google Sheets (requires credentials)")
    parser.add_argument("--credentials",
                        default="google-sheets-sync/credentials/service_account.json")
    parser.add_argument("--spreadsheet-id",
                        default=os.getenv("SPREADSHEET_ID", ""))
    args = parser.parse_args()

    tracker = ApplicationTracker(db_path=args.db)

    if args.gsheets:
        print("Uploading to Google Sheets...")
        export_to_gsheets(tracker, args.credentials, args.spreadsheet_id)
    else:
        export_to_excel(tracker, args.output)


if __name__ == "__main__":
    main()
```

**Step 2: Test local Excel export**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m tracking.sheets_export --output /tmp/tracking_export.xlsx
```
Expected: "Exported N apps to /tmp/tracking_export.xlsx"

**Step 3: Verify exported Excel**

```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('/tmp/tracking_export.xlsx')
print('Sheets:', wb.sheetnames)
for name in wb.sheetnames:
    ws = wb[name]
    print(f'{name}: {ws.max_row-1} rows')
"
```
Expected: Sheets US/NonUS/HKMacauSingapore/国内 with row counts > 0

**Step 4: Commit**

```bash
git add tracking/sheets_export.py
git commit -m "feat: add sheets_export to push SQLite data back to Google Sheets format"
```

---

## Task 9: Add .gitignore entry for DB file

**Files:**
- Modify: `.gitignore` (create if not exists)

**Step 1: Check if .gitignore exists**

```bash
ls /Users/junming/code/SophiaJobHelper/.gitignore 2>/dev/null || echo "not found"
```

**Step 2: Add tracking DB to gitignore**

```bash
echo "tracking/applications.db" >> /Users/junming/code/SophiaJobHelper/.gitignore
echo "tracking/export_tracking.xlsx" >> /Users/junming/code/SophiaJobHelper/.gitignore
```

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore tracking DB and export files"
```

---

## Task 10: End-to-end verification

**Step 1: Run all tests**

```bash
cd /Users/junming/code/SophiaJobHelper
python -m pytest tracking/tests/ -v
```
Expected: All tests PASS

**Step 2: Verify full CLI workflow**

```bash
# Dashboard with real data
python -m tracking.cli dashboard

# List submitted applications
python -m tracking.cli list --status submitted | head -15

# Upcoming DDLs
python -m tracking.cli upcoming 30

# Show one application detail
python -m tracking.cli show 1

# Manually update status
python -m tracking.cli add "Test School" "Test Position" --region usa --deadline 2026-04-01
python -m tracking.cli dashboard  # should show +1 discovered
python -m tracking.cli update $(python -m tracking.cli list --status discovered | tail -1 | awk '{print $1}' | tr -d '#') long_list
```

**Step 3: Verify migration completeness**

```bash
python3 -c "
from tracking.tracking_db import ApplicationTracker
t = ApplicationTracker()
s = t.dashboard_summary()
print('Status counts:', s['counts'])
print('Total:', s['total'])
"
```

**Step 4: Final commit (if any uncommitted changes)**

```bash
git status
git add -A
git commit -m "feat: complete application tracking system (Phase 1-3)"
```

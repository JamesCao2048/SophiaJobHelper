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
        if not go:
            self._transition(app_id, "decision_nogo", "manual")

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
                "SELECT * FROM applications WHERE status=? ORDER BY deadline ASC",
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
                f"SELECT * FROM applications {where} ORDER BY deadline ASC",
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

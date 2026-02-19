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

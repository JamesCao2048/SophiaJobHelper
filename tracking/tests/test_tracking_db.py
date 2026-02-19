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

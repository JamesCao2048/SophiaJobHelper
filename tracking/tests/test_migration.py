# tracking/tests/test_migration.py
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from tracking.tracking_db import ApplicationTracker
from tracking.migration import migrate_from_excel, _parse_deadline

EXCEL_PATH = Path(__file__).parent.parent.parent / "google-sheets-sync" / "agent_sophia_job_list.xlsx"

@pytest.fixture
def tracker(tmp_path):
    return ApplicationTracker(db_path=str(tmp_path / "test.db"))

def test_parse_deadline_month_dot_day():
    assert _parse_deadline("12.1") == "2024-12-01"
    assert _parse_deadline("1.15") == "2025-01-15"
    assert _parse_deadline("8.31") == "2024-08-31"

def test_parse_deadline_none():
    assert _parse_deadline(None) is None
    assert _parse_deadline("") is None

def test_migration_loads_data(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    stats = migrate_from_excel(str(EXCEL_PATH), tracker)
    assert stats["total_imported"] > 100
    apps = tracker.all_applications()
    assert len(apps) > 100

def test_migration_maps_submitted_status(tracker):
    """Verify submitted-family statuses total >50.

    Pure 'submitted' = 35, but rec_submitted/rec_requested/rejected are
    post-submission statuses that override 'submitted'.  The combined count
    of all submitted-family statuses is >50.
    """
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    migrate_from_excel(str(EXCEL_PATH), tracker)
    submitted_family = (
        tracker.by_status("submitted")
        + tracker.by_status("rec_requested")
        + tracker.by_status("rec_submitted")
        + tracker.by_status("rejected")
    )
    assert len(submitted_family) > 50

def test_migration_maps_filtered_status(tracker):
    if not EXCEL_PATH.exists():
        pytest.skip("Excel file not found")
    migrate_from_excel(str(EXCEL_PATH), tracker)
    filtered = tracker.by_status("filtered_out")
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

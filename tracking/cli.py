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
import json
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
    "filtered_out":   "\033[90m",
    "researched":     CYAN,
    "analyzed":       CYAN,
    "decision_nogo":  "\033[90m",
    "materials_ready": YELLOW,
    "form_filling":   YELLOW,
    "submitted":      GREEN,
    "rec_requested":  YELLOW,
    "rec_submitted":  GREEN,
    "long_list":      GREEN,
    "short_list":     "\033[95m",
    "offer":          "\033[95m",
    "rejected":       RED,
}

def colored_status(status: str) -> str:
    c = STATUS_COLORS.get(status, "")
    return f"{c}{status}{RESET}" if c else status

def fmt_app(a: dict, verbose: bool = False) -> str:
    ddl = a.get("deadline") or "no DDL"
    priority = f"[{a['priority_tag']}]" if a.get("priority_tag") else ""
    fit = f" fit={a['fit_score']:.1f}" if a.get("fit_score") else ""
    school = (a.get("school") or "")[:40]
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
    try:
        tracker.update_status(app_id, new_status, changed_by="manual")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    app = tracker.get(app_id)
    print(f"#{app_id} {app['school']} → {colored_status(new_status)}")


def cmd_priority(tracker: ApplicationTracker, args):
    app_id = int(args.id)
    tag = args.tag if args.tag != "none" else None
    try:
        tracker.set_priority(app_id, tag)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
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
        if key is None:
            val = f"{app.get('hci_density_target','?')} / {app.get('hci_density_wide','?')}"
        else:
            val = app.get(key)
        if val:
            print(f"  {label:<30} {val}")

    if app.get("rec_letters"):
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
    parser.add_argument("--db", default=None, help="Path to SQLite DB")
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

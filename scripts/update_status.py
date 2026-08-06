#!/usr/bin/env python3
"""Update an application's status in meta.json and regenerate the tracker.

Usage:
    update_status.py <application_dir_or_company> <new_status> [--note "..."] [--submitted] [--follow-up YYYY-MM-DD]

Status values: preparing, submitted, recruiter_screen, hiring_manager,
               onsite, offer, rejected, withdrawn
"""
import argparse
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = os.environ.get("JAA_REPO", "/Users/niiamon/work/cv")
APPLICATIONS_DIR = Path(REPO) / "applications"

VALID_STATUSES = {
    "preparing",
    "submitted",
    "recruiter_screen",
    "hiring_manager",
    "onsite",
    "offer",
    "rejected",
    "withdrawn",
}


def find_app_dir(query: str) -> Path:
    """Find application directory by name, slug, or path."""
    query = query.strip()

    # If it's a path that exists, use it directly
    p = Path(query)
    if p.is_absolute() and p.exists() and p.is_dir():
        return p

    # If it's a relative path under APPLICATIONS_DIR
    p = APPLICATIONS_DIR / query
    if p.exists() and p.is_dir():
        return p

    # Search by name (matches anywhere in directory name)
    q_lower = query.lower()
    q_slug = re.sub(r"[^a-z0-9]+", "-", q_lower).strip("-")

    matches = []
    if APPLICATIONS_DIR.exists():
        for entry in APPLICATIONS_DIR.iterdir():
            if not entry.is_dir():
                continue
            if q_lower in entry.name.lower() or q_slug in entry.name:
                matches.append(entry)

    if not matches:
        sys.exit(f"No application directory matches '{query}' under {APPLICATIONS_DIR}")
    if len(matches) > 1:
        print(f"Multiple matches for '{query}':", file=sys.stderr)
        for m in matches:
            print(f"  {m.name}", file=sys.stderr)
        sys.exit(1)
    return matches[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", help="Application directory name, slug, or path")
    parser.add_argument("status", help=f"One of: {', '.join(sorted(VALID_STATUSES))}")
    parser.add_argument("--note", default=None, help="Append a note to meta.notes")
    parser.add_argument(
        "--submitted",
        action="store_true",
        help="Set key_dates.submitted to today",
    )
    parser.add_argument(
        "--follow-up",
        default=None,
        help="Override next_follow_up date (YYYY-MM-DD). Default: today+7d for submitted.",
    )
    args = parser.parse_args()

    if args.status not in VALID_STATUSES:
        sys.exit(f"Invalid status '{args.status}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}")

    app_dir = find_app_dir(args.app)
    meta_path = app_dir / "meta.json"
    if not meta_path.exists():
        sys.exit(f"No meta.json at {meta_path}")

    meta = json.loads(meta_path.read_text())
    meta["status"] = args.status

    today = date.today().isoformat()
    key_dates = meta.setdefault("key_dates", {})

    if args.submitted or args.status == "submitted":
        key_dates["submitted"] = today
        key_dates["last_contact"] = today

    if args.status == "submitted" and not args.follow_up:
        follow_up = (date.today() + timedelta(days=7)).isoformat()
        key_dates["next_follow_up"] = follow_up
    elif args.follow_up:
        key_dates["next_follow_up"] = args.follow_up

    if args.status in {"recruiter_screen", "hiring_manager", "onsite", "offer", "rejected", "withdrawn"}:
        key_dates["last_contact"] = today

    if args.note:
        existing = meta.get("notes", "") or ""
        meta["notes"] = (existing + "\n" if existing else "") + f"[{today}] {args.note}"

    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Updated {app_dir.name}: status = {args.status}")

    # Regenerate tracker
    tracker_script = Path(__file__).parent / "regenerate_tracker.py"
    if tracker_script.exists():
        os.system(f"python3 {tracker_script}")


if __name__ == "__main__":
    main()

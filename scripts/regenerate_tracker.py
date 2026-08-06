#!/usr/bin/env python3
"""Scan applications/ directory and regenerate tracker.md.

Each application's meta.json is the source of truth. tracker.md is the
derived dashboard view.

Usage:
    regenerate_tracker.py [--repo REPO_PATH]
"""
import json
import os
import sys
from pathlib import Path


REPO = os.environ.get("JAA_REPO", "/Users/niiamon/work/cv")
APPLICATIONS_DIR = Path(REPO) / "applications"
TRACKER = Path(REPO) / "tracker.md"

STATUS_ORDER = {
    "preparing": 0,
    "submitted": 1,
    "recruiter_screen": 2,
    "hiring_manager": 3,
    "onsite": 4,
    "offer": 5,
    "rejected": 6,
    "withdrawn": 7,
}

ACTIVE_STATUSES = {"preparing", "submitted", "recruiter_screen", "hiring_manager", "onsite"}


def infer_from_folder_name(name: str) -> dict:
    """Infer company/role/date from a folder name like 'acme__vp-engineering__2026-07-21'."""
    parts = name.split("__")
    company = parts[0].replace("-", " ").title() if parts else name
    role = parts[1].replace("-", " ").title() if len(parts) > 1 else ""
    date = parts[2] if len(parts) > 2 else ""
    return {"company": company, "role": role, "date_created": date}


def load_apps():
    apps = []
    if not APPLICATIONS_DIR.exists():
        return apps
    for entry in sorted(APPLICATIONS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        # Skip hidden directories (e.g., .DS_Store residue)
        if entry.name.startswith("."):
            continue
        meta_path = entry / "meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
            except json.JSONDecodeError as e:
                print(f"Warning: bad meta.json in {entry.name}: {e}", file=sys.stderr)
                inferred = infer_from_folder_name(entry.name)
                meta = {
                    "company": inferred["company"],
                    "role": inferred["role"],
                    "status": "preparing",
                    "source": "unknown",
                    "fit_score": None,
                    "key_dates": {},
                    "_inferred": True,
                }
        else:
            # No meta.json — folder exists but not yet adopted by the agent
            inferred = infer_from_folder_name(entry.name)
            meta = {
                "company": inferred["company"],
                "role": inferred["role"],
                "status": "preparing",
                "source": "unknown",
                "fit_score": None,
                "key_dates": {},
                "_inferred": True,
                "_needs_adoption": True,
            }
        meta["_dir"] = entry.name
        apps.append(meta)
    return apps


def render_table(apps, status_filter=None):
    if not apps:
        return "_No applications yet._\n"
    rows = []
    header = "| Company | Role | Status | Source | Fit | Submitted | Next follow-up | Dir |\n"
    sep = "|---------|------|--------|--------|-----|-----------|----------------|-----|\n"
    out = header + sep
    for a in apps:
        if status_filter and a.get("status") not in status_filter:
            continue
        company = a.get("company", "?")
        if a.get("_needs_adoption"):
            company = f"{company} ⚠️"  # flag: folder not yet adopted
        role = a.get("role", "?")
        status = a.get("status", "?")
        source = a.get("source", "?")
        fit = a.get("fit_score")
        fit_str = f"{fit}" if fit is not None else "—"
        submitted = (a.get("key_dates") or {}).get("submitted") or "—"
        follow_up = (a.get("key_dates") or {}).get("next_follow_up") or "—"
        d = a.get("_dir", "")
        out += f"| {company} | {role} | {status} | {source} | {fit_str} | {submitted} | {follow_up} | `{d}` |\n"
    return out


def main():
    apps = load_apps()
    apps.sort(
        key=lambda a: (
            STATUS_ORDER.get(a.get("status", ""), 99),
            a.get("date_created", ""),
        )
    )

    active = [a for a in apps if a.get("status") in ACTIVE_STATUSES]
    closed = [a for a in apps if a.get("status") in {"rejected", "withdrawn"}]
    offers = [a for a in apps if a.get("status") == "offer"]

    today_iso = __import__("datetime").date.today().isoformat()

    lines = [
        "# Job Application Tracker",
        "",
        f"_Last regenerated: {today_iso}_",
        "",
        f"**Summary:** {len(active)} active · {len(offers)} offers · {len(closed)} closed · {len(apps)} total",
        "",
        "## Active",
        "",
        render_table(active),
        "## Offers",
        "",
        render_table(offers),
        "## Closed (rejected / withdrawn)",
        "",
        render_table(closed),
        "## All applications",
        "",
        render_table(apps),
    ]

    TRACKER.write_text("\n".join(lines))
    print(f"Wrote {TRACKER}")
    print(f"  {len(apps)} applications ({len(active)} active, {len(offers)} offers, {len(closed)} closed)")


if __name__ == "__main__":
    main()

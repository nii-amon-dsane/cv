#!/usr/bin/env python3
"""Scaffold a new job application directory.

Creates:
  {REPO}/applications/<company>__<role-slug>__<YYYY-MM-DD>/
      meta.json
      jd.txt
"""
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

REPO = os.environ.get("JAA_REPO", "/Users/niiamon/work/cv")
APPLICATIONS_DIR = Path(REPO) / "applications"

VALID_SOURCES = [
    "portal",
    "recruiter_cold",
    "warm_intro",
    "referral",
    "direct_outreach",
]

VALID_STATUSES = [
    "preparing",
    "submitted",
    "recruiter_screen",
    "hiring_manager",
    "onsite",
    "offer",
    "rejected",
    "withdrawn",
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def main():
    print("=== New Job Application ===\n")

    company = input("Company name (required): ").strip()
    if not company:
        sys.exit("Company is required.")

    role = input("Role title as posted (required): ").strip()
    if not role:
        sys.exit("Role is required.")

    print(f"\nSource options: {', '.join(VALID_SOURCES)}")
    source = input("Source (default: portal): ").strip() or "portal"
    if source not in VALID_SOURCES:
        sys.exit(f"Invalid source. Must be one of: {', '.join(VALID_SOURCES)}")

    recruiter_name = input("Recruiter name (optional, Enter to skip): ").strip() or None
    recruiter_linkedin = (
        input("Recruiter LinkedIn URL (optional, Enter to skip): ").strip() or None
    )

    ats_default = "true" if source == "portal" else "false"
    ats = (
        input(f"ATS optimize? (true/false, default: {ats_default}): ").strip()
        or ats_default
    ).lower() == "true"

    today = date.today().isoformat()
    dir_name = f"{slugify(company)}__{slugify(role)}__{today}"
    app_dir = APPLICATIONS_DIR / dir_name

    if app_dir.exists():
        sys.exit(f"Directory already exists: {app_dir}")

    app_dir.mkdir(parents=True)

    meta = {
        "company": company,
        "role": role,
        "date_created": today,
        "source": source,
        "recruiter": {
            "name": recruiter_name,
            "linkedin": recruiter_linkedin,
        },
        "status": "preparing",
        "ats_optimize": ats,
        "fit_score": None,
        "fit_breakdown": None,
        "gaps": [],
        "angle_confirmed": False,
        "linkedin_type": None,
        "key_dates": {
            "submitted": None,
            "last_contact": None,
            "next_follow_up": None,
        },
        "notes": "",
    }

    (app_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    (app_dir / "jd.txt").write_text(
        f"# Job Description: {company} — {role}\n\n# Paste the JD below this line.\n"
    )

    print(f"\nCreated: {app_dir}")
    print(f"Next: paste the JD into {app_dir / 'jd.txt'}")
    print(f"Then invoke the skill to run match analysis.")


if __name__ == "__main__":
    main()

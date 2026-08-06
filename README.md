# Job Application Agent

Customizes job applications per role for Nii Amon Dsane.

## What it does

Per job application, generates:
- Tailored CV (markdown + PDF)
- Cover letter (markdown + PDF)
- Recruiter email (plain text)
- LinkedIn message (plain text)
- Interview prep doc (markdown)
- Tracker entry (auto-logged)

Interactive multi-step workflow: paste JD → match analysis → confirm angle → batch-generate → revise in chat → log to tracker.

## Install location

This repo contains both the skill and the versioned state (profile, applications, tracker).

- **Repo (skill + state)**: `/Users/niiamon/work/cv`
- **Harness pointer** (how the harness discovers the skill): `~/.agents/skills/job-application-agent/SKILL.md` — a thin pointer that redirects to `/Users/niiamon/work/cv/SKILL.md`

## Dependencies

- `pandoc` (PDF rendering)
- `typst` (PDF engine, lightweight)
- `python3` (scripts)

Install via Homebrew:
```bash
brew install pandoc typst
```

## First-time setup

If `profile/preferences.yaml` is missing or thin, the skill will guide you through a one-time bootstrap interview to capture:
- Target role types
- Geographies
- Sectors
- Company stage preference
- Comp floor (stored locally, never echoed in artifacts)
- Hard red lines
- Narrative themes
- Writing samples → style guide

## Usage

Open your agent harness (opencode, Claude Code, Codex, Pi) in `/Users/niiamon/work/cv`. Then say things like:

- "apply for Acme VP Engineering"
- "new application for Globex"
- "show tracker"
- "what should I follow up on"
- "update Acme: moved to onsite"
- "tighten the Acme cover letter"

The skill handles the rest.

## File layout

See `SKILL.md` and `DESIGN.md` (in the repo) for full details.

## Hard rules (never violated)

- Never invent skills, titles, dates, companies, degrees, languages
- Never invent metrics — only reuse from CV, or mark `[estimated — verify]`
- ATS keyword weaving uses truth only
- Voice stays the user's
- Comp floor never echoed in artifacts

## What's not in v1

- Video summaries (planned for v2 via Remotion)
- URL fetch + parse for JDs (paste only)
- DOCX output (add per-app flag if portal demands)
- Portal autofill
- Email/calendar integration

See `DESIGN.md` in the repo for full design decisions and v2 scope.

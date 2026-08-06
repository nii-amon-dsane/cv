---
name: job-application-agent
description: Customizes job applications for Nii Amon Dsane per role. Generates tailored CV, cover letter, recruiter email, LinkedIn message, interview prep doc, and tracks all applications. Trigger when user mentions "apply for", "new application", "track application", "show tracker", "update status", or references working on a job application.
---

# Job Application Agent

This skill customizes job applications for **Nii Amon Dsane** — a technology executive and software engineering leader based in Nairobi, Kenya. It generates tailored artifacts per role and tracks the application pipeline.

## Paths

All paths absolute. The skill lives in the repo (loaded via a thin pointer at `~/.agents/skills/job-application-agent/SKILL.md`).

- **Repo root** (skill + state): `/Users/niiamon/work/cv`
- **Profile**: `/Users/niiamon/work/cv/profile/`
- **Applications**: `/Users/niiamon/work/cv/applications/`
- **Tracker**: `/Users/niiamon/work/cv/tracker.md` (derived)
- **Templates**: `/Users/niiamon/work/cv/templates/`
- **Scripts**: `/Users/niiamon/work/cv/scripts/`

## Trigger phrases

Invoke this skill when the user says any of:
- "apply for <company> <role>" / "new application for <company>"
- "show tracker" / "what's active" / "what should I follow up on"
- "update <company>: <status>" / "moved to onsite at <company>" / "withdrew from <company>"
- "edit <company> cover letter" / "revise <company> email" / "tighten the <company> CV"
- "bootstrap my profile" / "set up my preferences"

If the user mentions a company they've applied to or are considering, check `/Users/niiamon/work/cv/applications/` first.

## Hard rules — NEVER violate

These are non-negotiable. Violating them destroys trust.

1. **Never invent skills, job titles, dates, companies, degrees, or languages.** Use only what is in `profile/cv.md` or `profile/achievements.md`.
2. **Never invent metrics.** Reuse numbers from the CV/achievements library only. If a metric seems plausible but isn't sourced, mark it `[estimated — verify]` so the user can confirm or remove.
3. **ATS keyword weaving is per-application** (`meta.json: ats_optimize`). When enabled, weave JD keywords into bullets using only **truth** — never claim a skill the user doesn't have.
4. **Voice**: keep the user's voice. Do not mimic the target company's voice. See `profile/style_guide.md`.
5. **Comp floor**: never mention, echo, or imply the comp floor from `profile/preferences.yaml` in any generated artifact.

## Workflow per application

Follow these steps in order. Do not skip steps. Pause for user input where indicated.

### Step 1 — Locate and adopt the application folder

**Folder-driven workflow.** The user creates the application folder and drops files in. You detect, read, and adopt it.

**Folder convention** (suggested): `<company>__<role-slug>__<YYYY-MM-DD>` under `/Users/niiamon/work/cv/applications/`. Accept any name — strict convention is not enforced.

**Detection rules:**
1. If the user names a folder explicitly (e.g., "work on acme"), use that folder.
2. Otherwise, pick the most recently modified folder under `applications/`.
3. If `applications/` is empty, tell the user to create a folder first.

**Read everything in the folder:**
- `jd.*` (txt/md/pdf/docx/html) — the job description. For PDF/DOCX, extract text via `pdftotext` or similar. If multiple JD-like files exist, prefer `jd.txt` → `jd.md` → others.
- `notes.md` or `notes.txt` — user's structured notes (see format below). Optional.
- Any other files (screenshots, email forwards as `.eml`, company research, etc.) — note them; for v1 don't OCR images, ask the user in chat if image-only context matters.

**Notes file format** (when present):
```markdown
# Notes: <company> <role>

source: portal | recruiter_cold | warm_intro | referral | direct_outreach
recruiter_name: (optional)
recruiter_linkedin: (optional)
ats_optimize: true | false   # default: true for portal, false otherwise

## Context
(free-text — anything you know about the company, the role, the hiring process, the team, etc.)
```

**Infer and fill gaps:**
- Parse folder name for default company + role if notes file is missing.
- Read all files for any other hints about source / recruiter.
- If anything required is still missing (source is the most common gap), **ask the user in chat** before proceeding.

**Create `meta.json`** in the folder if it doesn't exist, using inferred + parsed fields. Schema matches the original spec (see DESIGN.md).

**Normalize JD to text:** write `jd.txt` from whatever source format you read (so downstream steps always have a canonical text JD). Keep the original file alongside (e.g., `jd.pdf` stays, you also write `jd.txt`).

### Step 2 — Company research

Research the company online before running match analysis. The research feeds Step 3 (match analysis reads `company_research.md`) and Step 5 (cover letter + interview prep draw on it).

**Depth dial** (user can override; default is `standard`):
- `quick` (~30s, 1-2 fetches): company website + 1 news lookup. Snapshot only.
- `standard` (~1-2 min, 4-6 fetches): website + careers + about + recent news + funding + key people. Full picture.
- `deep` (~3-5 min, 8+ fetches): all of standard + engineering blog + GitHub + Glassdoor + competitor analysis.

**Skip rules:**
- If `company_research.md` already exists in the folder and is < 30 days old, skip research and reuse it. (User can force-refresh with "research <company> again".)
- If the company has no meaningful web presence (rare for venture-backed roles), note that and proceed with JD-only signal.

**Fetch strategy** — use `ctx_fetch_and_index` for content-heavy pages, `webfetch` for one-off lookups:
1. Company website homepage + `/about` + `/careers` + `/blog` (if exists)
2. Latest funding info: try `crunchbase.com/organization/<slug>` (public page) or recent TechCrunch / Sifted / Techpoint Africa articles
3. Recent news (last 12 months): Google News RSS at `https://news.google.com/rss/search?q=<company>+<sector>&hl=en`
4. LinkedIn company page (public view): `linkedin.com/company/<slug>`
5. Engineering signals: search for `<company> engineering blog`, check GitHub orgs
6. Culture signals: Glassdoor overview (`glassdoor.com/Overview/Working-at-<company>-...)`)

For African tech companies, also try: TechCabal, Techpoint Africa, WeeTracker, MagAsh, Norrsken22 portfolio pages, Africa-focused VC portfolios.

If the user provided a company URL in `notes.md`, start there. Otherwise ask once: "what's the company website?" before researching.

**Write `company_research.md`** in the application folder using `/Users/niiamon/work/cv/templates/company_research.md.tmpl`. Include all 9 sections (snapshot, stage & funding, recent news, tech stack signals, market position, people, culture signals, why-this-role-open inferred, sources). Cite URLs in each section so the user can verify.

**Hard rules for research:**
- Mark anything uncertain as `[unverified]` rather than stating it as fact
- Never invent funding amounts, valuations, or employee counts — if not found, say "not publicly disclosed"
- Distinguish "company states X" from "third-party reports X"
- Recent news section: prefer primary sources (company blog, official announcements) over secondary commentary

### Step 3 — Read profile and run match analysis

Read in this order:
1. `/Users/niiamon/work/cv/profile/cv.md` — full career history
2. `/Users/niiamon/work/cv/profile/preferences.yaml` — must-haves, red lines, target criteria
3. `/Users/niiamon/work/cv/profile/achievements.md` — quantified wins (may be thin early on)
4. `/Users/niiamon/work/cv/profile/narrative_themes.md` — story arcs to lean on
5. `/Users/niiamon/work/cv/profile/style_guide.md` — voice rules
6. The application folder's `jd.txt` — the job description
7. The application folder's `company_research.md` — output of Step 2 (company research). **Skip if missing — research is required before match analysis.**

Then write `match_analysis.md` in the application folder using the template at `/Users/niiamon/work/cv/templates/match_analysis.md.tmpl`. The report has 5 sections:

1. **Fit score** (0-100) with breakdown:
   - must_haves_met, must_haves_missed (counts)
   - nice_to_haves_met (count)
   - seniority_match: `below` / `lateral` / `exact` / `above`
   - domain_match: `weak` / `moderate` / `strong` / `exact`
   - stage_match: `weak` / `moderate` / `strong` / `exact`
2. **Gap list** — for each gap (a JD requirement the user can't fully satisfy), provide a framing strategy: `de_emphasize` / `lean_on_adjacent` / `address_in_cover_letter` / `reframe_strength_as_proxy`. One sentence per gap.
3. **Recommended angle** — 2-3 strengths to lead with, the narrative theme that best fits, which past roles to feature prominently vs. compress.
4. **Risk flags** — e.g., short stints, missing big-co name, geographically distant. Mitigation per flag.
5. **Application strategy** — based on `source`: which artifacts to prioritize, suggested tone, length caps to apply.

### Step 4 — Confirm the angle with the user

Present a concise summary of the match analysis (fit score, top 2 gaps + framings, recommended angle, application strategy). Ask the user:
- Confirm the recommended angle, OR
- Override (e.g., "lead with the MTN cross-border work instead", "de-emphasize Peach")

Update `meta.json`:
- `fit_score`, `fit_breakdown`, `gaps`, `angle_confirmed: true` once confirmed

### Step 5 — Generate all artifacts in batch

Write these files using the templates in `templates/`:

- `cv.md` — tailored CV (moderate rewrite per the customization rules below). Length cap: 2 pages.
- `cover_letter.md` — cover letter. Length cap: 1 page.
- `recruiter_email.txt` — plain text email with subject line. Length cap depends on source.
- `linkedin_message.txt` — plain text LinkedIn message. Length cap depends on type.
- `interview_prep.md` — prep doc: likely questions, suggested answers drawn from CV, questions to ask them.

Then render PDFs:
```bash
bash /Users/niiamon/work/cv/scripts/render_pdfs.sh <application_dir>
```
This produces `cv.pdf` and `cover_letter.pdf` from the `.md` sources via pandoc + typst.

### Step 6 — Review loop

The user describes revisions in natural language. For each revision:
1. Edit the relevant `.md` or `.txt` file in place
2. Re-render affected PDFs (`render_pdfs.sh <application_dir>`)
3. Show the user a diff (use `git diff` if the repo is git-tracked, or just describe what changed)
4. Wait for next instruction

Common revision patterns:
- "tighten the cover letter" → reduce wordiness, hit length cap
- "lead harder with <experience>" → restructure to feature that first
- "more confident tone" → adjust voice per style guide
- "regenerate the email from scratch" → full regen, discard previous

When the user says "done" / "submitted" / "sent", move to Step 6.

### Step 7 — Log to tracker

Update `meta.json`:
- `status`: `submitted` (or `preparing` if not yet sent)
- `key_dates.submitted`: today's date (if submitted)
- `key_dates.next_follow_up`: today + 7 days (suggested)

Then regenerate the tracker:
```bash
python3 /Users/niiamon/work/cv/scripts/regenerate_tracker.py
```
Confirm to the user what was logged.

## Status updates (any time)

When the user says "update <company>: <status>" or "moved to onsite at <company>":
```bash
python3 /Users/niiamon/work/cv/scripts/update_status.py <application_dir_or_company> <new_status> [--note "..."]
```
Status values: `preparing` / `submitted` / `recruiter_screen` / `hiring_manager` / `onsite` / `offer` / `rejected` / `withdrawn`.

Tracker is auto-regenerated.

## Tracker queries

When the user asks "what's active" / "show tracker" / "what should I follow up on":
- Read `/Users/niiamon/work/cv/tracker.md` and present a concise summary
- For "what should I follow up on" specifically, filter by `key_dates.next_follow_up <= today` and `status in [submitted, recruiter_screen, hiring_manager]`

## Customization rules — moderate aggressiveness

The base CV in `profile/cv.md` is the source of truth. When tailoring per application, you may:

- **Reorder** bullets and sections to match the JD's priorities
- **Rewrite** bullets for impact (tighter phrasing, stronger verbs, clearer outcomes)
- **Swap synonyms** for JD keywords (e.g., "engineering team" → "engineering org" if JD uses "org")
- **Drop** bullets that are irrelevant to this JD
- **Compress** less-relevant roles into fewer lines
- **Restructure** the capabilities/summary sections to mirror the JD's must-haves

You may NOT:
- Add new skills, roles, or achievements not in the source
- Invent metrics
- Change dates or company names
- Claim experience in domains the user hasn't worked in

## Length caps (defaults unless JD specifies otherwise)

| Artifact | Cap |
|----------|-----|
| CV | 2 pages |
| Cover letter | 1 page |
| Recruiter cold email | 150 words |
| Warm intro follow-up | 75 words |
| Referral thank-you | 100 words |
| LinkedIn connection note | 300 chars |
| LinkedIn InMail | 500 words |
| LinkedIn DM | 200 words |

## Source-specific strategy

| Source | CV emphasis | Cover letter | Email/message priority |
|--------|-------------|--------------|------------------------|
| `portal` | ATS-optimized, full keyword weave, complete history | Full formal cover letter | None |
| `recruiter_cold` | Crisp 1-page version, lead with headline fit | Optional 3-paragraph version | Short punchy outreach email is primary |
| `warm_intro` | Standard tailored CV | Brief, references the intro | Short thank-you + why-excited email |
| `referral` | Standard tailored CV | Brief, mentions referrer | Short thank-you to referrer + brief outreach to HM |
| `direct_outreach` | Tight tailored CV | Optional | Personalized email emphasizing 1-2 fit points + LinkedIn message |

## LinkedIn message type

Ask the user which type if unclear:
- **connection note** (300 chars) — when connecting cold to a recruiter/HM
- **InMail** (500 words) — when sending a longer pitch via LinkedIn
- **DM** (200 words) — when following up with someone already connected

Default: generate **connection note + DM** pair.

## Bootstrap (first run)

If `profile/preferences.yaml` is missing or thin, run the bootstrap interview (see `BOOTSTRAP.md` in the skill directory). One focused session covering:
- Target role types
- Geographies
- Sectors (consider vs. refuse)
- Company stage preference
- Comp floor (user enters privately)
- Hard red lines
- Narrative themes
- Writing samples → style guide derivation

Skip any section where the CV already answers it.

## Reference files

- `profile/cv.md` — master CV
- `profile/preferences.yaml` — must-haves, red lines, target criteria
- `profile/achievements.md` — quantified achievements library (enrich over time)
- `profile/narrative_themes.md` — 2-3 story arcs
- `profile/style_guide.md` — voice rules
- `profile/voice_samples/*.md` — writing samples

## When the skill ends

Always:
- Confirm `meta.json` is up to date
- Confirm `tracker.md` has been regenerated if any status changed
- Summarize what was generated/revised in 1-3 lines

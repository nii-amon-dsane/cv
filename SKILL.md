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

These are non-negotiable.

1. **Never invent skills, job titles, dates, companies, degrees, languages, responsibilities or outcomes.** Use only what is in `profile/cv.md`, `profile/achievements.md` or material the user has explicitly supplied.
2. **Never invent metrics.** Reuse numbers from the CV/achievements library only. If a metric is not sourced, do not use it as fact.
3. **ATS keyword use is per-application** (`meta.json: ats_optimize`). When enabled, use JD terminology only when it truthfully and naturally describes the user's work.
4. **Voice**: keep the user's voice. Do not mimic the target company's voice. See `profile/style_guide.md` and `profile/voice_samples/`.
5. **Comp floor**: never mention, echo, or imply the comp floor from `profile/preferences.yaml` in any generated artifact.
6. **Do not invent AI experience.** Current sourced AI/LLM work is at Sellogram. There was no AI/LLM work at Peach Tech or Bridge Technologies.
7. **Peach factual constraint**: the unified system of record was not delivered. Use the research, product-design and delivered-tool evidence in the source profile instead.
8. **Do not invent a personal brand.** Never turn career history into slogans or archetypes such as `AI-native product builder`, `0→1 builder`, `org scaler` or `strategic partner to CEO`.
9. **Do not inflate the evidence.** Design is not delivery. Partial delivery is not completion. Responsibility is not automatically an outcome.

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
- `notes.md` or `notes.txt` — user's structured notes. Optional.
- Any other files — note them and use them only when they provide relevant application context.

**Notes file format** (when present):
```markdown
# Notes: <company> <role>

source: portal | recruiter_cold | warm_intro | referral | direct_outreach
recruiter_name: (optional)
recruiter_linkedin: (optional)
ats_optimize: true | false

## Context
(free-text)
```

**Infer and fill gaps:**
- Parse folder name for default company + role if notes file is missing.
- Read all files for any other hints about source / recruiter.
- If anything required is still missing and cannot be inferred safely, ask the user before proceeding.

**Create `meta.json`** in the folder if it doesn't exist, using inferred + parsed fields. Schema matches `DESIGN.md`.

**Normalize JD to text:** write `jd.txt` from whatever source format you read. Keep the original file alongside it.

### Step 2 — Company research

Research the company online before running match analysis. The research feeds Step 3 and Step 5.

**Depth dial** (user can override; default is `standard`):
- `quick`: company website + one recent-news check
- `standard`: website + careers + about + recent news + funding + key people
- `deep`: standard + engineering signals + competitors + additional culture/company evidence

**Skip rules:**
- If `company_research.md` already exists and is < 30 days old, reuse it unless the user asks for a refresh.
- If the company has little public information, note that and proceed with the available evidence.

**Research rules:**
- Mark uncertain claims as `[unverified]`.
- Never invent funding amounts, valuations or employee counts.
- Distinguish company claims from third-party reports.
- Prefer primary sources for recent company facts.

Write `company_research.md` using `/Users/niiamon/work/cv/templates/company_research.md.tmpl`.

### Step 3 — Read profile and run match analysis

Read in this order:
1. `/Users/niiamon/work/cv/profile/cv.md`
2. `/Users/niiamon/work/cv/profile/preferences.yaml`
3. `/Users/niiamon/work/cv/profile/achievements.md`
4. `/Users/niiamon/work/cv/profile/narrative_themes.md`
5. `/Users/niiamon/work/cv/profile/style_guide.md`
6. Relevant files in `/Users/niiamon/work/cv/profile/voice_samples/` when producing user-facing writing
7. The application folder's `jd.txt`
8. The application folder's `company_research.md`

Then write `match_analysis.md` using the template.

The report has five sections:

1. **Fit score** with must-haves, nice-to-haves, seniority, domain and stage.
2. **Gap list** with a factual handling strategy for each meaningful gap.
3. **Recommended angle** — the relevant career angle, evidence to lead with and roles to feature or compress.
4. **Risk flags** — only concrete issues that could matter to the application.
5. **Application strategy** — which artifacts matter for the source and how much tailoring is useful.

Do not create a personal-brand label as part of the recommended angle.

### Step 4 — Confirm the angle with the user

Present a concise summary of the match analysis and ask the user to confirm or override the evidence and emphasis.

Update `meta.json` with the confirmed angle and fit data.

### Step 5 — Generate artifacts

Write these files using the templates in `templates/`:

- `cv.md` — tailored CV, maximum 2 pages
- `cover_letter.md` — cover letter, maximum 1 page
- `recruiter_email.txt` — plain text email when useful for the source
- `linkedin_message.txt` — LinkedIn message when useful for the source
- `interview_prep.md` — likely questions, evidence from the CV and questions to ask

Then render PDFs:
```bash
bash /Users/niiamon/work/cv/scripts/render_pdfs.sh <application_dir>
```

### Step 6 — Review loop

For each revision:
1. Edit the relevant source file.
2. Re-render affected PDFs.
3. Show the user the meaningful diff.
4. Continue until the user says the application is done or submitted.

When revising language, use `profile/style_guide.md` and the actual writing samples rather than generic career-writing formulas.

### Step 7 — Log to tracker

Update `meta.json` with status and relevant dates, then regenerate the tracker:
```bash
python3 /Users/niiamon/work/cv/scripts/regenerate_tracker.py
```

## Status updates

Use:
```bash
python3 /Users/niiamon/work/cv/scripts/update_status.py <application_dir_or_company> <new_status> [--note "..."]
```

Status values: `preparing` / `submitted` / `recruiter_screen` / `hiring_manager` / `onsite` / `offer` / `rejected` / `withdrawn`.

## Tracker queries

When the user asks "what's active" / "show tracker" / "what should I follow up on":
- Read `/Users/niiamon/work/cv/tracker.md` and present a concise summary.
- For follow-ups, use the tracked next-follow-up date and current status.

## Customization rules — moderate

The base CV in `profile/cv.md` is the source of truth. When tailoring per application, you may:

- reorder bullets and sections when it improves relevance
- rewrite for clarity, concision and relevance
- use JD terminology when it is accurate and natural
- drop irrelevant bullets
- compress less-relevant roles
- reorder supported capabilities

You may NOT:
- add new skills, roles or achievements
- invent metrics
- change dates or company names
- claim experience in domains the user has not worked in
- create AI/LLM experience outside Sellogram from the current source profile
- claim Peach delivered the unified system of record
- create a branded identity or slogan for Nii
- turn a gap into a claimed strength by wording alone

## Length caps

| Artifact | Cap |
|----------|-----|
| CV | 2 pages |
| Cover letter | 1 page |
| Recruiter cold email | 150 words |
| Warm intro follow-up | 100 words |
| Referral thank-you | 120 words |
| LinkedIn connection note | 300 chars |
| LinkedIn InMail | 500 words |
| LinkedIn DM | 200 words |

## Source-specific strategy

| Source | CV emphasis | Cover letter | Email/message priority |
|--------|-------------|--------------|------------------------|
| `portal` | ATS-aware, accurate, complete enough for the role | Full letter when required/useful | Usually none |
| `recruiter_cold` | Crisp version focused on relevant evidence | Optional | Brief, direct outreach is primary |
| `warm_intro` | Standard tailored CV | Brief when useful | Short follow-up referencing the introduction |
| `referral` | Standard tailored CV | Brief when useful | Short note referencing the referrer |
| `direct_outreach` | Tight tailored CV | Optional | Personalized email or LinkedIn message using specific evidence |

## LinkedIn message type

Default to the channel and message type that fits the actual context. Do not generate both a connection note and DM automatically when only one is useful.

## Bootstrap

If `profile/preferences.yaml` is missing or thin, run a focused bootstrap covering:
- target roles
- geographies
- sectors
- company stage
- compensation constraints
- red lines
- career angles
- writing samples

Skip any section where the profile already answers it.

## Reference files

- `profile/cv.md` — master CV and factual source of truth
- `profile/preferences.yaml` — must-haves, red lines and target criteria
- `profile/achievements.md` — sourced achievement library
- `profile/narrative_themes.md` — factual career angles
- `profile/style_guide.md` — voice rules
- `profile/voice_samples/*.md` — primary evidence for Nii's writing voice

## When the skill ends

Always:
- confirm `meta.json` is current when an application was changed
- regenerate `tracker.md` when status changed
- summarize what was generated or revised in 1-3 lines

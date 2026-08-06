# Job Application Agent — Design

## Verbatim user prompt

> Please check out my CV in the PDF file. I want us to build a job application agent that customizes job applications for any job that I want to apply for. please take me through a grill-me so that you can create a great agent for me

## Locked decisions (13)

| # | Axis | Decision |
|---|------|----------|
| 1 | Output scope (v1) | Full suite minus video: tailored CV, cover letter, recruiter email, LinkedIn message, interview prep, tracker |
| 2 | Workflow | Interactive multi-step: feed JD → match analysis → confirm angle → generate all artifacts → review per artifact → log to tracker |
| 3 | Tool form | Agent harness skill (opencode/Claude Code/Codex/Pi — any harness that loads `~/.agents/skills/`) |
| 4 | Master profile | Hybrid: CV (from PDF) + thin preferences addendum. Achievements library fills over time |
| 5 | Input shape | JD text + small structured form (company, role title, source, optional recruiter + context) |
| 6 | Customization aggressiveness | Moderate: rewrite bullets for impact, swap synonyms for JD keywords, drop irrelevant, restructure. Hard red lines below |
| 7 | Tracker | Per-app directory is source of truth; top-level `tracker.md` is derived |
| 8 | Match analysis | Structured 5-part report: fit score w/ breakdown + gap list w/ framing + recommended angle + risk flags + application strategy |
| 9 | Artifact formats | MD source + auto-rendered PDF for CV/cover letter; plain text for emails/messages; MD only for interview prep. Pandoc rendering, MD fallback |
| 10 | Voice capture | Style guide + 3-5 writing samples |
| 11 | Bootstrap | Hybrid: start from extracted CV, agent interviews for gaps (preferences, themes, voice) in one focused session |
| 12 | Review loop | Free-form chat → agent edits markdown in place → re-renders PDFs → shows diff |
| 13 | Video | Deferred to v2 |

## Hard red lines (non-negotiable)

- Never invent skills, titles, dates, companies, degrees, languages
- Never invent metrics — only reuse ones in the CV/master profile, or mark `[estimated]` for review
- ATS keyword weaving enabled per-app, but only with truth
- Voice: keep yours, don't mimic the company's

## Application sources (drives strategy)

- `portal` — heavy ATS-optimized CV, full cover letter
- `recruiter_cold` — short punchy outreach email + crisp CV
- `warm_intro` — brief follow-up email + CV
- `referral` — short thank-you note + CV
- `direct_outreach` — personalized email emphasizing fit + CV + optional LinkedIn message

## Workflow (concrete)

```
1. User invokes skill: "applying for <company> <role>" or similar trigger
2. Agent prompts for the structured form (JD, company, role, source, recruiter, context)
3. Agent reads profile/ + JD, runs match analysis → writes applications/<dir>/match_analysis.md
4. Agent presents match analysis summary, asks user to confirm or override the recommended angle
5. User confirms or redirects
6. Agent generates all artifacts in batch:
   - cv.md → cv.pdf
   - cover_letter.md → cover_letter.pdf
   - recruiter_email.txt
   - linkedin_message.txt
   - interview_prep.md
7. Agent presents summary of what was generated
8. Review loop: user describes changes → agent edits + re-renders + shows diff → repeat
9. On "done" or "submitted": agent updates meta.json status, regenerates tracker.md
```

## Directory layout

### Skill (cross-harness, installed once)

```
~/.agents/skills/job-application-agent/
├── SKILL.md                      # Harness-loaded instructions
├── README.md                     # Human-facing usage doc
├── profile/                      # Symlink or copy from the repo (see below)
├── templates/
│   ├── pandoc/
│   │   ├── cv_template.md
│   │   └── cover_letter_template.md
│   ├── match_analysis.md.tmpl
│   ├── cv.md.tmpl
│   ├── cover_letter.md.tmpl
│   ├── recruiter_email.txt.tmpl
│   ├── linkedin_message.txt.tmpl
│   └── interview_prep.md.tmpl
└── scripts/
    ├── new_application.py        # Scaffold application directory
    ├── render_pdfs.sh            # Pandoc MD → PDF
    ├── regenerate_tracker.py     # Scan apps/, write tracker.md
    └── update_status.py          # Update meta.json + regenerate tracker
```

### Repo (versioned, lives at /Users/niiamon/work/cv)

```
/Users/niiamon/work/cv/
├── Nii-Amon-Dsane-CV-2025-SEP-public.pdf   # Original
├── profile/
│   ├── cv.md                     # Full CV extracted from PDF (master source)
│   ├── preferences.yaml          # Target roles, geo, sectors, stage, comp floor, red lines
│   ├── achievements.md           # Quantified achievements library (enriches over time)
│   ├── narrative_themes.md       # 2-3 story arcs
│   ├── style_guide.md            # Voice rules
│   └── voice_samples/            # Writing samples (paste-in)
├── applications/                 # Per-app dirs created on use
│   └── <company>__<role-slug>__<YYYY-MM-DD>/
│       ├── meta.json             # Source of truth for this app
│       ├── jd.txt                # Original JD as pasted
│       ├── match_analysis.md     # 5-part report
│       ├── cv.md
│       ├── cv.pdf
│       ├── cover_letter.md
│       ├── cover_letter.pdf
│       ├── recruiter_email.txt
│       ├── linkedin_message.txt
│       └── interview_prep.md
└── tracker.md                    # Derived view, auto-regenerated
```

## meta.json schema

```json
{
  "company": "Acme",
  "role": "VP Engineering",
  "date_created": "2025-09-21",
  "source": "recruiter_cold",
  "recruiter": {
    "name": "...",
    "linkedin": "..."
  },
  "status": "preparing",
  "fit_score": 82,
  "fit_breakdown": {
    "must_haves_met": 7,
    "must_haves_missed": 1,
    "nice_to_haves_met": 4,
    "seniority_match": "exact",
    "domain_match": "strong",
    "stage_match": "strong"
  },
  "gaps": ["..."],
  "angle_confirmed": true,
  "key_dates": {
    "submitted": null,
    "last_contact": null,
    "next_follow_up": null
  },
  "notes": ""
}
```

## Status values

`preparing` → `submitted` → `recruiter_screen` → `hiring_manager` → `onsite` → `offer`
side: `rejected`, `withdrawn`

## Bootstrap procedure (first run)

1. Extract CV from PDF to `profile/cv.md` (already done in design)
2. Agent interviews user for:
   - Target role types
   - Geographies (Nairobi-only / remote / specific cities)
   - Sectors (consider vs. refuse)
   - Company stage preference
   - Comp floor (user enters privately; agent never echoes it back in artifacts)
   - Hard red lines
   - 2-3 narrative themes
3. User pastes 3-5 writing samples → agent writes `profile/style_guide.md`
4. Agent writes `profile/preferences.yaml`, `profile/narrative_themes.md`
5. `profile/achievements.md` starts empty; first application asks user to add 2-3 quantified wins

## Trigger phrases

- "apply for <company> <role>" / "new application for <company>"
- "show tracker" / "what's active"
- "update <company>: <status>" / "moved to onsite at <company>"
- "follow-up due" / "what should I follow up on"
- "edit <company> cover letter" / "revise <company> email"

## ATS keyword optimization

Per-application flag in meta.json: `ats_optimize: true|false`. Default true for `portal` source, false for others. When true, agent weaves JD keywords into CV bullets (using only truth).

## Length caps (defaults)

- CV: 2 pages
- Cover letter: 1 page
- Recruiter cold email: 150 words
- Warm intro follow-up: 75 words
- LinkedIn connection note: 300 chars
- LinkedIn InMail: 500 words
- LinkedIn DM: 200 words

## What's explicitly NOT in v1

- Video summaries (Remotion) — v2
- URL fetch + parse for JDs — paste only
- DOCX output — add per-app flag later if a portal demands
- Application autofill on portal websites
- Email integration (sending on your behalf)
- Calendar integration for interview scheduling
- Reference management

## Open implementation questions (resolve during build)

- Pandoc LaTeX engine choice (xelatex vs. pdflatex) for PDF rendering
- Whether to use a single global pandoc template or per-artifact templates
- How agent reads profile/cv.md efficiently without re-reading on every prompt
- Whether `fit_breakdown` weights are fixed or user-tunable
- LinkedIn message: default to connection-note + DM, or generate all 3 variants

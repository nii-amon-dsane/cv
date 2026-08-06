# How to Share This Skill with a ChatGPT User

## What you're sharing

One file: `chatgpt-mega-prompt.md` in this directory. Self-contained. No dependencies. No personal data of yours in it.

## How to share

Pick one:

### Option A — Send the file
Send `chatgpt-mega-prompt.md` to the recipient via whatever channel (email, Slack, WhatsApp, AirDrop). They open it, copy from `--- BEGIN PROMPT ---` to `--- END PROMPT ---`, paste into a new ChatGPT chat.

### Option B — Paste into a shared doc
Copy the prompt contents into a Google Doc / Notion page / GitHub Gist. Recipient copies from there.

### Option C — Host publicly (gist / repo)
```bash
# As a GitHub Gist (quickest public share)
gh gist create chatgpt-mega-prompt.md --public --desc "Job application agent mega-prompt for ChatGPT"
```
Share the gist URL with anyone.

## What the recipient does

1. Copy the prompt (from `--- BEGIN PROMPT ---` to `--- END PROMPT ---`).
2. Open a **new ChatGPT chat** (any tier works — Free, Plus, Team).
3. Paste as the first message. Send.
4. ChatGPT becomes their Job Application Agent. It walks them through setup (CV, preferences, writing style).
5. They use the same chat for all applications in their current "season".
6. Per application, they paste a JD + form fields → agent produces match analysis → they confirm angle → agent generates all artifacts → revision loop in chat.

## What ChatGPT cannot do for them

- Save files to disk — they copy/paste from chat to their own files
- Render PDFs — they paste markdown into a PDF generator (marktext, typst, pandoc, even browser print-to-PDF)
- Persistent tracker across chats — they maintain their own tracker externally, or keep one long chat per application season

## What you keep private

The mega-prompt does NOT include:
- Your CV
- Your preferences
- Your compensation floor
- Your narrative themes
- Your writing samples

The recipient supplies their own everything during ChatGPT's Phase 0 setup. Your personal data stays in your repo.

## Customization before sharing (optional)

If you want to make the prompt even more generic, search/replace before sharing:
- No personal references to remove — already generic

If you want to make it more opinionated for a specific recipient (e.g., a friend in a specific industry), edit:
- The example preferences in Phase 0 (currently shows varied examples)
- The narrative themes list (currently shows 6 archetypes)

## Versioning

This mega-prompt is a snapshot of `SKILL.md` in this skill. If you improve the skill, you'll want to re-distill the mega-prompt. The two files do not auto-sync.

To regenerate after major skill changes:
1. Open `SKILL.md` and the templates
2. Distill the workflow, rules, voice, and templates into a single linear prompt
3. Replace this `chatgpt-mega-prompt.md` file
4. Re-share

# Style Guide — Nii's Voice

This guide shapes how the agent writes on your behalf. The agent reads this before generating any artifact.

This is the v1 style guide derived from your CV's voice + sensible senior-exec defaults. It will be refined as you provide writing samples and as you flag things that "don't sound like you" in generated artifacts.

## Voice principles

1. **Short sentences.** Average 12-18 words. Break long ones.
2. **Outcome first.** Lead with what happened, not what you did.
   - ✅ "Delivered cross-border remittance product serving 70M MTN subscribers."
   - ❌ "Was responsible for the delivery of a cross-border remittance product that served 70M MTN subscribers."
3. **Active voice.** No passive constructions.
   - ✅ "Led team of 12."
   - ❌ "Team of 12 was led by me."
4. **Concrete over abstract.** Numbers, names, scales.
   - ✅ "Reached 80% completion in 3 months."
   - ❌ "Made significant progress in a short timeframe."
5. **Industry precision.** Use the right technical terms — they signal competence.
   - ✅ "Microservices orchestrated via AMQP message queues."
   - ❌ "Service-based architecture using messaging."
6. **No filler.** Cut adjectives and adverbs that don't carry weight.
   - ✅ "Built payment system."
   - ❌ "Successfully built a robust, scalable payment system."
7. **First person in cover letters/emails, implied in CV.**
   - CV: "Led team of 12" (no "I")
   - Cover letter: "I led a team of 12" (with "I")
8. **Present tense for current role, past tense for prior.**
   - Mira (current): "I'm building an AI agent for social commerce sellers."
   - Peach (prior): "I directed the Technology Group at Peach."

## Banned words and phrases

The agent must not use these. They smell AI-generated or generic.

| Banned | Reason |
|--------|--------|
| "passionate" | cliché, AI-smelling |
| "results-driven" | cliché, empty |
| "proven track record" | show, don't claim |
| "synergy" / "synergies" | empty corporate-speak |
| "leverage" (verb) | overused |
| "thrive" / "thriving" | cliché |
| "I am writing to apply for" | overused cover letter opener |
| "I hope this email finds you well" | spam-smelling |
| "please find attached my resume" | obvious, replace with substance |
| "delve into" | AI-smelling |
| "in today's fast-paced world" | filler |
| "unlock" (figurative) | overused |
| "seamlessly" | overused |
| "robust" | empty |
| "scalable" (without proof) | claim without evidence — instead, show the scale |
| "world-class" | unsubstantiated |
| "cutting-edge" | cliché |
| "best-in-class" | cliché |

## Sentence structure patterns (use these)

**Bullet pattern (CV)**: `[Strong verb] [specific thing] [metric or scope] [optional context].`
- "Delivered cross-border remittance product for MTN Group, reaching 70M subscribers in Nigeria."
- "Led team of 12 across development and digital transformation at Radio Africa."
- "Architected music streaming service with microservices + Akka pipeline + serverless."

**Paragraph opener (cover letter)**: `[Specific hook about company/role]. [Why it connects to you]. [What you'll show in this letter].`
- "Acme's pivot to AI-native logistics caught my attention — I'm currently shipping an AI agent for social commerce sellers at Mira, and the patterns translate. Below: three outcomes from my last three roles that map to what you're hiring for."

**Email opener (cold outreach)**: `[One sentence on why them specifically]. [Three bullets mapping their must-haves to your outcomes]. [Low-friction CTA].`

**LinkedIn connection note**: `[Who you are in 6 words]. [Why connecting is mutually valuable in 1 sentence]. [Optional CTA].` Must fit 300 chars.

## Tone by context

| Context | Tone |
|---------|------|
| CV | Confident, factual, terse |
| Cover letter | Confident, warm but not effusive, specific |
| Cold email | Direct, respectful of time, no fluff |
| Warm intro follow-up | Brief, gracious to connector, low-friction |
| LinkedIn message | Brief, personalized, conversational |
| Interview prep | Internal thinking, can be candid |

## Capitalization, punctuation, formatting

- Sentence case for headings (not Title Case For Every Word)
- One space after periods
- Em-dashes (—) with no spaces around them, or en-dashes with spaces — pick one, be consistent. Use em-dashes without spaces (matches CV).
- Bullets in CV use `-` (hyphen)
- No Oxford comma unless needed for clarity
- Numbers under 10 spelled out in prose ("three months", "five developers"), numerals in CV bullets ("3 months", "5 developers")

## What "doesn't sound like you"

You'll catch this in the review loop. Common patterns to flag and request revision:
- "It sounds like ChatGPT" → too many em-dashes, too many "leverages", too many compound sentences
- "Too formal" → likely using "utilize" / "facilitate" / "endeavor"
- "Too casual" → likely using contractions in cover letter (cover letters should not use "don't" / "can't" / "won't")
- "Too generic" → no specific company name, no specific metric, no specific role from your past

## Refining this guide

This guide is a living document. As you flag generated artifacts that "don't sound like you", the agent should:
1. Identify the pattern that missed
2. Add a rule here that prevents it next time
3. Update this file

Over the first 10 applications, this guide becomes tightly calibrated to your voice.

---

## Samples needed

To calibrate further, the agent needs 3-5 writing samples from you. Best sources:
- Past cover letters
- LinkedIn posts (yours, not recirculated)
- Blog posts (yours)
- Emails you've sent (to colleagues, recruiters, founders)
- Even a thoughtful Slack message capturing how you write informally

Place samples in `profile/voice_samples/` as markdown files (`sample_01_cover_letter.md`, etc.).

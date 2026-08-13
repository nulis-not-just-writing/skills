# nulis — article structure

*[Baca dalam bahasa Indonesia](id/nulis.md)*

**v1.4.0** · [download zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/nulis-1.4.0.zip)

Writing coaching for Q1 journal articles, built on *genre analysis*. Not a bulk drafting
machine — it guides you **move by move**, demands evidence for each claim, and calibrates the
language to your field.

## What it is actually for

Three situations bring most people here.

### 1. The data exists; the article does not

You have results, tables, maybe a few figures — but no sense of what belongs in the Introduction
and what belongs in the Discussion.

> *"I have survey data from 340 vocational school teachers on self-efficacy. Help me turn it into
> an article."*

What happens: the skill asks for your **field** and **research type** first. That is not small
talk — the answer decides which conventions get loaded. It then maps gap → RQ → design → results →
contribution, **one line per RQ running through all five sections**. That line is what later gets
used to check whether every question was actually answered.

What does *not* happen: it will not write a complete Introduction out of thin air. Where the
substance is missing, you get `[SITASI]` and `[DATA]` placeholders to fill.

### 2. A reviewer said "the contribution is unclear"

That comment nearly always means the chain broke somewhere — usually a gap announced in the
Introduction that the Discussion never closes.

> *"A reviewer says my contribution is unclear. Audit this draft."*

Audit mode checks each RQ's traceability across all five sections, move completeness, claim
calibration, terminology drift, and generative-AI style markers. The output is a ranked findings
list with locations — not a manuscript quietly rewritten behind your back.

### 3. You write in a field that is not shaped like IMRaD

Pure mathematics has no Methods and Results in the IMRaD sense. Humanities is often essay-style.
Computer science frequently uses IDBRC.

This skill **does not force one shape**. It loads your field's conventions and follows the
structure there — including how boldly a claim may be stated, which differs sharply between
fields.

## When to use it

- You have data and results but no idea how to assemble an article
- You need an outline that carries through from gap to contribution
- You want to audit a draft: does each section carry the right moves
- A reviewer said "the contribution is unclear" or "the gap is weak"

## Four modes

| Mode | For |
|---|---|
| **Outline** | mapping gap → RQ → design → results → contribution, one line per RQ across five sections |
| **Draft section** | writing move by move, with `[SITASI]`/`[DATA]` markers for what you must supply |
| **Audit** | checking move completeness, RQ traceability, claim calibration, AI style markers |
| **Refine** | fixing a specific passage you point at |

## What sets it apart

**The Introduction is written twice.** The recommended order: Methods/Results first → Draft-0
Introduction → Discussion → **rewrite the Introduction**. The point is to make the claims exactly
as strong as the evidence you actually got, rather than the evidence you hoped for at the start.

**Field calibration.** Natural sciences use boosters most freely; mathematics and physical
sciences most sparingly; humanities hedge most. This skill does not flatten that.

**Pure mathematics is not forced into IMRaD.** Its structure follows theorem–proof convention.

## What is inside

- `sections/` — move guidance per section, Title through Conclusion
- `research-types/` — quantitative, qualitative, mixed methods, **thematic analysis** (Braun &
  Clarke's six phases)
- `fields/` — mathematics, engineering/CS, natural sciences, social sciences, humanities
- `reporting-guidelines/` — own-words summaries of what COREQ, SRQR, and CROSS are for
- `ai-stylometry-flags.md` — the canonical AI-marker list, shared with two other skills
- `coherence.md`, `phrasebank.md`

## One trap people fall into often

**There are two thematic analyses, and they have different names.** Braun & Clarke (2006) is for
**primary data** — interview transcripts, focus groups. To synthesise findings from already
published articles in a systematic review, the method is **thematic synthesis** (Thomas & Harden
2008).

Writing *"we used Braun & Clarke thematic analysis"* in an SLR misnames the method, and
methodological reviewers flag it.

---

[← Back](README.md) · [Installation](Installation.md) · [Workflow](Workflow.md) · [FAQ](FAQ.md)

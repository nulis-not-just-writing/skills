# submit — the pre-submission gate

*[Baca dalam bahasa Indonesia](id/submit.md)*

**v1.5.0** · [download zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/submit-1.5.0.zip)

Sweeps a manuscript for **desk rejection** risk — rejection by the editor before it ever reaches a
reviewer, in roughly a ten-minute read, affecting 40–70% of submissions at reputable journals.

Most of the criteria **have nothing to do with scientific quality**. Good manuscripts are returned
routinely because the scope missed or an ethics statement was left blank.

## What it is actually for

### 1. The manuscript is ready and you want to know what will kill it

> *"I want to send this to [journal name]. Here are its author guidelines. Check it."*

The skill runs **in order, from cheapest and most lethal first**. Journal scope before hyphens.
The moment a fatal finding appears, it **stops and reports** — because polishing sentences in a
manuscript aimed at the wrong journal is work that will be thrown away entirely.

What you must have ready: **the target journal's author guidelines URL**. Without it roughly half
the risk cannot be assessed, and the skill will say so rather than guess — word limits and required
statements differ between journals from the same publisher.

### 2. It came back without review and you do not know why

This is the situation that brings most people here, and the answer is often surprising: **most
desk-rejection criteria never touch scientific quality.** Good manuscripts are returned because an
ethics statement was blank, a word limit was exceeded, or anonymity leaked through file metadata.

### 3. You want to know whether the citations actually exist

Three statuses that other tools usually merge, and the difference matters:

| Status | Meaning | What to do |
|---|---|---|
| `VERIFIED` | matches the index | — |
| `MISMATCH` | DOI is right, authors or year are off | the work is real; the bibliography entry is wrong |
| `UNVERIFIED` | not found in any index | **a strong sign of a fabricated citation** |

And one check rarely found elsewhere: `check_claim_fidelity.py` asks **whether the source actually
says that** — verbatim quotations absent from the source, concept attributions where not one of
the words appears, cardinal claims ("reports three strategies") whose number is never stated.

If the source's full text is unavailable, **that script stays silent**. It never guesses.

## When to use it

- The manuscript is considered finished and about to be sent
- It was rejected without review and you do not know why
- You are choosing or changing target journals
- You are assembling a submission package: cover letter, highlights, ethics statements, anonymisation

## This is a gate, not a quality sweep

The difference from `polish-manuscript` and `nulis` is not just the checklist but the **shape**:

- Those two are *improvement passes* — linear, exhaustive, weighing all dimensions equally
- This one is a **gate** — sequential, cheapest and most lethal first. **One fatal finding makes
  the rest irrelevant: stop, report, do not carry on sweeping.**

No point polishing hyphens in a manuscript aimed at the wrong journal.

## What you must prepare

1. The manuscript (`.docx`/`.tex`/`.md`)
2. **Target journal + its author guidelines URL** — non-negotiable; without it roughly half the
   risk cannot be assessed
3. Review model: double-blind or single-blind? Was it ever a preprint?
4. Names and affiliations of all authors

The author guidelines are **actually read**, not inferred from publisher habit — word limits and
required statements differ between journals from the same publisher.

## Five scripts

| Script | Checks |
|---|---|
| `sweep.py` | consistency **within** the manuscript: word count, seven required statements, two-way citation cross-check, anonymity leaks, orphan figures, leftover TODOs/tracked changes |
| `verify_refs.py` | references **against the outside world** — CrossRef, OpenAlex, PubMed |
| `check_claim_fidelity.py` | **does the source actually say that?** |
| `prisma_cascade_check.py` | PRISMA cascade arithmetic |
| `check_prisma_figure.py` | manuscript versus PRISMA figure |

---

[← Back](README.md) · [Installation](Installation.md) · [Workflow](Workflow.md) · [FAQ](FAQ.md)

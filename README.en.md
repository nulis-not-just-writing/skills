# Claude skills for journal article writing

*[Baca dalam bahasa Indonesia](README.md)*

Five Claude skills for writing, polishing, submitting, and revising journal articles at Q1
(Scopus/WoS) standard — plus one for running a systematic literature review end to end.

**Any field, any research design.** What differs between fields is not the workflow but the
convention, and these skills pick the right convention instead of flattening everything: claim
strength, section structure, and reporting standard are calibrated to your field and design.
IMRaD is not a law of nature, and a mathematics paper is not forced into the shape of a biology
paper.

## The skills

| Skill | Answers | Version |
|---|---|---|
| [`nulis`](nulis/) | does each section carry the right *moves*, and is every RQ traceable from gap to contribution? | 1.4.0 |
| [`polish-manuscript`](polish-manuscript/) | is the prose clear, the argument sound, the claims calibrated? | 1.4.0 |
| [`submit`](submit/) | will this survive the editor's first ten minutes, or come back before review? | 1.5.0 |
| [`revisi`](revisi/) | is every reviewer comment answered, and can the editor *find* each change? | 1.3.0 |
| [`slr-cowork`](slr-cowork/) | do the numbers reconcile and will the method hold up? | 1.5.0 |

## ⚠ A note on language

**The skills reply in whatever language you write in.** Ask in English, get English.

**The skill files themselves are written in Indonesian.** That text is instruction *to the model*,
not to you — Claude reads it fine and answers you in your language. You never need to read it.

**The documentation in [`docs/`](docs/) is in Indonesian.** If you want to read the guides rather
than just use the skills, you will need a translation. This is a real limitation, stated plainly
rather than hidden.

## Install

**Claude Desktop** — download a zip from [`dist/`](dist/), then
**Settings → Capabilities → Skills → Upload**. No git needed.

**Claude Code:**

```bash
git clone https://github.com/nulis-not-just-writing/skills.git
cp -R skills/nulis ~/.claude/skills/
```

Install only what you need — each skill works standalone.

## What makes them different

**Gates that stop, not lists that sprawl.** `submit` runs in order from cheapest and most lethal.
One fatal finding makes the rest irrelevant: it stops, reports, and does not carry on sweeping.
No point polishing hyphens in a manuscript aimed at the wrong journal.

**What can be counted is counted.** Acronyms, spelling, p-values, units, word limits, two-way
citation cross-checks, PRISMA cascade arithmetic — all handled by deterministic scripts you can
re-run, not judged by impression.

**Citations are never invented.** A tiered ladder: MCP tools if present, then DOI resolution, then
an explicit **"unverified"** flag. The rule that holds at all three tiers: a citation is never
accepted because it *looks plausible* — a plausible-looking author-year-journal combination is the
signature pattern of a fabricated reference.

**Editing must not destroy evidence.** `polish-manuscript` has a fidelity gate: every number and
every citation present before editing **must** still be present after. If one goes missing, that
passage is reverted and reported — not quietly patched.

**A step that cannot run is not counted as passed.** A script that fails to execute is reported as
a skipped step, never as "a problem with the manuscript". The two are never mixed in one findings
table.

**Each skill stands alone.** Fully functional on its own. If a neighbour is installed, some steps
go deeper — but nothing stalls because another skill is absent.

## Requirements

Nothing is mandatory. All five work without any of the tools below; what shrinks is speed and
traceability, not rigour — and the skill is required to *say* what it skipped.

| Tool | Used for | Without it |
|---|---|---|
| Python 3 | mechanical sweeps, fidelity gate, PRISMA audits | done manually, reduced coverage |
| pandoc | reading `.docx` | export to `.md` or `.tex` |
| MCP `scholar`/`zotero` | citation verification + retraction detection | falls back to web lookup, then explicit flagging |
| R + `robvis` | risk-of-bias traffic-light figures | robvis web app, or a study × domain table |

Every Python script is **stdlib-only** — no `pip install`, no virtualenv — and tested on both the
macOS system Python 3.9.6 and 3.12.

## Licence

**[CC BY-NC 4.0](LICENSE)**. Free to use, copy, adapt, and share **for non-commercial purposes**
with attribution. Commercial use — including paid training and paid products — needs separate
permission from the rights holder.

Researchers, students, lecturers, and educational institutions using these for research and
teaching need no permission at all; just credit the source.

Some content comes from third parties under different licences (MIT, CC BY 4.0). See
[`NOTICE.md`](NOTICE.md) at the root **and inside every skill** — both must travel with any
redistribution.

Quality-assessment instruments (RoB 2, ROBINS-I, AMSTAR 2, MMAT, AXIS) are **not reproduced** here
— only own-words summaries with citations, because a CrossRef metadata check showed the first
three carry only a text-and-data-mining licence and the other two have no registered licence at
all. Download the official forms from their own sources for submission appendices.

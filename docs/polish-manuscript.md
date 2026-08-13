# polish-manuscript — prose & mechanics

*[Baca dalam bahasa Indonesia](id/polish-manuscript.md)*

**v1.4.0** · [download zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/polish-manuscript-1.4.0.zip)

A ten-dimension audit of a draft whose structure is already sound. It acts as Senior Research
Assistant, Methodology Expert, Academic Logic Expert, and International Journal Editor at once.

## What it is actually for

### 1. The structure is right but the sentences are heavy

> *"This manuscript is complete but reads stiff and long-winded. Polish it."*

Ten dimensions are swept in order, from sentence clarity to claim calibration. What can be counted
is counted by scripts; what needs judgement is judged by the model. Your voice is preserved — the
goal is to clarify, **not** to flatten everything until all manuscripts sound alike.

### 2. You are worried it "smells like AI"

A reasonable worry, and one people usually check by reading aloud and guessing.

`cek-variasi-kalimat.py` replaces the guess with a number: it measures **burstiness** — the spread
of sentence lengths. Human prose rises and falls; generative prose tends to flatten. The number
shows **which paragraph** has gone flat, rather than issuing a verdict on the whole manuscript.

### 3. Numbers and terms drift between sections

The abstract says 340 respondents, Methods says 342. An acronym gets defined twice. `0,05` where
`0.05` was meant — a signature error for Indonesian authors writing in English, and checked
separately for exactly that reason.

`lint-mekanis.py` sweeps all of it deterministically. Re-run it any time and get the same result.

### The gate that matters most

Prose editing carries a risk few people notice: **a tidied sentence can lose a number or a
citation**. That is not polishing any more; that is losing evidence.

Hence `cek-fidelitas-suntingan.py`. Copy the manuscript **before** editing, then compare
afterwards. `ANGKA_BERGESER` and `SITASI_HILANG` are Major — that passage is **reverted and
reported**, never quietly patched.

This is the step most often missing from comparable tools, and the most expensive one to be
without.

## When to use it

- The draft is done but reads stiff or long-winded
- You are worried the manuscript "smells like AI"
- Numbers and acronyms are inconsistent between sections
- The claims feel either too bold or too timid

## Ten dimensions

1. Clarity, coherence, style
2. Argument construction
3. Cross-section consistency
4. IMRaD/CARS structure
5. Canonical terminology
6. **Generative-AI marker elimination**
7. **Mechanical conventions** — tense, acronyms, SI units
8. Statistical reporting & number validation
9. Figures/tables & required sections
10. Claim calibration

## Three scripts

All **stdlib-only**, no `pip install`.

| Script | Does |
|---|---|
| `lint-mekanis.py` | almost all of dimension 7 — acronyms, US/UK spelling, p-values, units, **decimal commas** |
| `cek-variasi-kalimat.py` | measures burstiness for dimension 6 — replaces "read it aloud and listen" with a number |
| `cek-fidelitas-suntingan.py` | **the gate**: every number and citation present before editing must still be present after |

The decimal-comma check was added deliberately: it is the signature error of Indonesian authors
writing English manuscripts — `0,05` where `0.05` was meant.

## The fidelity gate

Copy the manuscript before editing, then afterwards:

```bash
python ~/.claude/skills/polish-manuscript/scripts/cek-fidelitas-suntingan.py \
    --sebelum /tmp/naskah-sebelum.tex --sesudah NASKAH.tex --strict
```

`ANGKA_BERGESER` and `SITASI_HILANG` are **Major**. When they fire, the passage is restored to its
original form and reported to the author — not fixed unilaterally.

## Non-negotiable rules

**An environment failure is not a manuscript finding.** A script that cannot run is reported as a
skipped step, never as "a problem with the manuscript".

**The author's voice is preserved.** The aim is clarity, not homogenisation into something that
sounds like AI.

---

[← Back](README.md) · [Installation](Installation.md) · [Workflow](Workflow.md) · [FAQ](FAQ.md)

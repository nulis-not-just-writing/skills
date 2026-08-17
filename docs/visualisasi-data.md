# visualisasi-data — figures that speak the language of the research

*[Baca dalam bahasa Indonesia](id/visualisasi-data.md)*

**v1.0.0** · [download zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/visualisasi-data-1.0.0.zip)

Designs and draws scientific figures whose **visual form follows the research context** rather than
defaulting to bars and lines — and then holds them to the rules that make a figure true: data
fidelity, visible spread, colour-blind safety, print specification, caption, pre-submission QA.

## The problem it addresses

A weak figure rarely fails on aesthetics. It fails because **its shape says nothing about the thing
being studied**.

Alpha power at 14 electrodes becomes a 14-bar chart. Prevalence across 38 provinces becomes 38
sorted bars. Ten studies in a meta-analysis become a table. Every one of those is "correct", and
every one throws away information that was already in the data — that electrodes have positions on
a scalp, provinces have positions on a map, and studies have different precision.

## The referent test

Before choosing a chart type, answer one question: **what is a single row of this data, in the real
world?** The visual form follows that answer, not habit.

| One row of data is… | Correct visual language | Not |
|---|---|---|
| A position on the scalp | Topography / 10-20 montage | A bar per electrode |
| An administrative region | Map, cartogram, tile-grid | Sorted bars per region |
| One study in a synthesis | Forest plot | A table of effect sizes |
| An ordinal questionnaire item | Diverging stacked bar | Bars of mean Likert scores |
| A coefficient in a model | Dot-whisker plot | A regression table |
| Latent constructs and their paths | A path diagram redrawn from the estimates | A SmartPLS screenshot |
| Persons **and** items on one scale | Wright map (Rasch) | Bars of mean scores |
| Two continuous inputs → one output | 3D surface **+** 2D contour | 3D alone, or a table |
| Alternatives × many criteria | Parallel coordinates | Score bars / radar plot |

A bar chart becomes legitimate only when the referent genuinely *is* an abstract category with no
position, order, or relation — and even then individual data points must sit on top of it when
n < 25.

The full table runs to 22 rows and covers alluvial flows, event studies, Lorenz curves, Pareto
fronts, confusion matrices, waterfall charts, PRISMA/CONSORT flows, and more.

## Three layers in every finished figure

The one most often missing is the third.

1. **Substrate** — the field the data is laid on: a head, a map, a genome, a time axis, a matrix, a
   latent space. This is what makes a figure speak the domain's language.
2. **Quantity channel** — how numbers are mapped: sequential colour for one-directional magnitude,
   diverging colour for signed magnitude centred on a semantic zero, position, size. One quantity,
   one channel.
3. **Uncertainty** — spread across replicates drawn behind the mean, confidence intervals, n
   written down, test results reported as they are **including the non-significant ones**. "n.s." is
   a result, not an absence.

## Fourteen domain routes, and no dead end for the rest

Fourteen domain files are loaded on demand — EEG/MEG/fNIRS, geospatial, clinical/epidemiology,
omics, ML engineering, survey/psychometrics, education and Rasch/IRT, economics and business,
PLS-SEM and CB-SEM, qualitative, chemistry and materials, environmental and geosciences,
bibliometrics and review, 3D surfaces and MCDM. Each carries that domain's canonical forms, the
usual traps, and code recipes.

**A field not on the list is not a dead end.** The visual substrate is not determined by the name of
a field but by the **structure of its data**, and there is a finite number of those structures. A
separate reference maps 22 structures — position on a physical object, cyclic time, directional
data, the crossing of two categories, flows, hierarchies, trade-offs, agreement between two
instruments — each to its substrate, plus a five-step procedure for finding the convention of a
field you do not yet know.

The rule is explicit: **never fall back to a bar chart just because the field is not listed.**

## Honesty limits

**Geometry is never invented.** Electrode positions, regional boundaries, map coordinates, and
molecular structures come from standard sources — not estimated. If the source is missing, the skill
says so and asks for it, or draws a schematic that is **explicitly labelled as schematic**.

**Data is never invented.** If the data does not exist yet, the skeleton figure is drawn with
placeholder data marked `[DATA PLACEHOLDER]` *inside the image*, so it cannot reach the manuscript
unnoticed.

**Null results are not smoothed away.** A non-significant result is still drawn and still labelled.
A panel title may not claim more than its test supports.

**Illustrative traces** — simulations drawn to explain a mechanism — must be generated from the
study's own measured parameters, and labelled "illustrative" both inside the panel *and* in the
caption.

## Verification you can actually run

Three checks catch three different classes of defect, and the third is the one usually skipped:

| Check | Catches |
|---|---|
| `check_layout` | layout: panels collapsing to zero size — raised as an error, not a warning |
| `check_overlaps` | geometric: text overlapping text, or colliding with a spine |
| Panel crops → **look at the image** | perceptual: low-contrast labels, crossed leader lines, swapped series colours |

A geometric check cannot see a swapped colour. Only looking at the rendered panel can.

There is also a command-line sweep against the saved file:

```bash
python scripts/figcheck.py figures/fig2_topografi.png --kolom single
```

## Print-ready by construction

Vector (PDF/EPS) for the manuscript plus 300 dpi PNG for preview, written by a single
`save_figure()` call. Font size **at final print size** at least 7 pt. Width follows the journal's
column — typically 85 mm single, 180 mm double. The target is asked for in step 0, **before**
anything is drawn, not after.

## When to use it

- You need a figure for a journal article and want it to look like it belongs in that field
- Your figures are monotonous — everything ends up a bar chart or a line chart
- A reviewer said your figures are uninformative, unreadable, or below specification
- You are preparing images for `.tex` or `.docx` and need column widths and fonts to be right
- You have a PLS-SEM model and are about to paste a SmartPLS screenshot into the manuscript
- Two hyperparameters sweep into one metric and a table is hiding the shape of it

## Requirements

This is the one skill in the repository that is **not stdlib-only**. `matplotlib` and `numpy` are
required; `scipy`, `pillow`, `pypdf`, and `mne` are optional and only deepen particular checks.
`topomap` does **not** need MNE — the 10-20 coordinates are baked into the module.

See [Requirements](Requirements.md).

## Where it sits in the chain

`nulis` decides which results deserve to be figures · **`visualisasi-data`** designs and draws them
· `polish-manuscript` checks for orphan figures — referenced but absent, or present but never
referenced · `submit` checks the figures against the journal's author guidelines · `revisi` handles
reviewers' figure requests.

---

[← Back](README.md) · [Installation](Installation.md) · [Workflow](Workflow.md) · [FAQ](FAQ.md)

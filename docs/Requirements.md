# Requirements & environment

*[Baca dalam bahasa Indonesia](id/Prasyarat.md)*

**Nothing is mandatory.** All five skills work without any of the tools below — what shrinks is
speed and traceability, not the obligations. The skill is required to *say* what it skipped rather
than skipping it quietly.

| Tool | For | Without it |
|---|---|---|
| **Python 3** | mechanical sweeps, fidelity gate, PRISMA audits | done manually, reduced coverage |
| **pandoc** | reading `.docx` manuscripts | export the manuscript to `.md` or `.tex` |
| **MCP `scholar` / `zotero`** | citation verification + retraction detection | falls back to `WebSearch`/`WebFetch`, then to manual flagging |
| **R + the `robvis` package** | risk-of-bias traffic-light figures | the robvis web app (no R needed), or a study × domain table |

## Python

Every script is **stdlib-only** — no `pip install`, no virtualenv. Tested on both the macOS system
Python 3.9.6 and 3.12.

```bash
python3 -V     # check
```

Not installed? macOS: `xcode-select --install`. Windows: `winget install Python.Python.3.12`.

### ⚠ CA certificates on macOS

Python from python.org **does not ship CA certificates**. The consequence is that `verify_refs.py`
reports **every** reference as `UNVERIFIED` — including the ones that genuinely exist.

That is a network failure, **not a manuscript finding**. If all references turn `UNVERIFIED` at
once, suspect the certificates first:

```bash
python3 -c "import ssl,os; p=ssl.get_default_verify_paths().openssl_cafile; print(p, os.path.exists(p))"
"/Applications/Python 3.12/Install Certificates.command"   # adjust the version number
```

Each Python version has its own certificate directory — installing a new version reintroduces the
problem.

## pandoc

Only affects `.docx` input. For `.tex` and `.md`, every script runs fully.

```bash
brew install pandoc          # macOS
winget install JohnMacFarlane.Pandoc
```

## MCP for citation verification

Without MCP, verification still runs through `WebSearch`/`WebFetch` — resolve the DOI at `doi.org`,
match title, first author, year, and journal name. What cannot be done without MCP: **automatic
retraction detection**.

The rule that holds at all three tiers: **a citation is never accepted because it "looks
plausible"**. A plausible-looking author–year–journal combination is the signature pattern of a
fabricated reference.

## R + robvis (`slr-cowork` only)

Only for risk-of-bias figures. **There is a web app**, so R is not required at all.

```r
install.packages("robvis")
```

---

[← Back](README.md) · [Installation](Installation.md) · [Workflow](Workflow.md) · [FAQ](FAQ.md) · [Licence](Licence.md)

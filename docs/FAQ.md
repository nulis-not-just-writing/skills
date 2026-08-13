# FAQ

*[Baca dalam bahasa Indonesia](id/Tanya-jawab.md)*

## Do I have to install all five?

No. **Each skill works fully on its own.** Install what you need. If a neighbour is present some
steps go deeper — but nothing stalls because another skill is absent.

## How do I invoke them?

You do not. A skill activates by itself when you mention something relevant — *"help me write the
introduction"*, *"my manuscript was rejected without review"*, *"I want to do a systematic
review"*.

## Do I need Python?

Not required. Without Python some dimensions are done manually and **the skill is required to say
that coverage is reduced** — rather than skipping quietly. If you do have it, no `pip install` is
needed: every script is stdlib-only.

## All my references suddenly came back `UNVERIFIED`. Is my manuscript broken?

Almost certainly **not**. Suspect the CA certificates first — Python from python.org on macOS does
not ship them, and the result is that every lookup fails at once. See
[Requirements](Requirements.md).

A network failure is **not a manuscript finding**.

## My manuscript is in Indonesian. Does that work?

Yes. **The conversation follows your language** — ask in Indonesian, get Indonesian. The
manuscript's language is separate and follows the target journal — usually English, and there is a
dedicated check for **Indonesian calques** that commonly slip through: *"It is known that…"*, *"It
can be concluded…"*, `0,05` where `0.05` was meant.

## My corpus is national journals. Scopus returns very few hits.

That is a feature of **index coverage, not of the field**. A re-measurement on 12 August 2026 found
indexed Indonesian journals (OJS) deposit abstracts to Crossref on 92–100% of records, while three
Elsevier education journals deposited **0%**.

`slr-cowork` includes Garuda, Moraref, SINTA, and PTKIN repository routes, plus a rule requiring
you to state coverage limitations in the Limitations section.

## I do not speak Indonesian. Can I use these?

Yes, fully. **The skills reply in whatever language you write in** — ask in English, get English.

Both this documentation and the Indonesian version are maintained: English pages live in `docs/`,
Indonesian in [`docs/id/`](id/README.md).

The one thing still in Indonesian is the **content of the skill files themselves**. That text is
instruction *to the model*, not to you — Claude reads it and answers in your language. You never
need to read it.

## May I use these for paid training?

**Not without permission.** The licence is CC BY-NC 4.0 — non-commercial. For research and
teaching (including regular university classes) no permission is needed at all; just credit the
source. See [Licence](Licence.md).

## May I modify and redistribute my own version?

Yes, for non-commercial purposes, with attribution. **`NOTICE.md` must travel with it** — there is
one at the root and one inside each skill, and their contents differ according to what that skill
carries.

## Can I use these in ChatGPT / Gemini?

The files are ordinary markdown, so any model can read the content. But the Skill format —
automatic loading, progressive disclosure, script execution — is Claude-specific. Elsewhere you
would have to paste the content manually.

## I found a methodological error. Where do I report it?

Open an issue in the [repo](https://github.com/nulis-not-just-writing/skills/issues). Include the
skill, the file, and the source you believe is correct — with a DOI if there is one, it is far
faster to verify.

---

[← Back](README.md) · [Installation](Installation.md) · [Workflow](Workflow.md) · [Requirements](Requirements.md) · [Licence](Licence.md)

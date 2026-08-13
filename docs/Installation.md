# Installation

*[Baca dalam bahasa Indonesia](id/Pemasangan.md)*

Two ways, depending on which Claude you use.

## Claude Desktop — easiest, no git

**Not sure which Claude you have?** If you use Claude in a browser or a desktop application, this
is your section. If you type `claude` into a terminal, skip to [Claude Code](#claude-code--copy-or-symlink).

1. **Download** the skill you want. Each link saves the file straight to your computer:

   | Skill | What it does | Download |
   |---|---|---|
   | `nulis` | article structure | [nulis-1.4.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/nulis-1.4.0.zip) |
   | `polish-manuscript` | prose & mechanics | [polish-manuscript-1.4.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/polish-manuscript-1.4.0.zip) |
   | `submit` | pre-submission gate | [submit-1.5.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/submit-1.5.0.zip) |
   | `revisi` | after the editor's decision | [revisi-1.3.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/revisi-1.3.0.zip) |
   | `slr-cowork` | systematic review | [slr-cowork-1.5.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/slr-cowork-1.5.0.zip) |

   **Do not unzip it.** Claude Desktop wants the `.zip` exactly as downloaded.

2. Open Claude Desktop → **Settings** → **Capabilities** → **Skills**
3. Click **Upload**
4. Choose the `.zip` you just downloaded

Done. **You never call the skill by name** — it activates on its own when you mention something
relevant. Try *"I want to start writing an article from this survey data"* and `nulis` should wake
up.

> The zip filename carries the version. When an update lands, the filename differs — so you always
> know which version you have installed.

## Claude Code — copy or symlink

```bash
git clone https://github.com/nulis-not-just-writing/skills.git
cd skills
```

**Copy** (simple, but does not follow updates):

```bash
cp -R nulis polish-manuscript submit revisi slr-cowork ~/.claude/skills/
```

**Symlink** (follows updates on every `git pull`):

```bash
for s in nulis polish-manuscript submit revisi slr-cowork; do
  ln -s "$PWD/$s" ~/.claude/skills/$s
done
```

Install only what you need — all five stand alone.

## Confirming it is installed

In Claude Code:

```bash
ls -la ~/.claude/skills/
```

Then try triggering it with an ordinary sentence, e.g. *"I want to start writing an article from
this survey data"* — `nulis` should activate without you naming it.

## Updating

```bash
cd skills && git pull
```

If you used a **symlink**, that is all. If you **copied**, repeat the `cp -R`. For Claude Desktop,
download the new zip and upload it again.

## Uninstalling

```bash
rm ~/.claude/skills/nulis          # symlink
rm -rf ~/.claude/skills/nulis      # copy
```

In Claude Desktop: **Settings → Capabilities → Skills**, then remove it from the list.

---

[← Back](README.md) · [Workflow](Workflow.md) · [Requirements](Requirements.md) · [FAQ](FAQ.md) · [Licence](Licence.md)

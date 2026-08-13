# Installation

*[Baca dalam bahasa Indonesia](id/Pemasangan.md)*

Two ways, depending on which Claude you use.

## Claude Desktop — easiest, no git

1. Open the [`dist/` folder](https://github.com/nulis-not-just-writing/skills/tree/main/dist) in the repo
2. Download the skill zip you want (e.g. `nulis-1.4.0.zip`)
3. In Claude Desktop: **Settings → Capabilities → Skills → Upload**
4. Select the zip

Done. The skill activates by itself when you mention something relevant — you never call it by
name.

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

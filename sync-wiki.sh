#!/usr/bin/env bash
# Cerminkan docs/ ke GitHub Wiki, dua bahasa.
#
# docs/ adalah SUMBER KANONIK — ia ikut versi bersama skill yang dijelaskannya.
# Wiki hanyalah cerminan. Jangan pernah menyunting wiki langsung: perubahannya
# akan tertimpa saat sinkronisasi berikutnya.
#
# Pemetaan halaman:
#   docs/README.md        →  Home            docs/id/README.md       →  ID-Beranda
#   docs/Installation.md  →  Installation    docs/id/Pemasangan.md   →  ID-Pemasangan
#   docs/Workflow.md      →  Workflow        docs/id/Alur-kerja.md   →  ID-Alur-kerja
#   docs/Requirements.md  →  Requirements    docs/id/Prasyarat.md    →  ID-Prasyarat
#   docs/FAQ.md           →  FAQ             docs/id/Tanya-jawab.md  →  ID-Tanya-jawab
#   docs/Licence.md       →  Licence         docs/id/Lisensi.md      →  ID-Lisensi
#   docs/<skill>.md       →  <skill>         docs/id/<skill>.md      →  ID-<skill>
#
# Wiki TIDAK berada di dalam pohon repo, jadi tautan relatif ke luar docs/ pasti
# mati kalau dibiarkan. Tiga kelas tautan ditulis ulang: sesama halaman docs jadi
# nama halaman wiki, lintas bahasa jadi nama pasangannya, dan tautan ke berkas
# repo jadi URL absolut.
#
# Arti "../" bergantung kedalaman berkas sumbernya: di docs/ menunjuk akar repo,
# di docs/id/ menunjuk docs/. Kedua folder diproses dengan aturan terpisah.
#
# Prasyarat sekali seumur repo: wiki harus sudah punya minimal satu halaman.
# GitHub baru membuat repo wiki setelah halaman pertama dibuat lewat antarmuka
# web — tidak ada API-nya.

set -euo pipefail
cd "$(dirname "$0")"

SLUG="nulis-not-just-writing/skills"
REMOTE="https://github.com/$SLUG.wiki.git"
BLOB="https://github.com/$SLUG/blob/main"
TREE="https://github.com/$SLUG/tree/main"

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

if ! git clone -q "$REMOTE" "$WORK/wiki" 2>/dev/null; then
  echo "✗ Repo wiki belum ada."
  echo "  Buka https://github.com/$SLUG/wiki"
  echo "  → 'Create the first page' → isi apa saja → Save Page."
  echo "  Lalu jalankan skrip ini lagi."
  exit 1
fi

W="$WORK/wiki"
find "$W" -maxdepth 1 -name '*.md' -delete

# ── Halaman Inggris (docs/*.md) ────────────────────────────────────────
for src in docs/*.md; do
  base=$(basename "$src")
  [ "$base" = "README.md" ] && dst="$W/Home.md" || dst="$W/$base"
  sed -E "
    s#\]\(\.\./([^)]*/)\)#](${TREE}/\1)#g
    s#\]\(\.\./([^)]+)\)#](${BLOB}/\1)#g
    s#\]\(id/README\.md\)#](ID-Beranda)#g
    s#\]\(id/([A-Za-z0-9_-]+)\.md\)#](ID-\1)#g
    s#\]\(README\.md\)#](Home)#g
    s#\]\(([A-Za-z0-9_-]+)\.md\)#](\1)#g
  " "$src" > "$dst"
done

# ── Halaman Indonesia (docs/id/*.md) ───────────────────────────────────
for src in docs/id/*.md; do
  base=$(basename "$src")
  case "$base" in
    README.md) dst="$W/ID-Beranda.md" ;;
    *)         dst="$W/ID-${base}" ;;
  esac
  sed -E "
    s#\]\(\.\./\.\./([^)]*/)\)#](${TREE}/\1)#g
    s#\]\(\.\./\.\./([^)]+)\)#](${BLOB}/\1)#g
    s#\]\(\.\./README\.md\)#](Home)#g
    s#\]\(\.\./([A-Za-z0-9_-]+)\.md\)#](\1)#g
    s#\]\(README\.md\)#](ID-Beranda)#g
    s#\]\(([A-Za-z0-9_-]+)\.md\)#](ID-\1)#g
  " "$src" > "$dst"
done

# ── Sidebar & footer ───────────────────────────────────────────────────
cat > "$W/_Sidebar.md" <<EOF
**[Home](Home)** · [Bahasa Indonesia](ID-Beranda)

**Start**
- [Installation](Installation)
- [Workflow](Workflow)
- [Requirements](Requirements)

**Skills**
- [nulis](nulis)
- [polish-manuscript](polish-manuscript)
- [submit](submit)
- [revisi](revisi)
- [slr-cowork](slr-cowork)

**More**
- [FAQ](FAQ)
- [Licence](Licence)

---

**[Bahasa Indonesia](ID-Beranda)**
- [Pemasangan](ID-Pemasangan)
- [Alur kerja](ID-Alur-kerja)
- [Prasyarat](ID-Prasyarat)
- [nulis](ID-nulis)
- [polish-manuscript](ID-polish-manuscript)
- [submit](ID-submit)
- [revisi](ID-revisi)
- [slr-cowork](ID-slr-cowork)
- [Tanya jawab](ID-Tanya-jawab)
- [Lisensi](ID-Lisensi)
EOF

# Footer muncul di SETIAP halaman wiki, jadi kata penutupnya cukup ditulis
# sekali di sini — tidak perlu disalin ke tiap halaman.
cat > "$W/_Footer.md" <<EOF
---

> **Knowledge unshared dies. Knowledge shared keeps living.**
>
> It grows in hands you will never meet and is carried on in work you will never read — and what
> never stops living never stops returning to you.

**Mubaroq ADB** · Akademi Digital Bandung | RPI Institute · <mubaroq@digitalbdg.ac.id>

<sub>Mirror of \`docs/\` — do not edit here; edit in the [repository]($TREE/docs). ·
Cerminan \`docs/\`, jangan disunting di sini. · CC BY-NC 4.0</sub>
EOF

# ── Gerbang: tidak boleh ada tautan yang pasti mati di wiki ────────────
sisa=$(grep -rlE '\]\((\.\./|[A-Za-z0-9_-]+\.md\))' "$W" 2>/dev/null || true)
if [ -n "$sisa" ]; then
  echo "✗ Masih ada tautan relatif/berekstensi yang akan mati di wiki:"
  for f in $sisa; do
    printf '  %s\n' "$(basename "$f")"
    grep -oE '\]\((\.\./[^)]*|[A-Za-z0-9_-]+\.md)\)' "$f" | sed 's/^/     /' | sort -u
  done
  exit 1
fi

cd "$W"
if [ -z "$(git status --porcelain)" ]; then
  echo "  Tidak ada perubahan — wiki sudah sama dengan docs/."
  exit 0
fi

git add -A
git -c user.name="Mubaroq ADB" -c user.email="isma@upi.edu" \
    commit -q -m "Segarkan dari docs/ (cerminan otomatis, dua bahasa)"
git push -q origin HEAD
echo "  ✓ Wiki disegarkan: $(ls *.md | wc -l | tr -d ' ') halaman"

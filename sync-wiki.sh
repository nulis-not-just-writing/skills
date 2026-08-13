#!/usr/bin/env bash
# Cerminkan docs/ ke GitHub Wiki.
#
# docs/ adalah SUMBER KANONIK — ia ikut versi bersama skill yang dijelaskannya.
# Wiki hanyalah cerminan. Jangan pernah menyunting wiki langsung: perubahannya
# akan tertimpa saat sinkronisasi berikutnya.
#
# Perbedaan yang ditangani skrip ini:
#   docs/README.md        →  Home.md          (beranda wiki)
#   [teks](Nama.md)       →  [teks](Nama)     (wiki tanpa ekstensi)
#   _Sidebar / _Footer    →  dibangkitkan     (khusus wiki)
#
# Prasyarat sekali seumur repo: wiki harus sudah punya minimal satu halaman.
# GitHub baru membuat repo wiki setelah halaman pertama dibuat lewat antarmuka
# web — tidak ada API-nya. Buka .../wiki → "Create the first page" → Save.

set -euo pipefail
cd "$(dirname "$0")"

REMOTE="https://github.com/nulis-not-just-writing/skills.wiki.git"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

if ! git clone -q "$REMOTE" "$WORK/wiki" 2>/dev/null; then
  echo "✗ Repo wiki belum ada."
  echo "  Buka https://github.com/nulis-not-just-writing/skills/wiki"
  echo "  → 'Create the first page' → isi apa saja → Save Page."
  echo "  Lalu jalankan skrip ini lagi."
  exit 1
fi

W="$WORK/wiki"
find "$W" -maxdepth 1 -name '*.md' -delete

for src in docs/*.md; do
  base=$(basename "$src")
  [ "$base" = "README.md" ] && dst="$W/Home.md" || dst="$W/$base"
  # buang ekstensi .md dari tautan internal; README.md → Home
  sed -E 's/\]\(README\.md\)/](Home)/g; s/\]\(([A-Za-z0-9_-]+)\.md\)/](\1)/g' "$src" > "$dst"
done

cat > "$W/_Sidebar.md" <<'EOF'
**[Beranda](Home)**

**Mulai**
- [Pemasangan](Pemasangan)
- [Alur kerja](Alur-kerja)
- [Prasyarat](Prasyarat)

**Skill**
- [nulis](nulis)
- [polish-manuscript](polish-manuscript)
- [submit](submit)
- [revisi](revisi)
- [slr-cowork](slr-cowork)

**Lain**
- [Tanya jawab](Tanya-jawab)
- [Lisensi](Lisensi)
EOF

cat > "$W/_Footer.md" <<'EOF'
Cerminan dari `docs/` — jangan disunting di sini, suntinglah di
[repo](https://github.com/nulis-not-just-writing/skills/tree/main/docs).
CC BY-NC 4.0 · Mubaroq ADB | RPI
EOF

cd "$W"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "  Tidak ada perubahan — wiki sudah sama dengan docs/."
  exit 0
fi

git add -A
git -c user.name="Mubaroq ADB" -c user.email="isma@upi.edu" \
    commit -q -m "Segarkan dari docs/ (cerminan otomatis)"
git push -q origin HEAD
echo "  ✓ Wiki disegarkan: $(ls *.md | wc -l | tr -d ' ') halaman"

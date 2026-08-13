#!/usr/bin/env bash
# Bangun ulang zip siap pasang dari sumber di repo ini.
#
# Nama berkasnya memuat versi (mis. nulis-1.3.0.zip) supaya sebuah zip tidak
# pernah "basi": versi baru menghasilkan berkas baru, bukan menimpa yang lama.
# Jalankan setiap kali versi skill dinaikkan, lalu commit hasilnya.
#
#   ./build-zips.sh          bangun semua
#   ./build-zips.sh nulis    bangun satu

set -euo pipefail
cd "$(dirname "$0")"
SKILLS=(nulis polish-manuscript submit revisi slr-cowork)
[ $# -gt 0 ] && SKILLS=("$@")

command -v zip >/dev/null || { echo "zip tidak ada di PATH"; exit 1; }
mkdir -p dist

for s in "${SKILLS[@]}"; do
  [ -f "$s/SKILL.md" ] || { echo "  ✗ $s: SKILL.md tidak ada"; exit 1; }

  v=$(awk '/^metadata:/{f=1} f&&/^  version:/{print $2; exit}' "$s/SKILL.md")
  [ -n "$v" ] || { echo "  ✗ $s: versi tidak terbaca dari frontmatter"; exit 1; }

  # buang zip versi lama untuk skill ini supaya dist/ tidak menumpuk
  rm -f "dist/$s"-*.zip
  out="dist/$s-$v.zip"

  find "$s" -name '.DS_Store' -delete 2>/dev/null || true
  find "$s" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
  zip -r -q -X "$out" "$s" -x "*/.DS_Store" "*/__pycache__/*" "*.pyc"

  # gerbang: NOTICE wajib ikut, sampah wajib nol.
  # Daftar isi diambil SEKALI ke variabel — `grep -q` di dalam pipeline akan
  # membuat `unzip` kena SIGPIPE dan `pipefail` salah membacanya sebagai gagal.
  listing=$(unzip -l "$out")

  case "$listing" in
    *"$s/NOTICE.md"*) ;;
    *) echo "  ✗ $out: NOTICE.md tidak ikut — atribusi wajib ada di tiap zip"; exit 1 ;;
  esac

  j=$(printf '%s\n' "$listing" | grep -cE '\.DS_Store|__MACOSX|__pycache__|\.pyc' || true)
  [ "$j" = "0" ] || { echo "  ✗ $out: $j berkas sampah ikut"; exit 1; }

  n=$(printf '%s\n' "$listing" | tail -1 | awk '{print $2}')
  printf "  ✓ %-32s v%-8s %2s berkas  %s\n" "$(basename "$out")" "$v" "$n" "$(du -h "$out" | cut -f1)"
done

echo
echo "  Selesai. Commit isi dist/ agar pengguna bisa mengunduh langsung."

#!/usr/bin/env python3
"""
Ukur variasi panjang kalimat (burstiness) — penopang dimensi 6.

Diadaptasi dari check_sentence_variety.py milik medsci-skills (MIT, Aperivue).
Lihat NOTICE.md di akar repo. Perubahan: keluaran bahasa Indonesia, dukungan .tex,
singkatan Indonesia ditambahkan, dan catatan provenance ambang di bawah.

MENGAPA INI ADA
`ai-stylometry-flags.md` §4 menyebut "keseragaman ritme" sebagai penanda AI, dan §1
menjelaskan burstiness rendah sebagai sinyal yang dipakai detektor. Tapi instruksinya
selama ini "baca keras, dengarkan ritmenya" — tidak ada yang mengukur. Padahal sapuan
anti-AI justru cenderung MERATAKAN ritme, bukan memulihkannya: model memendekkan
kalimat panjang dan memanjangkan yang pendek sampai semuanya berkumpul di tengah,
dan keseragaman itu sendiri adalah penanda.

AMBANG DAN ASALNYA (baca sebelum mengubah angkanya)
  --short-max 12 / --long-min 25  Bukan dari korpus mana pun. Ini spesifikasi skill itu
      sendiri: teks yang mensyaratkan campuran kalimat pendek dan panjang lalu tidak
      memuat salah satunya telah melanggar aturannya sendiri. Gerbang ini karena itu
      hanya menyala pada kasus yang tak ambigu — SATU BAND KOSONG — dan untuk selain
      itu hanya melaporkan sebarannya alih-alih mengarang batas.
  --long-max 70   Diwarisi dari versi asal: 2 x 35, dua kali batas atas rentang
      "kalimat panjang" 25-35. Penulis asalnya menguji pada 6 naskah miliknya dan
      angka 70 hanya menjaring ~1% kalimat, sedangkan batas 35 akan menghukum ~24%
      kalimat pada naskah yang mereka anggap baik.
      CATATAN JUJUR: validasi itu milik korpus mereka, bukan korpus Anda. Angka ini
      BELUM diuji ulang pada naskah Anda sendiri. Perlakukan sebagai titik awal yang
      masuk akal, bukan temuan empiris tentang tulisan Anda.

Vonis:
  KALIMAT_SERAGAM   (Minor) tidak ada kalimat pendek ATAU tidak ada yang panjang —
                            semuanya berkumpul di band tengah.
  KALIMAT_KEPANJANGAN (Minor) ada kalimat melebihi --long-max; pembaca kehilangan
                            subjek sebelum predikatnya tiba. Pecah.

Dibatasi agar positif palsunya rendah:
  * Heading, butir daftar, baris tabel, blok kode, dan front matter dikecualikan —
    panjangnya tidak mengatakan apa pun tentang ritme prosa.
  * Diam bila kalimatnya di bawah --min-sentences (default 15): abstrak atau catatan
    pendek terlalu sedikit untuk membuat ritme bermakna.

Pemakaian:
    python cek-variasi-kalimat.py NASKAH.tex
    python cek-variasi-kalimat.py NASKAH.md --json --out qc/variasi.json
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

FENCE_RE = re.compile(r"```.*?```", re.S)
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
SKIP_LINE_RE = re.compile(r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|\||>\s|!\[|\[.*\]:)")
CITE_RE = re.compile(r"\[@[^\]\s]+\]|\[\d+(?:\s*[-–,]\s*\d+)*\]")
WORD_RE = re.compile(r"[A-Za-z0-9''-]+")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[\"'(]?[A-Z0-9])")

# Singkatan yang titiknya tidak boleh mengakhiri kalimat. Urutan penting: panjang dulu.
SINGKATAN = (
    "et al.", "e.g.", "i.e.", "cf.", "vs.", "approx.", "Fig.", "Figs.", "Tab.", "No.",
    "Dr.", "Prof.", "St.", "Sr.", "Jr.", "Inc.", "Ltd.", "min.", "max.", "sec.",
    "dkk.", "dll.", "dsb.", "hlm.", "Vol.", "Ed.", "eds.", "terj.",
)
_SENTINEL = "\x00ABBR%d\x00"
_DOT = "\x00DOT\x00"

# Lingkungan LaTeX yang isinya bukan prosa.
TEX_ENV_RE = re.compile(
    r"\\begin\{(equation|align|table|tabular|figure|itemize|enumerate|lstlisting|verbatim)\*?\}"
    r".*?\\end\{\1\*?\}", re.S)


def baca_prosa(path: Path) -> tuple[str, str]:
    """Kembalikan (teks_prosa, catatan_sumber)."""
    suffix = path.suffix.lower()
    if suffix == ".tex":
        raw = path.read_text(encoding="utf-8", errors="ignore")
        raw = re.sub(r"(?<!\\)%.*", " ", raw)
        raw = TEX_ENV_RE.sub(" ", raw)
        raw = re.sub(r"\$[^$]*\$", " ", raw)
        raw = re.sub(r"\\(?:cite|ref|label|autoref|cref|eqref|includegraphics|input|usepackage)"
                     r"\w*(?:\[[^\]]*\])?\{[^}]*\}", " ", raw)
        raw = re.sub(r"\\(?:section|subsection|subsubsection|chapter|title|caption)"
                     r"\*?\{[^}]*\}", " ", raw)
        raw = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", raw)
        raw = raw.replace("{", " ").replace("}", " ")
        return " ".join(raw.split()), "dibaca langsung (markup LaTeX dibuang)"
    if suffix in (".md", ".markdown", ".txt"):
        return _prosa_markdown(path.read_text(encoding="utf-8", errors="ignore")), "dibaca langsung"
    try:
        out = subprocess.run(["pandoc", str(path), "-t", "markdown-smart", "--wrap=none"],
                             capture_output=True, text=True, check=True)
    except FileNotFoundError:
        sys.exit("Error: pandoc tidak ditemukan. Pasang pandoc, atau berikan .md/.tex/.txt.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc gagal membaca {path}\n{e.stderr.strip()}")
    return _prosa_markdown(out.stdout), "lewat pandoc"


def _prosa_markdown(text: str) -> str:
    """Hanya prosa badan: buang front matter, blok kode, heading, daftar, tabel, kutipan."""
    text = FRONTMATTER_RE.sub("", text)
    text = FENCE_RE.sub(" ", text)
    kept = [ln for ln in text.splitlines() if ln.strip() and not SKIP_LINE_RE.match(ln)]
    return " ".join(kept)


def pecah_kalimat(prosa: str) -> list[str]:
    masked = prosa
    for i, ab in enumerate(SINGKATAN):
        masked = masked.replace(ab, _SENTINEL % i)
    # Lindungi desimal ("0.05", "p = .03") dari pemecah kalimat.
    masked = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + _DOT + m.group(2), masked)
    masked = re.sub(r"(?<=[=<>]\s)\.(\d)", lambda m: _DOT + m.group(1), masked)

    out = []
    for part in SENT_SPLIT_RE.split(masked):
        restored = part.replace(_DOT, ".")
        for i, ab in enumerate(SINGKATAN):
            restored = restored.replace(_SENTINEL % i, ab)
        restored = restored.strip()
        if restored:
            out.append(restored)
    return out


def hitung_kata(kalimat: str) -> int:
    return len(WORD_RE.findall(CITE_RE.sub(" ", kalimat)))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Ukur variasi panjang kalimat (burstiness) — penopang dimensi 6.")
    ap.add_argument("path", help="Naskah (.tex/.md/.txt/.docx/...)")
    ap.add_argument("--out", type=Path, help="tulis JSON ke berkas ini")
    ap.add_argument("--short-max", type=int, default=12, help="kalimat pendek = <= sekian kata")
    ap.add_argument("--long-min", type=int, default=25, help="kalimat panjang = >= sekian kata")
    ap.add_argument("--long-max", type=int, default=70,
                    help="di atas ini dianggap kepanjangan (default 70 = 2 x 35; lihat docstring)")
    ap.add_argument("--min-sentences", type=int, default=15, help="diam bila kalimatnya kurang dari ini")
    ap.add_argument("--json", action="store_true", help="cetak JSON ke stdout")
    ap.add_argument("--strict", action="store_true", help="exit 1 bila ada vonis")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        sys.exit(f"Error: {path} tidak ditemukan")

    prosa, sumber = baca_prosa(path)
    panjang = [n for n in (hitung_kata(k) for k in pecah_kalimat(prosa)) if n > 0]

    vonis: list[dict] = []
    stat: dict = {"jumlah_kalimat": len(panjang)}

    if len(panjang) >= args.min_sentences:
        pendek = [n for n in panjang if n <= args.short_max]
        panjang_band = [n for n in panjang if n >= args.long_min]
        kepanjangan = sorted((n for n in panjang if n > args.long_max), reverse=True)
        stat.update({
            "jumlah_pendek": len(pendek),
            "jumlah_panjang": len(panjang_band),
            "median_kata": round(statistics.median(panjang), 1),
            "min_kata": min(panjang),
            "max_kata": max(panjang),
            "simpangan_baku": round(statistics.pstdev(panjang), 1),
            # Dilaporkan, tidak dihakimi: batas atas band adalah 35, tapi melampauinya
            # lazim pada naskah yang baik. Ini informasi untuk penyunting, bukan vonis.
            "di_atas_band_35": len([n for n in panjang if n > 35]),
            "kata_kalimat_kepanjangan": kepanjangan,
        })
        if not pendek or not panjang_band:
            hilang = "pendek" if not pendek else "panjang"
            band = f"<= {args.short_max} kata" if not pendek else f">= {args.long_min} kata"
            vonis.append({
                "vonis": "KALIMAT_SERAGAM", "tingkat": "Minor", "band_hilang": hilang,
                "pesan": (f"Tidak ada kalimat {hilang} ({band}) dari {len(panjang)} kalimat "
                          f"(median {stat['median_kata']}, rentang {stat['min_kata']}-{stat['max_kata']}). "
                          "Keseragaman panjang itu sendiri penanda AI — lihat ai-stylometry-flags.md §4."),
            })
        if kepanjangan:
            vonis.append({
                "vonis": "KALIMAT_KEPANJANGAN", "tingkat": "Minor", "jumlah": len(kepanjangan),
                "kata": kepanjangan,
                "pesan": (f"{len(kepanjangan)} kalimat melebihi {args.long_max} kata "
                          f"({', '.join(str(n) for n in kepanjangan)}). Band panjang adalah 25-35 kata; "
                          f"{args.long_max} dua kali batas atasnya, jadi ini bukan 'kalimat yang lebih "
                          "panjang' dalam arti yang dimaksud — pembaca kehilangan subjek sebelum "
                          "predikatnya tiba. Pecah."),
            })
    else:
        stat["dilewati"] = (f"hanya {len(panjang)} kalimat "
                            f"(< --min-sentences {args.min_sentences})")

    amplop = {"pemeriksa": "cek-variasi-kalimat", "berkas": str(path), "metode_baca": sumber,
              "short_max": args.short_max, "long_min": args.long_min, "long_max": args.long_max,
              "statistik": stat, "vonis": vonis}

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(amplop, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.json:
        print(json.dumps(amplop, indent=2, ensure_ascii=False))
    else:
        print(f"\nVARIASI KALIMAT — {path.name}")
        print("=" * 62)
        print(f"  sumber: {sumber}")
        if "dilewati" in stat:
            print(f"  DILEWATI — {stat['dilewati']}")
        else:
            print(f"  {stat['jumlah_kalimat']} kalimat | median {stat['median_kata']} kata | "
                  f"rentang {stat['min_kata']}-{stat['max_kata']} | simpangan {stat['simpangan_baku']}")
            print(f"  {stat['jumlah_pendek']} pendek (<= {args.short_max}) / "
                  f"{stat['jumlah_panjang']} panjang (>= {args.long_min})")
            print(f"  {stat['di_atas_band_35']} kalimat di atas 35 kata (dilaporkan, bukan vonis)")
        for v in vonis:
            print(f"\n  [{v['tingkat']}] {v['vonis']}")
            print(f"    {v['pesan']}")
        if not vonis and "dilewati" not in stat:
            print("\n  bersih: kedua band panjang kalimat terisi")

    if args.strict and vonis:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

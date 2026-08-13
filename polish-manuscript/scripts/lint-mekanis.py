#!/usr/bin/env python3
"""
Lint mekanis naskah: memeriksa konvensi yang bisa diperiksa mesin (dimensi 7).

Diadaptasi dari lint_consistency.py milik medsci-skills (MIT, Aperivue) — lihat
NOTICE.md di akar repo. Perubahan dari versi asal:
  - keluaran dalam bahasa Indonesia, mengikuti gaya laporan sweep.py
  - membaca .tex langsung (nomor baris tetap cocok dengan sumber), .docx lewat pandoc
  - kosakata medis diganti kosakata lintas bidang (pendidikan, sosial, teknik)
  - tambahan cek 9: desimal koma — galat khas penulis Indonesia yang menulis
    naskah berbahasa Inggris ("p = 0,05" alih-alih "p = 0.05")

Yang diperiksa:
  1. Akronim      - didefinisikan sekali, dipakai sebelum didefinisikan,
                    didefinisikan tapi tak pernah dipakai, dipakai tanpa definisi
  2. Ejaan        - campuran varian US/UK (analyze/analyse, behavior/behaviour)
  3. Rentang angka- hyphen di antara angka yang seharusnya en-dash (5-10)
  4. Nilai p      - campuran huruf P/p; "P = 0.000" yang mustahil
  5. Tanda hubung - varian bentuk istilah yang sama (follow-up/followup/follow up)
  6. Angka kecil  - digit 1-9 ditulis sebagai angka di dalam prosa
  7. Satuan       - tidak ada spasi antara nilai dan satuan (5mg)
  8. Pemisah ribuan - judul tabel/gambar memakai pemisah berbeda dari badan naskah
  9. Desimal koma - koma dipakai sebagai pemisah desimal di naskah Inggris

Script ini TIDAK PERNAH menulis ulang teks, mengubah angka, menyunting sitasi, atau
menilai isi ilmiah — hanya melaporkan. Urutan keluarannya stabil (deterministik),
jadi bisa dipakai sebagai pemeriksa regresi.

Pemakaian:
    python lint-mekanis.py NASKAH.tex
    python lint-mekanis.py NASKAH.md --strict   # exit 1 bila ada temuan
    python lint-mekanis.py NASKAH.docx --json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Konfigurasi (tetap, deterministik)
# --------------------------------------------------------------------------- #
# Akronim yang begitu lazim sehingga tidak perlu didefinisikan di dalam teks.
# Sengaja konservatif: akronim yang bermakna ganda antar bidang (SEM = structural
# equation modeling / standard error of the mean; PCA; ANOVA di sebagian jurnal)
# TIDAK dimasukkan, karena justru itulah yang wajib didefinisikan.
ABBR_WHITELIST = {
    "AI", "DNA", "RNA", "USA", "UK", "EU", "WHO", "UNESCO", "OECD", "PISA",
    "ID", "OK", "PDF", "URL", "HTML", "HTTP", "API", "AND", "OR", "NOT",
    "CD", "TV", "GPS", "IQ", "SD", "CI", "USD", "IDR",
}

# Keluarga ejaan US <-> UK: bentuk kanonik "us" -> regex yang cocok dengan varian UK.
#
# CATATAN PRESISI (dari versi asal, dipertahankan) — jangan "sederhanakan" empat
# yang pertama kembali menjadi `\w*`. Keluarga -ise/-ize bertabrakan dengan kata yang
# IDENTIK di kedua dialek, dan pencocokan sufiks yang rakus menghitungnya sebagai
# bukti UK:
#     analys + \w*        -> "analysis", "analyses"      (nomina universal)
#     organis + \w*       -> "organism", "organisms"     (universal)
#     characteris + \w*   -> "characteristic(s)"         (universal)
#     optimis + \w*       -> "optimism"                  (universal)
SPELLING_FAMILIES = [
    ("analyze", r"\banalys(e|ed|ing|able)\b"),
    ("organize", r"\borganis(e|es|ed|ing|ation|ations|ational|er|ers)\b"),
    ("characterize", r"\bcharacteris(e|es|ed|ing|ation|ations)\b"),
    ("optimize", r"\boptimis(e|es|ed|ing|ation|ations)\b"),
    ("randomize", r"\brandomis\w*\b"),
    ("standardize", r"\bstandardis\w*\b"),
    ("categorize", r"\bcategoris\w*\b"),
    ("conceptualize", r"\bconceptualis\w*\b"),
    ("operationalize", r"\boperationalis\w*\b"),
    ("behavior", r"\bbehaviour(s|al|ally)?\b"),
    ("color", r"\bcolour(s|ed|ing)?\b"),
    ("favor", r"\bfavour(s|ed|able)?\b"),
    ("center", r"\bcentre(s|d)?\b"),
    ("labeled", r"\blabelled\b"),
    ("modeling", r"\bmodelling\b"),
    ("program", r"\bprogramme(s|d)?\b"),
    ("practice", r"\bpractis(e|ed|ing)\b"),
    ("aging", r"\bageing\b"),
    ("judgment", r"\bjudgement(s)?\b"),
    ("enrollment", r"\benrolment(s)?\b"),
    ("fulfill", r"\bfulfil(s|led|ling)?\b"),
]
SPELLING_US = {
    "analyze": r"\banaly(z|ze|zed|zing|zes)\w*\b",
    "organize": r"\borganiz\w*\b",
    "characterize": r"\bcharacteriz\w*\b",
    "optimize": r"\boptimiz\w*\b",
    "randomize": r"\brandomiz\w*\b",
    "standardize": r"\bstandardiz\w*\b",
    "categorize": r"\bcategoriz\w*\b",
    "conceptualize": r"\bconceptualiz\w*\b",
    "operationalize": r"\boperationaliz\w*\b",
    "behavior": r"\bbehavior(s|al|ally)?\b",
    "color": r"\bcolor(s|ed|ing)?\b",
    "favor": r"\bfavor(s|ed|able)?\b",
    "center": r"\bcenter(s|ed)?\b",
    "labeled": r"\blabeled\b",
    "modeling": r"\bmodeling\b",
    "program": r"\bprogram(s|med)?\b",
    "practice": r"\bpractic(e|ed|ing)\b",
    "aging": r"\baging\b",
    "judgment": r"\bjudgment(s)?\b",
    "enrollment": r"\benrollment(s)?\b",
    "fulfill": r"\bfulfill(s|ed|ing)?\b",
}

# Keluarga varian tanda hubung/terminologi (dicocokkan tanpa peduli kapitalisasi).
# Dipilih yang sering muncul di naskah pendidikan, sosial, dan teknik.
HYPHEN_FAMILIES = [
    ("follow-up", [r"\bfollow-up\b", r"\bfollowup\b", r"\bfollow up\b"]),
    ("long-term", [r"\blong-term\b", r"\blongterm\b", r"\blong term\b"]),
    ("well-being", [r"\bwell-being\b", r"\bwellbeing\b"]),
    ("decision-making", [r"\bdecision-making\b", r"\bdecision making\b"]),
    ("meta-analysis", [r"\bmeta-analys[ei]s\b", r"\bmetaanalys[ei]s\b", r"\bmeta analys[ei]s\b"]),
    ("self-efficacy", [r"\bself-efficacy\b", r"\bself efficacy\b", r"\bselfefficacy\b"]),
    ("problem-solving", [r"\bproblem-solving\b", r"\bproblem solving\b"]),
    ("dataset", [r"\bdataset(s)?\b", r"\bdata set(s)?\b", r"\bdata-set(s)?\b"]),
    ("pre-test", [r"\bpre-test\b", r"\bpretest\b", r"\bpre test\b"]),
    ("post-test", [r"\bpost-test\b", r"\bposttest\b", r"\bpost test\b"]),
    ("e-learning", [r"\be-learning\b", r"\belearning\b"]),
    ("socio-economic", [r"\bsocio-economic\b", r"\bsocioeconomic\b"]),
    ("cross-sectional", [r"\bcross-sectional\b", r"\bcross sectional\b"]),
    ("semi-structured", [r"\bsemi-structured\b", r"\bsemistructured\b", r"\bsemi structured\b"]),
    ("higher-order", [r"\bhigher-order\b", r"\bhigher order\b"]),
]

# Satuan yang tidak ambigu bila menempel pada angka. Satuan satu huruf (m, s, K, V,
# W, J, N, B) SENGAJA tidak dimasukkan: "1990s" akan tertangkap sebagai "1990"+"s",
# dan "3D" sebagai angka+satuan. Kesalahan semacam itu membuat penulis berhenti
# menjalankan linter, yang jauh lebih mahal daripada satu-dua temuan yang terlewat.
UNIT_TOKENS = (
    "mg", "kg", "mL", "ml", "mm", "cm", "km", "ms", "min", "Hz", "kHz", "MHz",
    "dB", "kPa", "MPa", "px", "pt", "kB", "MB", "GB", "TB", "rpm", "mol",
)
UNIT_RE = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)(" + "|".join(sorted(UNIT_TOKENS, key=len, reverse=True)) + r")(?![\w])"
)

ABBR_DEF_RE = re.compile(r"\(([A-Z][A-Z0-9]{1,5})\)")
ABBR_USE_RE = re.compile(r"(?<![A-Za-z])([A-Z]{2,6})(?![A-Za-z])")
NUM_RANGE_RE = re.compile(r"(?<![\w/.\-])(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)(?![\w/.\-])")
PVAL_RE = re.compile(r"(?<![A-Za-z])([Pp])\s*([=<>])\s*(0?\.\d+|\d+\.\d+|\.\d+)")
SMALL_NUM_RE = re.compile(r"(?<![\w.=<>+\-/])([1-9])\s+([a-z]{3,})")

# Digit yang MENAMAI sesuatu bukan kuantitas terhitung, dan mengejanya justru salah.
# "type 2 diabetes" bukan "type two diabetes" — begitu pula Grade 3, Tahap 4, Item 7,
# Tabel 2, Gambar 1. Aturan ini semula menyala pada semuanya. Jadi kata penanda di
# depannya — bukan digitnya — yang menentukan.
#
# Sengaja dikunci pada kata SEBELUMNYA, bukan pada yang mengikuti: "8 participants" dan
# "3 themes" adalah hitungan dan tetap harus ditandai, padahal dari sisi kanan bentuknya
# identik dengan "type 2 diabetes".
DESIGNATOR_WORDS = (
    # struktur dokumen
    "figure", "figures", "fig", "figs", "table", "tables", "section", "sections", "panel",
    "appendix", "supplement", "supplementary", "reference", "ref", "equation", "eq", "chapter",
    "box", "step", "item", "question", "aim", "objective", "part", "page", "line", "row",
    "column", "note", "phase", "gambar", "tabel", "lampiran", "bagian", "bab", "butir",
    # penanda studi & pengukuran
    "type", "grade", "stage", "class", "level", "group", "arm", "cohort", "visit", "cycle",
    "tier", "category", "version", "model", "site", "center", "centre", "wave", "round",
    "session", "period", "day", "week", "month", "year", "quarter", "semester",
    "factor", "construct", "dimension", "cluster", "condition", "task", "trial", "block",
    "scale", "subscale", "form", "code", "theme", "cohort", "grade", "kelas", "siklus",
    "tahap", "faktor", "kelompok", "sesi", "pertemuan",
)
DESIGNATOR_RE = re.compile(
    r"(?:^|[^\w-])(?:" + "|".join(DESIGNATOR_WORDS) + r")\.?\s*$", re.IGNORECASE)

FLOAT_TITLE_RE = re.compile(r"^\s*\*{0,2}\s*(?:Table|Figure|Tabel|Gambar)\s+\d+", re.IGNORECASE)
COMMA_GROUP_RE = re.compile(r"\b\d{1,3}(?:,\d{3})+\b")
PERIOD_GROUP_RE = re.compile(r"\b\d{1,3}(?:\.\d{3})+\b")

# Cek 9 (tambahan, tidak ada di versi asal). Koma desimal pada angka yang jelas
# BUKAN pemisah ribuan: tepat 1-2 digit di belakang koma. Pemisah ribuan selalu
# tepat 3 digit ("1,200"), jadi pola ini tidak menabraknya.
DECIMAL_COMMA_RE = re.compile(r"(?<![\d,])(\d+),(\d{1,2})(?![\d])")
# Konteks statistik: koma desimal di sini nyaris pasti galat, bukan gaya.
STAT_CONTEXT_RE = re.compile(
    r"\b(?:p|P|r|R|t|F|z|M|SD|CI|alpha|α|β|beta|χ2|chi)\s*[=<>]\s*$")


def baca_baris(path):
    """Kembalikan (daftar_baris, catatan_sumber).

    .md/.txt/.tex dibaca langsung supaya nomor baris tetap cocok dengan berkas sumber
    yang akan disunting penulis. Untuk .tex, komentar dan matematika diganti spasi —
    panjang barisnya dipertahankan agar nomor baris tidak bergeser.
    .docx dan kawan-kawannya lewat pandoc; nomor barisnya milik hasil konversi.
    """
    suffix = path.suffix.lower()
    if suffix in (".md", ".markdown", ".txt"):
        return path.read_text(errors="ignore").splitlines(), "dibaca langsung"
    if suffix == ".tex":
        raw = path.read_text(errors="ignore").splitlines()
        return [_bersihkan_tex(b) for b in raw], "dibaca langsung (komentar & matematika LaTeX diabaikan)"
    try:
        out = subprocess.run(
            ["pandoc", str(path), "-t", "markdown-smart", "--wrap=none"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError:
        sys.exit("Error: pandoc tidak ditemukan. Pasang pandoc lebih dulu, "
                 "atau berikan berkas .md/.tex/.txt.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc gagal membaca {path}\n{e.stderr.strip()}")
    md = re.sub(r"\\([\[\]()*_$<>\"'.,\-~^@%&{}|!?:;+=/])", r"\1", out.stdout)
    return md.splitlines(), "lewat pandoc — NOMOR BARIS milik hasil konversi, bukan berkas sumber"


def _bersihkan_tex(baris):
    """Ganti komentar dan matematika inline dengan spasi, panjang baris dipertahankan."""
    m = re.search(r"(?<!\\)%", baris)
    if m:
        baris = baris[:m.start()] + " " * (len(baris) - m.start())
    baris = re.sub(r"\$[^$]*\$", lambda m: " " * len(m.group(0)), baris)
    baris = re.sub(r"\\(?:cite|ref|label|autoref|cref|eqref|includegraphics|input|usepackage)"
                   r"\w*(?:\[[^\]]*\])?\{[^}]*\}",
                   lambda m: " " * len(m.group(0)), baris)
    return baris


# --------------------------------------------------------------------------- #
# Pemeriksaan (masing-masing mengembalikan list[(baris, pesan)])
# --------------------------------------------------------------------------- #
def cek_akronim(lines):
    out = []
    defs, uses, def_lines = {}, {}, {}
    for i, line in enumerate(lines, 1):
        for m in ABBR_DEF_RE.finditer(line):
            ab = m.group(1)
            defs.setdefault(ab, i)
            def_lines.setdefault(ab, set()).add(i)
    for i, line in enumerate(lines, 1):
        masked = ABBR_DEF_RE.sub(lambda m: " " * len(m.group(0)), line)
        for m in ABBR_USE_RE.finditer(masked):
            uses.setdefault(m.group(1), []).append(i)

    for ab in sorted(set(defs) | set(uses)):
        if ab in ABBR_WHITELIST:
            continue
        u, d = uses.get(ab, []), defs.get(ab)
        if d is None:
            if len(u) >= 2:
                out.append((min(u), f'"{ab}" dipakai {len(u)}x tapi tak pernah didefinisikan'))
            continue
        if len(def_lines.get(ab, set())) > 1:
            out.append((sorted(def_lines[ab])[1], f'"{ab}" didefinisikan lebih dari sekali'))
        before = [ln for ln in u if ln < d]
        if before:
            out.append((min(before), f'"{ab}" dipakai sebelum didefinisikan (definisi di L{d})'))
        if not u:
            out.append((d, f'"{ab}" didefinisikan tapi tak pernah dipakai'))
    return out


def cek_ejaan(lines):
    text = "\n".join(lines)
    us_total = uk_total = 0
    hits = []
    for us_form, uk_re in SPELLING_FAMILIES:
        us_re = SPELLING_US[us_form]
        uk_total += len(re.findall(uk_re, text, re.I))
        us_total += len(re.findall(us_re, text, re.I))
        for i, line in enumerate(lines, 1):
            for _ in re.finditer(uk_re, line, re.I):
                hits.append((i, f'keluarga "{us_form}": ejaan UK di sini', "uk"))
            for _ in re.finditer(us_re, line, re.I):
                hits.append((i, f'keluarga "{us_form}": ejaan US di sini', "us"))
    if us_total == 0 and uk_total == 0:
        return [], None
    dominan = "US" if us_total >= uk_total else "UK"
    minoritas = "uk" if dominan == "US" else "us"
    out = [(ln, f"{msg} (naskah didominasi {dominan})")
           for ln, msg, side in hits if side == minoritas]
    return out, dominan


def cek_rentang_angka(lines):
    return [(i, f'"{m.group(0)}" — pakai en-dash untuk rentang angka ({m.group(1)}–{m.group(2)})')
            for i, line in enumerate(lines, 1) for m in NUM_RANGE_RE.finditer(line)]


def cek_nilai_p(lines):
    kapital = kecil = 0
    hits = []
    for i, line in enumerate(lines, 1):
        for m in PVAL_RE.finditer(line):
            letter = m.group(1)
            if letter == "P":
                kapital += 1
            else:
                kecil += 1
            hits.append((i, letter, m.group(3), m.group(0)))
    if not hits:
        return [], None
    dominan = "P" if kapital >= kecil else "p"
    out = []
    for i, letter, val, raw in hits:
        try:
            num = float(val)
        except ValueError:
            num = None
        if num is not None and num == 0:
            out.append((i, f'"{raw}" — nilai p tidak mungkin tepat 0; laporkan sebagai {letter} < .001'))
        if letter != dominan:
            out.append((i, f'"{raw}" — kapitalisasi tidak konsisten (naskah memakai "{dominan}")'))
    return out, dominan


def cek_tanda_hubung(lines):
    out = []
    for canon, variants in HYPHEN_FAMILIES:
        per_variant = {}
        for vre in variants:
            vlines = [i for i, line in enumerate(lines, 1) if re.search(vre, line, re.I)]
            if vlines:
                per_variant[vre] = vlines
        if len(per_variant) >= 2:
            first = min(min(v) for v in per_variant.values())
            out.append((first, f'bentuk "{canon}" tidak konsisten ({len(per_variant)} varian dipakai)'))
    return out


def cek_angka_kecil(lines):
    out = []
    for i, line in enumerate(lines, 1):
        for m in SMALL_NUM_RE.finditer(line):
            word = m.group(2)
            if word in UNIT_TOKENS:
                continue
            if DESIGNATOR_RE.search(line[: m.start(1)]):
                continue
            out.append((i, f'"{m.group(1)} {word}" — eja angka satu digit di dalam prosa'))
    return out


def cek_satuan(lines):
    return [(i, f'"{m.group(0)}" — beri spasi antara nilai dan satuan ({m.group(1)} {m.group(2)})')
            for i, line in enumerate(lines, 1) for m in UNIT_RE.finditer(line)]


def cek_pemisah_ribuan(lines):
    """Presisi tinggi: hanya menyala bila bilangan YANG SAMA muncul dengan koma di
    badan naskah DAN dengan titik di judul tabel/gambar. Angka desimal tiga digit
    yang sah tidak pernah juga muncul dalam bentuk berkoma."""
    out = []
    comma_vals = {}
    for i, line in enumerate(lines, 1):
        for m in COMMA_GROUP_RE.finditer(line):
            comma_vals.setdefault(m.group(0).replace(",", ""), i)
    if not comma_vals:
        return out
    for i, line in enumerate(lines, 1):
        if not FLOAT_TITLE_RE.match(line):
            continue
        for m in PERIOD_GROUP_RE.finditer(line):
            norm = m.group(0).replace(".", "")
            if norm in comma_vals:
                out.append((i, f'"{m.group(0)}" di judul float memakai titik sebagai pemisah ribuan, '
                               f'sedangkan badan naskah menulisnya "{int(norm):,}" (L{comma_vals[norm]})'))
    return out


def cek_desimal_koma(lines):
    """Koma sebagai pemisah desimal — galat khas penulis Indonesia yang menulis
    naskah berbahasa Inggris. Hanya menyala pada 1-2 digit di belakang koma;
    pemisah ribuan yang sah selalu tepat 3 digit, jadi tidak tertangkap di sini."""
    out = []
    for i, line in enumerate(lines, 1):
        for m in DECIMAL_COMMA_RE.finditer(line):
            konteks = line[max(0, m.start() - 24): m.start()]
            statistik = bool(STAT_CONTEXT_RE.search(konteks))
            catatan = " — konteks statistik, hampir pasti galat" if statistik else ""
            out.append((i, f'"{m.group(0)}" — koma dipakai sebagai pemisah desimal; '
                           f'naskah berbahasa Inggris memakai titik ({m.group(1)}.{m.group(2)}){catatan}'))
    return out


# --------------------------------------------------------------------------- #
# Laporan
# --------------------------------------------------------------------------- #
KATEGORI = [
    ("1. Akronim", "akronim"),
    ("2. Ejaan (konsistensi US/UK)", "ejaan"),
    ("3. Rentang angka", "rentang"),
    ("4. Nilai p", "nilai_p"),
    ("5. Tanda hubung / terminologi", "tanda_hubung"),
    ("6. Angka kecil dalam prosa", "angka_kecil"),
    ("7. Satuan", "satuan"),
    ("8. Pemisah ribuan (judul vs badan)", "pemisah_ribuan"),
    ("9. Desimal koma", "desimal_koma"),
]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Lint mekanis naskah — konvensi yang bisa diperiksa mesin (dimensi 7).")
    ap.add_argument("path", help="Naskah (.tex/.md/.txt/.docx/...)")
    ap.add_argument("--strict", action="store_true", help="exit 1 bila ada temuan")
    ap.add_argument("--json", action="store_true", help="keluarkan JSON mentah")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        sys.exit(f"Error: {path} tidak ditemukan")

    lines, sumber = baca_baris(path)

    ejaan, dominan_ejaan = cek_ejaan(lines)
    nilai_p, dominan_p = cek_nilai_p(lines)
    hasil = {
        "akronim": cek_akronim(lines),
        "ejaan": ejaan,
        "rentang": cek_rentang_angka(lines),
        "nilai_p": nilai_p,
        "tanda_hubung": cek_tanda_hubung(lines),
        "angka_kecil": cek_angka_kecil(lines),
        "satuan": cek_satuan(lines),
        "pemisah_ribuan": cek_pemisah_ribuan(lines),
        "desimal_koma": cek_desimal_koma(lines),
    }
    total = sum(len(v) for v in hasil.values())

    if args.json:
        print(json.dumps({
            "berkas": str(path), "metode_baca": sumber,
            "dialek_dominan": dominan_ejaan, "gaya_p_dominan": dominan_p,
            "total_temuan": total,
            "temuan": {k: [{"baris": ln, "pesan": msg} for ln, msg in sorted(v)]
                       for k, v in hasil.items()},
        }, indent=2, ensure_ascii=False))
    else:
        print(f"\nLINT MEKANIS — {path.name}")
        print("=" * 62)
        print(f"  sumber baris: {sumber}")
        if dominan_ejaan:
            print(f"  dialek dominan: {dominan_ejaan}")
        if dominan_p:
            print(f"  gaya nilai p dominan: \"{dominan_p}\"")
        for judul, key in KATEGORI:
            items = hasil[key]
            print(f"\n{judul}")
            if not items:
                print("  tidak ada temuan")
                continue
            for ln, msg in sorted(items, key=lambda x: (x[0], x[1]))[:20]:
                print(f"  L{ln}: {msg}")
            if len(items) > 20:
                print(f"  ... dan {len(items) - 20} lagi")
        print("\n" + "-" * 62)
        print(f"Total {total} temuan di {sum(1 for v in hasil.values() if v)} kategori.")
        print("Temuan di atas mekanis, bukan penilaian. Konvensi jurnal target menang")
        print("bila berbeda — periksa author guidelines sebelum menerapkan.")

    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    raise SystemExit(main())

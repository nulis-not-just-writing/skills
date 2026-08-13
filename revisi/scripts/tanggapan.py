"""
Alat bantu revisi: memecah surat keputusan menjadi butir, dan memeriksa
kelengkapan surat tanggapan terhadap butir-butir itu.

Pemakaian:
    python tanggapan.py pecah SURAT-KEPUTUSAN.docx [--json]
    python tanggapan.py cek DOCKET.md SURAT-TANGGAPAN.docx [--json]

Menerima .docx / .txt / .md / .pdf / .odt (apa pun yang bisa dibaca pandoc).

`pecah` melaporkan:
  - blok per reviewer/editor yang terdeteksi
  - butir kandidat dengan ID stabil (ED.1, R1.1, R1.2, ...)
  - butir majemuk: satu butir yang tampaknya memuat lebih dari satu permintaan
  - docket markdown siap tempel

`cek` melaporkan:
  - butir yang TIDAK dijawab sama sekali di surat tanggapan  <- penyebab ronde kedua
  - jawaban tanpa penunjuk lokasi perubahan (Section/hal./baris/Tabel)
  - frasa defensif yang berisiko menyinggung reviewer
  - "we thank the reviewer" yang diulang di hampir tiap butir

Script ini MENGHITUNG, tidak memutuskan. Atomisitas butir dan mutu jawaban tetap
penilaian manusia — lihat SKILL.md.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Pembuka blok: siapa yang berbicara. Editor didahulukan karena suratnya
# mengalahkan komentar reviewer (lihat references/membaca-keputusan.md).
BLOCK_PATTERNS = [
    ("ED", r"^\s*(?:comments?\s+(?:from|by|of)\s+the\s+)?"
           r"(?:handling\s+|associate\s+|senior\s+|guest\s+)?editor(?:'s)?"
           r"(?:\s+comments?|\s+in\s+chief)?\s*[:.\-]?\s*$"),
    ("ED", r"^\s*(?:komentar|catatan)\s+editor\s*[:.\-]?\s*$"),
    ("R",  r"^\s*(?:comments?\s+(?:from|by|of)\s+)?"
           r"(?:reviewer|referee|reviewer's|referee's|peninjau|penelaah)\s*"
           r"#?\s*(\d+|one|two|three|four|five|i{1,3}|iv|v)\b.*$"),
]

# Penanda butir bernomor di dalam satu blok.
ITEM_PATTERNS = [
    r"^\s*(?:comment|point|item|butir|komentar)\s*#?\s*(\d+)\s*[:.)\-]\s*",
    r"^\s*(\d{1,2})\s*[.)]\s+",
    r"^\s*[(\[](\d{1,2})[)\]]\s+",
    r"^\s*[-•*–]\s+",
]

# Sub-judul yang memisahkan kelompok butir, bukan butir itu sendiri.
GROUP_RE = re.compile(
    r"^\s*(?:major|minor|general|specific|substantive)\s+"
    r"(?:comments?|points?|issues?|concerns?|revisions?)\s*[:.\-]?\s*$", re.I)

# Sinyal permintaan. Dipakai untuk mendeteksi butir majemuk — satu paragraf
# reviewer sering memuat tiga permintaan sekaligus, dan yang ketiga yang terlupa.
REQUEST_CUES = [
    r"\bshould\b", r"\bmust\b", r"\bplease\b", r"\bneeds?\s+to\b", r"\bought\s+to\b",
    r"\brecommend", r"\bsuggest", r"\bconsider\b", r"\bclarif", r"\bexplain\b",
    r"\bjustif", r"\bprovide\b", r"\breport\b", r"\badd\b", r"\bremove\b",
    r"\brevise\b", r"\brewrite\b", r"\bexpand\b", r"\bshorten\b", r"\bdiscuss\b",
    r"\bunclear\b", r"\bnot\s+clear\b", r"\bmissing\b", r"\black(?:s|ing)?\b",
    r"\bwhy\s+(?:did|do|does|was|were|is|are)\b", r"\bhow\s+(?:did|do|does|was|were)\b",
    r"\bit\s+would\s+be\s+(?:helpful|useful|better)\b", r"\bI\s+(?:would\s+)?encourage\b",
    r"\bharus\b", r"\bsebaiknya\b", r"\bmohon\b", r"\bjelaskan\b", r"\btambahkan\b",
    r"\bperlu\b", r"\bkurang\s+jelas\b", r"\bmengapa\b",
]
REQUEST_RE = re.compile("|".join(REQUEST_CUES), re.I)

# Penunjuk lokasi perubahan. Jawaban tanpa ini memaksa editor mencari sendiri.
LOCATION_RE = re.compile(
    r"\b(?:section|sect\.|sec\.|subsection|page|pages|pp?\.|line|lines|ll?\.|"
    r"paragraph|para\.|table|tables|figure|figures|fig\.|appendix|"
    r"bagian|halaman|hal\.|baris|tabel|gambar|lampiran)\s*"
    r"[\dIVXA-Z]", re.I)

# Frasa yang membuat surat terbaca defensif. Reviewer membacanya lagi.
DEFENSIVE_PATTERNS = [
    ("menyalahkan reviewer",
     r"\bthe\s+reviewer\s+(?:is\s+)?(?:wrong|incorrect|mistaken|"
     r"misunderstood|misunderstands|failed\s+to|clearly\s+did\s+not)\b|"
     r"\breviewer\s+(?:tampaknya\s+)?(?:keliru|salah\s+paham|tidak\s+membaca)\b"),
    ("meremehkan",
     r"\bobviously\b|\bclearly\s+(?:stated|explained|described)\b|"
     r"\bas\s+(?:we\s+)?(?:already|clearly)\s+(?:stated|said|explained|noted)\b|"
     r"\bas\s+any(?:one|body)\s+(?:familiar|working)\b|\bsudah\s+jelas\b"),
    ("menolak mentah",
     r"\bwe\s+(?:strongly\s+)?disagree\b(?![^.]{0,120}\bhowever\b)|"
     r"\bthis\s+is\s+(?:beyond|outside)\s+the\s+scope\b(?![^.]{0,160}"
     r"(?:however|instead|we\s+have|nevertheless))|"
     r"\bwe\s+(?:will\s+not|refuse\s+to|see\s+no\s+reason\s+to)\b"),
    ("mengeluh",
     r"\bunfortunately[,\s]+the\s+reviewer\b|\bthe\s+review\s+process\b|"
     r"\bthe\s+(?:long|lengthy)\s+(?:delay|wait|review)\b"),
    ("janji tanpa perubahan",
     r"\bwe\s+will\s+(?:address|consider|include|do)\s+(?:this|that|it)\s+"
     r"in\s+(?:a\s+)?future\b|\bin\s+our\s+next\s+(?:paper|study)\b"),
]

THANKS_RE = re.compile(
    r"\bwe\s+(?:would\s+like\s+to\s+)?thank\s+the\s+(?:reviewer|referee)|"
    r"\bwe\s+(?:are\s+)?(?:sincerely\s+)?(?:grateful|appreciate)\b|"
    r"\bkami\s+(?:meng)?ucapkan\s+terima\s+kasih\b", re.I)

ID_RE = re.compile(r"\b((?:ED|R\d+)\.\d+[a-z]?)\b")

WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5}


def to_text(path):
    """Baca berkas lewat pandoc; plain agar penomoran asli reviewer tak hilang."""
    if path.suffix.lower() in (".txt", ".md", ".markdown"):
        return path.read_text(encoding="utf-8", errors="replace")
    try:
        out = subprocess.run(
            ["pandoc", str(path), "-t", "plain", "--wrap=none"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError:
        sys.exit("Error: pandoc tidak ditemukan. Pasang pandoc lebih dulu.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc gagal membaca {path}\n{e.stderr.strip()}")
    return out.stdout


def detect_blocks(text):
    """Pecah surat menjadi [(label, judul, isi)] per reviewer/editor.

    Bila tak ada pembuka blok yang dikenali, seluruh surat jadi satu blok R1 —
    lebih baik salah label daripada kehilangan butir.
    """
    lines = text.splitlines()
    marks = []
    for i, line in enumerate(lines):
        if len(line) > 120:                     # baris panjang = prosa, bukan judul
            continue
        for kind, pattern in BLOCK_PATTERNS:
            m = re.match(pattern, line, re.I)
            if not m:
                continue
            num = None
            if kind == "R" and m.groups():
                raw = (m.group(1) or "").lower()
                num = int(raw) if raw.isdigit() else WORD_NUM.get(raw)
            marks.append((i, kind, num, line.strip()))
            break

    if not marks:
        return [("R1", "(tanpa pembuka blok — seluruh surat dianggap satu reviewer)", text)]

    blocks, seen_r = [], 0
    for j, (i, kind, num, title) in enumerate(marks):
        end = marks[j + 1][0] if j + 1 < len(marks) else len(lines)
        if kind == "ED":
            label = "ED"
        else:
            seen_r += 1
            label = f"R{num or seen_r}"
        body = "\n".join(lines[i + 1:end]).strip()
        if body:
            blocks.append((label, title, body))
    return blocks


def split_items(body):
    """Pecah isi blok menjadi butir kandidat.

    Kembalikan [(teks, metode, label_asli)]. `label_asli` adalah penomoran
    reviewer sendiri ("Major 1", "3") — surat tanggapan harus memakai penomoran
    itu agar reviewer mengenali komentarnya, sementara ID internal tetap urut
    supaya tidak bentrok saat penomoran reviewer mengulang di tiap kelompok.

    Prosa sebelum butir bernomor pertama TIDAK boleh dibuang: di situlah
    reviewer menumpuk permintaan tanpa nomor, dan itu yang paling sering
    terlupa dijawab.
    """
    lines = body.splitlines()
    starts, group_lines = [], set()
    group = None
    for i, line in enumerate(lines):
        if GROUP_RE.match(line):
            group_lines.add(i)
            group = re.sub(r"\s*[:.\-]\s*$", "", line.strip()).title()
            continue
        for pattern in ITEM_PATTERNS:
            m = re.match(pattern, line)
            if m:
                num = m.group(1) if m.groups() and m.group(1) else None
                starts.append((i, group, num))
                break

    def strip_groups(chunk_lines):
        return "\n".join(l for k, l in chunk_lines if k not in group_lines).strip()

    if len(starts) > 1:
        items = []
        first = starts[0][0]
        preamble = strip_groups(list(enumerate(lines))[:first])
        if preamble:
            items.append((preamble, "prosa sebelum butir bernomor", "paragraf pembuka"))
        for j, (s, grp, num) in enumerate(starts):
            end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
            chunk = strip_groups(list(enumerate(lines))[s:end])
            if not chunk:
                continue
            label = " ".join(x for x in (grp, num) if x) or "—"
            items.append((chunk, "penomoran reviewer", label))
        return items

    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    paras = [p for p in paras if not GROUP_RE.match(p)]
    return [(p, "paragraf", f"paragraf {n}") for n, p in enumerate(paras, 1)]


def count_requests(text):
    """Berapa kalimat dalam butir ini yang memuat sinyal permintaan."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return sum(1 for s in sentences if REQUEST_RE.search(s))


def clean(text, limit=None):
    out = " ".join(text.split())
    if limit and len(out) > limit:
        out = out[:limit].rstrip() + "…"
    return out


def cmd_pecah(args):
    text = to_text(args.path)
    blocks, out = detect_blocks(text), []
    for label, title, body in blocks:
        items = split_items(body)
        for n, (chunk, method, label_asli) in enumerate(items, 1):
            body_only = re.sub(r"^\s*(?:\d{1,2}\s*[.)]|[(\[]\d{1,2}[)\]]|[-•*–])\s*",
                               "", chunk)
            reqs = count_requests(body_only)
            out.append({
                "id": f"{label}.{n}",
                "nomor_asli": label_asli,
                "blok": title,
                "metode_pecah": method,
                "kutipan": clean(body_only),
                "sinyal_permintaan": reqs,
                "majemuk": reqs >= 2,
                "tanpa_sinyal": reqs == 0,
                "kata": len(body_only.split()),
            })
    return {"berkas": str(args.path),
            "blok_terdeteksi": [{"label": b[0], "judul": clean(b[1], 80)} for b in blocks],
            "butir": out}


def print_pecah(r):
    print(f"\nPEMECAHAN SURAT KEPUTUSAN — {Path(r['berkas']).name}")
    print("=" * 68)
    print("\nBLOK TERDETEKSI")
    for b in r["blok_terdeteksi"]:
        print(f"  [{b['label']:>3}] {b['judul']}")
    if len(r["blok_terdeteksi"]) == 1:
        print("  PERINGATAN: hanya satu blok. Bila surat memuat beberapa reviewer,")
        print("              pembukanya tidak dikenali — pecah manual.")

    items = r["butir"]
    compound = [i for i in items if i["majemuk"]]
    print(f"\n{len(items)} BUTIR KANDIDAT ({len(compound)} perlu diperiksa ulang)")
    for it in items:
        mark = "!" if it["majemuk"] else " "
        print(f"\n {mark} {it['id']}  (nomor reviewer: {it['nomor_asli']})  "
              f"[{it['metode_pecah']}, {it['kata']} kata, "
              f"{it['sinyal_permintaan']} sinyal permintaan]")
        print(f"     {clean(it['kutipan'], 240)}")
        if it["majemuk"]:
            print("     -> PERIKSA: tampaknya memuat lebih dari satu permintaan. "
                  "Pecah jadi a/b/c.")
        if it["tanpa_sinyal"]:
            print("     -> tak ada kata perintah. Bisa jadi pujian — tapi bisa juga "
                  "keluhan yang dinyatakan sebagai pernyataan ('X is not reported'). "
                  "Baca sendiri.")

    print("\n" + "-" * 68)
    print("DOCKET (tempel ke berkas kerja, lalu isi tiga kolom terakhir)\n")
    print("| ID | Nomor reviewer | Kutipan | Jenis | Keputusan | Tindakan & lokasi |")
    print("|---|---|---|---|---|---|")
    for it in items:
        print(f"| {it['id']} | {it['nomor_asli']} | "
              f"{clean(it['kutipan'], 90).replace('|', '/')} |  |  |  |")
    print("\nJenis: mekanis · klarifikasi · analisis tambahan · data baru · "
          "beda pendapat · salah baca · di luar cakupan")
    print("Keputusan: LAKUKAN · SEBAGIAN · TOLAK")
    print("\nButir di atas kandidat, bukan putusan. Baca surat aslinya sendiri —")
    print("reviewer sering menyelipkan permintaan di tengah paragraf pujian.")


def cmd_cek(args):
    docket = to_text(args.docket)
    reply = to_text(args.reply)

    ids = []
    for m in ID_RE.finditer(docket):
        if m.group(1) not in ids:
            ids.append(m.group(1))
    if not ids:
        sys.exit("Error: tidak ada ID butir (ED.1 / R1.2 / ...) di docket. "
                 "Jalankan `pecah` lebih dulu.")

    # Potong surat tanggapan per ID: dari satu ID sampai ID berikutnya.
    hits = [(m.group(1), m.start()) for m in ID_RE.finditer(reply)]
    answers = {}
    for j, (pid, start) in enumerate(hits):
        end = hits[j + 1][1] if j + 1 < len(hits) else len(reply)
        answers.setdefault(pid, "")
        answers[pid] += reply[start:end]

    missing = [i for i in ids if i not in answers]
    thin, no_loc = [], []
    for pid in ids:
        if pid in missing:
            continue
        body = answers[pid]
        if len(body.split()) < 12:
            thin.append({"id": pid, "kata": len(body.split()),
                         "kutipan": clean(body, 120)})
        elif not LOCATION_RE.search(body):
            no_loc.append({"id": pid, "kutipan": clean(body, 140)})

    defensive = []
    for label, pattern in DEFENSIVE_PATTERNS:
        for m in re.finditer(pattern, reply, re.I):
            s = max(0, m.start() - 60)
            defensive.append({"jenis": label, "temuan": clean(m.group(0)),
                              "kutipan": clean(reply[s:m.end() + 60])})

    thanks = len(THANKS_RE.findall(reply))
    return {
        "butir_di_docket": len(ids),
        "butir_dijawab": len(ids) - len(missing),
        "TIDAK_DIJAWAB": missing,
        "jawaban_terlalu_pendek": thin,
        "jawaban_tanpa_lokasi": no_loc,
        "frasa_defensif": defensive,
        "ucapan_terima_kasih": thanks,
        "id_asing_di_surat": [p for p in answers if p not in ids],
    }


def print_cek(r):
    print("\nPEMERIKSAAN SURAT TANGGAPAN")
    print("=" * 68)
    print(f"\n  butir di docket ....... {r['butir_di_docket']}")
    print(f"  butir dijawab ......... {r['butir_dijawab']}")

    if r["TIDAK_DIJAWAB"]:
        print(f"\n  !! {len(r['TIDAK_DIJAWAB'])} BUTIR TIDAK DIJAWAB SAMA SEKALI: "
              + ", ".join(r["TIDAK_DIJAWAB"]))
        print("     Ini penyebab ronde revisi kedua yang paling sering. "
              "Tidak ada butir yang boleh dilewat,")
        print("     termasuk yang Anda tolak — penolakan tetap harus ditulis.")
    else:
        print("\n  semua butir docket punya jawaban")

    if r["id_asing_di_surat"]:
        print(f"\n  ID di surat tapi tak ada di docket: "
              + ", ".join(r["id_asing_di_surat"]) + "  (salah ketik?)")

    if r["jawaban_terlalu_pendek"]:
        print(f"\n  {len(r['jawaban_terlalu_pendek'])} jawaban sangat pendek "
              "(mungkin baru judul, belum isi):")
        for h in r["jawaban_terlalu_pendek"]:
            print(f"    {h['id']} ({h['kata']} kata) — {h['kutipan']}")

    if r["jawaban_tanpa_lokasi"]:
        print(f"\n  {len(r['jawaban_tanpa_lokasi'])} jawaban tanpa penunjuk lokasi "
              "perubahan (Section/hal./baris/Tabel):")
        for h in r["jawaban_tanpa_lokasi"][:12]:
            print(f"    {h['id']} — {h['kutipan']}")
        print("    Editor memverifikasi dengan membuka lokasi yang Anda sebut. "
              "Tanpa itu ia harus mencari sendiri.")

    if r["frasa_defensif"]:
        print(f"\n  {len(r['frasa_defensif'])} frasa berisiko defensif:")
        for h in r["frasa_defensif"][:10]:
            print(f"    [{h['jenis']}] {h['temuan']!r}")
            print(f"        ...{h['kutipan']}...")
        print("    Reviewer membaca surat ini. Ubah jadi pengakuan + koreksi naskah.")

    t = r["ucapan_terima_kasih"]
    if t > 3:
        print(f"\n  ucapan terima kasih: {t} kali — cukup sekali di pembuka.")
        print("    Pujian yang diulang tiap butir memanjangkan surat dan terbaca hampa.")

    print("\n" + "-" * 68)
    print("Script memeriksa kelengkapan, bukan mutu jawaban. Butir yang 'dijawab'")
    print("belum tentu terjawab — baca sendiri butir yang Anda tolak.")


def main():
    p = argparse.ArgumentParser(description="Alat bantu revisi & surat tanggapan")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("pecah", help="Pecah surat keputusan menjadi butir")
    a.add_argument("path", type=Path, help="Surat keputusan (.docx/.txt/.pdf/...)")
    a.add_argument("--json", action="store_true")

    b = sub.add_parser("cek", help="Periksa kelengkapan surat tanggapan")
    b.add_argument("docket", type=Path, help="Docket berisi ID butir")
    b.add_argument("reply", type=Path, help="Surat tanggapan")
    b.add_argument("--json", action="store_true")

    args = p.parse_args()
    for attr in ("path", "docket", "reply"):
        f = getattr(args, attr, None)
        if f is not None and not f.is_file():
            sys.exit(f"Error: {f} tidak ditemukan")

    report = cmd_pecah(args) if args.cmd == "pecah" else cmd_cek(args)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.cmd == "pecah":
        print_pecah(report)
    else:
        print_cek(report)


if __name__ == "__main__":
    main()

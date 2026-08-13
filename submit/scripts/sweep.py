"""
Sapuan mekanis pra-submisi: menghitung hal-hal yang bisa dihitung dari naskah.

Pemakaian:
    python sweep.py NASKAH.docx --authors "Nama A;Nama B" [--bib refs.bib]
                    [--abstract-limit 250] [--word-limit 6000] [--json]

Menerima .docx / .tex / .md / .odt / .rtf (apa pun yang bisa dibaca pandoc).

Yang dilaporkan:
  1. Jumlah kata  - total, badan naskah (tanpa daftar pustaka), abstrak, keywords
  2. Pernyataan wajib - Ethics/IRB, Consent, COI, Funding, Data Availability,
                        Author Contributions, Acknowledgements
  3. Daftar pustaka - jumlah, sebaran tahun, % lima tahun terakhir, rasio sitasi-diri
  4. Sitasi        - silang sitasi dalam teks dengan daftar pustaka (dua arah)
  5. Anonimitas    - nama penulis & frasa pembocor di badan naskah (double-blind)
  6. Figur & tabel - jumlah caption, rujukan dalam teks, rujukan menggantung
  7. Angka abstrak - angka di abstrak yang tidak muncul di badan naskah
  8. Sisa penulisan - TODO/placeholder, tracked changes, komentar & metadata .docx

Script ini MENGHITUNG, tidak memutuskan. Hasilnya bahan mentah untuk gerbang di SKILL.md.
Batas kata/abstrak hanya dibandingkan bila diberikan lewat flag - ambil angkanya dari
author guidelines jurnal target, jangan diasumsikan.
"""

import argparse
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

# Pernyataan wajib. Pola dicari di heading dulu (kuat), lalu di seluruh teks (lemah).
STATEMENTS = [
    ("Ethics / IRB", r"ethic|institutional review board|\bIRB\b|ethical approval|"
                     r"komite etik|persetujuan etik|kelaikan etik|ethical clearance"),
    ("Informed consent", r"informed consent|written consent|persetujuan setelah penjelasan"),
    ("Conflict of Interest", r"conflict of interest|competing interest|"
                             r"declaration of interest|konflik kepentingan"),
    ("Funding", r"\bfunding\b|financial support|funded by|grant number|"
                r"pendanaan|sumber dana|hibah"),
    ("Data Availability", r"data availability|availability of data|data sharing|"
                          r"data can be found|ketersediaan data"),
    ("Author Contributions", r"author contribution|CRediT|authorship contribution|"
                             r"kontribusi penulis"),
    ("Acknowledgements", r"acknowledg|ucapan terima kasih"),
]

# Frasa yang membocorkan identitas pada naskah double-blind.
LEAK_PHRASES = [
    r"\bour (?:previous|earlier|prior|recent) (?:work|study|studies|paper|research)\b",
    r"\bwe (?:have )?(?:previously|earlier) (?:showed|shown|demonstrated|reported|found)\b",
    r"\bas we (?:showed|have shown|reported|demonstrated)\b",
    r"\bin our (?:lab|laboratory|group|institution|university)\b",
    r"penelitian (?:kami|penulis) (?:sebelumnya|terdahulu)",
    r"(?:seperti|sebagaimana) (?:telah )?(?:kami|penulis) (?:tunjukkan|laporkan|teliti)",
]

# Sisa proses penulisan yang lolos ke berkas submisi.
RESIDUE_PATTERNS = [
    ("penanda kerja", r"\b(?:TODO|FIXME|XXX|TBD)\b"),
    ("sitasi placeholder", r"\[\s*(?:cite|citation needed|ref|rujukan|sitasi)\s*\]|"
                           r"\\cite\w*\{\s*\}|\[\s*\?+\s*\]"),
    ("teks contoh", r"lorem ipsum"),
    ("placeholder generik", r"\b(?:PLACEHOLDER|INSERT (?:TEXT|HERE)|"
                            r"isi menyusul|dilengkapi kemudian|akan ditambahkan)\b"),
    ("perintah catatan LaTeX", r"\\(?:todo|note|comment|hl|marginpar)\b"),
]

# Tiga gaya sitasi yang mungkin muncul setelah pandoc: numerik [n], kunci @key
# (hasil konversi \cite{} dari .tex), dan penulis-tahun.
CITE_NUM_RE = re.compile(r"\[([0-9][0-9,;\s\u2013\u2014-]*)\]")
CITE_KEY_RE = re.compile(r"(?<![\w@.])@([A-Za-z][\w:.+-]*[\w])")
CITE_PAREN_RE = re.compile(r"\(([^()]{3,400}?(?:19|20)\d{2}[a-z]?[^()]{0,60})\)")
CITE_NARR_RE = re.compile(
    r"\b([A-Z][\w'\u2019-]+(?:\s+(?:et\s+al\.?|&\s+[A-Z][\w'\u2019-]+|"
    r"and\s+[A-Z][\w'\u2019-]+|dan\s+[A-Z][\w'\u2019-]+))?)\s*\(((?:19|20)\d{2})[a-z]?\)")

NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$", re.M)
REF_HEADING_RE = re.compile(
    r"^(?:references|bibliography|reference list|works cited|"
    r"daftar pustaka|daftar rujukan|kepustakaan)\b", re.I)
ABSTRACT_HEADING_RE = re.compile(r"^(?:abstract|abstrak|summary|ringkasan)\b", re.I)
KEYWORD_RE = re.compile(
    r"^\s*(?:\*\*)?(?:keywords?|kata kunci|key words)(?:\*\*)?\s*[::]\s*(.+)$",
    re.I | re.M)


def to_markdown(path):
    """Baca naskah lewat pandoc; markdown dipilih agar heading tetap terbaca."""
    try:
        out = subprocess.run(
            ["pandoc", str(path), "-t", "markdown-smart", "--wrap=none"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError:
        sys.exit("Error: pandoc tidak ditemukan. Pasang pandoc lebih dulu.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: pandoc gagal membaca {path}\n{e.stderr.strip()}")
    if out.stderr.strip():
        print(f"[pandoc] {out.stderr.strip()}", file=sys.stderr)
    return unescape_md(out.stdout)


def unescape_md(md):
    """Pandoc meng-escape tanda baca ("\\[1\\]"), yang merusak pencocokan pola.
    Kembalikan ke bentuk aslinya - kecuali "#" agar tidak memunculkan heading palsu."""
    return re.sub(r"\\([\[\]()*_$<>\"'.,\-~^@%&{}|!?:;+=/])", r"\1", md)


def split_sections(md):
    """Pecah markdown menjadi [(judul_heading, isi)]. Teks sebelum heading pertama
    diberi judul kosong."""
    matches = list(HEADING_RE.finditer(md))
    if not matches:
        return [("", md)]
    sections = []
    if matches[0].start() > 0:
        sections.append(("", md[:matches[0].start()]))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        sections.append((m.group(2).strip(), md[m.end():end]))
    return sections


def strip_markup(text):
    """Buang sisa markup agar hitungan kata mendekati hitungan editor."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#*_`>|]", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    return text


def count_words(text):
    return len(re.findall(r"\b[\w'-]+\b", strip_markup(text)))


def find_section(sections, pattern_re):
    for title, body in sections:
        if title and pattern_re.match(title):
            return title, body
    return None, None


def check_statements(sections, full_text):
    results = []
    headings = [t for t, _ in sections if t]
    for label, pattern in STATEMENTS:
        rx = re.compile(pattern, re.I)
        in_heading = any(rx.search(h) for h in headings)
        if in_heading:
            results.append({"statement": label, "status": "ada", "where": "heading"})
        elif rx.search(full_text):
            results.append({"statement": label, "status": "disebut",
                            "where": "badan teks, bukan section tersendiri"})
        else:
            results.append({"statement": label, "status": "TIDAK ADA", "where": None})
    return results


def parse_bib(path):
    """Ambil (tahun, teks_entri) dari file .bib."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    entries = []
    for chunk in re.split(r"\n\s*@", "\n" + text)[1:]:
        m = re.search(r"year\s*=\s*[{\"']?\s*(\d{4})", chunk, re.I)
        entries.append(((int(m.group(1)) if m else None), chunk))
    return entries


def parse_reflist(body):
    """Pecah section daftar pustaka menjadi entri. Kembalikan (entri, metode).

    Penanda [n] dicari di mana pun, bukan hanya di awal baris: pandoc menggabungkan
    baris-baris yang berdempetan menjadi satu paragraf, sehingga seluruh daftar
    pustaka bisa berakhir sebagai satu baris panjang.
    """
    body = body.strip()
    if not body:
        return [], "kosong"
    if len(re.findall(r"\[\d+\]", body)) > 1:
        # Teks sebelum penanda pertama (catatan gaya sitasi, judul kolom) bukan
        # entri — kalau ikut terhitung, seluruh penomoran entri bergeser satu.
        parts = re.split(r"(?=\[\d+\])", body)
        if parts and not re.match(r"\s*\[\d+\]", parts[0]):
            parts = parts[1:]
        return [p.strip() for p in parts if p.strip()], "penanda [n]"
    if len(re.findall(r"(?:^|\n)\s*\d+\.\s", body)) > 1:
        parts = re.split(r"\n(?=\s*\d+\.\s)", body)
        return [p.strip() for p in parts if p.strip()], "penanda n."
    parts = re.split(r"\n\s*\n", body)
    if len(parts) > 1:
        return [p.strip() for p in parts if p.strip()], "baris kosong"
    parts = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if len(parts) > 1:
        return parts, "per baris"
    # Satu blok tanpa penanda: pisahkan pada pola "tahun) " / "tahun. " antar entri.
    parts = re.split(r"(?<=\)\.)\s+(?=[A-Z])", body)
    return ([p.strip() for p in parts if p.strip()],
            "heuristik akhir-entri (PERKIRAAN KASAR — verifikasi manual)")


def analyse_refs(entries, surnames, this_year):
    """entries: [(tahun|None, teks)]"""
    years = [y for y, _ in entries if y and 1900 < y <= this_year + 1]
    self_cited = 0
    if surnames:
        for _, txt in entries:
            if any(re.search(rf"\b{re.escape(s)}\b", txt, re.I) for s in surnames):
                self_cited += 1
    recent = [y for y in years if y >= this_year - 5]
    return {
        "jumlah_entri": len(entries),
        "entri_bertahun": len(years),
        "tahun_terlama": min(years) if years else None,
        "tahun_terbaru": max(years) if years else None,
        "median_tahun": sorted(years)[len(years) // 2] if years else None,
        "persen_5_tahun_terakhir": round(100 * len(recent) / len(years), 1) if years else None,
        "sitasi_diri": self_cited,
        "persen_sitasi_diri": round(100 * self_cited / len(entries), 1) if entries else None,
        "sebaran_tahun": dict(sorted(Counter(years).items())) if years else {},
    }


def check_anonymity(body_text, authors):
    """Cari nama penulis dan frasa pembocor di badan naskah (tanpa daftar pustaka)."""
    hits = []
    for author in authors:
        full = author.strip()
        if not full:
            continue
        for m in re.finditer(rf"\b{re.escape(full)}\b", body_text, re.I):
            hits.append({"jenis": "nama penulis", "temuan": full,
                         "kutipan": snippet(body_text, m.start(), m.end())})
        parts = full.split()
        if len(parts) > 1:
            surname = parts[-1]
            if len(surname) > 3:
                for m in re.finditer(rf"\b{re.escape(surname)}\b", body_text):
                    if not any(h["kutipan"] == snippet(body_text, m.start(), m.end())
                               for h in hits):
                        hits.append({"jenis": "nama belakang penulis", "temuan": surname,
                                     "kutipan": snippet(body_text, m.start(), m.end())})
    for pattern in LEAK_PHRASES:
        for m in re.finditer(pattern, body_text, re.I):
            hits.append({"jenis": "frasa pembocor", "temuan": m.group(0),
                         "kutipan": snippet(body_text, m.start(), m.end())})
    return hits


def snippet(text, start, end, pad=45):
    s = text[max(0, start - pad):min(len(text), end + pad)]
    return " ".join(s.split())


def check_floats(md, body_text):
    """Silangkan caption figur/tabel dengan rujukan dalam teks.

    Nomor caption dikumpulkan sebagai HIMPUNAN, bukan dihitung kemunculannya:
    kalimat yang kebetulan dibuka "Table 2 reports..." dan daftar isi tabel di
    akhir naskah sama-sama cocok dengan pola caption, sehingga penghitungan
    kemunculan menggelembung dan memunculkan tabel hantu.

    Pola juga menerima "![Figure 1. ..." — pandoc menaruh caption gambar .docx
    di alt-text, bukan sebagai baris tersendiri.
    """
    fig_cap = re.compile(r"^\s*(?:!\[)?(?:\*\*)?(?:Figure|Fig\.?|Gambar)\s*(\d+)", re.I | re.M)
    tab_cap = re.compile(r"^\s*(?:!\[)?(?:\*\*)?(?:Table|Tabel)\s*(\d+)", re.I | re.M)
    fig_caps = {int(n) for n in fig_cap.findall(md)}
    tab_caps = {int(n) for n in tab_cap.findall(md)}
    captions = {"figur": len(fig_caps), "tabel": len(tab_caps)}
    fig_nums = set(int(n) for n in re.findall(
        r"(?:Figure|Fig\.?|Gambar)\s*(\d+)", body_text, re.I))
    tab_nums = set(int(n) for n in re.findall(
        r"(?:Table|Tabel)\s*(\d+)", body_text, re.I))
    dangling = re.findall(r"(?:Figure|Fig\.?|Table|Gambar|Tabel)\s*\?\?", body_text, re.I)
    dangling += re.findall(r"\\(?:ref|autoref|cref)\{[^}]*\}", body_text)
    # Dirujuk tapi tak punya caption = rujukan ke objek yang tidak ada.
    # Punya caption tapi tak pernah dirujuk = objek yatim. Keduanya temuan editor.
    return {
        "caption_terdeteksi": captions,
        "nomor_figur_caption": sorted(fig_caps),
        "nomor_tabel_caption": sorted(tab_caps),
        "nomor_figur_dirujuk": sorted(fig_nums),
        "nomor_tabel_dirujuk": sorted(tab_nums),
        "figur_dirujuk_tanpa_caption": sorted(fig_nums - fig_caps),
        "tabel_dirujuk_tanpa_caption": sorted(tab_nums - tab_caps),
        "figur_tak_pernah_dirujuk": sorted(fig_caps - fig_nums),
        "tabel_tak_pernah_dirujuk": sorted(tab_caps - tab_nums),
        "rujukan_menggantung": dangling,
    }


def expand_num_citation(inner):
    """"[3, 5-7]" -> [3, 5, 6, 7]. Rentang tak masuk akal dibuang."""
    nums = []
    for part in re.split(r"[,;]", inner):
        part = part.strip()
        m = re.fullmatch(r"(\d+)\s*[–—-]\s*(\d+)", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < a <= b <= a + 200:
                nums.extend(range(a, b + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def collect_author_year(text):
    """Ambil pasangan (nama belakang, tahun) dari sitasi penulis-tahun."""
    pairs = []
    for m in CITE_PAREN_RE.finditer(text):
        for chunk in re.split(r";", m.group(1)):
            c = re.search(r"([A-Z][\w'’-]{2,})[^;]*?((?:19|20)\d{2})", chunk)
            if c:
                pairs.append((c.group(1), c.group(2)))
    for m in CITE_NARR_RE.finditer(text):
        surname = re.match(r"[A-Z][\w'’-]+", m.group(1)).group(0)
        pairs.append((surname, m.group(2)))
    return pairs


def check_citations(body_text, entries, entry_keys):
    """Silangkan sitasi dalam teks dengan daftar pustaka, dua arah.

    Sitasi ke entri yang tidak ada, dan entri yang tak pernah disitir, sama-sama
    terbaca editor sebagai naskah yang tidak diperiksa penulisnya sendiri.
    """
    numeric = [(m.start(), n) for m in CITE_NUM_RE.finditer(body_text)
               for n in expand_num_citation(m.group(1))]
    keys = [m.group(1) for m in CITE_KEY_RE.finditer(body_text)]
    ay = collect_author_year(body_text)

    counts = {"numerik [n]": len(numeric), "kunci @key": len(keys), "penulis-tahun": len(ay)}
    style = max(counts, key=counts.get)
    n_entries = len(entries)
    out = {"gaya_terdeteksi": style if counts[style] else "TIDAK TERDETEKSI",
           "hitung_per_gaya": counts, "jumlah_entri_pustaka": n_entries,
           "sitasi_tanpa_entri": [], "entri_tak_disitir": [],
           "penomoran_berurutan": None, "catatan": None}
    if not counts[style]:
        out["catatan"] = ("tidak ada sitasi terdeteksi — periksa manual; sitasi mungkin "
                          "hilang saat konversi (mis. field code Mendeley/Zotero di .docx)")
        return out

    if style == "numerik [n]":
        cited = sorted({n for _, n in numeric})
        out["jumlah_sitasi"] = len(numeric)
        out["jumlah_unik"] = len(cited)
        if n_entries:
            out["sitasi_tanpa_entri"] = [n for n in cited if n > n_entries]
            out["entri_tak_disitir"] = [n for n in range(1, n_entries + 1) if n not in cited]
        first_order = []
        for _, n in numeric:
            if n not in first_order:
                first_order.append(n)
        out["penomoran_berurutan"] = first_order == sorted(first_order)
        out["urutan_pertama_muncul"] = first_order[:20]
        if n_entries == 0:
            out["catatan"] = "daftar pustaka tak terbaca — silang dua arah dilewati"
    elif style == "kunci @key":
        uniq = sorted(set(keys))
        out["jumlah_sitasi"] = len(keys)
        out["jumlah_unik"] = len(uniq)
        if entry_keys:
            known = set(entry_keys)
            out["sitasi_tanpa_entri"] = [k for k in uniq if k not in known]
            out["entri_tak_disitir"] = sorted(known - set(uniq))
        else:
            out["catatan"] = "kunci sitasi ditemukan tapi tak ada file .bib — jalankan ulang dengan --bib"
    else:
        uniq = sorted(set(ay))
        out["jumlah_sitasi"] = len(ay)
        out["jumlah_unik"] = len(uniq)
        matched = set()
        for surname, year in uniq:
            hit = None
            for i, (_, txt) in enumerate(entries):
                if year in txt and re.search(rf"\b{re.escape(surname)}\b", txt, re.I):
                    hit = i
                    break
            if hit is None:
                out["sitasi_tanpa_entri"].append(f"{surname} ({year})")
            else:
                matched.add(hit)
        out["entri_tak_disitir"] = [
            snippet(entries[i][1], 0, min(70, len(entries[i][1])), pad=0)
            for i in range(n_entries) if i not in matched]
        out["catatan"] = ("pencocokan penulis-tahun bersifat PERKIRAAN — nama dengan ejaan "
                          "berbeda atau et al. tanpa nama pertama bisa salah tanding")
    return out


def check_abstract_numbers(abs_body, body_text):
    """Angka di abstrak yang tidak muncul di badan naskah.

    Editor membaca abstrak lalu melompat ke tabel pertama; angka yang tidak
    bertemu di antara keduanya merusak kredibilitas sebelum reviewer terlibat.
    """
    if not abs_body:
        return None

    def as_float(tok):
        if re.fullmatch(r"\d{1,3},\d{3}", tok):      # pemisah ribuan
            return float(tok.replace(",", ""))
        return float(tok.replace(",", "."))

    body_vals = set()
    for m in NUMBER_RE.finditer(body_text):
        try:
            body_vals.add(as_float(m.group(0)))
        except ValueError:
            continue

    abs_text = strip_markup(abs_body)
    missing, checked = [], 0
    for m in NUMBER_RE.finditer(abs_text):
        tok = m.group(0)
        before = abs_text[max(0, m.start() - 12):m.start()]
        after = abs_text[m.end():m.end() + 2]
        try:
            val = as_float(tok)
        except ValueError:
            continue
        is_year = tok.isdigit() and len(tok) == 4 and 1900 <= val <= 2099
        significant = (not tok.isdigit()) or len(tok) >= 2 or "=" in before or after.startswith("%")
        if is_year or not significant:
            continue
        checked += 1
        # Toleransi pembulatan: 34% di abstrak vs 34,2% di Results tetap dihitung cocok.
        norm = tok.replace(",", "") if re.fullmatch(r"\d{1,3},\d{3}", tok) else tok.replace(",", ".")
        decimals = len(norm.split(".")[1]) if "." in norm else 0
        if any(round(v, decimals) == val for v in body_vals):
            continue
        missing.append({"angka": tok + ("%" if after.startswith("%") else ""),
                        "kutipan": snippet(abs_text, m.start(), m.end())})
    return {"angka_diperiksa": checked, "tidak_ditemukan_di_badan": missing}


def check_residue(md, path):
    """Sisa proses penulisan: penanda kerja, tracked changes, komentar, metadata."""
    hits = []
    for label, pattern in RESIDUE_PATTERNS:
        for m in re.finditer(pattern, md, re.I if label == "teks contoh" else 0):
            hits.append({"jenis": label, "temuan": m.group(0).strip(),
                         "kutipan": snippet(md, m.start(), m.end())})
    return {"temuan": hits, "docx": check_docx_traces(path)}


def check_docx_traces(path):
    """Jejak di dalam .docx yang tak terlihat setelah konversi pandoc."""
    if path.suffix.lower() != ".docx":
        return None
    try:
        with zipfile.ZipFile(path) as z:
            def part(name):
                return z.read(name).decode("utf-8", "replace") if name in z.namelist() else ""
            doc = part("word/document.xml")
            core = part("docProps/core.xml")
            # Template default pandoc menyertakan comments.xml kosong — hitung isinya,
            # bukan keberadaan berkasnya.
            comments = len(re.findall(r"<w:comment[ >]", part("word/comments.xml")))
    except (zipfile.BadZipFile, KeyError, OSError) as e:
        return {"error": str(e)}

    def tag(name):
        m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", core, re.S)
        return m.group(1).strip() if m else None

    return {
        "tracked_changes": len(re.findall(r"<w:(?:ins|del)\b", doc)),
        "komentar": comments,
        "teks_disorot": len(re.findall(r"<w:highlight\b", doc)),
        "metadata_creator": tag("dc:creator"),
        "metadata_last_modified_by": tag("cp:lastModifiedBy"),
    }


def build_report(args):
    md = to_markdown(args.path)
    sections = split_sections(md)
    this_year = datetime.now().year

    _, ref_body = find_section(sections, REF_HEADING_RE)
    _, abs_body = find_section(sections, ABSTRACT_HEADING_RE)

    body_md = "".join(
        b for t, b in sections
        if not (t and REF_HEADING_RE.match(t))
    )
    body_text = strip_markup(body_md)
    # Abstrak ikut dibuang agar angkanya tidak mencocoki dirinya sendiri.
    body_no_abs = strip_markup("".join(
        b for t, b in sections
        if not (t and (REF_HEADING_RE.match(t) or ABSTRACT_HEADING_RE.match(t)))
    ))

    kw = KEYWORD_RE.search(md)
    keywords = [k.strip() for k in re.split(r"[;,]", kw.group(1)) if k.strip()] if kw else []

    authors = [a.strip() for a in args.authors.split(";") if a.strip()] if args.authors else []
    surnames = [a.split()[-1] for a in authors if a.split()]

    entry_keys = []
    if args.bib:
        entries = parse_bib(args.bib)
        ref_method = f"file .bib ({Path(args.bib).name})"
        entry_keys = [m.group(1) for _, chunk in entries
                      if (m := re.match(r"\w+\s*\{\s*([^,\s]+)", chunk))]
    elif ref_body is not None:
        raw, ref_method = parse_reflist(ref_body)
        entries = []
        for e in raw:
            m = re.search(r"\b((?:19|20)\d{2})\b", e)
            entries.append(((int(m.group(1)) if m else None), e))
    else:
        entries, ref_method = [], "TIDAK DITEMUKAN"

    report = {
        "berkas": str(args.path),
        "jumlah_kata": {
            "total": count_words(md),
            "tanpa_daftar_pustaka": count_words(body_md),
            "abstrak": count_words(abs_body) if abs_body else None,
            "keywords": len(keywords),
        },
        "batas": {
            "kata": args.word_limit,
            "abstrak": args.abstract_limit,
        },
        "heading_terdeteksi": [t for t, _ in sections if t],
        "pernyataan_wajib": check_statements(sections, md),
        "daftar_pustaka": {"metode_baca": ref_method,
                           **analyse_refs(entries, surnames, this_year)},
        "sitasi": check_citations(body_text, entries, entry_keys),
        "anonimitas": check_anonymity(body_text, authors) if authors else None,
        "figur_tabel": check_floats(md, body_text),
        "angka_abstrak": check_abstract_numbers(abs_body, body_no_abs),
        "residu": check_residue(md, args.path),
    }
    return report


def print_citations(c, line):
    """Bagian 4 — silang sitasi dengan daftar pustaka."""
    print("\n4. SITASI <-> DAFTAR PUSTAKA")
    line("gaya sitasi terdeteksi", c["gaya_terdeteksi"])
    if "jumlah_sitasi" in c:
        line("sitasi dalam teks", f"{c['jumlah_sitasi']} ({c['jumlah_unik']} unik)")
    line("entri daftar pustaka", c["jumlah_entri_pustaka"])
    if c["sitasi_tanpa_entri"]:
        line("DISITIR TAPI TAK ADA DI PUSTAKA",
             ", ".join(str(x) for x in c["sitasi_tanpa_entri"][:20]))
    if c["entri_tak_disitir"]:
        vals = c["entri_tak_disitir"]
        line("entri tak pernah disitir", f"{len(vals)} entri")
        for v in vals[:10]:
            print(f"      - {v}")
        if len(vals) > 10:
            print(f"      ... dan {len(vals) - 10} lagi")
    if not c["sitasi_tanpa_entri"] and not c["entri_tak_disitir"] and "jumlah_sitasi" in c:
        print("  kedua arah cocok — tidak ada sitasi yatim maupun entri yatim")
    if c["penomoran_berurutan"] is False:
        line("PENOMORAN TIDAK BERURUTAN",
             " ".join(f"[{n}]" for n in c.get("urutan_pertama_muncul", [])))
        print("      (banyak guidelines menuntut nomor sitasi urut sesuai penyebutan pertama)")
    if c["catatan"]:
        print(f"  CATATAN: {c['catatan']}")


def print_abstract_numbers(a, line):
    """Bagian 7 — angka abstrak yang tak bertemu di badan naskah."""
    print("\n7. ANGKA ABSTRAK <-> BADAN NASKAH")
    if a is None:
        print("  dilewati — section abstrak tidak ditemukan")
        return
    line("angka diperiksa", a["angka_diperiksa"])
    if not a["tidak_ditemukan_di_badan"]:
        print("  semua angka abstrak punya pasangan di badan naskah")
        return
    print(f"  {len(a['tidak_ditemukan_di_badan'])} angka tidak ditemukan di badan naskah:")
    for h in a["tidak_ditemukan_di_badan"][:12]:
        print(f"    {h['angka']!r} — ...{h['kutipan']}...")
    print("  CATATAN: pembulatan & satuan berbeda bisa memicu alarm palsu — verifikasi manual.")


def print_residue(res, line):
    """Bagian 8 — sisa proses penulisan."""
    print("\n8. SISA PROSES PENULISAN")
    hits = res["temuan"]
    if not hits:
        print("  tidak ada penanda kerja/placeholder terdeteksi")
    else:
        print(f"  {len(hits)} penanda tersisa:")
        for h in hits[:12]:
            print(f"    [{h['jenis']}] {h['temuan']!r}")
            print(f"        ...{h['kutipan']}...")
        if len(hits) > 12:
            print(f"    ... dan {len(hits) - 12} lagi")
    d = res["docx"]
    if d is None:
        print("  (jejak .docx tidak diperiksa — berkas bukan .docx)")
        return
    if "error" in d:
        print(f"  .docx tidak bisa dibuka: {d['error']}")
        return
    line("tracked changes", d["tracked_changes"] or "tidak ada")
    line("komentar tertinggal", d["komentar"] or "tidak ada")
    line("teks disorot (highlight)", d["teks_disorot"] or "tidak ada")
    line("metadata dc:creator", d["metadata_creator"] or "kosong")
    line("metadata lastModifiedBy", d["metadata_last_modified_by"] or "kosong")
    if d["metadata_creator"] or d["metadata_last_modified_by"]:
        print("      (bersihkan sebelum unggah pada submisi double-blind)")


def print_report(r):
    def line(label, value):
        print(f"  {label:.<38} {value}")

    print(f"\nSAPUAN MEKANIS — {Path(r['berkas']).name}")
    print("=" * 62)

    print("\n1. JUMLAH KATA")
    wc, lim = r["jumlah_kata"], r["batas"]
    line("total", wc["total"])
    line("tanpa daftar pustaka", wc["tanpa_daftar_pustaka"])
    if lim["kata"]:
        over = wc["tanpa_daftar_pustaka"] - lim["kata"]
        line("batas jurnal", f"{lim['kata']} -> "
             + (f"LEBIH {over} kata" if over > 0 else f"aman ({-over} sisa)"))
    if wc["abstrak"] is None:
        line("abstrak", "SECTION ABSTRAK TIDAK DITEMUKAN")
    else:
        line("abstrak", wc["abstrak"])
        if lim["abstrak"]:
            over = wc["abstrak"] - lim["abstrak"]
            line("batas abstrak", f"{lim['abstrak']} -> "
                 + (f"LEBIH {over} kata" if over > 0 else "aman"))
    line("keywords", wc["keywords"] or "TIDAK DITEMUKAN")

    print("\n2. PERNYATAAN WAJIB")
    for s in r["pernyataan_wajib"]:
        mark = {"ada": "OK  ", "disebut": "?   ", "TIDAK ADA": "HILANG"}[s["status"]]
        suffix = f"  ({s['where']})" if s["where"] and s["status"] != "ada" else ""
        print(f"  [{mark}] {s['statement']}{suffix}")

    print("\n3. DAFTAR PUSTAKA")
    d = r["daftar_pustaka"]
    line("metode baca", d["metode_baca"])
    line("jumlah entri", d["jumlah_entri"])
    if d["entri_bertahun"]:
        line("rentang tahun", f"{d['tahun_terlama']}–{d['tahun_terbaru']} "
                              f"(median {d['median_tahun']})")
        line("terbit 5 tahun terakhir", f"{d['persen_5_tahun_terakhir']}%")
    if d["persen_sitasi_diri"] is not None:
        flag = "  <-- TINGGI" if d["persen_sitasi_diri"] > 20 else ""
        line("sitasi diri", f"{d['sitasi_diri']} entri "
                            f"({d['persen_sitasi_diri']}%){flag}")

    print_citations(r["sitasi"], line)

    print("\n5. ANONIMITAS (double-blind)")
    a = r["anonimitas"]
    if a is None:
        print("  dilewati — nama penulis tidak diberikan (--authors)")
    elif not a:
        print("  tidak ada kebocoran terdeteksi di badan naskah")
    else:
        print(f"  {len(a)} kebocoran terdeteksi:")
        for h in a[:15]:
            print(f"    [{h['jenis']}] {h['temuan']!r}")
            print(f"        ...{h['kutipan']}...")
        if len(a) > 15:
            print(f"    ... dan {len(a) - 15} lagi")
        print("  CATATAN: metadata file, acknowledgements, dan teks di dalam gambar")
        print("           tidak terdeteksi script — periksa manual.")

    print("\n6. FIGUR & TABEL")
    f = r["figur_tabel"]
    line("caption figur", f["caption_terdeteksi"]["figur"])
    line("caption tabel", f["caption_terdeteksi"]["tabel"])
    line("nomor figur dirujuk di teks", f["nomor_figur_dirujuk"] or "tidak ada")
    line("nomor tabel dirujuk di teks", f["nomor_tabel_dirujuk"] or "tidak ada")
    for key, label in (
        ("figur_dirujuk_tanpa_caption", "FIGUR DIRUJUK TAPI TAK ADA"),
        ("tabel_dirujuk_tanpa_caption", "TABEL DIRUJUK TAPI TAK ADA"),
        ("figur_tak_pernah_dirujuk", "figur tak pernah dirujuk di teks"),
        ("tabel_tak_pernah_dirujuk", "tabel tak pernah dirujuk di teks"),
    ):
        if f[key]:
            line(label, ", ".join(str(n) for n in f[key]))
    if f["rujukan_menggantung"]:
        line("RUJUKAN MENGGANTUNG", ", ".join(sorted(set(f["rujukan_menggantung"]))))

    print_abstract_numbers(r["angka_abstrak"], line)
    print_residue(r["residu"], line)

    print("\n" + "-" * 62)
    print("Angka di atas bahan mentah. Bandingkan dengan author guidelines jurnal")
    print("target, lalu jalankan gerbang G1–G5 dan Tahap 2–3 di SKILL.md.")


def main():
    p = argparse.ArgumentParser(
        description="Sapuan mekanis pra-submisi untuk risiko desk rejection")
    p.add_argument("path", help="Naskah (.docx/.tex/.md/...)")
    p.add_argument("--authors", help='Nama penulis dipisah ";" — untuk sitasi-diri & anonimitas')
    p.add_argument("--bib", help="File .bib (lebih akurat daripada membaca daftar pustaka)")
    p.add_argument("--word-limit", type=int, help="Batas kata dari author guidelines")
    p.add_argument("--abstract-limit", type=int, help="Batas kata abstrak dari author guidelines")
    p.add_argument("--json", action="store_true", help="Keluarkan JSON mentah")
    args = p.parse_args()

    path = Path(args.path)
    if not path.is_file():
        sys.exit(f"Error: {path} tidak ditemukan")
    args.path = path

    report = build_report(args)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()

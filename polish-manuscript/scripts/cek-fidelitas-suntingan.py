#!/usr/bin/env python3
"""
Batasi seberapa banyak naskah boleh berubah oleh satu sapuan penyuntingan.

Diadaptasi dari check_rewrite_fidelity.py milik medsci-skills (MIT, Aperivue).
Lihat NOTICE.md di akar repo. Perubahan: keluaran bahasa Indonesia, dukungan .tex,
pengenalan sitasi LaTeX (\\cite{...}) di samping gaya pandoc.

MENGAPA INI ADA
SKILL.md polish-manuscript menyatakan dua janji yang selama ini tidak ada yang
menegakkan: "pertahankan suara penulis" dan "JANGAN mengubah angka sendiri, laporkan
untuk dikonfirmasi penulis". Penyuntingan anti-AI bersifat mengurangi: buang penandanya,
pertahankan kalimat penulisnya. Tapi model yang diminta "buat ini terdengar manusiawi"
juga akan menulis ulang paragraf yang sebenarnya tidak bermasalah, dan hasilnya cukup
lancar sehingga kehilangannya tak terlihat saat ditinjau — suara penulis lenyap dan tak
seorang pun bisa menunjuk kalimat tempat ia hilang.

Penyuntingan pola-demi-pola menyentuh sebagian kecil kata; penulisan ulang menyeluruh
menyentuh sebagian besar. Selisih itu bisa diukur, jadi skrip ini mengukurnya alih-alih
memercayai bahwa penyuntingannya sudah menahan diri.

Vonis:
  ANGKA_BERGESER   (Mayor) jumlah kemunculan sebuah token angka berubah.
  SITASI_HILANG    (Mayor) sitasi yang ada sebelum penyuntingan tidak ada sesudahnya.
  JEJAK_SUNTING_BESAR (Minor) lebih dari --warn-pct kata berubah — baca ulang diff-nya.

MENGAPA DUA YANG PERTAMA MENGIKAT DAN YANG KETIGA TIDAK
Dua yang pertama adalah janji eksplisit SKILL.md, jadi pelanggarannya tak ambigu.
Persentase jejak tidak punya dasar sekuat itu. Diukur pada fixture versi asal, sapuan
anti-AI yang BENAR pada satu Discussion yang menggelembung mengubah 61% token kata —
karena mengganti paragraf limitasi dan simpulan yang formulaik memang menulis ulang
paragraf utuh. Ambang keras akan menggagalkan justru penyuntingan yang diminta. Jadi
persentasenya dilaporkan supaya manusia bisa menyadari angka yang janggal; ia bukan
bukti penyuntingan berlebihan dengan sendirinya, dan defaultnya sengaja longgar.

Dibatasi agar positif palsunya rendah:
  * Perbandingan pada token KATA, bukan karakter — perbaikan tanda baca saja
    (em-dash -> kurung, curly quote -> lurus) nyaris tidak menggerakkan angkanya.
  * Penanda sitasi dibuang sebelum ekstraksi angka, jadi nomor rujukan diperiksa
    sekali sebagai sitasi dan tidak lagi sebagai angka.
  * Blok kode dikecualikan dari kedua sisi.

Pemakaian:
    python cek-fidelitas-suntingan.py --sebelum asli.tex --sesudah hasil.tex
    python cek-fidelitas-suntingan.py --sebelum a.md --sesudah b.md --strict
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

FENCE_RE = re.compile(r"```.*?```", re.S)
VERBATIM_RE = re.compile(r"\\begin\{(lstlisting|verbatim)\*?\}.*?\\end\{\1\*?\}", re.S)
# Kunci sitasi pandoc, penanda numerik, dan \cite{...} LaTeX (termasuk varian natbib).
CITEKEY_RE = re.compile(r"\[@[^\]\s]+\]")
NUMMARK_RE = re.compile(r"\[\d+(?:\s*[-–,]\s*\d+)*\]")
TEXCITE_RE = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")
WORD_RE = re.compile(r"[A-Za-z0-9''-]+")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def _buang_kode(teks: str) -> str:
    return VERBATIM_RE.sub(" ", FENCE_RE.sub(" ", teks))


def _sitasi(teks: str) -> Counter:
    kunci = CITEKEY_RE.findall(teks)
    tanda = NUMMARK_RE.findall(teks)
    # \cite{a,b} dihitung sebagai dua sitasi terpisah, supaya menghapus satu kunci
    # dari dalam kurung kurawal tetap tertangkap.
    tex = [k.strip() for grup in TEXCITE_RE.findall(teks) for k in grup.split(",") if k.strip()]
    return Counter([k.strip() for k in kunci + tanda] + [f"cite:{k}" for k in tex])


def _angka(teks: str) -> Counter:
    """Token angka setelah penanda sitasi dibuang, supaya nomor rujukan tidak
    terhitung dua kali sebagai statistik."""
    tanpa_sitasi = TEXCITE_RE.sub(" ", NUMMARK_RE.sub(" ", CITEKEY_RE.sub(" ", teks)))
    return Counter(NUMBER_RE.findall(tanpa_sitasi.replace(",", "")))


def _kata(teks: str) -> list[str]:
    return WORD_RE.findall(teks.lower())


def _fraksi_berubah(sebelum: list[str], sesudah: list[str]) -> float:
    """Fraksi token kata yang berbeda, diukur terhadap sisi yang lebih panjang supaya
    penyuntingan tidak bisa menurunkan skornya dengan cara menghapus teks."""
    if not sebelum and not sesudah:
        return 0.0
    matcher = difflib.SequenceMatcher(a=sebelum, b=sesudah, autojunk=False)
    cocok = sum(blok.size for blok in matcher.get_matching_blocks())
    penyebut = max(len(sebelum), len(sesudah))
    return 1.0 - (cocok / penyebut) if penyebut else 0.0


def _selisih(sebelum: Counter, sesudah: Counter) -> list[dict]:
    out = []
    for token in sorted(set(sebelum) | set(sesudah)):
        b, a = sebelum.get(token, 0), sesudah.get(token, 0)
        if b != a:
            out.append({"token": token, "sebelum": b, "sesudah": a})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Batasi seberapa banyak naskah boleh berubah oleh satu sapuan penyuntingan.")
    ap.add_argument("--sebelum", required=True, type=Path, help="naskah sebelum disunting")
    ap.add_argument("--sesudah", required=True, type=Path, help="naskah sesudah disunting")
    ap.add_argument("--out", type=Path, help="tulis JSON ke berkas ini")
    ap.add_argument("--warn-pct", type=float, default=70.0,
                    help="Minor bila lebih dari sekian %% kata berubah (default 70; lihat docstring)")
    ap.add_argument("--json", action="store_true", help="cetak JSON ke stdout")
    ap.add_argument("--strict", action="store_true", help="exit 1 bila ada vonis Mayor")
    args = ap.parse_args(argv)

    for p in (args.sebelum, args.sesudah):
        if not p.is_file():
            sys.exit(f"Error: {p} tidak ditemukan")

    a_raw = _buang_kode(args.sebelum.read_text(encoding="utf-8", errors="ignore"))
    b_raw = _buang_kode(args.sesudah.read_text(encoding="utf-8", errors="ignore"))

    berubah_pct = round(_fraksi_berubah(_kata(a_raw), _kata(b_raw)) * 100, 1)
    selisih_angka = _selisih(_angka(a_raw), _angka(b_raw))
    selisih_sitasi = _selisih(_sitasi(a_raw), _sitasi(b_raw))

    vonis: list[dict] = []
    if berubah_pct > args.warn_pct:
        vonis.append({
            "vonis": "JEJAK_SUNTING_BESAR", "tingkat": "Minor",
            "berubah_pct": berubah_pct, "ambang_pct": args.warn_pct,
            "pesan": (f"{berubah_pct}% token kata berubah (ambang penasihat {args.warn_pct}%). "
                      "Sapuan anti-AI yang menyeluruh bisa sah mencapai angka ini ketika paragraf "
                      "limitasi atau simpulan yang formulaik memang harus diganti; baca ulang diff-nya "
                      "dan pastikan argumen penulis — bukan sekadar pilihan katanya — selamat."),
        })
    if selisih_angka:
        vonis.append({
            "vonis": "ANGKA_BERGESER", "tingkat": "Mayor", "token": selisih_angka[:40],
            "pesan": (f"{len(selisih_angka)} token angka berubah jumlah kemunculannya. "
                      "Penyuntingan tidak boleh pernah mengubah angka — laporkan ke penulis, "
                      "jangan perbaiki sendiri."),
        })
    if selisih_sitasi:
        vonis.append({
            "vonis": "SITASI_HILANG", "tingkat": "Mayor", "token": selisih_sitasi[:40],
            "pesan": (f"{len(selisih_sitasi)} sitasi berubah jumlah kemunculannya. "
                      "Penyuntingan tidak boleh menghapus atau memindahkan sitasi."),
        })

    amplop = {"pemeriksa": "cek-fidelitas-suntingan",
              "sebelum": str(args.sebelum), "sesudah": str(args.sesudah),
              "berubah_pct": berubah_pct,
              "kata_sebelum": len(_kata(a_raw)), "kata_sesudah": len(_kata(b_raw)),
              "vonis": vonis}

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(amplop, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.json:
        print(json.dumps(amplop, indent=2, ensure_ascii=False))
    else:
        print(f"\nFIDELITAS SUNTINGAN — {args.sebelum.name} -> {args.sesudah.name}")
        print("=" * 62)
        print(f"  {berubah_pct}% kata berubah ({len(_kata(a_raw))} -> {len(_kata(b_raw))} kata)")
        for v in vonis:
            print(f"\n  [{v['tingkat']}] {v['vonis']}")
            print(f"    {v['pesan']}")
            for t in v.get("token", [])[:10]:
                print(f"      {t['token']!r}: {t['sebelum']}x -> {t['sesudah']}x")
        if not vonis:
            print("\n  bersih: jejak dalam batas, angka dan sitasi utuh")

    if args.strict and any(v["tingkat"] == "Mayor" for v in vonis):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

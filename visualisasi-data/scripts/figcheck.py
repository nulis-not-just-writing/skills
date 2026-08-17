#!/usr/bin/env python3
"""figcheck.py — QA mekanis figur sebelum disisipkan ke naskah.

    python figcheck.py figures/fig2.png --kolom single
    python figcheck.py figures/*.png --kolom double --json

Yang diperiksa (yang bisa dihitung; sisanya butuh mata — lihat aturan 9.2):
  1. DPI tertanam dan resolusi piksel efektif pada lebar kolom target
  2. Lebar fisik terhadap lebar kolom jurnal
  3. Keberadaan pasangan vektor (.pdf/.eps/.svg) untuk setiap raster
  4. Rasio aspek yang ekstrem (figur pipih sulit dibaca setelah diperkecil)
  5. Ruang kosong tepi berlebih (figur tidak "mengisi kotaknya", aturan 3.5)
  6. Font tertanam pada PDF (Type 42, bukan kurva) bila pypdf tersedia

Skrip ini TIDAK dapat menilai fidelitas data, kalibrasi klaim, atau
keterbacaan warna. Itu tugas manusia dan agen yang membaca aturan-figur.md.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

MM = 25.4
KOLOM = {"single": 85.0, "double": 180.0}      # mm, default lazim penerbit
DPI_MIN = 300
DPI_MIN_LINEART = 600                          # garis murni: banyak jurnal minta 600/1200


def _cek_raster(path, lebar_mm, dpi_min):
    temuan, info = [], {}
    try:
        from PIL import Image
    except ImportError:
        return ["Pillow tidak terpasang — pemeriksaan raster dilewati"], info
    with Image.open(path) as im:
        w, h = im.size
        dpi = im.info.get("dpi", (None, None))[0]
    info.update(piksel=[w, h], dpi_tertanam=dpi)
    dpi_efektif = w / (lebar_mm / MM)
    info["dpi_pada_lebar_kolom"] = round(dpi_efektif, 1)
    # toleransi 3%: bbox_inches="tight" memangkas beberapa piksel tepi
    if dpi_efektif < dpi_min * 0.97:
        temuan.append(f"resolusi {dpi_efektif:.0f} dpi pada lebar {lebar_mm:.0f} mm "
                      f"(< {dpi_min}); render ulang lebih besar, jangan diperbesar")
    if dpi and abs(dpi - dpi_efektif) / max(dpi, 1) > 0.12:
        arah = "lebih kecil" if dpi_efektif < dpi else "lebih besar"
        temuan.append(f"figur digambar untuk lebar lain: dpi tertanam {dpi:.0f} vs "
                      f"{dpi_efektif:.0f} dpi pada {lebar_mm:.0f} mm — penerbit akan "
                      f"menskalanya {arah}, dan ukuran font ikut berubah")
    ar = h / w
    info["rasio_tinggi_lebar"] = round(ar, 3)
    if ar < 0.25:
        temuan.append(f"rasio {ar:.2f} sangat pipih; panel akan sulit dibaca")
    if ar > 2.2:
        temuan.append(f"rasio {ar:.2f} sangat jangkung; pertimbangkan tata ulang panel")
    return temuan, info


def _cek_margin(path, ambang=0.06):
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return []
    with Image.open(path) as im:
        a = np.asarray(im.convert("L"))
    isi = a < 250
    if not isi.any():
        return ["citra tampak kosong"]
    ys, xs = np.where(isi)
    h, w = a.shape
    m = [xs.min() / w, (w - 1 - xs.max()) / w, ys.min() / h, (h - 1 - ys.max()) / h]
    nama = ["kiri", "kanan", "atas", "bawah"]
    besar = [f"{n} {v*100:.0f}%" for n, v in zip(nama, m) if v > ambang]
    if besar:
        return [f"ruang kosong tepi berlebih ({', '.join(besar)}) — "
                f"data tidak mengisi kotaknya (aturan 3.5)"]
    return []


def _cek_vektor(path):
    stem = os.path.splitext(path)[0]
    for ext in (".pdf", ".eps", ".svg"):
        if os.path.exists(stem + ext):
            return [], stem + ext
    return ["tidak ada pasangan vektor (.pdf/.eps/.svg); banyak jurnal "
            "mensyaratkan vektor untuk figur line-art"], None


def _cek_font_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return []
    try:
        rd = PdfReader(path)
        page = rd.pages[0]
        fonts = page.get("/Resources", {}).get("/Font", {})
        if not fonts:
            return ["PDF tidak memuat font — teks kemungkinan dikonversi jadi "
                    "kurva; set rcParams['pdf.fonttype']=42 agar teks tetap teks"]
    except Exception as e:                       # noqa: BLE001
        return [f"PDF tidak terbaca ({e})"]
    return []


def periksa(path, kolom="single", lebar_mm=None, dpi_min=DPI_MIN):
    lebar = lebar_mm if lebar_mm else KOLOM.get(kolom, KOLOM["single"])
    hasil = {"file": path, "lebar_kolom_mm": lebar, "temuan": [], "info": {}}
    if not os.path.exists(path):
        hasil["temuan"].append("file tidak ditemukan")
        return hasil
    ext = os.path.splitext(path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg", ".tif", ".tiff"):
        t, i = _cek_raster(path, lebar, dpi_min)
        hasil["temuan"] += t
        hasil["info"].update(i)
        hasil["temuan"] += _cek_margin(path)
        tv, v = _cek_vektor(path)
        hasil["temuan"] += tv
        if v:
            hasil["info"]["vektor"] = v
            if v.endswith(".pdf"):
                hasil["temuan"] += _cek_font_pdf(v)
    elif ext == ".pdf":
        hasil["temuan"] += _cek_font_pdf(path)
        hasil["info"]["catatan"] = "PDF vektor: resolusi tidak relevan"
    else:
        hasil["temuan"].append(f"format {ext} tidak diperiksa")
    return hasil


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--kolom", choices=list(KOLOM), default="single",
                    help="lebar kolom jurnal target (default: single/85 mm)")
    ap.add_argument("--lebar-mm", type=float, default=None,
                    help="lebar eksplisit dari author guidelines, menimpa --kolom")
    ap.add_argument("--dpi-min", type=int, default=DPI_MIN)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    out = [periksa(f, a.kolom, a.lebar_mm, a.dpi_min) for f in a.files]
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        for h in out:
            print(f"\n=== {h['file']}  (target {h['lebar_kolom_mm']:.0f} mm)")
            for k, v in h["info"].items():
                print(f"    {k}: {v}")
            if h["temuan"]:
                for t in h["temuan"]:
                    print(f"  ! {t}")
            else:
                print("  lolos pemeriksaan mekanis")
        print("\nPemeriksaan mekanis tidak menilai fidelitas data, kalibrasi "
              "klaim, atau keterbacaan warna — lihat gambarnya (aturan 9.2).")
    return 1 if any(h["temuan"] for h in out) else 0


if __name__ == "__main__":
    sys.exit(main())

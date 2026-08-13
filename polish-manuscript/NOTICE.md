# NOTICE — karya pihak ketiga di dalam skill `polish-manuscript`

Skill ini memuat karya turunan dari pihak ketiga. Pemberitahuan di bawah wajib ikut pada setiap
salinan dan distribusi ulang.

## Diadaptasi — MIT

- Sumber: `Aperivue/medsci-skills` — https://github.com/Aperivue/medsci-skills
- Pemegang hak: Aperivue (https://aperivue.com), 2026
- Lisensi: **MIT**

| Berkas di sini | Asal di repo hulu | Perubahan |
|---|---|---|
| `scripts/lint-mekanis.py` | `skills/polish-language/scripts/lint_consistency.py` | keluaran bahasa Indonesia; membaca `.tex` langsung (nomor baris tetap cocok dengan sumber) dan `.docx` lewat pandoc; kosakata medis diganti kosakata lintas bidang; **cek baru** untuk desimal koma — galat khas penulis Indonesia yang menulis naskah berbahasa Inggris |
| `scripts/cek-variasi-kalimat.py` | `skills/humanize/scripts/check_sentence_variety.py` | keluaran bahasa Indonesia; dukungan `.tex`; singkatan Indonesia (dkk., dll., hlm.) ditambahkan ke pemecah kalimat |
| `scripts/cek-fidelitas-suntingan.py` | `skills/humanize/scripts/check_rewrite_fidelity.py` | keluaran bahasa Indonesia; mengenali `\cite{...}` LaTeX termasuk kunci majemuk `\cite{a,b}`, yang tidak dilihat versi hulu |

Ketiganya **stdlib-only** (satu impor `python-docx` bersifat lazy, hanya saat membaca `.docx`).

## Ambang yang diwarisi belum divalidasi ulang

Angka 70 kata pada `cek-variasi-kalimat.py` berasal dari korpus enam naskah milik penulis hulu,
**bukan** dari naskah pengguna skill ini. Perlakukan sebagai titik awal yang masuk akal, bukan
temuan empiris tentang tulisan Anda sendiri.

## Yang sengaja TIDAK diambil

Daftar 27 pola gaya AI milik skill `humanize` hulu tidak diserap; `nulis/ai-stylometry-flags.md`
sudah lebih lengkap.

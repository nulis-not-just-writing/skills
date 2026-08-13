# Diagram alir PRISMA 2020

Dibaca pada **Tahap 9**, setelah audit numerik (`outputs/numeric_audit.md`) selesai.

Diagram alir memetakan perjalanan informasi sepanjang review: rekaman yang diidentifikasi,
disaring, dinilai kelayakannya, dimasukkan, dan dikeluarkan **beserta alasannya**. Ini figur
wajib, dan angkanya adalah hal pertama yang direkonsiliasi editor.

**Aturan keras dari `manuscript-rules.md` berlaku penuh di sini: angka diambil dari berkas
artefak, tidak diketik ulang dari ingatan.** Setiap kotak di bawah harus punya sumber di
`outputs/`. Bila sebuah angka tidak ada sumbernya, tulis `[UNRESOLVED: ...]`, jangan ditebak.

---

## Tiga istilah yang tidak boleh tertukar

Kekeliruan paling umum, dan yang paling cepat terlihat oleh reviewer:

| Istilah | Artinya |
|---|---|
| **Record** (rekaman) | judul dan/atau abstrak sebuah laporan yang terindeks di basis data atau registri |
| **Report** (laporan) | dokumennya — artikel jurnal, preprint, abstrak konferensi, bab buku |
| **Study** (studi) | investigasinya — bisa dilaporkan dalam lebih dari satu report |

Satu studi bisa punya beberapa laporan; satu laporan bisa memuat beberapa studi. Diagram alir
melacak ketiganya, dan kotak terakhir memisahkan "studi yang dimasukkan" dari "laporan atas studi
yang dimasukkan" justru karena angkanya sering berbeda.

---

## Memilih template

Empat template resmi. Ditentukan dua pertanyaan:

1. Review **baru** atau **pemutakhiran** review sebelumnya?
2. Pencarian hanya **basis data/registri**, atau juga **sumber lain** (situs web, penelusuran
   sitasi, literatur kelabu, organisasi)?

| Jenis review | Sumber | Template |
|---|---|---|
| Baru | basis data & registri saja | A |
| Baru | ditambah sumber lain | B |
| Pemutakhiran | basis data & registri saja | C |
| Pemutakhiran | ditambah sumber lain | D |

Sebagian besar SLR memakai **A** atau **B**. Yang menentukan hanyalah **penelusuran sitasi formal
di akhir Tahap 6** — yang di `slr-cowork` berstatus **opsional**, bukan langkah wajib. Dijalankan
→ template **B**. Tidak dijalankan → template **A**.

**Penelusuran sitasi di Tahap 3 tidak menggeser template.** Di sana ia dipakai untuk menguji
sensitivitas search string, dan SKILL.md menegaskan hasilnya "belum menjadi record yang dihitung".
Sesuatu yang tidak menyumbang record tidak menciptakan untai identifikasi kedua. Yang menciptakannya
hanya penelusuran formal dari daftar INCLUDED.

Bila template B dipakai, kekeliruan yang khas adalah menaruh hasil penelusuran sitasi diam-diam di
kolom basis data — angkanya lalu tidak rekonsiliasi, dan itu ketahuan saat audit numerik.

---

## Isi tiap kotak dan dari mana angkanya

### Fase IDENTIFIKASI

| Kotak | Isinya | Sumber angka |
|---|---|---|
| Rekaman dari basis data | hitungan mentah per basis data, disebutkan namanya — mis. "Scopus (n = 245), Web of Science (n = 189), DOAJ (n = 112)" | berkas ekspor Tahap 4 |
| Rekaman dari registri | hasil pencarian registri uji coba bila ada | ekspor registri |
| Duplikat dibuang | rekaman yang muncul di lebih dari satu basis data | log deduplikasi (Zotero/Mendeley/Rayyan/Covidence) |
| Dibuang alat otomatis | rekaman yang **dinilai** alat otomatis lalu ditolak | log alat; bila tak memakai, tulis 0 atau hilangkan barisnya |
| Dibuang karena alasan lain | mis. artikel retracted, bahasa di luar kriteria yang tidak tersaring saat pencarian | catatan keputusan Tahap 4 |

### Fase PENYARINGAN

| Kotak | Isinya | Sumber angka |
|---|---|---|
| Rekaman disaring | sisa setelah deduplikasi dan pembuangan pra-saring — inilah yang judul-abstraknya benar-benar dibaca | total identifikasi − duplikat − pembuangan lain |
| Rekaman dikeluarkan | dikeluarkan pada tahap judul-abstrak | `round1.tsv` Tahap 5 |
| Laporan dicari teks lengkapnya | yang lolos saring judul-abstrak | hitungan INCLUDE + MAYBE Tahap 5 |
| Laporan tak diperoleh | teks lengkap yang gagal didapat — berbayar, tak ada ILL, penulis tak menjawab | log Tahap 6 |
| Laporan dinilai kelayakannya | yang benar-benar dibaca utuh | laporan dicari − tak diperoleh |
| **Laporan dikeluarkan, dengan alasan** | tiap alasan spesifik dan dihitung | `round2.tsv` / `round3_adjudication.tsv` |

Baris terakhir yang paling sering asal-asalan. Alasannya harus **terkait kriteria inklusi**, bukan
kategori kabur: "Populasi tidak sesuai (n = 8)", "Desain studi tidak sesuai (n = 5)", "Tidak ada
outcome relevan (n = 3)", "Bukan studi empiris (n = 2)". "Tidak relevan (n = 18)" akan ditanya
reviewer.

**Bila memakai prioritisasi penyaringan (*active learning*), kotak "rekaman disaring" berubah
arti.** Angkanya adalah rekaman yang **benar-benar dilihat manusia**, bukan total setelah
deduplikasi — sisanya tidak pernah dinilai siapa pun. Jangan menaruh sisa itu di kotak "dibuang
alat otomatis": kotak itu untuk rekaman yang **dinilai** alat lalu ditolak, sedangkan pada
prioritisasi rekaman sisa tidak dinilai sama sekali. PRISMA 2020 memang belum punya slot yang
tepat untuk keadaan ini — pengembang ASReview menyatakannya terus terang. Yang dikerjakan review
terbitan: sebut keempat angkanya di prosa Methods (teridentifikasi, disaring manusia, aturan
berhenti + estimasi recall, dimasukkan), lalu pilih satu perlakuan diagram dan **nyatakan pilihan
itu di legenda figur**. Rujukan dan contoh kalimatnya di `rujukan-ai-screening.md` §5.

### Fase DIMASUKKAN

| Kotak | Isinya | Sumber angka |
|---|---|---|
| Studi dimasukkan dalam review | jumlah studi berbeda yang masuk sintesis | lembar ekstraksi Tahap 7 |
| Laporan atas studi yang dimasukkan | jumlah dokumennya | hitung dokumen sebenarnya — bisa berbeda dari jumlah studi |

### Template B/D — kolom sumber lain

Rekaman dari situs web, dari penelusuran sitasi (mundur: daftar pustaka studi yang masuk; maju:
siapa yang menyitir studi itu), dan dari organisasi/kontak peneliti. Untai ini punya alur
"dicari–tak diperoleh–dinilai–dikeluarkan" sendiri, lalu **bergabung di kotak "studi dimasukkan"**.

---

## Verifikasi aritmetika sebelum menggambar

Kaskadenya adalah penjumlahan berantai, dan galat satu-angka di dalamnya sering ditemukan editor.
Tersedia pemeriksa otomatis milik `submit` — tetapi **ia menuntut tiga berkas TSV per ronde, dan
`slr-cowork` tidak menghasilkannya.** Keputusan penyaringan di sini hidup sebagai sheet di dalam
`screening.xlsx` dan `fulltext_screening.xlsx`. Ekspor dulu, baru jalankan:

```bash
# 1) ekspor sheet keputusan menjadi TSV (sesuaikan nama sheet & kolom proyek Anda)
python3 - <<'PY'
import pandas as pd, pathlib
pathlib.Path("outputs/cascade").mkdir(parents=True, exist_ok=True)
pd.read_excel("screening.xlsx",          sheet_name="data"       ).to_csv("outputs/cascade/round1.tsv", sep="\t", index=False)
pd.read_excel("fulltext_screening.xlsx", sheet_name="data"       ).to_csv("outputs/cascade/round2.tsv", sep="\t", index=False)
pd.read_excel("fulltext_screening.xlsx", sheet_name="adjudikasi" ).to_csv("outputs/cascade/round3.tsv", sep="\t", index=False)
PY

# 2) jalankan pemeriksa (--round1/2/3 wajib; --manuscript dan --out opsional)
python3 ~/.claude/skills/submit/scripts/hulu/prisma_cascade_check.py \
    --round1 outputs/cascade/round1.tsv \
    --round2 outputs/cascade/round2.tsv \
    --round3 outputs/cascade/round3.tsv \
    --manuscript outputs/manuscript_final.md \
    --out outputs/prisma_cascade.json
```

Bila nama kolom keputusan berbeda dari bawaan skrip, tunjuk lewat `--r1-col` / `--r2-col` / `--r3-col`.

Skrip menghitung kaskade kanonik dari keputusan mentah lalu membandingkannya dengan prosa naskah.
**Tiga batas yang harus Anda tahu:** pembandingan prosa hanya mengenali beberapa frasa baku bahasa
Inggris, angka "records identified" tidak diperiksa sama sekali, dan untai penelusuran sitasi
(template B) berada di luar jangkauannya. Jadi kelolosan skrip bukan bukti kaskadenya benar —
cocokkan sisanya dengan mata terhadap `numeric_audit.md`.

Prasyarat: `submit` terpasang di `~/.claude/skills/`. Bila tidak, lewati langkah ini dan
rekonsiliasi manual — ketiga persamaan di bawah tetap wajib cocok.

Tiga rekonsiliasi yang wajib cocok:

1. disaring = identifikasi − duplikat − pembuangan lain
2. dinilai kelayakannya = dicari teks lengkapnya − tak diperoleh
3. studi dimasukkan = dinilai kelayakannya − dikeluarkan (jumlah seluruh alasan)

---

## Menggambar

Ikuti konvensi figur Tahap 8: **SVG untuk submisi, PNG 300 DPI untuk pratinjau**, disimpan di
`outputs/figures/`. Beri label `Figure 1. PRISMA 2020 flow diagram of study selection` kecuali
urutan figur menuntut nomor lain, dan tempatkan di Results.

Bila jurnal target meminta berkas Word, tabel bersel gabung dengan panah "→"/"↓" sudah memadai;
banyak jurnal juga menerima unggahan SVG/PDF terpisah. Template resmi berformat Word dan PowerPoint
tersedia di prisma-statement.org — **memakai template resmi lebih aman daripada menggambar ulang**,
karena tata letak dan nama kotaknya sudah sesuai standar.

---

**Sumber:** Page MJ, McKenzie JE, Bossuyt PM, dkk. *The PRISMA 2020 statement: an updated guideline
for reporting systematic reviews.* BMJ. 2021;372:n71.
DOI [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71) — CC BY 4.0.
Struktur template dan panduan per kotak diadaptasi dari `slr-prisma` (MIT); lihat NOTICE.md.

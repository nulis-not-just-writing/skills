# visualisasi-data — figur yang berbahasa sesuai risetnya

*[Read this in English](../visualisasi-data.md)*

**v1.0.0** · [unduh zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/visualisasi-data-1.0.0.zip)

Merancang dan membuat figur ilmiah yang **bentuk visualnya mengikuti konteks riset**, bukan jatuh ke
bar dan line sebagai kebiasaan — lalu menahannya pada aturan yang membuat sebuah figur benar:
fidelitas data, sebaran yang tampak, aman buta warna, spesifikasi cetak, caption, dan QA
pra-submisi.

## Masalah yang ditangani

Figur yang lemah jarang gagal karena estetika. Ia gagal karena **bentuknya tidak mengatakan apa-apa
tentang objek yang diteliti**.

Kekuatan alfa 14 elektroda dijadikan bar chart 14 batang. Prevalensi 38 provinsi dijadikan 38 batang
terurut. Sepuluh studi meta-analisis dijadikan tabel. Semuanya "benar", dan semuanya membuang
informasi yang sudah ada di dalam data — bahwa elektroda punya posisi di kepala, provinsi punya
posisi di peta, dan studi punya presisi yang berbeda-beda.

## Uji Rujukan

Sebelum memilih jenis grafik, jawab satu pertanyaan: **satu baris data ini *adalah* apa di dunia
nyata?** Bentuk visualnya mengikuti jawaban itu, bukan mengikuti kebiasaan.

| Satu baris data adalah… | Bahasa visual yang benar | Bukan |
|---|---|---|
| Posisi di kulit kepala | Topografi / montase 10-20 | Bar per elektroda |
| Wilayah administratif | Peta, kartogram, tile-grid | Bar terurut per wilayah |
| Satu studi dalam sintesis | Forest plot | Tabel effect size |
| Item kuesioner ordinal | Diverging stacked bar | Bar rerata Likert |
| Koefisien dalam model | Dot-whisker plot | Tabel regresi |
| Konstruk laten dan jalur antar-konstruk | Diagram jalur digambar ulang dari angka estimasi | Tangkapan layar SmartPLS |
| Peserta **dan** butir pada satu skala | Peta Wright (Rasch) | Bar skor rerata |
| Dua input kontinu → satu luaran | Permukaan 3D **+** kontur 2D | 3D saja, atau tabel |
| Alternatif × banyak kriteria | Koordinat paralel | Bar skor / radar plot |

Bar chart baru sah bila rujukannya **memang** kategori abstrak tanpa posisi, urutan, atau relasi —
dan bahkan saat itu, titik data individual wajib ditampilkan di atasnya bila n < 25.

Tabel lengkapnya 22 baris, mencakup alluvial, event study, kurva Lorenz, front Pareto, confusion
matrix, diagram air terjun, diagram alir PRISMA/CONSORT, dan lainnya.

## Tiga lapis di setiap figur yang selesai

Yang paling sering hilang adalah lapis ketiga.

1. **Substrat** — bidang tempat data diletakkan: kepala, peta, genom, sumbu waktu, matriks, ruang
   laten. Substrat inilah yang membuat figur "berbahasa" domainnya.
2. **Kanal kuantitas** — bagaimana angka dipetakan: warna sekuensial untuk besaran satu arah, warna
   divergen untuk besaran bertanda dengan pusat pada nol semantik, posisi, ukuran. Satu kuantitas,
   satu kanal.
3. **Ketidakpastian** — sebaran antar-ulangan digambar di belakang rerata, selang kepercayaan, n
   tertulis, hasil uji dilaporkan apa adanya **termasuk yang tidak signifikan**. "n.s." adalah
   hasil, bukan kekosongan.

## Empat belas rute domain, dan tidak ada jalan buntu untuk sisanya

Empat belas berkas domain dimuat sesuai kebutuhan — EEG/MEG/fNIRS, geospasial, klinis-epidemiologi,
omics-genomik, ML engineering, survei-psikometri, pendidikan dan Rasch/IRT, ekonomi-bisnis, PLS-SEM
dan CB-SEM, kualitatif, kimia-material, lingkungan-geosains, bibliometrik-review, serta permukaan 3D
dan MCDM. Tiap berkas memuat bentuk kanonik domainnya, jebakan yang lazim, dan resep kode.

**Bidang yang tidak ada di daftar bukan jalan buntu.** Substrat visual tidak ditentukan oleh nama
bidang melainkan oleh **struktur datanya**, dan struktur itu jumlahnya terbatas. Satu berkas rujukan
terpisah memetakan 22 struktur — posisi pada objek fisik, waktu bersiklus, data berarah, persilangan
dua kategori, aliran, hierarki, trade-off, kesepakatan dua alat ukur — masing-masing ke substratnya,
plus prosedur lima langkah untuk menemukan konvensi bidang yang belum dikenal.

Aturannya eksplisit: **jangan pernah mundur ke bar chart hanya karena bidangnya tidak terdaftar.**

## Batas kejujuran

**Geometri tidak pernah dikarang.** Posisi elektroda, batas wilayah, koordinat peta, dan struktur
molekul diambil dari sumber standar — bukan diperkirakan. Bila sumbernya tidak ada, skill
mengatakannya dan meminta user menyediakan, atau menggambar bentuk skematik yang **dilabeli
eksplisit sebagai skematik**.

**Data tidak pernah dikarang.** Bila datanya belum ada, figur kerangka digambar dengan data
placeholder yang ditandai `[DATA PLACEHOLDER]` *di dalam gambar*, supaya mustahil lolos ke naskah
tanpa disadari.

**Hasil nol tidak dihaluskan.** Hasil yang tidak signifikan tetap digambar dan tetap dilabeli. Judul
panel tidak boleh mengklaim melebihi ujinya.

**Trace ilustratif** — simulasi untuk menjelaskan mekanisme — wajib dibangkitkan dari parameter
terukur studi itu sendiri, dan dilabeli "ilustratif" di dalam panel *dan* di caption.

## Verifikasi yang benar-benar bisa dijalankan

Tiga pemeriksaan menangkap tiga jenis cacat yang berbeda, dan yang ketiga justru paling sering
dilewati:

| Pemeriksaan | Menangkap |
|---|---|
| `check_layout` | tata letak: panel menciut jadi nol — dijadikan galat, bukan warning |
| `check_overlaps` | geometris: teks bertumpang teks, atau menabrak spine |
| Potongan panel → **lihat gambarnya** | perseptual: label berkontras rendah, penunjuk menyilang, warna seri tertukar |

Cek geometris tidak bisa melihat warna yang tertukar. Hanya melihat panel yang sudah dirender yang
bisa.

Ada juga sapuan baris perintah terhadap berkas hasil simpan:

```bash
python scripts/figcheck.py figures/fig2_topografi.png --kolom single
```

## Siap cetak sejak awal

Vektor (PDF/EPS) untuk naskah plus PNG 300 dpi untuk pratinjau, ditulis oleh satu panggilan
`save_figure()`. Ukuran font **pada ukuran cetak akhir** minimal 7 pt. Lebar mengikuti kolom jurnal
— umumnya 85 mm satu kolom, 180 mm dua kolom. Tujuan akhirnya ditanyakan di langkah 0, **sebelum**
apa pun digambar, bukan sesudah.

## Kapan dipakai

- Butuh figur untuk artikel jurnal dan ingin figurnya terbaca seperti milik bidang itu
- Figur Anda monoton — semuanya berakhir jadi bar chart atau line chart
- Reviewer bilang figur Anda tidak informatif, tidak terbaca, atau di bawah spesifikasi
- Sedang menyiapkan gambar untuk `.tex` atau `.docx` dan lebar kolom serta fontnya harus benar
- Punya model PLS-SEM dan hendak menempelkan tangkapan layar SmartPLS ke naskah
- Dua hyperparameter disapu jadi satu metrik, dan tabel menyembunyikan bentuknya

## Prasyarat

Ini satu-satunya skill di repo ini yang **bukan stdlib-only**. `matplotlib` dan `numpy` wajib;
`scipy`, `pillow`, `pypdf`, dan `mne` opsional dan hanya memperdalam pemeriksaan tertentu. `topomap`
**tidak** membutuhkan MNE — koordinat 10-20 sudah dibakukan di dalam modulnya.

Lihat [Prasyarat](Prasyarat.md).

## Posisinya dalam rantai

`nulis` menentukan hasil mana yang layak jadi figur · **`visualisasi-data`** merancang dan
membuatnya · `polish-manuscript` memeriksa figur yatim — dirujuk tapi tak ada, atau ada tapi tak
pernah dirujuk · `submit` memeriksa kepatuhan figur terhadap author guidelines jurnal · `revisi`
menangani permintaan perbaikan figur dari reviewer.

---
name: visualisasi-data
description: >-
  Rancang dan buat figur ilmiah yang bahasa visualnya mengikuti konteks riset, bukan
  bar/line generik: data EEG jadi kepala dengan elektroda di posisi 10-20 sebenarnya, data
  antarwilayah jadi peta/kartogram, meta-analisis jadi forest plot, item Likert jadi
  diverging bar, sapuan dua hyperparameter atau permukaan fuzzy jadi permukaan 3D
  berpasangan peta kontur (setara surf/gensurf MATLAB), MCDM jadi koordinat paralel,
  asesmen jadi peta Wright Rasch, PLS-SEM jadi diagram jalur digambar ulang dari angka
  estimasi (gaya naskah atau mirip SmartPLS, bukan tangkapan layar). Bidang di luar 14
  domain bawaan ditangani lewat tabel struktur data yang memetakan struktur ke substrat
  visual. Gunakan saat user meminta grafik, plot, visualisasi, topografi, peta, atau figur
  artikel jurnal; saat figurnya monoton atau ditolak reviewer; atau saat menyiapkan gambar
  untuk .tex/.docx. Mencakup uji rujukan, aturan kebenaran figur, komposisi multi-panel,
  spesifikasi siap-cetak, caption, dan QA pra-submisi.
metadata:
  author: Mubaroq ADB | RPI
  version: 1.0.0
---

# figur — Bahasa Visual Sesuai Konteks Riset

Figur yang lemah jarang gagal karena estetika. Ia gagal karena **bentuknya tidak
mengatakan apa-apa tentang objek yang diteliti**: kekuatan alfa 14 elektroda
dijadikan bar chart 14 batang, prevalensi 38 provinsi dijadikan bar chart 38
batang terurut, sepuluh studi meta-analisis dijadikan tabel. Semua "benar", dan
semuanya membuang informasi yang sudah ada di dalam data — bahwa elektroda punya
posisi di kepala, provinsi punya posisi di peta, dan studi punya presisi yang
berbeda-beda.

Skill ini mengerjakan dua hal yang berbeda dan keduanya wajib:

1. **Memilih bentuk visual dari rujukan datanya** (bagian utama skill ini).
2. **Menjaga kebenaran figur** — fidelitas data, ketidakpastian, label, warna,
   spesifikasi cetak (`references/aturan-figur.md`).

Bentuk yang tepat dengan sebaran yang disembunyikan tetap figur yang buruk.
Begitu pula sebaliknya.

## Langkah 0 — Wajib: tetapkan konteks dulu

Jangan menggambar apa pun sebelum lima hal ini jelas. Tanyakan dengan daftar
bernomor biasa (**jangan AskUserQuestion**), dan tanyakan hanya yang belum
diketahui dari percakapan atau dari datanya:

1. **Klaim figur** — satu kalimat yang harus dibuat benar oleh figur ini. Bukan
   "visualisasi hasil eksperimen", tapi "beban kognitif menaikkan theta frontal
   tapi tidak alfa parietal". Satu figur, satu klaim.
2. **Unit observasi** — satu baris data ini *adalah* apa? (lihat Uji Rujukan)
3. **Sumber angka** — file/tabel mana yang jadi acuan. Figur dan tabel naskah
   **wajib membaca berkas agregat yang sama**; ini sumber ketidakcocokan angka
   yang paling sering lolos sampai proofread.
4. **Struktur ketidakpastian** — ada berapa ulangan/subjek/seed/fold, dan
   sebarannya dilaporkan sebagai apa (SD, SEM, CI 95%, kuartil).
5. **Tujuan akhir** — jurnal target dan lebar kolomnya, atau presentasi/poster.
   Ini menentukan ukuran fisik dan ukuran font, dan harus diketahui **sebelum**
   menggambar, bukan sesudah.

Bila user tidak punya jawaban untuk (4), tanyakan sekali lagi dengan tegas:
figur tanpa lapis ketidakpastian hanya sah untuk kuantitas yang memang tunggal
dan eksak (jumlah partisipan, spesifikasi perangkat).

## Prinsip inti — Uji Rujukan

Sebelum memilih jenis grafik, jawab: **satu baris data ini adalah apa di dunia
nyata?** Bentuk visualnya mengikuti jawaban itu, bukan mengikuti kebiasaan.

| Satu baris data adalah… | Bahasa visual yang benar | Bukan |
|---|---|---|
| Posisi di kulit kepala | Topografi/montase 10-20 | Bar per elektroda |
| Pasangan waktu × frekuensi | Peta time-frequency | Line per band |
| Wilayah administratif | Peta, kartogram, tile-grid | Bar terurut per wilayah |
| Posisi di genom | Manhattan plot | Tabel p-value |
| Satu studi dalam sintesis | Forest plot | Tabel effect size |
| Pasien sepanjang waktu | Swimmer/spaghetti/Kaplan-Meier | Bar rerata per kelompok |
| Item kuesioner ordinal | Diverging stacked bar | Bar rerata Likert |
| Koefisien dalam model | Dot-whisker plot | Tabel regresi |
| Konstruk laten dan jalur antar-konstruk | Diagram jalur digambar ulang | Tangkapan layar SmartPLS |
| Peserta **dan** butir pada satu skala | Peta Wright (Rasch) | Bar skor rerata |
| Kontribusi komponen ke perubahan total | Diagram air terjun | Tabel selisih |
| Efek per periode di sekitar guncangan | Event study | Dua bar sebelum-sesudah |
| Ketimpangan distribusi | Kurva Lorenz + Gini | Rasio 20% teratas saja |
| Perpindahan antar kategori | Alluvial/Sankey | Dua pie chart |
| Pasangan simpul (relasi) | Network / matriks adjacency | Daftar |
| Komposisi menjumlah 1 | Stacked bar, ternary | Pie |
| Dua input kontinu → satu luaran | Permukaan 3D **+** kontur 2D | 3D saja, atau tabel |
| Alternatif × banyak kriteria | Koordinat paralel | Bar skor / radar plot |
| Trade-off dua metrik | Scatter + front Pareto | Dua bar chart |
| Prediksi vs aktual per kelas | Confusion matrix | Bar akurasi |
| Titik di ruang fisik/kedalaman | Profil/penampang, sumbu terbalik | Line biasa |
| Tahap dalam alur seleksi | Diagram alir (PRISMA/CONSORT) | Prosa |

Bar chart baru sah bila rujukannya **memang** kategori abstrak tanpa posisi,
urutan, atau relasi — dan bahkan saat itu, titik data individual wajib
ditampilkan di atasnya bila n < 25.

## Tiga lapis setiap figur

Setiap figur yang selesai punya ketiganya. Yang paling sering hilang adalah
lapis 3.

1. **Substrat** — bidang tempat data diletakkan: kepala, peta, genom, sumbu
   waktu, matriks, ruang laten. Substrat inilah yang membuat figur "berbahasa"
   domain.
2. **Kanal kuantitas** — bagaimana angka dipetakan: warna sekuensial (besaran
   satu arah), warna divergen (besaran bertanda, pusat pada nol semantik),
   posisi, ukuran. Satu kuantitas satu kanal.
3. **Ketidakpastian** — sebaran antar-ulangan digambar di belakang rerata,
   selang kepercayaan, n tertulis, hasil uji dilaporkan apa adanya **termasuk
   yang tidak signifikan**. "n.s." adalah hasil, bukan kekosongan.

## Rute per domain

Baca **hanya** file domain yang relevan (progressive disclosure). Setiap file
berisi: bentuk kanonik domain itu, kapan dipakai, jebakan yang lazim, dan
resep kode.

| Konteks riset | Baca |
|---|---|
| EEG, MEG, fNIRS, ERP, konektivitas otak, BCI | `references/domains/neuro-eeg.md` |
| Negara, provinsi, kabupaten, titik koordinat, penginderaan jauh | `references/domains/geospasial.md` |
| Uji klinis, epidemiologi, diagnostik, meta-analisis, survival | `references/domains/klinis-epidemiologi.md` |
| Genomik, transkriptomik, proteomik, mikrobiom, filogeni | `references/domains/omics-genomik.md` |
| Machine learning, sistem, benchmark, ablasi, optimasi | `references/domains/ml-engineering.md` |
| Survei, psikometri, SEM, kuesioner lintas bidang | `references/domains/sosial-survei.md` |
| Pendidikan, asesmen, Rasch/IRT, pra-pascates, evaluasi pembelajaran | `references/domains/pendidikan.md` |
| Ekonomi, keuangan, akuntansi, bisnis, data panel, ketimpangan | `references/domains/ekonomi-bisnis.md` |
| SEM: PLS-SEM (SmartPLS), CB-SEM, diagram jalur, mediasi/moderasi | `references/domains/sem-pls.md` |
| Wawancara, etnografi, studi kasus, analisis tematik | `references/domains/kualitatif.md` |
| Kimia, material, spektroskopi, difraksi, termodinamika | `references/domains/kimia-material.md` |
| Hidrologi, iklim, tanah, oseanografi, geologi | `references/domains/lingkungan-geosains.md` |
| Scoping/systematic review, bibliometrik, pemetaan bidang | `references/domains/bibliometrik-review.md` |
| Permukaan 3D, response surface, hyperparameter, fuzzy, MCDM (TOPSIS/AHP/SAW) | `references/domains/permukaan-3d-mcdm.md` |

**Bidang yang tidak ada di tabel → baca `references/domain-baru.md`.** Sepuluh
file di atas adalah jalan pintas, bukan batas cakupan. Substrat visual tidak
ditentukan oleh nama bidang melainkan oleh **struktur datanya**, dan struktur itu
jumlahnya terbatas — file `domain-baru.md` memuat tabel 22 struktur (posisi pada
objek fisik, waktu bersiklus, data berarah, persilangan dua kategori, aliran,
hierarki, trade-off, kesepakatan dua alat ukur, …) beserta substrat untuk
masing-masing, plus prosedur lima langkah untuk menemukan konvensi bidang yang
belum kamu kenal. **Jangan pernah mundur ke bar chart hanya karena bidangnya
tidak terdaftar.**

## Aturan yang selalu berlaku

Ringkas di sini; versi lengkap dengan alasan dan ujinya di
`references/aturan-figur.md` — **baca file itu sebelum render final.**

- **Fidelitas.** Baris yang dieksklusi tidak boleh masuk statistik ringkas.
  Judul yang berbentuk klaim harus benar untuk **setiap** kategori di sumbu.
  Satu klaim kuantitatif punya satu angka kanonik di seluruh naskah.
- **Sebaran wajib tampil.** Bar rerata polos dilarang bila ada ulangan: pakai
  titik individual, box/violin, atau bar + CI. Nyatakan n.
- **Warna mengikat entitas.** Sekali sebuah warna dipakai untuk satu kondisi,
  warna itu dipakai untuk kondisi tersebut di semua panel semua figur. Kontribusi
  sendiri digambar pekat; pembanding digambar abu-abu berbobot rendah.
- **Aman buta warna.** Jangan pernah merah vs hijau untuk dua hal yang
  dikontraskan. Jangan pakai colormap pelangi/jet.
- **Ekonomi label.** Setiap tanda harus bisa dikenali dari figur saja; sisanya
  (n, apa yang dikontrol, kepanjangan akronim, caveat) pindah ke caption.
- **Siap cetak.** Vektor (PDF/EPS) untuk naskah + PNG 300 dpi untuk pratinjau.
  Ukuran font **pada ukuran cetak akhir** minimal 7 pt. Lebar mengikuti kolom
  jurnal (umumnya 85 mm satu kolom, 180 mm dua kolom).
- **Verifikasi setelah render.** Jalankan cek tumpang-tindih dan lihat hasil
  gambarnya, jangan hanya mempercayai kodenya.

## Batas kejujuran

- **Jangan mengarang geometri.** Posisi elektroda, batas wilayah, koordinat
  peta, dan struktur molekul diambil dari sumber standar (montase MNE, shapefile
  resmi, database struktur) — bukan diperkirakan. Bila sumbernya tidak ada,
  katakan dan minta user menyediakan, atau gunakan bentuk skematik yang
  **dilabeli eksplisit sebagai skematik**.
- **Jangan mengarang data.** Bila data belum ada, buat figur kerangka dengan
  data placeholder yang ditandai jelas `[DATA PLACEHOLDER]` di dalam gambar,
  supaya mustahil lolos ke naskah tanpa disadari.
- **Jangan menghaluskan hasil nol.** Hasil yang tidak signifikan tetap
  digambar dan dilabeli. Judul panel tidak boleh mengklaim melebihi ujinya.
- **Trace ilustratif** (simulasi untuk menjelaskan mekanisme) harus dibangkitkan
  dari parameter terukur studi itu sendiri, dilabeli "ilustratif" di dalam panel
  **dan** di caption.

## Alur kerja

1. Tetapkan konteks (Langkah 0).
2. Jalankan Uji Rujukan → tentukan substrat → baca file domain yang relevan
   (atau `references/domain-baru.md` bila bidangnya tidak terdaftar).
3. Baca `references/aturan-figur.md`.
   **Bila figurnya lebih dari satu panel**, baca juga
   `references/multi-panel.md` — klaim satu kalimat → kerangka panel bergrid
   (a = kail, b = pemikul klaim, sisanya bukti) → verifikasi berlapis →
   putaran telaah bermusuhan.
4. Muat perkakas dan gaya dasar:

   ```python
   import sys; sys.path.insert(0, "scripts")   # atau ~/.claude/skills/visualisasi-data/scripts
   from vizkit import *
   apply_style()                          # ladder font, tick keluar, legenda tanpa bingkai
   fig, ax = new_figure(width="single")   # 85 mm; "double" = 180 mm
   ```

   Perkakas yang tersedia:

   | Kelompok | Fungsi |
   |---|---|
   | Gaya & simpan | `apply_style`, `new_figure`, `save_figure`, `panel_letter` |
   | Multi-panel | `panel_grid` (grid 12 kolom dari kerangka panel, menolak kerangka tak konsisten), `panel_crops` (kotak potong per panel untuk cek perseptual), `check_layout` (axes menciut jadi galat, bukan warning) |
   | Warna | `palette`, `focal_comparator`, `ramp`, `cvd_check` |
   | Ketidakpastian | `spread_lines`, `mean_line`, `points_with_mean`, `sig_stars`, `sig_bracket` |
   | Substrat kepala | `electrode_xy`, `draw_head`, `topomap`, `montage_glyph`, `ELECTRODES_1020` |
   | Substrat peta | `tile_map`, `ID_PROVINSI_TILES` |
   | Bentuk domain | `likert_diverging`, `forest_plot`, `dot_whisker`, `confusion_matrix`, `alluvial` |
   | Dua input → satu luaran | `surface_pair` (3D + kontur berpasangan, penanda optimum), `scatter3d` |
   | Banyak kriteria | `parallel_coordinates` (MCDM, kriteria biaya dibalik otomatis) |
   | SEM | `pls_path_diagram` (dua gaya: `journal` dan `smartpls` (lingkaran biru + indikator kuning); tata letak otomatis, reflektif/formatif, jalur n.s. tetap tampak, menolak model bersiklus) |
   | Asesmen & ekonomi-bisnis | `wright_map` (item-person Rasch, melaporkan kesenjangan skala), `event_study` (menandai koefisien pra-perlakuan yang signifikan), `waterfall` (rotasi label terukur otomatis), `lorenz_curve` (Gini dihitung dari kurva yang digambar) |
   | Substrat generik (lintas bidang) | `rose_plot` (data berarah/bersiklus + statistik sirkular), `slope_plot` (dua kondisi berpasangan), `ridgeline` (banyak distribusi), `bubble_matrix` (persilangan dua kategori, sel kosong ditandai) |
   | Verifikasi | `check_overlaps`, `check_layout`, `cvd_check` |

   Semuanya matplotlib murni — `topomap` tidak membutuhkan MNE (koordinat 10-20
   sudah dibakukan di dalam modul dari montase `standard_1020`; set
   `prefer_mne=True` untuk membacanya langsung dari MNE bila terpasang).
5. Gambar dengan bentuk domain, lengkap dengan lapis ketidakpastian.
6. Simpan: `save_figure(fig, "fig2_topografi")` → menulis `.pdf` **dan** `.png`.
7. QA berlapis — tiga pemeriksaan, tiga jenis cacat:

   ```python
   check_layout(fig, "fig2")     # tata letak: axes menciut? (multi-panel)
   check_overlaps(fig, "fig2")   # geometris: teks bertumpang / menabrak spine
   paths = save_figure(fig, "fig2_topografi")
   for huruf, box in panel_crops(fig).items():
       host.view_image(paths[-1], crop=box)     # perseptual: LIHAT tiap panel
   ```

   ```bash
   python scripts/figcheck.py figures/fig2_topografi.png --kolom single
   ```

   Cek geometris tidak menangkap label berkontras rendah, penunjuk yang
   menyilang, atau warna seri yang tertukar — potongan panel itulah yang
   menangkapnya. Untuk figur multi-panel, tambahkan pemeriksaan lintas panel
   (`references/multi-panel.md` §4): pengikatan warna, satu-angka-satu-klaim,
   dan kosakata yang seragam antara skema dan label sumbu.
8. Sisipkan ke naskah dan tulis caption mengikuti
   `references/integrasi-naskah.md`.

## Rantai skill

`nulis` menyusun struktur section dan menentukan hasil mana yang layak jadi
figur · **`visualisasi-data`** merancang dan membuat figurnya · `polish-manuscript` memoles
prosa dan memeriksa figur yatim (dirujuk tapi tak ada, atau ada tapi tak
dirujuk) · `submit` memeriksa kepatuhan format figur terhadap author guidelines
sebelum dikirim · `revisi` menangani permintaan perbaikan figur dari reviewer.

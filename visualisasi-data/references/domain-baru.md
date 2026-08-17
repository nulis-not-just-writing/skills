# Bidang di Luar Sepuluh Domain

Sepuluh file domain adalah **jalan pintas, bukan batas cakupan**. File ini
prosedur untuk bidang yang tidak ada di tabel — dan prosedurnya bekerja karena
satu fakta: **substrat visual tidak ditentukan oleh nama bidang, melainkan oleh
struktur datanya**, dan struktur itu jumlahnya terbatas.

Riset akustik, arkeologi, ilmu pangan, akuntansi, robotika, linguistik korpus,
farmakokinetik, ilmu olahraga, arsitektur, astronomi, ilmu perpustakaan — tidak
satu pun punya file sendiri, dan semuanya tertangani oleh tabel di bawah.

---

## Langkah 1 — Klasifikasikan struktur, bukan bidang

Jangan bertanya "ini bidang apa". Tanyakan **struktur unit observasinya**, lalu
ambil substratnya dari tabel ini.

| Struktur data | Substrat | Contoh lintas bidang |
|---|---|---|
| **Posisi pada objek fisik** | Gambar objek + nilai pada posisinya | Sensor pada bilah turbin, regangan pada jembatan, keausan pada gigi, kerusakan pada artefak, tekanan pada telapak kaki |
| **Posisi pada bidang/ruang 2-3D** | Peta, denah, penampang, volume | Denah situs arkeologi, lantai pabrik, ruang kelas, kanopi hutan, sebaran kursi di ruang sidang |
| **Posisi pada sumbu terurut fisik** | Profil sepanjang sumbu | Kedalaman, ketinggian, jarak dari pantai, posisi sepanjang usus, jarak dari pusat kota, posisi dalam rantai polimer |
| **Koordinat spektral / frekuensi** | Spektrum, sumbu mengikuti konvensi bidang | Akustik, optik, getaran mesin, spektrum daya sinyal apa pun |
| **Waktu kontinu** | Deret waktu; run individual di belakang rerata | Semua bidang |
| **Waktu bersiklus** | Diagram mawar / plot polar (`rose_plot`) | Jam kedatangan pasien, musim panen, fase bulan, siklus produksi, jam sibuk lalu lintas |
| **Waktu sampai kejadian** | Kurva survival + tabel berisiko | Kegagalan komponen, putus sekolah, keluar kerja, kambuh, umur pakai material |
| **Dua kondisi berpasangan** | Slope/dumbbell (`slope_plot`) | Pratest-pascates, sebelum-sesudah kebijakan, dua rilis, dua musim |
| **Banyak distribusi, dukungan sama** | Ridgeline (`ridgeline`) | Skor per sekolah, harga per pasar, durasi per operator |
| **Data berarah (sudut)** | Mawar + statistik sirkular (`rose_plot`) | Orientasi serat, arah gerak, sudut sendi, arah hadap bangunan |
| **Persilangan dua kategori** | Matriks gelembung/heatmap (`bubble_matrix`) | Bahan × proses, kebijakan × sektor, metode × luaran, spesies × habitat |
| **Relasi antar entitas** | Network, matriks adjacency, dendrogram | Rantai pasok, jaringan sitasi, interaksi sosial, ko-okurensi kata |
| **Aliran/perpindahan berkuantitas** | Sankey/alluvial (`alluvial`) | Neraca energi, alur dana, perpindahan pekerjaan, alur material |
| **Hierarki / bagian-keseluruhan** | Treemap, sunburst, icicle | Anggaran, taksonomi, struktur organisasi, struktur berkas |
| **Komposisi menjumlah 1** | Stacked bar, ternary (3 komponen) | Komposisi paduan, alokasi waktu, pangsa pasar, komposisi tanah |
| **Trade-off dua kriteria** | Scatter + front Pareto | Biaya-kinerja, kekuatan-bobot, presisi-recall, hasil-emisi |
| **Estimasi + ketidakpastian** | Dot-whisker (`dot_whisker`), forest (`forest_plot`) | Semua bidang yang mengestimasi parameter |
| **Ordinal dari responden** | Diverging stacked bar (`likert_diverging`) | Semua bidang yang memakai kuesioner |
| **Prediksi vs aktual** | Confusion matrix, kalibrasi, Bland-Altman | Semua bidang yang memvalidasi model/alat ukur |
| **Kesepakatan dua pengukur/alat** | Bland-Altman (selisih vs rerata) | Validasi instrumen di bidang apa pun |
| **Tahap dalam alur proses** | Diagram alir bernomor | Seleksi sampel, alur produksi, pipeline analisis |
| **Kategori nominal murni** | Bar/lollipop + titik individual | Hanya bila tidak ada struktur lain yang berlaku |

Bila ada dua struktur sekaligus (posisi **dan** waktu), substrat mengikuti yang
**paling membawa temuan**, dan yang lain jadi facet atau animasi/panel berturut.

## Langkah 2 — Cari konvensi bidangnya, jangan diciptakan

Setiap bidang mapan punya bentuk kanonik yang pembacanya harapkan, dan
melanggarnya membuat reviewer harus belajar ulang membaca figur. Sebelum
menggambar, luangkan satu langkah:

1. **Tanya user**: "Di jurnal target, hasil seperti ini biasanya digambar
   bagaimana? Ada contoh figur yang Anda anggap bagus?" Ini sumber tercepat dan
   paling akurat — user tahu bidangnya.
2. **WebSearch/WebFetch** artikel terbaru di jurnal target dengan jenis data
   yang sama; lihat figurnya. Cari kata kunci bidang + "figure" atau nama
   bentuknya.
3. **Periksa reporting guideline** bidang itu bila ada — banyak yang mewajibkan
   diagram tertentu (CONSORT, PRISMA, ARRIVE, STARD, TRIPOD, MIQE).

Tiga hal yang harus dipastikan dari konvensi:

- **Arah sumbu** (mis. wavenumber dan ppm menurun ke kanan; kedalaman terbalik).
- **Satuan dan transformasi baku** (log, dB, z-score, per kapita).
- **Bentuk yang diharapkan** untuk klaim jenis itu.

## Langkah 3 — Gambar substratnya dengan geometri yang benar

Bila substratnya objek fisik atau ruang, geometrinya **harus dari sumber**, bukan
digambar berdasarkan ingatan:

- Denah, layout, penampang → gambar teknik/CAD/foto berskala dari user.
- Batas wilayah → shapefile resmi.
- Struktur molekul/kristal → file struktur (CIF/PDB/MOL).
- Posisi sensor → tabel koordinat pemasangan.

Bila sumbernya tidak ada, ada dua jalan yang sah dan satu yang tidak:

- **Sah**: minta filenya ke user.
- **Sah**: gambar skema abstrak yang menjaga hubungan topologis (urutan,
  ketetanggaan) tanpa mengklaim akurasi metrik — dan **tulis "skematik" di dalam
  panel dan di caption**. `tile_map` adalah contoh pola ini.
- **Tidak sah**: menggambar geometri perkiraan yang terlihat seperti geometri
  sebenarnya. Pembaca tidak bisa membedakannya, dan itu klaim palsu.

## Langkah 4 — Terapkan tiga lapis dan aturan umum

Setelah substrat ditentukan, sisanya identik dengan domain mana pun:
kanal kuantitas satu-satu, lapis ketidakpastian wajib tampil, lalu seluruh
`aturan-figur.md`. Tidak ada bidang yang dikecualikan dari kewajiban
menampilkan sebaran, menyatakan n, atau memakai palet aman buta warna.

## Langkah 5 — Bila ternyata sering dipakai, jadikan file domain

Kalau kamu mengerjakan bidang yang sama tiga kali dan tiap kali mengulang
Langkah 2, itu tanda bidang tersebut layak punya file sendiri di
`references/domains/`. Formatnya sudah baku: tabel bentuk kanonik, aturan wajib
domain, jebakan yang lazim lolos, resep kode. Tawarkan ke user untuk
menambahkannya.

---

## Contoh penerapan

**Riset akustik ruang kelas** (tidak ada file domainnya). Unit observasi: waktu
dengung per pita oktaf, diukur di 9 titik dalam ruangan.

Dua struktur sekaligus: *koordinat spektral* (pita oktaf) dan *posisi dalam
ruang* (titik ukur). Temuannya adalah variasi antar-titik → substrat utama
**denah ruangan** dengan nilai pada posisi titik ukur, difacet per pita oktaf;
atau sebaliknya bila temuannya spektral. Denah diambil dari gambar arsitek, bukan
digambar ulang. Ambang standar (mis. rekomendasi waktu dengung untuk ruang
kelas) digambar sebagai garis referensi, dan sebarannya antar-pengukuran
ditampilkan — bukan satu angka per titik.

**Riset ilmu pangan — uji sensori panelis.** Unit observasi: skor 8 atribut oleh
30 panelis untuk 4 formula.

Struktur: *estimasi + ketidakpastian* pada banyak atribut sekaligus. Konvensi
bidangnya adalah spider/radar plot — dan di sini konvensi bidang berbenturan
dengan aturan umum (radar plot menyulitkan pembacaan besaran dan bentuknya
berubah bila urutan atribut diubah). Jalan tengah yang jujur: gambar bentuk yang
benar (dot-whisker per atribut, formula sebagai warna terikat) sebagai figur
utama, sebutkan pada user bahwa radar plot lazim di bidangnya, dan biarkan dia
memutuskan. Jangan diam-diam mengganti konvensi bidang tanpa memberi tahu.

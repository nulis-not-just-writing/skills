# SLR untuk Korpus Doktrinal / Normatif

Dibaca ketika korpus review bukan studi empiris: kajian hukum (fikih muamalah, hukum
positif, analisis putusan), filsafat, teologi, kajian teks, atau telaah konseptual.
Sebagian besar instrumen SLR arus utama lahir dari epidemiologi klinis dan **tidak punya
objek** pada korpus semacam ini. Yang tidak berlaku adalah **instrumennya**, bukan
tahapnya — sistematisitas, transparansi, dan dua penilai tetap wajib.

## Kerangka pengganti PICO

PICO mengandaikan populasi, intervensi, dan outcome terukur. Pada riset doktrinal, tiga
komponen itu memang tidak ada. Susun kerangka yang memenuhi **kriteria fungsional**: tiap
blok harus tertelusur ke minimal satu RQ, dan tiap blok punya *what counts / what doesn't
count / edge cases* seperti operational definition pada PICO.

Contoh kerangka yang lazim dipakai: Konsep — Konteks normatif — Sumber otoritatif —
Batasan/kewenangan — Luaran analitis. Nyatakan di Methods bahwa PICO tidak diterapkan
**beserta alasannya**; jangan diam-diam mengosongkan kolom PICO.

Simpan di `outputs/kerangka_konseptual.md`. Setiap rujukan skill ke
`pico_definitions.md` berlaku untuk file terminologi kanonikal proyek, apa pun namanya.

## Status sumber primer

Bedakan tegas dan perlakukan berbeda:

| Jenis | Perlakuan |
|---|---|
| **Literatur akademik** tentang topik | Objek screening; masuk hitungan diagram PRISMA |
| **Sumber primer otoritatif** (fatwa, regulasi, putusan pengadilan, teks kanonik) | Objek analisis, ditelusuri terpisah; **tidak masuk hitungan PRISMA**; dicatat di log tersendiri dengan tanggal akses |

Untuk instrumen hukum positif, verifikasi **nomor, tahun, dan status berlaku/dicabut** ke
sumber resmi — sejajar dengan kewajiban verifikasi DOI untuk sumber akademik. Nomor
regulasi yang salah atau sudah dicabut adalah kesalahan fatal di manuskrip hukum.

### Pelaporan korpus sumber primer di Methods — wajib, terpisah

Sumber primer tidak masuk diagram PRISMA, tetapi **tetap harus dilaporkan** dengan
ketelitian yang sama. Dasarnya PRISMA 2020 item 6–7 (sumber informasi dan strategi
pencarian), yang berlaku untuk **seluruh** sumber yang dipakai review — bukan hanya yang
melewati alur screening. Sumber primer yang dianalisis tanpa dilaporkan cara
memperolehnya membuat bagian analisis tidak dapat direplikasi, dan itu justru inti
kritik yang sering diarahkan ke review doktrinal.

Laporkan sebagai **subseksi tersendiri** di Methods, terpisah dari alur PRISMA, memuat:

- **Jenis dan jumlah** per kategori — mis. fatwa DSN-MUI (n), POJK/PBI (n), putusan pengadilan (n)
- **Sumber penelusuran** — situs DSN-MUI, JDIH OJK/BI, Direktori Putusan MA — dengan tanggal akses
- **Rentang waktu** instrumen yang dicakup, beserta alasannya
- **Kriteria pemilihan** — mengapa instrumen ini, bukan yang lain; ini yang paling sering hilang dan paling mudah ditanyakan reviewer
- **Status keberlakuan** per instrumen pada tanggal akses

Jumlah sumber primer yang jauh melebihi jumlah studi akademik adalah hal **lazim** pada
review doktrinal dan tidak perlu diseimbangkan — keduanya menjawab pertanyaan berbeda.
Studi akademik menjadi objek sintesis bukti; sumber primer menjadi objek analisis
normatif. Yang tidak boleh terjadi adalah keduanya tercampur dalam satu hitungan, atau
sumber primer muncul di Results tanpa pernah dijelaskan asal-usulnya di Methods.

Simpan di `outputs/sumber_primer_log.md`, dan jaga agar jumlah yang disebut di Methods
identik dengan isi log — angka ini masuk audit numerik lintas section seperti angka
PRISMA.

Aturan larangan menyitasi studi yang terbit setelah tanggal search berlaku untuk **studi**.
Regulasi atau putusan baru yang terbit setelah tanggal search justru perlu disebut agar
analisis tidak usang — sebutkan sebagai perkembangan pasca-search, bukan sebagai bagian
korpus yang disintesis.

## Gerbang feasibility — ambang operasional

Panduan utama menetapkan bahwa feasibility review doktrinal dinilai dari kecukupan sumber
primer dan keragaman posisi, bukan jumlah artikel. Agar gerbang itu dapat diuji, tetapkan
ambangnya **di form kesepakatan sebelum search dijalankan**, bukan sesudah hasilnya
terlihat. Titik awal yang wajar, untuk dinilai peneliti sesuai bidangnya:

| Dimensi | Ambang awal | Alasan |
|---|---|---|
| Keragaman posisi | ≥3 posisi berbeda atas pertanyaan inti | Di bawah ini, tidak ada yang bisa disintesis — hanya satu pandangan yang diulang |
| Cakupan sumber primer | ≥5 instrumen/teks otoritatif dibedah secara substantif | Menjamin analisis menyentuh sumbernya, bukan hanya komentar atas sumber |
| Literatur yang benar-benar membahas konstruk inti | ≥10 tulisan lolos kriteria blok utama | Membedakan tulisan yang menjadikannya objek analisis dari yang menyebutnya sebagai latar |
| Jumlah total (indikator sekunder) | 20–50 | Dipakai sebagai penunjuk kasar saja, bukan penentu |

Angka-angka ini pertimbangan kelayakan praktis, **tidak berasal dari literatur
metodologis** — nyatakan demikian bila masuk Methods, dan sesuaikan dengan kepadatan
literatur bidang yang bersangkutan.

## Quality appraisal

Tidak ada instrumen risk of bias yang berlaku. Yang dinilai adalah **kualitas
argumentasi**. Domain yang lazim dan bisa dinilai dua penilai secara reliabel:

- Ketertelusuran sumber: apakah dalil, pasal, atau teks yang dirujuk dapat diverifikasi
- Kesetiaan kutipan terhadap teks aslinya
- Transparansi metode penalaran (metode istinbath, kerangka penafsiran, alur argumen)
- Akurasi rujukan otoritatif (nomor, tahun, status)
- Eksplisitas rantai argumen dari premis ke simpulan
- Perlakuan atas pandangan tandingan dan khilafiyah
- Deklarasi posisi normatif penulis

Ancaman validitas yang khas bidang ini dan **tidak punya padanan** dalam kosakata risk of
bias: penulis berafiliasi dengan otoritas yang sedang dinilai kewenangannya, dan
sirkularitas — memakai produk hukum sebuah lembaga sebagai dalil pembenar kewenangan
lembaga itu sendiri. Catat sebagai *flag* terpisah, bukan skor.

**Rubrik buatan sendiri wajib**: dicari dulu apakah instrumen yang sesuai sudah ada;
dinyatakan tak tervalidasi di Methods; dilampirkan penuh sebagai apendiks; dan **tidak
dipakai sebagai gerbang eksklusi keras** — pakai untuk stratifikasi dan pembobotan klaim.

## Kepercayaan bukti

GRADE menilai certainty of effect estimates; domain imprecision (lebar CI) dan publication
bias (funnel plot) tidak punya objek tanpa effect size. Gunakan **GRADE-CERQual** bila
sintesisnya kualitatif, atau rumuskan **pernyataan kekuatan warrant per RQ** dengan
kriteria yang dinyatakan eksplisit — misalnya otoritas sumber yang dirujuk, konvergensi
argumen lintas mazhab atau aliran, dan ketahanan terhadap keberatan yang sudah diajukan.
Ikat aturan hedging ke pernyataan itu; overclaiming justru paling sering terjadi di
tulisan normatif yang tidak punya angka untuk menahannya.

## Sintesis

**Vote counting berbahaya pada korpus normatif.** Menghitung berapa penulis berpendapat X
mengubah bobot dalil menjadi popularitas — ijmaʿ semu. Kekuatan sebuah posisi ada pada
argumen dan sumbernya, bukan pada jumlah pemegangnya; posisi minoritas berdalil kuat
ditampilkan setara dan dinilai dari kekuatan argumennya. Bila frekuensi tetap dilaporkan,
nyatakan tegas bahwa itu peta persebaran wacana, bukan ukuran kebenaran.

Heterogenitas di sini **bukan gangguan**. Perbedaan metode penalaran antar penulis
biasanya justru objek yang mau dipetakan. Uji lima kriteria meta-analysis akan gagal
secara definisional (tidak ada outcome, tidak ada effect size) — nyatakan sekali di
`synthesis_path_decision.md` bahwa meta-analysis tidak berlaku secara konseptual, jangan
menulisnya sebagai kegagalan uji statistik.

## Komposisi penilai dan bahasa

Kompetensi dua penilai sering **tidak simetris** — menilai istinbath dan menilai regulasi
keuangan adalah keahlian berbeda. Panel lintas keahlian lebih tepat daripada dua screener
identik; nyatakan konfigurasinya di Methods.

Catat **bahasa korpus** dan kompetensi bahasa penilai di Tahap 1. Bila penilaian menuntut
membaca sumber dalam bahasa aslinya (Arab, dan sebagainya), nyatakan kompetensi itu — dan
laporkan sebagai limitasi bila tidak terpenuhi.

Untuk manuskrip berbahasa Inggris di bidang kajian keislaman, tetapkan **satu sistem
transliterasi** (IJMES atau Library of Congress) di Tahap 1 dan masukkan konsistensinya ke
audit terminologi.

## Database

Scopus dan Web of Science berdaya cakup rendah untuk literatur berbahasa Indonesia dan
Arab. Sertakan Garuda, SINTA, Moraref, DOAJ, Index Islamicus, dan repositori PTKIN, lalu
**justifikasi pilihan itu di Methods** dengan angka hits per database — reviewer yang
menuntut "database internasional" dijawab dengan bukti cakupan, bukan dengan mengganti
korpus.

## Kappa untuk keputusan interpretatif

Bedakan κ untuk **keputusan faktual** (tahun terbit, jenis dokumen — ambang ≥0.60 wajar)
dari κ untuk **keputusan interpretatif** (apakah sebuah tulisan benar-benar memakai
penalaran maslahah mursalah, misalnya). Untuk yang interpretatif, laporkan κ **per domain**
dengan ambang yang dijustifikasi terpisah, dan dokumentasikan sengketa substantif secara
naratif — satu angka agregat menyembunyikan persis informasi yang paling berguna.

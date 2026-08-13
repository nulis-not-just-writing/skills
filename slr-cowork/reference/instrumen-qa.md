# Instrumen quality assessment — memilih, memakai, melaporkan

Dibaca pada **Tahap 7**, dan butir E form kesepakatan diisi dari sini **sebelum** Tahap 7 berjalan.

Berisi **ringkasan kata sendiri** yang cukup untuk memilih instrumen, memakainya, dan melaporkannya
dengan benar — bukan salinan instrumennya, karena sebagian besar tidak berlisensi terbuka.

> **Bukan pengganti formulir resmi.** Untuk lampiran submisi, unduh instrumen aslinya dari sumber
> resminya. Ringkasan di sini untuk kerja, bukan untuk dilampirkan.

---

## Aturan yang paling sering dilanggar, dan ini pintu masuknya

**Tiga instrumen yang paling relevan untuk bidang pendidikan dan ilmu sosial — MMAT, AXIS, dan
AMSTAR 2 — sama-sama melarang menghitung skor total.** Pengembangnya menyatakan itu eksplisit.

Ini bertabrakan dengan kebiasaan yang lazim di naskah Indonesia: memberi angka tiap butir,
menjumlahkannya, lalu menetapkan ambang "≥70% = kualitas tinggi". Dengan instrumen-instrumen itu,
prosedur tersebut **bukan penyederhanaan melainkan penyalahgunaan alat**, dan reviewer metodologis
mengenalinya.

Konsekuensinya untuk Tahap 7: gerbang "threshold eksklusi dijustifikasi" **hanya berlaku bila
instrumennya memang menghasilkan skor**. Bila tidak, yang dijustifikasi bukan ambang angka
melainkan **aturan keputusan berbasis butir** — misalnya "studi dikeluarkan bila kriteria
pengambilan sampel dan kriteria pengukuran keduanya tidak terpenuhi". Nyatakan aturannya di
Methods, apa pun bentuknya.

---

## Memilih instrumen — satu per desain, jangan dipaksakan lintas desain

| Desain studi | Instrumen | Catatan |
|---|---|---|
| Kualitatif (wawancara, etnografi, studi kasus) | **CASP Qualitative** atau **MMAT kategori 1** | CASP lebih rinci; MMAT lebih ringkas dan konsisten bila korpus campuran |
| RCT / eksperimen berrandomisasi | **RoB 2** | untuk pendidikan, eksperimen kelas berrandomisasi masuk sini |
| Kuasi-eksperimen / intervensi tanpa randomisasi | **ROBINS-I** | berat; untuk korpus non-klinis pertimbangkan MMAT kategori 3 |
| Kohort / kasus-kontrol | **NOS** — versi **berbeda** untuk masing-masing | jangan pakai versi kohort untuk kasus-kontrol |
| Survei / cross-sectional | **AXIS** | 20 butir; lazim dipakai untuk survei pendidikan |
| Deskriptif kuantitatif lain | **MMAT kategori 4** | |
| Mixed methods | **MMAT kategori 5** + kategori untai masing-masing | untai kualitatif dan kuantitatif **dinilai terpisah juga** |
| Review of reviews | **AMSTAR 2** | |
| Doktrinal / normatif | tidak ada instrumen yang berlaku | `reference/doctrinal-review.md` |

**Korpus campuran desain adalah keadaan lazim di bidang Anda.** Dua jalan: pakai MMAT untuk
seluruh korpus (satu alat, lima kategori, hasil sebanding), atau pakai instrumen spesifik per
desain lalu **stratifikasi pelaporan per instrumen** — jangan menggabungkan skor lintas
instrumen menjadi satu peringkat.

---

## Status lisensi — diverifikasi 12 Agustus 2026

Diperiksa lewat **field `license` metadata CrossRef**, bukan dari indeks pihak ketiga.

| Instrumen | Sitasi | Yang dikembalikan CrossRef | Boleh disalin verbatim? |
|---|---|---|---|
| **NOS** | Wells GA dkk., Ottawa Hospital Research Institute | — (bukan artikel ber-DOI) | **ya** — domain publik |
| **AMSTAR 2** | Shea BJ dkk. *BMJ* 2017;358:j4008. DOI [10.1136/bmj.j4008](https://doi.org/10.1136/bmj.j4008) — 8.197 sitasi | **hanya lisensi TDM BMJ** | **tidak** |
| **RoB 2** | Sterne JAC dkk. *BMJ* 2019;366:l4898 | **hanya lisensi TDM BMJ** | **tidak** |
| **ROBINS-I** | Sterne JAC dkk. *BMJ* 2016;355:i4919 | **hanya lisensi TDM BMJ** | **tidak** |
| **AXIS** | Downes MJ dkk. *BMJ Open* 2016;6(12):e011458. DOI [10.1136/bmjopen-2016-011458](https://doi.org/10.1136/bmjopen-2016-011458) — 1.903 sitasi | **tidak ada field `license`** | belum jelas — periksa halaman artikelnya |
| **MMAT 2018** | Hong QN dkk. *Education for Information* 2018;34(4):285–291. DOI [10.3233/efi-180221](https://doi.org/10.3233/efi-180221) — **3.170 sitasi** | **tidak ada field `license`** | belum jelas — instrumennya didistribusikan lewat situs MMAT sendiri; ikuti syarat di sana |
| **CASP** | Critical Appraisal Skills Programme, casp-uk.net | — (bukan artikel jurnal) | ikuti syarat di situsnya; sitir checklist beserta versi/tahunnya |

**Tiga instrumen BMJ — AMSTAR 2, RoB 2, ROBINS-I — hanya punya lisensi *text and data mining*.**
Itu bukan lisensi yang mengizinkan penerbitan ulang. Ringkasan kata sendiri saja.

Dua yang "belum jelas" berarti persis itu: CrossRef tidak mencatat lisensinya, **bukan** bahwa ia
tertutup — dan bukan pula bahwa ia terbuka. *BMJ Open* umumnya CC BY, tetapi metadata untuk artikel
AXIS ini tidak menyatakannya, jadi jangan mengandaikan.

> **Kenapa diperiksa sendiri.** Indeks lisensi milik repo pihak ketiga yang kami panen ternyata
> keliru untuk RoB 2 dan ROBINS-I — mengklaim CC BY untuk keduanya. Percayai metadata sumber, bukan
> ringkasan orang lain.

Untuk keperluan kerja, ringkasan kata sendiri di bawah sudah memadai dan tidak menyentuh soal
lisensi sama sekali.

---

## MMAT 2018 — ringkasan kerja

Alat tunggal untuk korpus campuran desain. Struktur: **2 pertanyaan penyaring**, lalu **5 kategori
desain, masing-masing 5 kriteria**. Jawaban tiap kriteria: **Ya / Tidak / Tidak dapat dinilai**.

**Dua pertanyaan penyaring** ditanyakan lebih dulu untuk semua studi — apakah ada pertanyaan riset
yang jelas, dan apakah data yang dikumpulkan memungkinkan pertanyaan itu dijawab. Bila keduanya
tidak, studi itu mungkin bukan riset empiris dan kategori mana pun tidak berlaku.

**Lima kategori:** (1) kualitatif; (2) RCT; (3) kuantitatif non-randomisasi; (4) kuantitatif
deskriptif; (5) mixed methods. Studi mixed methods dinilai kategori 5 **dan** kategori untai
kualitatif serta kuantitatifnya.

**Aturan pelaporan yang mengikat:** versi 2018 **tidak menganjurkan menghitung skor gabungan**.
Laporkan penilaian **per kriteria**, biasanya sebagai tabel studi × kriteria. Menyajikan
"MMAT 80%" mengabaikan instruksi pengembangnya.

---

## AXIS — ringkasan kerja

**20 butir** untuk studi cross-sectional, hasil panel Delphi 18 pakar internasional dengan ambang
konsensus **80%** — dipilih dari 39 komponen kandidat. Yang membuatnya cocok untuk survei
pendidikan: ia menilai **tiga hal sekaligus** — mutu desain, mutu pelaporan, dan risiko bias —
sementara instrumen lain hanya salah satunya.

Pengembangnya juga menerbitkan **dokumen penjelas** yang memperluas tiap pertanyaan dengan tafsiran
sederhana dan contoh konsep epidemiologis, ditujukan bagi pengguna non-pakar. **Unduh keduanya
bersamaan** — instrumen tanpa dokumen penjelasnya sulit diterapkan konsisten oleh dua penilai.

**Tidak menghasilkan skor ringkas.**

> Daftar 20 butirnya sengaja tidak direproduksi di sini: lisensinya belum jelas (lihat tabel di
> atas), dan meringkasnya dari ingatan berisiko keliru. Ambil daftarnya dari artikel aslinya.

---

## NOS — ringkasan kerja

Sistem bintang, **maksimum 9 bintang**, dan **versinya berbeda antara kohort dan kasus-kontrol**.
Memakai versi yang salah adalah kekeliruan yang mudah terlihat.

| Domain | Kohort | Kasus-kontrol | Bintang maks |
|---|---|---|---|
| **Selection** | 4 butir | 4 butir | 4 |
| **Comparability** | 1 butir | 1 butir | **2** |
| **Outcome / Exposure** | Outcome, 3 butir | Exposure, 3 butir | 3 |

Domain Comparability bernilai dua bintang dari satu butir — itu yang paling sering salah dihitung.

NOS **memang** menghasilkan angka, jadi ambang eksklusi berbasis skor sah di sini — tetapi
ambangnya tetap harus dijustifikasi dan diuji lewat sensitivity analysis, bukan diambil dari
kebiasaan. Perlakuan bintang sebagai skala interval juga tidak dibenarkan.

---

## AMSTAR 2 — ringkasan kerja

**16 butir**, dipakai hanya bila korpus Anda berupa **review**, bukan studi primer.

Yang membedakannya: **tujuh butir ditetapkan sebagai kritis**. Kegagalan pada butir kritis
menurunkan kepercayaan seluruh review, seberapa pun butir lain terpenuhi. Keluarannya adalah
**peringkat kepercayaan** — High / Moderate / Low / Critically low — **bukan skor**.

Pengembangnya menyatakan tegas bahwa AMSTAR 2 tidak dimaksudkan menghasilkan skor gabungan.
Peringkatnya ditentukan oleh **berapa banyak kelemahan kritis dan non-kritis**, bukan oleh
persentase butir yang lulus.

---

## RoB 2 dan ROBINS-I — kapan benar-benar perlu

Keduanya berat dan lahir dari epidemiologi klinis. Untuk bidang pendidikan, pakai **hanya bila
korpusnya memang eksperimen**.

**RoB 2** — lima domain: proses randomisasi; penyimpangan dari intervensi yang dimaksudkan; data
luaran yang hilang; pengukuran luaran; pemilihan hasil yang dilaporkan. Tiap domain punya
pertanyaan sinyal berkondisi, dan putusan domain digabung menjadi putusan keseluruhan
(Low / Some concerns / High). **Isi formulir resminya** untuk penilaian yang dilaporkan — pertanyaan
sinyalnya banyak dan sebagian bercabang.

**ROBINS-I** — tujuh domain, dengan **penilaian pra-asesmen** yang menuntut Anda merumuskan
"target trial" hipotetis lebih dulu. Tanpa langkah itu, sisanya kehilangan acuan. Berat untuk
korpus non-klinis; MMAT kategori 3 sering lebih sepadan.

Untuk keduanya, **jangan menyusun ringkasan sendiri lalu menyebutnya RoB 2** — sebut instrumen
yang benar-benar Anda jalankan.

---

## Bila tidak ada yang cocok

Aturannya sudah ada di SKILL.md dan tetap berlaku: cari dulu apakah instrumen yang sesuai sudah
ada di bidang tersebut; bila memang tidak ada, susun rubrik eksplisit dengan domain yang
dijustifikasi; nyatakan statusnya **tak tervalidasi** di Methods; lampirkan rubrik penuh sebagai
apendiks; dan rubrik buatan sendiri **tidak dipakai sebagai gerbang eksklusi keras**.

Untuk korpus doktrinal-normatif, domain yang lazim dan dapat dinilai dua penilai sudah didaftar di
`reference/doctrinal-review.md` — jangan menyusun ulang dari nol.

---

## Menyajikan hasilnya — pakai robvis, jangan buat sendiri

PRISMA item 18 menuntut penilaian risk of bias disajikan **per studi**, bukan sebagai proporsi
gabungan. Audit atas **24 SR/MA di satu jurnal radiologi** menemukan hanya **tujuh** yang
menyajikan hasil penilaian lengkap per studi — salah satu sebabnya, membuat gambarnya merepotkan.
Audit yang sama menemukan **24 dari 42 baris** checklist dipenuhi kurang dari 80% naskah, dan
registrasi protokol (item 24) serta ketersediaan data (item 27) dilaporkan **nol** naskah.

Angka itu dari satu jurnal dan satu bidang — perlakukan sebagai indikasi, bukan tingkat kepatuhan
umum. Disebut di sini sebagai hitungan mentah, bukan persentase, karena penyebutnya di naskah asli
adalah naskah yang benar-benar menilai risk of bias, bukan seluruh 24.

**Park HY, Suh CH, Woo S, Kim PH, Kim KW.** *Quality Reporting of Systematic Review and
Meta-Analysis According to PRISMA 2020 Guidelines: Results from Recently Published Papers in the
Korean Journal of Radiology.* **Korean Journal of Radiology.** 2022;23(3):355. DOI
[10.3348/kjr.2021.0808](https://doi.org/10.3348/kjr.2021.0808)

Bidang ini sudah punya alat bakunya:

**McGuinness LA, Higgins JPT.** *Risk-of-bias VISualization (robvis): An R package and Shiny web app
for visualizing risk-of-bias assessments.* **Research Synthesis Methods.** 2021;12(1):55–61. DOI
[10.1002/jrsm.1411](https://doi.org/10.1002/jrsm.1411) — **4.737 sitasi**.

Menghasilkan dua figur baku: **traffic light plot** (per studi × per domain — inilah yang memenuhi
item 18) dan **summary bar plot** (proporsi per domain). Alat yang didukung: **ROB2, ROBINS-I,
QUADAS-2, ROB1**.

**Tersedia sebagai aplikasi web**, jadi tidak perlu memasang R sama sekali. Bila R ada:

```r
library(robvis)
d <- read.csv("outputs/rob2.csv", check.names = FALSE)
ggplot2::ggsave("outputs/figures/rob2_traffic.svg", rob_traffic_light(d, tool = "ROB2"), width = 8, height = 4)
ggplot2::ggsave("outputs/figures/rob2_summary.svg", rob_summary(d, tool = "ROB2"), width = 8, height = 3)
```

Format CSV-nya: kolom `Study`, `D1`–`D5`, `Overall`, `Weight` (isi 1 bila tidak membobot).
Keluarannya **SVG**, sesuai konvensi figur Tahap 8.

**Satu jebakan yang perlu diketahui.** robvis hanya menerima tiga nilai untuk RoB 2: **Low /
Some concerns / High**. Nilai lain didiamkan — barisnya dibuang dengan peringatan yang mudah
terlewat. Ini bukan keterbatasan robvis, melainkan koreksi: **"No information" bukan putusan
domain yang sah di RoB 2.** NI adalah opsi jawaban untuk *pertanyaan sinyal*; putusan tingkat
domain selalu jatuh ke salah satu dari tiga. Bila tabel Anda memuat "No information" di tingkat
domain, yang tercampur adalah jawaban pertanyaan sinyal dengan putusan domain — perbaiki
penilaiannya, jangan akali gambarnya.

**NOS, MMAT, AXIS, dan AMSTAR 2 tidak didukung robvis.** Untuk keempatnya sajikan tabel studi ×
kriteria — dan ingat tiga di antaranya melarang skor gabungan, jadi tabel per butir memang bentuk
yang benar, bukan kompromi.

> **Catatan keputusan (12 Agu 2026).** Kami menguji `meta-rob2-plot` dari `aipoch/medical-research-skills`
> dan **tidak memakainya**. Skripnya berjalan dan hitungannya benar, tetapi: label domain 5 tertulis
> *"optional reporting"* — RoB 2 domain 5 adalah **selection of the reported result**, dan label itu
> akan muncul di sumbu figur naskah terbit; keluarannya PNG **150 DPI** saja, gagal memenuhi
> konvensi SVG-untuk-submisi maupun ambang 300 DPI kebanyakan jurnal; dan teks keluarannya hasil
> terjemahan mesin. Menulis penggantinya sendiri juga ditolak: robvis sudah tervalidasi, disitir
> 4.737 kali, dan gambarnya dikenali reviewer.

---

## Yang dilaporkan di manuskrip

- **Nama instrumen dan versinya**, disitir. "Kualitas dinilai dengan checklist standar" bukan
  pelaporan.
- **Berapa penilai, bekerja independen atau tidak, dan bagaimana ketidaksepakatan diselesaikan** —
  PRISMA 2020 item 11.
- **Penilaian per studi**, bukan hanya proporsi gabungan — item 18 PRISMA, dan butir yang paling
  sering gagal (lihat audit Park dkk. di bagian penyajian).
- **Sifat pemakaiannya** — eksklusi, atau stratifikasi dan pembobotan klaim — beserta alasannya.
- Bila instrumennya melarang skor gabungan, **jangan menyajikan persentase**.

---

**Catatan penyusunan.** Ringkasan di berkas ini ditulis dengan kata sendiri; tidak ada teks
instrumen yang disalin. Sitasi dan jumlah sitasi diverifikasi ke CrossRef pada 12 Agustus 2026.
Struktur "satu instrumen per desain, NOS dipisah kohort/kasus-kontrol" diadaptasi dari pola
`aipoch/medical-research-skills` (MIT) — polanya, bukan isinya; lihat NOTICE.md.

# Aturan Penulisan Manuskrip SLR (PRISMA 2020)

Dibaca saat memasuki Tahap 9. Berlaku untuk seluruh langkah penulisan sampai compile.

## Urutan penulisan terbalik

Methods → Results → Discussion → Future Research → Introduction → Conclusions →
References → Abstract → Title → audit + compile.

Alasannya: Methods mengunci seluruh angka; Results memakai angka itu apa adanya;
Introduction ditulis terakhir agar argumen gap selaras dengan temuan yang benar-benar
diperoleh, bukan dengan temuan yang diharapkan di awal.

Setiap section ditulis ke `outputs/manuscript/<section>.md`, direview user
**per paragraf** sebelum lanjut ke section berikutnya. Catat status di
`outputs/_provenance_log.md` (drafted / edited by author / approved by author /
claims verified against artifact files). File provenance ini **internal**, tidak
pernah menjadi supplementary material.

---

## Standar

PRISMA 2020 **27 item** — bukan PRISMA-ScR 22 item; keduanya standar berbeda.
Cochrane Handbook untuk metodologi sintesis.

---

## Bahasa sesuai jalur sintesis

Ikuti keputusan `synthesis_path_decision.md`. Ini bukan preferensi gaya — memakai
bahasa jalur yang salah adalah kesalahan metodologis.

**Jalur A (narrative/thematic)**
- Boleh: "synthesis indicates", "consistent finding across studies", "evidence suggests", rentang effect size individual yang disebut eksplisit sebagai indikatif
- Dilarang: "pooled effect", "d = X across studies", "overall effect size"

**Jalur B (meta-analysis)**
- Boleh: "pooled estimate", "[N] studies were meta-analyzed", "I² = X%"
- Dilarang: mencampur vote counting tanpa kualifikasi

---

## Framing Methods: nomenklatur peran

| Item PRISMA | Peran | Nilai κ |
|---|---|---|
| Item 8 — Selection process | Screener 1 dan Screener 2 | *inter-screener agreement* |
| Item 9 — Data collection | Extractor 1 dan Extractor 2 | *inter-extractor agreement* |
| Item 11 — Risk of bias | Rater 1 dan Rater 2 | *inter-rater agreement* |

Sebagian jurnal memakai "Reviewer 1/2" untuk item 8 — ikuti konvensi jurnal target dan
gunakan satu istilah secara konsisten di seluruh manuskrip.

Angka κ **diambil dari file artefak** (sheet kappa di `screening.xlsx` /
`extraction.xlsx`) — tidak pernah digenerate atau diestimasi.

## Pengungkapan perkakas dan pembantuan

Manuskrip melaporkan **prosedur**, dan prosedur dinyatakan dengan peran, bukan dengan
perkakas. Di seluruh Methods, Results, dan Discussion, yang muncul adalah Screener 1/2,
Extractor 1/2, Rater 1/2 — sebagaimana review yang dikerjakan tim mana pun.

Pengungkapan perkakas yang dipakai ditempatkan pada **satu section pernyataan** di akhir
manuskrip, sesuai kebijakan jurnal target. Isinya menyatakan apa yang benar-benar dipakai
dan pada tahap apa, serta penegasan bahwa keputusan akhir dan akurasi konten adalah
tanggung jawab penulis. Periksa kebijakan jurnal target sebelum menulisnya — cakupan yang
diminta berbeda-beda antar penerbit, dan sebagian meminta pengungkapan lebih rinci bila
perkakas dipakai pada tahap seleksi atau ekstraksi, bukan sekadar penyuntingan bahasa.

Yang **tidak** boleh masuk ke teks manuskrip di section mana pun: nama produk atau vendor
sebagai pengganti nama peran, dan kosakata kerja internal — "Pass 1/Pass 2", "blind
prompt", "sesi cowork", "batch screening", nama file kerja. Itu jejak proses, bukan
metode.

**Integritas angka kesepakatan — nama mengikuti konfigurasi.** Ambil namanya dari butir C
form kesepakatan, jangan dari kebiasaan:

| Konfigurasi | Istilah di Methods |
|---|---|
| Dua penilai manusia independen | *inter-screener / inter-extractor / inter-rater agreement* |
| Dua penilai manusia, sebagian korpus | idem, **dengan cakupan sampel dinyatakan** |
| Satu penilai | *intra-screener agreement* |
| Peneliti + pass AI, tiap baris dikonfirmasi manusia | ***human–AI agreement*** (atau *reviewer–LLM agreement*) |
| Satu proses dijalankan dua kali | bukan kesepakatan antar-penilai — **jangan dilaporkan sebagai κ antar-penilai** |

Baris keempat adalah konfigurasi yang **sah**, dan penamaannya yang tepat justru
menguntungkan: *human–AI agreement* adalah angka yang dapat dipertahankan, sementara
*inter-screener agreement* menyatakan ada dua penilai manusia independen — pernyataan yang
runtuh begitu editor meminta log per-screener.

Bila pass AI dipakai, Methods memuat tiga hal: perkakas dan versinya, tahap pemakaiannya,
dan penegasan bahwa keluaran AI diperlakukan sebagai usulan yang dikonfirmasi atau
dibatalkan peneliti per baris. Pengungkapannya mengikuti kebijakan jurnal target — sebagian
penerbit menuntut rincian lebih bila perkakas menyentuh tahap seleksi atau ekstraksi, bukan
sekadar penyuntingan bahasa.

**Paragraf Methods dan Limitations siap adaptasi, berikut rujukan yang wajib disitir, ada di
`reference/rujukan-ai-screening.md`.** Tiga hal dari sana yang paling menentukan diterima
tidaknya naskah: sitir pernyataan sikap bersama Cochrane/Campbell/JBI/CEE sebagai dasar
kepatuhan; **ikut sitir peringatan yang kritis terhadap AI** — reviewer yang mengenal
literatur ini akan mencarinya, dan ketiadaannya lebih mencurigakan daripada kehadirannya;
dan laporkan **κ Cohen bersama PABAK** karena korpus penyaringan sangat timpang sehingga satu
angka saja menyesatkan. Kalimat Limitations tentang kemungkinan kekeliruan berkorelasi antar
kedua pass **jangan dihapus** — kekhawatiran itu tidak hilang karena konfigurasinya sah, ia
berpindah menjadi keterbatasan yang diungkapkan.

Bila review dikerjakan satu screener, nyatakan terbuka di Methods dan Limitations —
termasuk cakupan verifikasi bila sebagian korpus diperiksa ulang secara independen.

Tanggung jawab akhir atas setiap klaim, angka, sitasi, dan interpretasi ada pada penulis.

## Batas peran antar-section (anti-leak)

Konten yang sama tidak boleh muncul di dua section dengan framing identik.

1. **Prior reviews** — Introduction: apa yang sudah dipetakan review terdahulu dan gap apa yang tersisa *sebelum* review ini. Discussion: bagaimana temuan review ini berdialog dengan review terdahulu. Jangan mengulang ringkasan yang sama.
2. **Gap** — Discussion limitations: keterbatasan saat ini beserta dampaknya. Future Research: agenda yang bisa ditindaklanjuti (RQ + metodologi). Pernyataan gap jangan identik di keduanya.
3. **Angka** — Methods: rubrik dan alur, belum ada N spesifik. Results: seluruh angka (N, κ, distribusi). Abstract: angka pilihan. N dan κ tidak boleh berbeda antar section.
4. **Implikasi** — Discussion: detail tiga jalur (riset/praktik/kebijakan). Conclusions: ringkasan 1–2 kalimat per jalur. Jangan paragraf identik.
5. **Klaim geografis** — cakupan geografis di Title wajib konsisten dengan Abstract, kriteria eligibility di Methods, pembahasan kejujuran geografis di Discussion, dan Limitations.
6. **Terminologi SLR vs ScR** — jangan pernah menulis "scoping review", "charting", atau "PCC" di manuskrip ini.

---

## Referensi: kontekstual, bukan checklist

Pilih rujukan yang benar-benar mendukung argumen spesifik di prose.

- Metodologi SLR: Page et al. (2021) PRISMA 2020; Higgins et al. (2023) Cochrane Handbook; Booth et al. / Petticrew & Roberts
- Tool RoB — sitasi **hanya yang dipakai**: RoB 2 (Sterne et al., 2019), ROBINS-I (Sterne et al., 2016), NOS (Wells et al.), AMSTAR 2 (Shea et al., 2017), MMAT (Hong et al., 2018)
- GRADE (Guyatt et al. dan seri lanjutannya) — bila ada penilaian certainty per outcome
- Justifikasi coverage Scopus (Mongeon & Paul-Hus, 2016; Martín-Martín et al., 2018) — hanya bila memang membuat argumen perbandingan coverage

Jangan block-cite beberapa rujukan sekaligus tanpa argumen unik per rujukan; reviewer
membacanya sebagai name-dropping. Verifikasi kelengkapan setiap sitasi sebelum submit —
metadata yang Anda ingat bisa usang.

---

## Audit akhir sebelum compile

Tulis seluruh temuan ke `outputs/coherence_audit.md`. Setiap subcek dilaporkan PASS atau
disertai daftar isu spesifik beserta usulan perbaikan.

**A. Repetisi** — kalimat nyaris identik di ≥2 section, khususnya prior reviews
(Intro vs Discussion), gap (Discussion vs Future Research), dan implikasi
(Discussion vs Conclusions).

**B. Terminologi** — konsistensi term kanonikal dari `pico_definitions.md`; tidak ada
istilah scoping review yang menyusup.

**C. Bahasa jalur** — Jalur A bebas dari bahasa pooled; Jalur B bebas dari vote counting
tanpa kualifikasi.

**D. Konsistensi nomenklatur peran** — pindai seluruh section (kecuali section pernyataan
di akhir) untuk kosakata proses yang seharusnya tidak muncul di teks metode: nama produk
atau vendor sebagai pengganti nama peran, "Pass 1/Pass 2", "blind prompt", "sesi cowork",
"batch screening", dan "inter-pass agreement". Pastikan peran disebut konsisten sebagai
Screener 1/2, Extractor 1/2, Rater 1/2 di Methods, Results, dan Abstract.

Lalu **cocokkan istilah kesepakatan dengan butir C form** (tabel di atas). Dua kegagalan
yang dicari: naskah menulis *inter-screener agreement* padahal form mencatat konfigurasi (c)
atau (d); atau naskah memakai pass AI tanpa section pengungkapan. Keduanya isu kritis —
yang pertama misrepresentasi metode, yang kedua pelanggaran kebijakan jurnal. Nama perkakas
tetap **tidak** boleh menggantikan nama peran di Methods; ia hidup di section pernyataan.

**E. Konsistensi numerik** — baca ulang file artefak, lalu pastikan tiap angka berikut
konsisten di Methods, Results, dan Abstract: total records identified; records screened
dan excluded; reports assessed for eligibility dan excluded with reasons; jumlah final
included; κ_TA, κ_FT, κ_extract, κ_rob; distribusi geografis; GRADE per outcome; pooled
estimate (Jalur B). **Setiap ketidakcocokan angka adalah isu kritis** — tandai dan tunjuk
file sumber yang benar.

**F. Kebocoran kosakata internal** — nama file (`outputs/`, `screening.xlsx`,
`extraction.xlsx`, nama sheet), isi provenance log, rujukan ke modul pelatihan, "draft v1",
"iteration 3", "pilot batch". Manuskrip harus berdiri sendiri.

**G. Suara workflow pelatihan** — "as per the training", "modul ini", "the workflow
document", "the cowork session". Ganti dengan prosa akademik bersuara penulis.

**H. Kalke bahasa Indonesia** (bila manuskrip berbahasa Inggris) — "It is known that…",
"It can be concluded…", "Many studies have…" sebagai pembuka generik, "On the other hand"
berlebihan, "Furthermore"/"Moreover" bertumpuk sebagai pengisi, struktur kalimat yang
mengikuti pola Indonesia. Ganti dengan konstruksi akademik Inggris yang wajar.

**I. Klaim geografis** — tarik pernyataan cakupan dari Title, Abstract, Introduction,
eligibility di Methods, Discussion, dan Limitations; setiap divergensi adalah isu.

**J. Hedging vs GRADE** — kekuatan bahasa klaim wajib setara level GRADE outcome-nya:
HIGH → bahasa tegas boleh; MODERATE → "likely", "probably"; LOW → "may", "suggests";
VERY LOW → "tentative", "uncertain". Setiap ketidakcocokan adalah isu.

**K. PRISMA 2020 27 item** — periksa satu per satu, tulis ke
`outputs/prisma_2020_checklist.md` dengan lokasi tiap item di manuskrip (section +
halaman/paragraf). Item yang tidak berlaku diberi keterangan alasannya.

**K2. PRISMA 2020 for Abstracts — 12 item, pass tersendiri.** Jalankan **setelah** K selesai,
atas Abstract saja, dengan `reference/checklist-abstrak.md`. **Laporkan skornya terpisah
berpenyebut 12**; jangan pernah dijumlahkan ke total checklist utama — melipatnya ke sana persis
cara dua belas item ini menghilang. Item 2 checklist utama tidak menilai apa pun, ia hanya
menunjuk ke instrumen ini. Dua item yang paling sering nol: kriteria eligibility dan registrasi.

**K3. SWiM 9 item — hanya bila jalur sintesisnya A.** Periksa dengan
`reference/swim-jalur-a.md`, tulis ke `outputs/swim_checklist.md`. Dipakai **bersama** PRISMA
2020, bukan menggantikannya. Yang paling sering gagal: item 3 — "narrative synthesis" disebut
tanpa prosedurnya dijelaskan dan dijustifikasi.

---

## Compile

Gabungkan section menjadi `outputs/manuscript_final.md`, lalu konversi ke
`manuscript_final.docx` (pandoc bila tersedia; alternatifnya `python-docx`). Sertakan
diagram alur PRISMA dengan angka yang diambil dari file artefak — jangan mengetik ulang
angka dari ingatan. Tutup dengan `pre_submission_checklist.md` dan `modul9_summary.md`.

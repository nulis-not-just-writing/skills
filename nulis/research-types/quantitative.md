# Riset Kuantitatif

Kata kunci mutu: **reproducibility** (APA JARS-Quant). Reviewer Q1 menilai apakah studi bisa direplikasi dari laporan Anda.

## Standar pelaporan
- **APA JARS-Quant (2018, Publication Manual ed. 7)** — menetapkan isi setiap section, bukan hanya Methods. Tabel per desain di apastyle.apa.org/jars.
- Per desain studi (EQUATOR Network): **CONSORT** (RCT/eksperimen acak), **STROBE** (observasional: kohort, case-control, cross-sectional), **PRISMA** (systematic review/meta-analisis), SQUIRE (quality improvement), CARE (case report). Jalankan checklist yang sesuai sebelum submit — banyak jurnal Q1 mewajibkan lampiran checklist-nya.
- **CROSS** (Sharma dkk. 2021) — studi berbasis **kuesioner/survei**, desain paling lazim di riset pendidikan dan sosial. Melengkapi STROBE, tidak menggantikannya: STROBE menangani logika epidemiologisnya, CROSS menangani hal khas instrumen survei — pengembangan & validasi kuesioner, cara administrasi, tingkat respons, dan bias nonrespons. **Ringkasan maksud tiap kelompok item: [`../reporting-guidelines/cross.md`](../reporting-guidelines/cross.md).**

  Untuk instrumen berbahasa Inggris yang diadaptasi ke konteks Indonesia, tiga hal wajib dilaporkan dan sering hilang sekaligus: izin dari pengembang asli, prosedur terjemahan maju-mundur, dan validasi ulang pada sampel Anda sendiri.

## Yang dinarasikan per section
- **Introduction**: variabel & hubungan yang diuji eksplisit; hipotesis bernomor (H1, H2) diturunkan dari teori/literatur, ditempatkan di akhir Introduction/kerangka teoretis.
- **Methods**: desain eksplisit (between/within, faktor & level); dasar ukuran sampel (power analysis a priori); operasionalisasi variabel + properti psikometrik instrumen (reliabilitas, validitas); prosedur cukup untuk replikasi; rencana analisis + penanganan missing data & outlier; praregistrasi bila ada.
- **Results**: statistik deskriptif dulu; asumsi uji dilaporkan; tiap uji: statistik, df, p eksak, **effect size + 95% CI** (p-value saja tidak cukup untuk Q1); hasil sesuai hipotesis maupun tidak — keduanya dilaporkan.
- **Discussion**: interpretasi berbasis magnitude (effect size), bukan hanya signifikansi; batas generalisasi mengikuti sampling; klaim kausal HANYA untuk desain eksperimental.

## Bahasa
- Presisi statistik: "significant" hanya dalam arti statistik; jangan "very significant".
- "Prove" dilarang — gunakan *support/consistent with/fail to support*.
- Angka: konsisten desimal, format APA/jurnal target; angka di teks = tabel.

## Red flags audit
- Hipotesis muncul tiba-tiba tanpa turunan teori (HARKing terindikasi)
- p-value tanpa effect size · sampel tanpa justifikasi ukuran
- Klaim kausal dari data korelasional
- Analisis di Results yang tidak diumumkan di Methods

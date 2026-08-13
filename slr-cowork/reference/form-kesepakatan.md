# Form Kesepakatan Kerja SLR

Diisi di **Tahap 1**, disimpan sebagai `outputs/kesepakatan_kerja.md`, dan menjadi rujukan
tunggal untuk seluruh tahap berikutnya.

## Mengapa form ini ada

Tanpa kesepakatan tertulis di awal, keputusan metodologis tetap harus diambil — hanya saja
diambil diam-diam di tengah jalan, oleh siapa pun yang kebetulan mengerjakan tahap itu,
dan sering baru ketahuan saat manuskrip ditulis. Jenis κ, ambang eksklusi, sistem
transliterasi, status sumber primer: semuanya menentukan angka yang masuk manuskrip, dan
semuanya mahal untuk diubah setelah screening berjalan.

**Cara mengisi.** Ajukan **nilai default** untuk setiap butir, jangan menyodorkan form
kosong. Peneliti mengonfirmasi atau mengoreksi. Butir yang benar-benar bergantung pada
kondisi proyek (komposisi screener, jenis korpus, jurnal target) ditanyakan; sisanya
cukup dikonfirmasi sekali.

**Status butir.** 🔒 = **terkunci** — mengubahnya setelah tahap terkait berjalan berarti
mengulang pekerjaan. ✎ = boleh ditetapkan menyusul, tetapi sebelum tahap yang memakainya.

---

## Template

```markdown
# Kesepakatan Kerja SLR
Tanggal: [YYYY-MM-DD] | Terakhir diubah: [YYYY-MM-DD]

## A. Identitas proyek
- Judul kerja:
- Bidang / sub-bidang:
- Folder kerja:
- Bahasa kerja (diskusi & artefak):            [default: Indonesia]
- Bahasa manuskrip:                            [default: Inggris]
- Jurnal target + tier:
- Gaya sitasi:                                 [APA 7 / Vancouver / sesuai jurnal]
- Kebijakan pengungkapan perkakas jurnal:      [dicek pada: ____]

## B. Jenis korpus & kerangka 🔒
- Jenis korpus:            [empiris / doktrinal-normatif / campuran]
- Bahasa korpus:
- Kerangka RQ:             [PICO / PECO / SPIDER / kerangka konseptual: ____]
- Kerangka sintesis:       [TCCM / ADO / lain: ____]
- Registrasi protokol:     [PROSPERO / OSF / lainnya / tidak — alasan: ____]

> Korpus doktrinal-normatif → baca `reference/doctrinal-review.md` sebelum Tahap 2.

## C. Komposisi screener 🔒
- Screener 1:              [nama/peran] — cara keputusan dihasilkan:
- Screener 2:              [nama/peran] — cara keputusan dihasilkan:
- Arbiter (konflik):       [nama/peran]
- Kompetensi bahasa tiap screener terhadap korpus:

Uji independensi (ketiganya wajib YA agar κ boleh disebut *inter-screener agreement*):
- [ ] Keputusan dihasilkan sendiri-sendiri, tanpa melihat keputusan lain sebelum keduanya selesai
- [ ] Pola kesalahan tidak berkorelasi — sumber kekeliruan berbeda
- [ ] Ada penanggung jawab tiap keputusan yang dapat mempertahankannya

Konfigurasi yang dipilih — **menentukan nama angka kesepakatan**:
- [ ] (a) rekan penilai kedua untuk seluruh korpus → *inter-screener agreement*
- [ ] (b) verifikasi independen sampel [__]% oleh screener kedua → *inter-screener agreement* pada sampel itu
- [ ] (c) satu screener saja → *intra-screener agreement*; keterbatasan dinyatakan terbuka
- [ ] (d) perkakas AI sebagai pass kedua → ***human–AI agreement***

Bila (d) dipilih — ketiganya wajib tercentang:
- [ ] Perkakas + versi + tahap pemakaian dicatat: ______________________
- [ ] **Tiap baris** dikonfirmasi atau dibatalkan peneliti; keluaran AI adalah usulan, bukan keputusan
- [ ] Rencana pengungkapan di manuskrip sesuai kebijakan jurnal target: ______________________

> Nama angkanya mengikuti konfigurasi, bukan sebaliknya. (d) adalah jalur sah — yang tidak
> sah adalah menyebut hasilnya *inter-screener agreement*. Rujukan terbit yang
> membenarkannya, dua batas kerasnya, dan paragraf Methods siap adaptasi ada di
> `reference/rujukan-ai-screening.md`; **baca sebelum Tahap 5**.
>
> **(d) hanya berlaku untuk penyaringan (Tahap 5–6), tidak untuk quality assessment
> (Tahap 7).** Bukti kinerja AI pada penilaian risk of bias jauh lebih lemah — κ 0,06–0,39
> pada uji validasi empat model. Untuk Tahap 7 dengan satu penilai, pakai opsi (c).

## D. Parameter reliabilitas 🔒
- Jenis κ screening:       [Cohen unweighted — keputusan nominal include/exclude]
- Jenis κ QA:              [weighted linear — skala ordinal] / [Fleiss bila >2 penilai]
- Ambang agregat:          [κ ≥ 0.60]
- Ambang κ per kriteria:   [lihat catatan di bawah]
- Sampel kalibrasi screening: [20 record]
- Sampel kalibrasi QA:     [20% studi atau 5 studi, mana yang lebih besar]
- Verifikasi silang ekstraksi: [20% entri]
- Definisi "kesalahan" ekstraksi:
  - Field faktual (tahun, N, desain) → error rate: [selisih nilai]
  - Field naratif (rumusan, argumen) → κ interpretatif: [kesesuaian makna, bukan kesamaan kata]

## E. Quality assessment ✎ (tetapkan sebelum Tahap 7 — pilih dari `reference/instrumen-qa.md`)
- Instrumen per stratum:
  - Stratum [__] (n=[__]): [instrumen + versi] — [tervalidasi / disusun sendiri]
- Instrumen ini menghasilkan skor?  [ya — NOS] / [**tidak** — MMAT, AXIS, AMSTAR 2]
- Sifat:                   [exclusionary / stratifikasi + pembobotan] — alasan:
- **Aturan keputusan** + justifikasi:
  - bila berskor → ambang: [____] beserta alasannya
  - bila tak berskor → aturan berbasis butir: [mis. "dikeluarkan bila kriteria __ dan __ keduanya gagal"]

> Instrumen yang **melarang skor gabungan** tidak boleh diberi ambang persentase. Menyajikan
> "MMAT 80%" atau "AMSTAR 2 = 12/16" mengabaikan instruksi pengembangnya dan terbaca reviewer.
- Bila instrumen disusun sendiri: [ ] dicari dulu instrumen tervalidasi  [ ] dilampirkan penuh sebagai apendiks  [ ] status tak-tervalidasi dinyatakan di Methods

## F. Kepercayaan bukti ✎ (tetapkan sebelum Tahap 8)
- Metode sintesis kualitatif: [tidak berlaku / thematic synthesis (Thomas & Harden 2008) / meta-ethnography / framework synthesis / meta-aggregation JBI / critical interpretive synthesis] — alasan:
- Instrumen:               [GRADE per outcome / GRADE-CERQual / rubrik warrant per RQ]
- Pemetaan hedging:        [HIGH → tegas; MODERATE → likely/probably; LOW → may/suggests; VERY LOW → tentative]

> Baris pertama diisi **hanya bila studi yang disintesis kualitatif**. Metode QES yang dipilih wajib
> **dinamai dan disitir di Methods**, dan prosedurnya benar-benar dijalankan — lihat
> `reference/sintesis-kualitatif.md`. Menyusun temuan studi *kuantitatif* ke dalam tema bukan
> thematic synthesis; itu narrative synthesis yang diorganisasi tematik, dan barisnya diisi "tidak berlaku".

## G. Kriteria eligibility — NILAI, bukan hanya nama 🔒 (wajib terisi sebelum Tahap 3)
- Rentang tahun:           [dari ____ sampai tanggal search] — justifikasi 3 lapis:
- Jenis dokumen:           [artikel jurnal peer-review / prosiding / tesis / buku / bab buku]
- Bahasa literatur yang di-screening:
- Bahasa sumber primer yang dianalisis:   [boleh berbeda dari baris di atas]
- Yurisdiksi / wilayah:
- Status peer-review:

### Legenda reason code eksklusi 🔒 (wajib terisi sebelum Tahap 5)

| Kode | Alasan | Tahap |
|---|---|---|
| E1 | [mis. Bukan populasi sasaran] | judul-abstrak |
| E2 | [mis. Bukan intervensi/konstruk sasaran] | judul-abstrak |
| E3 | [mis. Jenis dokumen tidak sesuai] | judul-abstrak |
| F1 | [mis. Tidak ada luaran/temuan yang dapat diekstraksi] | teks lengkap |
| F2 | [mis. Populasi sasaran tidak dapat dipisahkan] | teks lengkap |
| F3 | [mis. Teks lengkap tidak diperoleh] | teks lengkap |

> Kriteria faktual tanpa **nilai** tidak dapat disaring maupun dihitung κ-nya. Menyebut
> "rentang tahun" sebagai kriteria tanpa menetapkan tahunnya membuat Tahap 5 berhenti.
>
> **Legenda kode wajib tinggal di sini, bukan hanya di dalam `screening.xlsx`.** Gerbang
> validitas reason code (Tahap 6) membandingkan kode yang dipakai terhadap legenda yang
> terdaftar **di protokol**; bila berkas ini tidak memuatnya, skrip tidak dapat menilai dan
> **diam** — melaporkan bersih padahal tidak memeriksa apa pun. Satu nomor kode = satu makna,
> tetap sama dari judul-abstrak sampai teks lengkap.
>
> `F3` di atas adalah **reason code eksklusi** hanya bila teks lengkap benar-benar tidak
> diperoleh setelah seluruh jalur ditempuh. Pada diagram PRISMA, *reports not retrieved*
> adalah **kotak tersendiri**, bukan alasan eksklusi — jangan tertukar saat menghitung.

## H. Pencarian & sumber ✎ (tetapkan di Tahap 3)
- Database + justifikasi:
- Tanggal search:          [YYYY-MM-DD]
- Update policy:           [re-run bila > __ bulan sebelum submit]
- Penelusuran sitasi:      [backward + forward dari __ studi; metode: ____]
- Status sumber primer:    [masuk hitungan PRISMA / ditelusuri terpisah — lihat doctrinal-review.md]
- Prioritisasi penyaringan (*active learning*): [tidak dipakai / alat: ____ versi ____]
  - Aturan berhenti **ditetapkan di muka**:   [mis. SAFE (Boetje & van de Schoot 2024) / estimasi recall ≥__%]
  - Fase pengaman pasca-berhenti:             [penyaringan ulang rekaman tak berlabel / rekaman tereksklusi / tidak ada]

> Prioritisasi **bukan** pengganti screener kedua — ia mengatur urutan, bukan menyediakan
> penilaian independen. Bila hanya prioritisasi yang dipakai, komposisi screener tetap (c).
> Berhenti "ketika kurvanya sudah datar" bukan aturan; tetapkan dan namai sebelum mulai.
> Detail dan cara melaporkannya di `reference/rujukan-ai-screening.md` §5.

## I. Konvensi penulisan
- Nomenklatur peran:       [Screener 1/2, Extractor 1/2, Rater 1/2]
- Sistem transliterasi:    [IJMES / Library of Congress / tidak relevan]
- Terminologi kanonikal:   [diisi dari Tahap 2 → pico_definitions.md / kerangka_konseptual.md]

## Catatan perubahan
| Tanggal | Butir | Dari → Menjadi | Alasan | Dampak pada pekerjaan yang sudah jalan |
|---|---|---|---|---|
```

---

## Ambang κ per kriteria — cara menetapkannya

Ini butir yang paling sering diabaikan dan paling sering menimbulkan masalah, karena satu
angka agregat **menyembunyikan kriteria mana yang menanggung ketidaksepakatan**. Screening
dengan κ keseluruhan 0,72 bisa saja berisi satu kriteria dengan κ 0,31 — dan justru
kriteria itu yang akan ditanyakan reviewer.

Bedakan dua jenis keputusan, dan tetapkan ambangnya terpisah:

| Jenis | Contoh | Ambang | Bila gagal |
|---|---|---|---|
| **Faktual** — dapat diverifikasi dari teks | rentang tahun, jenis dokumen, desain studi, negara | κ ≥ 0.60; nilai rendah berarti kriteria salah dibaca, bukan sulit | Perjelas rumusannya; ini kesalahan operasional, bukan perbedaan tafsir |
| **Interpretatif** — menuntut penilaian | apakah studi ini benar-benar memakai konstruk X, bukan sekadar menyebut istilahnya | ambang dijustifikasi terpisah dan dinyatakan di Methods; κ ≥ 0.60 tetap target, tetapi 0.41–0.60 dapat diterima **bila** disertai dokumentasi naratif atas sengketa dan aturan resolusinya | Pertajam operational definition dengan *edge case* terdokumentasi; bila tetap rendah, itu temuan tentang kaburnya konstruk di literatur — laporkan, jangan sembunyikan |

**Aturan praktis:** hitung κ agregat *dan* κ per kriteria. Kriteria dengan κ terendah
menunjukkan rubrik mana yang harus dipertajam — itu informasi yang paling berguna dari
seluruh perhitungan, dan hilang bila hanya melaporkan satu angka.

Untuk korpus doktrinal-normatif, mayoritas keputusan bersifat interpretatif. Nyatakan itu
di Methods sebagai karakteristik korpus, bukan sebagai kelemahan yang perlu ditutupi.

---

## Aturan pemakaian

**Setiap tahap membaca form ini lebih dulu.** Bila sebuah butir sudah ditetapkan, pakai —
jangan tanyakan ulang dan jangan improvisasi nilai lain. Bila butir yang dibutuhkan masih
kosong, tetapkan bersama peneliti **sekarang**, isikan ke form, baru lanjutkan.

**Butir bertenggat ditegakkan, bukan sekadar dicatat.** Butir yang menyebut tenggat tahap
(misalnya "arbiter ditetapkan sebelum Tahap 5", "nilai kriteria eligibility sebelum
Tahap 3") diperiksa **di awal tahap itu**. Bila masih kosong, tahap tidak dibuka sebelum
diisi — tenggat yang hanya tertulis di form dan tidak pernah diperiksa sama saja dengan
tidak ada.

**Form harus konsisten dengan folder tempatnya berada.** Bila form merujuk artefak yang
tidak ada di folder kerja, jangan diam-diam melanjutkan: periksa apakah ada salinan di
tempat lain, laporkan kemungkinan dua jalur artefak yang berbeda, dan minta peneliti
memastikan mana yang berlaku. File definisi yang hilang — kerangka konseptual, operational
definition — berdampak sampai Tahap 5 meski bukan data record-level.

**Perubahan dicatat, tidak ditimpa diam-diam.** Butir 🔒 yang berubah setelah tahap
terkait berjalan wajib masuk tabel Catatan perubahan beserta dampaknya — misalnya
mengubah ambang eksklusi QA setelah penilaian selesai berarti komposisi korpus berubah dan
sensitivity analysis harus diulang.

**Form ini dokumen internal**, bukan supplementary material. Isinya menjadi bahan Methods,
tetapi tidak dilampirkan apa adanya.

---

## Bila form dibuat menyusul

Proyek yang sudah berjalan tanpa form tetap membutuhkannya — tetapi form yang disusun
belakangan **bukan kesepakatan, melainkan rekonstruksi**, dan perbedaan itu harus terlihat
di dokumennya. Form yang tampak resmi untuk keputusan yang tidak pernah benar-benar
disepakati siapa pun adalah risiko yang diciptakan oleh form itu sendiri.

Aturannya:

- Beri tanda tegas di kepala file: **DRAF REKONSTRUKSI — BELUM DIKONFIRMASI**, beserta tanggal penyusunan dan tahap proyek saat itu.
- **Label sumber tiap butir**: `[terekam]` bila diambil dari artefak yang ada, `[rekonstruksi]` bila disimpulkan dari hasil kerja, `[usulan]` bila ditetapkan sekarang dan menunggu konfirmasi, `[kosong]` bila memang belum ada.
- Butir `[rekonstruksi]` dan `[usulan]` **tidak boleh dipakai untuk membenarkan angka yang sudah terlanjur dilaporkan**. Bila komposisi screener tidak pernah tercatat, κ yang sudah ada tidak menjadi *inter-screener agreement* hanya karena form belakangan menuliskannya begitu.
- Minta peneliti mengonfirmasi butir per butir sebelum status draf dicabut. Konfirmasi menyeluruh sekali klik justru menghapus manfaat pelabelan di atas.

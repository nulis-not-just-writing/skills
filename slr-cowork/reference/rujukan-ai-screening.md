# Rujukan untuk pemakaian AI dalam penyaringan

Dibaca **saat butir C form kesepakatan menetapkan opsi (d)** — peneliti sebagai pass pertama,
perkakas AI sebagai pass kedua — dan dibaca ulang di Tahap 9 saat menulis Methods dan
Limitations.

Berkas ini memuat rujukan terbit yang membenarkan konfigurasi itu, paragraf Methods siap
adaptasi, dan dua batas yang tidak boleh dilewati. Seluruh metadata diverifikasi ke CrossRef
pada **12 Agustus 2026**; semuanya `journal-article`, bukan preprint.

---

## 1. Otoritas kebijakan — sitir ini lebih dulu

**Flemyng E, Noel-Storr A, Macura B, Gartlehner G, Thomas J, Meerpohl JJ, Jordan Z, Minx J,
Eisele-Metzger A, Hamel C, Jemioło P, Porritt K, Grainger M.** *Position Statement on
Artificial Intelligence (AI) Use in Evidence Synthesis Across Cochrane, the Campbell
Collaboration, JBI, and the Collaboration for Environmental Evidence 2025.* **Campbell
Systematic Reviews.** 2025;21(4). DOI [10.1002/cl2.70074](https://doi.org/10.1002/cl2.70074)

Empat organisasi sintesis bukti terbesar menyatakan bersama bahwa AI **boleh** dipakai. Tiga
butirnya menjadi dasar langsung opsi (d):

> - "Evidence synthesists are **ultimately responsible** for their evidence synthesis, including
>   the decision to use artificial intelligence (AI) and automation…"
> - "AI and automation in evidence synthesis should be used **with human oversight**."
> - "Any use of AI or automation that **makes or suggests judgements** should be **fully and
>   transparently reported** in the evidence synthesis report."

**Untuk bidang pendidikan dan ilmu sosial, sitir versi Campbell** — Campbell Collaboration
adalah rumah sintesis bukti bidang tersebut, dan reviewer Anda mengenalinya. Terbit serentak di:

- JBI Evidence Synthesis — DOI [10.11124/jbies-25-00480](https://doi.org/10.11124/jbies-25-00480)
- Environmental Evidence — DOI [10.1186/s13750-025-00374-5](https://doi.org/10.1186/s13750-025-00374-5)

Pelengkap untuk rapid review: **Gartlehner G, dkk.** *Responsible Integration of Artificial
Intelligence in Rapid Reviews: A Position Statement From the Cochrane Rapid Reviews Methods
Group.* Cochrane Evidence Synthesis and Methods. 2025;3(6). DOI
[10.1002/cesm.70063](https://doi.org/10.1002/cesm.70063)

---

## 2. Bukti kinerja agregat

| Rujukan | Jurnal | Angka kunci |
|---|---|---|
| **Laignelot F, Martin GL, Ossman M, Pingeon O, Boubaker A, Picovschi E, Kim J, Tannier X, Cohen JF, Dechartres A.** *Large language models show promising performance for some systematic review tasks but call for cautious implementation: a systematic review.* 2026;194:112221. DOI [10.1016/j.jclinepi.2026.112221](https://doi.org/10.1016/j.jclinepi.2026.112221) | Journal of Clinical Epidemiology | 63 studi, 148 penilaian kinerja. Penyaringan judul-abstrak: median **PPA 0,92** (IQR 0,69–0,98), **NPA 0,89** (0,72–0,95). Teks lengkap: PPA 0,93, NPA 0,92. Model pasca-GPT-4 lebih baik |
| **Shankar R, Goh Z, Xu Q.** *Techniques, Performance, and Feasibility of Natural Language Processing for Abstract Screening in Evidence Synthesis: A Systematic Review.* 2026;22(3). DOI [10.1177/18911803261469813](https://doi.org/10.1177/18911803261469813) | Campbell Systematic Reviews | 19 studi; sebagian besar **>90% recall**, penghematan beban **13–96%**. Memuat justifikasi dual screening: *"single reviewers can miss 5–13% of relevant studies"* |

Rujukan kedua ada di jurnal bidang pendidikan/ilmu sosial — pakai bila reviewer menuntut bukti
dari bidang sendiri, bukan dari kedokteran.

---

## 3. Angka kesepakatan langsung

**Guo E, Gupta M, Deng J, Park Y-J, Paget M, Naugler C.** *Automated Paper Screening for Clinical
Reviews Using Large Language Models: Data Analysis Study.* **Journal of Medical Internet
Research.** 2024;26:e48996. DOI [10.2196/48996](https://doi.org/10.2196/48996)

Lebih dari 24.000 judul-abstrak lintas enam review:

| Perbandingan | Nilai |
|---|---|
| Antara dua penyaring **manusia** independen | κ = **0,46** |
| Antara **LLM dan konsensus manusia** (PABAK) | κ = **0,96** |
| Akurasi keseluruhan | 0,91 |

Kesepakatan manusia–manusia lebih rendah daripada manusia–AI. Ini **bukan** bukti AI lebih benar
— konsensus manusia adalah standar rujukannya, jadi angka kedua sebagian tautologis. Yang
dipatahkannya adalah asumsi bahwa dua manusia otomatis lebih andal.

**Oami T, Okada Y, Nakada T.** *Performance of a Large Language Model in Screening Citations.*
**JAMA Network Open.** 2024;7(7):e2420496. DOI
[10.1001/jamanetworkopen.2024.20496](https://doi.org/10.1001/jamanetworkopen.2024.20496)

Sensitivitas **0,75 → 0,91 setelah prompt diperbaiki**, spesifisitas tetap 0,98–0,99. Waktu 1,3
vs 17,2 menit per 100 studi. Pakai untuk menunjukkan bahwa **kualitas prompt adalah variabel
metodologis**, bukan detail teknis — dan karena itu prompt wajib dilampirkan.

**Sciurti A, dkk.** *Compact large language models for title and abstract screening in systematic
reviews.* **Research Synthesis Methods.** 2025;17(2):332–347. DOI
[10.1017/rsm.2025.10044](https://doi.org/10.1017/rsm.2025.10044)

Model kompak, sebagian jalan **lokal dan gratis**; biaya API $0,14–1,93 per review. Sensitivitas
tinggi, presisi rendah (<10%). Relevan bila anggaran atau kerahasiaan data jadi pertimbangan.

---

## 4. Peringatan — wajib disitir, bukan disembunyikan

**Khraisha Q, Put S, Kappenberg J, Warraitch A, Hadfield K.** *Can large language models replace
humans in systematic reviews? Evaluating GPT-4's efficacy in screening and extracting data from
peer-reviewed and grey literature in multiple languages.* **Research Synthesis Methods.**
2024;15(4):616–626. DOI [10.1002/jrsm.1715](https://doi.org/10.1002/jrsm.1715)

Paling banyak disitir di topik ini. Pendekatan ***human-out-of-the-loop***: akurasi GPT-4 tampak
setara manusia, lalu **runtuh setelah dikoreksi terhadap kesepakatan-karena-kebetulan dan
ketimpangan dataset**.

Menyitirnya **menguatkan** posisi Anda, bukan melemahkan: yang gagal di sana adalah konfigurasi
tanpa manusia dalam lingkaran — persis yang opsi (d) larang. Reviewer yang tahu paper ini akan
mencarinya di daftar pustaka Anda; ketiadaannya lebih mencurigakan daripada kehadirannya.

**Nyrhi L, Ponkilainen V, Laaksonen J, Kuikka L, Paljakka L, Karjalainen T, Mattila VM,
Kuitunen I.** *Large language models for risk-of-bias assessment in randomised clinical trials —
a comparative validation study.* **eBioMedicine.** 2026;126:106238. DOI
[10.1016/j.ebiom.2026.106238](https://doi.org/10.1016/j.ebiom.2026.106238)

Empat LLM untuk RoB: κ hanya **0,06–0,39**; model konsisten *over-flagging*. Kesimpulan penulis:
tidak ada yang cukup andal untuk penilaian RoB otonom.

**Untuk ekstraksi data**, peringatan setara: **Bianchi J, Hirt J, Vogt M, Vetsch J.** *Data
Extractions Using a Large Language Model (Elicit) and Human Reviewers in Randomized Controlled
Trials.* Cochrane Evidence Synthesis and Methods. 2025;3(4). DOI
[10.1002/cesm.70033](https://doi.org/10.1002/cesm.70033) — hanya 20,7% ekstraksi setara manusia,
45,7% "sebagian setara"; verifikasi manusia dinyatakan perlu.

---

## 5. Konfigurasi ketiga: prioritisasi penyaringan (*active learning*)

**Ini bukan opsi (d), dan konsekuensinya berbeda.** Opsi (d) menjalankan pass kedua atas
**seluruh** rekaman. Prioritisasi penyaringan — ASReview, SWIFT-Active Screener, EPPI-Reviewer —
bekerja lain: model **mengurutkan** rekaman menurut kemungkinan relevansi, peneliti menyaring dari
atas, lalu **berhenti sebelum semuanya dilihat**. Sisa rekaman tidak pernah dinilai siapa pun.

Karena itu prioritisasi mengubah arti kotak *records screened* pada diagram PRISMA, dan itu bukan
tafsiran saya — pengembang ASReview sendiri yang menyatakannya:

> "**the PRISMA guidelines are not sufficient for reporting the screening phase in a reproducible
> manner**" — Lombaers, de Bruin & van de Schoot (2024)

**Lombaers P, de Bruin J, van de Schoot R.** *Reproducibility and Data Storage for Active
Learning-Aided Systematic Reviews.* **Applied Sciences.** 2024;14(9):3842. DOI
[10.3390/app14093842](https://doi.org/10.3390/app14093842) — memuat **RDAL Checklist**, daftar
periksa apa yang harus disimpan agar penyaringan berbasis active learning dapat direproduksi.

### Aturan pertama: aturan berhenti ditetapkan **di muka** dan dinamai

Berhenti "ketika kurvanya sudah datar" bukan metode; itu kesan. Rujukan bakunya:

**Boetje J, van de Schoot R.** *The SAFE procedure: a practical stopping heuristic for active
learning-based screening in systematic reviews and meta-analyses.* **Systematic Reviews.**
2024;13(1). DOI [10.1186/s13643-024-02502-7](https://doi.org/10.1186/s13643-024-02502-7)
— 112 sitasi.

Kesimpulan utamanya: **satu aturan berhenti saja tidak memadai**; SAFE menggabungkan beberapa
heuristik justru supaya tidak berhenti terlalu awal. Tetapkan aturannya di butir H form
kesepakatan **sebelum** penyaringan dimulai, bukan sesudah melihat hasilnya.

### Aturan kedua: yang tidak pernah dilihat tetap dilaporkan

Di sinilah PRISMA 2020 kurang. Templat diagramnya punya kotak *"records marked as ineligible by
automation tools"* di fase identifikasi — tetapi itu untuk rekaman yang **dinilai** alat otomatis
dan ditolak, sementara pada prioritisasi rekaman sisa **tidak dinilai sama sekali**. Menaruhnya di
kotak itu mengklaim penilaian yang tidak terjadi; menghilangkannya membuat kaskade tidak
rekonsiliasi.

Yang dikerjakan review terbitan sampai ada pedoman resmi: **laporkan keduanya secara eksplisit
di prosa Methods**, dan pilih satu perlakuan diagram lalu nyatakan pilihan itu di legenda figur.
Empat angka yang wajib muncul:

| Angka | Contoh dari review terbitan |
|---|---|
| Rekaman teridentifikasi | 32.006 |
| **Rekaman yang benar-benar disaring manusia** | 8.533 |
| **Aturan berhenti + estimasi recall saat berhenti** | berhenti saat alat memperkirakan **≥94% recall** |
| Studi dimasukkan | 1.684 |

Contoh itu dari **Jäggi L, Falgas Bague I, Wey H, Rüfli D, Viglietti PG, Fuhrimann S.** *Unequal
harvests: AI-assisted evidence map of trends and gaps in global farmer health research along SDG 3
priorities.* **BMJ Open.** 2026;16(6):e110537. DOI
[10.1136/bmjopen-2025-110537](https://doi.org/10.1136/bmjopen-2025-110537) — kalimat Methods-nya
layak ditiru polanya apa adanya.

Contoh kedua yang memakai SAFE secara berfase: **Thomas G, dkk.** *Harnessing artificial
intelligence for scalable evidence synthesis in reviews.* DIGITAL HEALTH. 2026. DOI
[10.1177/20552076261455158](https://doi.org/10.1177/20552076261455158) — 28.957 rekaman, hanya 18%
disaring manual, dengan **fase penyaringan ulang atas rekaman tak berlabel dan rekaman
tereksklusi** sebagai pengaman. Fase pengaman itu yang membuat klaim recall-nya dapat
dipertahankan.

### Aturan ketiga: prioritisasi bukan pengganti screener kedua

Prioritisasi menghemat beban; ia **tidak** menyediakan penilaian independen kedua. Keduanya
menjawab pertanyaan berbeda, dan sebuah review bisa memakai keduanya sekaligus — prioritisasi
untuk urutan, opsi (d) untuk pass kedua. Bila hanya prioritisasi yang dipakai, komposisi
screener tetap (c), dan angkanya tetap *intra-screener agreement*.

### Kapan ini sepadan

Prioritisasi berbayar-usaha pada korpus **puluhan ribu rekaman**. Pada korpus beberapa ratus —
ukuran lazim SLR bidang pendidikan dan kajian keislaman — biaya menyiapkan seed, menetapkan
aturan berhenti, mendokumentasikan iterasi model, dan menjalankan fase pengaman **melebihi**
penghematannya, sementara risiko kehilangan studi relevan tetap ada. Untuk korpus sebesar itu,
saring seluruhnya; opsi (d) sudah cukup.

---

## 6. Dua batas keras

**Batas 1 — AI untuk penyaringan, bukan untuk penilaian kualitas.** Bukti kinerja penyaringan
memadai (PPA 0,92); bukti kinerja RoB tidak (κ 0,06–0,39). Opsi (d) **hanya berlaku untuk
Tahap 5–6**. Quality assessment Tahap 7 tetap menuntut penilai manusia; bila hanya satu tersedia,
pakai opsi (c) dan laporkan sebagai keterbatasan.

**Batas 2 — laporkan κ Cohen bersama PABAK.** Korpus penyaringan sangat timpang: Oami memasukkan
8 dari 5.634 rekaman. Pada rasio seperti itu κ Cohen bisa rendah meski kesepakatannya hampir
sempurna — dan itulah distorsi yang Khraisha peringatkan. Guo memakai **PABAK**
(*prevalence-adjusted bias-adjusted kappa*) justru karena ini. Laporkan **keduanya, ditambah
sensitivitas dan spesifisitas terpisah**; satu angka tunggal pada data setimpang ini menyesatkan
ke dua arah sekaligus.

---

## 7. Paragraf Methods siap adaptasi

Ganti setiap `[...]`. Jangan pakai apa adanya — angka dan nama harus dari proyek Anda.

> Title and abstract screening was conducted in two passes. `[Researcher initials]` screened all
> records as the first pass. `[Model name and version, e.g. Claude Opus 4.5]` was then used as a
> documented second pass, receiving the same eligibility criteria (Appendix `[X]`, full prompt in
> Appendix `[Y]`) and returning an include/exclude suggestion with a stated reason for each
> record. Model outputs were treated as suggestions rather than decisions: `[Researcher initials]`
> independently confirmed or overturned every record, and `[n]` suggestions were overturned.
> Because a second independent human screener was not available, agreement between the two passes
> is reported as **human–AI agreement** rather than inter-screener agreement. Given the imbalance
> of the screening dataset (`[k]` included of `[N]` screened), we report Cohen's κ alongside the
> prevalence-adjusted bias-adjusted κ (PABAK), with sensitivity and specificity calculated
> against the final decisions (Guo et al., 2024). Our use of AI follows the RAISE recommendations
> endorsed by Cochrane, the Campbell Collaboration, JBI, and the Collaboration for Environmental
> Evidence (Flemyng et al., 2025): the tool was used under human oversight, and every point at
> which it made or suggested a judgement is reported here. No AI tool was used for quality
> appraisal or risk-of-bias assessment, where current models show poor agreement with human
> raters (Nyrhi et al., 2026).

## 8. Paragraf Limitations siap adaptasi

> Screening relied on a single human screener supported by a documented AI second pass rather
> than two independent human screeners. Evidence on AI-assisted screening is mixed: agreement
> approaching or exceeding that between human screeners has been reported (Guo et al., 2024;
> Oami et al., 2024), and a recent synthesis found median positive percent agreement of 0.92 for
> title and abstract screening (Laignelot et al., 2026). However, apparent accuracy has also been
> shown to fall substantially once chance agreement and dataset imbalance are accounted for,
> particularly where the model operates without human verification (Khraisha et al., 2024). We
> retained human decision authority over every record, but the two passes are not fully
> independent in the sense required for inter-rater statistics, and the possibility of correlated
> error between them cannot be excluded.

**Kalimat terakhir itu jangan dihapus.** Kekhawatiran kekeliruan berkorelasi tidak hilang karena
konfigurasinya sah — ia berpindah dari alasan menolak menjadi keterbatasan yang diungkapkan.
Reviewer yang menemukannya sendiri jauh lebih merugikan daripada Anda yang menyebutkannya lebih
dulu.

---

## Yang sengaja tidak dimasukkan

**Parmar M, dkk.** *Collaborative large language models (LLMs) are all you need for screening in
systematic reviews* — angkanya menarik (recall 98,5%, WSS 63,5% lewat kolaborasi GPT-4 +
Claude-3-Sonnet), tetapi CrossRef menandainya `posted-content` di openRxiv. **Preprint, belum
terbit.** Boleh dipantau; jangan disitir sebagai bukti terbit sampai statusnya berubah.

---

**Catatan kuartil.** Kuartil SJR/JCR **belum diverifikasi** dan bergantung pada kategori bidang
serta tahun — jurnal yang Q1 di "Medicine" belum tentu Q1 di "Education". Yang diverifikasi di
sini hanya status terbit, volume, dan halaman. Periksa kuartilnya di Scimago untuk kategori yang
Anda tuju sebelum menyebutnya di proposal atau laporan.

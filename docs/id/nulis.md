# nulis — struktur artikel

*[Read this in English](../nulis.md)*

**v1.4.0** · [unduh zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/nulis-1.4.0.zip)

Coaching menulis artikel jurnal Q1 berbasis *genre analysis*. Bukan mesin drafting borongan —
ia membimbing per **move**, menuntut bukti untuk tiap klaim, dan mengalibrasi bahasa sesuai bidang.

## Untuk apa sebenarnya skill ini

Tiga keadaan yang paling sering membawa orang ke sini.

### 1. Data sudah ada, artikelnya belum berbentuk

Anda punya hasil analisis, tabel, mungkin beberapa figur — tetapi belum tahu mana yang jadi
Introduction dan mana yang jadi Discussion.

> *"Saya punya data survei 340 guru SMK tentang efikasi diri. Bantu saya menyusunnya jadi
> artikel."*

Yang terjadi: skill menanyakan **bidang** dan **jenis riset** Anda lebih dulu — bukan basa-basi,
karena jawabannya menentukan konvensi mana yang dimuat. Lalu ia memetakan gap → RQ → desain →
hasil → kontribusi, **satu baris per RQ yang tembus lima section**. Baris itulah yang nanti
dipakai memeriksa apakah setiap pertanyaan benar-benar terjawab.

Yang **tidak** terjadi: ia tidak menulis Introduction lengkap dari udara kosong. Bila bahan
substantifnya belum ada, yang muncul adalah penanda `[SITASI]` dan `[DATA]` untuk Anda isi.

### 2. Reviewer bilang "kontribusinya tidak jelas"

Komentar itu hampir selalu berarti rantainya putus di suatu tempat — biasanya gap yang dinyatakan
di Introduction tidak pernah ditutup di Discussion.

> *"Reviewer bilang kontribusi saya tidak jelas. Audit draf ini."*

Mode audit memeriksa keterlacakan tiap RQ melintasi kelima section, kelengkapan *move*, kalibrasi
klaim, terminology drift, dan penanda gaya AI generatif. Hasilnya daftar temuan berperingkat
dengan lokasi — bukan naskah yang langsung disunting diam-diam.

### 3. Anda menulis di bidang yang tidak berbentuk IMRaD

Matematika murni tidak punya Methods dan Results dalam arti IMRaD. Humaniora kerap *essay-style*.
Ilmu komputer sering IDBRC.

Skill ini **tidak memaksa satu bentuk**. Ia memuat konvensi bidang Anda dan mengikuti struktur di
situ — termasuk seberapa berani klaim boleh dinyatakan, yang berbeda tajam antar bidang.

## Kapan dipakai

- Punya data dan hasil, belum tahu menyusunnya jadi artikel
- Butuh outline yang tembus dari gap sampai kontribusi
- Mau mengaudit draf: apakah tiap section punya move yang benar
- Reviewer bilang "kontribusinya tidak jelas" atau "gap-nya lemah"

## Empat mode

| Mode | Untuk |
|---|---|
| **Outline** | memetakan gap → RQ → desain → hasil → kontribusi, satu baris per RQ tembus lima section |
| **Draft section** | menulis per move, dengan penanda `[SITASI]`/`[DATA]` untuk yang harus Anda isi |
| **Audit** | memeriksa kelengkapan move, keterlacakan RQ, kalibrasi klaim, penanda gaya AI |
| **Refine** | memperbaiki bagian yang ditunjuk |

## Yang membedakannya

**Introduction ditulis dua kali.** Urutan yang disarankan: Methods/Results dulu → Draft-0
Introduction → Discussion → **tulis ulang Introduction**. Tujuannya agar klaim persis se-level
bukti yang benar-benar didapat, bukan yang diharapkan di awal.

**Kalibrasi per bidang.** Natural sciences paling berani memakai *boosters*; matematika dan
physical sciences paling hemat; humaniora paling banyak *hedging*. Skill ini tidak menyeragamkan.

**Matematika murni tidak dipaksa IMRaD.** Strukturnya mengikuti konvensi teorema-bukti.

## Isinya

- `sections/` — panduan move per section, Title sampai Conclusion
- `research-types/` — kuantitatif, kualitatif, mixed methods, **analisis tematik** (enam fase Braun & Clarke)
- `fields/` — matematika, engineering/CS, natural sciences, social sciences, humaniora
- `reporting-guidelines/` — ringkasan maksud COREQ, SRQR, CROSS dengan kata sendiri
- `ai-stylometry-flags.md` — daftar kanonik penanda gaya AI, dipakai bersama tiga skill
- `coherence.md`, `phrasebank.md`

## Satu jebakan yang sering kena

**Analisis tematik ada dua, dan namanya beda.** Braun & Clarke (2006) untuk **data primer** —
transkrip wawancara, FGD. Untuk menyintesis temuan artikel yang sudah terbit dalam tinjauan
sistematis, metodenya **thematic synthesis** (Thomas & Harden 2008).

Menulis *"we used Braun & Clarke thematic analysis"* pada sebuah SLR adalah salah kutip metode,
dan ditandai reviewer metodologis.

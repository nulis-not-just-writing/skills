# Skills penulisan artikel jurnal untuk Claude

[![Kunjungan](https://hits.sh/github.com/nulis-not-just-writing/skills.svg?style=flat-square&label=kunjungan&color=444444)](https://hits.sh/github.com/nulis-not-just-writing/skills/)

*[Read this in English](README.md)*

Enam skill Claude untuk menulis, memfigurkan, memoles, menyubmit, dan merevisi artikel jurnal
berstandar Q1 (Scopus/WoS) — termasuk satu yang menjalankan *systematic literature review* dari nol
sampai manuskrip.

**Bahasa kerjanya mengikuti bahasa Anda** — tanya dalam bahasa Indonesia, dijawab Indonesia;
tanya dalam bahasa Inggris, dijawab Inggris. Bahasa naskahnya sendiri mengikuti jurnal target,
terlepas dari bahasa percakapan.

**Bidang apa pun, jenis riset apa pun.** Yang berbeda antar bidang bukan langkahnya melainkan
konvensinya — dan skill ini memilih konvensi yang tepat alih-alih menyeragamkan. Kekuatan klaim,
struktur section, dan standar pelaporan dikalibrasi sesuai bidang dan desain riset Anda: IMRaD
bukan hukum alam, dan naskah matematika tidak dipaksa mengikuti pola naskah biologi.

## Skill

| Skill | Menjawab | Versi |
|---|---|---|
| [`nulis`](nulis/) | apakah tiap section punya *move* yang benar, dan apakah RQ terlacak dari gap sampai kontribusi? | 1.4.0 |
| [`visualisasi-data`](visualisasi-data/) | apakah bentuk figurnya mengatakan sesuatu tentang objek yang diteliti? | 1.0.0 |
| [`polish-manuscript`](polish-manuscript/) | apakah kalimatnya jelas, argumennya kokoh, klaimnya terkalibrasi? | 1.4.0 |
| [`submit`](submit/) | apakah naskah lolos sepuluh menit pertama editor, atau dipulangkan sebelum direview? | 1.5.0 |
| [`revisi`](revisi/) | apakah tiap butir komentar reviewer terjawab, dan bisakah editor menemukan perubahannya? | 1.3.0 |
| [`slr-cowork`](slr-cowork/) | apakah tinjauan sistematisnya dapat direkonsiliasi angkanya dan dipertahankan metodenya? | 1.5.0 |

## Apa yang dikerjakan masing-masing

**[`nulis`](nulis/)** — *struktur*. Coaching berbasis genre analysis: membimbing per *move*,
memetakan gap → RQ → desain → hasil → kontribusi sebagai satu baris per RQ yang tembus lima
section, dan mengalibrasi seberapa berani klaim boleh dinyatakan di bidang Anda. Empat mode:
outline, menyusun section, mengaudit draf, memperbaiki bagian tertentu.

**[`visualisasi-data`](visualisasi-data/)** — *figur*. Memilih bentuk visual dari apa yang satu baris
data itu *sebenarnya* — posisi di kulit kepala jadi topografi, wilayah jadi peta, studi dalam
sintesis jadi forest plot — alih-alih jatuh ke bar chart. Lalu menahan figurnya pada fidelitas data,
sebaran yang tampak, aman buta warna, dan spesifikasi cetak jurnal. Empat belas rute domain, plus
tabel struktur data supaya bidang yang tidak terdaftar tidak pernah jadi jalan buntu.

**[`polish-manuscript`](polish-manuscript/)** — *prosa*. Audit sepuluh dimensi atas draf yang
strukturnya sudah benar. Cirinya yang paling membedakan adalah **gerbang fidelitas**: tiap angka
dan sitasi yang ada sebelum penyuntingan wajib masih ada sesudahnya, atau bagian itu dikembalikan
dan dilaporkan.

**[`submit`](submit/)** — *gerbang*. Menyapu risiko desk rejection, yang mengenai 40–70% naskah
masuk dan sebagian besar kriterianya tidak menyentuh mutu ilmiah. Berjalan dari yang termurah dan
paling mematikan, lalu **berhenti di temuan fatal pertama**.

**[`revisi`](revisi/)** — *setelah keputusan*. Membongkar komentar reviewer jadi butir yang bisa
dilacak, memutuskan tiap butir berdasarkan argumennya alih-alih suara terbanyak, dan menulis surat
tanggapan yang hanya mengklaim perubahan yang benar-benar ada — sekaligus memberi tahu editor di
mana menemukannya.

**[`slr-cowork`](slr-cowork/)** — *tinjauan sistematis*. Sembilan tahap dari form kesepakatan
sampai manuskrip PRISMA 2020, dengan gerbang yang menangkap pertanyaan tak terjawab sejak awal dan
aritmetika yang harus rekonsiliasi. Menangani korpus doktrinal-normatif tempat instrumen klinis
tidak punya objek.

Halaman lengkap tiap skill, berikut skenario nyatanya, ada di [`docs/id/`](docs/id/README.md).

## Dokumentasi

Panduan lengkap ada di **[`docs/id/`](docs/id/README.md)** — pemasangan, alur kerja, prasyarat,
satu halaman per skill, dan tanya jawab. Versi Inggrisnya di [`docs/`](docs/README.md); keduanya
dijaga sejajar isinya.

Isi yang sama dicerminkan ke [Wiki](https://github.com/nulis-not-just-writing/skills/wiki), dua
bahasa. **`docs/` adalah sumbernya** — ia ikut versi bersama skill yang dijelaskannya; wiki
dibangkitkan ulang dengan `./sync-wiki.sh` dan jangan pernah disunting langsung.

## Berdiri sendiri atau berdampingan

**Setiap skill berfungsi penuh sendirian.** Bila tetangganya terpasang, sebagian langkah jadi
lebih dalam — tetapi tidak ada langkah yang macet karena tetangganya tidak ada. Tiap SKILL.md
memuat bagian *"Berdiri sendiri atau berdampingan"* dengan tabel: apa yang bertambah bila skill
lain ada, dan apa jalan keluarnya bila tidak.

Satu aturan berlaku di keenamnya: **langkah yang tidak bisa dijalankan tidak dianggap lolos.**
Skill diminta mengatakan apa adanya bahwa langkah itu di luar jangkauan, bukan diam-diam
melewatinya.

## Pasang

**Belum yakin punya yang mana?** Kalau Anda memakai Claude lewat peramban atau aplikasi desktop,
yang Anda butuhkan **Claude Desktop**. Kalau Anda mengetik `claude` di terminal, itu **Claude
Code**.

### Claude Desktop — tanpa git, tanpa terminal

1. **Unduh** skill yang Anda mau. Tiap tautan langsung menyimpan berkasnya ke komputer Anda:

   | Skill | Untuk apa | Unduh |
   |---|---|---|
   | `nulis` | struktur artikel | [nulis-1.4.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/nulis-1.4.0.zip) |
   | `visualisasi-data` | figur ilmiah | [visualisasi-data-1.0.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/visualisasi-data-1.0.0.zip) |
   | `polish-manuscript` | prosa & mekanik | [polish-manuscript-1.4.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/polish-manuscript-1.4.0.zip) |
   | `submit` | gerbang pra-submisi | [submit-1.5.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/submit-1.5.0.zip) |
   | `revisi` | setelah keputusan editor | [revisi-1.3.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/revisi-1.3.0.zip) |
   | `slr-cowork` | tinjauan sistematis | [slr-cowork-1.5.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/slr-cowork-1.5.0.zip) |

   Jangan di-*unzip*. Claude Desktop meminta berkas `.zip`-nya apa adanya.

2. Buka Claude Desktop → **Settings** → **Capabilities** → **Skills**
3. Klik **Upload**, lalu pilih berkas yang barusan Anda unduh
4. Selesai.

**Anda tidak perlu memanggil skill-nya.** Ia aktif sendiri ketika Anda menyebut hal yang relevan —
coba *"saya mau mulai menulis artikel dari data survei ini"*, dan `nulis` semestinya menyala.

Pasang yang Anda perlukan saja; tiap skill berdiri sendiri. Rincian langkah demi langkah, termasuk
cara memperbarui dan mencopot, ada di [docs/id/Pemasangan.md](docs/id/Pemasangan.md).

### Claude Code — untuk terminal

```bash
git clone https://github.com/nulis-not-just-writing/skills.git
cd skills
cp -R nulis visualisasi-data polish-manuscript submit revisi slr-cowork ~/.claude/skills/
```

Pasang yang Anda perlukan saja — keenamnya berdiri sendiri.
## Prasyarat

Lima skill teks punya skrip Python pembantu yang **semuanya stdlib-only** — tidak ada `pip install`,
tidak ada virtualenv — dan diuji jalan pada Python 3.9.6 bawaan macOS maupun 3.12.

Kelimanya tetap berfungsi tanpa Python: cakupan sebagian dimensi berkurang, dan skill diminta
mengatakan itu alih-alih diam. Pandoc opsional, hanya untuk masukan `.docx`.

| Kebutuhan | Untuk apa | Bila tidak ada |
|---|---|---|
| Python 3 | sapuan mekanis, gerbang fidelitas, audit PRISMA | dikerjakan manual, cakupan berkurang |
| pandoc | membaca `.docx` | ekspor naskah ke `.md` atau `.tex` |
| MCP `scholar`/`zotero` | verifikasi sitasi & deteksi retraksi | jatuh ke `WebSearch`/`WebFetch`, lalu ke penandaan manual |
| R + `robvis` | figur traffic-light risk of bias | aplikasi web robvis, atau tabel studi × domain |
| `matplotlib` + `numpy` | menggambar figur di `visualisasi-data` | **skill itu tidak bisa menggambar** — panduan rancangannya tetap berlaku |

**`visualisasi-data` pengecualiannya.** Ia menggambar, jadi `matplotlib` dan `numpy` memang wajib
(`pip install matplotlib numpy`). Paruh rancangannya — Uji Rujukan, rute domain, aturan figur —
berupa prosa dan tidak menuntut pemasangan apa pun.

## Rantai kerja

```
nulis ──▶ visualisasi-data ──▶ polish-manuscript ──▶ submit ──▶ [keputusan editor] ──▶ revisi
  ▲                                                                                       │
  └──────────────────── bila reviewer menuntut RQ/kontribusi berubah ─────────────────────┘

slr-cowork ──▶ (Tahap 9 menghasilkan manuskrip) ──▶ visualisasi-data ──▶ polish-manuscript ──▶ submit
```

## Lisensi

**[CC BY-NC 4.0](LICENSE)** — Creative Commons Attribution-NonCommercial 4.0 International.

Boleh dipakai, disalin, diubah, dan disebarkan **untuk keperluan non-komersial**, dengan
mencantumkan atribusi. Pemakaian komersial — termasuk pelatihan berbayar dan produk berbayar —
memerlukan izin terpisah dari pemegang hak.

Peneliti, mahasiswa, dosen, dan lembaga pendidikan yang memakainya untuk riset dan pengajaran
tidak perlu meminta izin apa pun; cukup cantumkan sumbernya.

### Atribusi pihak ketiga

Sebagian isi berasal dari pihak ketiga dengan lisensi berbeda — **MIT** dan **CC BY 4.0**. Lihat
[`NOTICE.md`](NOTICE.md) di akar dan `NOTICE.md` di dalam **setiap** skill; keduanya wajib ikut
bila Anda menyebarkan ulang.

Instrumen penilaian kualitas (RoB 2, ROBINS-I, AMSTAR 2, MMAT, AXIS) **tidak disalin** ke repo
ini — yang ada hanya ringkasan kata sendiri dengan sitasi, karena pemeriksaan metadata CrossRef
menunjukkan ketiganya yang pertama hanya berlisensi *text and data mining* dan dua sisanya tidak
punya lisensi terdaftar. Unduh formulir resminya dari sumber masing-masing untuk lampiran submisi.

---

> **Knowledge unshared dies. Knowledge shared keeps living.**
>
> It grows in hands you will never meet and is carried on in work you will never read — and what
> never stops living never stops returning to you.

**Mubaroq ADB** · Akademi Digital Bandung | RPI Institute · <mubaroq@digitalbdg.ac.id>

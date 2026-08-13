# Skills penulisan artikel jurnal untuk Claude

*[Read this in English](README.en.md)*

Lima skill Claude untuk menulis, memoles, menyubmit, dan merevisi artikel jurnal berstandar
Q1 (Scopus/WoS) — plus satu untuk menjalankan *systematic literature review* dari nol sampai
manuskrip.

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
| [`polish-manuscript`](polish-manuscript/) | apakah kalimatnya jelas, argumennya kokoh, klaimnya terkalibrasi? | 1.4.0 |
| [`submit`](submit/) | apakah naskah lolos sepuluh menit pertama editor, atau dipulangkan sebelum direview? | 1.5.0 |
| [`revisi`](revisi/) | apakah tiap butir komentar reviewer terjawab, dan bisakah editor menemukan perubahannya? | 1.3.0 |
| [`slr-cowork`](slr-cowork/) | apakah tinjauan sistematisnya dapat direkonsiliasi angkanya dan dipertahankan metodenya? | 1.5.0 |

## Dokumentasi

Panduan lengkap ada di **[`docs/`](docs/)** — pemasangan, alur kerja, prasyarat, satu halaman per
skill, dan tanya jawab. Mulai dari [`docs/README.md`](docs/README.md) bila belum tahu skill mana
yang Anda butuhkan.

Isi yang sama dicerminkan ke [Wiki](https://github.com/nulis-not-just-writing/skills/wiki).
**`docs/` adalah sumbernya** — ia ikut versi bersama skill yang dijelaskannya; wiki disegarkan
dengan `./sync-wiki.sh`.

## Berdiri sendiri atau berdampingan

**Setiap skill berfungsi penuh sendirian.** Bila tetangganya terpasang, sebagian langkah jadi
lebih dalam — tetapi tidak ada langkah yang macet karena tetangganya tidak ada. Tiap SKILL.md
memuat bagian *"Berdiri sendiri atau berdampingan"* dengan tabel: apa yang bertambah bila skill
lain ada, dan apa jalan keluarnya bila tidak.

Satu aturan berlaku di kelimanya: **langkah yang tidak bisa dijalankan tidak dianggap lolos.**
Skill diminta mengatakan apa adanya bahwa langkah itu di luar jangkauan, bukan diam-diam
melewatinya.

## Pasang

**Claude Desktop** — unduh zip yang Anda mau dari [`dist/`](dist/), lalu unggah lewat
**Settings → Capabilities → Skills**. Tidak perlu git.

- [`nulis-1.4.0.zip`](dist/nulis-1.4.0.zip)
- [`polish-manuscript-1.4.0.zip`](dist/polish-manuscript-1.4.0.zip)
- [`submit-1.5.0.zip`](dist/submit-1.5.0.zip)
- [`revisi-1.3.0.zip`](dist/revisi-1.3.0.zip)
- [`slr-cowork-1.5.0.zip`](dist/slr-cowork-1.5.0.zip)

**Claude Code** — salin foldernya:

```bash
git clone https://github.com/nulis-not-just-writing/skills.git
cp -R skills/nulis ~/.claude/skills/
```

Atau symlink bila ingin tetap mengikuti pembaruan:

```bash
ln -s "$PWD/skills/nulis" ~/.claude/skills/nulis
```

> Nama zip memuat versi supaya sebuah berkas tidak pernah "basi" — versi baru menghasilkan
> berkas baru, bukan menimpa yang lama. Bangun ulang dengan `./build-zips.sh` setelah menaikkan
> versi; skripnya menolak menghasilkan zip yang kehilangan `NOTICE.md` atau membawa berkas sampah.

## Prasyarat

Sebagian skill punya skrip Python pembantu. **Semuanya stdlib-only** — tidak ada `pip install`,
tidak ada virtualenv — dan diuji jalan pada Python 3.9.6 bawaan macOS maupun 3.12.

Skill tetap berfungsi tanpa Python: cakupan sebagian dimensi berkurang, dan skill diminta
mengatakan itu alih-alih diam. Pandoc opsional, hanya untuk masukan `.docx`.

| Kebutuhan | Untuk apa | Bila tidak ada |
|---|---|---|
| Python 3 | sapuan mekanis, gerbang fidelitas, audit PRISMA | dikerjakan manual, cakupan berkurang |
| pandoc | membaca `.docx` | ekspor naskah ke `.md` atau `.tex` |
| MCP `scholar`/`zotero` | verifikasi sitasi & deteksi retraksi | jatuh ke `WebSearch`/`WebFetch`, lalu ke penandaan manual |
| R + `robvis` | figur traffic-light risk of bias | aplikasi web robvis, atau tabel studi × domain |

## Rantai kerja

```
nulis ──▶ polish-manuscript ──▶ submit ──▶ [keputusan editor] ──▶ revisi
  ▲                                                                  │
  └──────────── bila reviewer menuntut RQ/kontribusi berubah ─────────┘

slr-cowork ──▶ (Tahap 9 menghasilkan manuskrip) ──▶ polish-manuscript ──▶ submit
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

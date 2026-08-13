# NOTICE — karya pihak ketiga di dalam repo ini

Repo ini memuat karya pihak ketiga. Pemberitahuan wajib ikut pada setiap salinan dan distribusi
ulang. **Tiap skill juga punya `NOTICE.md` sendiri** yang dilingkupi pada apa yang skill itu bawa
— berkas ini ringkasannya.

## Ringkasan per skill

| Skill | Membawa | Lisensi |
|---|---|---|
| `submit` | 5 skrip disalin apa adanya + kartu uji regresi | MIT |
| `polish-manuscript` | 3 skrip diadaptasi | MIT |
| `slr-cowork` | 3 checklist verbatim, 1 skrip, 1 pola desain, kutipan pernyataan sikap | CC BY 4.0 + MIT |
| `nulis` | konsep kerangka analisis tematik; ringkasan kata sendiri COREQ/SRQR/CROSS | MIT (konsep) |
| `revisi` | **konsep dari sumber non-komersial** | **CC BY-NC 4.0** ⚠ |

## Sumber

**`Aperivue/medsci-skills`** — https://github.com/Aperivue/medsci-skills — Aperivue, 2026, **MIT**.
Skrip di `submit/scripts/hulu/` disalin apa adanya supaya pembaruan hulu dapat ditarik bersih;
skrip di `polish-manuscript/scripts/` diadaptasi (keluaran bahasa Indonesia, dukungan LaTeX,
pemeriksaan khas penulis Indonesia). Sejumlah aturan metodologis di `slr-cowork` diserap sebagai
konsep, bukan teks.

**`keemanxp/slr-prisma`** — **MIT**, plus PRISMA 2020 (CC BY 4.0). Struktur panduan diagram alir.

**`keemanxp/thematic-analysis-skill`** — **MIT**. Kerangka analisis tematik, ditulis ulang dan
dipecah ke dua rumah: data primer di `nulis`, sintesis literatur di `slr-cowork`.

**`aipoch/medical-research-skills`** — **MIT**. Hanya **polanya** yang diambil (satu instrumen per
desain studi, NOS dipisah kohort/kasus-kontrol); tidak ada teks yang disalin.

**⚠ `Imbad0202/academic-research-skills`** — Cheng-I Wu, 2026, **CC BY-NC 4.0 (non-komersial)**.
Tiga prinsip keputusan editorial di `revisi/SKILL.md` Tahap 3, ditulis ulang sepenuhnya dengan
kata sendiri. **Batasan NC diperlakukan konservatif**: materi yang diturunkan dari sumber itu tidak
boleh masuk ke produk atau pelatihan berbayar tanpa izin pemegang hak. Rinciannya di
`revisi/NOTICE.md`.

## Salinan verbatim — CC BY 4.0

Lisensi diverifikasi lewat field `license` metadata CrossRef, bukan dari indeks pihak ketiga.

| Berkas | Sumber | DOI |
|---|---|---|
| `slr-cowork/reference/prisma-2020-checklist.md` | Page MJ dkk. *BMJ* 2021;372:n71 | [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71) |
| `slr-cowork/reference/checklist-abstrak.md` | idem — PRISMA 2020 for Abstracts | idem |
| `slr-cowork/reference/swim-jalur-a.md` | Campbell M dkk. *BMJ* 2020;368:l6890 | [10.1136/bmj.l6890](https://doi.org/10.1136/bmj.l6890) |

Kutipan beratribusi: pernyataan sikap RAISE (Flemyng E dkk. *Campbell Systematic Reviews*
2025;21(4), [10.1002/cl2.70074](https://doi.org/10.1002/cl2.70074)) — CC BY 4.0.

## Instrumen yang sengaja TIDAK disalin

Pemeriksaan CrossRef menunjukkan **RoB 2, ROBINS-I, dan AMSTAR 2 hanya punya lisensi *text and
data mining* BMJ**; **MMAT dan AXIS tidak punya field lisensi terdaftar**. Kelimanya muncul di
`slr-cowork/reference/instrumen-qa.md` **hanya sebagai ringkasan kata sendiri** dengan sitasi
lengkap.

Catatan koreksi: klaim CC BY untuk RoB 2 dan ROBINS-I yang beredar di indeks lisensi pihak ketiga
**tidak didukung** metadata CrossRef. Percayai metadata sumber, bukan ringkasan orang lain.

## Instrumen pelaporan yang diringkas dengan kata sendiri

COREQ ([10.1093/intqhc/mzm042](https://doi.org/10.1093/intqhc/mzm042)), SRQR
([10.1097/ACM.0000000000000388](https://doi.org/10.1097/ACM.0000000000000388)), dan CROSS
([10.1007/s11606-021-06737-1](https://doi.org/10.1007/s11606-021-06737-1)) diringkas maksudnya
di `nulis/reporting-guidelines/` karena status lisensi instrumen aslinya belum terselesaikan.
**Bukan pengganti checklist resmi** untuk lampiran submisi.

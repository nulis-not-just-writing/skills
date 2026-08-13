# submit — gerbang pra-submisi

*[Read this in English](../submit.md)*

**v1.5.0** · [unduh zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/submit-1.5.0.zip)

Menyapu naskah untuk risiko **desk rejection** — penolakan oleh editor sebelum naskah sampai ke
reviewer, dalam pembacaan sekitar sepuluh menit, dan mengenai 40–70% naskah masuk di jurnal
bereputasi.

Sebagian besar kriterianya **tidak menyentuh mutu ilmiah**. Naskah bagus rutin dipulangkan karena
scope-nya meleset atau pernyataan etiknya kosong.

## Untuk apa sebenarnya skill ini

### 1. Naskah siap kirim, dan Anda ingin tahu apa yang akan membunuhnya

> *"Naskah ini mau saya kirim ke [nama jurnal]. Ini author guidelines-nya. Periksa."*

Skill berjalan **berurutan dari yang termurah dan paling mematikan**. Scope jurnal lebih dulu,
bukan tanda hubung. Begitu ada temuan fatal, ia **berhenti dan melapor** — karena memoles kalimat
pada naskah yang salah jurnal adalah pekerjaan yang akan dibuang seluruhnya.

Yang wajib Anda siapkan: **URL author guidelines jurnal targetnya**. Tanpa itu kira-kira separuh
risiko tidak bisa dinilai, dan skill akan mengatakannya alih-alih menebak — batas kata dan
pernyataan wajib berbeda antar jurnal dalam satu penerbit yang sama.

### 2. Naskah dipulangkan tanpa direview dan Anda tidak tahu sebabnya

Ini keadaan yang paling sering membawa orang ke sini, dan jawabannya sering mengejutkan: **sebagian
besar kriteria desk rejection tidak menyentuh mutu ilmiah sama sekali.** Naskah bagus rutin
dipulangkan karena pernyataan etiknya kosong, batas katanya terlampaui, atau anonimitasnya bocor
di metadata.

### 3. Anda ingin tahu apakah sitasinya benar-benar ada

Tiga status yang biasanya disatukan alat lain, dan bedanya penting:

| Status | Artinya | Tindakan |
|---|---|---|
| `VERIFIED` | cocok dengan indeks | — |
| `MISMATCH` | DOI benar, penulis/tahun meleset | karyanya nyata, entri bibliografinya salah |
| `UNVERIFIED` | tidak ditemukan di indeks mana pun | **tanda kuat sitasi karangan** |

Dan satu pemeriksaan yang jarang ada di tempat lain: `check_claim_fidelity.py` menanyakan
**apakah sumbernya benar-benar mengatakan itu** — kutipan verbatim yang tidak ada di sumbernya,
atribusi konsep yang tak satu pun katanya muncul, klaim kardinal yang angkanya tak pernah
disebut.

Bila teks lengkap sumbernya tidak tersedia, **skrip itu diam**. Ia tidak pernah menebak.

## Kapan dipakai

- Naskah dianggap selesai dan hendak dikirim
- Pernah ditolak tanpa direview, tidak tahu kenapa
- Sedang memilih atau mengganti jurnal target
- Menyiapkan paket submisi: cover letter, highlights, pernyataan etik, anonimisasi

## Ini gerbang, bukan sapuan mutu

Bedanya dengan `polish-manuscript` dan `nulis` bukan cuma daftar periksanya, tapi **bentuknya**:

- Keduanya *improvement pass* — linear, menyeluruh, menimbang semua dimensi setara
- Skill ini **gerbang** — berurutan dari yang termurah dan paling mematikan. **Satu temuan fatal
  membuat sisanya tidak relevan: berhenti, laporkan, jangan lanjut menyisir.**

Percuma memoles tanda hubung pada naskah yang scope-nya salah jurnal.

## Yang wajib Anda siapkan

1. Naskah (`.docx`/`.tex`/`.md`)
2. **Jurnal target + URL author guidelines-nya** — tidak bisa ditawar; tanpa ini kira-kira separuh risiko tak bisa dinilai
3. Model review: double-blind atau single-blind? Pernah jadi preprint?
4. Nama & afiliasi semua penulis

Author guidelines **dibaca sungguhan**, bukan ditebak dari kebiasaan penerbit — batas kata dan
pernyataan wajib berbeda antar jurnal dalam satu penerbit yang sama.

## Lima skrip

| Skrip | Memeriksa |
|---|---|
| `sweep.py` | konsistensi **di dalam** naskah: jumlah kata, tujuh pernyataan wajib, silang sitasi dua arah, kebocoran anonimitas, figur yatim, sisa TODO/tracked changes |
| `verify_refs.py` | rujukan **terhadap dunia luar** — CrossRef, OpenAlex, PubMed |
| `check_claim_fidelity.py` | **apakah sumbernya benar-benar mengatakan itu?** |
| `prisma_cascade_check.py` | aritmetika kaskade PRISMA |
| `check_prisma_figure.py` | naskah versus figur PRISMA |

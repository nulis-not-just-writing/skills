# submit — gerbang pra-submisi

**v1.4.0** · [unduh zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/submit-1.4.0.zip)

Menyapu naskah untuk risiko **desk rejection** — penolakan oleh editor sebelum naskah sampai ke
reviewer, dalam pembacaan sekitar sepuluh menit, dan mengenai 40–70% naskah masuk di jurnal
bereputasi.

Sebagian besar kriterianya **tidak menyentuh mutu ilmiah**. Naskah bagus rutin dipulangkan karena
scope-nya meleset atau pernyataan etiknya kosong.

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

## Tiga status yang sering dicampur

`verify_refs.py` membedakan yang biasanya disatukan:

- **`VERIFIED`** — cocok
- **`MISMATCH`** — DOI benar, tapi daftar penulis atau tahunnya meleset. Karyanya nyata; entri bibliografinya salah
- **`UNVERIFIED`** — tidak ditemukan di indeks mana pun. **Tanda kuat sitasi karangan**

`check_claim_fidelity.py` menjawab yang tak terjawab skrip lain: kutipan verbatim yang tidak ada di
sumber, atribusi konsep yang tak satu pun katanya muncul, dan klaim kardinal ("melaporkan tiga
strategi") yang angkanya tak pernah disebut. **Bila teks lengkapnya tidak ada, skrip diam** — ia
tidak pernah menebak.

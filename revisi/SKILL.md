---
name: revisi
description: Kerjakan revisi naskah jurnal setelah keputusan editor - membaca surat keputusan, membongkar komentar reviewer menjadi butir yang bisa dilacak, memutuskan mana yang dikerjakan dan mana yang ditolak, menulis surat tanggapan (response to reviewers), dan memeriksa kelengkapannya sebelum dikirim balik. Gunakan saat user menerima major/minor revision, reject and resubmit, atau penolakan yang ingin dibanding; saat user bertanya bagaimana menjawab komentar reviewer, bagaimana menolak permintaan reviewer tanpa terdengar defensif, apa yang harus dilakukan bila dua reviewer bertentangan, atau apakah surat tanggapannya sudah lengkap. Untuk pemolesan prosa teks baru gunakan polish-manuscript; untuk perombakan struktur section gunakan nulis; untuk gerbang pra-submisi naskah baru gunakan submit.
metadata:
  author: Mubaroq ADB | RPI
  version: 1.2.0
---

# revisi — Menjawab Reviewer

Major revision adalah kabar baik yang paling sering disia-siakan. Naskah yang sampai
ke tahap ini sudah lolos desk rejection dan sudah dinilai layak diperbaiki; sebagian
besar akhirnya terbit. Yang gagal umumnya gagal bukan karena revisinya kurang, melainkan
karena **surat tanggapannya** — butir yang terlewat, penolakan yang terdengar
membangkang, atau perubahan yang tidak bisa ditemukan editor.

## Bentuk kerjanya: docket, bukan sapuan

Tiga skill tetangga bekerja atas **naskah**. Skill ini bekerja atas **daftar butir**:

- `nulis` berjalan per move, `polish-manuscript` per dimensi, `submit` per gerbang.
- Skill ini berjalan **per butir komentar**, dan tidak selesai sampai setiap butir
  punya keputusan, tindakan, lokasi, dan jawaban tertulis.

Aturan tunggal yang menaungi seluruh skill ini: **tidak ada butir yang boleh tidak
dijawab.** Termasuk butir yang Anda tolak, butir yang menurut Anda salah, dan butir
yang sudah dijawab di tempat lain. Butir yang dilewat adalah penyebab ronde kedua yang
paling sering, dan ronde kedua sering berarti reviewer baru.

Pembacanya dua orang sekaligus: **editor** yang memutuskan, dan **reviewer** yang
membaca ulang untuk memeriksa apakah keberatannya ditanggapi. Menulis untuk salah
satunya saja adalah kesalahan yang khas.

## Langkah 0 — Input wajib

Tanyakan dengan daftar bernomor biasa (jangan AskUserQuestion). Empat hal:

1. **Surat keputusan lengkap** — apa adanya, termasuk komentar semua reviewer.
   Jangan menerima ringkasannya; nuansa kalimat editor menentukan prioritas, dan
   ringkasan user hampir selalu sudah menyaring hal yang tidak enak dibaca.
2. **Naskah versi yang disubmit** — untuk melacak lokasi perubahan.
3. **Tenggat**, dan apakah masih bisa diperpanjang.
4. **Batas kemampuan riil** — bisakah eksperimen/pengambilan data baru dilakukan
   dalam tenggat itu? Ada dana, akses data, izin etik? Jawaban ini menentukan mana
   permintaan yang bisa dipenuhi dan mana yang harus dinegosiasikan. Menanyakannya
   di awal mencegah rencana revisi yang mustahil dikerjakan.

## Sapuan mekanis lebih dulu

```bash
python scripts/tanggapan.py pecah SURAT-KEPUTUSAN.docx
```

Script memecah surat menjadi blok per reviewer dan butir kandidat ber-ID, menandai
butir yang tampaknya memuat lebih dari satu permintaan, dan mencetak tabel docket siap
isi. Ia **menghitung, tidak memutuskan** — atomisitas butir tetap penilaian Anda.

Nanti, setelah surat tanggapan jadi:

```bash
python scripts/tanggapan.py cek DOCKET.md SURAT-TANGGAPAN.docx
```

---

## Tahap 1 — Baca keputusannya, bukan cuma komentarnya

Kebanyakan penulis melompat ke daftar reviewer dan melewati surat editornya. Itu
kesalahan urutan: **surat editor mengalahkan komentar reviewer.**

Editor sering sudah menyaring. "Please pay particular attention to Reviewer 2's
methodological concerns; Reviewer 1's request for additional experiments is desirable
but not mandatory" adalah instruksi yang menentukan seluruh rencana revisi — butir yang
sama bisa wajib atau opsional tergantung kalimat itu. Baca surat editor dulu, catat
prioritas dan izin yang ia berikan, baru buka komentar reviewer.

Yang harus keluar dari tahap ini: jenis keputusan yang sebenarnya, prioritas dari
editor, tenggat, dan **putusan apakah revisi ini layak dikerjakan sama sekali**. Untuk
*reject and resubmit* dengan permintaan yang setara riset baru, pindah jurnal kadang
lebih murah. Rinci di `references/membaca-keputusan.md` — termasuk kapan banding
(appeal) masuk akal dan kapan tidak.

## Tahap 2 — Bongkar jadi butir

Satu paragraf reviewer rutin memuat tiga permintaan. Yang ketiga yang terlupa.

Pecah sampai **atomik**: satu butir = satu tindakan yang bisa dicentang. Beri ID stabil
(`ED.1`, `R1.1`, `R2.3`) dan simpan **kutipan verbatim**-nya; jangan pernah
memparafrase komentar reviewer ke dalam docket, karena parafrase menghaluskan permintaan
tanpa Anda sadari.

Pertahankan juga **penomoran asli reviewer**. Surat tanggapan harus memakai penomoran
mereka agar mereka mengenali komentarnya sendiri; ID internal hanya untuk pelacakan.

Lalu klasifikasikan tiap butir — jenisnya menentukan pola jawabannya:

| Jenis | Ciri | Sikap dasar |
|---|---|---|
| Mekanis | typo, satuan, referensi hilang | kerjakan, jawab satu kalimat |
| Klarifikasi | reviewer tidak paham maksud Anda | **hampir selalu kesalahan naskah** — perbaiki naskahnya, bukan cuma jelaskan di surat |
| Analisis tambahan | bisa dengan data yang ada | kerjakan bila masuk akal |
| Data/eksperimen baru | mahal, butuh waktu | negosiasi; lihat `references/menanggapi.md` |
| Beda pendapat | teoretis/metodologis | boleh ditolak, dengan bayaran |
| Salah baca | reviewer keliru soal isi naskah | tetap perbaiki keterbacaannya |
| Di luar cakupan | meminta paper yang berbeda | tolak dengan konsesi |

Dua baris di tabel itu yang paling sering salah dikerjakan. **Klarifikasi dan salah
baca bukan alasan untuk membela diri.** Bila satu pembaca ahli salah menangkap, pembaca
lain akan salah menangkap juga — itu cacat naskah, apa pun perasaan Anda soal
kecermatan reviewer. Jawabannya selalu: naskah diperbaiki, lalu tunjukkan di mana.

## Tahap 3 — Putuskan per butir

Tiga keputusan saja: **LAKUKAN**, **SEBAGIAN**, **TOLAK**.

Tolak sedikit, dan bayar mahal untuk tiap penolakan. Surat yang menolak lebih dari
sekitar sepersepuluh butirnya terbaca sebagai penulis yang tidak kooperatif, dan editor
menilai itu sebelum menilai argumennya. Setiap TOLAK wajib memuat tiga hal: pengakuan
atas premis reviewer, alasan konkret (bukan "di luar cakupan" telanjang), dan
**konsesi** — limitasi yang ditulis, analisis pengganti, atau kalimat di Future Work.

Bila dua reviewer bertentangan, jangan diam-diam memihak satu. Naikkan ke editor secara
terbuka di surat: sebutkan pertentangannya, pilihan Anda, dan alasannya. Editor yang
memutuskan, dan ia akan menghargai bahwa Anda tidak menyembunyikannya.

### Tiga prinsip yang menjaga keputusan tetap jujur

Ketiganya mengatur cara Anda menimbang, bukan cara Anda menulis. Diserap dari standar
keputusan editorial academic-research-skills (lihat NOTICE.md).

1. **Simetri beban bukti.** LAKUKAN dan TOLAK menanggung beban yang sama. Menyimpulkan
   "reviewer keliru" menuntut bukti sekonkret menyimpulkan "reviewer benar" — kutipan
   dari naskah, angka dari data, rujukan yang bisa dibuka. Tidak ada arah yang boleh
   diberi kelonggaran. Dalam praktik, kecondongan yang lazim adalah menerima klaim
   reviewer tanpa memeriksanya karena menerima terasa lebih aman; itu tetap pelanggaran
   simetri, dan hasilnya naskah yang berubah tanpa alasan.

2. **Keputusan mengikuti kriteria, bukan distribusi.** Rasio "tolak sedikit" di atas
   adalah rambu kalibrasi, bukan kuota. Jangan pernah mengubah keputusan atas satu butir
   karena ingin menyesuaikan komposisi keseluruhan surat — bila sembilan dari sepuluh
   butir memang layak ditolak, tolak kesembilannya dan jelaskan; bila tak satu pun layak
   ditolak, jangan mengarang satu penolakan agar terlihat berpendirian. Yang menentukan
   adalah butirnya sendiri.

3. **Nada tidak boleh mengubah bobot.** Aturan kesopanan mengatur **kata**, bukan
   penilaian. Komentar reviewer yang disampaikan dengan kasar tidak menjadi lebih lemah
   karenanya, dan komentar yang disampaikan dengan halus tidak menjadi lebih kuat. Begitu
   pula ke arah sebaliknya: menulis tanggapan dengan nada tegas tidak membuat argumen
   Anda lebih berbobot. Nilai isinya lebih dulu, baru pilih nadanya.

## Tahap 4 — Tulis suratnya

Pola tiga bagian untuk **tiap** butir, tanpa kecuali:

1. **Kutipan komentar reviewer**, verbatim, dengan penomoran mereka.
2. **Apa yang Anda lakukan** — kalimat pertama langsung ke tindakan, bukan ke pujian.
3. **Di mana** — section, halaman, baris, nomor tabel/gambar. Bila teks berubah,
   kutipkan teks barunya.

Bagian ketiga yang paling sering hilang dan paling menentukan: editor memverifikasi
dengan membuka lokasi yang Anda sebut. Tanpa penunjuk lokasi, ia harus mencari sendiri —
dan sebagian tidak akan mencari.

Pola kalimat untuk setiap jenis butir, cara menolak tanpa terdengar membangkang, dan
aturan nada lengkapnya ada di `references/menanggapi.md`. Satu aturan nada yang
langsung berlaku di sini: **ucapkan terima kasih sekali di pembuka, lalu berhenti.**
"We thank the reviewer for this excellent and insightful comment" yang diulang empat
puluh kali memanjangkan surat, menunda isi, dan terbaca hampa.

## Tahap 5 — Paket & periksa

Kirim **tiga berkas**, bukan satu: surat tanggapan, naskah bertanda (highlight/tracked
changes), dan naskah bersih. Jangan pernah memaksa editor mendiff sendiri. Rinci —
berikut surat pengantar ke editor dan daftar periksa akhir — di
`references/paket-revisi.md`.

Sebelum kirim, jalankan `tanggapan.py cek`. Ia melaporkan butir yang tak dijawab,
jawaban tanpa penunjuk lokasi, frasa defensif, dan pujian berulang. Yang ia **tidak**
periksa: apakah jawabannya benar, dan apakah perubahan yang Anda klaim benar-benar ada
di naskah. Dua hal itu periksa sendiri, khususnya untuk butir yang Anda tolak.

### Urutan memanggil skill lain

Skill ini **membuka dan menutup** loop revisi; dua skill lain dipanggil di tengahnya,
dan hanya bila perlu:

```
revisi (Tahap 1–3: docket & keputusan)
   └─> nulis mode audit      — hanya bila ada butir yang menggeser struktur
   └─> polish-manuscript     — hanya untuk teks yang baru ditulis
revisi (Tahap 4–5: surat tanggapan & periksa)  ->  kirim balik
```

**`nulis` sebelum `polish`, bukan sebaliknya.** Memoles kalimat pada section yang
strukturnya masih akan dirombak adalah pekerjaan yang dibuang — alasan yang sama dengan
urutan di rantai menulis. Bila reviewer menuntut RQ diubah atau kontribusi digeser, itu
pekerjaan `nulis`, bukan tambal-sulam kalimat.

**`polish` hanya pada bagian baru.** Teks yang ditulis menjelang tenggat memang tempat
penanda AI dan klaim tak terkalibrasi paling sering masuk — tapi jangan memoles ulang
bagian yang tidak dikomentari (lihat aturan perubahan tak diminta di
`references/menanggapi.md`).

**Kirim balik bukan `submit` penuh.** Naskah revisi kembali ke editor yang sama dengan
nomor naskah yang sama; G1 (scope) dan G2 (jenis artikel) sudah tidak relevan. Yang
relevan sudah dicakup Tahap 5 lewat `sweep.py`. `submit` penuh dipanggil lagi hanya
untuk **reject and resubmit** dan untuk **pindah jurnal setelah ditolak**.

## Format keputusan

Buka dengan ringkasan satu tabel sebelum masuk ke butir:

| Blok | Butir | LAKUKAN | SEBAGIAN | TOLAK |
|---|---|---|---|---|

Lalu daftar butir berurutan sesuai urutan reviewer — **bukan** diurutkan menurut
prioritas Anda. Reviewer membaca sambil mencocokkan dengan komentarnya sendiri; urutan
yang diacak memaksanya mencari.

Sebutkan eksplisit bila ada butir yang **tidak bisa dikerjakan** dalam tenggat, beserta
alasan dan usulan (perpanjangan, atau menurunkannya jadi limitasi). Editor lebih
menerima keterbatasan yang dinyatakan di muka daripada janji yang tidak ditepati.

## Batas skill ini

- **Tidak mengerjakan risetnya.** Analisis tambahan, uji ulang, dan data baru tetap
  pekerjaan Anda; skill ini merencanakan dan menuliskannya.
- **Tidak menjamin diterima.** Revisi yang baik menaikkan peluang; keputusan tetap di
  editor.
- **Tidak menulis pembelaan untuk klaim yang memang lemah.** Bila reviewer benar dan
  datanya tidak mendukung klaim Anda, jawabannya menurunkan klaim — bukan menyusun
  argumen yang lebih pandai.

---

## Berdiri sendiri atau berdampingan

Skill ini **berfungsi penuh sendirian**. Membongkar komentar reviewer, memutuskan mana yang
dikerjakan, dan menulis surat tanggapan tidak menuntut skill lain.

| Bila terpasang | Yang bertambah | Tanpa itu |
|---|---|---|
| `submit` | `sweep.py` menyapu naskah revisi sekaligus | periksa manual lima hal di `references/paket-revisi.md`; yang paling sering terlewat: batas kata dan sisa tracked changes |
| `polish-manuscript` | pemolesan prosa teks baru hasil revisi | serahkan ke user sebagai langkah terpisah |
| `nulis` | perombakan struktur bila reviewer menuntut RQ atau kontribusi berubah | laporkan bahwa perombakannya di luar jangkauan sesi ini |

**Aturan:** surat tanggapan yang mengklaim perubahan yang belum benar-benar dikerjakan adalah
kegagalan paling mahal di tahap ini. Klaim hanya ditulis untuk perubahan yang sudah ada di naskah.

# Skills penulisan artikel jurnal untuk Claude

*[Read this in English](../README.md)*

Lima skill untuk menulis, memoles, menyubmit, dan merevisi artikel jurnal berstandar Q1
(Scopus/WoS) — plus satu untuk menjalankan *systematic literature review* dari nol sampai
manuskrip siap kirim.

**Bahasa kerjanya mengikuti bahasa Anda** — tanya dalam bahasa Indonesia, dijawab Indonesia;
tanya dalam bahasa Inggris, dijawab Inggris. Bahasa naskahnya sendiri mengikuti jurnal target,
terlepas dari bahasa percakapan.

Dokumentasi ini tersedia dua bahasa: halaman Inggris di [`docs/`](../README.md), Indonesia di
folder ini.

## Skill mana yang saya butuhkan?

Mulai dari keadaan Anda sekarang, bukan dari nama skill-nya.

| Keadaan Anda | Skill |
|---|---|
| Punya data dan hasil, belum tahu cara menyusunnya jadi artikel | **[nulis](nulis.md)** |
| Draf sudah jadi tapi terasa kaku, bertele-tele, atau "berbau AI" | **[polish-manuscript](polish-manuscript.md)** |
| Naskah dianggap selesai, mau dikirim ke jurnal | **[submit](submit.md)** |
| Naskah pernah ditolak tanpa direview, tidak tahu kenapa | **[submit](submit.md)** |
| Dapat keputusan *major/minor revision* dan komentar reviewer | **[revisi](revisi.md)** |
| Mau menulis tinjauan sistematis / *systematic review* | **[slr-cowork](slr-cowork.md)** |
| Reviewer bilang metode SLR Anda tidak dapat dipertahankan | **[slr-cowork](slr-cowork.md)** |

Belum yakin? Lihat **[Alur kerja](Alur-kerja.md)** — bagaimana kelimanya saling menyambung.

## Apa yang dikerjakan masing-masing

**[nulis](nulis.md)** — *struktur*. Coaching berbasis genre analysis: membimbing per *move*,
memetakan gap → RQ → desain → hasil → kontribusi sebagai satu baris per RQ yang tembus lima
section, dan mengalibrasi seberapa berani klaim boleh dinyatakan di bidang Anda. Empat mode:
outline, menyusun section, mengaudit draf yang sudah ada, memperbaiki bagian tertentu.

**[polish-manuscript](polish-manuscript.md)** — *prosa*. Audit sepuluh dimensi atas draf yang
strukturnya sudah benar. Cirinya yang paling membedakan adalah **gerbang fidelitas**: tiap angka
dan sitasi yang ada sebelum penyuntingan wajib masih ada sesudahnya, atau bagian itu dikembalikan
dan dilaporkan.

**[submit](submit.md)** — *gerbang*. Menyapu risiko desk rejection, yang mengenai 40–70% naskah
masuk dan sebagian besar kriterianya tidak menyentuh mutu ilmiah. Ia berjalan dari yang termurah
dan paling mematikan, lalu **berhenti di temuan fatal pertama**.

**[revisi](revisi.md)** — *setelah keputusan*. Membongkar komentar reviewer jadi butir yang bisa
dilacak, memutuskan tiap butir berdasarkan argumennya alih-alih suara terbanyak, dan menulis surat
tanggapan yang hanya mengklaim perubahan yang benar-benar ada — sekaligus memberi tahu editor di
mana menemukannya.

**[slr-cowork](slr-cowork.md)** — *tinjauan sistematis*. Sembilan tahap dari form kesepakatan
sampai manuskrip PRISMA 2020, dengan gerbang yang menangkap pertanyaan tak terjawab sejak awal dan
aritmetika yang harus rekonsiliasi. Menangani korpus doktrinal-normatif tempat instrumen klinis
tidak punya objek.

## Cakupan

**Bidang apa pun, jenis riset apa pun.** Yang berbeda antar bidang bukan langkahnya, melainkan
konvensinya — dan skill ini **memilih konvensi yang tepat alih-alih menyeragamkan**.

Langkah pertama di tiap sesi adalah menanyakan bidang dan jenis riset Anda, lalu memuat konvensi
yang sesuai. Kalibrasinya nyata, bukan basa-basi:

- **Kekuatan klaim.** Natural dan life sciences paling berani memakai *boosters* (*show*,
  *demonstrate*); matematika dan physical sciences paling hemat; humaniora paling banyak
  *hedging*. Menyeragamkannya membuat naskah terbaca salah kamar.
- **Struktur.** IMRaD bukan hukum alam. Matematika murni memakai konvensi teorema-bukti; ilmu
  komputer sering IDBRC; humaniora kerap *essay-style*. Tidak ada yang dipaksa.
- **Standar pelaporan.** Mengikuti jenis riset, bukan bidang: CONSORT, PRISMA, COREQ, SRQR,
  GRAMMS, APA JARS — dipilihkan sesuai desain yang Anda pakai.
- **Bahasa.** Percakapan mengikuti bahasa Anda; naskah mengikuti jurnal target. Keduanya
  terpisah — Anda bisa berdiskusi dalam bahasa Indonesia untuk naskah berbahasa Inggris.

Untuk korpus non-Inggris, jalur pencarian dan penilaian mutunya disesuaikan alih-alih dipaksakan
— lihat [slr-cowork](slr-cowork.md) dan [Tanya jawab](Tanya-jawab.md).

## Yang membedakannya

**Gerbang yang berhenti, bukan daftar yang panjang.** `submit` berjalan berurutan dari yang
termurah dan paling mematikan. Satu temuan fatal membuat sisanya tidak relevan: ia berhenti,
melaporkan, dan tidak lanjut menyisir. Percuma memoles tanda hubung pada naskah yang scope-nya
salah jurnal.

**Yang bisa dihitung, dihitung.** Akronim, ejaan, nilai p, satuan, batas kata, silang sitasi
dua arah, aritmetika kaskade PRISMA — semuanya dikerjakan skrip deterministik yang bisa Anda
jalankan ulang, bukan dinilai dari kesan.

**Sitasi tidak pernah dikarang.** Verifikasi berjenjang: MCP bila ada, lalu resolusi DOI, lalu
penandaan eksplisit **"belum terverifikasi"**. Yang tidak boleh dilanggar di ketiga tingkat:
sitasi tidak pernah dianggap benar karena "terlihat masuk akal" — kombinasi penulis-tahun-jurnal
yang tampak wajar justru pola khas sitasi karangan.

**Penyuntingan tidak boleh menghilangkan bukti.** `polish-manuscript` punya gerbang fidelitas:
tiap angka dan tiap sitasi yang ada sebelum penyuntingan **wajib** masih ada sesudahnya. Bila
hilang, bagian itu dikembalikan dan dilaporkan — bukan diperbaiki diam-diam.

**Langkah yang tak bisa dijalankan tidak dianggap lolos.** Skrip gagal jalan dilaporkan sebagai
langkah yang dilewati, bukan sebagai "naskah bermasalah". Keduanya tidak pernah dicampur dalam
satu tabel temuan — dan skill diminta menyebutkan apa yang dilewati, bukan mendiamkannya.

**Tiap skill berdiri sendiri.** Berfungsi penuh sendirian. Bila tetangganya terpasang, sebagian
langkah jadi lebih dalam — tetapi tidak ada yang macet karena skill lain tidak ada.

---

[Pemasangan](Pemasangan.md) · [Alur kerja](Alur-kerja.md) · [Prasyarat](Prasyarat.md) · [Tanya jawab](Tanya-jawab.md) · [Lisensi](Lisensi.md)

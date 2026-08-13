# Integritas (G4) & Anonimitas (G5)

Dua gerbang yang paling sering diabaikan penulis dan paling cepat mematikan naskah.
Kegagalan di sini bukan soal mutu — dan sebagian tidak bisa ditambal dengan revisi.

---

## G4 · Integritas

### Similarity index — bukan bagian gerbang ini

Skill ini **tidak menilai similarity index** dan tidak boleh berpura-pura menilainya.
Tanpa Turnitin/iThenticate angkanya tidak bisa dihitung, dan gerbang yang jawabannya
selalu "tidak bisa dinilai" hanya menambah baris kosong di tiap laporan.

Yang benar: perlakukan sebagai **butir tindakan pra-submisi** di T5
(`references/paket-submisi.md`), sejajar dengan mengurus ORCID — pekerjaan user, bukan
putusan skill. Sebutkan sekali di daftar tindakan, lalu lanjut; jangan menjadikannya
temuan, jangan memberinya vonis.

Yang **boleh** disampaikan bila user bertanya, sebagai pengetahuan, bukan penilaian:
ambang lazim total <15–20% dan <5% dari satu sumber tunggal (naskah 12% pun ditolak bila
9%-nya dari satu artikel); bagian paling berisiko biasanya Methods, definisi konsep baku,
dan deskripsi instrumen; serta **self-plagiarism dihitung sebagai plagiarisme** — metode
yang identik dengan artikel penulis sebelumnya harus diparafrase dan artikel lamanya
disitir. Yang terakhir ini berkelindan dengan salami slicing di bawah, yang memang
bisa dinilai dari jawaban user.

### Duplicate submission & salami slicing

- **Duplicate submission** — satu naskah tidak boleh berada di dua jurnal sekaligus.
  Ini pelanggaran serius, bukan sekadar desk reject; bisa berujung blacklist penerbit.
- **Salami slicing** — memecah satu riset menjadi beberapa artikel "terkecil yang bisa
  diterbitkan". Tanyakan: apakah ada artikel lain dari dataset yang sama? Bila ya, harus
  disebutkan di cover letter beserta apa yang membedakannya.

### Preprint

Kebijakan berbeda tajam antar jurnal. Cek eksplisit di guidelines: sebagian menerima
preprint tanpa syarat, sebagian mewajibkan pengungkapan, sebagian menolak naskah yang
sudah beredar. Bila naskah sudah jadi preprint, ini **wajib** disebut di cover letter.

### Pengungkapan penggunaan AI

Sebagian besar penerbit besar kini mewajibkan pernyataan bila AI generatif dipakai dalam
penulisan. Aturan yang berlaku umum:

- AI **tidak boleh** dicantumkan sebagai penulis
- Penggunaannya untuk penulisan/penyuntingan harus diungkap di section khusus
- Penulis tetap bertanggung jawab penuh atas seluruh isi

Kewajiban mengungkapkan ini **berdiri sendiri** — tidak menuntut skill lain. Yang diperiksa di
sini: apakah pemakaian AI diungkap di section yang benar, sesuai kebijakan jurnal target.

*Bila skill `nulis` terpasang*, `~/.claude/skills/nulis/ai-stylometry-flags.md` melengkapinya dari
sisi lain — daftar kanonik penanda **gaya** teks AI, dirujuk juga oleh dimensi 6
`polish-manuscript`. Keduanya menjawab pertanyaan berbeda: yang itu *apakah teksnya berbau AI*,
yang ini *apakah pemakaiannya diungkapkan*. Naskah bisa lolos satu dan gagal yang lain.

---

## G5 · Anonimitas (double-blind)

Hanya berlaku bila jurnal memakai double-blind review. Sekali identitas bocor, naskah
dikembalikan untuk diperbaiki — dan waktu antrean hilang.

### Yang diperiksa script

`scripts/sweep.py --authors "..."` menandai:

- nama penulis di badan naskah
- frasa pembocor: "penelitian kami sebelumnya", "in our previous work/study",
  "as we showed in", "our earlier paper"
- nama afiliasi/institusi
- URL repositori yang memuat identitas (github.com/nama-penulis, situs lab)
- **metadata `.docx`** — `dc:creator` dan `lastModifiedBy` dibaca langsung dari
  `docProps/core.xml` (bagian 8 laporan), berikut tracked changes & komentar yang
  tertinggal. Bersihkan sebelum unggah.

### Yang harus diperiksa manual

Script tidak bisa melihat ini:

- **Metadata PDF** — tersimpan di properti dokumen, di luar jangkauan script.
  Periksa dan bersihkan sendiri bila yang diunggah PDF.
- **Acknowledgements** — hampir selalu membocorkan institusi dan nomor hibah. Umumnya
  harus dihapus dari naskah anonim dan dipindah ke title page terpisah.
- **Nomor hibah** — sering bisa dilacak balik ke penulis.
- **Caption figur & watermark** di dalam gambar.
- **Nomor persetujuan etik** — bisa mengidentifikasi institusi. Sebagian jurnal minta
  disamarkan pada naskah anonim; cek guidelines.
- **Rasio sitasi-diri yang mencolok** — menyitir satu penulis sepuluh kali sama saja
  menuliskan namanya.

### Cara menyitir karya sendiri secara anonim

Jangan menghapus sitasinya — itu merusak naskah dan mudah ketahuan. Ubah rujukannya
menjadi orang ketiga:

> ~~"Dalam penelitian kami sebelumnya [12], kami menemukan…"~~
> "Penelitian terdahulu [12] menemukan…"

Sitasi tetap ada di daftar pustaka; yang dibuang hanya kepemilikannya di badan teks.

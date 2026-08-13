# Paket Revisi (Tahap 5)

Revisi yang baik masih bisa tertahan di editorial office karena berkasnya tidak lengkap
atau tidak sesuai permintaan. Semua di bawah murah dikerjakan.

## Tiga berkas, bukan satu

1. **Surat tanggapan** (*response to reviewers*) — dokumen terpisah, bukan bagian dari
   naskah, dan bukan email. Formatnya di `menanggapi.md`.
2. **Naskah bertanda** — perubahan terlihat: tracked changes, teks berwarna, atau
   `latexdiff` untuk LaTeX. Ini yang dipakai reviewer memeriksa.
3. **Naskah bersih** — semua perubahan diterima, tanpa markah. Ini yang dipakai
   memproduksi artikel.

Jangan pernah mengirim hanya naskah bersih dengan alasan "perubahannya sudah dijelaskan
di surat". Editor akan meminta versi bertanda dan Anda kehilangan satu putaran waktu.

Untuk LaTeX, `latexdiff naskah-lama.tex naskah-baru.tex > naskah-bertanda.tex`
menghasilkan versi bertanda yang rapi. Periksa hasil kompilasinya — `latexdiff` sering
merusak tabel dan lingkungan matematika kompleks, dan itu harus dibereskan manual
sebelum dikirim.

## Surat pengantar ke editor

Pendek, satu halaman, terpisah dari surat tanggapan. Empat paragraf:

1. Nomor naskah, judul, dan jenis revisi yang diminta.
2. **Ringkasan perubahan terbesar** — tiga sampai lima kalimat, menyebut yang
   substantif saja (analisis diganti, section ditulis ulang, data ditambah). Editor
   membaca ini untuk memutuskan apakah perlu dikirim ulang ke reviewer.
3. **Butir yang tidak dikerjakan**, bila ada, beserta alasan ringkas — dinyatakan di
   muka, bukan disembunyikan di tengah surat tanggapan.
4. Pernyataan bahwa semua penulis menyetujui versi revisi ini.

Bila editor memberi arahan spesifik di surat keputusannya, sebut eksplisit bahwa arahan
itu sudah diikuti dan di mana.

## Yang berubah di naskah dan mudah terlupa

Revisi mengubah angka dan struktur, dan bagian-bagian ini ikut terpengaruh tanpa
diingat:

- **Abstrak** — hampir selalu perlu diperbarui bila hasil berubah, dan hampir selalu
  terlupa. Angka di abstrak harus cocok dengan Results yang baru.
- **Conclusion** — klaim yang diturunkan di Discussion harus ikut turun di sini.
- **Batas kata** — revisi menambah teks; periksa ulang terhadap batas jurnal.
- **Penomoran figur/tabel** — bila ada yang ditambah atau dibuang, seluruh rujukan
  dalam teks bergeser.
- **Daftar pustaka** — referensi baru dari reviewer harus masuk daftar; referensi dari
  bagian yang dihapus mungkin jadi yatim.
- **Pernyataan wajib** — data availability berubah bila ada data baru; author
  contributions berubah bila ada penulis baru.

**Bila skill `submit` terpasang**, `~/.claude/skills/submit/scripts/sweep.py` menangkap semua ini
sekaligus pada naskah revisi: angka abstrak yang tak cocok, sitasi yang tak nyambung ke daftar
pustaka, figur yatim, batas kata, dan sisa tracked changes yang belum diterima di versi bersih.

**Bila tidak terpasang**, periksa manual dengan urutan yang sama — lima hal itu, satu per satu,
dan yang paling sering terlewat adalah **dua yang terakhir**: batas kata sering terlampaui karena
revisi hampir selalu menambah, dan tracked changes tertinggal karena versi bersih dibuat
terburu-buru menjelang tenggat. Katakan pada user bahwa sapuan mekanisnya dikerjakan manual.

## Penulis baru di tengah revisi

Bila revisi menuntut analisis yang dikerjakan orang baru, penambahan penulis **harus
disetujui editor** dan biasanya memerlukan pernyataan tertulis dari semua penulis. Ini
bukan formalitas: penambahan penulis diam-diam di tahap revisi termasuk pelanggaran
authorship yang bisa membatalkan naskah. Sebutkan di surat pengantar, jangan diam-diam
mengubah halaman judul.

## Daftar periksa sebelum kirim

- [ ] `tanggapan.py cek` bersih — tidak ada butir yang tak dijawab
- [ ] Setiap jawaban menyebut lokasi perubahan yang bisa dibuka
- [ ] Butir yang ditolak punya pengakuan premis + alasan konkret + konsesi
- [ ] Pertentangan antar-reviewer dinyatakan terbuka, bukan dipihak diam-diam
- [ ] Ucapan terima kasih hanya di pembuka
- [ ] Tidak ada frasa yang menyalahkan atau meremehkan reviewer
- [ ] Naskah bertanda **dan** bersih sama-sama disiapkan
- [ ] Naskah bersih benar-benar bersih — tracked changes sudah diterima, komentar
      dihapus, highlight dibuang (script `sweep.py` bagian 8 memeriksanya)
- [ ] Abstrak & Conclusion diperbarui mengikuti hasil yang berubah
- [ ] Batas kata masih terpenuhi setelah penambahan
- [ ] Daftar pustaka konsisten dengan sitasi baru
- [ ] Berkas dinamai sesuai permintaan sistem submisi
- [ ] Untuk double-blind: surat tanggapan juga harus anonim — nama institusi dan
      "in our lab" mudah lolos di sini karena surat ini ditulis terburu-buru
- [ ] Semua penulis membaca versi final dan surat tanggapannya

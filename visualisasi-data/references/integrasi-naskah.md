# Menyisipkan Figur ke Naskah dan Menulis Caption

Figur hanya berguna bila masuk ke naskah dengan benar. Bagian ini menangani
caption, penyisipan LaTeX/Word, dan pemeriksaan silang sebelum submit.

## Caption: empat bagian, urut

Caption yang baik dibaca berdiri sendiri, tanpa badan naskah. Susunannya:

1. **Judul singkat** — frasa, bukan kalimat, diakhiri titik. Ini yang muncul di
   daftar gambar.
2. **Apa yang digambar per panel** — huruf panel disebut eksplisit: "(a) …,
   (b) …". Caption yang menjanjikan panel yang sudah dihapus adalah kesalahan
   yang sering bertahan berputaran-putaran revisi; **cocokkan caption dengan
   panel yang benar-benar ada** setiap kali figur diperbarui.
3. **Konteks statistik** — n dan unit ulangan, konvensi sebaran (SD/SEM/CI 95%/
   IQR), uji yang dipakai dan koreksi perbandingan gandanya, ambang yang
   digambar.
4. **Catatan sumber dan caveat** — asal data, kepanjangan akronim, baris yang
   dieksklusi dan alasannya, penandaan panel ilustratif/skematik.

Contoh:

> **Gambar 3. Topografi perubahan daya theta pada tiga tingkat beban kerja.**
> (a–c) Perubahan daya theta (4–8 Hz) relatif baseline istirahat untuk kondisi
> 1-back, 2-back, dan 3-back. Skala warna sama untuk ketiga panel; nol dipusatkan
> pada tidak-ada-perubahan. Lingkaran putih menandai elektroda yang lolos koreksi
> FDR (q < 0,05; uji-t berpasangan, 14 perbandingan). n = 24 partisipan; nilai
> adalah rerata antar-partisipan. Elektroda digambar pada posisi montase 10-20;
> dua partisipan dikeluarkan karena artefak > 40% epoch.

## Yang tidak boleh ada di caption

- **Interpretasi yang seharusnya di Results/Discussion.** Caption menjelaskan
  apa yang tergambar, bukan berargumen.
- **Informasi yang seharusnya terbaca dari figur** (aturan 2.1). Bila caption
  harus menjelaskan garis mana yang mana, figurnya kurang label.
- **Angka yang berbeda dari badan naskah.** Satu klaim satu angka kanonik.

## LaTeX

```latex
\\begin{figure}[tb]
  \\centering
  \\includegraphics[width=\\linewidth]{figures/fig3_topografi_theta.pdf}
  \\caption{...}
  \\label{fig:topo}
\\end{figure}
```

- Sisipkan **PDF**, bukan PNG. PNG hanya untuk pratinjau cepat.
- `width=\\linewidth` (satu kolom) atau `figure*` + `\\textwidth` (dua kolom).
  **Jangan menskala dengan faktor sembarang** (`scale=0.8`) — itu mengubah
  ukuran font efektif dan bisa menembus batas 7 pt. Gambar ulang pada ukuran
  yang benar.
- Setiap `\\label` harus dirujuk `\\ref` di badan naskah, dan sebaliknya.

## Word / DOCX

- Sisipkan PNG 300+ dpi atau EMF/PDF bila jurnal menerimanya.
- Set ukuran gambar dalam sentimeter di Word (**bukan** persen), sesuai lebar
  kolom, lalu kunci rasio aspek.
- Banyak jurnal meminta figur sebagai **file terpisah** plus daftar caption di
  akhir naskah. Cek author guidelines.

## Pemeriksaan silang sebelum submit

Jalankan ini setiap kali figur atau angka berubah:

1. **Setiap figur dirujuk di teks**, urut nomor kemunculan pertama.
2. **Setiap rujukan `\\ref`/"Gambar N" punya figurnya.** Skill `submit`
   (`scripts/sweep.py`) mendeteksi caption yatim dan rujukan menggantung.
3. **Angka di figur = angka di tabel = angka di abstrak.** Bila figur dan tabel
   dibangun dari berkas agregat yang sama, ini otomatis; bila tidak, periksa
   manual.
4. **Caption menyebut panel yang benar-benar ada.**
5. **Kompilasi naskah dan lihat PDF akhirnya.** Ini pemeriksaan terakhir yang
   tidak boleh dilewati: figur yang bagus di workspace bisa berubah setelah
   LaTeX menskalanya, dan font 7 pt bisa jadi 5 pt tanpa peringatan.
6. **Kepatuhan author guidelines**: format file, resolusi minimum, mode warna
   (RGB/CMYK), biaya figur berwarna, dan apakah figur harus dapat dibaca dalam
   grayscale. Beberapa jurnal masih mencetak hitam-putih — bila demikian,
   pastikan setiap deret dibedakan juga oleh bentuk marker atau pola garis,
   bukan warna saja.

## Data di balik figur

Makin banyak jurnal mensyaratkan data sumber figur. Simpan satu berkas per
figur (`figures/fig3_source.csv`) berisi angka yang benar-benar digambar, dan
sebutkan di pernyataan ketersediaan data. Ini juga yang membuat figur dapat
dibangun ulang oleh reviewer atau oleh diri sendiri enam bulan kemudian.

## Nomor dan urutan

- Nomor figur mengikuti urutan **kemunculan pertama di teks**, bukan urutan
  pembuatan.
- Figur suplemen diberi awalan terpisah (S1, S2) dan tidak ikut penomoran utama.
- Bila satu panel pindah ke figur lain saat revisi, perbarui: nomor, caption,
  rujukan di teks, dan label internal panel. Keempatnya, bukan hanya satu.

# Aturan Kebenaran Figur

Baca sebelum render final, apa pun domainnya. Bagian 1–3 dan 8–9 adalah
**kebenaran** — berlaku mutlak, tidak ada isi estetikanya. Bagian 4–7 adalah
**panduan** — default yang menghasilkan figur bersih, boleh ditimpa oleh
keputusan sadar, kecuali butir yang menyatakan fakta perseptual (4.4, 4.5, 6.9).

---

## 1. Fidelitas data

**1.1 Baris yang dieksklusi.** Baris yang ditandai gugur/outlier/gagal QC
dihilangkan sama sekali, atau digambar dengan penanda terbuka/arsir yang berbeda
dan dinamai di keterangan. Ia **tidak pernah** ikut masuk ke statistik ringkas
yang digambar bersama baris yang disertakan.

**1.2 Hanya kondisi yang sebanding.** Lengan/kondisi yang diukur dengan n,
protokol, atau anggaran epoch berbeda tidak digambar sebagai sejajar. Pisahkan
dengan facet atau penanda pada label, dan nyatakan bedanya sekali di caption.

**1.3 Konsistensi internal.** Setiap keterangan, ambang, dan judul di dalam
figur harus terpenuhi oleh setiap baris yang digambar. Sebelum menyimpan,
telusuri tiap label kategori balik ke aturan yang mendefinisikannya. Bila ada
baris yang nilainya bertentangan dengan labelnya, **figurnya yang salah, bukan
datanya**.

**1.4 Judul-klaim harus benar.** Judul berbentuk kalimat diuji terhadap setiap
kategori di sumbu sebelum render. Bila ada satu saja yang bertentangan, beri
kualifikasi ("pada 3 dari 4 pasangan") atau turunkan jadi judul deskriptif.

**1.5 Nyatakan n dan apa yang dikontrol.** Setiap panel yang menggambar tanda
ringkas menyatakan n dan unit ulangannya (subjek? trial? seed? fold?). Setiap
small multiple yang menahan satu variabel menyatakan nilai yang ditahan.

**1.6 Struktur rujukan diambil dari rujukan.** Pohon, urutan, batas wilayah,
atau topologi yang digambar sebagai **konteks** memakai sumber standar, bukan
hasil inferensi dari data yang sedang digambar. Inferensi hanya sah bila
strukturnya memang *hasil* penelitian.

**1.7 Satu klaim satu angka.** Akurasi, runtime, prevalensi — satu nilai kanonik
yang sama di setiap panel, caption, tabel, dan abstrak. Tentukan definisinya
lalu pakai angka itu di mana-mana.

**1.8 Figur dan tabel membaca sumber yang sama.** Ambil angka dari berkas
agregat yang sama dengan yang dibaca tabel naskah. Kesalahan paling umum yang
lolos ke proofread: figur masih menampilkan hasil satu kali jalan sementara
tabel sudah pindah ke rerata multi-seed.

---

## 2. Ketidakpastian — lapis yang paling sering hilang

**2.1 Bar rerata polos dilarang** bila kuantitasnya punya ulangan. Pilih sesuai
n: n < 25 → titik individual dengan tanda median/rerata; n besar → box atau
violin; bila rerata memang pesan utamanya → bar + selang kepercayaan. Error bar
dan overlay titik mentah adalah alternatif, bukan pasangan.

**2.2 Sebutkan konvensinya.** "Mean ± SD", "mean ± SEM", "median (IQR)", "CI
95%" — tulis yang mana, di caption. SD, SEM, dan CI 95% berbeda faktor besar;
pembaca tidak boleh menebak.

**2.3 Multi-seed / multi-fold digambar, bukan diklaim.** Bila kuantitas dihitung
ulang lintas seed, gambar tiap seed sebagai garis tipis di belakang rerata
(`spread_lines` lalu `mean_line`). Jangan menyatakan "stabil lintas seed" dalam
prosa untuk hal yang bisa ditunjukkan figur.

**2.4 Hasil tak signifikan tetap dilaporkan.** `sig_stars(p)` mengembalikan
`"n.s."` — itu hasil. Bila satu panel membandingkan lengan yang tidak lolos
koreksi (FDR/Bonferroni), **judul panel harus mengatakannya**.

**2.5 Sebutkan koreksi perbandingan ganda.** Bila ada banyak uji (per elektroda,
per wilayah, per gen), nyatakan metode koreksinya dan gambarkan ambang setelah
koreksi, bukan p mentah.

---

## 3. Sumbu, skala, small multiples

**3.1 Padding.** Batas sumbu memberi jarak minimal satu radius marker dari data
di semua sisi. `ax.margins(0.04)` setelah plotting.

**3.2 Rentang terbuang.** Bila data menempati <40% rentang sumbu, potong sumbu
atau mulai dari lantai data dengan tick non-nol yang jelas. **Jangan pernah**
menggambar garis referensi atau anotasi di dalam celah potongan — celah itu
tidak punya koordinat.

**3.3 Sumbu log.** Tick terbaca manusia (`10²`, `1k`), bukan eksponen mentah.
**Jangan pernah** bar terisi pada sumbu nilai berskala log — panjang bar
mengkodekan rasio terhadap lantai sembarang. Pakai titik + tanda median.

**3.4 Sumbu bersama.** Sederet small multiples menampilkan label tick sekali
(panel paling kiri/bawah); panel dalam tetap punya tick tanpa label.

**3.5 Isi kotaknya.** Selubung data menempati ≥75% persegi panjang panelnya.
Bila aspek alaminya menyisakan pita kosong, ubah gridnya — jangan memberi
padding pada panel.

**3.6 Arah "lebih baik".** Bila tidak jelas dari label sumbu apakah tinggi atau
rendah yang lebih baik, beri isyarat kecil tegak ("lebih tinggi = lebih baik")
sekali per baris panel — bukan hanya di caption.

**3.7 Lebar fisik.** Figur dirancang pada lebar kolom jurnal target. Menambah
skema atau label tidak boleh membuat panel data lebih sempit dari sebelumnya.

---

## 4. Warna

**4.1 Pengikatan.** Sekali sebuah warna terikat pada satu entitas (metode,
kondisi, kelompok), warna persis itu dipakai untuk setiap tanda yang mewakili
entitas tersebut di seluruh figur dan seluruh naskah — garis, isian, marker,
teks, baris heatmap. Warna **adalah** rujukan silang; pembaca tidak boleh perlu
membuka legenda dua kali.

**4.2 Batasi jumlah hue.** Sesedikit yang data butuhkan. Bila figur
membandingkan satu deret fokal terhadap pembanding, deret fokal digambar pekat
dan berbobot; pembanding abu-abu/pudar. Mata harus menemukan kontribusi studi
ini lebih dulu.

**4.3 Kategori bertingkat.** Bila kategori bersarang, tingkat luar memilih
keluarga hue, tingkat dalam mengambil sampel di dalamnya (`ramp(hue, n)`).

**4.4 Kontinu dan divergen.** Sekuensial perseptual-uniform (`viridis`,
`magma`) untuk besaran satu arah; ramp satu hue untuk peringkat ordinal;
divergen (`RdBu_r`, `PuOr`) untuk kuantitas bertanda — **selalu** dipusatkan
pada nol yang bermakna (0, 1.0, atau median rujukan), bukan titik tengah data.

**4.5 Aman buta warna.** Jangan pernah kontras merah/hijau untuk dua hal yang
diperlawankan. Sisakan satu hue alarm untuk penanda galat/anomali dan jangan
pakai ulang sebagai warna deret data. Uji dengan `cvd_check()`. Jangan pakai
`jet`/`rainbow` — gradasinya tidak perseptual-uniform dan menciptakan tepi palsu.

**4.6 Dua palet, dua legenda.** Bila satu figur memakai dua sistem warna
kategorikal, tiap legenda diletakkan berdampingan dengan panel pertama tempat
paletnya berlaku.

---

## 5. Tipografi

**5.1 Judul kalimat.** Judul panel menyatakan perbandingannya dalam bahasa
biasa, berat normal, rata kiri. Nama metrik ada di sumbu, bukan di judul.

**5.2 Tiga ukuran font saja**, dipetakan ke peran bukan ke ruang kosong:
judul/label sumbu/identitas deret pada ukuran dasar; legenda/anotasi satu
tingkat lebih kecil; label tick satu tingkat lagi. Huruf panel satu-satunya
pengecualian (tebal, lebih besar). Bila label tidak muat, perbaiki tata letak
atau perpendek teksnya — jangan mengambil ukuran antara.
`apply_style(sizes=(8,7,6))`.

**5.3 Ukuran minimum pada ukuran cetak.** Setelah figur diperkecil ke lebar
kolom, font terkecil tetap ≥7 pt. Ini alasan `new_figure(width=...)`
mengembalikan ukuran fisik sebenarnya: gambar pada ukuran akhir, jangan
menskala setelahnya.

**5.4 Nomenklatur.** Nama spesies, gen, dan variabel yang konvensinya dimiringkan
tetap dimiringkan. Akronim diperluas sekali pada kemunculan pertama.

**5.5 Angka pada tanda.** Maksimal 2 angka penting, dan hanya untuk angka utama
yang akan dikutip pembaca. Sisanya dibaca dari sumbu. Teks di atas bidang
berwarna harus kontras ≥4.5:1; kalau tidak, letakkan di luar bidang.

**5.6 Tanpa kode internal.** Label sumbu memakai nama bahasa manusia; singkatan
dari kode program hanya boleh muncul dalam kurung setelah nama terbaca.
Pembanding dilabeli dengan **apa** dia, bukan perannya ("montase 58 kanal",
bukan "baseline").

**5.7 Huruf panel.** Tebal, kiri atas, di luar kotak sumbu. Huruf besar/kecil
mengikuti konvensi jurnal target.

---

## 6. Bentuk grafik menurut bentuk data

**6.1 Kategorikal × numerik.** Tampilkan sebarannya, bukan hanya ringkasannya
(lihat 2.1). Kategori yang tidak ada di satu kelompok ditandai (`n.d.`, `—`,
atau bayangan arsir) di slotnya — slot kosong terbaca sebagai nol. Bar bernilai
nol diberi stub/titik yang terlihat di garis dasar.

**6.2 Kategori dengan satu observasi.** Titik terisi dengan tangkai tipis ke nol
semantik (lollipop), bukan bar.

**6.3 Deret kontinu.** Rerata-per-x sebagai garis bermarker; run individual
sebagai garis tipis transparan di belakangnya. Label tiap deret dengan teks
langsung di ujung kanan garisnya, lebih baik daripada kotak legenda.

**6.4 Distribusi pada dukungan yang sama.** Bila dua distribusi banyak
bertumpang, susun sebagai panel kecil bersumbu-x sama atau ridgeline. Tumpuk
hanya bila pemisahannya jelas.

**6.5 Matriks.** Heatmap di bawah ~200 sel: cetak nilainya di setiap sel.
Nyatakan ambangnya sekali di label colorbar.

**6.6 Embedding.** Scatter reduksi dimensi (UMAP, t-SNE, PCA) membuang tick dan
label tick; sepasang panah kecil di sudut menamai sumbunya. Klaster dilabeli
dengan garis penunjuk tipis ke teks di ruang kosong.

**6.7 Prediksi vs observasi berpasangan.** Susun sebagai dua jalur bersebelahan
dengan x dan warna identik; biarkan kesejajarannya yang membawa perbandingan.

**6.8 Inset.** Hubungkan inset detail ke wilayah sumbernya secara terlihat —
kotak pembatas dengan garis penghubung.

**6.9 Labeli ekstremnya.** Pada scatter observasi bernama, labeli langsung
minimal maksimum, minimum, dan titik yang ditandai. Setelah render, pastikan
setiap ujung garis penunjuk berakhir dalam satu radius marker dari baris yang
dinamainya.

---

## 7. Tata letak dan narasi

**7.1 Tunjukkan apa yang diukur sebelum hasilnya.** Pembaca harus paham apa yang
dibandingkan sebelum melihat perbandingannya — lewat judul bahasa biasa, skema
berlabel, atau urutan panel. Skema memakai kata dan glif yang sama dengan label
panel data.

**7.2 Satu figur, satu pesan.** Figur multi-panel punya satu kalimat yang ingin
dibuat benar. Setiap panel menyatakan, mendukung, atau membatasi kalimat itu;
panel yang tidak melakukan ketiganya pindah ke suplemen.

**7.3 Legenda di ruang kosong.** Tanpa bingkai, di dalam ruang kosong alami
figur, atau diganti pelabelan langsung.

**7.4 Header pita untuk faceting bersarang.** Satu header membentang per
kelompok, bukan judul berulang di tiap panel.

**7.5 Busur figur naskah.** Figur 1 mewujudkan pitch satu kalimat paper sebagai
data (cakupan, bukan arsitektur perangkat lunak). Figur berikutnya: mekanisme →
bukti → robustness → aplikasi.

**7.6 Jangan mendekor ulang panel yang sudah lolos.** Antar putaran revisi,
panel yang sudah benar tidak dibuat lebih ramai untuk memperbaiki apa pun.

---

## 8. Anti-pola (kesalahan, bukan selera)

- Merah dan hijau sebagai dua kategori yang diperlawankan.
- Colormap `jet`/`rainbow`.
- Bar terisi pada sumbu nilai berskala log.
- Colormap divergen yang pusatnya titik tengah data, bukan nol semantik.
- Sumbu-y bar chart yang tidak mulai dari nol (memperbesar beda secara visual).
- Bar rerata tanpa sebaran padahal ada ulangan.
- Pie chart untuk lebih dari tiga irisan, atau pie 3D dalam bentuk apa pun.
- Sumbu-y ganda dengan skala berbeda pada satu panel (korelasi semu).
- Judul sumbu yang hanya mengulang label tick.
- Arah "lebih baik" yang hanya dijelaskan di caption.
- Garis "referensi" yang digambar pada nilai yang justru salah satu titik data.
- Baris yang dieksklusi tapi ikut masuk statistik ringkas.
- Garis penunjuk yang tanda terdekatnya bukan baris yang dilabelinya.
- Teks figur yang tidak terbaca setelah diperkecil ke lebar kolom.

---

## 9. Verifikasi setelah render

**9.1 Cek geometris.**

```python
check_overlaps(fig, "fig2")     # tumpang-tindih teks/spine + teks keluar kanvas
```

Perbaiki (geser, perpendek, selang-seling) lalu simpan ulang sampai bersih.

**9.2 Cek perseptual.** Cek geometris tidak menangkap label berkontras rendah,
penunjuk yang saling menyilang, atau warna deret yang tertukar. **Lihat PNG-nya**
panel per panel:

- Apakah setiap glif terbaca di atas latarnya?
- Apakah elemen terkecil punya garis tepi atau stub?
- Adakah garis penunjuk yang menyilang?
- Bisakah satu warna deret dikira warna deret lain?
- Apakah legenda berada di dekat yang dijelaskannya?

**9.3 Cek cetak.**

```bash
python scripts/figcheck.py figures/fig2.png --kolom single
```

Memeriksa: DPI, lebar fisik terhadap lebar kolom, dan keberadaan pasangan vektor.

**9.4 Cek terakhir — di dokumen jadi.** Kompilasi naskah, lalu lihat figur di
PDF akhir. Figur yang bagus di workspace bisa jadi buruk setelah LaTeX
menskalanya.

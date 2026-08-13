# Konsistensi Internal (T0)

Editor jarang mendesk-reject naskah karena satu inkonsistensi. Ia mendesk-reject karena
inkonsistensi itu **memberitahunya sesuatu**: penulis tidak membaca ulang naskahnya
sendiri. Setelah kesimpulan itu terbentuk, sisa naskah dibaca dengan curiga.

Karena itu T0 dijalankan sebelum T1: gaya sitasi yang salah menandakan penulis tidak
membaca guidelines; sitasi yang tidak nyambung ke daftar pustaka menandakan penulis tidak
membaca naskahnya. Yang kedua lebih mematikan.

## Yang dihitung script

`scripts/sweep.py` menutup lima dari enam keluarga di bawah secara mekanis. Jalankan
dulu, baru nilai sisanya dengan mata.

### K1 · Sitasi ↔ daftar pustaka (bagian 4 laporan)

Disilang **dua arah**, karena keduanya temuan yang berbeda:

- **Disitir tapi tak ada di pustaka** — `[23]` pada naskah dengan 19 entri, atau
  `(Elmira et al., 2022)` yang tak punya entri. Ini yang paling telanjang.
- **Entri tak pernah disitir** — sisa dari draf sebelumnya, atau referensi yang
  ditambahkan demi menyenangkan reviewer jurnal sebelumnya. Editor membacanya sebagai
  naskah daur ulang.
- **Penomoran tidak berurutan** — pada gaya numerik, banyak guidelines (Vancouver, IEEE,
  sebagian besar jurnal Elsevier) menuntut nomor urut sesuai penyebutan pertama. Naskah
  yang dimulai dengan `[3]` biasanya hasil menyusun ulang paragraf tanpa memperbarui
  nomor.

Script mengenali tiga gaya: numerik `[n]`, kunci `@key` (hasil konversi `\cite{}` dari
`.tex` — jalankan dengan `--bib` agar bisa disilang), dan penulis-tahun.

**Bila laporan berkata "tidak ada sitasi terdeteksi", jangan lega.** Penyebab paling
umum: sitasi `.docx` masih berupa *field code* Mendeley/Zotero yang tidak ikut terkonversi.
Minta user melakukan *unlink citations* atau kirim PDF-nya, lalu jalankan ulang.

Pada gaya penulis-tahun, pencocokan bersifat perkiraan — ejaan nama yang berbeda antara
badan teks dan daftar pustaka justru salah satu temuan yang dicari, jadi periksa
setiap "tak ada di pustaka" satu per satu sebelum melaporkannya.

### K2 · Angka abstrak ↔ badan naskah (bagian 7)

Editor membaca abstrak lalu melompat ke tabel pertama. Angka yang tidak bertemu di antara
keduanya merusak kredibilitas sebelum reviewer terlibat — dan bagi sebagian editor ini
sinyal *data integrity*, bukan sekadar kecerobohan.

Script menandai angka abstrak yang tak punya pasangan di badan naskah, dengan toleransi
pembulatan. Alarm palsu wajar (satuan berbeda, angka yang memang hanya ada di abstrak
sebagai ringkasan) — verifikasi tiap temuan.

Yang **tidak** terdeteksi script dan harus dibaca sendiri: n yang berbeda antara Methods
dan Results, total kolom tabel yang tidak menjumlah, persentase yang jumlahnya bukan 100,
dan derajat kebebasan yang tak cocok dengan n.

### K3 · Figur/tabel ↔ rujukan teks (bagian 6)

Sudah disapu sejak awal: caption yatim, nomor yang dirujuk tanpa caption, `Figure ??`,
`\ref{}` menggantung. Tambahan yang perlu mata: apakah penomoran mengikuti urutan
penyebutan pertama, dan apakah isi caption cocok dengan yang dikatakan teks tentangnya.

### K4 · Sisa proses penulisan (bagian 8)

`TODO`, `[cite]`, `XXX`, `lorem ipsum`, `\todo{}`. Untuk `.docx`, script juga membuka
berkasnya langsung dan melaporkan tracked changes yang belum diterima, komentar yang
belum dihapus, teks yang masih tersorot, serta `dc:creator` dan `lastModifiedBy` di
metadata — tiga terakhir sekaligus menutup sebagian G5.

Satu komentar tertinggal cukup untuk mengubah kesan "naskah siap" menjadi "naskah draf".

### K5 · Pernyataan wajib ↔ isi naskah

Script hanya memeriksa **keberadaan** tujuh pernyataan (bagian 2), tidak isinya. Yang
harus disilang manual:

| Pernyataan | Disilang dengan |
|---|---|
| Ethics/IRB | nomor persetujuan yang disebut di Methods — harus sama persis |
| Funding | nomor hibah di Acknowledgements, dan afiliasi penyandang dana |
| Data Availability | URL/DOI repositori yang dijanjikan — buka betulan, pastikan hidup dan tidak *private* |
| Author Contributions | daftar penulis di halaman judul — jangan ada nama yang hilang atau berlebih |
| Conflict of Interest | afiliasi & pendanaan yang diungkap di tempat lain |
| Informed consent | ada-tidaknya partisipan manusia menurut Methods |

Data Availability yang menunjuk repositori tertutup adalah temuan yang sering muncul dan
selalu dikembalikan.

## Yang perlu mata, bukan script

### K6 · Konsistensi lintas berkas submisi

Sistem submisi menyimpan judul, daftar penulis, dan abstrak **terpisah** dari berkas
naskah. Editorial office membandingkannya. Yang harus identik:

- **Judul** — di sistem submisi, halaman judul, naskah, dan cover letter. Beda satu kata
  pun terbaca sebagai naskah yang disalin dari submisi sebelumnya.
- **Daftar dan urutan penulis** — di sistem, halaman judul, dan Author Contributions.
  Beda satu nama antara sistem dan naskah biasanya dikembalikan sebelum editor melihatnya.
- **Corresponding author** — satu orang yang sama di semua tempat, dengan email yang sama.
- **Abstrak** — yang ditempel di sistem submisi sering versi lama.
- **Nama jurnal di cover letter** — kesalahan klasik pada naskah yang sedang berkeliling;
  editor membacanya sebagai penolakan dari tempat lain.
- **Afiliasi** — konsisten antar penulis dan dengan nomor persetujuan etik.

Ini seluruhnya administratif, nol kaitan dengan mutu, dan setiap butirnya cukup untuk
memulangkan naskah tanpa dibaca.

### Klaim yang berpindah

Tiga tempat yang harus mengatakan hal yang sama: **pertanyaan penelitian** di akhir
Introduction, **apa yang diukur** di Methods, dan **apa yang disimpulkan** di Conclusion.
Naskah yang menjanjikan tiga RQ lalu menjawab dua, atau menyimpulkan sesuatu yang tak
pernah diukur, gagal di Tahap 2 (E5) — bukan di sini.

## Batas dengan polish-manuscript

Yang **tidak** dikerjakan T0, karena sudah jadi dimensi 3, 5, dan 6
`polish-manuscript`: konsistensi istilah dan istilah kanonik, akronim yang didefinisikan
dua kali atau tak pernah, tense antar-section, dan ejaan US/UK yang campur.

Itu semua temuan reviewer, bukan temuan editor. Menariknya ke sini akan mengubah gerbang
ini menjadi improvement pass — persis yang dihindari skill ini.

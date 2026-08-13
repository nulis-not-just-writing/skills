# Penelusuran Sitasi & Verifikasi Referensi

Dibaca **sebelum** menjalankan: uji sensitivitas string (Tahap 3), penelusuran sitasi
formal dan gerbang retraksi (akhir Tahap 6), serta verifikasi daftar pustaka (Tahap 9).

## Tentukan perkakas dulu, sebelum mulai

Periksa apa yang benar-benar tersedia — jangan berasumsi, dan jangan pula berhenti karena
yang disebut pertama tidak ada. Urutan pemeriksaan:

1. **Tool MCP** dari server `scholar-paper-search` (Claude Desktop): `get_paper_by_doi`,
   `get_open_access_pdf`, `search_openalex`, `search_crossref`, `search_semantic_scholar`.
   Bekerja tanpa kunci API. Periksa dengan `server_status`.
2. **Fungsi kernel** dari skill pendamping (Claude Science): `skill({skill:
   "literature-review"})` memberi `verify_dois`, `crossref_lookup`, `expand_citations`,
   `search_openalex` — memproses daftar DOI sekaligus. Skill ini **tidak ada di Claude
   Desktop**; jangan mencoba memuatnya di sana.
3. **Manual**: daftar pustaka PDF untuk backward, fitur "cited by" basis data untuk
   forward, doi.org dan situs penerbit untuk verifikasi.

Ketiganya sah. Yang **tidak** sah adalah melewati langkahnya karena perkakas tingkat 1 dan
2 tidak tersedia. Catat di `search_log.md` jalur mana yang dipakai — reviewer menanyakan
metode penelusuran sitasi, dan "manual dari daftar pustaka PDF" adalah jawaban yang
diterima; kekosongan tidak.

---

## Penelusuran sitasi (snowballing) — akhir Tahap 6

**Status: opsional.** JBI tidak mensyaratkan citation chasing, dan PRISMA 2020 hanya
menyediakan jalur pelaporan bila dikerjakan — bukan mewajibkannya. Ini metode pelengkap
yang dipakai ketika ada alasan menduga pencarian basis data belum menjangkau, bukan
langkah rutin yang harus ada di setiap review.

Alasan yang sah untuk menjalankannya: studi benchmark yang sudah diketahui relevan tidak
tertangkap string; bidangnya memakai istilah yang sangat beragam antar-aliran; banyak
literatur bidang itu terbit di kanal yang tidak terindeks. Alasan yang **tidak** sah:
jumlah studi terasa sedikit dan ingin diperbanyak.

Apa pun keputusannya, catat di `search_log.md` — termasuk keputusan untuk tidak
menjalankannya beserta alasannya. Reviewer menanyakan apakah pencarian memadai; keputusan
terdokumentasi adalah jawaban, kekosongan bukan.

Dari 3–5 studi paling relevan (atau seluruh studi INCLUDED bila korpus kecil), lakukan
dua arah:

- **Backward** — telusuri daftar pustaka: menemukan karya fondasional yang menjadi rujukan bersama bidang tersebut.
- **Forward** — telusuri yang menyitasi: menemukan karya terbaru yang memperluas atau membantah temuan.

```python
hasil = expand_citations("10.xxxx/xxxxx", n_backward=50, n_forward=15)
```

Kandidat baru **masuk ke alur screening yang sama** dengan kriteria dan screener yang
sama — jangan dimasukkan langsung sebagai INCLUDED.

### Bila dijalankan: putaran kedua adalah kolom paralel

Kandidat dari penelusuran sitasi menjalani title/abstract → akuisisi → teks lengkap, persis
seperti kolam utama. Terasa seperti mengulang pekerjaan, tetapi PRISMA 2020 memang
menggambarkannya sebagai **kolom paralel** — itu sebabnya diagramnya punya dua sisi.

Kelola dengan tiga aturan:

- **Hitungan terpisah sejak identifikasi.** Buat blok tersendiri di `search_log.md`: identified → screened → sought → assessed → included, khusus jalur ini. Menggabungkannya ke hitungan basis data membuat diagram tidak dapat direkonsiliasi, dan itu ketahuan saat audit numerik.
- **κ tidak dihitung ulang dari nol.** Kriteria dan screener-nya sama, jadi kesepakatan jalur ini dilaporkan sebagai bagian dari κ tahap yang bersangkutan. Bila jumlahnya cukup besar (>20 record), laporkan κ terpisah sebagai pemeriksaan konsistensi.
- **Berhenti saat jenuh.** Satu putaran penuh tanpa studi baru yang lolos = korpus jenuh. Laporkan itu di Methods — kejenuhan adalah bukti kecukupan pencarian, bukan sekadar catatan prosedural.

**Pelaporan PRISMA 2020.** Diagram memisahkan dua jalur identifikasi: lewat basis
data/registri, dan lewat **metode lain** (penelusuran sitasi, situs organisasi, kontak
pakar). Studi hasil snowballing dihitung di jalur kedua.

Perkakas mengikuti tangga di awal berkas ini. `expand_citations` (Claude Science)
mengerjakan dua arah sekaligus tetapi menuntut kunci OpenAlex; `search_openalex` /
`search_semantic_scholar` (Claude Desktop) bekerja tanpa kunci; jalur manual memakai daftar
pustaka PDF untuk backward dan fitur "cited by" basis data untuk forward. Apa pun yang
dipakai, catat metodenya di `search_log.md` — itu yang ditanyakan reviewer, bukan
perkakasnya.

---

## Pemeriksaan retraksi — gerbang wajib sebelum sintesis

Studi yang sudah dicabut atau diberi *expression of concern*, bila ikut disintesis, akan
mencemari kesimpulan dan sangat merusak bila ditemukan reviewer. Jalankan pemeriksaan ini
di **akhir Tahap 6** (setelah daftar INCLUDED final) dan ulangi **sebelum submit**:

Periksa tiap DOI dengan tool MCP yang mengembalikan metadata Crossref — hasilnya memuat penanda
retraksi berupa relasi *update-to* Crossref dan/atau awalan judul "RETRACTED". Pada server
`scholar-paper-search` tool-nya `get_paper_by_doi`; pada `paper-search-mcp` padanannya
`get_crossref_paper_by_doi`. Keduanya bekerja tanpa kunci API.

Di Claude Science, satu panggilan memproses seluruh daftar sekaligus:

```python
hasil = verify_dois([daftar_doi_studi_included])
dicabut = [d for d, v in hasil.items() if v.get("retracted")]
```

`verify_dois` membaca metadata CrossRef — termasuk penanda retraksi — dan **tidak
memerlukan kredensial apa pun**.

Bila ada yang dicabut: keluarkan dari sintesis, catat di tabel eksklusi dengan alasan
"retracted", laporkan di Methods, dan periksa apakah temuan berubah. Bila studi itu
tetap dibahas karena alasan tertentu, statusnya wajib dinyatakan eksplisit di teks.

DOI yang mengembalikan `ok: False` berarti tidak resolve — periksa ulang; DOI yang salah
ketik dan DOI yang tidak pernah ada terlihat sama di daftar pustaka.

---

## Verifikasi daftar pustaka — Tahap 9

Ini tahap paling rawan kesalahan dalam seluruh proyek. **Entri referensi tidak pernah
disusun dari nol** — yang dikerjakan hanya memformat, memverifikasi, dan mengaudit
referensi yang sudah ada di dalam teks.

Ganti verifikasi manual satu per satu dengan pemeriksaan terprogram:

```python
hasil = verify_dois(semua_doi_dalam_manuskrip)
```

Setiap entri kembali dengan judul, penulis, tahun, jurnal, dan status retraksi dari
CrossRef. Bandingkan dengan yang tertulis di manuskrip; **nama penulis dan tahun diambil
dari rekaman yang dikembalikan, bukan dari ingatan** — ingatan menyediakan nama yang
masuk akal, bukan nama yang benar.

Untuk referensi tanpa DOI, `crossref_lookup("string referensi lengkap")` mencari
padanannya. Yang tetap tidak ditemukan ditandai untuk diperiksa manual — jangan dibiarkan
lolos dan jangan ditebak.

Tiga audit dijalankan berurutan atas hasil yang sama:

1. **Kelengkapan** — penulis, tahun, judul, jurnal, volume, halaman, DOI sesuai gaya sitasi jurnal target.
2. **Audit temporal** — bandingkan tahun terbit dengan tanggal search di `search_log.md`. Studi primer yang terbit **setelah** tanggal search tidak boleh disitasi sebagai bagian korpus: hapus, atau perbarui search sesuai *update policy*. Sitasi konteks di Introduction/Discussion boleh, tetapi diberi tanda. (Untuk sumber primer hukum, lihat `reference/doctrinal-review.md` — aturannya berbeda.)
3. **Sitasi yatim** — sitasi dalam teks yang tidak punya entri di daftar pustaka, dan sebaliknya.

Simpan tabel hasil verifikasi sebagai artefak; itu bukti kerja yang berguna bila reviewer
mempertanyakan sebuah rujukan.

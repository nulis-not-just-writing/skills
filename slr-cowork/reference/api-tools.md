# Tool API untuk SLR — kapan dipakai, dan batasnya

Dibaca saat menjalankan tahap yang menyentuh basis data: **Tahap 3–4** (pencarian),
**Tahap 6** (akuisisi + retraksi), **Tahap 9** (verifikasi referensi).

Tool tersedia bila server `scholar-paper-search` terpasang. Bila tidak tersedia, seluruh tahap
tetap dapat dijalankan lewat export manual — panduan ini tidak membuat API menjadi syarat.

## Periksa dulu server mana yang benar-benar terpasang

**Jangan menyimpulkan dari nama entri di konfigurasi.** Ada dua server berbeda yang lazim
terdaftar dengan nama pendek `scholar`, dan set tool-nya tidak sama. Periksa tool yang benar-benar
muncul, lalu pakai kolom yang sesuai:

| Yang dicari | `scholar-paper-search` (scholar-node) | `paper-search-mcp` (Python) |
|---|---|---|
| Penanda | ada `elsevier_status`, `server_status` | ada `search_unpaywall`, `download_with_fallback` |
| Pencarian Scopus | `search_scopus`, `scopus_export_csv` | **tidak ada** — export manual scopus.com |
| Pencarian bebas-kunci | `search_openalex`, `search_crossref`, `search_doaj`, `search_europepmc`, `search_pubmed` | `search_openalex`, `search_crossref`, `search_doaj`, `search_europepmc`, `search_pubmed`, `search_core`, `search_google_scholar` |
| Metadata + status retraksi per DOI | `get_paper_by_doi` | `get_crossref_paper_by_doi` |
| Status open access | `get_open_access_pdf` | `search_unpaywall` |
| Akuisisi PDF | `batch_acquire_pdfs` (massal), `download_pdf` | `download_with_fallback`, `download_openalex`, `download_arxiv`, dst. — **per studi, tidak ada mode massal** |
| Abstrak Elsevier | `scopus_abstract`, `sciencedirect_fulltext` | **tidak ada** |
| Simpan teks lengkap ke berkas | `pdf_to_text` | `read_*_paper` mengembalikan teks ke percakapan — simpan sendiri ke `fulltext/<label>.md` |

Konsekuensi bila yang terpasang **paper-search-mcp**: Tahap 3–4 berjalan manual lewat
scopus.com (dan Garuda/Moraref untuk korpus Indonesia); akuisisi batch penutup Tahap 5 disusun
sebagai daftar manual dengan kolom yang sama, bukan sekali jalan; sisa berkas ini tetap berlaku,
termasuk seluruh aturan di bawah. Gerbang retraksi dan verifikasi referensi **tetap otomatis**,
lewat `get_crossref_paper_by_doi`.

Sisa berkas ini memakai penamaan `scholar-paper-search`. Bila server Anda yang lain, ganti nama
tool-nya lewat tabel di atas — aturannya tidak berubah.

## Peta tool (`scholar-paper-search`)

| Tahap | Tool | Kunci |
|---|---|---|
| 3–4 | `search_scopus`, `scopus_export_csv` | Scopus API key |
| 3–4 | `search_openalex`, `search_crossref`, `search_doaj`, `search_europepmc` | tidak perlu |
| 4 | `scopus_abstract` — melengkapi abstrak kosong (dua jalur otomatis) | Scopus/ScienceDirect key |
| 3 | `elsevier_status` — periksa hak akses per API + sisa kuota | kunci apa pun |
| 5→6 | `batch_acquire_pdfs` — akuisisi massal + laporan unduh manual | email kontak (Unpaywall) |
| 6 | `get_open_access_pdf`, `download_pdf`, `read_pdf` | email kontak (Unpaywall) |
| 6 | `download_arxiv`, `read_arxiv_paper` — preprint | tidak perlu |
| 6 | `sciencedirect_fulltext` — hanya konten langganan institusi | ScienceDirect key |
| 6 | `read_pdf` — baca bertahap untuk keputusan include/exclude | tidak perlu |
| 7 | `pdf_to_text` — simpan teks studi INCLUDED sebagai `.md` untuk ekstraksi | tidak perlu |
| 6, 9 | `get_paper_by_doi` — verifikasi metadata + status retraksi via Crossref | tidak perlu |
| 3–4 | `search_semantic_scholar` — penelusuran sitasi | opsional |

Jalankan `elsevier_status` sekali di awal Tahap 3: memastikan kunci terpasang, dan
menampilkan sisa kuota sebelum kuota mingguan terpakai untuk query yang belum final.

## Aturan yang tidak berubah karena adanya API

**Query dilaporkan apa adanya.** `search_scopus` meneruskan sintaks Scopus tanpa
menerjemahkan, sehingga search string di manuskrip identik dengan yang dieksekusi.
Simpan query final, tanggal eksekusi, dan jumlah hits per basis data ke `search_log.md`
segera setelah dijalankan — indeks berubah, dan angka yang tidak dicatat saat itu tidak
dapat direproduksi kemudian.

**Angka identifikasi PRISMA adalah total hits, bukan jumlah record yang terambil.** Query
dengan 1.240 hits yang diambil 200 record tetap dilaporkan 1.240 pada kotak identifikasi;
`scopus_export_csv` mengembalikan keduanya secara terpisah — jangan tertukar.

**Tidak ada tool yang memutuskan include/exclude.** Pencarian, pengambilan metadata, dan
verifikasi boleh diotomatiskan; keputusan penyaringan tidak. Menjalankan penilaian otomatis
dua kali lalu menghitung κ antar keduanya tetap bukan kesepakatan antar-penilai — tidak ada
manusia yang memutuskan apa pun di sana, jadi angkanya mengukur kestabilan keluaran.

Bedakan dari konfigurasi yang **sah**: peneliti sebagai pass pertama, perkakas AI sebagai pass
kedua, dan **tiap baris dikonfirmasi atau dibatalkan peneliti**. Itu opsi (d) pada butir C form
kesepakatan, dan angkanya dilaporkan sebagai *human–AI agreement*. Aturan lengkapnya di SKILL.md.

**Export tanpa abstrak tidak dapat disaring.** Scopus Search API pada view STANDARD tidak
mengembalikan abstrak. Periksa jumlah abstrak kosong yang dilaporkan `scopus_export_csv`
sebelum menutup Tahap 4; lengkapi dengan `fetch_abstracts=true` (memakan kuota) atau
export manual dari scopus.com.

## Akuisisi batch — penutup Tahap 5

Dijalankan sekali atas seluruh daftar INCLUDED, sebelum penilaian teks lengkap dimulai:

```
batch_acquire_pdfs(records=[
  {id: "R001", label: "Chen 2019", doi: "10.xxxx/xxxx"},
  ...
])
```

Yang berhasil disimpan ke `pdfs/`; sisanya masuk `acquisition_report.md` sebagai daftar
**perlu unduh manual** beserta alasan per studi — berbayar, tanpa DOI, DOI salah tulis,
atau tautan mati. Peneliti mengerjakan daftar itu di luar sesi dan menaruh hasilnya di
`pdfs/` dengan nama sesuai kolom Label.

Alasannya dipisahkan dari penilaian: bila akuisisi dikerjakan satu per satu saat menilai,
Tahap 6 terhenti setiap kali menemui artikel berbayar. Dengan batch, peneliti tahu sejak
awal berapa banyak yang perlu diusahakan manual dan dapat mengerjakannya sekaligus.

Studi yang tetap tidak terjangkau setelah seluruh jalur manual dicoba dihitung sebagai
*reports not retrieved* — kotak tersendiri pada PRISMA 2020, **bukan** reason code
eksklusi. Perbarui laporan setelah jalur manual dikerjakan; angka akhirnya yang masuk
diagram.

## Akuisisi per studi — Tahap 6

Untuk studi yang belum terjangkau batch, urutan per DOI, berhenti pada yang pertama
berhasil:

1. `get_open_access_pdf` — cek status open access (Unpaywall bila email kontak diisi, jatuh ke OpenAlex bila tidak). Mengembalikan tautan legal, bukan mengakali paywall.
2. `sciencedirect_fulltext` — untuk DOI Elsevier (`10.1016`) bila kunci terpasang; mengembalikan teks, bukan berkas PDF.
3. `download_arxiv` / `read_arxiv_paper` — preprint.
4. Manual: repositori institusi, Garuda/Moraref/SINTA untuk korpus Indonesia, permintaan ke penulis.

### Membaca: dua kedalaman untuk dua tahap

Kedalaman baca mengikuti keperluan tahapnya — jangan disamakan.

**Tahap 6, penilaian teks lengkap.** Yang diputuskan hanya include/exclude, dan itu
biasanya tuntas dari abstrak, metode, serta bagian yang memuat konstruk inti. Pakai
`read_pdf` dengan `max_chars` terbatas dan lanjutkan `start_char` hanya bila keputusannya
belum jelas. Sebagian besar kandidat tereksklusi — menyimpan teks lengkap seluruh kandidat
di tahap ini adalah pekerjaan yang terbuang, karena hanya sebagian yang akan dibaca lagi.

Yang wajib dicatat cukup: reason code eksklusi, dan **letak bukti** yang mendasarinya
(bagian atau posisi karakter), supaya konflik antar-screener dapat ditelusuri tanpa
membuka ulang berkasnya.

**Tahap 7, ekstraksi.** Barulah simpan teks lengkap studi INCLUDED sebagai berkas:

```
pdf_to_text(source=…, label="Chen 2019", doi="10.xxxx/xxxx")
sciencedirect_fulltext(doi=…, simpan=true, label="Chen 2019")
```

Berkas mendarat di `fulltext/<label>.md` pada folder unduhan, dengan header berisi DOI,
sumber, dan tanggal akses. Alasannya: pada ekstraksi setiap studi dibaca berkali-kali —
per field ekstraksi, per domain quality assessment, lalu saat verifikasi silang dan saat
memeriksa kutipan. Berkas teks membuat pembacaan itu murah, konsisten antar-extractor,
dan dapat dikutip posisinya.

`read_pdf` **tidak menulis berkas apa pun** — hasilnya hidup selama percakapan saja.
`pdf_to_text` menulis berkas yang bertahan. Perbedaan itu yang menentukan kapan memakai
yang mana.

Bila `pdf_to_text` melaporkan teks sangat pendek (di bawah ~1.000 karakter), PDF-nya
kemungkinan hasil pindaian tanpa lapisan teks — perlu OCR atau versi lain dari artikel;
catat sebagai kendala akuisisi, jangan diamkan sebagai studi tanpa isi.

Bila unduhan gagal, jalankan `server_status` lebih dulu: sebagian kegagalan berasal dari
folder unduhan, bukan dari tautannya.

**Yang wajib dicatat ke `acquisition_log.md` per studi**: DOI, jalur yang berhasil (atau
seluruh jalur yang gagal), tanggal akses, dan status akhir. Angka *not retrieved* pada
diagram PRISMA diambil dari log ini — dan PRISMA 2020 memisahkannya sebagai kotak
tersendiri, bukan sebagai reason code eksklusi.

**Otomasi berhenti pada akuisisi.** Membaca teks boleh dibantu perkakas; keputusan
include/exclude dan isi sel ekstraksi ditetapkan screener yang bertanggung jawab atasnya.
Teks hasil `read_pdf` adalah bahan baca, bukan pengganti penilaian.

## Mengapa Crossref saja tidak cukup untuk bidang non-Indonesia

Ini perbedaan yang menentukan pilihan sumber, dan hasilnya berlawanan arah antar bidang.

Crossref memuat **metadata** DOI dari hampir semua penerbit, tetapi abstrak bersifat
**opsional** — penerbit besar tidak menyetorkannya, penerbit OJS umumnya menyetorkan.

**Diukur ulang 12 Agustus 2026** — 100 record terbaru per jurnal, terbit sejak 2023,
lewat `api.crossref.org/journals/{ISSN}/works?select=abstract`:

| Jurnal | Record ber-abstrak |
|---|---|
| Computers & Education (Elsevier) | **0 / 100** |
| Teaching and Teacher Education (Elsevier) | **0 / 100** |
| Learning and Instruction (Elsevier) | **0 / 100** |
| Jurnal Pendidikan IPA Indonesia | 95 / 100 |
| JPBI | 100 / 100 |
| Al-Jami'ah | 56 / 56 |
| Jurnal Iqra' | 70 / 76 |
| Ulumuna | 45 / 48 |

Nol persen versus **92–100%**. Perbedaannya bukan soal mutu jurnal melainkan **kebiasaan setoran
metadata penerbitnya**.

Angka ini bisa berubah — kebijakan setoran penerbit berubah dari waktu ke waktu. **Ukur ulang
untuk jurnal yang benar-benar ada di korpus Anda** dengan perintah yang sama sebelum memutuskan
jalur pencarian.

Konsekuensinya untuk screening title/abstract:

| Bidang | Crossref cukup? | Jalur yang dipakai |
|---|---|---|
| Kajian keislaman, hukum, pendidikan Indonesia | ya — abstrak tersedia | Crossref/OpenAlex + penelusuran manual Garuda/Moraref |
| Bidang internasional dengan penerbit komersial | **tidak** — abstrak kosong | Scopus/ScienceDirect, atau export manual scopus.com |

Jangan menyimpulkan sebuah artikel "tidak punya abstrak" dari kosongnya field Crossref;
yang kosong adalah setoran penerbit, bukan artikelnya.

## Hak akses kunci Elsevier — periksa per API, bukan sekadar terpasang

Satu kunci dapat berhak atas sebagian API dan ditolak pada sisanya. Yang paling menipu:
**Abstract Retrieval dapat membalas 200 dengan field abstrak kosong** — bukan galat,
sehingga mudah lolos tanpa disadari dan baru ketahuan saat screening tidak punya bahan.

Jalankan `elsevier_status` sebelum merancang query. Bacanya:

| Hasil | Arti | Tindakan |
|---|---|---|
| `scopus_search.ok: false` status 400/401 | Kunci tidak berhak atas Scopus Search | Pencarian lewat export manual scopus.com; kunci tetap berguna untuk abstrak dan teks lengkap |
| `abstract_retrieval.abstrak_terisi: false` | View META_ABS di luar hak akses (lazim di luar jaringan institusi) | Abstrak diambil otomatis lewat Article Retrieval untuk DOI Elsevier (`10.1016`) |
| `article_retrieval.fulltext_chars > 0` | Teks lengkap terjangkau, termasuk artikel berbayar | Jalur akuisisi Tahap 6 dan pengisian abstrak |
| status 429 | Kuota mingguan habis | Tunggu `resets_at`; rancang query sebelum mengeksekusi berulang |

`scopus_abstract` sudah menempuh dua jalur secara otomatis dan melaporkan jalur mana yang
berhasil pada field `abstract_via`. Bila keduanya gagal, field `catatan` menjelaskan sebab
dan jalan keluarnya — jangan diamkan record tanpa abstrak masuk ke Tahap 5.

## Cakupan — apa yang tidak terjangkau

Basis data nasional Indonesia (Garuda, SINTA, Moraref) **tidak punya API publik**;
penelusurannya manual lewat portal, dan hasilnya digabungkan sebagai basis data
tersendiri dengan jumlah hits dicatat terpisah.

Bagi topik yang literaturnya didominasi jurnal nasional — kajian keislaman, hukum
Indonesia, pendidikan lokal — Scopus dan WoS hanya menjangkau sebagian korpus. Jangan
menyimpulkan kelangkaan literatur dari sedikitnya hits Scopus; itu ciri cakupan indeks,
bukan ciri bidangnya. Nyatakan keterbatasan cakupan basis data di Limitations.

Sebaliknya, jurnal nasional yang **sudah terindeks Scopus umumnya juga ada di Crossref**
lengkap dengan abstrak, sehingga verifikasi referensi dan deteksi retraksi tetap bekerja
untuk korpus Indonesia meski pencariannya manual.

## Galat yang sering muncul

| Gejala | Sebab | Tindakan |
|---|---|---|
| 401 | Kunci ditolak | Periksa kunci; pastikan sudah diaktifkan untuk API yang dipanggil |
| 403 padahal kunci valid | Permintaan dari luar jaringan institusi | Jalankan dari jaringan kampus/VPN, atau minta insttoken ke admin lisensi |
| 429 | Kuota mingguan habis | Tunggu waktu reset yang dilaporkan; rancang query sebelum mengeksekusi berulang |
| Abstrak kosong pada hasil pencarian | Batas view STANDARD | `scopus_abstract` per DOI, atau export manual |
| Teks lengkap ScienceDirect ditolak | Artikel di luar langganan | Jalur akuisisi bertingkat Tahap 6 |

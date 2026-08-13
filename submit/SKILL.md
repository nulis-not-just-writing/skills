---
name: submit
description: Sapu naskah pra-submisi untuk risiko desk rejection — penolakan oleh editor sebelum naskah sampai ke reviewer. Gunakan saat user hendak submit artikel ke jurnal (Scopus/WoS), bertanya apakah naskahnya siap submit, bertanya kenapa naskahnya ditolak tanpa direview, memilih atau mengganti jurnal target, atau menyiapkan paket submisi (cover letter, highlights, pernyataan etik, anonimisasi double-blind). Berjalan sebagai gerbang bertahap - kecocokan scope, jenis artikel dan batas, pernyataan wajib, integritas (duplicate submission, salami slicing, preprint, disclosure AI), anonimitas, kesan sepuluh menit editor pada judul-abstrak-figur, konsistensi internal (sitasi versus daftar pustaka, angka abstrak versus hasil, sisa TODO dan tracked changes), kepatuhan author guidelines, dan kesehatan daftar pustaka - lalu berhenti di temuan fatal alih-alih melaporkan semuanya sekaligus. Untuk pemolesan prosa gunakan polish-manuscript; untuk struktur move per section gunakan nulis.
metadata:
  author: Mubaroq ADB | RPI
  version: 1.5.0
---

# submit — Gerbang Pra-Submisi

Desk rejection bukan penolakan peer review. Ia keputusan **editor**, diambil sebelum
naskah dikirim ke reviewer, dalam pembacaan sekitar sepuluh menit, dan mengenai 40–70%
naskah masuk di jurnal bereputasi. Sebagian besar kriterianya **tidak menyentuh mutu
ilmiah** — naskah bagus rutin dipulangkan karena scope-nya meleset atau pernyataan
etiknya kosong.

**Bahasa kerja mengikuti bahasa yang dipakai user** — balas dalam bahasa yang ia pakai bertanya; bila belum jelas, Indonesia. Ini soal bahasa percakapan saja: seluruh aturan, gerbang, dan ambang di skill ini berlaku sama untuk bahasa apa pun. **Bahasa naskah** mengikuti target jurnal, terlepas dari bahasa percakapannya.

## Ini gerbang, bukan sapuan mutu

Bedanya dengan `polish-manuscript` dan `nulis` bukan cuma daftar periksanya, tapi
bentuknya:

- Keduanya adalah **improvement pass** — berjalan linear, menyeluruh, menimbang semua
  dimensi setara, lalu melaporkan semuanya.
- Skill ini adalah **gerbang** — berurutan dari yang termurah dan paling mematikan.
  **Satu temuan fatal membuat sisanya tidak relevan: berhenti, laporkan, jangan
  lanjut menyisir.** Percuma memoles em-dash pada naskah yang scope-nya salah jurnal.

Pembacanya juga beda: keduanya menulis untuk reviewer, skill ini untuk editor.

## Langkah 0 — Input wajib

Tanyakan dengan daftar bernomor biasa (jangan AskUserQuestion). Empat hal:

1. **Naskah** — file `.docx` / `.tex` / `.md`.
2. **Jurnal target** — nama **dan** URL author guidelines-nya. Ini tidak bisa
   ditawar. Tanpa jurnal target, Gerbang G1–G2 dan T1 tak bisa dinilai, dan itu
   kira-kira separuh dari total risiko. Bila user belum punya target, jalankan Tahap 2–3
   saja lalu **katakan eksplisit** gerbang mana yang dilewati dan kenapa.
3. **Model review** — double-blind atau single-blind? Sudah pernah jadi preprint?
   Pernah disubmit ke jurnal lain?
4. **Nama & afiliasi semua penulis** — dipakai untuk mengukur rasio sitasi-diri dan
   mendeteksi kebocoran anonimitas.

Lalu **baca author guidelines-nya sungguhan** dengan WebFetch. Jangan menebak dari
kebiasaan penerbit — batas kata, gaya sitasi, dan pernyataan wajib berbeda antar jurnal
dalam satu penerbit yang sama.

## Sapuan mekanis lebih dulu

**Periksa prasyarat sebelum menjalankan apa pun:**

```bash
command -v python3 >/dev/null && python3 -V || echo "PYTHON TIDAK ADA"
command -v pandoc  >/dev/null && pandoc -v | head -1 || echo "PANDOC TIDAK ADA"
```

Semua skrip di skill ini **stdlib-only** — tidak ada `pip install`, tidak ada venv.
Satu pengecualian: `check_claim_fidelity.py` memerlukan `python-docx` **hanya** bila
naskahnya `.docx`; untuk `.tex`/`.md` tidak tersentuh.

- **Python tidak ada** → jangan jalankan apa pun dan jangan tampilkan traceback. Gerbang
  T0, T2, T2b, dan T2c tidak bisa dijalankan — **katakan itu eksplisit di laporan** (lihat
  aturan "sebutkan gerbang mana yang dilewati"). Sisanya (G1–G5, Tahap 2) tetap penuh
  karena berbasis pembacaan, bukan skrip. Cara memasang: macOS `xcode-select --install`,
  Windows `winget install Python.Python.3.12`.
- **Pandoc tidak ada** → hanya memengaruhi input `.docx`. Minta user mengekspor ke `.md`,
  atau pasang pandoc.

**Kegagalan lingkungan bukan temuan naskah.** Skrip yang tidak bisa jalan dilaporkan
sebagai gerbang yang dilewati, bukan sebagai naskah bermasalah. Keduanya jangan pernah
dicampur dalam satu tabel temuan.

Setelah prasyarat aman, hitung yang bisa dihitung sebelum menilai yang perlu penilaian:

```bash
python scripts/sweep.py NASKAH.docx --authors "Nama Penulis A;Nama Penulis B"
python scripts/sweep.py NASKAH.tex --authors "..." --bib refs.bib --json
```

Script melaporkan: jumlah kata (total & abstrak), keberadaan tujuh pernyataan wajib,
kesehatan daftar pustaka (jumlah, sebaran tahun, rasio sitasi-diri), silang sitasi
dengan daftar pustaka dua arah, kebocoran anonimitas, figur/tabel beserta rujukan
menggantung, angka abstrak yang tak muncul di badan naskah, serta sisa proses penulisan
(TODO/placeholder, tracked changes, komentar & metadata `.docx`). Ia **menghitung, tidak
memutuskan** — hasilnya bahan mentah untuk gerbang di bawah.

`sweep.py` memeriksa konsistensi **di dalam** naskah. Dua skrip di `scripts/hulu/`
memeriksa naskah **terhadap dunia luar** — jalankan keduanya sebelum T2:

```bash
python scripts/hulu/verify_refs.py refs.bib --project-root .
python scripts/hulu/check_claim_fidelity.py --manuscript NASKAH.md \
    --fulltext-dir path/ke/pdf-teks --bib refs.bib
```

- **`verify_refs.py`** meresolusi DOI/PMID ke CrossRef, OpenAlex, dan PubMed, lalu
  menulis `qc/reference_audit.json`. Statusnya membedakan tiga hal yang sering
  dicampur: `VERIFIED`, `MISMATCH` (DOI benar tapi daftar penulis/tahun meleset), dan
  `UNVERIFIED` (tidak ditemukan di indeks mana pun — tanda kuat sitasi karangan).
- **`check_claim_fidelity.py`** menjawab pertanyaan yang tidak bisa dijawab skrip mana
  pun di atas: **apakah sumbernya benar-benar mengatakan itu?** Butuh teks lengkap
  sumber (Markdown hasil konversi PDF) di satu direktori. Tiga probe: kutipan verbatim
  yang tidak ada di sumber (Mayor), atribusi konsep yang tak satu pun kata isinya muncul
  di sumber, dan klaim kardinal ("melaporkan tiga strategi") yang angkanya tak pernah
  disebut. Bila teks lengkapnya tidak ada, skrip diam — ia tidak pernah menebak.

**Catatan lingkungan (macOS).** Python dari python.org tidak membawa sertifikat CA. Bila
sertifikatnya belum dipasang, `verify_refs.py` melaporkan **semua** rujukan sebagai
`UNVERIFIED` dengan bukti "lookup failed" — termasuk yang benar-benar ada. Itu kegagalan
jaringan, **bukan temuan naskah**.

Di mesin ini sudah dipasang (12 Agustus 2026, `Install Certificates.command`), jadi
tidak perlu tindakan apa pun. Yang perlu diingat: **pemasangan Python versi baru
mengulang masalahnya** — tiap versi punya direktori sertifikat sendiri. Bila suatu saat
seluruh rujukan tiba-tiba `UNVERIFIED` serentak, curigai sertifikat lebih dulu sebelum
menuduh naskah:

```bash
python3 -c "import ssl,os; p=ssl.get_default_verify_paths().openssl_cafile; print(p, os.path.exists(p))"
"/Applications/Python 3.13/Install Certificates.command"   # sesuaikan nomor versinya
```

---

## Tahap 1 — Gerbang mematikan

Jalankan berurutan. Kena satu, **berhenti di situ**.

### G1 · Kecocokan scope
Pemicu desk reject nomor satu. Baca *aims & scope* jurnal, lalu tiga artikel terbaru
yang mereka terbitkan. Pertanyaan editor: "apakah pembaca jurnal saya mencari ini?"
Rinci di `references/kecocokan-jurnal.md`.

**Gagal → jangan perbaiki naskah, ganti jurnal.** Sarankan 3 alternatif beserta alasan.

### G2 · Jenis artikel & batas keras
Cocokkan naskah dengan *article type* yang jurnal buka (original research, review,
short communication, case study). Lalu batas keras: jumlah kata, jumlah figur/tabel,
jumlah referensi, panjang abstrak. Naskah 9.000 kata untuk batas 6.000 dipulangkan
otomatis, sering oleh sistem sebelum editor membacanya.

### G3 · Pernyataan wajib
Ethics/IRB approval (dengan nomor persetujuan), informed consent, Conflict of Interest,
Funding, Data Availability, Author Contributions, Acknowledgements. Yang mana yang wajib
ditentukan guidelines — tapi **Ethics dan COI hampir selalu wajib**, dan kosongnya
adalah desk reject tercepat yang ada.

Untuk riset yang melibatkan manusia/hewan tanpa nomor IRB: ini fatal dan tidak bisa
ditambal belakangan. Hentikan dan katakan terus terang.

### G4 · Integritas
Duplicate submission, salami slicing, kebijakan preprint jurnal, dan disclosure
penggunaan AI. Keempatnya bisa dinilai dari naskah dan dari jawaban user di Langkah 0.
Rinci di `references/integritas-dan-anonimitas.md`.

**Similarity index bukan gerbang di sini.** Tidak ada akses Turnitin/iThenticate, dan
gerbang yang hasilnya selalu "tidak bisa dinilai" cuma menambah bising. Ia dipindahkan
jadi butir tindakan pra-submisi di T5 — sesuatu yang user kerjakan sendiri, seperti
mengurus ORCID, bukan sesuatu yang skill ini putuskan.

### G5 · Anonimitas (hanya bila double-blind)
Nama penulis di badan naskah, "in our previous work [12]", afiliasi di caption figur,
acknowledgement yang membocorkan identitas, metadata file, dan URL repositori pribadi.
Script mendeteksi sebagian; sisanya perlu mata. Rinci di file yang sama dengan G4.

---

## Tahap 2 — Sepuluh menit editor

Editor membaca judul → abstrak → figur → paragraf terakhir Introduction, lalu memutuskan.
Nilai persis empat titik itu, dengan mata editor yang belum tahu apa-apa soal riset ini.

- **E1 · Judul** — apakah temuannya terbaca dari judul saja? Judul deskriptif
  ("Sebuah studi tentang X") lebih lemah daripada judul yang menyatakan hasil.
- **E2 · Abstrak** — harus memuat temuan **konkret dengan angka**. Abstrak tanpa hasil
  spesifik adalah cacat fatal. Tiga angka kalibrasi yang cukup untuk memutuskan di sini:
  Results nyaris universal pada abstrak terbit (493 dari 500 yang disurvei; Life Sciences
  100%), hanya 2,4% memakai lima move penuh sementara **tiga move paling lazim (41%)**, dan
  panjang lazimnya 150–250 kata. Jangan memaksakan template lima move bila jurnal target
  tidak memakainya — tiru pola 3–5 abstrak terbit terbaru di jurnal itu. *(Bila skill `nulis`
  terpasang, uraian penuhnya di `~/.claude/skills/nulis/sections/title-abstract.md`.)* Lalu lakukan
  yang editor lakukan setelah membaca abstrak: **lompat ke tabel/figur pertama dan
  cocokkan angkanya**. Script menandai angka abstrak yang tak punya pasangan di badan
  naskah (bagian 7 laporan); angka yang berbeda antara abstrak dan Results dibaca
  sebagian editor sebagai persoalan integritas data, bukan kecerobohan.
- **E3 · Novelty terbaca dalam 30 detik** — apakah ada kalimat eksplisit yang
  menyatakan apa yang belum pernah dikerjakan orang lain? Bila kontribusinya harus
  dicari-cari, editor tidak akan mencarinya.
- **E4 · Figur pertama** — bisa dipahami tanpa membaca teks? Ini sering satu-satunya
  figur yang editor lihat.
- **E5 · Cacat metodologis yang kasat mata** — n terlalu kecil untuk uji yang dipakai,
  tidak ada kelompok kontrol, klaim kausal dari desain korelasional, hasil yang tidak
  menjawab RQ. Bukan audit metodologi mendalam; cukup yang terlihat sekilas.

Bila naskah gagal di sini, masalahnya penyajian, bukan jurnalnya — **bisa diperbaiki**.
Serahkan ke `nulis` (struktur move) atau `polish-manuscript` (prosa).

---

## Tahap 3 — Gerbang teknis

Murah diperbaiki, tapi tetap mematikan karena menandakan penulis tidak membaca guidelines.

- **T0 · Konsistensi internal** — sitasi yang tidak nyambung ke daftar pustaka (dua arah:
  disitir tanpa entri, dan entri tak pernah disitir), nomor sitasi tidak urut, angka
  abstrak yang tak cocok dengan Results, pernyataan wajib yang isinya bertabrakan dengan
  Methods, sisa `TODO`/tracked changes/komentar, serta judul & daftar penulis yang berbeda
  antara naskah, cover letter, dan sistem submisi. Sebagian besar sudah dihitung
  `sweep.py` — tinggal dinilai. Rinci di `references/konsistensi.md`.

  Didahulukan atas T1 karena beda sinyalnya: gaya sitasi yang salah berarti penulis tidak
  membaca guidelines; sitasi yang tidak nyambung berarti penulis tidak membaca naskahnya
  sendiri. Yang kedua lebih mahal.

- **T1 · Kepatuhan author guidelines** — gaya sitasi, template, abstrak terstruktur
  vs. bebas, line numbering, penomoran halaman, urutan section, format file.
- **T2 · Kesehatan daftar pustaka** — rasio sitasi-diri (waspada >20%), umur referensi
  (jurnal Q1 umumnya menuntut mayoritas 5 tahun terakhir), referensi **retracted**, dan
  sumber non-terindeks/predatoris. Untuk memverifikasi, pakai tingkat tertinggi yang
  tersedia: `verify_refs.py` (deterministik, reproducible, menulis artefak audit), lalu
  MCP `scholar`/`zotero` bila terpasang — hanya MCP yang bisa mendeteksi **retraction**,
  yang tidak dilihat `verify_refs.py`. Kalau keduanya tak ada, `WebSearch`/`WebFetch`;
  kalau semua gagal, tandai "belum terverifikasi".

  **Tangga itu berlaku utuh tanpa skill lain**, dan aturan yang menopangnya satu kalimat:
  sitasi tidak pernah dianggap benar karena "terlihat masuk akal" — kombinasi
  penulis-tahun-jurnal yang tampak wajar justru pola khas sitasi karangan. DOI yang tidak
  resolve adalah tanda kuat. Laporkan status verifikasi apa adanya; sepuluh sitasi
  terverifikasi lebih baik daripada tiga puluh yang diasumsikan benar. *(Bila skill `nulis`
  terpasang, versi kanoniknya di `~/.claude/skills/nulis/ai-stylometry-flags.md` §5 —
  dipakai bersama oleh tiga skill, jadi itu yang menang bila berbeda.)*

  **`MISMATCH` bukan `UNVERIFIED`.** Yang pertama berarti karyanya nyata tapi entri
  bibliografinya salah — diperbaiki dengan menyalin metadata yang benar. Yang kedua
  berarti karyanya mungkin tidak pernah ada — itu persoalan integritas, bukan
  pengetikan, dan harus dikonfirmasi ke penulis sebelum apa pun disubmit.

- **T2b · Fidelitas klaim** — sitasi yang nyata pun bisa menempel pada kalimat yang tidak
  dikatakan sumbernya. DOI-nya resolve, penulisnya cocok, daftar pustakanya rapi, dan
  kalimatnya tetap salah. Inilah yang diperiksa `check_claim_fidelity.py`. Tanpa teks
  lengkap sumber, gerbang ini **tidak bisa dijalankan** — katakan begitu, jangan
  lewati diam-diam.

- **T2c · Kaskade PRISMA** (hanya untuk systematic review / scoping review) — aritmetika
  alur PRISMA adalah penjumlahan berantai, dan galat satu-angka di dalamnya sering
  ditemukan editor. Bila ada artefak penyaringan per ronde:

  ```bash
  python scripts/hulu/prisma_cascade_check.py --round1 round1.tsv --round2 round2.tsv \
      --round3 round3_adjudication.tsv --manuscript NASKAH.md --out qc/prisma.json
  ```

  Skrip menghitung kaskade kanonik dari keputusan mentah lalu membandingkannya dengan
  prosa naskah. **Batasnya nyata:** pembandingan prosa hanya mengenali beberapa frasa
  baku bahasa Inggris ("records were included after title and abstract", "retrieved for
  full-text", "included in the qualitative synthesis") dan **tidak** memeriksa angka
  "records identified". Bila naskah memakai frasa lain, skrip lolos tanpa memeriksa —
  cocokkan sisanya dengan mata.
- **T3 · Kualitas bahasa** — bukan soal sempurna, tapi apakah editor non-penutur asli
  bisa membacanya lancar. Bila tidak, sarankan language editing sebelum submit.
- **T4 · Figur teknis** — resolusi (umumnya ≥300 dpi raster, atau vektor), mode warna,
  format file, keterbacaan saat dicetak hitam-putih, ukuran font di dalam figur.
- **T5 · Paket submisi** — cover letter, highlights, graphical abstract, ORCID semua
  penulis, saran reviewer, corresponding author. Template di
  `references/paket-submisi.md`.

---

## Format keputusan

Akhiri dengan satu vonis, bukan daftar panjang:

| Vonis | Arti |
|---|---|
| **SIAP SUBMIT** | tidak ada temuan Tahap 1; Tahap 2–3 bersih atau tinggal kosmetik |
| **PERBAIKI DULU** | ada temuan, semuanya bisa diperbaiki tanpa ganti jurnal — daftarkan berurutan |
| **GANTI JURNAL** | G1 atau G2 gagal — naskahnya tidak salah, jurnalnya yang salah |
| **BERHENTI** | G3 (etik) atau G4 (integritas) gagal — tidak bisa ditambal, harus diselesaikan di luar naskah |

Untuk temuan, sajikan berperingkat dengan lokasi konkret:

| Prioritas | Gerbang | Temuan | Lokasi | Tindakan |
|---|---|---|---|---|

Sebutkan juga secara eksplisit **gerbang mana yang tidak bisa dijalankan** dan kenapa
(mis. jurnal target belum ditentukan, guidelines tidak bisa diakses). Jangan diam-diam
melewatinya — user akan mengira sudah diperiksa.

### Ambang butir kritis — kehadiran mengalahkan persentase

Godaan setelah menjalankan semua skrip adalah melaporkan skor: "naskah lolos 23 dari 26
pemeriksaan (88%)". **Jangan.** Persentase kepatuhan adalah ringkasan kasar — dua naskah
dengan angka sama bisa jauh berbeda kelayakannya, karena tidak semua butir berbobot sama.

Tiga aturan:

1. **Butir kritis bersifat lulus/gagal.** Sebagian kecil butir tidak bisa ditawar. Bila
   salah satunya hilang, angkat sebagai **temuan kritis di kepala laporan** berapa pun
   persentase keseluruhannya. Naskah yang 90% patuh tapi pernyataan etiknya kosong bukan
   "90% layak submit" — ia desk reject.
2. **Persentase itu sinyal sekunder**, berguna untuk membedakan "menyeluruh" dari
   "tipis". Ia **bukan** garis desk reject. Jangan pernah menyatakan ambang numerik yang
   tidak dipublikasikan jurnal — bila guidelines tidak menyebut angka, tidak ada angka.
3. **Ketentuan jurnal sendiri bersifat keras.** Panel wajib yang hilang, checklist yang
   salah untuk desain yang dipakai, format berkas yang tidak sesuai — verifikasi ke
   author guidelines, jangan pernah mengarangnya.

Butir yang diperlakukan kritis di skill ini:

| Gerbang | Butir kritis (hilang → temuan kritis) |
|---|---|
| G1/G2 | scope tidak cocok; jenis artikel tidak dibuka jurnal; melampaui batas keras |
| G3 | Ethics/IRB (untuk riset dengan subjek manusia/hewan); Conflict of Interest |
| G4 | duplicate submission; disclosure penggunaan AI bila jurnal mewajibkan |
| G5 | identitas penulis bocor di naskah double-blind |
| T0 | sitasi yang tidak nyambung ke daftar pustaka; angka abstrak ≠ angka Results |
| T2 | rujukan berstatus `UNVERIFIED`; rujukan **retracted** |
| T2b | `CITED_QUOTE_ABSENT` — kutipan yang tidak ada di sumbernya |

Sisanya dilaporkan sebagai temuan biasa, berperingkat, tanpa skor.

## Batas skill ini

- **Tidak menilai mutu ilmiah.** Itu pekerjaan peer review. Lolos gerbang ini berarti
  naskah sampai ke reviewer, bukan berarti akan diterima.
- **Tidak mengukur similarity index.** Bukan gerbang, bukan temuan — cuma satu butir
  tindakan di daftar periksa T5 yang user kerjakan sendiri. Jangan memberinya vonis dan
  jangan menyebutnya sebagai gerbang yang dilewati; ia memang bukan bagian dari gerbang.
- **Tidak menggantikan** `polish-manuscript` (prosa) atau `nulis` (struktur move).
  Panggil keduanya untuk temuan Tahap 2.
- **Berhenti di tombol submit.** Begitu keputusan editor turun — major revision, minor
  revision, atau reject and resubmit — pekerjaannya pindah ke `revisi`: membongkar
  komentar reviewer jadi butir, memutuskan mana yang ditolak, dan menulis surat
  tanggapan. Gerbang ini tidak menilai komentar reviewer.

---

## Berdiri sendiri atau berdampingan

Skill ini **berfungsi penuh sendirian**. Seluruh gerbangnya — scope, batas, pernyataan wajib,
integritas, anonimitas, kesan sepuluh menit, konsistensi internal, kesehatan daftar pustaka —
berjalan tanpa skill lain, dan `scripts/` seluruhnya milik sendiri.

| Bila terpasang | Yang bertambah | Tanpa itu |
|---|---|---|
| `nulis` | daftar kanonik penanda AI, kalibrasi abstrak yang lebih rinci, struktur move per section | angka kalibrasi inti dan tangga verifikasi sudah tertanam di SKILL.md ini |
| `polish-manuscript` | pemolesan prosa bila temuan menuntutnya | laporkan temuannya, serahkan perbaikan prosa ke user |
| `revisi` | penanganan setelah keputusan editor | di luar jangkauan skill ini |

**Aturan:** gerbang yang tidak bisa dijalankan **tidak dianggap lolos**. Bedakan "diperiksa dan
aman" dari "tidak diperiksa" secara eksplisit di laporan.

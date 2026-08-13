# Tanya jawab

## Apakah harus memasang kelimanya?

Tidak. **Tiap skill berfungsi penuh sendirian.** Pasang yang Anda perlukan. Bila tetangganya ada,
sebagian langkah jadi lebih dalam — tapi tidak ada yang macet karena skill lain tidak ada.

## Bagaimana cara memanggilnya?

Tidak perlu dipanggil. Skill aktif sendiri ketika Anda menyebut hal yang relevan — *"bantu saya
menulis introduction"*, *"naskah saya ditolak tanpa direview"*, *"saya mau bikin systematic
review"*.

## Harus pasang Python?

Tidak wajib. Tanpa Python, sebagian dimensi dikerjakan manual dan **skill diminta mengatakan
bahwa cakupannya berkurang** — bukan diam-diam melewatinya. Bila ada, tidak perlu `pip install`
apa pun: semua skrip stdlib-only.

## Semua rujukan saya tiba-tiba `UNVERIFIED`. Naskah saya bermasalah?

Hampir pasti **bukan**. Curigai sertifikat CA dulu — Python dari python.org di macOS tidak
membawanya, dan akibatnya semua lookup gagal serentak. Lihat [Prasyarat](Prasyarat.md).

Kegagalan jaringan **bukan temuan naskah**.

## Naskah saya bahasa Indonesia. Bisa?

Bisa. **Bahasa percakapan mengikuti bahasa Anda** — tanya Indonesia, dijawab Indonesia. Bahasa
naskahnya terpisah dan mengikuti jurnal target —
biasanya Inggris, dan ada pemeriksaan khusus untuk **kalke bahasa Indonesia** yang sering lolos:
*"It is known that…"*, *"It can be concluded…"*, `0,05` yang seharusnya `0.05`.

## Korpus saya jurnal nasional. Scopus hits-nya sedikit.

Itu **ciri cakupan indeks, bukan ciri bidangnya**. Pengukuran ulang 12 Agustus 2026 menemukan
jurnal Indonesia terindeks (OJS) menyetorkan abstrak ke Crossref pada 92–100% record, sementara
tiga jurnal pendidikan Elsevier menyetorkan **0%**.

`slr-cowork` menyertakan jalur Garuda, Moraref, SINTA, dan repositori PTKIN, serta aturan
menyatakan keterbatasan cakupan di Limitations.

## Saya bukan penutur bahasa Indonesia. Bisa dipakai?

Bisa, penuh. **Skill membalas dalam bahasa yang Anda pakai bertanya** — tulis dalam bahasa
Inggris, dijawab bahasa Inggris.

Isi berkas skill-nya memang berbahasa Indonesia, tetapi teks itu **instruksi untuk model**, bukan
untuk Anda; Claude membacanya dan menjawab dalam bahasa Anda. Anda tidak perlu membacanya sama
sekali.

Batas nyatanya: **dokumentasi di `docs/` ini berbahasa Indonesia.** Bila Anda ingin membaca
panduannya — bukan sekadar memakai skill-nya — Anda perlu terjemahan. Ringkasan berbahasa Inggris
ada di [`README.en.md`](https://github.com/nulis-not-just-writing/skills/blob/main/README.en.md).

## Boleh dipakai untuk pelatihan berbayar?

**Tidak, tanpa izin.** Lisensinya CC BY-NC 4.0 — non-komersial. Untuk riset dan pengajaran
(termasuk kelas reguler di kampus) tidak perlu izin apa pun; cukup cantumkan sumbernya. Lihat
[Lisensi](Lisensi.md).

## Boleh saya ubah dan sebarkan versi saya sendiri?

Boleh, untuk keperluan non-komersial, dengan atribusi. **`NOTICE.md` wajib ikut** — ada di akar dan
di dalam tiap skill, dan isinya berbeda-beda sesuai apa yang skill itu bawa.

## Bisa dipakai di ChatGPT / Gemini?

Berkasnya markdown biasa, jadi isinya bisa dibaca model mana pun. Tapi format Skill —
pemuatan otomatis, *progressive disclosure*, eksekusi skrip — spesifik Claude. Di tempat lain
Anda harus menempel isinya manual.

## Saya menemukan kekeliruan metodologis. Ke mana melapor?

Buka issue di [repo](https://github.com/nulis-not-just-writing/skills/issues). Sertakan skill,
berkas, dan sumber yang menurut Anda benar — kalau ada DOI-nya, jauh lebih cepat diverifikasi.

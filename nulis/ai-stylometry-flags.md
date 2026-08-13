# Flag AI Generative Stylometry

Tujuan: menghilangkan penanda gaya tulisan AI generatif dari naskah — bukan untuk mengelabui detektor secara curang, tapi karena penanda ini membuat prosa terbaca generik, hampa, dan **menurunkan kredibilitas di mata reviewer** jurnal Q1. Editor makin terlatih mengenalinya; naskah yang "berbau AI" sering di-desk-reject atau dicurigai integritasnya. Suara ilmiah yang autentik = kalibrasi klaim + kepadatan substansi, dua hal yang justru dinilai tinggi.

**Berkas ini adalah daftar kanonik penanda AI untuk ketiga skill menulis.** `polish-manuscript` (dimensi 6) merujuk ke sini alih-alih menyimpan daftarnya sendiri; `submit` memakainya lewat rujukan yang sama. Bila menambah penanda baru, tambahkan di sini — jangan di tempat lain.

Jalankan audit ini sebagai bagian dari mode audit dan sebelum submit (gerbang pra-submisi ada di skill `submit`).

## 1. Bagaimana stylometry/detektor menandai teks
Dua sinyal utama yang dipakai model deteksi (mis. berbasis perplexity–burstiness):
- **Perplexity rendah** — pilihan kata terlalu dapat diprediksi, klise, "aman".
- **Burstiness rendah** — panjang & ritme kalimat terlalu seragam; manusia bervariasi (kalimat pendek tajam diselingi kalimat panjang kompleks).

Implikasi menulis: **variasikan panjang & struktur kalimat**, pakai istilah teknis presisi khas bidang (bukan kata umum megah), dan biarkan ritme naik-turun. (Ingat temuan empiris: abstrak paper highly-cited justru lebih kompleks & bervariasi secara sintaksis — lihat `sections/title-abstract.md`.)

## 2. Kosakata penanda (lexical tells) — ganti dengan istilah bidang
Kata/frasa yang overrepresented di teks LLM dan jarang di prosa ilmiah asli:
- Verba tren: *delve into, underscore, showcase, leverage, navigate, foster, unlock, harness, illuminate, spotlight*
- Adjektiva kosong-megah: *pivotal, crucial, vital, robust, comprehensive, nuanced, multifaceted, intricate, seamless, meaningful, significant* (bila non-statistik), *rich, holistic, transformative*
- Metafora klise: *tapestry, landscape, realm, arena, at the forefront, in the ever-evolving world of, a testament to*
- Nomina hampa: *insights, dynamics, complexities, interplay, synergy, framework* (bila tak dirujuk konkret)

Aturan: bila kata bisa dipakai di paper bidang apa pun tanpa berubah makna, kemungkinan itu penanda — ganti dengan istilah yang hanya bermakna di bidang Anda.

## 3. Frasa boilerplate & meta-komentar — hapus
- "It is important to note that...", "It is worth mentioning that...", "It should be emphasized that..." → langsung nyatakan isinya.
- "In today's world / In the modern era / In recent years" sebagai pembuka basa-basi.
- "This section will discuss...", "As mentioned earlier..." berlebihan (over-signposting) — signposting secukupnya, lihat `coherence.md`.
- Kalimat ringkasan hampa: "In conclusion, this study has shown the importance of...", "Overall, these findings highlight..." tanpa isi baru.
- "plays a crucial role in", "sheds light on", "paves the way for".

## 4. Pola struktural yang menciri
- **Keseragaman ritme** — banyak kalimat 20–25 kata beruntun. Pecah; selingi kalimat pendek.
- **Triadic overload** — obsesi daftar tiga item ("X, Y, and Z") berulang di banyak kalimat.
- **"Not only... but also"** dan **"From X to Y"** yang berulang.
- **Paragraf simetris** — semua paragraf ~4 kalimat dengan pola topik→elaborasi→contoh→transisi identik.
- **"This" menggantung** — "This shows...", "This suggests..." tanpa nomina ("This *finding* suggests..."). Selalu beri nomina ringkasan.
- **Over-hedging seragam** — bukan kalibrasi cermat, tapi mengaburkan segala klaim; hedge harus proporsional dengan bukti (lihat kalibrasi per bidang di `sections/discussion.md`).
- **Parallelism berlebih** — setiap kalimat berstruktur cermin, terasa mekanis.
- **Enumerasi kaku** — "First,/Firstly, … Second,/Secondly, … Third," di awal kalimat berurutan. Ganti dengan transisi yang mengalir atau integrasikan penomorannya ke dalam argumen.
- **Antitesis berpola** — "It's not just X, it's Y", "This isn't merely … it's …", "From X to Y". Sekali mungkin efektif; berulang jadi tanda tangan mesin.

## 4a. Tanda baca penciri (punctuation tells) — paling sering ditandai reviewer
- **Em-dash (—) berlebihan.** LLM gemar menyisipkan em-dash untuk aposisi/penekanan ("the method — which we developed — shows..."). Di prosa ilmiah asli em-dash jarang; ganti dengan koma, tanda kurung, atau pecah jadi dua kalimat. Batas aman: nyaris nol per paragraf; bila terasa "berirama em-dash", itu penanda.
- **Titik dua (:) berlebihan.** Pola khas AI: kalimat pengantar diikuti ":" lalu daftar/penjelasan, berulang-ulang ("The results reveal three insights:", "This raises a question:"). Pakai titik dua hanya bila benar-benar memperkenalkan daftar/kutipan formal; selebihnya tulis sebagai kalimat utuh.
- **En-dash & bullet** di tempat yang seharusnya prosa mengalir; hindari mengubah paragraf argumen jadi daftar berpoin.
- **Semicolon (;) bertebaran** sebagai perekat serba-guna — pakai hemat dan hanya untuk memisah klausa independen terkait.
- Aturan praktis: baca satu halaman, hitung em-dash dan titik dua. Bila lebih dari satu-dua per halaman tanpa alasan kuat (daftar/kutipan sejati), pangkas.

## 4b. Tipografi — jejak tempel dari editor AI
Penanda yang tertinggal bukan pada kata, melainkan pada karakternya. Paling sering muncul pada naskah yang disalin-tempel dari jendela chat.
- **Unicode "cerdas"** — curly quotes (" " ' '), karakter elipsis tunggal (…) alih-alih tiga titik, en-dash di tempat hyphen, dan non-breaking space yang tak disengaja. Normalkan sesuai gaya jurnal/kelas dokumen; di LaTeX ini juga sumber galat kompilasi.
- **Penekanan berlebihan** — **bold** pada kata kunci di tengah kalimat, dan paragraf argumen yang dipecah jadi bullet/numbered list. Naskah jurnal menuntut prosa mengalir; daftar berpoin dipakai hemat dan hanya bila isinya memang enumeratif.
- **Emoji & simbol dekoratif** — nol toleransi di naskah ilmiah.
- **Heading bertingkat berlebihan** — pembagian sub-sub-section setiap dua paragraf, khas keluaran AI yang menstrukturkan segalanya.

## 5. Risiko integritas khas akademik (paling berbahaya)
- **Sitasi halusinasi** — LLM mengarang referensi yang tampak nyata (nama, tahun, jurnal, bahkan DOI palsu). **WAJIB verifikasi setiap sitasi** sebelum masuk naskah, dengan cara apa pun yang tersedia (tangga di bawah). Ini penyebab retraction & tuduhan misconduct.
- **Klaim tanpa sumber** yang disajikan seolah fakta mapan ("Studies have shown that..." tanpa studi nyata).
- **Angka/statistik yang tidak berasal dari data Anda** — cek silang setiap angka dengan Results.
- **Parafrase generik literatur** yang tak mencerminkan isi sebenarnya paper yang disitir.
- **Konten metodologis samar** yang tidak sesuai apa yang benar-benar dilakukan — bahaya khusus di Methods.

### Tangga verifikasi sitasi (kanonik untuk nulis, polish-manuscript, submit)
Pakai tingkat tertinggi yang tersedia di lingkungan user — jangan berasumsi MCP terpasang:

1. **MCP `scholar` / `zotero`** bila ada. Paling akurat: metadata penuh, bisa membaca isi paper, dan mendeteksi retraction.
2. **`WebSearch` + `WebFetch`** bila MCP tak ada. Resolusikan DOI lewat `doi.org`, lalu cocokkan **judul, penulis pertama, tahun, dan nama jurnal** di halaman penerbit atau Crossref. DOI yang tidak resolve adalah tanda kuat sitasi karangan.
3. **Keduanya tak tersedia** → tandai eksplisit **"BELUM TERVERIFIKASI"** dan minta user memeriksa sendiri. 

Aturan yang tidak boleh dilanggar di ketiga tingkat: **sitasi tidak pernah dianggap benar karena "terlihat masuk akal"**. Kombinasi penulis-tahun-jurnal yang tampak wajar justru pola khas sitasi halusinasi. Laporkan status verifikasi apa adanya; naskah dengan sepuluh sitasi terverifikasi lebih baik daripada tiga puluh yang diasumsikan benar.

## 6. Checklist audit (jalankan sebelum submit)
- [ ] Tidak ada verba/adjektiva tren dari daftar §2 yang tak berfungsi
- [ ] Tidak ada frasa boilerplate/meta-komentar hampa (§3)
- [ ] Panjang & struktur kalimat bervariasi (burstiness) — baca keras, dengarkan ritmenya
- [ ] Em-dash (—) dan titik dua (:) hemat: maksimal satu-dua per halaman, hanya untuk daftar/kutipan sejati
- [ ] Tiap "This/These" punya nomina ringkasan
- [ ] Hedging proporsional dengan bukti, bukan kabut seragam
- [ ] **Setiap sitasi terverifikasi nyata** (judul, penulis, tahun, DOI) — nol toleransi
- [ ] Setiap angka cocok dengan data/Results
- [ ] Istilah teknis presisi bidang menggantikan kata umum megah
- [ ] Prosa terdengar seperti penulis manusia yang menguasai bidangnya, bukan ringkasan ensiklopedia

## Catatan sikap
Menghapus penanda ini **bukan** soal lolos detektor, melainkan menulis dengan suara ilmiah sendiri: spesifik, terkalibrasi, padat substansi, jujur pada sumber. Bila naskah memang ditulis/dibantu AI, tetap patuhi kebijakan disclosure jurnal target — banyak jurnal Q1 mewajibkan pernyataan penggunaan AI di Methods/Acknowledgements.

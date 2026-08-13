# Matematika & Ilmu Formal

Struktur **BUKAN** IMRaD dan **bukan** urutan logis ketat ala Bourbaki/Hilbert. Acuan: Halmos "How to Write Mathematics" (1970), Knuth dkk. "Mathematical Writing" (1987), Krantz "A Primer of Mathematical Writing".

## Struktur paper (Krantz)
1. **Introduction**: 1–2 paragraf ringkasan hasil utama dalam **bahasa non-teknis** → sejarah masalah & hasil terdahulu → persis apa kemajuan paper ini → outline organisasi. (Padanan CARS: territory = sejarah/konteks; niche = masalah terbuka; occupying = teorema utama.)
2. **Materi eksplanatori di depan, teknis di belakang**. Bagian bukti utama berisi "big steps": rumuskan lema-lema teknis + jelaskan bagaimana mereka dirangkai jadi teorema. **Dorong detail bukti lema yang berat ke akhir paper**.
3. **Spiral plan** (Halmos) untuk paper ekspositori/panjang: tiap section = satu konsep dengan pola *motivate → define → examples → counterexamples*; section baru mereview section sebelumnya dari sudut pandang konsep baru.

## Menyatakan teorema (aturan konkret)
- Teorema dinyatakan **duluan**, sebelum buktinya — jangan "hanging theorem" yang muncul setelah pengembaraan.
- Panjang statement ≤10 baris, idealnya ≤5, sebisanya 1 kalimat. Capai dengan **mendefinisikan istilah pengikat** ("regular", "amenable", "admissible") sebelum teorema sehingga banyak hipotesis mengerut. Tidak pernah perlu menyatakan teorema dengan 25 hipotesis bernomor.
- Statement **self-contained**: tidak bergantung asumsi di teks sebelumnya.
- Bebas chit-chat ("Without loss of generality we may assume...").

## Signposting bukti (Krantz)
- **"Claim" device**: "We claim that the following is true... Assuming this claim for the moment, we complete the proof; the claim is proved in Section X."
- **"Proof deferred to Section 8"** untuk detail berat.
- Pembaca harus **selalu tahu status setiap pernyataan**: proved / unproved / to-be-proved / will-not-be-proved.

## Gaya kalimat (Knuth)
- Simbol dari dua formula berbeda dipisahkan kata: ~~"Consider Sq, q < p"~~ → "Consider Sq, where q < p".
- Jangan awali kalimat dengan simbol: ~~"xⁿ − a has..."~~ → "The polynomial xⁿ − a has...".
- Kalimat tepat sebelum teorema/algoritma = kalimat lengkap atau diakhiri titik dua.
- **Blah test**: kalimat harus tetap mengalir bila semua formula (kecuali paling sederhana) diganti "blah". Jangan gaya PR — jangan sekadar mendaftar formula; ikat dengan *running commentary*.
- "we" = penulis+pembaca bersama (dialog), bukan pengganti formal "I"; "I" dihindari kecuali persona penulis relevan.
- **Rendah hati**: tanpa superlatif pujian untuk karya sendiri, eksplisit maupun implisit.
- "The best notation is no notation" — minimalkan notasi; utamakan prosa.
- Organisasikan di sekitar **contoh & counterexample konkret**, bukan generalitas maksimal ("big general theories are afterthoughts of small profound insights").

## Abstract
≤10 baris, self-contained, **tanpa referensi bibliografi**, notasi & jargon minimum.

## Checklist audit
- [ ] Introduction membuka dengan ringkasan non-teknis hasil utama
- [ ] Teorema dinyatakan sebelum bukti, ≤10 baris, self-contained
- [ ] Detail teknis berat didorong ke belakang; big steps di depan
- [ ] Status tiap pernyataan selalu jelas (signposting)
- [ ] Lolos blah test; tidak ada kalimat diawali simbol
- [ ] Tanpa superlatif untuk karya sendiri

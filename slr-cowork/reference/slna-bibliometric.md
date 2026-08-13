# Jalur Opsional: Bibliometric Analysis / SLNA (VOSviewer)

Dipakai **hanya** bila review diperluas menjadi Systematic Literature Network Analysis —
kombinasi SLR dan analisis bibliometrik. Untuk SLR biasa, lewati seluruh jalur ini.

Rujukan metodologis: Aria & Cuccurullo (2017) bibliometrix; Donthu et al. (2021)
panduan bibliometric review.

## Posisi dalam alur

Berjalan paralel dengan Tahap 8, memakai **export Scopus mentah dari Tahap 4** —
bukan korpus final pasca-screening, karena analisis jaringan memerlukan cakupan luas
untuk memetakan struktur intelektual bidang.

## Struktur artefak

```
exports/thesaurus_keywords.txt, thesaurus_authors.txt
outputs/bibliometric_log.md
outputs/vosviewer_parameters.md
outputs/cluster_interpretation.md
outputs/slna_integration.md
outputs/figures/fig_network_*.svg + .png
vosviewer/            file proyek + export network
modul_bibliometric_summary.md
```

## Langkah

**1. Persiapan data + thesaurus.** Bersihkan export Scopus mentah. Bangun file thesaurus
untuk menyatukan varian: bentuk jamak/tunggal, ejaan Inggris-Amerika/Britania, akronim
versus bentuk panjang, nama penulis yang tidak konsisten. Thesaurus yang buruk
menghasilkan cluster yang terpecah palsu.

**2. Analisis VOSviewer + justifikasi parameter.** Eksekusi VOSviewer dijalankan user
secara manual — Anda menyiapkan input, menjustifikasi parameter, dan menafsirkan output.
Setiap parameter berikut wajib dijustifikasi eksplisit di `vosviewer_parameters.md`,
karena reviewer akan menanyakan mengapa cluster berbentuk seperti itu:

- Tipe analisis (co-occurrence, co-authorship, co-citation, bibliographic coupling)
- Unit analisis (all keywords / author keywords / index keywords)
- Metode counting (full atau fractional)
- Ambang minimum kemunculan
- Jumlah item yang ditampilkan
- Metode normalisasi (association strength / fractionalization / LinLog)
- Resolusi clustering
- Ukuran cluster minimum
- Parameter layout (attraction/repulsion)

**3. Interpretasi cluster.** Setiap cluster diberi label berdasarkan kriteria kuantitatif
bertingkat — bukan kesan visual: kekuatan total link, jumlah kemunculan, kepadatan
internal, dan posisi temporal. Beri nama tematik pada tiap cluster, lengkapi dengan
istilah paling representatif dan interpretasi substantifnya.

**4. Integrasi SLNA.** Ini bagian yang membuat SLNA bernilai lebih daripada dua analisis
yang berdiri sendiri: pertemukan struktur jaringan dengan temuan sintesis sistematis.
Tunjukkan di mana keduanya **selaras** (cluster yang ramai bersesuaian dengan tema temuan
yang kuat), di mana **berbeda** (cluster ramai tetapi bukti primernya lemah, atau tema
kuat yang jaringannya tipis), dan apa makna perbedaan itu bagi agenda riset lanjutan.

Overlay temporal berguna untuk memperlihatkan tema yang sedang menguat versus yang
memudar — ini bahan langsung untuk section Future Research.

## Pelaporan di manuskrip

Jelaskan metode bibliometrik di Methods sebagai komponen terpisah dari sintesis
sistematis, dengan korpus dan tujuannya sendiri yang dinyatakan jelas. Jangan
menampilkan cluster bibliometrik seolah-olah temuan sintesis bukti — keduanya menjawab
pertanyaan berbeda: yang satu memetakan struktur perhatian bidang, yang lain menilai
kekuatan bukti.

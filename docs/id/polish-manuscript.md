# polish-manuscript — prosa & mekanik

*[Read this in English](../polish-manuscript.md)*

**v1.4.0** · [unduh zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/polish-manuscript-1.4.0.zip)

Audit sepuluh dimensi atas draf yang strukturnya sudah benar. Bertindak sebagai Asisten Peneliti
Senior, Pakar Metodologi, Pakar Logika Akademik, dan Editor Jurnal Internasional sekaligus.

## Untuk apa sebenarnya skill ini

### 1. Draf sudah benar strukturnya, tapi kalimatnya berat

> *"Naskah ini sudah lengkap tapi terasa kaku dan bertele-tele. Poles."*

Sepuluh dimensi disapu berurutan, dari kejelasan kalimat sampai kalibrasi klaim. Yang bisa
dihitung dihitung skrip; yang butuh penilaian dinilai model. Suara Anda dipertahankan — tujuannya
memperjelas, **bukan** menyeragamkan sampai semua naskah terdengar sama.

### 2. Anda khawatir naskahnya "berbau AI"

Kekhawatiran yang wajar, dan biasanya orang mengeceknya dengan membaca keras lalu menebak.

`cek-variasi-kalimat.py` menggantikan tebakan itu dengan angka: ia mengukur **burstiness** —
sebaran panjang kalimat. Prosa manusia naik-turun; prosa generatif cenderung rata. Angka itu
menunjukkan **di paragraf mana** ritmenya datar, bukan sekadar memberi vonis untuk seluruh naskah.

### 3. Angka dan istilah tidak konsisten antar-section

Abstrak menulis 340 responden, Methods menulis 342. Akronim didefinisikan dua kali. `0,05` yang
seharusnya `0.05` — galat khas penulis Indonesia yang menulis dalam bahasa Inggris, dan sengaja
diperiksa terpisah.

`lint-mekanis.py` menyapu semua itu secara deterministik. Jalankan ulang kapan pun, hasilnya sama.

### Gerbang yang paling menentukan

Penyuntingan prosa punya satu risiko yang jarang disadari: **kalimat yang dirapikan bisa
menghilangkan angka atau sitasi**. Itu bukan pemolesan lagi, itu kehilangan bukti.

Karena itu ada `cek-fidelitas-suntingan.py`. Salin naskah **sebelum** menyunting, lalu bandingkan
setelahnya. `ANGKA_BERGESER` dan `SITASI_HILANG` berstatus Mayor — bagian itu **dikembalikan ke
bentuk semula dan dilaporkan**, bukan diperbaiki diam-diam.

Ini langkah yang paling sering tidak ada di alat sejenis, dan yang paling mahal bila hilang.

## Kapan dipakai

- Draf sudah jadi tapi terasa kaku atau bertele-tele
- Khawatir naskahnya "berbau AI"
- Angka dan akronim tidak konsisten antar-section
- Klaimnya terasa terlalu berani atau terlalu malu-malu

## Sepuluh dimensi

1. Kejelasan, koherensi, gaya
2. Konstruksi argumen
3. Konsistensi antar-section
4. Struktur IMRaD/CARS
5. Istilah kanonik
6. **Eliminasi penanda generatif AI**
7. **Konvensi mekanis** — tense, akronim, satuan SI
8. Pelaporan statistik & validasi angka
9. Figur/tabel & section wajib
10. Kalibrasi klaim

## Tiga skrip

Semua **stdlib-only**, tanpa `pip install`.

| Skrip | Mengerjakan |
|---|---|
| `lint-mekanis.py` | dimensi 7 hampir seluruhnya — akronim, ejaan US/UK, nilai p, satuan, **desimal koma** |
| `cek-variasi-kalimat.py` | mengukur *burstiness* untuk dimensi 6 — mengganti "baca keras, dengarkan ritmenya" dengan angka |
| `cek-fidelitas-suntingan.py` | **gerbang**: tiap angka dan sitasi yang ada sebelum penyuntingan wajib masih ada sesudahnya |

Cek desimal koma sengaja ditambahkan: itu galat khas penulis Indonesia yang menulis naskah
berbahasa Inggris — `0,05` yang seharusnya `0.05`.

## Gerbang fidelitas

Ini yang paling penting dan paling sering tidak ada di alat sejenis. Salin naskah sebelum
menyunting, lalu setelah selesai:

```bash
python ~/.claude/skills/polish-manuscript/scripts/cek-fidelitas-suntingan.py \
    --sebelum /tmp/naskah-sebelum.tex --sesudah NASKAH.tex --strict
```

`ANGKA_BERGESER` dan `SITASI_HILANG` berstatus **Mayor**. Bila menyala, bagian itu dikembalikan ke
bentuk semula dan dilaporkan ke penulis — bukan diperbaiki sendiri.

## Aturan yang tidak ditawar

**Kegagalan lingkungan bukan temuan naskah.** Skrip yang tidak bisa jalan dilaporkan sebagai
langkah yang dilewati, bukan sebagai "naskah bermasalah".

**Suara penulis dipertahankan.** Tujuannya memperjelas, bukan menyeragamkan sampai terdengar
seperti AI.

# Review Sistematis, Scoping Review, dan Bibliometrik

Figur di jenis naskah ini punya beban khusus: ia bukan hanya menyajikan hasil,
tapi juga **membuktikan bahwa prosesnya dapat direproduksi**. Diagram alir dan
peta bukti adalah bagian dari metode, bukan ilustrasi.

## Bentuk kanonik

| Yang ingin ditunjukkan | Bentuk | Catatan |
|---|---|---|
| Seleksi studi | Diagram alir PRISMA 2020 | Wajib; angka setiap kotak harus berjumlah konsisten |
| Cakupan bukti (scoping) | Peta bukti gelembung (populasi × intervensi) | Ukuran = jumlah studi, warna = kualitas |
| Sebaran karakteristik studi | Panel ringkas: tahun, negara, desain, n | Bukan tabel karakteristik panjang |
| Risiko bias per studi | Traffic-light plot (RoB 2 / ROBINS-I) | Plus bar ringkasan per domain |
| Efek gabungan | Forest plot (lihat `klinis-epidemiologi.md`) | — |
| Bias publikasi | Funnel plot + uji Egger | Hanya bila k ≥ 10 |
| Ketahanan hasil | Leave-one-out / analisis sensitivitas | Menjawab kekhawatiran reviewer |
| Perkembangan bidang per tahun | Deret publikasi + penanda peristiwa | Tandai tahun potong pencarian |
| Struktur kolaborasi/topik | Peta ko-kata / ko-sitasi berklaster | Klaster dinamai manual, bukan angka |
| Perkembangan topik | Peta tematik / plot overlay temporal | Warna = tahun rata-rata |
| Kesenjangan bukti | Matriks intervensi × luaran, sel kosong ditandai | Sel kosong **adalah** temuannya |

## Aturan wajib domain ini

**Diagram alir PRISMA harus berjumlah benar.** Identifikasi − duplikat −
disaring − dikecualikan = disertakan. Reviewer menjumlahkannya. Cantumkan alasan
eksklusi teks lengkap beserta jumlahnya, bukan hanya total.

**Cantumkan tanggal potong pencarian dan basis data** di figur atau caption.
Tanpa itu, review tidak dapat diperbarui oleh orang lain.

**Peta bukti: sel kosong ditandai eksplisit.** Justru kekosongan itulah
kontribusi scoping review — beri arsir atau simbol "belum ada studi", jangan
biarkan kosong tanpa keterangan sehingga terbaca sebagai "tidak diperiksa".

**Funnel plot hanya bila k ≥ 10.** Di bawah itu, uji asimetri tidak berdaya dan
figurnya menyesatkan. Katakan bila dilewati dan mengapa.

**Klaster bibliometrik diberi nama substantif.** "Klaster 1 (merah)" tidak
menyampaikan apa pun. Baca istilah dominan tiap klaster dan beri nama tematik;
sebutkan algoritma klasterisasi, resolusi, dan ambang minimum kemunculan.

**Jangan mengklaim tren dari tahun berjalan.** Tahun pencarian dilakukan selalu
tampak menurun karena indeksasi belum lengkap. Potong atau tandai tahun terakhir
sebagai parsial.

**Risiko bias digambar per studi, bukan hanya diringkas.** Bar ringkasan
menyembunyikan studi mana yang bermasalah; traffic-light memungkinkan pembaca
menilai sendiri.

## Jebakan yang sering lolos

- Diagram alir PRISMA versi 2009 pada naskah yang mengklaim mengikuti PRISMA
  2020 (jumlah kotak dan istilahnya berbeda).
- Peta jaringan VOSviewer diekspor sebagai tangkapan layar beresolusi rendah
  dengan label yang tidak terbaca setelah diperkecil ke lebar kolom. Ekspor
  vektor, atau gambar ulang dengan hanya simpul yang dibahas.
- Word cloud kata kunci — sama dilarangnya seperti di riset kualitatif.
- Bar jumlah publikasi per negara berdasarkan afiliasi penulis pertama saja,
  tanpa disebut aturan penghitungannya (full counting vs fractional).
- Peta bukti yang ukuran gelembungnya sebanding jumlah studi tapi legendanya
  tidak memberi acuan ukuran.

## Resep

Peta bukti (bubble matrix) dengan sel kosong yang ditandai:

```python
from vizkit import apply_style, new_figure, save_figure
import numpy as np

apply_style()
fig, ax = new_figure(width="double", height_ratio=0.55)

for i, luaran in enumerate(luaran_list):
    for j, interv in enumerate(intervensi_list):
        k = jumlah[i, j]
        if k == 0:
            ax.scatter(j, i, s=70, facecolor="none", edgecolor="0.75",
                       lw=0.6, hatch="///", zorder=2)
        else:
            ax.scatter(j, i, s=40 + 28 * k, c=warna_kualitas[i, j],
                       edgecolor="white", lw=0.5, zorder=3)
            ax.text(j, i, str(k), ha="center", va="center", fontsize=5.5, c="white")
ax.set_xticks(range(len(intervensi_list))); ax.set_xticklabels(intervensi_list, rotation=30, ha="right")
ax.set_yticks(range(len(luaran_list))); ax.set_yticklabels(luaran_list)
ax.invert_yaxis()
ax.set_title("Luaran retensi jangka panjang belum diteliti untuk tiga dari lima intervensi")
ax.text(1.0, -0.28, "Lingkaran arsir kosong = belum ada studi · angka = jumlah studi · pencarian s.d. 31 Mei 2026",
        transform=ax.transAxes, ha="right", fontsize=5.5, color="0.35")
save_figure(fig, "fig2_peta_bukti")
```

Diagram alir PRISMA: gunakan kotak `FancyBboxPatch` + `annotate` berpanah, atau
paket `PRISMA2020` (R). Angka diambil dari satu berkas hitungan yang sama dengan
yang dikutip di teks.

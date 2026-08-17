# Sosial, Survei, Psikometri, Ekonometrika

Dua kebiasaan merusak di bidang ini: **merata-ratakan skala Likert** seolah
interval, dan **menyajikan model regresi sebagai tabel** padahal koefisien
adalah estimasi dengan ketidakpastian yang lebih baik dilihat daripada dibaca.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Respons item ordinal | Diverging stacked bar | Netral dibelah di titik nol |
| Banyak item satu konstruk | Diverging bar terurut + % setuju | Terurut menurut besar, bukan nomor item |
| Koefisien model | Dot-whisker plot | Terstandardisasi bila skala berbeda |
| Perbandingan beberapa spesifikasi model | Specification curve | Menjawab tuduhan p-hacking |
| Model persamaan struktural | Diagram jalur berlabel β dan p | Bukan tabel matriks |
| Struktur faktor | Heatmap loading + cut-off | Loading rendah disembunyikan, ambang disebut |
| Unit lintas waktu (panel) | Spaghetti + rerata kelompok | Bukan bar rerata per gelombang |
| Efek moderasi | Plot marginal effect / johnson-neyman | Bukan sekadar p interaksi |
| Distribusi pendapatan/ketimpangan | Kurva Lorenz, kepadatan | Bukan bar rerata |
| Sebaran demografi sampel | Piramida penduduk / dot | Untuk menilai keterwakilan |
| Kesenjangan antar kelompok | Slope/dumbbell plot | Menampilkan dua titik dan jaraknya |
| Bobot survei dan desain | Estimasi tertimbang + CI desain | CI naif menyesatkan |

## Aturan wajib domain ini

**Likert digambar sebagai proporsi, bukan rerata.** "Rerata 3,4 dari 5"
menyembunyikan apakah distribusinya menumpuk di tengah atau terbelah di dua
kutub — dan dua pola itu punya arti substantif yang berlawanan. Gunakan
`likert_diverging`: setuju ke kanan, tidak setuju ke kiri, netral dibelah atau
disisihkan sebagai kolom terpisah (katakan yang mana).

**Koefisien terstandardisasi bila prediktor berbeda satuan.** Membandingkan
panjang whisker koefisien "usia (tahun)" dan "pendapatan (juta rupiah)" tanpa
standardisasi tidak bermakna. Nyatakan bila terstandardisasi.

**Gambar CI, bukan bintang.** Bintang signifikansi menyembunyikan presisi.
Nyatakan tingkat CI, dan untuk data survei kompleks gunakan galat baku yang
memperhitungkan desain (strata, klaster, bobot).

**Kategori referensi dinyatakan** pada setiap prediktor kategorikal —
koefisien tanpa kategori acuan tidak dapat dibaca.

**Ukuran sel kecil ditandai.** Estimasi dari 9 responden dan 900 responden tidak
boleh digambar dengan bobot visual sama. Tampilkan n per kelompok di label
sumbu.

**Non-respons dan hilang data dilaporkan** — sebagai kategori terpisah atau di
caption. Grafik yang diam-diam listwise-deletion menampilkan sampel yang bukan
sampel yang dijelaskan di Methods.

**SEM: hanya gambar jalur yang diestimasi.** Diagram jalur dengan panah tanpa
koefisien tidak dapat dinilai. Cantumkan β terstandardisasi, dan indeks
kecocokan model (CFI, TLI, RMSEA, SRMR) di catatan panel.

## Jebakan yang sering lolos

- Bar rerata Likert dengan sumbu 1–5 dan error bar SEM yang sangat kecil karena
  n besar, menyiratkan presisi yang tidak relevan untuk data ordinal.
- Diverging bar yang tidak menyebut apakah netral diikutkan.
- Dumbbell plot tanpa arah waktu yang jelas (mana titik awal?).
- Pie chart komposisi etnis/pendidikan dengan tujuh irisan.
- Skala warna kategori politik yang memakai merah/hijau.
- Membandingkan gelombang survei dengan instrumen yang berubah, tanpa catatan.

## Resep

```python
from vizkit import apply_style, new_figure, likert_diverging, dot_whisker, save_figure

apply_style()
fig, ax = new_figure(width="double", height_ratio=0.6)
likert_diverging(
    ax,
    items=label_item,                 # list[str], sudah diurutkan menurut % setuju
    counts=matriks_hitung,            # (n_item, n_kategori), urut STS→SS
    categories=["STS", "TS", "N", "S", "SS"],
    neutral_index=2, split_neutral=True,
    n_per_item=n_item,                # ditampilkan di ujung label
)
ax.set_title("Kesediaan memakai perangkat harian lebih tinggi daripada kenyamanan pemasangan")
save_figure(fig, "fig2_likert")
```

Dot-whisker koefisien:

```python
fig, ax = new_figure(width="single")
dot_whisker(ax, labels=nama_prediktor, est=beta, lo=ci_lo, hi=ci_hi,
            null_value=0, xlabel="β terstandardisasi (CI 95%)",
            ref_note="Acuan: perempuan, pendidikan menengah")
```

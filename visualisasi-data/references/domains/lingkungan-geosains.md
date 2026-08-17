# Lingkungan dan Geosains — hidrologi, iklim, tanah, oseanografi, geologi

Substrat bidang ini: **kedalaman/ketinggian**, **waktu bersiklus**, **penampang
melintang**, dan **peta**. Dua konvensi yang paling sering dilanggar orang luar
bidang: sumbu kedalaman harus terbalik, dan data musiman tidak boleh
dirata-ratakan tahunan tanpa menampilkan siklusnya.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Nilai per kedalaman | Profil vertikal, sumbu-y terbalik | Permukaan di atas |
| Nilai per kedalaman × waktu | Hovmöller / kontur waktu-kedalaman | Bukan garis per kedalaman |
| Nilai per waktu, berulang tahunan | Climatology + pita persentil | Tahun fokus digambar di atas pita |
| Debit sungai | Hidrograf + hyetograph terbalik di atas | Hujan turun dari atas, konvensi bidang |
| Frekuensi kejadian ekstrem | Kurva durasi / periode ulang | Sumbu probabilitas, bukan linear |
| Arah + kecepatan (angin, arus) | Wind rose / quiver | Bukan dua line plot terpisah |
| Komposisi ion air | Diagram Piper / Stiff | Standar hidrogeokimia |
| Ukuran butir tanah/sedimen | Kurva gradasi kumulatif, x log | Segitiga tekstur untuk klasifikasi |
| Lapisan stratigrafi | Kolom litologi + simbol standar | Skala kedalaman jelas |
| Orientasi struktur geologi | Stereonet / diagram mawar | Data terarah butuh statistik sirkular |
| Neraca massa/energi | Diagram Sankey | Menunjukkan input = output |
| Anomali iklim | Peta/deret divergen, pusat = normal | Nyatakan periode baseline |
| Perubahan tutupan lahan | Alluvial + peta perubahan | Bukan dua pie |

## Aturan wajib domain ini

**Sumbu kedalaman terbalik** (`ax.invert_yaxis()`), permukaan di atas.
Berlaku untuk profil tanah, kolom air, dan inti sedimen. Untuk ketinggian
atmosfer, sebaliknya.

**Anomali menyebut periode baseline-nya** ("relatif 1991–2020"). Anomali tanpa
baseline tidak punya arti, dan angkanya berubah bila baselinenya berubah.
Colormap divergen berpusat nol.

**Data berarah pakai statistik sirkular.** Rerata aritmetik dari 350° dan 10°
adalah 180°, yang salah arah. Gunakan wind rose atau rerata vektor.

**Siklus musiman ditampilkan sebelum tren.** Rerata tahunan dari data yang
puncaknya bergeser musim menyembunyikan justru mekanismenya.

**Periode ulang digambar pada sumbu probabilitas** (Gumbel/log), bukan linear —
inilah yang membuat garis frekuensi banjir dapat diekstrapolasi secara visual.
Sertakan pita ketidakpastian; ekstrapolasi 100 tahun dari 30 tahun rekaman punya
CI yang lebar dan itu harus terlihat.

**Sebutkan sumber, resolusi, dan periode data** untuk setiap dataset
penginderaan jauh atau reanalisis. Termasuk versi produk.

**Titik pengambilan sampel digambar di peta** bersama panel hasilnya. Klaim
spasial tanpa memperlihatkan sebaran titik pengambilan tidak dapat dinilai
representativitasnya.

## Jebakan yang sering lolos

- Deret waktu iklim dengan sumbu-y yang dipilih agar tren terlihat dramatis, atau
  sebaliknya diratakan.
- Smoothing (moving average) tanpa menyebut lebar jendela, dan tanpa menampilkan
  data mentah di belakangnya.
- Interpolasi spasial (IDW/kriging) yang menjalar jauh dari titik pengukuran
  tanpa masker; gambar titik pengukurannya di atas hasil interpolasi.
- Gap data yang dijembatani garis lurus sehingga terlihat kontinu. Putuskan
  garis pada gap.
- Menggabungkan instrumen/metode berbeda dalam satu deret waktu tanpa penanda
  titik pergantian.

## Resep

Climatology dengan pita persentil dan tahun fokus:

```python
from vizkit import apply_style, new_figure, save_figure
import numpy as np

apply_style()
fig, ax = new_figure(width="single")

doy = np.arange(1, 367)
ax.fill_between(doy, p10, p90, color="0.85", lw=0, label="Rentang 10–90% (1991–2020)")
ax.fill_between(doy, p25, p75, color="0.7", lw=0, label="Rentang 25–75%")
ax.plot(doy, median, c="0.35", lw=0.9, label="Median 1991–2020")
ax.plot(doy, tahun_2024, c="#d1495b", lw=1.4, label="2024")
ax.set_xlabel("Hari dalam tahun"); ax.set_ylabel("Debit (m$^3$ s$^{-1}$)")
ax.set_title("Debit 2024 berada di bawah kuartil bawah sepanjang musim kemarau")
ax.legend(frameon=False, fontsize=6, loc="upper right")
save_figure(fig, "fig3_climatology")
```

Profil vertikal: plot nilai pada sumbu-x, kedalaman pada sumbu-y, lalu
`ax.invert_yaxis()` dan `ax.xaxis.set_label_position("top"); ax.xaxis.tick_top()`.

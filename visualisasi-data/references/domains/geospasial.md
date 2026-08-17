# Geospasial — negara, provinsi, kabupaten, titik, raster

Bila unit observasinya wilayah atau titik di permukaan bumi, substratnya
**peta**. Bar chart 38 provinsi terurut membuang seluruh informasi keruangan —
padahal pola spasial (klaster, gradien barat-timur, kontras urban-rural) hampir
selalu jadi temuan yang paling menarik.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Nilai per wilayah administratif | Choropleth | **Wajib** dinormalisasi per kapita/per luas |
| Nilai per wilayah, luas sangat timpang | Kartogram atau tile-grid map | Jakarta tak boleh hilang karena kecil |
| Wilayah tanpa shapefile / ingin keterbacaan | Tile-grid (`tile_map`) | Satu kotak per wilayah, posisi relatif dijaga |
| Titik pengamatan (stasiun, sampel, kasus) | Peta titik berukuran/berwarna | Beri jitter bila bertumpuk |
| Kepadatan titik yang sangat banyak | Hexbin / kernel density | Titik individual jadi gumpalan hitam |
| Aliran antar wilayah (migrasi, perdagangan) | Peta aliran / matriks OD | Bukan dua pie |
| Nilai kontinu di grid | Raster + kontur | Sertakan skala dan proyeksi |
| Perubahan antar dua waktu | Peta selisih, divergen, pusat 0 | Bukan dua peta absolut berdampingan |
| Nilai + ketidakpastian per wilayah | Peta ganda (nilai + CI) atau arsir | Estimasi wilayah kecil tidak boleh polos |

## Aturan wajib domain ini

**Choropleth hampir selalu butuh normalisasi.** Peta jumlah kasus mentah adalah
peta jumlah penduduk. Gunakan per 100.000 penduduk, per km², atau rasio
standardisasi. Bila memang jumlah absolut yang dimaksud, gunakan simbol
proporsional (lingkaran), bukan pewarnaan wilayah.

**Batas wilayah dari shapefile resmi, bukan digambar tangan.** Sumber: BPS,
GADM, Natural Earth, atau geoBoundaries. Bila shapefile tidak tersedia di
lingkungan, **jangan menggambar peta perkiraan** — gunakan `tile_map` yang jujur
sebagai skema, atau minta user menyediakan filenya. `tile_map` sudah membawa tata
letak 38 provinsi Indonesia (`ID_PROVINSI_TILES`).

**Sebutkan proyeksinya**, dan jangan pakai Web Mercator untuk peta yang
membandingkan luas — ia melebih-lebihkan lintang tinggi secara ekstrem. Untuk
Indonesia (dekat khatulistiwa) distorsinya kecil, tapi tetap tulis proyeksinya.

**Klasifikasi nilai adalah keputusan analitik, bukan default.** Quantile,
equal-interval, dan Jenks menghasilkan peta yang terlihat sangat berbeda dari
data yang sama. Nyatakan metodenya dan jumlah kelas di caption. Untuk data
menceng, quantile; untuk perbandingan antar-waktu, gunakan **kelas yang sama**
di semua peta.

**Skala bar, panah utara, dan sumber data** ada di setiap peta. Sumber data
adalah keharusan etis, bukan hiasan.

**Wilayah tanpa data ditandai eksplisit** (abu-abu dengan pola arsir + entri
legenda "tidak ada data"), bukan dibiarkan putih — putih terbaca sebagai nilai
terendah.

**Ketidakpastian estimasi wilayah kecil.** Kecamatan dengan 12 responden dan
kecamatan dengan 1.200 responden tidak boleh diwarnai dengan bobot visual sama.
Gunakan peta berpasangan (estimasi + lebar CI) atau transparansi berbanding
presisi, dan katakan di caption.

## Jebakan yang sering lolos

- Peta yang sebenarnya peta populasi (lihat normalisasi di atas).
- Colormap pelangi pada choropleth — menciptakan batas kelas palsu.
- Divergen dengan pusat pada rerata data padahal nol yang bermakna (perubahan
  0%, rasio 1.0).
- Inset Jakarta/pulau kecil yang tidak diberi keterangan skala berbeda.
- Peta dunia yang membandingkan negara tanpa menyebut tahun data; negara sering
  punya tahun survei berbeda.
- Kabupaten yang mekar/berubah nama antar periode dicocokkan berdasarkan nama
  saja — cocokkan berdasarkan kode wilayah, dan catat pemekarannya.

## Resep

Tile-grid tanpa dependensi geospasial (selalu tersedia):

```python
from vizkit import apply_style, new_figure, tile_map, ID_PROVINSI_TILES, save_figure

apply_style()
fig, ax = new_figure(width="double", height_ratio=0.55)
tile_map(ax, ID_PROVINSI_TILES, values=prevalensi,   # dict {kode/nama: nilai}
         cmap="magma_r", label_fmt="{:.0f}",
         cbar_label="Prevalensi per 100.000 penduduk (2024)",
         missing_label="tidak ada data")
ax.set_title("Prevalensi tertinggi terkonsentrasi di Indonesia bagian timur")
save_figure(fig, "fig1_peta_prevalensi")
```

Choropleth sungguhan bila shapefile ada:

```python
# butuh geopandas: manage_packages(environment="vizkit", packages=["geopandas"])
import geopandas as gpd
gdf = gpd.read_file("data/idn_admin1.geojson").merge(df, on="kode_bps")
gdf.plot(ax=ax, column="prev_per_100k", scheme="quantiles", k=5,
         cmap="magma_r", edgecolor="white", linewidth=0.3,
         missing_kwds={"color": "0.9", "hatch": "///", "label": "tidak ada data"},
         legend=True)
ax.set_axis_off()
```

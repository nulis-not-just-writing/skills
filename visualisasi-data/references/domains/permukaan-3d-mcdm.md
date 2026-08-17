# Permukaan 3D, Response Surface, dan MCDM

Satu file untuk dua kebutuhan yang tampak berbeda tapi berbagi struktur data
yang sama: **dua input kontinu → satu luaran skalar**. Sapuan hyperparameter ML,
response surface optimasi proses, permukaan aturan fuzzy (`gensurf` MATLAB), dan
analisis sensitivitas bobot MCDM semuanya berbentuk itu.

Ditambah bagian kedua untuk MCDM secara umum, yang strukturnya berbeda:
**banyak alternatif × banyak kriteria**.

---

## Bagian A — Dua input kontinu → satu luaran

### Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Luaran pada grid dua input | **Permukaan 3D + kontur 2D berdampingan** (`surface_pair`) | Bentuk default; alasan di bawah |
| Luaran + ingin membaca nilai | Kontur/heatmap 2D saja | Bila bentuk permukaan bukan temuannya |
| Luaran + bentuk permukaan itu temuannya | Permukaan 3D + kontur | Punggungan, pelana, interaksi |
| Tiga input atau lebih | Panel kontur (satu per level input ketiga) | **Bukan** 4D |
| Titik eksperimen tidak di grid | Kontur hasil model + titik teramati di atasnya | Wajib gambar titiknya |
| Dua luaran sekaligus | Dua panel kontur bersumbu identik, atau overlay kontur | Bukan dua sumbu-z |

### Kenapa berpasangan, bukan 3D saja

Ini aturan utama bagian ini, dan alasannya perseptual bukan selera:

- Permukaan 3D menyampaikan **bentuk** dengan baik — kelengkungan, punggungan,
  pelana, ada-tidaknya interaksi antar input.
- Permukaan 3D **buruk untuk membaca nilai**: sudut pandang menyembunyikan
  bagian belakang, perspektif membuat dua tinggi yang sama tampak berbeda, dan
  pembaca tidak bisa mengambil angka dari sumbu z yang miring.
- Kontur 2D melakukan persis kebalikannya.

Menggambar hanya salah satunya berarti membuang salah satu kemampuan itu.
`surface_pair(fig, X, Y, Z, ...)` menggambar keduanya dengan skala warna dan
penanda optimum yang sama, dan memakai ruang halaman yang kurang lebih sama
dengan satu permukaan 3D besar.

### Aturan wajib

**Catat sudut pandang** (`elev`, `azim`). Sudut pandang mengubah kesimpulan yang
bisa ditarik pembaca — punggungan bisa tersembunyi di balik puncak. `surface_pair`
mencantumkannya otomatis sebagai judul kecil. Bila memilih sudut non-default,
sebutkan alasannya di caption.

**Gambar titik yang benar-benar diamati** (`data_points=`) bila permukaannya
hasil model, interpolasi, atau sistem aturan. Tanpa itu pembaca tidak bisa
membedakan wilayah yang didukung data dari ekstrapolasi — dan permukaan halus
selalu *terlihat* seperti didukung data di seluruh bidangnya. Ini kesalahan
paling sering pada figur RSM: permukaan kuadratik mulus dari 13 titik
Box-Behnken, digambar tanpa satu pun titik itu terlihat.

**Sumbu-z tidak boleh melewati rentang yang mungkin.** Akurasi tidak bisa
negatif, proporsi tidak bisa > 1, skor kompetensi tidak bisa di luar skalanya.
Bila model kuadratik mengekstrapolasi ke luar rentang sah, potong permukaannya
(mask) atau nyatakan batas validitas — jangan gambar nilai yang mustahil.

**Hindari sumbu log pada panel 3D.** Tick minor log berdesakan dan tidak
terbaca pada proyeksi miring. Bila salah satu input berskala log (learning rate,
konsentrasi), pakai log pada **panel kontur** dan gambar panel 3D dengan input
yang sudah ditransformasi (`log10 lr`) sebagai label sumbunya.

**Grid interpolasi bukan data.** Nyatakan resolusi grid dan metode
interpolasi/model di caption. Untuk RSM, sebutkan orde model dan R²/R² adjusted.

**Colormap perseptual-uniform**, dan divergen (`vcenter=`) hanya bila luarannya
bertanda relatif suatu acuan.

**Optimum ditandai di kedua panel** dengan nilainya. `surface_pair(optimum="max")`
menandai otomatis dan mengembalikan `(x, y, z)`-nya, sehingga angka di caption
dan di teks dapat diambil dari nilai yang sama — bukan diketik ulang.

### Jebakan yang sering lolos

- Permukaan mulus dari 9–15 titik eksperimen tanpa memperlihatkan titiknya.
- Sudut pandang dipilih agar puncaknya "terlihat bagus" dan lembah yang tidak
  mendukung narasi tersembunyi di belakang.
- Sumbu-z tanpa satuan, atau "Nilai" sebagai label.
- Permukaan fuzzy digambar seolah hasil pengukuran; ia adalah **luaran sistem
  aturan** — labeli demikian.
- Wireframe rapat pada grid 100×100 yang menjadi bidang hitam saat dicetak;
  pakai `rstride`/`cstride` atau grid lebih kasar.
- Dua permukaan ditumpuk dalam satu axes 3D — nyaris selalu tidak terbaca; pakai
  dua panel atau permukaan selisih.

### Resep

```python
from vizkit import apply_style, surface_pair, save_figure, check_overlaps
import matplotlib.pyplot as plt, numpy as np

apply_style()
K, P = np.meshgrid(np.linspace(0, 100, 40), np.linspace(0, 100, 40))
Z = defuzz(K, P)                     # luaran sistem aturan / model

fig = plt.figure(figsize=(180/25.4, 180/25.4*0.42))   # jangan constrained_layout
ax3, ax2, opt = surface_pair(
    fig, K, P, Z,
    xlabel="Skor kognitif", ylabel="Skor psikomotorik",
    zlabel="Kompetensi (defuzzifikasi)",
    optimum="max", levels=8,
    data_points=titik_responden)     # WAJIB bila permukaan = hasil model
print(opt)                            # (x, y, z) -> pakai angka ini di caption
check_overlaps(fig, "fig4")
save_figure(fig, "fig4_permukaan_kompetensi", dpi=330)
```

`surface_pair` menonaktifkan `constrained_layout` dan menempatkan kedua panel
secara eksplisit — matplotlib tidak dapat menghitung ukuran axes 3D dan akan
menciutkannya ke nol. Buat figure-nya **tanpa** `constrained_layout=True`.

---

## Bagian B — MCDM: banyak alternatif × banyak kriteria

Struktur ini berbeda dan lebih sering salah digambar. Skor TOPSIS/AHP/SAW/
PROMETHEE rutin disajikan sebagai tabel panjang atau bar peringkat — keduanya
menyembunyikan hal yang justru dicari analisis MCDM: **di mana trade-off-nya**.

### Bentuk kanonik

| Yang ingin ditunjukkan | Bentuk | Catatan |
|---|---|---|
| Profil alternatif lintas kriteria | **Koordinat paralel** (`parallel_coordinates`) | Trade-off = garis bersilangan |
| Peringkat akhir + kontribusi kriteria | Bar bertumpuk terurut (kontribusi tertimbang) | Bukan bar skor total polos |
| Sensitivitas terhadap bobot | Garis peringkat vs bobot satu kriteria | Menjawab kritik reviewer paling umum |
| Sensitivitas dua bobot sekaligus | Permukaan/kontur (Bagian A) | Wilayah diwarnai per alternatif pemenang |
| Perbandingan berpasangan (AHP) | Heatmap matriks + CR | Consistency Ratio wajib dilaporkan |
| Dominasi antar alternatif | Scatter dua kriteria + front Pareto | Alternatif terdominasi ditandai |
| Kesepakatan beberapa metode MCDM | Bump chart peringkat antar metode | Peringkat sering berbeda antar metode |
| Bobot dari beberapa pakar | Titik per pakar + rerata | Bukan hanya rerata bobot |

### Aturan wajib

**Kriteria biaya dibalik dan ditandai.** Dalam satu figur, "makin ke atas makin
baik" harus berlaku di semua sumbu. `parallel_coordinates(higher_better=[...])`
membalik kriteria biaya dan menandainya `↓` pada label.

**Rentang mentah tiap sumbu ditampilkan.** Koordinat paralel ternormalisasi tanpa
rentang membuat pembaca tidak bisa memulihkan nilai aslinya — dan normalisasi
min-maks membuat selisih 0,3 poin tampak sama besar dengan selisih 30 poin bila
rentangnya sempit. Helper mencantumkannya di label tick.

**Bobot dinyatakan di figur atau caption**, beserta asalnya (pakar? entropi?
AHP?). Peringkat MCDM adalah fungsi bobot; tanpa bobot, figur tidak dapat
ditafsirkan.

**Analisis sensitivitas hampir selalu diminta reviewer.** Peringkat yang berubah
saat satu bobot digeser 10% adalah temuan penting, dan menyembunyikannya
merugikan penulis sendiri saat review. Gambarkan.

**Jangan pakai radar/spider plot** sebagai figur utama meski lazim di beberapa
bidang: luas area yang terbentuk tidak punya makna, bentuknya berubah total bila
urutan kriteria diubah, dan sumbu radial sulit dibaca. Bila konvensi jurnal
target menuntutnya, gambar bentuk yang benar sebagai figur utama, **beri tahu
user** bahwa konvensi bidangnya berbeda, dan biarkan dia yang memutuskan.

**Skala normalisasi disebutkan** (min-maks, vektor, atau linear sum) — hasil
peringkat berbeda antar pilihan, dan itu bagian dari metode.

### Jebakan yang sering lolos

- Bar skor TOPSIS dengan tiga desimal, memberi kesan presisi yang tidak dimiliki
  metode berbobot subjektif.
- Alternatif diurutkan menurut abjad/kode, bukan menurut peringkat.
- Consistency Ratio AHP tidak dilaporkan (ambang lazim CR < 0,1).
- Koordinat paralel dengan 40 alternatif tanpa penonjolan — jadi bola benang.
  Pakai `focal=` untuk menonjolkan yang dibahas, sisanya abu-abu.
- Peringkat dari beberapa metode MCDM ditampilkan sebagai tabel, padahal
  perbedaannya justru layak dibahas.

### Resep

```python
from vizkit import apply_style, new_figure, parallel_coordinates, save_figure

apply_style()
fig, ax = new_figure(width="double", height_ratio=0.44)
parallel_coordinates(
    ax,
    labels=alternatif,                        # mis. paket pelatihan / siswa
    criteria=["Kognitif", "Psikomotorik", "Sikap", "Biaya", "Durasi"],
    values=matriks_keputusan,                 # (n_alternatif, n_kriteria) MENTAH
    higher_better=[True, True, True, False, False],
    focal=["A3", "A6"],                       # yang dibahas di teks
)
ax.set_title("A3 unggul pada kognitif tetapi kalah pada biaya pelatihan")
save_figure(fig, "fig3_mcdm_profil")
```

Untuk sensitivitas dua bobot sekaligus, hitung skor pada grid `(w1, w2)` lalu
pakai `surface_pair` dari Bagian A — atau, bila yang menarik adalah **alternatif
mana yang menang** di tiap kombinasi bobot, gambar peta wilayah kemenangan
(`ax.contourf` dengan indeks pemenang dan colormap kategorikal).

# SEM: PLS-SEM (SmartPLS) dan CB-SEM

Figur utama bidang ini adalah **diagram jalur**, dan kesalahan yang paling
sering ditemukan reviewer bukan soal model melainkan soal berkasnya: tangkapan
layar SmartPLS/AMOS beresolusi rendah, fontnya tidak dapat diatur, dan angkanya
tidak terbaca setelah diperkecil ke lebar kolom.

**Jangan pernah menempelkan tangkapan layar perangkat lunak SEM sebagai figur
naskah.** Gambar ulang modelnya dari angka hasil estimasi
(`pls_path_diagram`). Selain lolos syarat resolusi, figurnya jadi dapat
direproduksi dan angkanya dijamin sama dengan tabel.

## Dua gaya tampilan

`pls_path_diagram(..., style=...)` menyediakan dua tampilan dari data yang sama:

| `style` | Tampilan | Kapan dipakai |
|---|---|---|
| `"journal"` (bawaan) | Kotak putih bergaris, satu hue | Naskah jurnal; aman untuk cetak grayscale |
| `"smartpls"` | Lingkaran biru + persegi indikator kuning | Bila pembaca/penguji terbiasa dengan tampilan SmartPLS dan ingin mengenalinya seketika |

Keduanya digambar ulang dari angka estimasi, jadi resolusi, ukuran font, dan
reproduktibilitasnya sama-sama benar — `"smartpls"` **bukan** tangkapan layar,
hanya meniru bahasa visualnya.

Satu peringatan untuk `"smartpls"`: kuning indikator berkontras rendah terhadap
putih dan hilang pada cetak hitam-putih. Bila jurnal target mencetak grayscale
atau mengenakan biaya untuk figur berwarna, pakai `"journal"`.

Pada gaya `"smartpls"` diameter lingkaran **diukur dari label terpanjang**
(termasuk baris R²), lalu jarak antar kolom dan posisi tepi disesuaikan supaya
tidak ada lingkaran yang bersentuhan atau terpotong. Nama konstruk yang panjang
karena itu memperbesar seluruh diagram — pertimbangkan singkatan dengan
kepanjangan di caption.

## Reflektif vs formatif

Arah panah pengukuran adalah **klaim teoretis**, bukan pilihan tampilan:

```python
pls_path_diagram(ax, konstruk, jalur, indicators=ind,
                 mode="reflective")                    # konstruk -> indikator
pls_path_diagram(ax, konstruk, jalur, indicators=ind,
                 mode={"PEU": "formative", "INT": "reflective"})   # campuran
```

Model reflektif: konstruk menyebabkan indikatornya (panah keluar dari
konstruk), indikator saling berkorelasi dan dapat dipertukarkan. Model
formatif: indikator membentuk konstruk (panah masuk ke konstruk), dan
kriteria evaluasinya berbeda — bukan loading dan AVE, melainkan bobot luar,
VIF, dan signifikansi bobot. Menggambar arah yang salah berarti menyajikan
model yang salah.

## Bentuk kanonik

| Yang ingin ditunjukkan | Bentuk | Catatan |
|---|---|---|
| Model struktural + hasil | **Diagram jalur** (`pls_path_diagram`) | β, signifikansi, R² di dalam kotak |
| Model dengan indikator | Diagram jalur + kotak indikator + loading | Hanya bila model kecil; jika besar, pindah ke tabel |
| Koefisien jalur + CI bootstrap | Dot-whisker (`dot_whisker`) | CI persentil bootstrap, bukan bintang saja |
| Validitas diskriminan (HTMT) | Heatmap segitiga bawah + ambang | Ambang 0,85/0,90 digambar |
| Reliabilitas & AVE per konstruk | Dot plot + garis ambang (0,7 / 0,5) | Bukan tabel bila konstruknya banyak |
| Loading vs cross-loading | Heatmap indikator × konstruk | Cross-loading tinggi langsung terlihat |
| Efek moderasi | Simple slope plot (garis per level moderator) | Wajib; β interaksi saja tidak cukup |
| Efek mediasi | Diagram jalur + tabel efek langsung/tak langsung | Sebutkan jenis mediasi (VAF/Zhao) |
| Analisis multigrup (MGA) | Dot-whisker berpasangan per kelompok | Beda antar-kelompok beserta p |
| IPMA (importance-performance) | Scatter kepentingan × kinerja + garis rerata | Kuadran diberi label |
| Prediksi out-of-sample | PLSpredict: Q², RMSE vs benchmark LM | Semakin diminta reviewer |

## Aturan wajib domain ini

**Jalur tidak signifikan tetap digambar** — putus-putus, tipis, berlabel "n.s.".
Hipotesis yang tidak didukung adalah hasil. `pls_path_diagram` menggambarnya
demikian dan mengembalikan daftar `tidak_signifikan` supaya tidak lolos tanpa
disadari.

**R² ditulis di dalam kotak konstruk endogen**, bukan hanya di tabel. Bila
memakai R² adjusted, katakan yang mana.

**Nyatakan apa yang dilaporkan pada jalur.** β terstandardisasi? Nilai t?
p bootstrap? Berapa subsampel bootstrap (biasanya 5.000) dan jenis selang
kepercayaannya (percentile / BCa)? Ini bagian dari metode, dan reviewer
PLS-SEM hampir selalu menanyakannya.

**PLS-SEM tidak punya uji kecocokan model klasik.** Jangan mencantumkan CFI,
TLI, atau RMSEA pada diagram PLS — itu milik CB-SEM. Untuk PLS laporkan SRMR
(dengan hati-hati), R², f², Q², dan bila relevan hasil PLSpredict. Untuk
CB-SEM barulah indeks kecocokan disertakan, lengkap dengan χ²/df.

**Indikator hanya digambar bila modelnya kecil.** Model dengan 6 konstruk × 5
indikator menghasilkan 30 kotak yang tidak terbaca pada lebar kolom. Gambarkan
model strukturalnya saja dan pindahkan loading ke tabel pengukuran — itu yang
lazim di jurnal, dan lebih terbaca.

**Ukuran sampel dan metode estimasi disebutkan** di caption: n, algoritma
(PLS path weighting), skema pembobotan, dan penanganan data hilang.

**Moderasi butuh simple slope plot.** Koefisien interaksi yang signifikan tidak
memberi tahu pembaca *bentuk* moderasinya — apakah memperkuat, melemahkan, atau
membalik arah. Gambarkan garis hubungan pada −1 SD, rerata, dan +1 SD moderator.

**Arah panah adalah klaim teoretis, bukan hasil.** Model reflektif dan formatif
digambar berbeda (panah dari konstruk ke indikator vs sebaliknya). Nyatakan
jenis pengukuran tiap konstruk; salah gambar berarti salah model.

## Jebakan yang sering lolos

- Tangkapan layar SmartPLS dengan latar abu-abu dan font bawaan yang buram.
- Diagram yang menampilkan nilai t di panah tapi caption menyebut β.
- Panah dua arah antar konstruk pada model PLS rekursif (PLS standar tidak
  mengestimasi model non-rekursif) — `pls_path_diagram` menolak model bersiklus.
- HTMT dilaporkan hanya sebagai "semua < 0,85" tanpa matriksnya.
- Mediasi diklaim dari signifikansi jalur a dan b saja, tanpa menguji efek tak
  langsung a×b beserta CI bootstrap-nya.
- R² tinggi ditonjolkan pada model dengan konstruk endogen berindikator tunggal.
- Diagram yang kotaknya berbeda ukuran tanpa alasan — ukuran kotak tidak
  mengkodekan apa pun; jangan biarkan pembaca menyangka demikian.

## Resep

```python
from vizkit import apply_style, new_figure, pls_path_diagram, save_figure, check_overlaps

apply_style()
konstruk = {"PEU": "Persepsi\\nKemudahan", "PU": "Persepsi\\nKegunaan",
            "ATT": "Sikap", "INT": "Niat\\nMenggunakan"}
jalur = {                       # angka diambil dari keluaran bootstrap
    ("PEU", "PU"):  {"beta": 0.512, "p": 0.000},
    ("PU",  "ATT"): {"beta": 0.436, "p": 0.000},
    ("PEU", "ATT"): {"beta": 0.221, "p": 0.014},
    ("ATT", "INT"): {"beta": 0.604, "p": 0.000},
    ("PU",  "INT"): {"beta": 0.078, "p": 0.312},   # n.s. -> tetap digambar
}
fig, ax = new_figure(width="double", height_ratio=0.46)
res = pls_path_diagram(ax, konstruk, jalur,
                       r2={"PU": 0.262, "ATT": 0.381, "INT": 0.447})
print(res["tidak_signifikan"])      # harus dibahas di Discussion
check_overlaps(fig, "fig2"); save_figure(fig, "fig2_model_struktural")
```

Tata letak disusun otomatis menurut kedalaman topologis (eksogen di kiri,
endogen di kanan); rantai lurus diselang-seling naik-turun agar jalur yang
melompati kolom tidak menembus kotak. Untuk tata letak sesuai gambar teori,
berikan `positions={"PEU": (0.1, 0.5), ...}`.

Indikator (opsional, hanya untuk model kecil):

```python
indikator = {"PEU": [("PEU1", 0.81), ("PEU2", 0.87), ("PEU3", 0.79)],
             "INT": [("INT1", 0.88), ("INT2", 0.91)]}
pls_path_diagram(ax, konstruk, jalur, indicators=indikator, r2=r2)
```

Tampilan gaya SmartPLS (lingkaran biru + persegi kuning):

```python
fig, ax = new_figure(width="double", height_ratio=0.64)   # lingkaran butuh tinggi
pls_path_diagram(ax, konstruk, jalur, indicators=indikator, r2=r2,
                 style="smartpls")
```

## Memindahkan angka dari SmartPLS

Jangan mengetik ulang angka dari layar — itu sumber ketidakcocokan figur-tabel
yang paling sering lolos. Ekspor hasilnya, lalu baca berkasnya:

```python
import pandas as pd
pc = pd.read_excel("report.xlsx", sheet_name="Path Coefficients")
bt = pd.read_excel("report.xlsx", sheet_name="Bootstrapping")   # p / t
jalur = {(r["from"], r["to"]): {"beta": r["beta"], "p": r["p"]}
         for _, r in gabung.iterrows()}
```

Nama sheet dan kolom berbeda antar versi SmartPLS, jadi **cetak dulu
`pd.ExcelFile(path).sheet_names` dan `df.columns`** sebelum menulis pemetaan —
jangan mengasumsikan nama kolom. Setelah itu, angka di figur dan di tabel
berasal dari berkas yang sama dan tidak mungkin berbeda (aturan 1.8).

Simple slope moderasi (matplotlib biasa, tidak butuh helper khusus):

```python
for lvl, gaya in ((-1, ":"), (0, "-"), (+1, "--")):
    y = b0 + (b_x + b_int * lvl) * x_grid      # moderator pada -1/0/+1 SD
    ax.plot(x_grid, y, ls=gaya, c=hue, label=f"Moderator {lvl:+d} SD")
```

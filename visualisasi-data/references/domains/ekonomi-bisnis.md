# Ekonomi, Keuangan, dan Bisnis

Substrat bidang ini: **sumbu waktu dengan struktur** (musiman, rezim, guncangan),
**dekomposisi perubahan**, dan **distribusi yang menceng ekstrem**. Dua
kesalahan yang paling merusak kredibilitas: memotong sumbu nilai agar tren
terlihat dramatis, dan menampilkan nominal ketika yang bermakna adalah riil atau
per kapita.

Untuk regresi lintas-seksi dan data survei umum, lihat `sosial-survei.md`.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Kontribusi komponen ke perubahan total | **Waterfall** (`waterfall`) | Laba, varians anggaran, dekomposisi pertumbuhan |
| Efek per periode di sekitar guncangan | **Event study** (`event_study`) | DiD dinamis, ITS; koefisien pra = uji tren paralel |
| Ketimpangan distribusi | **Kurva Lorenz + Gini** (`lorenz_curve`) | Pendapatan, aset, konsentrasi pelanggan |
| Indikator lintas waktu, banyak entitas | Spaghetti + sorotan entitas fokus | Bukan tabel panel |
| Harga aset harian | Garis + pita volatilitas; return, bukan level | Level harga tidak stasioner |
| Distribusi return | Histogram + QQ plot vs normal | Ekor tebal adalah temuannya |
| Dua indikator berbeda satuan | Dua panel bersumbu-x sama, atau indeks (basis = 100) | **Bukan** sumbu-y ganda |
| Peringkat entitas antar waktu | Bump chart | Perubahan posisi terlihat |
| Struktur biaya/pendapatan | Stacked bar/area + total di atasnya | Batasi ke 5–6 komponen + "lainnya" |
| Portofolio risiko-imbal hasil | Scatter + frontier efisien | Ukuran = bobot/nilai |
| Elastisitas / hubungan log-log | Scatter log-log + garis regresi | Kemiringan = elastisitas, cantumkan |
| Rasio keuangan lintas perusahaan | Dot plot terurut + median industri | Bukan bar per perusahaan |
| Alur dana/barang | Sankey (`alluvial`) | Neraca harus seimbang |
| Siklus bisnis | Deret + pita resesi berbayang | Sumber penanggalan resesi disebut |
| Perkiraan ke depan | Fan chart (pita interval bertingkat) | Ketidakpastian melebar ke depan |
| Konsentrasi pasar | HHI/CR4 lintas waktu, atau Lorenz | Definisi pasar dinyatakan |

## Aturan wajib domain ini

**Sumbu nilai dimulai dari nol untuk bar.** Untuk garis, sumbu boleh dipotong,
tapi potongannya harus terlihat dan skalanya jujur. Sumbu-y yang dipilih agar
kenaikan 2% memenuhi tinggi panel adalah manipulasi visual, dan reviewer
ekonomi terlatih menangkapnya.

**Nominal vs riil, dan per kapita.** Deret nominal jangka panjang hampir selalu
menyesatkan. Nyatakan deflator dan tahun dasar ("harga konstan 2020"), atau
alasan memakai nominal. Perbandingan antar-negara/wilayah dinormalisasi per
kapita atau terhadap PDB.

**Sumbu-y ganda dilarang** untuk dua deret berbeda satuan pada satu panel.
Korelasi visual yang dihasilkannya sepenuhnya artefak pilihan skala. Pakai dua
panel bersusun dengan sumbu-x identik, atau indeks berbasis 100 pada periode
acuan.

**Skala log untuk pertumbuhan.** Bila datanya tumbuh eksponensial, sumbu log
membuat laju pertumbuhan yang sama terlihat sebagai kemiringan yang sama —
itulah yang biasanya ingin dibandingkan. Beri tick terbaca manusia (1k, 10k).

**Mata uang, satuan, dan periode di label sumbu**, termasuk apakah miliar/triliun
dan apakah kurs tetap atau berlaku. "Rp" saja tidak cukup.

**Event study wajib menampilkan koefisien pra-perlakuan.** Itu uji asumsi tren
paralel yang bisa dinilai pembaca; menyembunyikannya adalah kelalaian serius.
`event_study` mengembalikan daftar periode pra yang signifikan supaya tidak
lolos tanpa disadari. Periode acuan digambar sebagai titik kosong berlabel, bukan
dihilangkan.

**Galat baku yang dikelompokkan.** Data panel perusahaan/wilayah butuh clustered
SE; CI naif jauh terlalu sempit. Nyatakan tingkat klasternya di caption.

**Gini dihitung dari data yang digambar.** Jangan mengutip Gini dari sumber lain
sementara kurvanya dari sampel sendiri. `lorenz_curve` mengembalikan Gini yang
dihitung dengan trapesium pada kurva yang tergambar, sehingga keduanya tidak
mungkin berbeda.

**Waterfall harus berjumlah benar.** Awal + Σ komponen = akhir. Bila ada
komponen "lain-lain" yang besar, itu tanda dekomposisinya belum selesai — jangan
sembunyikan sebagai residual.

## Jebakan yang sering lolos

- Grafik saham/penjualan dengan sumbu dimulai dari nilai minimum data.
- Pertumbuhan year-on-year dibandingkan dengan basis yang berbeda (efek basis
  rendah pasca-krisis) tanpa catatan.
- Deret yang menggabungkan metodologi statistik berbeda (perubahan tahun dasar
  BPS, revisi definisi) tanpa penanda titik sambungan.
- Proyeksi digambar dengan gaya garis yang sama dengan data historis — bedakan
  (putus-putus + pita ketidakpastian) dan beri garis vertikal di batas data.
- Pie chart pangsa pasar tujuh pemain.
- Rerata pendapatan pada distribusi yang menceng — laporkan median, dan bila
  memakai rerata, katakan alasannya.
- Sampel yang hanya berisi perusahaan yang bertahan (survivorship bias) tanpa
  disebut.

## Resep

Dekomposisi laba (waterfall):

```python
from vizkit import apply_style, new_figure, waterfall, save_figure, check_overlaps

apply_style()
fig, ax = new_figure(width="single", height_ratio=0.9)
st = waterfall(ax,
               labels=["Volume", "Harga", "Biaya bahan", "Beban SDM", "Kurs"],
               deltas=[42., 18., -27., -13., 6.],
               start=180.,
               start_label="Laba 2024", end_label="Laba 2025")
ax.set_ylabel("Laba operasi (miliar Rp, harga berlaku)")
assert abs(st["akhir"] - laba_2025_dilaporkan) < 0.5   # jumlah harus cocok
ax.set_title("Kenaikan harga tertutup oleh biaya bahan baku")
check_overlaps(fig, "fig3"); save_figure(fig, "fig3_waterfall_laba")
```

Rotasi label sumbu-x dipilih otomatis lewat pengukuran (0/30/45/60/90°) sampai
label tidak bertabrakan — tidak perlu diatur manual.

Event study:

```python
fig, ax = new_figure(width="single")
st = event_study(ax, periods=t, coefs=beta, lo=ci_lo, hi=ci_hi,
                 ref_period=-1, treat_at=-0.5,
                 ylabel="Δ log penjualan (CI 95%, klaster per wilayah)")
if st["pra_signifikan"]:
    print("PERINGATAN tren paralel:", st["pra_signifikan"])   # harus dibahas
ax.set_title("Tidak ada tren pra-perlakuan; efek muncul sejak periode 0")
```

Ketimpangan:

```python
fig, ax = new_figure(width="single", height_ratio=1.0)
gini = lorenz_curve(ax, pendapatan_rt, label="Pendapatan rumah tangga 2025")
ax.legend(loc="upper left", bbox_to_anchor=(0, 0.82))
# `gini` inilah angka yang dikutip di teks — bukan diketik ulang
```

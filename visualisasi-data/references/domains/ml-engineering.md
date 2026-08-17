# Machine Learning, Sistem, dan Rekayasa

Bidang ini paling sering jatuh ke tabel angka dan bar akurasi. Padahal
substratnya kaya: **ruang trade-off**, **matriks kebingungan**, **kurva
belajar**, **jalur pipeline**, dan **ruang hyperparameter**.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Model pada dua metrik yang bertukar | Scatter + front Pareto | Akurasi vs latensi/parameter/energi |
| Prediksi vs kelas sebenarnya | Confusion matrix ternormalisasi baris | Bukan satu angka akurasi |
| Komponen yang dilepas | Ablasi: batang selisih dari model penuh | Nol = model penuh, bukan nol absolut |
| Performa vs ukuran data/model | Kurva belajar / scaling, sumbu log-log | Sertakan pita antar-seed |
| Performa per epoch | Kurva train/val + tanda early stopping | Keduanya, jangan train saja |
| Hasil pencarian hyperparameter | Coordinate/parallel-coordinates plot | Bukan tabel grid |
| Kontribusi fitur | SHAP beeswarm / permutation importance + CI | Bukan bar importance polos |
| Latensi/throughput | Distribusi + persentil p50/p95/p99 | Rerata latensi menyembunyikan ekor |
| Arsitektur / alur data | Diagram blok berlabel | Kata dan glif sama dengan panel data |
| Perbandingan pada banyak dataset | Critical-difference diagram | Setelah uji Friedman–Nemenyi |
| Kegagalan model | Galeri contoh salah klasifikasi | Kualitatif, sangat meyakinkan |

## Aturan wajib domain ini

**Multi-seed adalah tulang punggung, bukan pelengkap.** Satu angka akurasi dari
satu seed tidak dapat dinilai. Jalankan minimal 3–5 seed, gambar tiap seed di
belakang rerata (`spread_lines` + `mean_line`) atau sebagai titik per seed
dengan bar rerata. Selisih 0,4 poin antara dua metode yang variabilitas
antar-seed-nya 1,2 poin bukan temuan.

**Bar akurasi tanpa sumbu nol yang benar adalah manipulasi.** Bila memotong
sumbu untuk melihat selisih kecil, potongan harus terlihat eksplisit dan
selisihnya harus lolos uji.

**Ablasi digambar relatif terhadap model penuh.** Sumbu = Δ metrik, nol =
model penuh, batang ke kiri berarti komponen itu penting. Ini langsung menjawab
pertanyaan reviewer, sementara bar akurasi absolut memaksanya mengurangi
sendiri.

**Baseline dilabeli dengan apa dia, bukan perannya.** "Regresi logistik pada
fitur band-power", bukan "baseline". Pembanding digambar abu-abu, metode sendiri
pekat.

**Anggaran komputasi disebutkan.** Perbandingan model yang salah satunya
dilatih 10× lebih lama bukan perbandingan. Cantumkan di panel atau caption:
jumlah parameter, epoch, atau GPU-hour.

**Latensi dilaporkan sebagai distribusi.** p50/p95/p99, bukan rerata. Untuk
sistem interaktif, ekornyalah yang dirasakan pengguna.

**Confusion matrix dinormalisasi per baris** (recall per kelas) dan nilainya
dicetak di setiap sel. Untuk kelas timpang, matriks jumlah mentah didominasi
kelas mayoritas dan tidak informatif.

**Kurva belajar log-log** bila menguji hukum skala, dengan kemiringan yang
dicantumkan. Sumbu linear menyembunyikan hubungan pangkat.

## Jebakan yang sering lolos

- Kurva validasi yang berhenti tepat di titik terbaik (cherry-picked epoch).
  Gambar sampai akhir pelatihan, tandai titik yang dipilih.
- Front Pareto digambar sebagai garis yang melewati titik non-dominan.
- Bar chart untuk 12 varian ablasi yang urutannya menurut nama file, bukan
  menurut besar efek.
- Metrik yang berbeda definisinya antar panel (macro-F1 di satu, weighted-F1 di
  lain) dengan label "F1" yang sama.
- Sumbu-y ganda akurasi dan loss dalam satu panel.

## Resep

Ablasi relatif + sebaran seed:

```python
from vizkit import apply_style, new_figure, points_with_mean, save_figure
import numpy as np

apply_style()
fig, ax = new_figure(width="single")

delta = {k: acc[k] - acc["penuh"] for k in komponen}      # matriks (n_seed,)
y = np.arange(len(komponen))
for i, k in enumerate(komponen):
    ax.scatter(delta[k], np.full_like(delta[k], i) + np.random.uniform(-.08, .08, delta[k].size),
               s=8, c="0.6", lw=0, zorder=2)
    m = delta[k].mean()
    ax.plot([0, m], [i, i], lw=3, c="#1f6feb", solid_capstyle="butt", zorder=1)
ax.axvline(0, c="0.2", lw=0.8)
ax.set_yticks(y); ax.set_yticklabels(label_komponen)
ax.set_xlabel("Δ akurasi seimbang vs. model penuh (poin)")
ax.set_title("Menghapus adaptasi per-subjek paling merugikan performa")
ax.text(1.0, 1.02, "n = 5 seed", transform=ax.transAxes, ha="right", fontsize=6)
save_figure(fig, "fig4_ablasi")
```

Confusion matrix: `confusion_matrix(ax, cm, labels, normalize="row")` dari
`vizkit`.

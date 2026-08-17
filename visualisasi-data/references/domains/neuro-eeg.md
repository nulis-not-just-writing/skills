# Neurofisiologi — EEG, MEG, fNIRS, ERP, BCI

Substrat domain ini adalah **kepala**, **sumbu waktu terkunci-stimulus**, dan
**bidang waktu-frekuensi**. Hampir semua kesalahan visual di bidang ini berasal
dari membuang salah satu substrat itu dan menggantinya dengan sumbu kategori.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Nilai per elektroda (satu kondisi) | Topografi (`topomap`) | Interpolasi di dalam kepala |
| Subset kanal / montase | Glif kepala (`montage_glyph`) | Elektroda aktif pekat, sisanya kosong |
| Amplitudo per waktu, per kondisi | Butterfly / ERP overlay | Sumbu waktu, 0 = onset stimulus |
| Daya per waktu × frekuensi | Peta TF (pcolormesh) | Divergen bila ERD/ERS relatif baseline |
| Daya per band per region | Bar band + titik subjek | Band slot lebar sama, label Hz |
| Pasangan elektroda (konektivitas) | Busur di atas kepala / matriks | Ambang eksplisit, jangan gambar semua |
| Klaster signifikan lintas kanal-waktu | Raster kanal × waktu + kontur klaster | Hasil permutation test |
| Akurasi decoding per waktu | Kurva waktu + pita chance + bar klaster | Chance level digambar, bukan diasumsikan |
| Trial per subjek | Raster/ERPimage | Trial diurutkan menurut variabel perilaku |

## Aturan wajib domain ini

**Posisi elektroda diambil dari montase standar, tidak diperkirakan.**
`electrode_xy()` di `vizkit.py` memuat koordinat 10-20/10-10 dari tabel bawaan
yang diturunkan dari montase standar (`standard_1020`). Bila MNE terpasang,
`electrode_xy(..., prefer_mne=True)` membacanya langsung dari MNE. Jangan
menempatkan elektroda dengan mengira-ngira sudut.

**Gambar hidung dan telinga.** Tanpa penanda arah, pembaca tidak bisa tahu mana
anterior. `draw_head()` menggambar outline + nasion + preaurikular.

**Skala warna topografi harus simetris untuk kuantitas bertanda.** Beda kondisi,
nilai t, ERD/ERS: `vmin=-vmax`, colormap divergen, nol tepat di tengah. Untuk
kuantitas satu arah (daya absolut), sekuensial.

**Satu skala warna untuk satu deret topografi.** Bila menampilkan topografi
beberapa kondisi berdampingan, semuanya memakai `vmin`/`vmax` yang sama dan satu
colorbar bersama. Colorbar per panel dengan skala berbeda membuat perbandingan
antar-panel mustahil, dan itu justru tujuan panelnya berdampingan.

**Tandai elektroda yang signifikan di atas topografi**, jangan buat panel
terpisah. Titik putih besar / tanda silang pada posisi elektroda yang lolos
koreksi.

**Sumbu waktu ERP: nol = onset, dan katakan onset apa.** Sertakan periode
baseline di dalam rentang plot, beri garis vertikal di 0. Konvensi polaritas
(negatif ke atas) masih dipakai sebagian lab — bila dipakai, **tulis di sumbu**,
jangan biarkan pembaca menebak.

**Band frekuensi: slot lebar sama dengan rentang Hz di label.** Sumbu log
frekuensi sungguhan membuat delta (0,5–4 Hz) jadi blok terlebar dan alfa
(8–13 Hz) salah satu tersempit — menarik mata ke band yang justru tidak
diinterpretasi. Pakai slot sama lebar, tulis "Theta (4–8 Hz)" di ticknya.

**Band yang tidak diinterpretasi digambar arsir tanpa isian** dan dianotasi
sebagai dikesampingkan (mis. kenaikan gamma yang diduga artefak miogenik).
Hadir, tapi terlihat bukan bagian dari argumen.

**Konektivitas: jangan gambar semua pasangan.** 14 kanal = 91 pasangan; semuanya
digambar menjadi bola benang. Beri ambang (nilai atau top-k setelah koreksi),
nyatakan ambangnya di caption, dan tebal garis mengkodekan kekuatan.

**Jumlah trial setelah artifact rejection wajib dilaporkan** — di caption atau
panel. Perbedaan jumlah trial antar kondisi adalah confound yang bisa dilihat
reviewer dari figur.

## Jebakan yang sering lolos

- Topografi dari 14 kanal digambar dengan interpolasi sehalus 64 kanal, sehingga
  terlihat punya resolusi spasial yang tidak dimilikinya. **Selalu gambar titik
  elektrodanya**, dan untuk montase jarang pertimbangkan kontur kasar.
- Interpolasi menjalar ke luar batas kepala. Gunakan masking lingkaran (sudah
  ditangani `topomap`).
- Rerata grand-average tanpa sebaran antar-subjek. EEG bervariasi besar antar
  individu; gambar tiap subjek tipis di belakang, atau pita CI.
- Kurva decoding tanpa garis chance, atau chance diasumsikan 50% padahal kelas
  tidak seimbang.
- Judul "decoder mengungguli baseline" pada panel yang selisihnya tidak lolos
  FDR.

## Resep

```python
from vizkit import (apply_style, new_figure, save_figure, topomap,
                    montage_glyph, spread_lines, mean_line, sig_stars,
                    check_overlaps)
import numpy as np

apply_style()
fig, axes = new_figure(width="double", nrows=1, ncols=3)

# Topografi tiga kondisi, satu skala warna bersama
chs = ["AF3","F7","F3","FC5","T7","P7","O1","O2","P8","T8","FC6","F4","F8","AF4"]
vmax = np.abs(np.stack([nilai[k] for k in kondisi])).max()
for ax, k in zip(axes, kondisi):
    im = topomap(ax, chs, nilai[k], vmin=-vmax, vmax=vmax, cmap="RdBu_r",
                 signif=lolos_fdr[k])          # titik putih di kanal signifikan
    ax.set_title(f"{k}")
cb = fig.colorbar(im, ax=axes, fraction=0.03)
cb.set_label("Δ daya theta (dB, vs. baseline)")

check_overlaps(fig, "fig3")
save_figure(fig, "fig3_topografi_theta")
```

Glif montase di atas kurva ablasi:

```python
montage_glyph(ax_glif, all_channels=chs, active=["AF3","AF4","F3","F4"],
              hue="#1f6feb", size=0.9)
```

# Pendidikan dan Asesmen

Bidang ini punya dua substrat yang khas dan sering diabaikan: **skala laten
bersama** (kemampuan peserta dan kesulitan butir pada satu sumbu) dan
**lintasan belajar per peserta**. Kesalahan paling merusak di sini bukan soal
estetika, melainkan menyajikan skor mentah seolah interval dan merata-ratakan
kelas seolah individu.

Untuk konvensi kuesioner/Likert dan model regresi umum, lihat juga
`sosial-survei.md`; file ini menangani yang khas pendidikan.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Peserta **dan** butir pada satu skala | **Peta Wright** (`wright_map`) | Rasch/IRT; menjawab apakah tes menjangkau peserta |
| Butir: kesulitan × daya beda | Scatter dengan zona penerimaan | Butir bermasalah dilabeli langsung |
| Peluang jawab benar vs kemampuan | Kurva karakteristik butir (ICC) | Satu kurva per butir, atau kurva informasi tes |
| Skor pra dan pasca per peserta | Slope plot (`slope_plot`) | Bukan dua bar rerata |
| Skor lintas beberapa waktu | Spaghetti + rerata model | Menampilkan variasi lintasan |
| Peserta bersarang dalam kelas/sekolah | Caterpillar plot efek acak + CI | Bukti sebaran antar-sekolah, bukan satu ICC |
| Distribusi skor antar kelas/sekolah | Ridgeline (`ridgeline`) | Bimodalitas terlihat, box plot menyembunyikan |
| Sebaran nilai vs ambang KKM | Histogram + garis ambang | Perhatikan penumpukan tepat di ambang |
| Pilihan jawaban pengecoh | Analisis distraktor (proporsi per opsi × kuintil) | Pengecoh yang tak pernah dipilih itu temuan |
| Kesalahan konsepsi | Matriks tema × peserta | Lihat `kualitatif.md` |
| Rubrik multi-dimensi | Dot-whisker per dimensi | Bukan radar plot |
| Alur peserta antar level | Alluvial (`alluvial`) | Perpindahan level kompetensi |
| Waktu sampai tuntas/putus | Kurva survival | Retensi, kelulusan tepat waktu |
| Kesepakatan antar-penilai | Bland-Altman atau matriks kappa | Rubrik butuh bukti reliabilitas |
| Kompetensi dari dua sub-skor | Permukaan 3D + kontur | Lihat `permukaan-3d-mcdm.md` |

## Aturan wajib domain ini

**Skor mentah bukan skala interval.** Selisih 5 poin di rentang tengah tidak
sama dengan 5 poin di ujung atas. Bila studi memakai Rasch/IRT, gambarkan pada
skala logit dan katakan demikian; bila memakai skor mentah, jangan menghitung
selisih rerata seolah interval tanpa menyebut batasannya.

**Peta Wright wajib melaporkan kesenjangan dan penjangkauan.** Dua hal yang
dicari pembaca: (a) apakah sebaran butir menutupi sebaran peserta — butir
menumpuk di logit 0 sementara peserta di +2 berarti tes terlalu mudah; (b)
adakah celah pada skala tanpa butir, yaitu rentang kemampuan yang tak terukur.
`wright_map` mengembalikan keduanya sebagai angka, jadi caption dapat memakai
nilai yang sama dengan yang tergambar.

**Sekolah/kelas adalah unit klaster.** Data siswa bersarang; galat baku naif
terlalu kecil dan CI terlalu sempit. Bila analisisnya multilevel, gambarkan
sebaran efek acak antar-sekolah (caterpillar plot), bukan hanya koefisien level
siswa.

**Ukuran efek, bukan hanya p.** Cohen's d atau Hedges' g dengan CI; untuk
pra-pascates gunakan d yang memperhitungkan korelasi berpasangan dan nyatakan
mana yang dipakai. Selisih signifikan pada n = 300 bisa berukuran efek
sepele — dan figur yang hanya menampilkan bintang menyembunyikannya.

**Normalized gain punya batas.** Bila memakai N-gain Hake, ingat nilainya tidak
stabil untuk pretest sangat tinggi (penyebut mengecil). Tampilkan sebaran
individualnya, bukan hanya rerata kelas.

**Drop-out digambar, bukan dihapus diam-diam.** Peserta yang tidak mengikuti
pascates membuat rerata pascates naik seolah membaik. Laporkan jumlahnya dan
apakah analisisnya intention-to-treat atau complete-case.

**Anonimitas peserta.** Jangan menampilkan nama, NIS, atau kombinasi atribut
yang mengidentifikasi (satu-satunya siswa perempuan di kelas X). Kode peserta
konsisten (P01, S03).

## Jebakan yang sering lolos

- Bar rerata pretest-posttest dua batang dengan error bar SEM: menyembunyikan
  bahwa sebagian siswa justru menurun. Pakai slope plot.
- Sumbu skor 0–100 dipotong mulai 60 agar selisih tampak besar.
- Rerata kelas dibandingkan seolah unit independen padahal jumlah kelasnya
  empat.
- Nilai dengan dua desimal dari rubrik berskala 1–4.
- Grafik "peningkatan" yang sebenarnya regresi ke rerata (kelompok dipilih
  karena skor awal rendah).
- Peta Wright tanpa arah skala yang jelas — tulis di sumbu mana ujung "lebih
  mampu" dan mana "lebih sulit".

## Resep

Peta Wright dengan dua panel bersumbu-y bersama:

```python
from vizkit import apply_style, wright_map, save_figure, check_overlaps
import matplotlib.pyplot as plt

apply_style()
fig, (ax_p, ax_i) = plt.subplots(
    1, 2, figsize=(85/25.4, 85/25.4*1.25), sharey=True,
    gridspec_kw={"width_ratios": [1, 1.15]}, constrained_layout=True)

st = wright_map(ax_p, ax_i,
                abilities=theta,              # estimasi kemampuan (logit)
                item_labels=kode_butir,
                difficulties=beta,            # kesulitan butir (logit)
                se=se_butir)
print(st)   # selisih rerata & kesenjangan terbesar -> pakai di caption
ax_p.set_title("Butir terkonsentrasi di bawah rerata kemampuan peserta")
check_overlaps(fig, "fig2")
save_figure(fig, "fig2_peta_wright")
```

Pra-pascates per peserta (bukan bar rerata):

```python
fig, ax = new_figure(width="single", height_ratio=1.1)
res = slope_plot(ax, kode_siswa, pretest, posttest,
                 tick_labels=("Pratest", "Pascates"), value_fmt="{:.0f}")
ax.set_ylabel("Skor pemahaman konsep")
ax.set_title(f"{res['turun']} dari {sum(res.values())} siswa menurun")  # judul diuji ke data
```

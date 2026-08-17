# Klinis dan Epidemiologi

Bidang ini punya bentuk figur yang **diwajibkan reporting guideline**. Reviewer
akan mencarinya, dan ketiadaannya sering jadi alasan revisi mayor. Sebelum
merancang, cek guideline yang berlaku: CONSORT (RCT), STROBE (observasional),
PRISMA (review sistematis), STARD (diagnostik), TRIPOD (model prediksi).

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Peserta melewati tahap studi | Diagram alir CONSORT/STROBE | Wajib, dengan angka di setiap kotak |
| Satu studi dalam sintesis | Forest plot | Ukuran kotak ∝ bobot; garis nol efek |
| Waktu sampai kejadian | Kurva Kaplan-Meier | **Wajib** tabel jumlah berisiko di bawah |
| Efek pada banyak subkelompok | Forest plot subkelompok + uji interaksi | Bukan p per subkelompok saja |
| Performa diagnostik | Kurva ROC + AUC (CI) | Untuk kelas timpang, tambahkan PR curve |
| Kalibrasi model prediksi | Kurva kalibrasi + histogram | Diskriminasi saja tidak cukup |
| Kejadian per waktu (wabah) | Kurva epidemi (epicurve) | Batang per interval, bukan garis halus |
| Karakteristik dasar dua kelompok | Love plot / SMD | Bukan tabel p-value keseimbangan |
| Lintasan biomarker per pasien | Spaghetti + rerata model | Bukan bar rerata per kunjungan |
| Respons per pasien | Waterfall / swimmer plot | Standar onkologi |
| Efek samping | Volcano/dot plot per organ | Bukan tabel panjang |

## Aturan wajib domain ini

**Kaplan-Meier tanpa tabel jumlah berisiko tidak lengkap.** Ekor kurva bisa
ditopang tiga pasien; pembaca harus bisa melihatnya. Tambahkan juga tanda
sensor. Sebutkan uji log-rank dan HR (CI 95%) di dalam panel.

**Forest plot: sumbu rasio berskala log.** Rasio (OR, RR, HR) simetris pada
skala log — 0,5 dan 2,0 harus berjarak sama dari 1,0. Garis nol efek digambar
(1,0 untuk rasio, 0 untuk beda rerata). Ukuran kotak sebanding bobot studi,
diamond untuk ringkasan, dan laporkan heterogenitas (I², τ², p).

**Klaim kausal tidak boleh masuk judul figur observasional.** "Berhubungan
dengan", bukan "menurunkan risiko". Judul figur adalah tempat overclaiming
paling sering lolos karena tidak ikut disunting saat polishing prosa.

**CI, bukan p sendirian.** Figur yang hanya menampilkan bintang signifikansi
menyembunyikan besaran efek. Tampilkan estimasi titik + CI 95%.

**Kelas timpang: ROC menyesatkan.** Pada prevalensi rendah, AUC bisa tinggi
sementara PPV buruk. Sertakan precision-recall dan sebutkan prevalensinya.

**Model prediksi: diskriminasi + kalibrasi.** Kurva kalibrasi dengan garis
identitas, dan nyatakan apakah internal, internal-eksternal, atau eksternal
validation.

**Denominator selalu terlihat.** Persentase tanpa n adalah cacat. Untuk figur
sebaran kelompok kecil, gambar titik individual — 4 dari 5 pasien tidak boleh
tampil sebagai "80%" tanpa konteks.

## Jebakan yang sering lolos

- KM dengan sumbu-y dipotong 0,7–1,0 untuk membuat perbedaan terlihat besar;
  bila dilakukan, potongan harus terlihat jelas dan dinyatakan.
- Analisis subkelompok dengan p per subkelompok tanpa uji interaksi — figur ini
  hampir selalu memancing kritik reviewer.
- Epicurve dengan lebar bin yang dipilih agar puncaknya terlihat rapi. Nyatakan
  lebar bin dan tanggal potong data.
- Waterfall plot tanpa garis ambang respons (mis. −30% RECIST).
- Bar rerata biomarker per kunjungan yang menyembunyikan drop-out; pasien yang
  keluar studi membuat rerata naik seolah membaik.

## Resep

```python
from vizkit import apply_style, new_figure, forest_plot, save_figure

apply_style()
fig, ax = new_figure(width="single", height_ratio=1.0)
forest_plot(ax,
            labels=[s["nama"] for s in studi],
            est=[s["or"] for s in studi],
            lo=[s["lo"] for s in studi],
            hi=[s["hi"] for s in studi],
            weights=[s["w"] for s in studi],
            summary=(or_pool, lo_pool, hi_pool),
            log_scale=True, null_value=1.0,
            xlabel="Odds ratio (CI 95%)")
ax.set_title("Intervensi berhubungan dengan penurunan odds pada 8 dari 10 studi")
ax.text(0.98, -0.14, f"I² = {i2:.0f}%, τ² = {tau2:.3f}, p = {p_het:.3f}",
        transform=ax.transAxes, ha="right", fontsize=6)
save_figure(fig, "fig2_forest")
```

Kaplan-Meier dengan tabel berisiko: gunakan `lifelines`
(`manage_packages(environment="vizkit", packages=["lifelines"], use_pip=True)`),
`KaplanMeierFitter.plot_survival_function(ax=ax, show_censors=True)` lalu
`lifelines.plotting.add_at_risk_counts(kmf_a, kmf_b, ax=ax)`.

# Figur Multi-Panel: Dari Klaim ke Panel

Satu panel dinilai dari kebenarannya sendiri; figur multi-panel dinilai dari
apakah **susunannya** membuat satu kalimat menjadi benar. Dua hal berbeda, dan
yang kedua punya kegagalan khasnya sendiri: panel yang benar semua tapi
figurnya tidak menyatakan apa pun.

Baca file ini bila figurnya lebih dari satu panel. Untuk figur panel tunggal,
`aturan-figur.md` sudah cukup.

## 1. Klaim dulu, panel kemudian

Tulis **satu kalimat** yang harus dibuat benar oleh figur ini bagi pembaca yang
tidak membaca apa pun selain figur itu. Bukan judul, bukan topik — kalimat yang
bisa salah.

- Buruk: "Hasil eksperimen dekoding" (topik, tidak bisa salah)
- Buruk: "Model kami bagus" (tidak terukur)
- Baik: "Fitur konektivitas frontal memikul sebagian besar akurasi dekoding,
  dan keunggulannya bertahan lintas subjek."

Kalimat itu menentukan panel mana yang ada. Panel yang tidak menyatakan,
mendukung, atau membatasi kalimat itu **pindah ke suplemen** — bukan diperkecil.

## 2. Kerangka panel

Susun kerangkanya sebelum menggambar apa pun. Setiap panel dapat: huruf, peran,
posisi grid, dan **satu kalimat pesan** yang harus disampaikannya.

| Huruf | Peran | Isi |
|---|---|---|
| a | kail (hook) | Skema/hero selebar figur. Mengasumsikan pembaca tanpa konteks: apa yang diukur, dengan apa, terhadap apa. Memakai kata dan glif yang sama dengan label panel data. |
| b | pemikul klaim | Grafik yang **sendirian** membuat kalimat klaim benar. Kalau pembaca hanya melihat b, klaimnya sudah tersampaikan. |
| c, d, … | bukti | Diurutkan menurut seberapa kuat ia menopang b: robustness, ablasi, generalisasi, batas keberlakuan. |

Aturan tambahan:

- **Satu baris per sub-klaim.** Baris adalah unit naratif, bukan unit ruang.
- **5-10 panel** untuk figur naskah utama. Lebih dari itu, pecah jadi dua figur.
- **Grid 12 kolom** memberi keleluasaan colspan (½ = 6, ⅓ = 4, ¼ = 3, 7/12 = 7)
  tanpa mengubah lebar figur.
- **Tinggi baris ditentukan, bukan ditebak.** Baris skema lebih pendek daripada
  baris data; baris dengan label sumbu panjang butuh lebih tinggi. `panel_grid`
  mewajibkan `row_heights_mm` justru karena ini keputusan desain.

```python
from vizkit import apply_style, panel_grid, check_layout, panel_crops, save_figure

apply_style()
specs = [
    {"letter": "a", "row": 0, "col": 0, "colspan": 12},               # kail
    {"letter": "b", "row": 1, "col": 0, "colspan": 7},                # pemikul klaim
    {"letter": "c", "row": 1, "col": 7, "colspan": 5},                # bukti
    {"letter": "d", "row": 2, "col": 0, "colspan": 6},
    {"letter": "e", "row": 2, "col": 6, "colspan": 6},
]
fig, ax = panel_grid(specs, width="double", row_heights_mm=[32, 60, 56])
# ... gambar ke ax["a"], ax["b"], ...
```

`panel_grid` menolak kerangka yang tidak konsisten: baris di luar
`row_heights_mm`, `col+colspan` melewati grid, huruf panel duplikat, dan
`row_heights_mm` yang tidak diberikan. Huruf panel dibubuhkan otomatis.

Panel dengan proyeksi khusus: `{"letter": "b", ..., "projection": "3d"}`.

## 3. Verifikasi berlapis — geometris, tata letak, perseptual

Tiga pemeriksaan berbeda menangkap tiga jenis cacat berbeda. Jalankan
ketiganya, dalam urutan ini:

```python
check_layout(fig, "fig2")      # 1. tata letak: axes menciut? (galat, bukan warning)
check_overlaps(fig, "fig2")    # 2. geometris: teks bertumpang, menabrak spine
paths = save_figure(fig, "fig2_hasil_utama")
for huruf, box in panel_crops(fig).items():
    host.view_image(paths[-1], crop=box)      # 3. perseptual: LIHAT tiap panel
```

**Mengapa `check_layout` terpisah.** Bila tinggi baris tidak cukup untuk label
dan judul panelnya, matplotlib menciutkan axes ke nol dan hanya memberi
`UserWarning` — mudah terlewat, padahal figurnya rusak. `check_layout` mengubah
itu jadi galat yang menyebut baris tersempit. Panggil **setelah** semua panel
digambar: sebelum diisi, panel kosong selalu "muat".

**Mengapa potong-dan-lihat wajib.** Cek geometris tidak menangkap label
berkontras rendah, garis penunjuk yang menyilang tiga garis lain, atau dua
warna seri yang tertukar. Untuk setiap potongan, tanyakan:

- Setiap tanda dan glif terbaca terhadap latarnya?
- Elemen terkecil punya goresan/stub, atau hilang saat diperkecil?
- Ada garis penunjuk yang menyilang?
- Ada warna seri yang bisa dikira warna seri lain?
- Legenda duduk di sebelah hal yang dijelaskannya?
- Huruf panel menabrak isi panel atau label sumbu?

## 4. Pemeriksaan lintas panel

Ini yang tidak terlihat saat memeriksa panel satu per satu:

**4.1 Pengikatan warna lintas panel.** Satu entitas = satu warna di **seluruh**
panel. Bila "metode kami" biru di panel b, ia biru juga di panel d dan di baris
heatmap panel e. Warna adalah rujukan silang; pembaca tidak boleh perlu melihat
legenda dua kali.

**4.2 Satu angka satu klaim.** Akurasi yang dikutip di judul panel b, di caption,
dan di abstrak harus nilai yang sama, dari berkas yang sama.

**4.3 Kosakata seragam.** Kata yang dipakai di skema panel a adalah kata yang
sama di label sumbu panel b. "Fitur konektivitas" di a tidak boleh menjadi
"conn_feat" di b.

**4.4 Sumbu bersama diberi label sekali.** Sederet panel yang berbagi sumbu-y
menampilkan label tick di panel paling kiri saja; panel dalam tetap punya tick
tanpa label.

**4.5 Arah "lebih baik" sekali per baris,** bukan per panel.

**4.6 Isi kotaknya (aturan 3.5).** Selubung data tiap panel menempati ≥75%
persegi panjangnya. Bila aspek alami panel menyisakan pita kosong, **ubah
gridnya** (rowspan, panel komplementer bertumpuk) — jangan memberi padding.
Panel skema adalah pengecualian yang sah, tapi tetap harus terisi teks/glif,
bukan kosong.

## 5. Putaran revisi

Setelah figur lolos ketiga pemeriksaan, baca ulang sebagai **penelaah yang
bermusuhan**: cari cacat, bukan konfirmasi. Yang paling sering ditemukan:

- Judul panel yang mengklaim lebih dari yang ditunjukkan datanya (aturan 1.4).
  Uji setiap judul terhadap **setiap** kategori di sumbunya, dengan assertion
  bila memungkinkan — bukan dengan membaca sekilas.
- Label yang redundan bagi pembaca yang punya konteks bidang → hapus.
- Panel yang tidak menopang kalimat klaim → pindah ke suplemen.

Dua aturan untuk putaran berikutnya:

**Jangan mendekor ulang panel yang sudah lolos.** Menambah tanda atau label
pada panel yang sudah benar adalah regresi, bukan perbaikan.

**Berhenti saat temuan menjadi pengecualian yang dicari-cari.** Bila putaran
terakhir hanya menghasilkan keberatan yang butuh pembenaran panjang, figurnya
sudah selesai. Terus mencari temuan sampai dapat adalah gejala pelabelan
berlebih, bukan ketelitian.

## 6. Bila figur ini bagian dari satu naskah

Urutan figur punya busurnya sendiri (aturan 7.5): Figur 1 mewujudkan pitch satu
kalimat naskah sebagai data — cakupan, bukan arsitektur perangkat lunak.
Berikutnya: mekanisme → bukti → robustness → aplikasi. Satu panel dinilai
terhadap pitch naskah, bukan hanya terhadap klaim figurnya sendiri; isi boleh
berpindah antar figur bila di situ tempat ceritanya.

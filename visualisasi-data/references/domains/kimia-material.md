# Kimia dan Material

Substrat bidang ini adalah **sumbu spektral**, **diagram fase/komposisi**, dan
**struktur**. Konvensi sumbu di sini bukan selera — membalik arah sumbu
wavenumber atau ppm membuat spektrum tidak terbaca oleh pembaca bidang.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Intensitas per bilangan gelombang | Spektrum FTIR/Raman, x menurun | Offset vertikal untuk beberapa sampel |
| Intensitas per 2θ | Difraktogram XRD + posisi puncak rujukan | Tanda referensi dari basis data |
| Pergeseran kimia NMR | Spektrum, ppm menurun | Integrasi dicantumkan |
| Absorbansi vs panjang gelombang | Spektrum UV-Vis | Sebutkan pelarut dan konsentrasi |
| Massa vs suhu | Kurva TGA + turunan (DTG) | Dua sumbu wajar di sini, beri label jelas |
| Arus vs potensial | Voltammogram siklik | Arah pindai dengan panah, laju pindai |
| Komposisi tiga komponen | Diagram ternary | Bukan tiga bar terpisah |
| Fase vs suhu/komposisi | Diagram fase berlabel wilayah | Wilayah dinamai, bukan hanya garis |
| Struktur molekul/kristal | Gambar struktur / sel satuan | Dari file struktur, bukan gambar tangan |
| Distribusi ukuran partikel | Histogram + n partikel terukur | Rerata ± SD dan n wajib |
| Sifat vs komposisi (paduan) | Scatter + tren + pita error | Bukan bar per komposisi |
| Kinetika reaksi | Konsentrasi vs waktu + kurva model | Residual di panel bawah |
| Citra mikroskop (SEM/TEM) | Panel citra + skala bar terbakar | Skala bar wajib, di dalam citra |

## Aturan wajib domain ini

**Arah sumbu mengikuti konvensi.** FTIR/Raman: bilangan gelombang menurun ke
kanan. NMR: ppm menurun ke kanan. Melanggarnya membuat pembaca bidang harus
membaca ulang dari awal.

**Skala bar pada citra mikroskop ditempatkan di dalam citra**, bukan hanya
disebut di caption, dan tetap benar setelah citra dipotong atau diperkecil.
Sebutkan tegangan akselerasi/mode perbesaran.

**Spektrum bertumpuk memakai offset yang dinyatakan** ("offset 0,2 a.u.") dan
sumbu intensitas ditandai sebagai arbitrary units bila memang demikian.

**Puncak yang diklaim harus ditandai** dengan penugasan (assignment) di panel
atau tabel pendamping. Spektrum tanpa penugasan tidak mendukung klaim apa pun.

**XRD: tampilkan pola rujukan** (stick pattern dari ICDD/COD) di bawah data,
sehingga identifikasi fase dapat diperiksa pembaca.

**Ulangan sintesis dilaporkan.** Satu batch bukan bukti reprodusibilitas.
Nyatakan berapa batch/spesimen dan gambarkan sebarannya.

**Struktur digambar dari file struktur** (CIF, PDB, MOL) memakai perkakas yang
sesuai, bukan digambar ulang manual. Sebutkan sumber dan kode identifikasinya.

## Jebakan yang sering lolos

- Spektrum yang dinormalisasi tanpa disebut, lalu diklaim "intensitas meningkat".
- Puncak XRD yang bergeser karena kesalahan tinggi sampel diinterpretasi sebagai
  perubahan parameter kisi tanpa standar internal.
- Sumbu-y ganda TGA/DSC yang keduanya tidak diberi warna yang mengikat ke
  kurvanya.
- Histogram ukuran partikel dari 30 partikel dilaporkan dengan tiga angka
  penting.
- Citra SEM yang tingkat kecerahannya berbeda antar panel yang dibandingkan.
- Diagram fase yang menyalin dari literatur tanpa atribusi dan tanpa menandai
  bagian mana yang hasil studi ini.

## Resep

Spektrum bertumpuk dengan penugasan puncak:

```python
from vizkit import apply_style, new_figure, ramp, save_figure

apply_style()
fig, ax = new_figure(width="single", height_ratio=1.1)

warna = ramp("#1f6feb", len(sampel))
for i, (nama, spek) in enumerate(sampel.items()):
    ax.plot(wn, spek / spek.max() + i * 0.35, lw=0.9, c=warna[i])
    ax.text(wn.min() + 20, i * 0.35 + 0.05, nama, fontsize=6, c=warna[i])

for pos, tugas in penugasan.items():          # {1650: "amida I (C=O)"}
    ax.axvline(pos, ls=":", lw=0.5, c="0.6", zorder=0)
    ax.text(pos, ax.get_ylim()[1], tugas, rotation=90, va="top", ha="right", fontsize=5.5)

ax.set_xlim(wn.max(), wn.min())               # konvensi: menurun ke kanan
ax.set_xlabel("Bilangan gelombang (cm$^{-1}$)")
ax.set_ylabel("Absorbansi ternormalisasi (offset 0,35 a.u.)")
ax.set_title("Pita amida I menguat seiring naiknya kandungan pengisi")
save_figure(fig, "fig2_ftir")
```

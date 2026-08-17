# Kualitatif — wawancara, etnografi, studi kasus, analisis tematik

Riset kualitatif sering tidak divisualisasikan sama sekali, atau justru
divisualisasikan dengan cara yang mengkhianati epistemologinya: word cloud dan
bar frekuensi kode mengubah makna menjadi hitungan. Visualisasi yang benar di
sini menampilkan **struktur, proses, dan hubungan**, bukan frekuensi.

## Bentuk kanonik

| Yang ingin ditunjukkan | Bentuk | Catatan |
|---|---|---|
| Hierarki kode → subtema → tema | Diagram pohon / treemap berlabel | Bukan daftar bertingkat di prosa |
| Kutipan sebagai bukti tema | Tabel bukti (tema × kutipan × partisipan) | Bentuk figur paling kuat di bidang ini |
| Hubungan antar tema | Peta konsep / network berarah | Panah diberi label relasinya |
| Urutan kejadian per kasus | Timeline / event-sequence per partisipan | Menampilkan variasi lintasan |
| Kehadiran tema per partisipan | Matriks tema × partisipan (terisi/kosong) | Jujur soal siapa mengatakan apa |
| Proses / model yang dibangun | Diagram model grounded theory | Kondisi → aksi → konsekuensi |
| Tahap pengumpulan & saturasi | Kurva saturasi (kode baru per wawancara) | Bukti empiris klaim saturasi |
| Perbandingan lintas kasus | Tabel matriks lintas-kasus (Miles & Huberman) | Kasus di baris, dimensi di kolom |
| Posisi peneliti / audit trail | Diagram alur keputusan analitik | Mendukung dependability |
| Konteks lapangan | Denah/peta situs, foto berlabel | Anonimisasi wajib |

## Aturan wajib domain ini

**Jangan mengubah makna jadi frekuensi.** "Tema X muncul 47 kali" hampir tidak
pernah temuan; bahwa tema X muncul pada 11 dari 12 partisipan **termasuk yang
menolak intervensi** adalah temuan. Bila menampilkan hitungan, gambarkan sebagai
kehadiran per partisipan, bukan total kemunculan.

**Word cloud dilarang.** Ukuran kata mengkodekan frekuensi mentah, mengabaikan
konteks dan negasi, dan tata letaknya acak sehingga posisi tidak bermakna. Tidak
ada pertanyaan penelitian kualitatif yang dijawabnya.

**Matriks tema × partisipan harus jujur soal ketidakhadiran.** Sel kosong
berarti tema itu tidak muncul pada partisipan tersebut — bukan berarti tidak
ditanyakan. Bedakan keduanya dengan simbol berbeda.

**Kutipan diberi atribusi kode partisipan yang konsisten** (P03, bukan "seorang
guru"), dan konteks minimal (peran, lama pengalaman) yang tidak
mengidentifikasi. Semua nama, institusi, dan lokasi yang bisa
mengidentifikasi dihapus dari figur — termasuk dari tangkapan layar perangkat
lunak analisis.

**Diagram model menyebut sumber setiap kotak.** Kotak yang berasal dari data
dibedakan dari kotak yang berasal dari teori yang dipinjam.

**Jangan meminjam presisi kuantitatif.** Persentase pada n = 12 ("58% partisipan")
memberi kesan generalisasi yang tidak diklaim desainnya. Tulis "7 dari 12".

## Jebakan yang sering lolos

- Tangkapan layar NVivo/Atlas.ti mentah sebagai figur — tidak terbaca setelah
  diperkecil dan sering membocorkan nama file berisi identitas.
- Network kode otomatis dengan 80 simpul yang tidak bisa dibaca dan tidak
  dijelaskan aturan penariknya.
- Diagram model yang panahnya tidak berlabel, sehingga hubungannya bisa dibaca
  sebagai apa saja.
- Tabel bukti yang kutipannya dipotong sehingga kehilangan hedging asli
  partisipan.

## Resep

Matriks tema × partisipan (matplotlib murni):

```python
from vizkit import apply_style, new_figure, save_figure
import numpy as np

apply_style()
fig, ax = new_figure(width="double", height_ratio=0.5)

# status: 2 = muncul kuat, 1 = disinggung, 0 = tidak muncul, -1 = tidak ditanyakan
for i, tema in enumerate(tema_list):
    for j, p in enumerate(partisipan):
        s = status[i, j]
        if s == -1:
            ax.text(j, i, "–", ha="center", va="center", color="0.6", fontsize=6)
        elif s > 0:
            ax.scatter(j, i, s=60 if s == 2 else 22, c="#1f6feb",
                       edgecolor="white", lw=0.4, zorder=3)
ax.set_xticks(range(len(partisipan))); ax.set_xticklabels(partisipan, fontsize=6)
ax.set_yticks(range(len(tema_list))); ax.set_yticklabels(tema_list)
ax.set_xlabel("Partisipan"); ax.invert_yaxis()
ax.set_title("Kekhawatiran privasi muncul pada 11 dari 12 partisipan, lintas peran")
ax.text(1.0, -0.16, "Besar = tema dominan · kecil = disinggung · – = tidak ditanyakan",
        transform=ax.transAxes, ha="right", fontsize=6, color="0.35")
save_figure(fig, "fig1_matriks_tema")
```

Kurva saturasi: sumbu-x urutan wawancara, sumbu-y jumlah kode baru kumulatif dan
kode baru per wawancara — dataran yang mendatar adalah bukti saturasi yang bisa
dilihat reviewer, bukan sekadar diklaim.

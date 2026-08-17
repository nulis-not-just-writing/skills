# Omics — genomik, transkriptomik, proteomik, mikrobiom, filogeni

Substrat bidang ini: **koordinat genom**, **ruang embedding sel**, **pohon**,
dan **matriks fitur × sampel**. Skala datanya besar, sehingga aturan utamanya
adalah memilih apa yang **tidak** digambar.

## Bentuk kanonik

| Unit observasi | Bentuk | Catatan |
|---|---|---|
| Varian pada posisi genom | Manhattan plot | Sumbu = koordinat, bukan indeks |
| Kualitas uji asosiasi | QQ plot + λ_GC | Wajib mendampingi Manhattan |
| Gen dengan efek + signifikansi | Volcano plot | Ambang FC dan FDR digambar, gen kunci dilabeli |
| Ekspresi gen × sampel | Heatmap z-score per baris | Dendrogram bila clustering itu hasilnya |
| Sel individual | UMAP/t-SNE + label klaster | Tanpa tick; klaster dilabeli langsung |
| Ekspresi gen penanda per klaster | Dot plot (ukuran = % sel, warna = rerata) | Bukan heatmap datar |
| Komposisi taksonomi per sampel | Stacked bar relatif + urutan bermakna | Batasi ke top-k + "lainnya" |
| Jarak antar komunitas | Ordinasi PCoA/NMDS + elips | Sertakan PERMANOVA R² dan p |
| Kekayaan/keragaman alfa | Box + titik per sampel | Sebutkan kedalaman rarefaksi |
| Hubungan evolusioner | Pohon filogeni + nilai dukungan | Bootstrap/posterior di simpul |
| Enrichment jalur | Dot plot terurut (GeneRatio × p.adj) | Bukan bar p-value |
| Segmen kromosom / sintenik | Ideogram / plot melingkar | Untuk perbandingan genom |

## Aturan wajib domain ini

**Manhattan plot memakai koordinat fisik**, bukan indeks SNP berurutan; jarak
antar-titik membawa makna LD. Garis ambang genome-wide (5×10⁻⁸) digambar dan
dinyatakan. Sertakan QQ plot dengan λ_GC — Manhattan tanpa QQ mengundang
pertanyaan stratifikasi populasi.

**Volcano: kedua ambang digambar**, dan yang dilabeli hanya gen yang benar-benar
dibahas di teks. Melabeli 60 gen membuat panel tidak terbaca dan tidak menambah
informasi.

**Heatmap ekspresi: nyatakan transformasinya.** z-score per baris, log2 CPM,
atau nilai mentah menghasilkan gambar yang sangat berbeda. Bila z-score,
colormap divergen berpusat 0. Bila dendrogramnya bukan hasil, jangan digambar.

**UMAP bukan bukti.** Jarak antar klaster di UMAP tidak dapat diinterpretasi
secara kuantitatif. Jangan menulis judul yang mengklaim "kelompok A lebih dekat
ke B". Sebutkan parameter (`n_neighbors`, `min_dist`) di caption.

**Komposisi mikrobiom: relatif atau absolut, katakan yang mana**, dan sebutkan
kedalaman sekuensing serta apakah dirarefaksi. Urutkan sampel menurut variabel
yang bermakna (kelompok, waktu), jangan menurut abjad ID sampel.

**Pohon filogeni tanpa nilai dukungan tidak dapat dinilai.** Cantumkan bootstrap
atau posterior probability, sebutkan modelnya, dan gambar skala substitusi.
Outgroup dinyatakan.

**Enrichment: laporkan p yang sudah dikoreksi dan latar (background) gene set.**
Enrichment tanpa background eksplisit tidak dapat direproduksi.

## Jebakan yang sering lolos

- Heatmap dengan clustering baris tapi tanpa menyebut metrik jarak dan metode
  linkage — hasilnya berubah drastis antar pilihan.
- Volcano dengan sumbu-x fold change linear (harus log2, agar naik dan turun
  simetris).
- Dot plot enrichment yang diurutkan menurut p, sehingga jalur redundant
  (parent-child GO term) memenuhi panel. Ringkas dulu dengan REVIGO atau
  serupa.
- Sumbu UMAP dengan tick dan label numerik — tidak bermakna, hapus.
- Colormap pelangi pada heatmap.

## Resep

```python
from vizkit import apply_style, new_figure, save_figure
import numpy as np

apply_style()
fig, ax = new_figure(width="single")

sig = (df.padj < 0.05) & (df.log2fc.abs() > 1)
ax.scatter(df.log2fc[~sig], -np.log10(df.padj[~sig]), s=3, c="0.75", lw=0)
ax.scatter(df.log2fc[sig], -np.log10(df.padj[sig]), s=6, c="#1f6feb", lw=0)
ax.axhline(-np.log10(0.05), ls="--", lw=0.6, c="0.4")
ax.axvline(-1, ls="--", lw=0.6, c="0.4"); ax.axvline(1, ls="--", lw=0.6, c="0.4")
for g in gen_dibahas:                      # hanya gen yang muncul di teks
    r = df.loc[g]
    ax.annotate(g, (r.log2fc, -np.log10(r.padj)), fontsize=6,
                xytext=(3, 3), textcoords="offset points", style="italic")
ax.set_xlabel("log$_2$ fold change"); ax.set_ylabel("−log$_{10}$ FDR")
ax.set_title("42 gen naik dan 17 turun pada kondisi perlakuan")
save_figure(fig, "fig3_volcano")
```

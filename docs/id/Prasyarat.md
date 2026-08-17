# Prasyarat & lingkungan

*[Read this in English](../Requirements.md)*

**Untuk lima skill teks, tidak ada yang wajib.** Kelimanya berfungsi tanpa satu pun perkakas di
bawah — yang berkurang adalah kecepatan dan keterlacakan, bukan kewajibannya. Skill diminta
mengatakan apa yang dilewati, bukan diam-diam melewatinya.

`visualisasi-data` pengecualiannya, dan itu dinyatakan terang-terangan di barisnya sendiri: skill
yang menggambar tidak bisa menggambar tanpa pustaka penggambar.

| Perkakas | Untuk apa | Bila tidak ada |
|---|---|---|
| **Python 3** | sapuan mekanis, gerbang fidelitas, audit PRISMA | dikerjakan manual, cakupan berkurang |
| **pandoc** | membaca naskah `.docx` | ekspor naskah ke `.md` atau `.tex` |
| **MCP `scholar` / `zotero`** | verifikasi sitasi + deteksi retraksi | jatuh ke `WebSearch`/`WebFetch`, lalu ke penandaan manual |
| **R + paket `robvis`** | figur *traffic-light* risk of bias | aplikasi web robvis (tanpa R), atau tabel studi × domain |
| **`matplotlib` + `numpy`** | menggambar figur di `visualisasi-data` | **skill itu tidak bisa merender** — panduan rancangannya tetap berlaku penuh |

## Python

Seluruh skrip di lima skill teks **stdlib-only** — tidak ada `pip install`, tidak ada virtualenv.
Diuji jalan pada Python 3.9.6 bawaan macOS maupun 3.12.

```bash
python3 -V     # cek
```

Belum ada? macOS: `xcode-select --install`. Windows: `winget install Python.Python.3.12`.

### ⚠ Sertifikat CA di macOS

Python dari python.org **tidak membawa sertifikat CA**. Akibatnya `verify_refs.py` melaporkan
**semua** rujukan sebagai `UNVERIFIED` — termasuk yang benar-benar ada.

Itu kegagalan jaringan, **bukan temuan naskah**. Bila seluruh rujukan tiba-tiba `UNVERIFIED`
serentak, curigai sertifikat lebih dulu:

```bash
python3 -c "import ssl,os; p=ssl.get_default_verify_paths().openssl_cafile; print(p, os.path.exists(p))"
"/Applications/Python 3.12/Install Certificates.command"   # sesuaikan nomor versinya
```

Tiap versi Python punya direktori sertifikat sendiri — memasang versi baru mengulang masalahnya.

## pandoc

Hanya memengaruhi masukan `.docx`. Untuk `.tex` dan `.md`, semua skrip jalan penuh.

```bash
brew install pandoc          # macOS
winget install JohnMacFarlane.Pandoc
```

## MCP untuk verifikasi sitasi

Tanpa MCP, verifikasi tetap berjalan lewat `WebSearch`/`WebFetch` — resolusikan DOI di `doi.org`,
cocokkan judul, penulis pertama, tahun, dan nama jurnal. Yang tidak bisa dilakukan tanpa MCP:
**deteksi retraksi otomatis**.

Aturan yang berlaku di ketiga tingkat: **sitasi tidak pernah dianggap benar karena "terlihat masuk
akal"**. Kombinasi penulis-tahun-jurnal yang tampak wajar justru pola khas sitasi karangan.

## matplotlib + numpy (khusus `visualisasi-data`)

Satu-satunya tempat di repo ini yang benar-benar menuntut `pip install`:

```bash
pip install matplotlib numpy
```

Semua yang digambar skill ini **matplotlib murni** — tanpa seaborn, tanpa plotly, tanpa R. Khususnya
`topomap` **tidak** membutuhkan MNE: koordinat elektroda 10-20 sudah dibakukan di dalam modul. Set
`prefer_mne=True` hanya bila Anda ingin membacanya langsung dari MNE.

Empat paket bersifat opsional dan masing-masing memperdalam tepat satu hal:

| Opsional | Memperdalam | Bila tidak ada |
|---|---|---|
| `scipy` | interpolasi topomap, KDE ridgeline | interpolasi lebih kasar, histogram menggantikan KDE |
| `pillow` | pemeriksaan raster di `figcheck.py` | cek dimensi dan dpi PNG dilewati |
| `pypdf` | pemeriksaan penyematan font PDF di `figcheck.py` | cek font tersemat dilewati |
| `mne` | membaca montase langsung dari MNE | koordinat 10-20 bawaan modul yang dipakai |

**Tanpa matplotlib skill ini tidak mundur ke grafik yang lebih buruk — ia berhenti merender dan
mengatakannya.** Paruh yang memilih bentuk visual berupa prosa dan tetap bekerja: Anda tetap
mendapat Uji Rujukan, rute domain, aturan figur, dan caption. Menggambarnya saja yang Anda kerjakan
sendiri.

## R + robvis (khusus `slr-cowork`)

Hanya untuk figur risk of bias. **Ada aplikasi web-nya**, jadi R sama sekali tidak wajib.

```r
install.packages("robvis")
```

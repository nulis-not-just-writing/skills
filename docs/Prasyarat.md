# Prasyarat & lingkungan

**Tidak ada yang wajib.** Kelima skill berfungsi tanpa satu pun perkakas di bawah — yang berkurang
adalah kecepatan dan keterlacakan, bukan kewajibannya. Skill diminta mengatakan apa yang dilewati,
bukan diam-diam melewatinya.

| Perkakas | Untuk apa | Bila tidak ada |
|---|---|---|
| **Python 3** | sapuan mekanis, gerbang fidelitas, audit PRISMA | dikerjakan manual, cakupan berkurang |
| **pandoc** | membaca naskah `.docx` | ekspor naskah ke `.md` atau `.tex` |
| **MCP `scholar` / `zotero`** | verifikasi sitasi + deteksi retraksi | jatuh ke `WebSearch`/`WebFetch`, lalu ke penandaan manual |
| **R + paket `robvis`** | figur *traffic-light* risk of bias | aplikasi web robvis (tanpa R), atau tabel studi × domain |

## Python

Seluruh skrip **stdlib-only** — tidak ada `pip install`, tidak ada virtualenv. Diuji jalan pada
Python 3.9.6 bawaan macOS maupun 3.12.

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

## R + robvis (khusus `slr-cowork`)

Hanya untuk figur risk of bias. **Ada aplikasi web-nya**, jadi R sama sekali tidak wajib.

```r
install.packages("robvis")
```

# Pemasangan

*[Read this in English](../Installation.md)*

Dua cara, tergantung Anda memakai Claude yang mana.

## Claude Desktop — paling mudah, tanpa git

**Belum yakin punya Claude yang mana?** Kalau Anda memakai Claude lewat peramban atau aplikasi
desktop, bagian inilah yang Anda butuhkan. Kalau Anda mengetik `claude` di terminal, langsung ke
[Claude Code](#claude-code--salin-atau-symlink).

1. **Unduh** skill yang Anda mau. Tiap tautan langsung menyimpan berkasnya ke komputer Anda:

   | Skill | Untuk apa | Unduh |
   |---|---|---|
   | `nulis` | struktur artikel | [nulis-1.4.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/nulis-1.4.0.zip) |
   | `polish-manuscript` | prosa & mekanik | [polish-manuscript-1.4.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/polish-manuscript-1.4.0.zip) |
   | `submit` | gerbang pra-submisi | [submit-1.5.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/submit-1.5.0.zip) |
   | `revisi` | setelah keputusan editor | [revisi-1.3.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/revisi-1.3.0.zip) |
   | `slr-cowork` | tinjauan sistematis | [slr-cowork-1.5.0.zip](https://github.com/nulis-not-just-writing/skills/raw/main/dist/slr-cowork-1.5.0.zip) |

   **Jangan di-*unzip*.** Claude Desktop meminta berkas `.zip`-nya persis seperti yang diunduh.

2. Buka Claude Desktop → **Settings** → **Capabilities** → **Skills**
3. Klik **Upload**
4. Pilih berkas `.zip` yang barusan Anda unduh

Selesai. **Anda tidak perlu memanggil skill-nya** — ia aktif sendiri ketika Anda menyebut hal yang
relevan. Coba *"saya mau mulai menulis artikel dari data survei ini"*, dan `nulis` semestinya
menyala.

> Nama zip memuat versi. Kalau nanti ada pembaruan, nama berkasnya berbeda — jadi Anda selalu
> tahu versi mana yang terpasang.

## Claude Code — salin atau symlink

```bash
git clone https://github.com/nulis-not-just-writing/skills.git
cd skills
```

**Salin** (mudah, tapi tidak ikut pembaruan):

```bash
cp -R nulis polish-manuscript submit revisi slr-cowork ~/.claude/skills/
```

**Symlink** (ikut pembaruan setiap `git pull`):

```bash
for s in nulis polish-manuscript submit revisi slr-cowork; do
  ln -s "$PWD/$s" ~/.claude/skills/$s
done
```

Pasang yang Anda perlukan saja — kelimanya berdiri sendiri.

## Memastikan sudah terpasang

Di Claude Code:

```bash
ls -la ~/.claude/skills/
```

Lalu coba pancing dengan kalimat biasa, misalnya *"saya mau mulai menulis artikel dari data
survei ini"* — `nulis` semestinya aktif tanpa Anda menyebut namanya.

## Memperbarui

```bash
cd skills && git pull
```

Bila Anda memakai **symlink**, selesai di situ. Bila **menyalin**, ulangi perintah `cp -R`.
Untuk Claude Desktop, unduh zip versi baru dan unggah lagi.

## Mencopot

```bash
rm ~/.claude/skills/nulis          # symlink
rm -rf ~/.claude/skills/nulis      # hasil salin
```

Di Claude Desktop: **Settings → Capabilities → Skills**, lalu hapus dari daftar.

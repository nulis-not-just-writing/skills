# Pemasangan

*[Read this in English](../Installation.md)*

Dua cara, tergantung Anda memakai Claude yang mana.

## Claude Desktop — paling mudah, tanpa git

1. Buka [folder `dist/`](https://github.com/nulis-not-just-writing/skills/tree/main/dist) di repo
2. Unduh zip skill yang Anda mau (mis. `nulis-1.3.0.zip`)
3. Di Claude Desktop: **Settings → Capabilities → Skills → Upload**
4. Pilih zip-nya

Selesai. Skill akan aktif sendiri ketika Anda menyebut hal yang relevan — tidak perlu memanggil
namanya.

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

"""vizkit — perkakas figur untuk skill `visualisasi-data`.

Matplotlib murni. Tidak ada dependensi wajib selain numpy + matplotlib.
Fungsi yang memerlukan paket tambahan menyebutkannya di docstring dan gagal
dengan pesan yang jelas, bukan diam-diam mundur ke bentuk generik.

    import sys; sys.path.insert(0, "scripts")
    from vizkit import *
    apply_style()
    fig, ax = new_figure(width="single")
"""

from __future__ import annotations

import math
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, PathPatch, Polygon
from matplotlib.path import Path

__all__ = [
    "MM", "COL_SINGLE", "COL_DOUBLE", "INK", "MUTE", "RULE", "COMPARATOR", "ALARM",
    "apply_style", "new_figure", "save_figure",
    "palette", "focal_comparator", "ramp",
    "spread_lines", "mean_line", "points_with_mean", "sig_stars", "sig_bracket",
    "electrode_xy", "draw_head", "topomap", "montage_glyph", "ELECTRODES_1020",
    "tile_map", "ID_PROVINSI_TILES",
    "likert_diverging", "forest_plot", "dot_whisker", "confusion_matrix", "alluvial",
    "rose_plot", "slope_plot", "ridgeline", "bubble_matrix",
    "surface_pair", "parallel_coordinates", "scatter3d",
    "wright_map", "event_study", "waterfall", "lorenz_curve",
    "pls_path_diagram", "SMARTPLS_CONSTRUCT", "SMARTPLS_INDICATOR",
    "panel_letter", "panel_grid", "panel_crops", "check_layout",
    "check_overlaps", "cvd_check",
]

# ---------------------------------------------------------------- konstanta

MM = 1.0 / 25.4              # milimeter -> inci
COL_SINGLE = 85 * MM         # lebar satu kolom lazim (mm)
COL_DOUBLE = 180 * MM        # lebar dua kolom / full width

INK = "#1a1a1a"              # teks dan spine
MUTE = "#6b7280"             # anotasi sekunder
RULE = "#d4d4d8"             # garis bantu
COMPARATOR = "#9ca3af"       # pembanding / baseline: bobot visual rendah
ALARM = "#d1495b"            # HANYA untuk galat/anomali, bukan deret data

# Palet kategorikal aman-CVD (Okabe-Ito, tanpa hitam).
_OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7",
              "#56B4E9", "#D55E00", "#F0E442", "#000000"]


# ------------------------------------------------------------------- gaya

def apply_style(sizes=(8, 7, 6), family="DejaVu Sans", dpi=300):
    """Tetapkan rcParams: ladder font tiga tingkat, tick keluar, legenda polos.

    sizes = (dasar, anotasi/legenda, tick). Ini ladder peran, bukan selera:
    judul/label sumbu pada `dasar`, legenda/anotasi satu tingkat turun, tick
    satu tingkat lagi. Jangan menambah ukuran keempat.
    """
    base, ann, tick = sizes
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": dpi,
        "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
        "font.family": family, "font.size": base,
        "axes.titlesize": base, "axes.labelsize": base,
        "axes.titleweight": "normal", "axes.titlelocation": "left",
        "axes.titlepad": 5.0,
        "legend.fontsize": ann, "legend.frameon": False,
        "legend.handlelength": 1.4, "legend.labelspacing": 0.3,
        "xtick.labelsize": tick, "ytick.labelsize": tick,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 2.6, "ytick.major.size": 2.6,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.6, "axes.edgecolor": INK,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK,
        "lines.linewidth": 1.2, "lines.markersize": 3.5,
        "grid.color": RULE, "grid.linewidth": 0.5,
        "pdf.fonttype": 42, "ps.fonttype": 42,   # font tertanam, bukan kurva
        "figure.autolayout": False,
    })


def new_figure(width="single", height_ratio=0.75, nrows=1, ncols=1,
               width_mm=None, **kw):
    """Buat figure pada ukuran cetak SEBENARNYA.

    width: "single" (85 mm), "double" (180 mm), atau angka inci.
    width_mm: menimpa `width` dengan lebar milimeter eksplisit dari author
              guidelines jurnal target.

    Menggambar pada ukuran akhir adalah cara paling andal menjaga font >= 7 pt;
    menskala figur setelah render selalu merusak ladder font.
    """
    if width_mm is not None:
        w = width_mm * MM
    elif width == "single":
        w = COL_SINGLE
    elif width == "double":
        w = COL_DOUBLE
    else:
        w = float(width)
    fig, axes = plt.subplots(nrows, ncols, figsize=(w, w * height_ratio),
                             constrained_layout=True, **kw)
    return fig, axes


def save_figure(fig, stem, outdir="figures", formats=("pdf", "png"), dpi=300,
                warn_shrink=True):
    """Simpan vektor untuk naskah + raster untuk pratinjau. Kembalikan path."""
    import os
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for ext in formats:
        p = os.path.join(outdir, f"{stem}.{ext}")
        fig.savefig(p, dpi=dpi)
        paths.append(p)

    # bbox_inches="tight" memangkas ruang kosong, sehingga lebar FISIK berkas
    # bisa menyusut dari figsize yang dirancang — figur lalu diperbesar penerbit
    # dan ukuran font efektif ikut berubah. Penyusutan besar dilaporkan di sini,
    # bukan dibiarkan muncul sebagai "resolusi kurang" di figcheck.
    png = next((q for q in paths if q.endswith(".png")), None)
    if png and warn_shrink:
        try:
            from PIL import Image
            with Image.open(png) as im:
                w_in = im.size[0] / dpi
            drift = (fig.get_size_inches()[0] - w_in) / fig.get_size_inches()[0]
            if drift > 0.04:
                print(f"[save_figure] {stem}: lebar tersimpan {w_in*25.4:.0f} mm "
                      f"vs rancangan {fig.get_size_inches()[0]*25.4:.0f} mm "
                      f"({drift*100:.0f}% terpangkas ruang kosong). Panel tidak "
                      f"mengisi kotaknya (aturan 3.5), atau naikkan dpi agar "
                      f"resolusi pada lebar kolom tetap >= 300.")
        except Exception:                            # noqa: BLE001
            pass
    return paths


# ------------------------------------------------------------------ warna

def palette(n=None, names=None):
    """Palet kategorikal aman buta warna (Okabe-Ito).

    Beri `names` untuk mendapat dict {nama: warna} yang bisa dipakai ulang di
    seluruh figur naskah — inilah cara mengikat warna ke entitas (aturan 4.1).
    """
    if names is not None:
        return {k: _OKABE_ITO[i % len(_OKABE_ITO)] for i, k in enumerate(names)}
    n = n or len(_OKABE_ITO)
    return _OKABE_ITO[:n]


def focal_comparator(focal_color="#0072B2"):
    """Pasangan (fokal, pembanding): kontribusi sendiri pekat, pembanding abu."""
    return focal_color, COMPARATOR


def ramp(hue, n, lo=0.30, hi=0.95):
    """Ramp satu-hue terang->gelap untuk kategori ORDINAL (tingkat beban,
    dosis, tahun). Jangan pakai untuk kategori nominal."""
    base = np.array(mpl.colors.to_rgb(hue))
    white = np.ones(3)
    return [mpl.colors.to_hex(white + (base - white) * t)
            for t in np.linspace(lo, hi, n)]


# --------------------------------------------------- ketidakpastian & uji

def spread_lines(ax, x, mat, color, alpha=0.28, lw=0.5, **kw):
    """Gambar setiap ulangan (baris `mat`) sebagai garis tipis di belakang.

    mat: (n_ulangan, n_x). Ini lapis yang paling sering hilang dari figur.
    """
    mat = np.asarray(mat)
    if mat.ndim != 2:
        raise ValueError(f"mat harus 2D (n_ulangan, n_x), diterima {mat.shape}")
    for row in mat:
        ax.plot(x, row, color=color, alpha=alpha, lw=lw, zorder=1, **kw)
    return mat.shape[0]


def mean_line(ax, x, mat, color, label=None, lw=1.4, marker="o", **kw):
    """Rerata antar-ulangan di atas sebaran. Pasangan wajib `spread_lines`."""
    mat = np.asarray(mat)
    return ax.plot(x, mat.mean(0), color=color, lw=lw, marker=marker,
                   label=label, zorder=3, **kw)


def points_with_mean(ax, xpos, values, color, jitter=0.07, mean_width=0.28,
                     size=10, seed=0, **kw):
    """Titik individual + palang rerata pada satu slot kategori.

    Bentuk yang benar untuk n kecil (aturan 2.1) — menggantikan bar rerata.
    """
    v = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    xs = xpos + rng.uniform(-jitter, jitter, v.size)
    ax.scatter(xs, v, s=size, c=color, alpha=0.75, lw=0, zorder=2, **kw)
    m = float(np.mean(v))
    ax.plot([xpos - mean_width / 2, xpos + mean_width / 2], [m, m],
            color=color, lw=1.8, solid_capstyle="butt", zorder=3)
    return m, v.size


def sig_stars(p, thresholds=((1e-3, "***"), (1e-2, "**"), (5e-2, "*"))):
    """Bintang signifikansi; mengembalikan "n.s." bila tidak signifikan.

    "n.s." adalah hasil yang dilaporkan, bukan kekosongan (aturan 2.4).
    Berikan p yang SUDAH dikoreksi bila ada perbandingan ganda.
    """
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return "—"
    for thr, s in thresholds:
        if p < thr:
            return s
    return "n.s."


def sig_bracket(ax, x1, x2, y, text, tick=None, color=INK, fontsize=None):
    """Kurung pembanding dengan label di atasnya."""
    tick = tick if tick is not None else abs(y) * 0.02 + 1e-9
    ax.plot([x1, x1, x2, x2], [y - tick, y, y, y - tick],
            lw=0.7, c=color, clip_on=False)
    ax.text((x1 + x2) / 2, y, text, ha="center", va="bottom",
            fontsize=fontsize or mpl.rcParams["legend.fontsize"], color=color)


# ------------------------------------------------------- substrat: kepala

# Koordinat 2D elektroda, diturunkan dari montase `standard_1020` MNE:
# bola dikepaskan (least-squares) ke seluruh posisi elektroda, lalu diproyeksi
# azimuthal-equidistant (r sebanding sudut dari vertex), dinormalisasi sehingga
# radius TERBESAR cincin Fp1/Fp2/F7/F8/T7/T8/P7/P8/O1/O2 = 1.0, sehingga tidak
# ada elektroda 10-20 yang jatuh di luar outline kepala. Elektroda cincin
# inferior (T9/T10, P9/P10, Iz, M1/M2, A1/A2) memang berada di r > 1: itu benar
# secara anatomis, dan topomap memotongnya di batas kepala.
# Sumbu: +y = anterior (hidung), +x = kanan. JANGAN mengarang koordinat baru;
# tambahkan dari montase standar bila butuh kanal lain.
ELECTRODES_1020 = {
    "A1":     (-1.3257, -0.1262),
    "A2":     (+1.3315, -0.1297),
    "AF1":    (-0.1430, +0.7192),
    "AF10":   (+0.6361, +1.0317),
    "AF2":    (+0.1416, +0.7202),
    "AF3":    (-0.2761, +0.7501),
    "AF4":    (+0.2766, +0.7471),
    "AF5":    (-0.4075, +0.7906),
    "AF6":    (+0.4018, +0.7936),
    "AF7":    (-0.5395, +0.8279),
    "AF8":    (+0.5311, +0.8342),
    "AF9":    (-0.6339, +1.0305),
    "AFz":    (-0.0038, +0.7169),
    "C1":     (-0.2262, +0.0413),
    "C2":     (+0.2293, +0.0441),
    "C3":     (-0.4638, +0.0358),
    "C4":     (+0.4684, +0.0411),
    "C5":     (-0.7139, +0.0261),
    "C6":     (+0.7177, +0.0343),
    "CP1":    (-0.2132, -0.1798),
    "CP2":    (+0.2220, -0.1790),
    "CP3":    (-0.4349, -0.2048),
    "CP4":    (+0.4427, -0.2010),
    "CP5":    (-0.6703, -0.2488),
    "CP6":    (+0.6767, -0.2407),
    "CPz":    (-0.0020, -0.1737),
    "Cz":     (-0.0020, +0.0437),
    "F1":     (-0.1917, +0.5001),
    "F10":    (+0.9497, +0.7824),
    "F2":     (+0.1958, +0.5058),
    "F3":     (-0.3848, +0.5270),
    "F4":     (+0.3872, +0.5382),
    "F5":     (-0.5774, +0.5734),
    "F6":     (+0.5831, +0.5778),
    "F7":     (-0.7661, +0.6387),
    "F8":     (+0.7635, +0.6458),
    "F9":     (-0.9489, +0.7820),
    "FC1":    (-0.2215, +0.2720),
    "FC2":    (+0.2192, +0.2780),
    "FC3":    (-0.4481, +0.2901),
    "FC4":    (+0.4494, +0.2954),
    "FC5":    (-0.6876, +0.3120),
    "FC6":    (+0.6872, +0.3197),
    "FCz":    (-0.0022, +0.2684),
    "FT10":   (+1.1622, +0.4334),
    "FT7":    (-0.9338, +0.3533),
    "FT8":    (+0.9293, +0.3685),
    "FT9":    (-1.1595, +0.4278),
    "Fp1":    (-0.2776, +0.9256),
    "Fp2":    (+0.2664, +0.9293),
    "Fpz":    (-0.0056, +0.9359),
    "Fz":     (-0.0028, +0.4943),
    "Iz":     (-0.0077, -1.0610),
    "M1":     (-1.2539, -0.4082),
    "M2":     (+1.2564, -0.4178),
    "O1":     (-0.2621, -0.8319),
    "O10":    (+0.3124, -1.0507),
    "O2":     (+0.2543, -0.8340),
    "O9":     (-0.3264, -1.0451),
    "Oz":     (-0.0054, -0.8355),
    "P1":     (-0.1829, -0.3973),
    "P10":    (+0.9258, -0.7298),
    "P2":     (+0.1914, -0.3914),
    "P3":     (-0.3719, -0.4293),
    "P4":     (+0.3766, -0.4240),
    "P5":     (-0.5576, -0.4883),
    "P6":     (+0.5559, -0.4899),
    "P7":     (-0.7423, -0.5754),
    "P8":     (+0.7410, -0.5774),
    "P9":     (-0.9314, -0.7203),
    "PO1":    (-0.1427, -0.6156),
    "PO10":   (+0.6311, -0.9466),
    "PO2":    (+0.1388, -0.6170),
    "PO3":    (-0.2813, -0.6353),
    "PO4":    (+0.2748, -0.6415),
    "PO5":    (-0.4049, -0.6804),
    "PO6":    (+0.4037, -0.6804),
    "PO7":    (-0.5142, -0.7475),
    "PO8":    (+0.5098, -0.7508),
    "PO9":    (-0.6416, -0.9374),
    "POz":    (-0.0037, -0.6054),
    "Pz":     (-0.0025, -0.3862),
    "T10":    (+1.2398, +0.0053),
    "T7":     (-0.9870, +0.0082),
    "T8":     (+0.9881, +0.0200),
    "T9":     (-1.2346, +0.0128),
    "TP10":   (+1.1410, -0.4048),
    "TP7":    (-0.9172, -0.3140),
    "TP8":    (+0.9186, -0.3121),
    "TP9":    (-1.1419, -0.3939),
}

# Alias sistem lama 10-20 -> penamaan 10-10 modern.
_ALIAS = {"T3": "T7", "T4": "T8", "T5": "P7", "T6": "P8"}


def electrode_xy(names, prefer_mne=False, strict=True):
    """Koordinat 2D untuk daftar nama elektroda. -> (n, 2) array.

    Sumbernya tabel bawaan yang diturunkan dari montase standar_1020; set
    prefer_mne=True untuk membacanya langsung dari MNE bila terpasang.
    Nama yang tidak dikenal memicu KeyError (strict=True) — ini disengaja:
    salah ketik nama kanal yang diam-diam dilewati menghasilkan topografi yang
    salah tanpa peringatan.
    """
    names = [_ALIAS.get(n, n) for n in names]
    if prefer_mne:
        try:
            import mne
            mont = mne.channels.make_standard_montage("standard_1020")
            pos = mont.get_positions()["ch_pos"]
            P = np.array([pos[n] for n in pos if n not in ("T3", "T4", "T5", "T6")])
            A = np.c_[2 * P, np.ones(len(P))]
            sol, *_ = np.linalg.lstsq(A, (P ** 2).sum(1), rcond=None)
            c = sol[:3]
            out = []
            for n in names:
                q = pos[n] - c
                th = np.arccos(np.clip(q[2] / np.linalg.norm(q), -1, 1))
                ph = np.arctan2(q[1], q[0])
                r = (th / (np.pi / 2)) * 0.94941
                out.append((r * np.cos(ph), r * np.sin(ph)))
            return np.array(out)
        except Exception as e:                      # noqa: BLE001
            warnings.warn(f"MNE tidak terpakai ({e}); memakai tabel bawaan.")
    missing = [n for n in names if n not in ELECTRODES_1020]
    if missing and strict:
        raise KeyError(f"elektroda tidak dikenal: {missing}. Tambahkan dari "
                       f"montase standar, jangan diperkirakan.")
    return np.array([ELECTRODES_1020[n] for n in names if n in ELECTRODES_1020])


def draw_head(ax, radius=1.0, lw=1.0, color=INK, nose=True, ears=True):
    """Outline kepala + hidung + telinga. Penanda arah wajib: tanpa hidung,
    pembaca tidak bisa tahu mana anterior."""
    ax.add_patch(Circle((0, 0), radius, fill=False, lw=lw, ec=color, zorder=4))
    if nose:
        w, h = 0.13 * radius, 0.16 * radius
        ax.plot([-w, 0, w], [radius * 0.99, radius + h, radius * 0.99],
                lw=lw, c=color, solid_joinstyle="round", zorder=4,
                clip_on=False)
    if ears:
        for s in (-1, 1):
            ax.add_patch(Ellipse((s * radius, 0.0), 0.10 * radius,
                                 0.34 * radius, fill=False, lw=lw, ec=color,
                                 zorder=3, clip_on=False))
    ax.set_xlim(-radius * 1.28, radius * 1.28)
    ax.set_ylim(-radius * 1.24, radius * 1.32)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return ax


def topomap(ax, channels, values, vmin=None, vmax=None, cmap="RdBu_r",
            res=200, levels=7, contours=True, show_names=False,
            signif=None, dot_size=9, radius=1.0, prefer_mne=False):
    """Topografi kulit kepala dengan elektroda pada posisi 10-20 sebenarnya.

    channels : nama kanal (dicocokkan ke montase standar)
    values   : satu nilai per kanal
    signif   : subset nama kanal yang lolos koreksi -> ditandai titik putih
               BESAR di atas topografi (jangan buat panel signifikansi
               terpisah)

    Untuk kuantitas BERTANDA (beda kondisi, nilai t, ERD/ERS) berikan
    vmin=-vmax dan colormap divergen, sehingga nol tepat di tengah skala.
    Bila menggambar beberapa kondisi berdampingan, pakai vmin/vmax yang SAMA
    untuk semuanya dan satu colorbar bersama.

    Interpolasi ditampilkan hanya di dalam batas kepala. Untuk montase jarang
    (< ~20 kanal) interpolasi halus melebih-lebihkan resolusi spasial: titik
    elektroda selalu digambar, dan pertimbangkan contours=True agar sifat
    interpolatifnya terlihat.
    """
    from scipy.interpolate import griddata

    values = np.asarray(values, dtype=float)
    xy = electrode_xy(channels, prefer_mne=prefer_mne)
    if len(xy) != len(values):
        raise ValueError(f"{len(xy)} kanal vs {len(values)} nilai — tidak cocok")
    if len(xy) < 4:
        raise ValueError("topomap butuh >= 4 kanal; untuk kanal sedikit "
                         "gunakan montage_glyph atau plot per-kanal")

    g = np.linspace(-radius, radius, res)
    gx, gy = np.meshgrid(g, g)
    # Interpolasi hanya di dalam convex hull elektroda; sisanya diisi tetangga
    # terdekat lalu dihaluskan ringan. Tidak ada titik jangkar buatan di tepi —
    # jangkar bernilai rerata menciptakan gradien palsu ke arah batas kepala.
    zi = griddata(xy, values, (gx, gy), method="cubic")
    near = griddata(xy, values, (gx, gy), method="nearest")
    zi = np.where(np.isnan(zi), near, zi)
    try:
        from scipy.ndimage import gaussian_filter
        zi = gaussian_filter(zi, sigma=res / 90.0)
    except Exception:                                    # noqa: BLE001
        pass
    zi[gx ** 2 + gy ** 2 > radius ** 2] = np.nan

    if vmax is None:
        vmax = float(np.nanmax(np.abs(values)))
    if vmin is None:
        vmin = -vmax if np.nanmin(values) < 0 else 0.0

    im = ax.imshow(zi, extent=(-radius, radius, -radius, radius), origin="lower",
                   cmap=cmap, vmin=vmin, vmax=vmax, interpolation="bilinear",
                   zorder=1)
    if contours:
        ax.contour(gx, gy, zi, levels=levels, colors="0.25",
                   linewidths=0.35, zorder=2)
    ax.scatter(xy[:, 0], xy[:, 1], s=dot_size, c="0.15", lw=0, zorder=5)
    if signif:
        sxy = electrode_xy(list(signif), prefer_mne=prefer_mne)
        ax.scatter(sxy[:, 0], sxy[:, 1], s=dot_size * 3.2, marker="o",
                   facecolor="white", edgecolor="0.1", lw=0.7, zorder=6)
    if show_names:
        for (x, y), n in zip(xy, channels):
            ax.text(x, y + 0.07, n, ha="center", va="bottom", fontsize=5,
                    zorder=6)
    draw_head(ax, radius=radius)
    return im


def montage_glyph(ax, all_channels, active, hue="#0072B2", radius=1.0,
                  size=14, inactive_size=6, label=None, prefer_mne=False):
    """Glif kepala kecil: kanal aktif pekat, kanal lain kosong.

    Dipakai di atas kurva ablasi atau di samping label kondisi, agar pembaca
    melihat SUBSET ELEKTRODA MANA yang dimaksud, bukan sekadar jumlahnya.
    """
    active = [_ALIAS.get(c, c) for c in active]
    all_channels = [_ALIAS.get(c, c) for c in all_channels]
    unknown = [c for c in active if c not in all_channels]
    if unknown:
        raise ValueError(f"kanal aktif di luar montase: {unknown}")
    xy_all = electrode_xy(all_channels, prefer_mne=prefer_mne)
    mask = np.array([c in set(active) for c in all_channels])
    ax.scatter(xy_all[~mask, 0], xy_all[~mask, 1], s=inactive_size,
               facecolor="none", edgecolor="0.65", lw=0.5, zorder=5)
    ax.scatter(xy_all[mask, 0], xy_all[mask, 1], s=size, c=hue, lw=0, zorder=6)
    draw_head(ax, radius=radius, lw=0.8, color="0.35")
    if label:
        ax.text(0, -radius * 1.30, label, ha="center", va="top",
                fontsize=mpl.rcParams["xtick.labelsize"])
    return ax


# --------------------------------------------------- substrat: peta ubin

# Tata letak ubin 38 provinsi Indonesia (kolom, baris); kolom naik ke timur,
# baris naik ke selatan. Ini SKEMA yang menjaga urutan relatif barat-timur dan
# utara-selatan, bukan peta bergeoreferensi — pakai bila shapefile tidak
# tersedia atau bila keterbacaan wilayah kecil (DKI, DIY) lebih penting
# daripada bentuk. Sebut "peta ubin (skematik)" di caption.
ID_PROVINSI_TILES = {
    "Aceh":                 (0, 0),
    "Sumatera Utara":       (1, 1),
    "Riau":                 (2, 2),
    "Kepulauan Riau":       (4, 2),
    "Sumatera Barat":       (1, 3),
    "Jambi":                (2, 3),
    "Kep. Bangka Belitung": (4, 3),
    "Bengkulu":             (1, 4),
    "Sumatera Selatan":     (2, 4),
    "Lampung":              (2, 5),
    "Kalimantan Utara":     (7, 0),
    "Kalimantan Timur":     (7, 1),
    "Kalimantan Barat":     (5, 2),
    "Kalimantan Tengah":    (6, 3),
    "Kalimantan Selatan":   (7, 3),
    "Sulawesi Utara":       (10, 0),
    "Gorontalo":            (9, 1),
    "Sulawesi Tengah":      (9, 2),
    "Sulawesi Barat":       (8, 3),
    "Sulawesi Selatan":     (9, 4),
    "Sulawesi Tenggara":    (10, 3),
    "Banten":               (3, 6),
    "DKI Jakarta":          (4, 6),
    "Jawa Barat":           (4, 7),
    "Jawa Tengah":          (5, 6),
    "DI Yogyakarta":        (5, 7),
    "Jawa Timur":           (6, 6),
    "Bali":                 (7, 6),
    "Nusa Tenggara Barat":  (8, 6),
    "Nusa Tenggara Timur":  (9, 6),
    "Maluku Utara":         (11, 1),
    "Maluku":               (11, 4),
    "Papua Barat Daya":     (12, 1),
    "Papua Barat":          (12, 2),
    "Papua Tengah":         (13, 2),
    "Papua Pegunungan":     (14, 3),
    "Papua":                (14, 1),
    "Papua Selatan":        (13, 4),
}


def tile_map(ax, tiles, values=None, labels=None, cmap="magma_r",
             vmin=None, vmax=None, cbar_label=None, label_fmt=None,
             missing_color="0.92", missing_label="tidak ada data",
             text_threshold=0.55, gap=0.08, abbrev=4, fontsize=None):
    """Peta ubin: satu kotak per wilayah, posisi relatif dijaga.

    tiles  : {nama_wilayah: (kolom, baris)} — mis. ID_PROVINSI_TILES
    values : {nama_wilayah: nilai}; wilayah tanpa nilai diberi warna + arsir
             "tidak ada data" (kotak kosong tanpa keterangan terbaca sebagai
             nilai terendah — aturan geospasial)
    labels : {nama: teks} untuk menimpa singkatan otomatis

    Keunggulan atas choropleth: wilayah kecil (DKI, DIY) tidak hilang, dan
    tidak butuh shapefile. Kelemahannya bentuk dan jarak hilang — karena itu
    WAJIB disebut skematik di caption.
    """
    fontsize = fontsize or mpl.rcParams["xtick.labelsize"]
    vals = {} if values is None else dict(values)
    numeric = [v for v in vals.values() if v is not None and not (
        isinstance(v, float) and math.isnan(v))]
    if numeric:
        vmin = min(numeric) if vmin is None else vmin
        vmax = max(numeric) if vmax is None else vmax
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cm = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap

    has_missing = False
    for name, (c, r) in tiles.items():
        v = vals.get(name)
        if v is None or (isinstance(v, float) and math.isnan(v)):
            fc, txt_c, has_missing = missing_color, "0.45", True
            ax.add_patch(mpl.patches.Rectangle(
                (c + gap / 2, -r + gap / 2), 1 - gap, 1 - gap,
                facecolor=fc, edgecolor="white", lw=0.6, hatch="///", zorder=2))
        else:
            rgba = cm(norm(v))
            fc = rgba
            lum = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
            txt_c = "white" if lum < text_threshold else "0.1"
            ax.add_patch(mpl.patches.Rectangle(
                (c + gap / 2, -r + gap / 2), 1 - gap, 1 - gap,
                facecolor=fc, edgecolor="white", lw=0.6, zorder=2))
        lab = (labels or {}).get(name) or _abbrev(name, abbrev)
        ax.text(c + 0.5, -r + 0.62, lab, ha="center", va="center",
                fontsize=fontsize, color=txt_c, zorder=3)
        if label_fmt and v is not None and not (isinstance(v, float) and math.isnan(v)):
            ax.text(c + 0.5, -r + 0.30, label_fmt.format(v), ha="center",
                    va="center", fontsize=fontsize * 0.92, color=txt_c, zorder=3)

    cols = [c for c, _ in tiles.values()]
    rows = [r for _, r in tiles.values()]
    ax.set_xlim(min(cols) - 0.1, max(cols) + 1.1)
    ax.set_ylim(-max(rows) - 0.1, -min(rows) + 1.1)
    ax.set_aspect("equal")
    ax.set_axis_off()
    if numeric:
        sm = mpl.cm.ScalarMappable(norm=norm, cmap=cm)
        cb = ax.figure.colorbar(sm, ax=ax, fraction=0.025, pad=0.02)
        cb.ax._vizkit_colorbar = True
        if cbar_label:
            cb.set_label(cbar_label)
    if has_missing:
        proxy = mpl.patches.Patch(facecolor=missing_color, hatch="///",
                                  edgecolor="white", label=missing_label)
        ax.legend(handles=[proxy], loc="lower left", fontsize=fontsize,
                  frameon=False, bbox_to_anchor=(0.0, -0.02))
    return ax


def _abbrev(name, n=4):
    parts = [p for p in name.replace(".", " ").split() if p]
    if len(parts) == 1:
        return parts[0][:n]
    return "".join(p[0] for p in parts if p[0].isupper())[:4] or parts[0][:n]


# ------------------------------------------------- bentuk khas domain lain

def likert_diverging(ax, items, counts, categories, neutral_index=None,
                     split_neutral=True, n_per_item=None, colors=None,
                     percent=True, fontsize=None):
    """Diverging stacked bar untuk item ordinal (Likert).

    counts : (n_item, n_kategori), urut dari paling tidak setuju ke paling
             setuju. Digambar sebagai PROPORSI, bukan rerata — rerata Likert
             menyembunyikan distribusi bimodal, yang artinya berlawanan dengan
             distribusi menumpuk di tengah.
    neutral_index / split_neutral : netral dibelah di titik nol (default) atau
             set split_neutral=False untuk mengecualikannya dari batang
             (katakan yang mana di caption).
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    counts = np.asarray(counts, dtype=float)
    if counts.shape != (len(items), len(categories)):
        raise ValueError(f"counts {counts.shape} != ({len(items)}, {len(categories)})")
    tot = counts.sum(1, keepdims=True)
    frac = counts / np.where(tot == 0, 1, tot)
    data = frac * 100 if percent else frac

    k = len(categories)
    ni = neutral_index
    if colors is None:
        neg = ramp("#762a83", (ni if ni is not None else k // 2))[::-1]
        pos = ramp("#1b7837", k - (ni + 1) if ni is not None else k - k // 2)
        colors = list(neg) + ([RULE] if ni is not None else []) + list(pos)

    for i in range(len(items)):
        row = data[i]
        if ni is not None:
            left = -(row[:ni].sum() + (row[ni] / 2 if split_neutral else 0))
        else:
            left = -row[:k // 2].sum()
        for j in range(k):
            w = row[j]
            if ni is not None and j == ni and not split_neutral:
                continue
            ax.barh(i, w, left=left, color=colors[j], height=0.72,
                    edgecolor="white", lw=0.4,
                    label=categories[j] if i == 0 else None)
            left += w

    ax.axvline(0, color=INK, lw=0.8, zorder=5)
    lab = list(items)
    if n_per_item is not None:
        lab = [f"{t}  (n={n})" for t, n in zip(items, n_per_item)]
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels(lab)
    ax.invert_yaxis()
    ax.set_xlabel("Persentase responden" if percent else "Proporsi responden")
    ax.legend(ncol=min(k, 5), loc="upper center", bbox_to_anchor=(0.5, -0.16),
              frameon=False, fontsize=fontsize)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    note = "netral dibelah di nol" if (ni is not None and split_neutral) else \
           ("netral dikecualikan" if ni is not None else "")
    if note:
        ax.text(1.0, 1.02, note, transform=ax.transAxes, ha="right",
                fontsize=fontsize, color=MUTE)
    return ax


def forest_plot(ax, labels, est, lo, hi, weights=None, summary=None,
                log_scale=True, null_value=1.0, xlabel=None,
                summary_label="Ringkasan (acak)", color="#0072B2",
                fontsize=None):
    """Forest plot: satu baris per studi, kotak sebanding bobot, diamond ringkas.

    log_scale=True untuk rasio (OR/RR/HR) — 0,5 dan 2,0 harus berjarak sama
    dari 1,0. Untuk beda rerata pakai log_scale=False dan null_value=0.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    est, lo, hi = map(lambda a: np.asarray(a, float), (est, lo, hi))
    n = len(labels)
    w = np.ones(n) if weights is None else np.asarray(weights, float)
    w = w / w.max()
    y = np.arange(n)

    ax.axvline(null_value, color="0.35", lw=0.8, zorder=1)
    for i in range(n):
        ax.plot([lo[i], hi[i]], [y[i], y[i]], color=color, lw=0.9, zorder=2)
        ax.scatter(est[i], y[i], s=18 + 90 * w[i], marker="s", c=color,
                   edgecolor="white", lw=0.4, zorder=3)

    yticks, ylabels = list(y), list(labels)
    if summary is not None:
        s_est, s_lo, s_hi = summary
        ys = n + 0.6
        ax.add_patch(Polygon([[s_lo, ys], [s_est, ys + 0.32],
                              [s_hi, ys], [s_est, ys - 0.32]],
                             closed=True, facecolor=INK, edgecolor="none",
                             zorder=4))
        yticks.append(ys)
        ylabels.append(summary_label)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    ax.invert_yaxis()
    if log_scale:
        ax.set_xscale("log")
        span = [np.nanmin(lo), np.nanmax(hi)]
        if summary is not None:
            span = [min(span[0], summary[1]), max(span[1], summary[2])]
        nice = [0.1, 0.2, 0.25, 0.33, 0.5, 0.67, 1, 1.5, 2, 3, 4, 5, 10, 20]
        ticks = [t for t in nice if span[0] * 0.85 <= t <= span[1] * 1.15]
        if null_value not in ticks:
            ticks = sorted(ticks + [null_value])
        ax.set_xticks(ticks)
        ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(
            lambda v, _: f"{v:g}"))
        ax.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    ax.set_xlabel(xlabel or ("Rasio (CI 95%)" if log_scale else "Beda (CI 95%)"))
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    return ax


def dot_whisker(ax, labels, est, lo, hi, null_value=0.0, color="#0072B2",
                xlabel=None, ref_note=None, sort=False, fontsize=None):
    """Koefisien model sebagai titik + CI. Pengganti tabel regresi.

    Bila prediktor berbeda satuan, berikan koefisien TERSTANDARDISASI dan
    katakan demikian di xlabel. ref_note menyatakan kategori acuan.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    est, lo, hi = map(lambda a: np.asarray(a, float), (est, lo, hi))
    order = np.argsort(est) if sort else np.arange(len(est))
    labels = [labels[i] for i in order]
    est, lo, hi = est[order], lo[order], hi[order]
    y = np.arange(len(labels))
    ax.axvline(null_value, color="0.35", lw=0.8, zorder=1)
    crosses = (lo <= null_value) & (hi >= null_value)
    for i in range(len(y)):
        c = COMPARATOR if crosses[i] else color
        ax.plot([lo[i], hi[i]], [y[i], y[i]], color=c, lw=1.0, zorder=2)
        ax.scatter(est[i], y[i], s=16, c=c, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel or "Koefisien (CI 95%)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    if ref_note:
        # Bukan di atas panel (y=1.02 adalah slot judul: catatan acuan yang
        # panjang selalu bertumpuk dengan judul), dan bukan di sudut mana pun
        # secara buta — sudut kanan-bawah biasanya ditempati baris terakhir.
        # Ruang di BAWAH sumbu-x dijamin kosong, jadi catatan diletakkan di
        # sana dan tingginya dibayar dengan margin bawah.
        ax.text(0.0, -0.14, ref_note, transform=ax.transAxes, ha="left",
                va="top", fontsize=fontsize, color=MUTE)
    return ax


def confusion_matrix(ax, cm, labels, normalize="row", cmap="Blues",
                     value_fmt=None, cbar_label=None, fontsize=None):
    """Matriks kebingungan ternormalisasi baris (recall per kelas) + nilai
    tercetak di setiap sel.

    normalize="row" adalah default yang benar untuk kelas timpang: matriks
    jumlah mentah didominasi kelas mayoritas. Jumlah mentah tetap dicetak
    dalam kurung agar denominator tidak hilang.
    """
    fontsize = fontsize or mpl.rcParams["xtick.labelsize"]
    cm = np.asarray(cm, dtype=float)
    if normalize == "row":
        denom = cm.sum(1, keepdims=True)
        M = cm / np.where(denom == 0, 1, denom)
        fmt = value_fmt or "{:.2f}"
        cbar_label = cbar_label or "Proporsi per kelas sebenarnya"
    elif normalize == "col":
        denom = cm.sum(0, keepdims=True)
        M = cm / np.where(denom == 0, 1, denom)
        fmt = value_fmt or "{:.2f}"
        cbar_label = cbar_label or "Proporsi per kelas prediksi"
    else:
        M = cm
        fmt = value_fmt or "{:.0f}"
        cbar_label = cbar_label or "Jumlah"
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=M.max())
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            lum = im.cmap(im.norm(M[i, j]))[:3]
            c = "white" if (0.299 * lum[0] + 0.587 * lum[1] + 0.114 * lum[2]) < 0.55 else "0.1"
            txt = fmt.format(M[i, j])
            if normalize in ("row", "col"):
                txt += f"\n({cm[i, j]:.0f})"
            ax.text(j, i, txt, ha="center", va="center", fontsize=fontsize, color=c)
    rot = 45 if max(len(str(x)) for x in labels) > 6 else 0
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=rot, ha="right" if rot else "center")
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
    ax.set_xlabel("Kelas prediksi"); ax.set_ylabel("Kelas sebenarnya")
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cb.ax._vizkit_colorbar = True
    cb.set_label(cbar_label)
    return im


def alluvial(ax, flows, left_order=None, right_order=None, colors=None,
             gap=0.02, label_fmt="{name} ({n})", fontsize=None):
    """Diagram alluvial dua tahap: perpindahan kategori (bukan dua pie).

    flows : {(kategori_kiri, kategori_kanan): jumlah}
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    L = left_order or sorted({a for a, _ in flows})
    R = right_order or sorted({b for _, b in flows})
    tot = sum(flows.values())
    if colors is None:
        colors = palette(names=L)
    lsz = {a: sum(v for (x, _), v in flows.items() if x == a) for a in L}
    rsz = {b: sum(v for (_, y), v in flows.items() if y == b) for b in R}

    def _stack(order, sizes):
        y, out = 1.0, {}
        for k in order:
            h = sizes[k] / tot * (1 - gap * (len(order) - 1))
            out[k] = [y - h, y]
            y -= h + gap
        return out

    lp, rp = _stack(L, lsz), _stack(R, rsz)
    lcur = {a: lp[a][1] for a in L}
    rcur = {b: rp[b][1] for b in R}
    for a in L:
        for b in R:
            v = flows.get((a, b), 0)
            if not v:
                continue
            h = v / tot * (1 - gap * (len(L) - 1))
            hr = v / tot * (1 - gap * (len(R) - 1))
            y0, y1 = lcur[a] - h, lcur[a]
            z0, z1 = rcur[b] - hr, rcur[b]
            lcur[a] -= h
            rcur[b] -= hr
            t = np.linspace(0, 1, 60)
            s = 3 * t ** 2 - 2 * t ** 3
            ax.fill_between(t, y0 + (z0 - y0) * s, y1 + (z1 - y1) * s,
                            color=colors[a], alpha=0.45, lw=0, zorder=2)
    for a in L:
        ax.add_patch(mpl.patches.Rectangle((-0.035, lp[a][0]), 0.035,
                                           lp[a][1] - lp[a][0],
                                           color=colors[a], zorder=3))
        ax.text(-0.05, (lp[a][0] + lp[a][1]) / 2,
                label_fmt.format(name=a, n=lsz[a]), ha="right", va="center",
                fontsize=fontsize)
    for b in R:
        ax.add_patch(mpl.patches.Rectangle((1.0, rp[b][0]), 0.035,
                                           rp[b][1] - rp[b][0],
                                           color="0.5", zorder=3))
        ax.text(1.05, (rp[b][0] + rp[b][1]) / 2,
                label_fmt.format(name=b, n=rsz[b]), ha="left", va="center",
                fontsize=fontsize)
    ax.set_xlim(-0.42, 1.42)
    ax.set_ylim(0, 1.02)
    ax.set_axis_off()
    return ax


# ------------------------------------------------------------ verifikasi

# ------------------------------------ substrat generik (lintas bidang)

# ---------------------------------------- substrat: dua input -> satu luaran

def surface_pair(fig, X, Y, Z, xlabel, ylabel, zlabel, cmap="viridis",
                 elev=28, azim=-130, levels=10, optimum="max", vcenter=None,
                 data_points=None, gs=None, fontsize=None):
    """Permukaan 3D DAN peta kontur 2D untuk kuantitas yang sama, berdampingan.

    Ini bentuk yang benar untuk struktur "dua input kontinu -> satu luaran":
    response surface (RSM), permukaan aturan fuzzy (setara `gensurf` MATLAB),
    analisis sensitivitas dua bobot kriteria MCDM, sapuan dua hyperparameter,
    dan potongan 2D loss landscape.

    Kenapa berpasangan, bukan 3D saja: permukaan 3D menyampaikan BENTUK
    (kelengkungan, punggungan, interaksi, pelana) tapi buruk untuk MEMBACA
    NILAI — sudut pandang menyembunyikan bagian belakang, perspektif membuat
    tinggi yang sama tampak berbeda, dan pembaca tidak bisa mengambil angka
    dari sumbu z yang miring. Kontur 2D melakukan kebalikannya. Satu panel
    saja selalu membuang salah satunya; menggambar keduanya memakai ruang yang
    sama dengan satu permukaan 3D besar dan menjawab kedua pertanyaan.

    optimum : "max" | "min" | None | (x, y) eksplisit -> ditandai di KEDUA panel
    vcenter : nol semantik untuk colormap divergen (mis. 0 untuk selisih)
    data_points : (n, 2) titik eksperimen/aturan yang benar-benar diamati ->
        digambar di panel kontur. WAJIB diisi bila permukaannya hasil model
        atau interpolasi: tanpa ini pembaca tidak bisa tahu bagian mana yang
        didukung data dan bagian mana ekstrapolasi.

    Kembalikan (ax3d, ax2d).
    """
    from mpl_toolkits.mplot3d import Axes3D          # noqa: F401  (registrasi)

    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    X, Y, Z = np.asarray(X), np.asarray(Y), np.asarray(Z)
    if not (X.shape == Y.shape == Z.shape):
        raise ValueError(f"X{X.shape}, Y{Y.shape}, Z{Z.shape} harus sebentuk "
                         "— pakai np.meshgrid")

    if vcenter is not None:
        vmax = float(np.nanmax(np.abs(Z - vcenter)))
        norm = mpl.colors.Normalize(vcenter - vmax, vcenter + vmax)
    else:
        norm = mpl.colors.Normalize(float(np.nanmin(Z)), float(np.nanmax(Z)))

    # constrained_layout tidak dapat menghitung ukuran axes 3D — label sumbunya
    # miring dan panjangnya bergantung sudut pandang — lalu menciutkan panel ke
    # nol sambil melempar UserWarning. Layout engine dimatikan dan kedua panel
    # ditempatkan eksplisit; hasilnya deterministik dan tidak bergantung versi
    # matplotlib.
    if fig.get_layout_engine() is not None:
        fig.set_layout_engine("none")
    L, R, B, T, GAP = 0.045, 0.985, 0.13, 0.90, 0.10
    w3 = (R - L - GAP) * 0.50
    ax3 = fig.add_axes([L, B - 0.03, w3, T - B + 0.03], projection="3d")
    ax2 = fig.add_axes([L + w3 + GAP, B, (R - L - GAP) - w3 - 0.075, T - B])

    ax3.plot_surface(X, Y, Z, cmap=cmap, norm=norm, rstride=1, cstride=1,
                     linewidth=0.15, edgecolor="white", antialiased=True,
                     alpha=0.95)
    ax3.contour(X, Y, Z, levels=levels, zdir="z",
                offset=float(np.nanmin(Z)), colors="0.6", linewidths=0.4)
    ax3.view_init(elev=elev, azim=azim)
    ax3.set_xlabel(xlabel, fontsize=fontsize, labelpad=2)
    ax3.set_ylabel(ylabel, fontsize=fontsize, labelpad=2)
    ax3.set_zlabel(zlabel, fontsize=fontsize, labelpad=2)
    ax3.tick_params(labelsize=mpl.rcParams["xtick.labelsize"] * 0.85, pad=0)
    for pane in (ax3.xaxis, ax3.yaxis, ax3.zaxis):
        pane.pane.set_facecolor("white")
        pane.pane.set_edgecolor(RULE)
    ax3.grid(True, lw=0.3)
    # Sudut pandang mengubah kesimpulan yang bisa ditarik dari permukaan; catat
    # agar figur dapat direproduksi. Ditaruh sebagai judul kecil di ATAS panel:
    # ruang di bawah axes 3D sudah dipakai label sumbu x/y yang miring.
    ax3.set_title(f"elev {elev}°, azim {azim}°", fontsize=fontsize * 0.9,
                  color=MUTE, loc="left", pad=2)

    cf = ax2.contourf(X, Y, Z, levels=levels * 2, cmap=cmap, norm=norm)
    cl = ax2.contour(X, Y, Z, levels=levels, colors="white", linewidths=0.4)
    clabels = ax2.clabel(cl, inline=True, fontsize=fontsize * 0.85, fmt="%.3g")
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel)
    cb = fig.colorbar(cf, ax=ax2, fraction=0.045, pad=0.02)
    cb.ax._vizkit_colorbar = True
    cb.set_label(zlabel)

    if data_points is not None:
        dp = np.asarray(data_points, dtype=float)
        ax2.scatter(dp[:, 0], dp[:, 1], s=9, facecolor="none",
                    edgecolor="0.15", lw=0.6, zorder=5,
                    label="titik teramati")
        # Legenda di bawah panel: sudut mana pun di dalam bidang kontur pasti
        # menimpa data — bidangnya terisi penuh menurut definisi.
        ax2.legend(loc="upper left", bbox_to_anchor=(0, -0.16), frameon=False,
                   fontsize=fontsize, handletextpad=0.3)

    opt = None
    if optimum in ("max", "min"):
        idx = (np.nanargmax(Z) if optimum == "max" else np.nanargmin(Z))
        i, j = np.unravel_index(idx, Z.shape)
        opt = (float(X[i, j]), float(Y[i, j]), float(Z[i, j]))
    elif isinstance(optimum, (tuple, list)) and len(optimum) >= 2:
        ox, oy = float(optimum[0]), float(optimum[1])
        i = int(np.argmin(np.abs(Y[:, 0] - oy)))
        j = int(np.argmin(np.abs(X[0, :] - ox)))
        opt = (ox, oy, float(Z[i, j]))
    if opt is not None:
        ax3.scatter([opt[0]], [opt[1]], [opt[2]], s=26, c=ALARM,
                    edgecolor="white", lw=0.5, depthshade=False, zorder=10)
        ax2.scatter([opt[0]], [opt[1]], s=26, c=ALARM, edgecolor="white",
                    lw=0.5, zorder=6)
        # Optimum nyaris selalu jatuh di daerah rapat label kontur. Anotasi
        # dicoba pada empat arah dan dipilih yang tidak menabrak label kontur
        # mana pun; bila semuanya menabrak, label kontur terdekat disembunyikan
        # (nilai puncak lebih penting daripada satu label garis).
        ann = None
        ax2.figure.canvas.draw()
        r2 = ax2.figure.canvas.get_renderer()
        cboxes = [t.get_window_extent(r2) for t in clabels if t.get_visible()]
        for dx, dy, ha, va in ((14, 14, "left", "bottom"),
                               (-14, 14, "right", "bottom"),
                               (14, -14, "left", "top"),
                               (-14, -14, "right", "top")):
            if ann is not None:
                ann.remove()
            ann = ax2.annotate(f"optimum {opt[2]:.3g}\n({opt[0]:.3g}, {opt[1]:.3g})",
                               xy=(opt[0], opt[1]), xytext=(dx, dy),
                               textcoords="offset points", fontsize=fontsize,
                               color=ALARM, ha=ha, va=va,
                               bbox=dict(fc="white", ec="none", alpha=0.8, pad=1.0),
                               arrowprops=dict(arrowstyle="-", color=ALARM, lw=0.5))
            ax2.figure.canvas.draw()
            ab = ann.get_window_extent(r2)
            if not any(ab.overlaps(cb) for cb in cboxes) and \
                    ax2.bbox.expanded(1.02, 1.02).contains(ab.x0, ab.y0):
                break
        else:
            for t, cb in zip([t for t in clabels if t.get_visible()], cboxes):
                if ann.get_window_extent(r2).overlaps(cb):
                    t.set_visible(False)
    return ax3, ax2, opt


def parallel_coordinates(ax, labels, criteria, values, focal=None,
                         cmap_by=None, higher_better=None, normalize=True,
                         color="#0072B2", show_range=True, fontsize=None):
    """Koordinat paralel: banyak alternatif dibandingkan pada banyak kriteria.

    Bentuk kanonik MCDM (TOPSIS/AHP/PROMETHEE/SAW) dan sapuan hyperparameter.
    Menggantikan tabel skor panjang dan bar peringkat: pembaca melihat sekaligus
    alternatif mana yang unggul di kriteria mana, dan di mana terjadi
    TRADE-OFF — garis yang bersilangan antar dua sumbu adalah trade-off, dan
    itu justru temuan yang dicari analisis MCDM.

    values : (n_alternatif, n_kriteria)
    higher_better : list bool per kriteria. Kriteria bertipe biaya (makin kecil
        makin baik) dibalik saat normalisasi DAN diberi tanda pada labelnya,
        supaya "makin ke atas makin baik" berlaku seragam di semua sumbu.
    focal : subset label yang ditonjolkan; sisanya abu-abu berbobot rendah.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    V = np.asarray(values, dtype=float)
    if V.shape != (len(labels), len(criteria)):
        raise ValueError(f"values {V.shape} != ({len(labels)}, {len(criteria)})")
    hb = [True] * len(criteria) if higher_better is None else list(higher_better)
    if len(hb) != len(criteria):
        raise ValueError("higher_better harus sepanjang criteria")

    raw_min, raw_max = V.min(0), V.max(0)
    if normalize:
        rng = np.where(raw_max - raw_min == 0, 1, raw_max - raw_min)
        N = (V - raw_min) / rng
        N = np.where(np.array(hb), N, 1 - N)      # kriteria biaya dibalik
    else:
        N = V

    x = np.arange(len(criteria))
    foc = list(dict.fromkeys(focal or []))
    fset = set(foc)
    # Setiap alternatif fokal mendapat HUE SENDIRI. Menggambar semua garis fokal
    # dengan satu warna membuatnya mustahil ditelusuri melewati persilangan —
    # dan persilangan justru bagian yang ingin dibaca (aturan 4.1). Warna
    # diambil dari palet aman buta warna.
    fcol = {lab: palette()[i % 8] for i, lab in enumerate(foc)} if foc else {}
    for i, lab in enumerate(labels):
        is_f = (not foc) or (lab in fset)
        c = fcol.get(lab, color if is_f else COMPARATOR)
        if cmap_by is not None and is_f:
            c = cmap_by[lab] if isinstance(cmap_by, dict) else cmap_by[i]
        ax.plot(x, N[i], c=c, lw=1.6 if (foc and lab in fset) else 0.9,
                alpha=1.0 if is_f else 0.30, zorder=3 if is_f else 1,
                marker="o", markersize=2.5)
        if is_f and (foc or len(labels) <= 8):
            # Dilabeli di KEDUA ujung: dengan satu label saja pembaca harus
            # menelusuri garis melewati setiap persilangan untuk tahu di mana
            # alternatif itu bermula.
            ax.text(x[-1] + 0.06, N[i, -1], lab, fontsize=fontsize, c=c,
                    va="center", ha="left")
            if foc and lab in fset:
                ax.text(x[0] - 0.06, N[i, 0], lab, fontsize=fontsize, c=c,
                        va="center", ha="right")

    for xi in x:
        ax.axvline(xi, c=RULE, lw=0.6, zorder=0)
    # Rentang mentah tiap sumbu masuk ke LABEL TICK, bukan teks mengambang:
    # teks di y=0/1 rutin menabrak garis data dan judul panel, sementara sumbu
    # ternormalisasi tanpa rentang membuat pembaca tidak bisa memulihkan nilai
    # aslinya (aturan 2.1).
    ticks = []
    for k, (crit, good) in enumerate(zip(criteria, hb)):
        nama = crit if good else f"{crit} ↓"
        ticks.append(f"{nama}\n{raw_min[k]:.3g}–{raw_max[k]:.3g}"
                     if show_range else nama)
    ax.set_xticks(x)
    ax.set_xticklabels(ticks)
    ax.set_xlim(-0.25, len(criteria) - 1 + 0.75)
    ax.set_ylim(-0.06, 1.12)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylabel("Ternormalisasi (atas = lebih baik)" if normalize else "Nilai")
    if not all(hb):
        ax.text(1.0, -0.34, "↓ = kriteria biaya (nilai kecil lebih baik), sumbu "
                            "dibalik · angka di bawah nama = rentang nilai mentah",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=fontsize * 0.9, color=MUTE)
    return N


def scatter3d(ax, x, y, z, color="#0072B2", size=12, floor=True, stems=False,
              elev=22, azim=-125, labels=None, fontsize=None, **kw):
    """Sebar titik 3D dengan isyarat kedalaman.

    Pakai HANYA bila datanya memang hidup di ruang tiga dimensi (koordinat
    fisik, tiga tujuan Pareto yang setara) — bukan untuk memaksakan variabel
    ketiga yang lebih baik jadi warna atau ukuran di plot 2D.

    Isyarat kedalaman wajib, karena tanpanya posisi 3D dari layar 2D bersifat
    ambigu: floor=True memproyeksikan bayangan ke lantai, stems=True menarik
    garis tegak dari lantai ke titik.
    """
    from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    x, y, z = map(lambda a: np.asarray(a, float), (x, y, z))
    zmin = float(np.nanmin(z))
    if floor:
        ax.scatter(x, y, np.full_like(z, zmin), s=size * 0.5, c="0.8",
                   lw=0, depthshade=False, zorder=1)
    if stems:
        for xi, yi, zi in zip(x, y, z):
            ax.plot([xi, xi], [yi, yi], [zmin, zi], c="0.8", lw=0.4, zorder=1)
    ax.scatter(x, y, z, s=size, c=color, depthshade=True, lw=0, zorder=3, **kw)
    if labels is not None:
        for xi, yi, zi, l in zip(x, y, z, labels):
            ax.text(xi, yi, zi, f" {l}", fontsize=fontsize)
    ax.view_init(elev=elev, azim=azim)
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.pane.set_facecolor("white")
        pane.pane.set_edgecolor(RULE)
    ax.set_title(f"elev {elev}°, azim {azim}°", fontsize=fontsize * 0.9,
                 color=MUTE, loc="left", pad=2)
    return ax


def _spread_labels(values, min_gap, lo=None, hi=None, iters=80):
    """Sebarkan posisi label 1-D agar berjarak >= min_gap, sedekat mungkin ke
    posisi aslinya. Dipakai untuk pelabelan langsung (aturan 6.3/6.9) bila
    beberapa unit punya nilai yang berdekatan."""
    v = np.asarray(values, dtype=float)
    order = np.argsort(v)
    y = v[order].copy()
    lo = y.min() if lo is None else lo
    hi = y.max() if hi is None else hi
    for _ in range(iters):
        moved = False
        for i in range(len(y) - 1):
            d = y[i + 1] - y[i]
            if d < min_gap:
                shift = (min_gap - d) / 2
                y[i] -= shift
                y[i + 1] += shift
                moved = True
        y[0] = max(y[0], lo)
        y[-1] = min(y[-1], hi)
        if not moved:
            break
    out = np.empty_like(y)
    out[order] = y
    return out


# --------------------------------------- substrat: asesmen & ekonomi-bisnis

def wright_map(ax_person, ax_item, abilities, item_labels, difficulties,
               bins=22, hue="#0072B2", item_color=None, se=None,
               unit="logit", fontsize=None):
    """Peta Wright (item-person map) Rasch: kemampuan peserta dan tingkat
    kesulitan butir pada SATU skala logit yang sama.

    Inilah figur yang menjawab pertanyaan yang tidak bisa dijawab oleh rerata
    skor: apakah instrumennya **menjangkau** peserta yang diukur. Butir yang
    menumpuk di logit 0 sementara peserta tersebar di +2 berarti tes terlalu
    mudah untuk kelompok itu, dan kesenjangan (gap) pada skala menandakan
    rentang kemampuan yang tidak terukur oleh butir mana pun.

    ax_person / ax_item : dua axes bersumbu-y BERSAMA (sharey=True).
    abilities   : estimasi kemampuan peserta (logit)
    difficulties: tingkat kesulitan tiap butir (logit)
    se          : galat baku tiap butir -> digambar sebagai bar horizontal

    Kembalikan dict: jangkauan, rerata, dan kesenjangan terbesar pada skala.
    """
    fontsize = fontsize or mpl.rcParams["ytick.labelsize"]
    ab = np.asarray(abilities, dtype=float)
    df = np.asarray(difficulties, dtype=float)
    if len(item_labels) != len(df):
        raise ValueError(f"{len(item_labels)} label vs {len(df)} kesulitan")

    lo = min(ab.min(), df.min()) - 0.5
    hi = max(ab.max(), df.max()) + 0.5

    ax_person.hist(ab, bins=bins, range=(lo, hi), orientation="horizontal",
                   color=hue, edgecolor="white", lw=0.4)
    ax_person.invert_xaxis()
    ax_person.set_xlabel("Jumlah peserta")
    ax_person.spines["left"].set_visible(False)
    ax_person.tick_params(axis="y", length=0, labelleft=False)

    ic = item_color or COMPARATOR
    order = np.argsort(df)
    ypos = _spread_labels(df, (hi - lo) * 0.028)
    for rank, i in enumerate(order):
        y, yr = ypos[i], df[i]
        ax_item.scatter(0, yr, s=14, c=ic, zorder=3, lw=0)
        if se is not None:
            ax_item.plot([-se[i] * 0.6, se[i] * 0.6], [yr, yr], c=ic, lw=0.8,
                         zorder=2)
        ax_item.text(0.06, y, item_labels[i], fontsize=fontsize, va="center",
                     ha="left", color=ic)
        if abs(y - yr) > (hi - lo) * 0.012:
            ax_item.plot([0.012, 0.055], [yr, y], c=ic, lw=0.4, alpha=0.7,
                         zorder=1)
    ax_item.set_xlim(-0.12, 1.0)
    ax_item.set_xticks([])
    ax_item.spines["bottom"].set_visible(False)
    ax_item.set_xlabel("Butir")

    for a in (ax_person, ax_item):
        a.set_ylim(lo, hi)
        a.axhline(0, c=RULE, lw=0.7, zorder=0)
    ax_person.set_ylabel(f"Skala bersama ({unit})")

    ds = np.sort(df)
    gaps = np.diff(ds)
    gap_max = float(gaps.max()) if len(gaps) else 0.0
    gpos = (float(ds[int(np.argmax(gaps))]), float(ds[int(np.argmax(gaps)) + 1])) \
        if len(gaps) else None
    return {"rerata_peserta": float(ab.mean()),
            "rerata_butir": float(df.mean()),
            "selisih": float(ab.mean() - df.mean()),
            "kesenjangan_terbesar": gap_max,
            "lokasi_kesenjangan": gpos}


def event_study(ax, periods, coefs, lo, hi, ref_period=-1, treat_at=-0.5,
                color="#0072B2", xlabel="Periode relatif terhadap perlakuan",
                ylabel=None, pre_label="Pra-perlakuan", post_label="Pasca",
                fontsize=None):
    """Plot event study: koefisien per periode relatif + CI, garis perlakuan.

    Bentuk kanonik desain difference-in-differences dinamis dan interrupted
    time series. Nilainya bukan sekadar menampilkan efek: koefisien PRA-perlakuan
    adalah **uji asumsi tren paralel** yang bisa dinilai pembaca dengan mata —
    koefisien pra yang berbeda dari nol secara sistematis meruntuhkan
    identifikasi, dan menyembunyikannya adalah kelalaian yang serius.

    ref_period : periode acuan yang dinormalkan ke nol (biasanya -1). Digambar
        sebagai titik kosong berlabel, bukan dihilangkan — pembaca harus tahu
        terhadap apa koefisien lain diukur.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    t = np.asarray(periods, dtype=float)
    b = np.asarray(coefs, dtype=float)
    lo_, hi_ = np.asarray(lo, float), np.asarray(hi, float)

    ax.axhline(0, c="0.35", lw=0.8, zorder=1)
    ax.axvline(treat_at, c=ALARM, ls="--", lw=0.9, zorder=1)

    pre = t < treat_at
    for m, alpha in ((pre, 0.55), (~pre, 1.0)):
        ax.errorbar(t[m], b[m], yerr=[b[m] - lo_[m], hi_[m] - b[m]],
                    fmt="o", ms=3.2, lw=0.9, capsize=1.8, color=color,
                    alpha=alpha, zorder=3)
    if ref_period is not None and ref_period in set(t.tolist()):
        k = int(np.where(t == ref_period)[0][0])
        ax.scatter([t[k]], [b[k]], s=22, facecolor="white", edgecolor=color,
                   lw=0.9, zorder=4)
        ax.annotate("acuan", xy=(t[k], b[k]), xytext=(0, -12),
                    textcoords="offset points", ha="center",
                    fontsize=fontsize, color=MUTE)

    # Penanda rezim dijangkarkan ke UJUNG panel, bukan ke garis perlakuan.
    # Menempatkannya relatif garis butuh mengukur lebar teks, dan pengukuran itu
    # keliru begitu constrained_layout mengubah lebar axes sesudahnya — label
    # yang lolos saat panel berdiri sendiri menabrak spine di figur multi-panel.
    # Garis perlakuan yang memisahkan kedua rezim, jadi label di ujung sudah
    # cukup tidak ambigu. Koordinat axes juga menjaga label tetap di bawah spine
    # atas berapa pun besar efeknya.
    ax.margins(y=0.14)
    ax.text(0.015, 0.97, pre_label, transform=ax.transAxes, ha="left",
            va="top", fontsize=fontsize, color=MUTE)
    ax.text(0.985, 0.97, post_label, transform=ax.transAxes, ha="right",
            va="top", fontsize=fontsize, color=MUTE)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel or "Estimasi efek (CI 95%)")
    ax.set_xticks(t)

    pre_sig = [int(x) for x, l, h in zip(t[pre], lo_[pre], hi_[pre])
               if not (l <= 0 <= h)]
    return {"pra_signifikan": pre_sig, "n_pra": int(pre.sum()),
            "n_pasca": int((~pre).sum())}


def waterfall(ax, labels, deltas, start=0.0, start_label="Awal",
              end_label="Akhir", color_up="#0072B2", color_down="#D55E00",
              color_total="0.35", value_fmt="{:+,.1f}", total_fmt="{:,.1f}",
              connector=True, fontsize=None):
    """Diagram air terjun: jembatan dari nilai awal ke akhir lewat kontribusi.

    Substrat "dekomposisi perubahan" — laba tahun lalu ke tahun ini, varians
    anggaran, perubahan pangsa pasar, dekomposisi pertumbuhan. Menggantikan
    tabel selisih: pembaca langsung melihat komponen mana yang menaikkan dan
    mana yang menggerus, beserta besarannya relatif satu sama lain.

    deltas: kontribusi tiap komponen (bertanda). Batang awal dan akhir
    berjangkar di nol; batang komponen mengambang.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    d = np.asarray(deltas, dtype=float)
    if len(labels) != len(d):
        raise ValueError(f"{len(labels)} label vs {len(d)} delta")
    end = start + d.sum()

    xs = np.arange(len(d) + 2)
    ax.bar(0, start, color=color_total, width=0.62, zorder=3)
    ax.text(0, start, total_fmt.format(start), ha="center", va="bottom",
            fontsize=fontsize)

    # Label nilai ditaruh di ATAS batang untuk kontribusi positif dan di BAWAH
    # untuk kontribusi negatif. Menaruh semuanya di atas membuat label batang
    # naik dan batang turun yang bersebelahan bertabrakan di ketinggian yang
    # hampir sama — dan posisi label sekaligus jadi isyarat arah kedua.
    run = start
    for i, (lab, v) in enumerate(zip(labels, d), start=1):
        naik = v >= 0
        c = color_up if naik else color_down
        ax.bar(i, v, bottom=run, color=c, width=0.62, zorder=3)
        top = run + v
        ax.text(i, max(run, top) if naik else min(run, top),
                value_fmt.format(v), ha="center",
                va="bottom" if naik else "top", fontsize=fontsize, color=c)
        if connector:
            ax.plot([i - 0.31, i + 0.31 + 0.38], [top, top], c="0.6", lw=0.5,
                    ls=":", zorder=2)
        run = top

    ax.bar(len(d) + 1, end, color=color_total, width=0.62, zorder=3)
    ax.text(len(d) + 1, end, total_fmt.format(end), ha="center", va="bottom",
            fontsize=fontsize)
    ax.axhline(0, c=INK, lw=0.7, zorder=1)
    # Rotasi label DIUKUR, bukan ditebak dari panjang string: lebar teks
    # bergantung font, dpi, dan lebar figur, sehingga ambang jumlah-karakter
    # meleset. Dicoba dari yang paling terbaca (0°) sampai yang pertama bebas
    # tabrakan.
    semua = [start_label] + list(labels) + [end_label]
    ax.set_xticks(xs)
    fig_ = ax.figure
    for rot in (0, 30, 45, 60, 90):
        ax.set_xticklabels(semua, rotation=rot,
                           ha="right" if rot else "center",
                           rotation_mode="anchor" if rot else None)
        # Digambar dua kali: constrained_layout menggeser axes pada draw
        # pertama, posisi label baru stabil pada draw kedua. Disyaratkan CELAH
        # minimum, bukan sekadar tidak bertumpang — layout masih menata ulang
        # sedikit pada draw berikutnya, sehingga rotasi yang lolos dengan margin
        # nol tetap bertabrakan di figur akhir.
        fig_.canvas.draw()
        fig_.canvas.draw()
        r = fig_.canvas.get_renderer()
        bx = [t.get_window_extent(r) for t in ax.get_xticklabels()]
        celah = min((bx[i + 1].x0 - bx[i].x1 for i in range(len(bx) - 1)),
                    default=np.inf)
        if celah >= 4.0:
            break
    ax.margins(y=0.16)
    return {"awal": float(start), "akhir": float(end),
            "perubahan": float(end - start)}


def lorenz_curve(ax, values, color="#0072B2", label=None, fill=True,
                 show_gini=True, equality_label="Kesetaraan sempurna",
                 fontsize=None):
    """Kurva Lorenz + koefisien Gini yang dihitung dari data yang digambar.

    Bentuk kanonik ketimpangan (pendapatan, aset, nilai ujian, pangsa pasar,
    konsentrasi pelanggan). Menggantikan "rasio 20% teratas" tunggal: kurvanya
    menunjukkan ketimpangan di SELURUH distribusi, dan dua distribusi dengan
    Gini yang sama bisa punya bentuk kurva yang sangat berbeda.

    Gini dihitung dengan aturan trapesium pada kurva yang benar-benar
    digambar, sehingga angka di caption dan gambar tidak mungkin berbeda.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    v = np.sort(np.asarray(values, dtype=float))
    if (v < 0).any():
        raise ValueError("kurva Lorenz butuh nilai non-negatif")
    n = v.size
    cum = np.concatenate([[0.0], np.cumsum(v) / v.sum()])
    x = np.arange(n + 1) / n

    ax.plot([0, 1], [0, 1], ls="--", lw=0.8, c="0.45", zorder=2,
            label=equality_label)
    ax.plot(x, cum, lw=1.4, c=color, zorder=3, label=label)
    if fill:
        ax.fill_between(x, cum, x, color=color, alpha=0.15, lw=0, zorder=1)

    gini = float(1 - 2 * np.trapezoid(cum, x)) if hasattr(np, "trapezoid") \
        else float(1 - 2 * np.trapz(cum, x))
    if show_gini:
        ax.text(0.05, 0.92, f"Gini = {gini:.3f}\nn = {n}", transform=ax.transAxes,
                fontsize=fontsize, va="top", color=color)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("Proporsi kumulatif populasi (terurut menaik)")
    ax.set_ylabel("Proporsi kumulatif total")
    return gini


def rose_plot(ax, directions, magnitudes=None, bins=16, color="#0072B2",
              units="deg", zero="N", clockwise=True, show_mean=True,
              label_fmt="{:.0f}°", fontsize=None):
    """Diagram mawar untuk data BERARAH atau BERSIKLUS.

    Substrat lingkaran, dipakai jauh lebih luas daripada yang disadari: arah
    angin/arus, orientasi struktur geologi, jam dalam sehari (kronobiologi,
    lalu lintas, IGD), bulan dalam setahun (fenologi, wabah musiman), fase
    siklus, sudut sendi, arah pandang.

    Alasan bentuk ini wajib untuk data berarah: rerata aritmetik dari 350° dan
    10° adalah 180° — arah yang berlawanan dengan keduanya. show_mean=True
    menggambar vektor rerata SIRKULAR beserta panjang resultan R (0 = sebaran
    seragam, 1 = terkonsentrasi sempurna); laporkan R, bukan simpangan baku
    biasa.

    ax harus polar:  ax = fig.add_subplot(projection="polar")
    units: "deg" | "rad" | "hour" (0-24) | "month" (1-12)
    """
    if getattr(ax, "name", "") != "polar":
        raise TypeError('rose_plot butuh sumbu polar: '
                        'ax = fig.add_subplot(projection="polar")')
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    d = np.asarray(directions, dtype=float)
    period = {"deg": 360.0, "rad": 2 * np.pi, "hour": 24.0, "month": 12.0}[units]
    if units == "month":
        d = d - 1                                   # Januari -> 0
    theta = (d % period) / period * 2 * np.pi

    edges = np.linspace(0, 2 * np.pi, bins + 1)
    if magnitudes is None:
        h, _ = np.histogram(theta, bins=edges)
        radial_label = "Jumlah pengamatan"
    else:
        m = np.asarray(magnitudes, dtype=float)
        idx = np.clip(np.digitize(theta, edges) - 1, 0, bins - 1)
        h = np.array([m[idx == i].sum() for i in range(bins)])
        radial_label = "Jumlah magnitudo"

    width = 2 * np.pi / bins
    ax.bar(edges[:-1], h, width=width, align="edge", color=color,
           edgecolor="white", lw=0.4, zorder=2)
    ax.set_theta_zero_location(zero)
    ax.set_theta_direction(-1 if clockwise else 1)

    if units == "hour":
        ax.set_xticks(np.arange(0, 24, 3) / 24 * 2 * np.pi)
        ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 24, 3)])
    elif units == "month":
        ax.set_xticks(np.arange(12) / 12 * 2 * np.pi)
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
                            "Jul", "Ags", "Sep", "Okt", "Nov", "Des"])

    stats = {}
    if show_mean and len(theta):
        w = np.ones_like(theta) if magnitudes is None else np.asarray(magnitudes, float)
        C, S = (w * np.cos(theta)).sum(), (w * np.sin(theta)).sum()
        R = np.hypot(C, S) / max(w.sum(), 1e-12)
        mean_theta = np.arctan2(S, C) % (2 * np.pi)
        ax.annotate("", xy=(mean_theta, h.max() * R), xytext=(mean_theta, 0),
                    arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2),
                    zorder=5)
        mean_unit = mean_theta / (2 * np.pi) * period + (1 if units == "month" else 0)
        stats = {"mean_direction": float(mean_unit), "R": float(R),
                 "n": int(len(theta))}
        ax.set_title(f"rerata sirkular {label_fmt.format(mean_unit)} · "
                     f"R = {R:.2f} · n = {len(theta)}", fontsize=fontsize,
                     color=MUTE, loc="left")
    # Pada sumbu polar, set_ylabel jatuh di tepi kiri dan rutin menabrak label
    # sudut. Label radial ditulis sebagai anotasi di luar lingkaran, di bawah.
    ax.text(0.5, -0.09, radial_label, transform=ax.transAxes, ha="center",
            va="top", fontsize=fontsize, color=MUTE)
    ax.grid(True, lw=0.4, alpha=0.6)
    return stats


def slope_plot(ax, labels, before, after, tick_labels=("Sebelum", "Sesudah"),
               color_up="#0072B2", color_down="#D55E00", color_flat=COMPARATOR,
               flat_tol=0.0, value_fmt="{:.2f}", highlight=None,
               label_gap=0.045, fontsize=None):
    """Slope plot: satu garis per unit antara dua kondisi/waktu.

    Substrat "perubahan berpasangan", dipakai di bidang mana pun yang mengukur
    unit yang sama dua kali: pra-pascates pendidikan, sebelum-sesudah
    intervensi, dua musim panen, dua rezim kebijakan, dua rilis perangkat
    lunak. Menggantikan dua bar chart berdampingan, yang membuang informasi
    PASANGAN — bar hanya menampilkan dua rerata dan menyembunyikan bahwa
    sebagian unit justru bergerak berlawanan arah.

    Warna mengkodekan arah perubahan; unit yang berubah di bawah flat_tol
    digambar netral. highlight: subset label yang ditebalkan.
    """
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]
    before = np.asarray(before, float)
    after = np.asarray(after, float)
    if not (len(labels) == len(before) == len(after)):
        raise ValueError("labels/before/after harus sama panjang")
    hi = set(highlight or [])
    naik = turun = datar = 0
    cols = []
    for b, a, lab in zip(before, after, labels):
        d = a - b
        if abs(d) <= flat_tol:
            cols.append(color_flat); datar += 1
        elif d > 0:
            cols.append(color_up); naik += 1
        else:
            cols.append(color_down); turun += 1

    for lab, b, a, c in zip(labels, before, after, cols):
        w = 1.6 if lab in hi else 0.9
        al = 1.0 if (not hi or lab in hi) else 0.45
        ax.plot([0, 1], [b, a], c=c, lw=w, alpha=al, zorder=2,
                solid_capstyle="round")
        ax.scatter([0, 1], [b, a], s=14 if lab in hi else 9, c=c, alpha=al,
                   zorder=3, lw=0)

    # Label disebar agar tidak bertumpuk saat nilai berdekatan; bila digeser
    # dari nilai aslinya, garis penunjuk tipis menghubungkannya ke titik
    # (aturan 6.9: ujung penunjuk harus jelas milik baris yang dinamainya).
    span = float(max(np.max(after), np.max(before)) -
                 min(np.min(after), np.min(before))) or 1.0
    gap = span * label_gap
    for side, vals, xtext, xpoint, ha in (
            ("kiri", before, -0.05, 0.0, "right"),
            ("kanan", after, 1.05, 1.0, "left")):
        ypos = _spread_labels(vals, gap)
        for lab, vraw, y, c in zip(labels, vals, ypos, cols):
            al = 1.0 if (not hi or lab in hi) else 0.45
            txt = (f"{lab}  {value_fmt.format(vraw)}" if side == "kiri"
                   else f"{value_fmt.format(vraw)}  {lab}")
            ax.text(xtext, y, txt, ha=ha, va="center", fontsize=fontsize,
                    color=c, alpha=al)
            if abs(y - vraw) > gap * 0.35:
                ax.plot([xpoint, xtext + (0.012 if side == "kiri" else -0.012)],
                        [vraw, y], c=c, lw=0.4, alpha=al * 0.7, zorder=1)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(tick_labels)
    ax.set_xlim(-0.55, 1.55)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    return {"naik": naik, "turun": turun, "datar": datar}


def ridgeline(ax, groups, data, color="#0072B2", overlap=0.55, bw=None,
              fill_alpha=0.85, show_median=True, n_note=True, fontsize=None):
    """Ridgeline: banyak distribusi pada dukungan yang sama, bertingkat.

    Dipakai saat ada >4 kelompok yang distribusinya perlu dibandingkan dan
    box plot membuang bentuknya (bimodalitas, ekor, pemotongan). Contoh lintas
    bidang: distribusi skor per sekolah, waktu respons per kondisi, curah hujan
    per dekade, harga per wilayah, panjang tuturan per penutur.

    data: list array (satu per kelompok, panjang boleh berbeda). Kelompok
    digambar dari bawah ke atas mengikuti urutan `groups` — urutkan menurut
    variabel yang bermakna (waktu, dosis, peringkat), bukan abjad.
    """
    from scipy.stats import gaussian_kde
    fontsize = fontsize or mpl.rcParams["ytick.labelsize"]
    if len(groups) != len(data):
        raise ValueError("groups dan data harus sama panjang")
    allv = np.concatenate([np.asarray(d, float) for d in data])
    grid = np.linspace(np.nanmin(allv), np.nanmax(allv), 256)
    step = 1.0
    colors = ramp(color, len(groups))
    for i, (g, d) in enumerate(zip(groups, data)):
        d = np.asarray(d, float)
        d = d[~np.isnan(d)]
        if d.size < 2:
            continue
        kde = gaussian_kde(d, bw_method=bw)
        y = kde(grid)
        y = y / y.max() * step * (1 + overlap)
        base = i * step
        ax.fill_between(grid, base, base + y, color=colors[i],
                        alpha=fill_alpha, lw=0, zorder=len(groups) - i)
        ax.plot(grid, base + y, color="white", lw=0.6,
                zorder=len(groups) - i + 0.1)
        if show_median:
            med = float(np.median(d))
            ax.plot([med, med], [base, base + kde(med)[0] / kde(grid).max() *
                                 step * (1 + overlap)],
                    color="white", lw=0.9, zorder=len(groups) - i + 0.2)
        lab = f"{g}  (n={d.size})" if n_note else str(g)
        ax.text(grid[0], base + 0.08, lab, fontsize=fontsize, va="bottom",
                ha="left", zorder=len(groups) + 2)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(-0.1, len(groups) * step + step * (1 + overlap))
    ax.margins(x=0.02)
    return ax


def bubble_matrix(ax, rows, cols, counts, values=None, cmap="viridis",
                  empty_label="belum ada data", size_scale=42, base_size=30,
                  print_counts=True, cbar_label=None, fontsize=None):
    """Matriks gelembung: cakupan/kesenjangan pada persilangan dua kategori.

    Substrat "peta cakupan", berguna jauh di luar scoping review: metode ×
    luaran, spesies × habitat, bahan × proses, kebijakan × sektor, kohor ×
    instrumen. SEL KOSONG adalah temuan — ditandai lingkaran arsir bernama,
    bukan dibiarkan putih (putih terbaca sebagai nol yang terukur).

    counts : (n_rows, n_cols) jumlah pengamatan/studi -> ukuran gelembung
    values : (n_rows, n_cols) kuantitas kedua (mis. mutu rerata) -> warna
    """
    fontsize = fontsize or mpl.rcParams["xtick.labelsize"]
    counts = np.asarray(counts, float)
    if counts.shape != (len(rows), len(cols)):
        raise ValueError(f"counts {counts.shape} != ({len(rows)}, {len(cols)})")
    norm = None
    if values is not None:
        values = np.asarray(values, float)
        norm = mpl.colors.Normalize(np.nanmin(values), np.nanmax(values))
        cm = mpl.colormaps[cmap] if isinstance(cmap, str) else cmap
    kosong = 0
    for i in range(len(rows)):
        for j in range(len(cols)):
            k = counts[i, j]
            if not k or np.isnan(k):
                kosong += 1
                ax.scatter(j, i, s=base_size * 2.0, facecolor="none",
                           edgecolor="0.75", lw=0.6, hatch="///", zorder=2)
                continue
            c = cm(norm(values[i, j])) if values is not None else "#0072B2"
            ax.scatter(j, i, s=base_size + size_scale * k, color=c,
                       edgecolor="white", lw=0.5, zorder=3)
            if print_counts:
                lum = mpl.colors.to_rgb(c)
                tc = "white" if (0.299 * lum[0] + 0.587 * lum[1] +
                                 0.114 * lum[2]) < 0.6 else "0.1"
                ax.text(j, i, f"{k:.0f}", ha="center", va="center",
                        fontsize=fontsize * 0.9, color=tc, zorder=4)
    # Rotasi mengikuti panjang label: 30 derajat cukup untuk label pendek,
    # tapi label panjang pada kolom rapat tetap bertabrakan pada sudut itu.
    rot = 45 if max(len(str(c)) for c in cols) > 8 else 30
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=rot, ha="right",
                       rotation_mode="anchor")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows)
    ax.set_xlim(-0.6, len(cols) - 0.4)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.invert_yaxis()
    if values is not None:
        sm = mpl.cm.ScalarMappable(norm=norm, cmap=cm)
        cb = ax.figure.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
        cb.ax._vizkit_colorbar = True
        if cbar_label:
            cb.set_label(cbar_label)
    if kosong:
        ax.legend(handles=[mpl.lines.Line2D(
            [], [], marker="o", ls="none", markerfacecolor="none",
            markeredgecolor="0.75", markersize=6, label=empty_label)],
            loc="upper left", bbox_to_anchor=(0, -0.30), frameon=False,
            fontsize=fontsize, handletextpad=0.4, borderpad=0.0)
    return {"sel_kosong": kosong, "sel_total": counts.size}


def panel_letter(ax, letter, case="lower", dx=-14, dy=6, fontsize=None,
                 above_title=True):
    """Huruf panel: tebal, kiri atas, DI LUAR kotak sumbu, dan di atas judul.

    Menempatkan huruf secara manual di koordinat figure hampir selalu berakhir
    menabrak judul panel atau keluar kanvas. Helper ini memakai offset points
    dari sudut kiri-atas axes, dan bila panel punya judul, huruf dinaikkan
    setinggi judul tersebut.

    case: "lower" -> a, b, c ; "upper" -> A, B, C (ikuti konvensi jurnal).
    """
    letter = letter.upper() if case == "upper" else letter.lower()
    # Ditandai supaya `panel_crops` dapat memberi nama kotak potongnya.
    ax._vizkit_letter = letter
    off_y = dy
    has_title = any(ax.get_title(loc=l) for l in ("left", "center", "right"))
    if above_title and has_title:
        # Tinggi judul diukur dari selisih tight bbox terhadap kotak sumbu:
        # dengan judul rata kiri (default gaya ini) ax.title adalah slot TENGAH
        # yang kosong, sehingga mengukurnya langsung selalu memberi nol.
        ax.figure.canvas.draw()
        r = ax.figure.canvas.get_renderer()
        extra_px = ax.get_tightbbox(r).y1 - ax.bbox.y1
        off_y += max(extra_px, 0.0) * 72.0 / ax.figure.dpi + 1.5
    return ax.annotate(letter, xy=(0, 1), xycoords="axes fraction",
                       xytext=(dx, off_y), textcoords="offset points",
                       fontweight="bold",
                       fontsize=fontsize or mpl.rcParams["font.size"] + 2,
                       va="bottom", ha="left", annotation_clip=False)


# Palet bawaan SmartPLS: lingkaran konstruk biru, persegi indikator kuning.
SMARTPLS_CONSTRUCT = "#4A7EBB"
SMARTPLS_INDICATOR = "#FFD966"


def pls_path_diagram(ax, constructs, paths, indicators=None, r2=None,
                     positions=None, hue="#0072B2", box_w=0.20, box_h=0.10,
                     ind_w=0.15, ind_h=0.052, sig_alpha=0.05,
                     path_fmt="{:.3f}", show_ns=True, style="journal",
                     mode="reflective", fontsize=None):
    """Diagram jalur PLS-SEM (setara tampilan SmartPLS), digambar sebagai figur.

    Tangkapan layar SmartPLS adalah figur yang paling sering ditolak reviewer:
    resolusinya rendah, fontnya tidak dapat diatur, dan angkanya tidak terbaca
    setelah diperkecil ke lebar kolom. Helper ini menggambar ulang model dari
    ANGKA HASIL ESTIMASI, sehingga figur dapat direproduksi dan lolos syarat
    resolusi.

    constructs : {nama: label} konstruk laten (kotak/oval)
    paths      : {(dari, ke): {"beta": .., "p": .., "t": ..}} jalur struktural
    indicators : {nama_konstruk: [(label_indikator, loading), ...]} opsional
    r2         : {nama_konstruk: nilai R^2} -> ditulis di dalam kotak
    positions  : {nama: (x, y)} 0-1; bila None, disusun otomatis kiri->kanan
                 menurut kedalaman topologis (eksogen di kiri, endogen di kanan)

    style : "journal" (bawaan) — kotak putih bergaris hue, mengikuti aturan
                figur naskah; atau "smartpls" — lingkaran biru + persegi
                indikator kuning, meniru tampilan SmartPLS agar pembaca yang
                terbiasa dengan perangkat itu langsung mengenalinya. Keduanya
                digambar ulang dari angka estimasi, jadi resolusinya benar dan
                fontnya mengikuti ladder skill ini. Catatan: kuning SmartPLS
                berkontras rendah terhadap putih dan tidak ideal untuk cetak
                hitam-putih; pakai "journal" bila jurnal target mencetak
                grayscale.
    mode  : "reflective" (panah konstruk -> indikator) atau "formative"
            (indikator -> konstruk). Ini klaim pengukuran, bukan selera: salah
            arah berarti salah model. Boleh berupa dict {konstruk: mode}.

    Jalur tidak signifikan digambar putus-putus dan tipis, bukan dihapus:
    hipotesis yang tidak didukung adalah hasil (aturan 2.4).
    """
    if style not in ("journal", "smartpls"):
        raise ValueError('style harus "journal" atau "smartpls"')
    smart = style == "smartpls"
    if smart:
        hue = SMARTPLS_CONSTRUCT
    fontsize = fontsize or mpl.rcParams["legend.fontsize"]

    # Tata letak otomatis: kedalaman = panjang rantai terpanjang menuju simpul.
    if positions is None:
        masuk = {k: [] for k in constructs}
        for (a, b) in paths:
            if a not in constructs or b not in constructs:
                raise KeyError(f"jalur ({a} -> {b}) memuat konstruk tak dikenal")
            masuk[b].append(a)
        depth, seen = {}, set()

        def _d(n, stack=()):
            if n in stack:
                raise ValueError(f"model memuat siklus pada '{n}'")
            if n in depth:
                return depth[n]
            depth[n] = 0 if not masuk[n] else 1 + max(
                _d(m, stack + (n,)) for m in masuk[n])
            return depth[n]

        for k in constructs:
            _d(k)
        kolom = {}
        for k, d in depth.items():
            kolom.setdefault(d, []).append(k)
        maxd = max(kolom) if kolom else 0
        # Kolom pertama/terakhir diberi ruang bagi indikatornya bila ada.
        kiri = 0.36 if (indicators and any(
            depth.get(k, 0) == 0 for k in indicators)) else 0.12
        kanan = 0.64 if (indicators and any(
            depth.get(k, 0) == maxd for k in indicators)) else 0.88
        # Rantai lurus (satu konstruk per kolom) diselang-seling naik-turun.
        # Bila semua kotak sejajar pada satu garis horizontal, jalur yang
        # melompati kolom menembus kotak di antaranya dan labelnya jatuh di
        # dalam kotak — persis kasus model TAM/UTAUT yang berbentuk rantai.
        rantai = all(len(ks) == 1 for ks in kolom.values()) and maxd >= 2
        positions = {}
        for d, ks in kolom.items():
            x = (kiri + kanan) / 2 if maxd == 0 else kiri + (kanan - kiri) * d / maxd
            for j, k in enumerate(sorted(ks)):
                if rantai:
                    y = 0.62 if d % 2 == 0 else 0.36
                elif len(ks) == 1:
                    y = 0.5
                else:
                    y = 0.86 - 0.72 * j / (len(ks) - 1)
                positions[k] = (x, y)

    # Lebar kotak diciutkan bila kolom rapat: dengan banyak kolom, box_w
    # bawaan membuat kotak bertetangga saling tumpang tindih.
    xs_uniq = sorted({round(px, 4) for px, _ in positions.values()})
    if len(xs_uniq) > 1:
        jarak = min(b - a for a, b in zip(xs_uniq, xs_uniq[1:]))
        box_w = min(box_w, jarak * 0.66)
    if smart and len(xs_uniq) > 1:
        # Lingkaran gaya SmartPLS memuai mengikuti teksnya (di bawah), sehingga
        # kolom perlu direnggangkan lebih dulu — kalau tidak, lingkaran
        # bertetangga saling bersentuhan dan label jalur jatuh di tepinya.
        pusat = sum(xs_uniq) / len(xs_uniq)
        positions = {k: (pusat + (px - pusat) * 1.34, py)
                     for k, (px, py) in positions.items()}
        xs_uniq = sorted({round(px, 4) for px, _ in positions.values()})
    if smart:
        # Lingkaran hanya menyediakan ~70% lebarnya sebagai ruang teks pada
        # baris terlebar (tali busur memendek menjauhi pusat), jadi diameternya
        # DIUKUR dari label terpanjang. Memakai box_w apa adanya membuat nama
        # konstruk dan R² terpotong di tepi lingkaran.
        ax.figure.canvas.draw()
        rr = ax.figure.canvas.get_renderer()
        butuh = 0.0
        for k, lab in constructs.items():
            teks = lab if r2 is None or k not in r2 else f"{lab}\nR² = {r2[k]:.3f}"
            probe = ax.text(0.5, -9e9, teks, fontsize=fontsize)
            w_ax = probe.get_window_extent(rr).width / max(ax.bbox.width, 1e-9)
            probe.remove()
            butuh = max(butuh, w_ax)
        box_w = max(box_w, butuh / 0.70)
        box_h = box_w      # jangkauan panah simetris untuk bentuk lingkaran

        # Setelah diameter membesar, kolom terluar bisa melewati tepi axes.
        # Posisi dirapatkan ke pusat secukupnya agar setiap lingkaran muat —
        # tanpa ini lingkaran pertama/terakhir terpotong spine.
        xs2 = sorted({round(px, 4) for px, _ in positions.values()})
        lo_x, hi_x = xs2[0] - box_w / 2, xs2[-1] + box_w / 2
        if lo_x < 0.01 or hi_x > 0.99:
            pusat2 = (xs2[0] + xs2[-1]) / 2
            rentang = max(hi_x - lo_x, 1e-9)
            skala = min(1.0, 0.98 / rentang)
            positions = {k: (pusat2 + (px - pusat2) * skala, py)
                         for k, (px, py) in positions.items()}
            xs2 = sorted({round(px, 4) for px, _ in positions.values()})
            geser = 0.0
            if xs2[0] - box_w / 2 < 0.01:
                geser = 0.01 - (xs2[0] - box_w / 2)
            elif xs2[-1] + box_w / 2 > 0.99:
                geser = 0.99 - (xs2[-1] + box_w / 2)
            if geser:
                positions = {k: (px + geser, py)
                             for k, (px, py) in positions.items()}

    # Rasio aspek axes dipakai agar "lingkaran" benar-benar bulat: sumbu 0-1
    # pada panel yang tidak persegi membuat lingkaran data tampak lonjong.
    ax.figure.canvas.draw()
    bbp = ax.get_position()
    fw, fh = ax.figure.get_size_inches()
    aspek = (bbp.width * fw) / max(bbp.height * fh, 1e-9)

    # Bentuk konstruk
    for k, lab in constructs.items():
        x, y = positions[k]
        if smart:
            ax.add_patch(Ellipse((x, y), box_w, box_w * aspek,
                                 facecolor=SMARTPLS_CONSTRUCT,
                                 edgecolor="#2F5F94", lw=0.9, zorder=4))
        else:
            ax.add_patch(mpl.patches.FancyBboxPatch(
                (x - box_w / 2, y - box_h / 2), box_w, box_h,
                boxstyle="round,pad=0.008", facecolor="white", edgecolor=hue,
                lw=1.0, zorder=4))
        teks = lab if r2 is None or k not in r2 else f"{lab}\nR² = {r2[k]:.3f}"
        ax.text(x, y, teks, ha="center", va="center", fontsize=fontsize,
                color="white" if smart else INK, zorder=5)

    # Indikator (persegi) di sisi luar konstruknya
    if indicators:
        for k, items in indicators.items():
            if k not in positions:
                raise KeyError(f"indikator untuk konstruk tak dikenal: {k}")
            x, y = positions[k]
            kiri = x <= 0.5
            # Jarak indikator-konstruk harus memuat label loading di antaranya;
            # 0,10 terlalu pendek dan labelnya terdorong ke dalam kotak.
            jarak_ind = 0.16
            sx = x - box_w / 2 - jarak_ind if kiri else x + box_w / 2 + jarak_ind
            n = len(items)
            for j, (ilab, load) in enumerate(items):
                iy = y + (n - 1) / 2 * (ind_h + 0.018) - j * (ind_h + 0.018)
                ax.add_patch(mpl.patches.Rectangle(
                    (sx - ind_w / 2, iy - ind_h / 2), ind_w, ind_h,
                    facecolor=SMARTPLS_INDICATOR if smart else "white",
                    edgecolor="#BF9000" if smart else COMPARATOR,
                    lw=0.7, zorder=4))
                ax.text(sx, iy, ilab, ha="center", va="center",
                        fontsize=fontsize * 0.85, zorder=5)
                x0 = sx + ind_w / 2 if kiri else sx - ind_w / 2
                x1 = x - box_w / 2 if kiri else x + box_w / 2
                # Arah panah = klaim pengukuran. Reflektif: konstruk menyebabkan
                # indikator (panah keluar dari konstruk). Formatif: sebaliknya.
                m_k = mode.get(k, "reflective") if isinstance(mode, dict) else mode
                if m_k not in ("reflective", "formative"):
                    raise ValueError(f'mode "{m_k}" tidak dikenal untuk {k}')
                ekor, kepala = ((x1, y), (x0, iy)) if m_k == "reflective" \
                    else ((x0, iy), (x1, y))
                ax.annotate("", xy=kepala, xytext=ekor,
                            arrowprops=dict(arrowstyle="->",
                                            color="#8C6D00" if smart else COMPARATOR,
                                            lw=0.6, shrinkA=0, shrinkB=0),
                            zorder=3)
                # Loading ditaruh dekat UJUNG INDIKATOR panah (t=0,28 dari sisi
                # indikator), bukan titik tengah: titik tengah panah jatuh di
                # dalam kotak konstruk ketika indikatornya banyak dan panahnya
                # miring. Rata teks mengikuti sisi agar menjauhi konstruk.
                t_ = 0.50
                ax.text(x0 + (x1 - x0) * t_, iy + (y - iy) * t_ + 0.008,
                        f"{load:.2f}", fontsize=fontsize * 0.8, color=MUTE,
                        ha="center", va="bottom",
                        bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.5),
                        zorder=5)

    # Jalur struktural
    ringkas = {"signifikan": [], "tidak_signifikan": []}
    _label_jalur = []
    for (a, b), st in paths.items():
        xa, ya = positions[a]
        xb, yb = positions[b]
        beta = st["beta"]
        pv = st.get("p")
        sig = (pv is not None and pv < sig_alpha)
        (ringkas["signifikan"] if sig else ringkas["tidak_signifikan"]).append(
            (a, b))
        if not sig and not show_ns:
            continue
        dx, dy = xb - xa, yb - ya
        norm = math.hypot(dx, dy) or 1.0
        sh = box_w / 2 * abs(dx) / norm + box_h / 2 * abs(dy) / norm
        ax.annotate("", xy=(xb - dx / norm * sh, yb - dy / norm * sh),
                    xytext=(xa + dx / norm * sh, ya + dy / norm * sh),
                    arrowprops=dict(arrowstyle="-|>",
                                    color=hue if sig else COMPARATOR,
                                    lw=1.3 if sig else 0.7,
                                    ls="-" if sig else (0, (3, 2)),
                                    shrinkA=0, shrinkB=0),
                    zorder=3)
        lab = path_fmt.format(beta)
        if pv is not None:
            lab += "  " + (sig_stars(pv) if sig else "n.s.")
        # Label ditaruh di titik 0,42 sepanjang jalur (bukan tepat di tengah)
        # dan digeser tegak lurus arah panah. Titik tengah dua jalur yang
        # berbagi satu konstruk sering berimpit dengan kotak konstruk ketiga.
        px, py = -dy / norm, dx / norm
        if py < 0:
            px, py = -px, -py
        # Posisi label sepanjang jalur dicoba dari tengah lalu bergeser: dua
        # jalur yang bertemu di satu konstruk punya titik tengah berdekatan,
        # sehingga label pada t tetap saling menabrak.
        txt = None
        for t_ in (0.50, 0.38, 0.62, 0.30, 0.70):
            if txt is not None:
                txt.remove()
            txt = ax.text(xa + dx * t_ + px * 0.045, ya + dy * t_ + py * 0.045,
                          lab, ha="center", va="center", fontsize=fontsize * 0.9,
                          color=hue if sig else MUTE,
                          bbox=dict(fc="white", ec="none", alpha=0.88, pad=0.8),
                          zorder=6)
            ax.figure.canvas.draw()
            rr = ax.figure.canvas.get_renderer()
            bb = txt.get_window_extent(rr)
            if not any(bb.overlaps(o.get_window_extent(rr))
                       for o in _label_jalur):
                break
        _label_jalur.append(txt)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    return ringkas


# --------------------------------------------- komposisi figur multi-panel

def panel_grid(specs, width="double", row_heights_mm=None, ncol=12,
               hspace=None, wspace=None, letter_case="lower", dx=-14, dy=6):
    """Bangun figur multi-panel dari kerangka panel, lalu bubuhi huruf panel.

    specs : list dict, satu per panel, dengan kunci:
        letter  — huruf panel ("a", "b", ...)
        row     — indeks baris (0-based)
        col     — kolom awal pada grid `ncol` kolom (0-based)
        colspan — lebar dalam kolom grid (bawaan: sisa baris)
        rowspan — tinggi dalam baris (bawaan 1)
        projection — opsional, mis. "3d" atau "polar"
    row_heights_mm : tinggi setiap baris dalam mm. Wajib — tinggi baris adalah
        keputusan desain (panel skema lebih pendek daripada panel data), bukan
        sesuatu yang pantas ditebak seragam.

    Grid 12 kolom memberi keleluasaan colspan (½, ⅓, ¼, 7/12 dan seterusnya)
    tanpa mengubah lebar figur.

    Mengembalikan (fig, axes) dengan `axes` dict huruf -> Axes.

    Aturan urutan panel (aturan-figur 7.1-7.2): panel **a** adalah kail —
    skema/hero yang mengasumsikan pembaca tanpa konteks; panel **b** memikul
    klaim figur, yaitu grafik yang sendirian membuat kalimat klaim benar;
    sisanya bukti, diurutkan menurut seberapa kuat ia menopang b.
    """
    if not specs:
        raise ValueError("specs kosong")
    if row_heights_mm is None:
        raise ValueError("row_heights_mm wajib: tinggi baris adalah keputusan "
                         "desain, bukan nilai bawaan yang aman")
    # Catatan satuan: COL_SINGLE/COL_DOUBLE sudah dalam INCI (mm x MM), jadi
    # tidak boleh dikali MM lagi. `width` numerik diperlakukan sebagai mm,
    # sejalan dengan row_heights_mm.
    lebar_in = {"single": COL_SINGLE, "double": COL_DOUBLE}.get(width)
    if lebar_in is None:
        if not isinstance(width, (int, float)):
            raise ValueError('width harus "single", "double", atau lebar mm')
        lebar_in = float(width) * MM

    nrow = len(row_heights_mm)
    for s in specs:
        if not 0 <= s["row"] < nrow:
            raise ValueError(f'panel {s["letter"]}: row={s["row"]} di luar '
                             f'{nrow} baris pada row_heights_mm')
        if s["col"] + s.get("colspan", ncol - s["col"]) > ncol:
            raise ValueError(f'panel {s["letter"]}: col+colspan melewati '
                             f'{ncol} kolom')
    huruf = [s["letter"] for s in specs]
    if len(set(huruf)) != len(huruf):
        raise ValueError(f"huruf panel duplikat: {huruf}")

    total_in = sum(row_heights_mm) * MM
    fig = plt.figure(figsize=(lebar_in, total_in), constrained_layout=True)
    gs = fig.add_gridspec(nrow, ncol, height_ratios=row_heights_mm,
                          hspace=hspace, wspace=wspace)
    axes = {}
    for s in specs:
        r0, r1 = s["row"], s["row"] + s.get("rowspan", 1)
        c0 = s["col"]
        c1 = c0 + s.get("colspan", ncol - c0)
        kw = {"projection": s["projection"]} if s.get("projection") else {}
        ax = fig.add_subplot(gs[r0:r1, c0:c1], **kw)
        axes[s["letter"]] = ax
    for s in specs:
        panel_letter(axes[s["letter"]], s["letter"], case=letter_case,
                     dx=dx, dy=dy)

    # Tinggi baris disimpan agar `check_layout` dapat menyebut baris penyebab
    # bila axes menciut. Pemeriksaan TIDAK dilakukan di sini: pada titik ini
    # panel masih kosong, sedangkan constrained_layout menghitung dari isinya.
    fig._vizkit_row_heights = list(row_heights_mm)
    return fig, axes


def check_layout(fig, name="figur"):
    """Pastikan constrained_layout benar-benar diterapkan setelah menggambar.

    Bila tinggi baris tidak cukup untuk label dan judul panelnya, matplotlib
    menciutkan axes ke nol dan hanya memberi UserWarning — mudah terlewat,
    padahal figurnya rusak. Panggil ini SETELAH semua panel digambar dan
    SEBELUM `save_figure`; ia mengembalikan True bila tata letak sehat dan
    melempar ValueError yang menyebut baris tersempit bila tidak.
    """
    with warnings.catch_warnings(record=True) as tercatat:
        warnings.simplefilter("always")
        fig.canvas.draw()
        ciut = [w for w in tercatat if "collapsed to zero" in str(w.message)]
    if ciut:
        tinggi = getattr(fig, "_vizkit_row_heights", None)
        petunjuk = ""
        if tinggi:
            sempit = sorted(enumerate(tinggi), key=lambda t: t[1])[:2]
            petunjuk = (" Baris tersempit (indeks, mm): "
                        + ", ".join(f"({i}, {h:g})" for i, h in sempit) + ".")
        raise ValueError(
            f"[{name}] tata letak gagal: axes menciut ke nol — tinggi baris "
            f"tidak cukup untuk label dan judul panelnya.{petunjuk} "
            "Naikkan row_heights_mm, atau kurangi dekorasi panel.")
    return True


def panel_crops(fig, pad_px=6):
    """Kotak potong (0-1, koordinat gambar) setiap panel untuk cek perseptual.

    Cek geometris (`check_overlaps`) tidak menangkap label berkontras rendah,
    garis penunjuk yang menyilang, atau warna seri yang tertukar. Simpan PNG,
    lalu potong dan LIHAT tiap panel:

        paths = save_figure(fig, "fig2")
        for huruf, box in panel_crops(fig).items():
            host.view_image(paths[-1], crop=box)

    Kotak diambil dari tight bbox tiap axes (termasuk label dan judulnya),
    dinormalkan terhadap ukuran kanvas.
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    out = {}
    for i, ax in enumerate(fig.axes):
        if getattr(ax, "_vizkit_colorbar", False):
            continue
        try:
            bb = ax.get_tightbbox(r)
        except Exception:                                 # noqa: BLE001
            bb = ax.bbox
        if bb is None:
            continue
        # Nama kunci: huruf panel bila ada, kalau tidak indeks axes.
        nama = getattr(ax, "_vizkit_letter", None) or f"ax{i}"
        x0 = max((bb.x0 - pad_px) / W, 0.0)
        x1 = min((bb.x1 + pad_px) / W, 1.0)
        # Koordinat crop dihitung dari ATAS gambar (konvensi pustaka gambar),
        # sedangkan bbox matplotlib dari bawah — karena itu dibalik.
        y0 = max(1.0 - (bb.y1 + pad_px) / H, 0.0)
        y1 = min(1.0 - (bb.y0 - pad_px) / H, 1.0)
        out[nama] = (x0, y0, x1, y1)
    return out


def check_overlaps(fig, name="figure", verbose=True):
    """Cek geometris: teks bertumpang, teks menabrak spine, teks keluar kanvas.

    Kembalikan dict temuan. Ini BUKAN pengganti melihat gambarnya — label
    berkontras rendah, penunjuk yang menyilang, dan warna yang tertukar hanya
    tertangkap mata (aturan 9.2).
    """
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    # Peta ticklabel -> axes pemiliknya, termasuk axes colorbar (Text.axes tidak
    # terisi di sana). Ticklabel di luar rentang sumbunya tetap ada sebagai
    # objek Text meski tidak tergambar; memasukkannya menghasilkan lapor palsu.
    tick_owner, tick_live = {}, set()
    for ax in fig.axes:
        for axis, lim in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            lo, hi = sorted(lim)
            locs = list(axis.get_majorticklocs()) + list(axis.get_minorticklocs())
            labs = (list(axis.get_majorticklabels()) +
                    list(axis.get_minorticklabels()))
            for loc, lab in zip(locs, labs):
                tick_owner[lab] = ax
                if lo - 1e-9 <= loc <= hi + 1e-9:
                    tick_live.add(lab)

    def _live(t):
        if not (t.get_text().strip() and t.get_visible()):
            return False
        ax = tick_owner.get(t)
        if ax is None:
            return True
        # tick di luar rentang sumbu tetap ada sebagai objek Text meski tidak
        # tergambar; memasukkannya menghasilkan lapor palsu
        return ax.axison and t in tick_live

    texts = [(t, t.get_window_extent(r)) for t in fig.findobj(mpl.text.Text)
             if _live(t)]
    spines = [(s, s.get_window_extent(r)) for ax in fig.axes
              for s in ax.spines.values() if s.get_visible()]
    ticks = {ax: {t for t, a in tick_owner.items() if a is ax} for ax in fig.axes}
    tt = [(a.get_text(), b.get_text())
          for i, (a, ba) in enumerate(texts)
          for b, bb in texts[i + 1:] if ba.overlaps(bb)]
    ts = [(t.get_text(), s.axes.get_label() or "axes")
          for t, bt in texts for s, bs in spines
          if bt.overlaps(bs) and t not in ticks.get(s.axes, ())]
    # Teks yang melewati kanvas: TERPOTONG bila figur disimpan apa adanya, tapi
    # AMAN bila savefig memakai bbox_inches="tight" (kanvas diperluas saat
    # menyimpan). Konsekuensinya berbeda, jadi dilaporkan sebagai dua kategori:
    # dengan tight, meluber hanya berarti lebar fisik figur bertambah dari yang
    # dirancang — figcheck.py yang menangkap dampaknya pada dpi efektif.
    pad = 0.5
    fb = fig.bbox
    lubar = [t.get_text() for t, bt in texts
             if bt.x0 < fb.x0 - pad or bt.y0 < fb.y0 - pad
             or bt.x1 > fb.x1 + pad or bt.y1 > fb.y1 + pad]
    tight = str(mpl.rcParams.get("savefig.bbox", "")) == "tight"
    out = [] if tight else lubar
    res = {"teks_bertumpang": tt, "teks_menabrak_spine": ts,
           "teks_keluar_kanvas": out}
    if verbose:
        total = sum(len(v) for v in res.values())
        if total == 0:
            print(f"[{name}] cek geometris bersih")
        else:
            for k, v in res.items():
                if v:
                    print(f"[{name}] {k}: {v[:8]}{' …' if len(v) > 8 else ''}")
        if tight and lubar:
            print(f"[{name}] catatan: {len(lubar)} teks melewati kanvas tapi "
                  f"aman karena savefig bbox='tight' — kanvas melebar saat "
                  f"disimpan, jadi periksa lebar akhirnya dengan figcheck.py")
    return res


def cvd_check(colors, kind="deuteranopia"):
    """Simulasi buta warna kasar (Brettel/Viénot) + jarak minimum antar warna.

    Kembalikan (warna_tersimulasi, jarak_minimum). Jarak < ~0.10 berarti dua
    warna berisiko tertukar; ganti salah satunya. Ini pemeriksaan cepat, bukan
    pengganti perkakas simulasi khusus.
    """
    M = {
        "deuteranopia": np.array([[0.625, 0.375, 0.0],
                                  [0.70, 0.30, 0.0],
                                  [0.0, 0.30, 0.70]]),
        "protanopia": np.array([[0.567, 0.433, 0.0],
                                [0.558, 0.442, 0.0],
                                [0.0, 0.242, 0.758]]),
        "tritanopia": np.array([[0.95, 0.05, 0.0],
                                [0.0, 0.433, 0.567],
                                [0.0, 0.475, 0.525]]),
    }[kind]
    rgb = np.array([mpl.colors.to_rgb(c) for c in colors])
    sim = np.clip(rgb @ M.T, 0, 1)
    d = np.inf
    for i in range(len(sim)):
        for j in range(i + 1, len(sim)):
            d = min(d, float(np.linalg.norm(sim[i] - sim[j])))
    return [mpl.colors.to_hex(c) for c in sim], (d if np.isfinite(d) else None)

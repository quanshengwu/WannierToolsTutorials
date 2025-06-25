#!/usr/bin/env python3
# Author: Yuzhi Wang
# Email: yuzhiwang@iphy.ac.cn

import os
import re
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.core import Spin


def read_fermi(outcar="OUTCAR"):
    """Extract E‑fermi from OUTCAR, supporting “E‑fermi = x” and “E‑fermi : x”."""
    pattern = re.compile(r"E-fermi\s*[:=]\s*([-+]?\d*\.\d+|\d+)")
    with open(outcar) as f:
        for line in f:
            m = pattern.search(line)
            if m:
                return float(m.group(1))
    raise RuntimeError("Cannot find E-fermi in OUTCAR")


def read_band_dat(filename):
    """
    Read a band.dat–style file into a list of (k_array, energy_array).
    Bands separated by blank lines.
    """
    bands = []
    ks, es = [], []
    with open(filename) as f:
        for line in f:
            s = line.strip()
            if not s:
                if ks:
                    bands.append((np.array(ks), np.array(es)))
                    ks, es = [], []
            else:
                k, e = s.split()
                ks.append(float(k))
                es.append(float(e))
        if ks:
            bands.append((np.array(ks), np.array(es)))
    return bands


def mask_from_image(path, threshold=250):
    """Convert PNG to boolean mask by thresholding any channel < threshold."""
    img = np.array(Image.open(path).convert("RGB"))
    return np.any(img < threshold, axis=2)


def compute_jaccard(m1, m2):
    inter = np.logical_and(m1, m2).sum()
    union = np.logical_or(m1, m2).sum()
    return inter/union if union > 0 else 0.0


def compute_dice(m1, m2):
    inter = np.logical_and(m1, m2).sum()
    return 2*inter/(m1.sum()+m2.sum()) if (m1.sum()+m2.sum()) > 0 else 0.0


def plot_single(bs, bands_source, fermi, out_png, color, ls, ylim):
    """Plot one set of bands (DFT or Wannier) onto its own PNG."""
    fig, ax = plt.subplots(figsize=(6, 4))
    d = bs.distance
    # plot DFT
    if bands_source == "dft":
        for band in bs.bands[Spin.up]:
            ax.plot(d, band - bs.efermi, color=color, lw=1, linestyle=ls)
    else:  # "wan"
        # we pass wan_bands via bs._user_wan in this case
        for k_arr, e_arr in bs._user_wan:
            ax.plot(k_arr, e_arr, color=color, lw=1, linestyle=ls)
    # high-symmetry markers
    xt, xl = [], []
    for br in bs.branches:
        i = br["start_index"]
        name = br["name"].split("-")[0]
        xt.append(d[i])
        xl.append(name)
        ax.axvline(d[i], color="k", ls="--", lw=0.5)
    last = bs.branches[-1]
    ie = last["end_index"]
    ne = last["name"].split("-")[1]
    xt.append(d[ie])
    xl.append(ne)
    ax.axvline(d[ie], color="k", ls="--", lw=0.5)

    ax.set_xticks(xt)
    ax.set_xticklabels(xl)
    ax.set_xlabel("K‑point path")
    ax.set_ylabel("Energy (E–E$_F$) (eV)")
    ax.axhline(0, color="k", lw=1)
    ax.set_ylim(*ylim)
    ax.set_xlim(d[0], d[-1])
    plt.tight_layout()
    fig.savefig(out_png, dpi=300)
    plt.close(fig)


def main():
    # assume current dir has band/vasprun.xml, OUTCAR; and wan/wannier90_band.dat
    e_fermi = read_fermi("OUTCAR")
    e_fermi_band = read_fermi("band/OUTCAR")

    vasprun = Vasprun("band/vasprun.xml")
    bs = vasprun.get_band_structure(line_mode=True)

    # DFT_band.dat
    os.makedirs("band", exist_ok=True)
    with open("band/DFT_band.dat", "w") as fout:
        for band in bs.bands[Spin.up]:
            for x, e in zip(bs.distance, band - bs.efermi):
                fout.write(f"{x:.6f} {e:.6f}\n")
            fout.write("\n")

    # read wannier bands and attach to bs for convenience
    wan = read_band_dat("wan/wannier90_band.dat")
    wan = [(k, e - e_fermi_band) for k, e in wan]
    bs._user_wan = wan

    os.makedirs("plots", exist_ok=True)

    # plot individual PNGs
    plot_single(bs, "dft", e_fermi, "plots/dft.png",
                color="blue", ls="-",  ylim=(-3, 3))
    plot_single(bs, "wan", e_fermi, "plots/wan.png",
                color="red",  ls="-", ylim=(-3, 3))

    # compute pixel overlap
    m1 = mask_from_image("plots/dft.png")
    m2 = mask_from_image("plots/wan.png")
    j = compute_jaccard(m1, m2)
    d = compute_dice(m1, m2)
    print(f"Jaccard: {j:.4f}, Dice: {d:.4f}")

    # combined PDF
    fig, ax = plt.subplots(figsize=(6, 4))
    # DFT
    for band in bs.bands[Spin.up]:
        ax.plot(bs.distance, band - bs.efermi, color="blue", lw=1)
    # Wannier
    for k_arr, e_arr in wan:
        ax.plot(k_arr, e_arr, color="red", lw=1, linestyle="--")
    # markers
    xt, xl = [], []
    for br in bs.branches:
        i = br["start_index"]
        xt.append(bs.distance[i])
        xl.append(br["name"].split("-")[0])
        ax.axvline(bs.distance[i], color="k", ls="--", lw=0.5)
    ie = bs.branches[-1]["end_index"]
    xt.append(bs.distance[ie])
    xl.append(bs.branches[-1]["name"].split("-")[1])
    ax.axvline(bs.distance[ie], color="k", ls="--", lw=0.5)

    ax.set_xticks(xt)
    ax.set_xticklabels(xl)
    ax.set_xlabel("K‑point path")
    ax.set_ylabel("Energy (E–E$_F$) (eV)")
    ax.axhline(0, color="k", lw=1)
    ax.set_ylim(-6, 6)
    ax.set_xlim(bs.distance[0], bs.distance[-1])
    plt.tight_layout()
    fig.savefig("plots/combined.pdf")
#    plt.show()


if __name__ == "__main__":
    main()

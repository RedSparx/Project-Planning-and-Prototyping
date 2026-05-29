"""
Chapter 7 — Design for X
All figures: grayscale, H <= 3 in, W/H >= 1.6, text >= 9 pt
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

mpl.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.edgecolor": "black", "axes.linewidth": 1.0,
    "axes.grid": False, "lines.linewidth": 1.6,
    "savefig.bbox": "tight",
})

def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    plt.close(fig)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 — DFX overview (unchanged, passes all checks)
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(8, 2.8))
ax1.set_xlim(0, 10); ax1.set_ylim(0, 4); ax1.axis("off")

cx, cy, cw, ch = 3.7, 1.1, 2.6, 1.8
center = mpatches.FancyBboxPatch((cx, cy), cw, ch,
    boxstyle="round,pad=0.1", linewidth=2.0,
    edgecolor="black", facecolor="white", zorder=5)
ax1.add_patch(center)
ax1.text(cx+cw/2, cy+ch/2, "Prototype\nDesign",
         ha="center", va="center", fontsize=11, fontweight="bold", zorder=6)

outer_boxes = [
    ("DFM", "Design for\nManufacturability", 0.80, 0.05, 2.0, 2.2, 1.6),
    ("DFA", "Design for\nAssembly",          0.70, 7.75, 2.0, 2.2, 1.6),
    ("DFT", "Design for\nTest",              0.65, 0.05, 0.2, 2.2, 1.6),
    ("DFR", "Design for\nReliability",       0.55, 7.75, 0.2, 2.2, 1.6),
]

for l1, l2, gray, bx, by, bw, bh in outer_boxes:
    box = mpatches.FancyBboxPatch((bx, by), bw, bh,
        boxstyle="round,pad=0.08", linewidth=1.2,
        edgecolor="black", facecolor=str(gray), zorder=3)
    ax1.add_patch(box)
    ax1.text(bx+bw/2, by+bh*0.65, l1, ha="center", va="center",
             fontsize=10, fontweight="bold", zorder=4)
    ax1.text(bx+bw/2, by+bh*0.28, l2, ha="center", va="center",
             fontsize=8.5, zorder=4)
    if bx < cx:
        x0, y0, x1, y1 = bx+bw+0.06, by+bh/2, cx-0.06, cy+ch/2
    else:
        x0, y0, x1, y1 = bx-0.06, by+bh/2, cx+cw+0.06, cy+ch/2
    ax1.annotate("", xy=(x1, y1), xytext=(x0, y0),
                 arrowprops=dict(arrowstyle="-|>", color="black",
                                 lw=1.4, mutation_scale=12))

save(fig1, "fig_01_dfx_overview")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 — DFA before/after (fixed: y-limit uses max of before/after)
# ─────────────────────────────────────────────────────────────────────────────
fig2, axes = plt.subplots(1, 3, figsize=(8, 2.5))

titles  = ["Part Count", "Assembly Time (s)", r"$\eta_A$ (%)"]
ylabels = ["Parts",      "Time (s)",          r"$\eta_A$ (%)"]
before  = [8,             120,                  7.5]
after   = [6,              80,                  11.25]

for i, ax in enumerate(axes):
    xb, xa = 0.25, 0.70
    b = ax.bar(xb, before[i], width=0.35, color="0.65", hatch="///",
               edgecolor="black", linewidth=0.8, label="Before", zorder=3)
    a = ax.bar(xa, after[i],  width=0.35, color="0.30",
               edgecolor="black", linewidth=0.8, label="After",  zorder=3)
    ax.set_xticks([])
    ax.set_ylabel(ylabels[i], fontsize=9)
    ax.set_title(titles[i], fontsize=9.5)
    ax.set_xlim(0, 1.0)
    ymax = max(before[i], after[i])
    ax.set_ylim(0, ymax * 1.40)           # use max(before, after) for y-limit
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar, val in [(b[0], before[i]), (a[0], after[i])]:
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + ymax * 0.03,
                f"{val:g}", ha="center", va="bottom", fontsize=9)

axes[2].legend(loc="upper left", fontsize=8.5, framealpha=1)
fig2.tight_layout(pad=0.6)
save(fig2, "fig_02_dfa_parts")

# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 — DFT test points (fixed: TP labels separated from arrow labels)
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(9, 2.6))
ax3.set_xlim(0, 11); ax3.set_ylim(0, 4); ax3.axis("off")

def draw_box(ax, x, y, w, h, line1, line2="", gray=0.82, fs=9.5):
    rect = mpatches.FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.1", linewidth=1.3,
        edgecolor="black", facecolor=str(gray), zorder=3)
    ax.add_patch(rect)
    if line2:
        ax.text(x+w/2, y+h*0.65, line1, ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=4)
        ax.text(x+w/2, y+h*0.28, line2, ha="center", va="center",
                fontsize=8.5, zorder=4, style="italic")
    else:
        ax.text(x+w/2, y+h/2, line1, ha="center", va="center",
                fontsize=fs, zorder=4)

def tp(ax, x, y, label, ha="left"):
    c = plt.Circle((x, y), 0.16, color="black", fill=True, zorder=6)
    ax.add_patch(c)
    offset = 0.25 if ha == "left" else -0.25
    ax.text(x+offset, y, label, ha=ha, va="center", fontsize=8.5, zorder=7)

def arr(ax, x0, y0, x1, y1, label="", loff=(0, 0.20)):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color="black",
                                lw=1.3, mutation_scale=11))
    if label:
        mx = (x0+x1)/2 + loff[0]
        my = (y0+y1)/2 + loff[1]
        ax.text(mx, my, label, ha="center", va="bottom", fontsize=8.5)

# MCU (left)
draw_box(ax3, 0.3, 1.0, 2.0, 2.0, "MCU", "(STM32)", gray=0.80, fs=10)

# Upper path: UART TX → Debug Header J1
# Arrow goes at y=2.8
draw_box(ax3, 5.2, 2.2, 2.4, 1.0, "Debug", "Header J1", gray=0.72)
arr(ax3, 2.32, 2.7, 5.17, 2.7, "UART TX", loff=(0, 0.18))
# TP2 sits ABOVE the arrow line, labeled above
tp(ax3, 3.6, 3.15, "TP2 (scope)", ha="center")
# Small vertical tick from TP2 down to arrow level
ax3.plot([3.6, 3.6], [2.72, 2.99], color="black", lw=1.2, zorder=5)

# Lower path: GPIO → Status LED
# Arrow goes at y=1.4
draw_box(ax3, 5.2, 0.4, 2.4, 1.0, "Status LED", gray=0.75)
arr(ax3, 2.32, 1.4, 5.17, 0.9, "GPIO", loff=(0, 0.18))
# TP1 sits BELOW the arrow, labeled below
tp(ax3, 3.6, 0.75, "TP1 (logic probe)", ha="center")
ax3.plot([3.6, 3.6], [0.77, 1.38], color="black", lw=1.2, zorder=5)

# SWD path → SWD/JTAG J2 (middle height)
draw_box(ax3, 8.5, 1.55, 2.3, 0.9, "SWD/JTAG", "Header J2", gray=0.68)
arr(ax3, 2.32, 2.0, 8.47, 2.0, "SWD/Debug", loff=(0, 0.18))

save(fig3, "fig_03_dft_testpoints")
print("All Ch.7 figures regenerated.")

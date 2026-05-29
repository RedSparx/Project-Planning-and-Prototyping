"""
gen_figures.py
Generate all three figures for Chapter 4 of the LaTeX textbook.
Grayscale only, landscape orientation, figsize height <= 3.0 in.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np

# ── Global rcParams ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":        "sans-serif",
    "font.size":          11,
    "axes.titlesize":     11,
    "axes.labelsize":     10,
    "xtick.labelsize":    9,
    "ytick.labelsize":    9,
    "legend.fontsize":    9,
    "figure.dpi":         200,
    "savefig.dpi":        200,
    "savefig.bbox":       "tight",
    "savefig.pad_inches": 0.05,
    "text.color":         "black",
    "axes.edgecolor":     "black",
    "axes.labelcolor":    "black",
    "xtick.color":        "black",
    "ytick.color":        "black",
})

OUTDIR = "."   # script runs from its own directory

# ── Risk-band colour map (grayscale face values) ─────────────────────────────
def risk_gray(r):
    if r <= 4:
        return 0.85   # low
    elif r <= 9:
        return 0.55   # medium
    elif r <= 16:
        return 0.30   # high
    else:
        return 0.10   # critical


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIG 01 — 5×5 Risk Matrix
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def make_fig01():
    prob_labels = ["Rare (1)", "Unlikely (2)", "Possible (3)",
                   "Likely (4)", "Almost Certain (5)"]
    cons_labels = ["Negligible\n(1)", "Minor\n(2)", "Moderate\n(3)",
                   "Major\n(4)", "Catastrophic\n(5)"]

    fig, ax = plt.subplots(figsize=(7, 3.0))

    for pi in range(5):          # probability row  (0=Rare … 4=Almost Certain)
        p = pi + 1               # numeric 1–5
        for ci in range(5):      # consequence col  (0=Negligible … 4=Catastrophic)
            c = ci + 1
            r = p * c
            gray = risk_gray(r)
            # hatch pattern to aid differentiation for adjacent shades
            hatch = ""
            if r <= 4:
                hatch = ""
            elif r <= 9:
                hatch = ".."
            elif r <= 16:
                hatch = "///"
            else:
                hatch = "xxx"

            rect = mpatches.FancyBboxPatch(
                (ci - 0.5, pi - 0.5), 1.0, 1.0,
                boxstyle="square,pad=0",
                facecolor=str(gray),
                edgecolor="black",
                linewidth=0.6,
                hatch=hatch,
                zorder=1,
            )
            ax.add_patch(rect)

            # annotation text colour: white on dark cells, black on light cells
            txt_col = "white" if gray < 0.45 else "black"
            ax.text(ci, pi, str(r),
                    ha="center", va="center",
                    fontsize=8.5, fontweight="bold",
                    color=txt_col, zorder=2)

    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.set_xticks(range(5))
    ax.set_xticklabels(cons_labels, fontsize=8.5)
    ax.set_yticks(range(5))
    ax.set_yticklabels(prob_labels, fontsize=8.5)
    ax.set_xlabel("Consequence  →", fontsize=10, labelpad=4)
    ax.set_ylabel("Probability  ↑", fontsize=10, labelpad=4)
    ax.tick_params(length=0)

    # Legend
    legend_items = [
        mpatches.Patch(facecolor=str(0.85), edgecolor="black", linewidth=0.6,
                       label="Low  (R ≤ 4)"),
        mpatches.Patch(facecolor=str(0.55), edgecolor="black", linewidth=0.6,
                       hatch="..", label="Medium  (4 < R ≤ 9)"),
        mpatches.Patch(facecolor=str(0.30), edgecolor="black", linewidth=0.6,
                       hatch="///", label="High  (9 < R ≤ 16)"),
        mpatches.Patch(facecolor=str(0.10), edgecolor="black", linewidth=0.6,
                       hatch="xxx", label="Critical  (R > 16)"),
    ]
    ax.legend(handles=legend_items, loc="upper left",
              bbox_to_anchor=(1.01, 1.0), borderaxespad=0,
              fontsize=8.5, frameon=True, edgecolor="black",
              handlelength=1.5, handleheight=1.2)

    fig.tight_layout()
    stem = "fig_01_risk_matrix"
    fig.savefig(f"{OUTDIR}/{stem}.pdf")
    fig.savefig(f"{OUTDIR}/{stem}.png", dpi=200)
    plt.close(fig)
    print(f"saved {stem}.pdf + {stem}.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIG 02 — Requirement vs Design (side-by-side panels)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def make_fig02():
    req_items = [
        "Sort accuracy ≥ 95 %",
        "MQTT latency ≤ 200 ms",
        "BOM cost ≤ $500 CAD",
    ]
    design_items = [
        "VL53L1X ToF sensor +\nthreshold classifier",
        "ESP32 with MQTT\nover TLS",
        "STM32F4 + off-shelf\nmotor driver",
    ]

    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.axis("off")

    # Draw vertical divider at x=0.5 (in axes coords)
    ax.plot([0.5, 0.5], [0.0, 1.0], color="black", linewidth=1.2,
            transform=ax.transAxes, clip_on=False)

    # Panel titles — placed at top with clear space below
    ax.text(0.25, 0.97, "Requirement  (What)",
            ha="center", va="top", fontsize=11, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.75, 0.97, "Design  (How)",
            ha="center", va="top", fontsize=11, fontweight="bold",
            transform=ax.transAxes)

    # Position boxes: 3 rows, starting below title area
    # y0 from bottom: rows at 0.60, 0.33, 0.04  height=0.24
    box_y = [0.62, 0.34, 0.04]
    box_h = 0.24
    left_x0, left_x1 = 0.02, 0.46
    right_x0, right_x1 = 0.54, 0.98

    for i, (req, des) in enumerate(zip(req_items, design_items)):
        y0 = box_y[i]
        # Left box (requirement) — lighter gray
        fancy = mpatches.FancyBboxPatch(
            (left_x0, y0), left_x1 - left_x0, box_h,
            boxstyle="round,pad=0.01",
            facecolor="0.88", edgecolor="black", linewidth=0.8,
            transform=ax.transAxes, clip_on=False, zorder=2,
        )
        ax.add_patch(fancy)
        ax.text((left_x0 + left_x1) / 2, y0 + box_h / 2, req,
                ha="center", va="center", fontsize=9.5,
                transform=ax.transAxes, zorder=3)

        # Right box (design) — medium gray
        fancy2 = mpatches.FancyBboxPatch(
            (right_x0, y0), right_x1 - right_x0, box_h,
            boxstyle="round,pad=0.01",
            facecolor="0.70", edgecolor="black", linewidth=0.8,
            transform=ax.transAxes, clip_on=False, zorder=2,
        )
        ax.add_patch(fancy2)
        ax.text((right_x0 + right_x1) / 2, y0 + box_h / 2, des,
                ha="center", va="center", fontsize=9.5,
                transform=ax.transAxes, zorder=3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    stem = "fig_02_req_vs_design"
    fig.savefig(f"{OUTDIR}/{stem}.pdf")
    fig.savefig(f"{OUTDIR}/{stem}.png", dpi=200)
    plt.close(fig)
    print(f"saved {stem}.pdf + {stem}.png")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FIG 03 — Critical Unknowns (horizontal bar chart)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def make_fig03():
    items = [
        ("Sort sensor accuracy\nat conveyor speed",  20),
        ("MQTT reliability\nover factory Wi-Fi",      16),
        ("Actuator repeatability\nat 6 items/min",    12),
        ("Embedded inference\nlatency ≤ 5 ms",         9),
        ("3D-print bracket holds\nunder vibration",    4),
    ]
    # Already sorted longest-first
    labels = [x[0] for x in items]
    scores = [x[1] for x in items]
    grays  = [risk_gray(r) for r in scores]

    # Hatch patterns matching fig_01
    def hatch_for(r):
        if r <= 4:   return ""
        elif r <= 9: return ".."
        elif r <= 16: return "///"
        else:        return "xxx"

    hatches = [hatch_for(r) for r in scores]

    fig, ax = plt.subplots(figsize=(8, 2.8))

    y_positions = np.arange(len(items))
    bars = ax.barh(y_positions, scores,
                   color=[str(g) for g in grays],
                   edgecolor="black", linewidth=0.7,
                   height=0.55)

    # Apply hatch patterns
    for bar, h in zip(bars, hatches):
        bar.set_hatch(h)

    # R value labels at end of each bar
    for i, (score, bar) in enumerate(zip(scores, bars)):
        txt_x = score + 0.3
        ax.text(txt_x, i, f"R={score}",
                va="center", ha="left", fontsize=9, fontweight="bold")

    # Threshold lines
    ax.axvline(x=9,  color="black", linestyle="--", linewidth=1.0,
               label="Medium/High (R=9)")
    ax.axvline(x=16, color="black", linestyle=":",  linewidth=1.2,
               label="High/Critical (R=16)")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=8.8)
    ax.set_xlabel("Risk Score  R = P × C", fontsize=10)
    ax.set_xlim(0, 26)
    ax.set_ylim(-0.5, len(items) - 0.5)
    ax.invert_yaxis()   # highest risk at top
    ax.tick_params(axis="x", labelsize=9)
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    # Legend for threshold lines
    ax.legend(loc="lower right", fontsize=8.5, frameon=True,
              edgecolor="black")

    # Risk-band legend patches (reuse fig_01 style)
    band_handles = [
        mpatches.Patch(facecolor="0.85", edgecolor="black", lw=0.6,
                       label="Low  (R≤4)"),
        mpatches.Patch(facecolor="0.55", edgecolor="black", lw=0.6,
                       hatch="..", label="Medium  (R≤9)"),
        mpatches.Patch(facecolor="0.30", edgecolor="black", lw=0.6,
                       hatch="///", label="High  (R≤16)"),
        mpatches.Patch(facecolor="0.10", edgecolor="black", lw=0.6,
                       hatch="xxx", label="Critical  (R>16)"),
    ]
    ax.legend(handles=band_handles, loc="lower right",
              fontsize=8.5, frameon=True, edgecolor="black",
              handlelength=1.4)

    fig.tight_layout()
    stem = "fig_03_critical_unknowns"
    fig.savefig(f"{OUTDIR}/{stem}.pdf")
    fig.savefig(f"{OUTDIR}/{stem}.png", dpi=200)
    plt.close(fig)
    print(f"saved {stem}.pdf + {stem}.png")


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    make_fig01()
    make_fig02()
    make_fig03()
    print("All figures done.")

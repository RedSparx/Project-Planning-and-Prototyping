"""
gen_figures.py
Generate figures for Chapter 3: Prototype vs. Product & Selective Prototyping.

Figures produced:
  fig_01_cost_of_change.{pdf,png}   — bar chart, figsize (6, 2.8)
  fig_02_selective_decision.{pdf,png} — horizontal decision flow, figsize (9, 2.8)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.patches import Polygon
import numpy as np
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Figure 1 — Cost of Change bar chart
# ---------------------------------------------------------------------------

def make_fig01():
    stages = ["Concept", "Design", "Build", "Production"]
    values = [1, 10, 100, 1000]
    labels = ["1×", "10×", "100×", "1 000×"]
    hatches = ["", "//", "//", "xx"]
    colors = ["0.80", "0.60", "0.40", "0.18"]

    fig, ax = plt.subplots(figsize=(6, 2.8))

    bars = ax.bar(stages, values, color=colors, hatch=hatches,
                  edgecolor="black", linewidth=0.8, zorder=3)

    ax.set_yscale("log")
    ax.set_ylim(0.5, 5000)
    ax.set_ylabel("Relative cost to fix a flaw (log scale)", fontsize=9)
    ax.set_title("Cost of Change Escalates with Project Stage", fontsize=10)
    ax.tick_params(axis="both", labelsize=9)

    # Custom y-tick labels
    ax.set_yticks([1, 10, 100, 1000])
    ax.set_yticklabels(["1×", "10×", "100×", "1 000×"], fontsize=9)

    ax.yaxis.grid(True, which="major", linestyle="--", linewidth=0.5,
                  color="0.75", zorder=0)
    ax.set_axisbelow(True)

    # Bar top labels — placed well above each bar top
    offsets = [1.55, 1.45, 1.45, 1.45]
    for bar, lbl, off in zip(bars, labels, offsets):
        top = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2,
                top * off,
                lbl,
                ha="center", va="bottom",
                fontsize=9, fontweight="bold")

    # Annotation arrow pointing to the Build bar
    # Arrow starts from text box (lower-left area) and ends near Build bar mid
    ax.annotate(
        "Fix here costs\n100× vs. Concept",
        xy=(2, 60),          # tail of arrow near Build bar, mid-height
        xytext=(0.65, 8),    # text position — left side, well clear of bars
        fontsize=8,
        ha="center",
        arrowprops=dict(
            arrowstyle="->",
            color="black",
            lw=1.2,
            connectionstyle="arc3,rad=-0.25",
        ),
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.5", lw=0.8),
        zorder=5,
    )

    fig.tight_layout(pad=0.5)

    base = os.path.join(OUT_DIR, "fig_01_cost_of_change")
    fig.savefig(base + ".pdf", dpi=150, bbox_inches="tight")
    fig.savefig(base + ".png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {base}.pdf / .png")


# ---------------------------------------------------------------------------
# Figure 2 — Horizontal selective-prototyping decision flow
# ---------------------------------------------------------------------------

def draw_box(ax, cx, cy, w, h, text, fc, ec="black", tc="black",
             bold=False, fontsize=9):
    """Draw a rounded rectangle centred at (cx, cy)."""
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.04",
        facecolor=fc, edgecolor=ec, linewidth=1.0,
        zorder=3,
        transform=ax.transData, clip_on=False,
    )
    ax.add_patch(patch)
    weight = "bold" if bold else "normal"
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fontsize, fontweight=weight, color=tc,
            zorder=4, clip_on=False)


def draw_diamond(ax, cx, cy, w, h, text, fc, fontsize=9):
    """Draw a diamond centred at (cx, cy) with half-widths w, h."""
    verts = np.array([
        [cx,     cy + h],
        [cx + w, cy    ],
        [cx,     cy - h],
        [cx - w, cy    ],
    ])
    poly = Polygon(verts, closed=True,
                   facecolor=fc, edgecolor="black", linewidth=1.0,
                   zorder=3)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fontsize, zorder=4, clip_on=False,
            multialignment="center")


def arrow(ax, x0, y0, x1, y1, lw=1.2):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color="black",
                                lw=lw, mutation_scale=10),
                zorder=2)


def make_fig02():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(0, 9)
    ax.set_ylim(-1.2, 1.2)
    ax.axis("off")

    # ---- layout constants ----
    # Row y-level for the main flow
    ROW_Y = 0.5           # y for boxes and diamonds
    TERM_Y = -0.55        # y for "Prototype it" terminals below diamonds
    BOX_W = 0.90          # rectangle half-width
    BOX_H = 0.32          # rectangle half-height
    DW = 0.52             # diamond half-width (data x)
    DH = 0.34             # diamond half-height (data y)

    # x positions
    X_START   = 0.65      # "Subsystem" box
    X_D1      = 2.35      # Diamond 1
    X_D2      = 4.45      # Diamond 2
    X_D3      = 6.55      # Diamond 3
    X_END     = 8.35      # "Specify & trust" box
    # Prototype terminals (below each diamond)
    X_P1      = X_D1
    X_P2      = X_D2
    X_P3      = X_D3

    # ---- start box ----
    draw_box(ax, X_START, ROW_Y, BOX_W, BOX_H * 1.1,
             "Subsystem", fc="0.88", fontsize=9, bold=False)

    # ---- arrow: start → D1 ----
    arrow(ax, X_START + BOX_W / 2, ROW_Y,
              X_D1 - DW - 0.03, ROW_Y)

    # ---- Diamond 1 ----
    draw_diamond(ax, X_D1, ROW_Y, DW, DH,
                 "Novel or\nunprecedented?", fc="0.78")

    # "No" arrow right → D2
    arrow(ax, X_D1 + DW + 0.03, ROW_Y,
              X_D2 - DW - 0.03, ROW_Y)
    ax.text((X_D1 + DW + 0.06 + X_D2 - DW - 0.06) / 2,
            ROW_Y + 0.10, "No",
            ha="center", va="bottom", fontsize=8)

    # "Yes" arrow down → Prototype it
    arrow(ax, X_D1, ROW_Y - DH - 0.03,
              X_D1, TERM_Y + BOX_H / 2 + 0.03)
    ax.text(X_D1 + 0.08, (ROW_Y - DH + TERM_Y + BOX_H / 2) / 2,
            "Yes", ha="left", va="center", fontsize=8)

    # Prototype it terminal 1
    draw_box(ax, X_P1, TERM_Y, BOX_W * 1.05, BOX_H,
             "Prototype it", fc="0.15", tc="white", fontsize=9, bold=True)

    # ---- Diamond 2 ----
    draw_diamond(ax, X_D2, ROW_Y, DW, DH,
                 "High uncertainty\nin performance?", fc="0.78")

    # "No" arrow right → D3
    arrow(ax, X_D2 + DW + 0.03, ROW_Y,
              X_D3 - DW - 0.03, ROW_Y)
    ax.text((X_D2 + DW + 0.06 + X_D3 - DW - 0.06) / 2,
            ROW_Y + 0.10, "No",
            ha="center", va="bottom", fontsize=8)

    # "Yes" arrow down → Prototype it
    arrow(ax, X_D2, ROW_Y - DH - 0.03,
              X_D2, TERM_Y + BOX_H / 2 + 0.03)
    ax.text(X_D2 + 0.08, (ROW_Y - DH + TERM_Y + BOX_H / 2) / 2,
            "Yes", ha="left", va="center", fontsize=8)

    # Prototype it terminal 2
    draw_box(ax, X_P2, TERM_Y, BOX_W * 1.05, BOX_H,
             "Prototype it", fc="0.15", tc="white", fontsize=9, bold=True)

    # ---- Diamond 3 ----
    draw_diamond(ax, X_D3, ROW_Y, DW, DH,
                 "High consequence\nif it fails?", fc="0.78")

    # "No" arrow right → Specify & trust
    arrow(ax, X_D3 + DW + 0.03, ROW_Y,
              X_END - BOX_W / 2 - 0.03, ROW_Y)
    ax.text((X_D3 + DW + 0.06 + X_END - BOX_W / 2 - 0.06) / 2,
            ROW_Y + 0.10, "No",
            ha="center", va="bottom", fontsize=8)

    # "Yes" arrow down → Prototype it
    arrow(ax, X_D3, ROW_Y - DH - 0.03,
              X_D3, TERM_Y + BOX_H / 2 + 0.03)
    ax.text(X_D3 + 0.08, (ROW_Y - DH + TERM_Y + BOX_H / 2) / 2,
            "Yes", ha="left", va="center", fontsize=8)

    # Prototype it terminal 3
    draw_box(ax, X_P3, TERM_Y, BOX_W * 1.05, BOX_H,
             "Prototype it", fc="0.15", tc="white", fontsize=9, bold=True)

    # ---- Specify & trust terminal ----
    draw_box(ax, X_END, ROW_Y, BOX_W * 1.10, BOX_H * 1.25,
             "Specify &\ntrust", fc="0.75", fontsize=9, bold=True)

    # ---- Title ----
    ax.set_title("Selective Prototyping Decision", fontsize=10, pad=6)

    fig.tight_layout(pad=0.3)

    base = os.path.join(OUT_DIR, "fig_02_selective_decision")
    fig.savefig(base + ".pdf", dpi=150, bbox_inches="tight")
    fig.savefig(base + ".png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {base}.pdf / .png")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    make_fig01()
    make_fig02()
    print("All figures generated.")

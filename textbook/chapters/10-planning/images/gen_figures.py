"""
gen_figures.py
Generate 3 grayscale figures for Chapter 10 – Planning & Schedule Management.
Outputs: fig_01_gantt.{pdf,png}, fig_02_cpm_network.{pdf,png}, fig_03_pert_dist.{pdf,png}
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from scipy.stats import beta as scipy_beta
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ── shared style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "sans-serif",
    "font.size":         9,
    "axes.linewidth":    1.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
})

DARK  = 0.35   # critical fill
LIGHT = 0.75   # non-critical fill

def save(fig, name):
    fig.savefig(os.path.join(OUT, f"{name}.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(OUT, f"{name}.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {name}.pdf / .png")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 1 – Gantt Chart
# ═══════════════════════════════════════════════════════════════════════════════
def make_gantt():
    fig, ax = plt.subplots(figsize=(9, 2.8))

    # Activities: (label, start_day, end_day_inclusive, critical)
    activities = [
        ("A: PCB Design",              1,  3,  True),
        ("B: Component Procurement",   4, 10, False),
        ("C: PCB Fabrication",         4,  8,  True),
        ("D: PCB Assembly",           11, 12,  True),
        ("E: Firmware Integration",    4,  7, False),
        ("F: System Test",            13, 15,  True),
    ]

    n = len(activities)
    bar_h = 0.50
    # Row 0 = top (A), row n-1 = bottom (F)
    y_positions = list(range(n - 1, -1, -1))   # [5,4,3,2,1,0]

    for i, (label, start, end, crit) in enumerate(activities):
        y = y_positions[i]
        fc = str(DARK) if crit else str(LIGHT)
        ec = "black" if crit else "0.40"
        lw = 1.2 if crit else 1.0
        # bar from start-0.5 to end+0.5 (each day occupies 1 unit)
        ax.barh(y, end - start + 1, left=start - 0.5,
                height=bar_h, color=fc, edgecolor=ec, linewidth=lw,
                align="center", zorder=3)

    # ── Milestone diamonds + labels ──
    # Place at y = -1.1 (below all bars), label below diamond
    milestone_y = -1.15
    milestones = [
        (3,  "Design\ncomplete"),
        (12, "Board\nready"),
        (15, "Gate 3"),
    ]
    for day, mtext in milestones:
        ax.plot(day, milestone_y, marker="D", markersize=7,
                color="black", markeredgewidth=1.0, zorder=5,
                clip_on=False)
        ax.text(day, milestone_y - 0.30, mtext,
                ha="center", va="top", fontsize=8, linespacing=1.1,
                clip_on=False)

    # Light vertical gridlines every 3 days
    for gx in range(3, 16, 3):
        ax.axvline(gx + 0.5, color="0.82", linewidth=0.75, zorder=1)

    # ── Axes ──
    ax.set_xlim(0.5, 15.5)
    ax.set_ylim(-2.6, n - 0.5 + 0.4)
    ax.set_xticks(range(1, 16))
    ax.set_xticklabels([str(d) for d in range(1, 16)], fontsize=9)
    ax.set_xlabel("Day", fontsize=9, labelpad=3)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([a[0] for a in activities], fontsize=9)
    ax.tick_params(axis="y", length=0, pad=4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend (top right, inside plot area)
    crit_patch = mpatches.Patch(facecolor=str(DARK), edgecolor="black",
                                linewidth=1.0, label="Critical path")
    nc_patch   = mpatches.Patch(facecolor=str(LIGHT), edgecolor="0.40",
                                linewidth=1.0, label="Non-critical")
    ax.legend(handles=[crit_patch, nc_patch], loc="upper right",
              fontsize=8, frameon=True, framealpha=0.95,
              edgecolor="0.5", handlelength=1.2, borderpad=0.5)

    fig.subplots_adjust(left=0.22, right=0.97, top=0.97, bottom=0.28)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 2 – CPM Network Diagram
# ═══════════════════════════════════════════════════════════════════════════════
def make_cpm():
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.set_aspect("equal")
    ax.axis("off")

    # Canvas coordinates
    ax.set_xlim(-0.3, 10.8)
    ax.set_ylim(-0.4, 3.4)

    BOX_W = 1.55
    BOX_H = 0.88

    # Node positions (cx, cy)
    nodes = {
        "A": dict(x=0.5,  y=1.5, ES=0,  EF=3,  LS=0,  LF=3,  dur=3, crit=True),
        "B": dict(x=3.5,  y=2.6, ES=3,  EF=10, LS=3,  LF=10, dur=7, crit=True),
        "C": dict(x=3.5,  y=1.5, ES=3,  EF=8,  LS=5,  LF=10, dur=5, crit=False),
        "E": dict(x=3.5,  y=0.4, ES=3,  EF=7,  LS=8,  LF=12, dur=4, crit=False),
        "D": dict(x=6.6,  y=2.1, ES=10, EF=12, LS=10, LF=12, dur=2, crit=True),
        "F": dict(x=9.6,  y=2.1, ES=12, EF=15, LS=12, LF=15, dur=3, crit=True),
    }

    def right_port(name):
        nd = nodes[name]
        return nd["x"] + BOX_W / 2, nd["y"]

    def left_port(name):
        nd = nodes[name]
        return nd["x"] - BOX_W / 2, nd["y"]

    # Edges: (src, dst, critical, connection_style)
    edges = [
        ("A", "B", True,  "arc3,rad=-0.15"),
        ("A", "C", False, "arc3,rad=0.0"),
        ("A", "E", False, "arc3,rad=0.15"),
        ("B", "D", True,  "arc3,rad=0.0"),
        ("C", "D", False, "arc3,rad=0.0"),
        ("D", "F", True,  "arc3,rad=0.0"),
        ("E", "F", False, "arc3,rad=0.55"),
    ]

    for src, dst, crit, conn in edges:
        x0, y0 = right_port(src)
        x1, y1 = left_port(dst)
        lw    = 2.0 if crit else 1.0
        ls    = "solid" if crit else "dashed"
        color = "black" if crit else "0.45"
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=lw,
                linestyle=ls,
                mutation_scale=10,
                connectionstyle=conn,
            ),
            zorder=2,
        )

    # ── Draw node boxes ──
    for name, nd in nodes.items():
        cx, cy = nd["x"], nd["y"]
        fc = str(DARK) if nd["crit"] else str(LIGHT)
        lw = 1.5 if nd["crit"] else 1.0

        rect = FancyBboxPatch(
            (cx - BOX_W / 2, cy - BOX_H / 2), BOX_W, BOX_H,
            boxstyle="square,pad=0.02",
            facecolor=fc, edgecolor="black", linewidth=lw, zorder=3,
        )
        ax.add_patch(rect)

        row_gap = BOX_H * 0.28
        ax.text(cx, cy + row_gap, f"ES={nd['ES']}  EF={nd['EF']}",
                ha="center", va="center", fontsize=7.5, zorder=4)
        ax.text(cx, cy, f"{name}  (d={nd['dur']})",
                ha="center", va="center", fontsize=9,
                fontweight="bold", zorder=4)
        ax.text(cx, cy - row_gap, f"LS={nd['LS']}  LF={nd['LF']}",
                ha="center", va="center", fontsize=7.5, zorder=4)

    # Legend — placed inside lower-right of axes
    crit_patch = mpatches.Patch(facecolor=str(DARK), edgecolor="black",
                                linewidth=1.0, label="Critical")
    nc_patch   = mpatches.Patch(facecolor=str(LIGHT), edgecolor="0.3",
                                linewidth=1.0, label="Non-critical")
    ax.legend(handles=[crit_patch, nc_patch],
              loc="lower right", fontsize=8, frameon=True,
              framealpha=0.95, edgecolor="0.5",
              bbox_to_anchor=(1.0, 0.0), bbox_transform=ax.transAxes)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.12)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 3 – PERT Beta Distribution
# ═══════════════════════════════════════════════════════════════════════════════
def make_pert():
    fig, ax = plt.subplots(figsize=(7, 2.6))

    a, m, b = 4.0, 7.0, 14.0
    t_e   = (a + 4 * m + b) / 6          # ≈ 7.667
    sigma = (b - a) / 6                   # ≈ 1.667

    # PERT beta shape parameters
    alpha_p = 1 + 4 * (m - a) / (b - a)
    beta_p  = 1 + 4 * (b - m) / (b - a)
    dist    = scipy_beta(alpha_p, beta_p, loc=a, scale=(b - a))

    x = np.linspace(a - 0.2, b + 0.2, 600)
    y = dist.pdf(x)

    peak_y = dist.pdf(m)

    # Shaded ±σ region
    x_shade = np.linspace(t_e - sigma, t_e + sigma, 300)
    y_shade = dist.pdf(x_shade)
    ax.fill_between(x_shade, y_shade, alpha=1.0,
                    color=str(LIGHT), zorder=1)

    # Main curve on top
    ax.plot(x, y, color="black", linewidth=1.5, zorder=3)

    # y ceiling for text placement
    y_top = peak_y * 1.10

    # ── Vertical reference lines ──
    # a=4 dashed
    ax.axvline(a, color="black", linewidth=1.0, linestyle="dashed", zorder=2)
    # m=7 dashed
    ax.axvline(m, color="black", linewidth=1.0, linestyle="dashed", zorder=2)
    # b=14 dashed
    ax.axvline(b, color="black", linewidth=1.0, linestyle="dashed", zorder=2)
    # t_e solid
    ax.axvline(t_e, color="black", linewidth=1.5, linestyle="solid", zorder=4)

    # ── Text labels for vertical lines (all at same y = y_top * 0.98) ──
    label_y = y_top * 0.97
    ax.text(a,    label_y, f"$a$={int(a)}",
            ha="center", va="top", fontsize=9)
    ax.text(m - 0.35, label_y, f"$m$={int(m)}",
            ha="right", va="top", fontsize=9)
    ax.text(t_e + 0.2, label_y, f"$t_e$={t_e:.2f}",
            ha="left", va="top", fontsize=9)
    ax.text(b,    label_y, f"$b$={int(b)}",
            ha="center", va="top", fontsize=9)

    # ── σ bracket: double-headed arrow spanning one σ on the right side ──
    # Place arrow from t_e to t_e+σ, label to the right and below
    brack_y = -peak_y * 0.13
    ax.annotate("", xy=(t_e + sigma, brack_y), xytext=(t_e, brack_y),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.3),
                zorder=5)
    ax.text(t_e + sigma + 0.2, brack_y,
            f"$\\sigma$ = {sigma:.2f} d",
            ha="left", va="center", fontsize=8.5)

    # ── Axes ──
    ax.set_xlim(2.0, 16.0)
    ax.set_ylim(-peak_y * 0.30, y_top)
    ax.set_xlabel("Duration (days)", fontsize=9)
    ax.set_ylabel("Probability density", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9)

    # Legend
    shade_patch = mpatches.Patch(
        facecolor=str(LIGHT), edgecolor="none",
        label=f"$t_e \\pm \\sigma$ = [{t_e-sigma:.1f}, {t_e+sigma:.2f}] d"
    )
    ax.legend(handles=[shade_patch], loc="upper right", fontsize=8,
              frameon=True, framealpha=0.95, edgecolor="0.5")

    fig.subplots_adjust(left=0.11, right=0.97, top=0.93, bottom=0.24)
    return fig


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating figures …")
    save(make_gantt(),  "fig_01_gantt")
    save(make_cpm(),    "fig_02_cpm_network")
    save(make_pert(),   "fig_03_pert_dist")
    print("Done.")

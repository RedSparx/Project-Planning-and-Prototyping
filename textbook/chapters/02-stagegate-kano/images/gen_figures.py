"""
gen_figures.py
Chapter 2 — Product Development & the Stage-Gate Model
Generates fig_01_stagegate, fig_02_kano_map, fig_03_kano_csds, fig_04_scope_decision
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "savefig.bbox": "tight",
})

def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    print(f"saved {stem}.pdf + {stem}.png")


# ─────────────────────────────────────────────────────────────────────────────
# fig_01_stagegate
# ─────────────────────────────────────────────────────────────────────────────
def make_fig01():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    stages = ["Discovery", "Scoping", "Build\nBusiness\nCase", "Development", "Testing &\nValidation\n/ Launch"]
    gates  = ["G1", "G2", "G3", "G4", "G5"]

    # Layout: explicit widths for stages and gates
    stage_w = 0.130
    gate_w  = 0.032    # narrower diamonds
    gap     = 0.012    # gap between elements

    # Total width check
    total = 5 * stage_w + 5 * gate_w + 9 * gap  # 9 gaps between 10 elements
    left_pad = (1.0 - total) / 2

    # Build positions
    positions = []  # (type, left_x, width)
    cx = left_pad
    for i in range(5):
        positions.append(("stage", cx, stage_w))
        cx += stage_w + gap
        positions.append(("gate", cx, gate_w))
        cx += gate_w + gap

    box_bottom = 0.22
    box_top    = 0.75
    box_cy     = (box_bottom + box_top) / 2
    box_h      = box_top - box_bottom

    stage_items = [p for p in positions if p[0] == "stage"]
    gate_items  = [p for p in positions if p[0] == "gate"]

    # ── Annotation bands (drawn first, behind)
    # band1: Scoping (idx 1) + Build Business Case (idx 2)
    b1_l = stage_items[1][1] - 0.005
    b1_r = stage_items[2][1] + stage_items[2][2] + 0.005
    ax.add_patch(FancyBboxPatch((b1_l, box_bottom - 0.04), b1_r - b1_l, box_h + 0.08,
                                boxstyle="round,pad=0.005", lw=0,
                                facecolor=str(0.90), zorder=0))
    ax.text((b1_l + b1_r) / 2, box_top + 0.10, "This course\n(Project I)",
            ha="center", va="bottom", fontsize=8, zorder=1)

    # band2: Development (idx 3) + Testing (idx 4)
    b2_l = stage_items[3][1] - 0.005
    b2_r = stage_items[4][1] + stage_items[4][2] + 0.005
    ax.add_patch(FancyBboxPatch((b2_l, box_bottom - 0.04), b2_r - b2_l, box_h + 0.08,
                                boxstyle="round,pad=0.005", lw=0,
                                facecolor=str(0.82), zorder=0))
    ax.text((b2_l + b2_r) / 2, box_top + 0.10, "Project II",
            ha="center", va="bottom", fontsize=8, zorder=1)

    # ── Backbone arrow (behind boxes)
    x_arrow_start = stage_items[0][1]
    x_arrow_end   = gate_items[-1][1] + gate_items[-1][2] + 0.005
    ax.annotate("", xy=(x_arrow_end, box_cy), xytext=(x_arrow_start - 0.005, box_cy),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5), zorder=1)

    # ── Stage boxes (rounded rectangles)
    for i, (_, sx, sw) in enumerate(stage_items):
        ax.add_patch(FancyBboxPatch((sx, box_bottom), sw, box_h,
                                    boxstyle="round,pad=0.012", lw=1.2,
                                    edgecolor="black", facecolor=str(0.75), zorder=2))
        ax.text(sx + sw / 2, box_cy, stages[i],
                ha="center", va="center", fontsize=9, zorder=3, linespacing=1.3)

    # ── Gate diamonds (small, not overlapping stage boxes)
    diam_hw = gate_w * 0.80   # half-width — keep well within the gate slot
    diam_hh = box_h * 0.35    # half-height — kept well within box height
    for i, (_, gx, gw) in enumerate(gate_items):
        gcx = gx + gw / 2
        diamond = plt.Polygon(
            [[gcx - diam_hw, box_cy],
             [gcx,           box_cy + diam_hh],
             [gcx + diam_hw, box_cy],
             [gcx,           box_cy - diam_hh]],
            closed=True, lw=1.2, edgecolor="black", facecolor="white", zorder=2)
        ax.add_patch(diamond)
        ax.text(gcx, box_cy, gates[i],
                ha="center", va="center", fontsize=8, fontweight="bold", zorder=3)

    # ── Bottom note
    ax.text(0.5, 0.03, "Gate decisions:  Go / Kill / Hold / Recycle",
            ha="center", va="bottom", fontsize=8,
            transform=ax.transAxes)

    fig.tight_layout(pad=0.3)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# fig_02_kano_map
# ─────────────────────────────────────────────────────────────────────────────
def make_fig02():
    fig, ax = plt.subplots(figsize=(7, 2.8))

    x = np.linspace(0, 1, 300)

    # All curves in [0, 1] space: 0 = fully dissatisfied, 1 = fully delighted, 0.5 = neutral
    #
    # 1. Threshold/Basic: very dissatisfied when absent (~0.03), stays low until ~0.65,
    #    then sigmoid-rises to ~0.60 (approaches but stays below neutral at x→1).
    threshold2 = 0.03 + 0.57 / (1 + np.exp(-10 * (x - 0.72)))

    # 2. Performance: near-linear from ~0.05 (almost dissatisfied) to ~0.95 (almost delighted)
    performance2 = 0.05 + 0.90 * x

    # 3. Delighter: starts slightly below neutral (0.48) when absent,
    #    rises steeply (concave-up) to delighted (0.98)
    delighter2 = 0.48 + 0.50 * (x ** 1.4)

    # 4. Indifferent: slightly below neutral (0.44) — flat throughout
    #    This gives clear visual separation from Threshold end and Delighter start
    indifferent2 = np.full_like(x, 0.44)

    # Reference lines
    ax.axhline(0.5, color="gray", lw=0.8, alpha=0.3, zorder=0)
    ax.axvline(0.5, color="gray", lw=0.8, alpha=0.3, zorder=0)

    # Plot curves
    ax.plot(x, threshold2,   ls="-.",  lw=1.5, color="black", label="Threshold")
    ax.plot(x, performance2, ls="-",   lw=2.0, color="black", label="Performance")
    ax.plot(x, delighter2,   ls="--",  lw=1.5, color="black", label="Delighter")
    ax.plot(x, indifferent2, ls=":",   lw=1.2, color="black", label="Indifferent")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Absent", "Fully present"], fontsize=9)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Dissatisfied", "Delighted"], fontsize=9)
    ax.set_xlabel("Feature Fulfilment →", fontsize=9, labelpad=3)
    ax.set_ylabel("Customer Satisfaction →", fontsize=9, labelpad=3)

    ax.legend(loc="upper left", fontsize=8, framealpha=0.9,
              handlelength=2.5, borderpad=0.5)

    fig.tight_layout(pad=0.4)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# fig_03_kano_csds
# ─────────────────────────────────────────────────────────────────────────────
def make_fig03():
    fig, ax = plt.subplots(figsize=(6, 2.8))

    # Quadrant dividers
    ax.axvline(0.5, color="black", lw=1.0, ls="--", zorder=1)
    ax.axhline(0.5, color="black", lw=1.0, ls="--", zorder=1)

    # Quadrant labels — placed in corners, well away from data points
    lkw = dict(ha="center", va="center", fontsize=9, color="0.60", zorder=2)
    ax.text(0.75, 0.93, "Performance", **lkw)
    ax.text(0.12, 0.93, "Threshold",   **lkw)
    ax.text(0.75, 0.07, "Delighter",   **lkw)
    ax.text(0.12, 0.07, "Indifferent", **lkw)

    # Data points: (name, CS, |DS|, label_dx, label_dy, ha)
    features = [
        ("Sort acc.",  0.63, 0.70,  0.04,  0.05, "left"),
        ("MQTT",       0.73, 0.20,  0.04, -0.06, "left"),
        ("Conveyor",   0.27, 0.80,  0.04,  0.05, "left"),
        ("Housing",    0.20, 0.27,  0.04, -0.06, "left"),
        ("AI detect.", 0.80, 0.19, -0.04,  0.05, "right"),
    ]

    for name, cs, ds, dx, dy, ha in features:
        ax.plot(cs, ds, "o", ms=6, color="black", zorder=3)
        ax.text(cs + dx, ds + dy, name, fontsize=8, ha=ha, va="center", zorder=4)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Satisfaction Coefficient  CS", fontsize=9)
    ax.set_ylabel("|Dissatisfaction Coefficient|  |DS|", fontsize=9)
    ax.tick_params(labelsize=8)

    fig.tight_layout(pad=0.4)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# fig_04_scope_decision
# ─────────────────────────────────────────────────────────────────────────────
def make_fig04():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def rounded_box(cx, cy, w, h, fill_gray, text, fontsize=9, text_color="black", zorder=2):
        x0, y0 = cx - w / 2, cy - h / 2
        ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                    boxstyle="round,pad=0.02",
                                    lw=1.2, edgecolor="black",
                                    facecolor=str(fill_gray), zorder=zorder))
        ax.text(cx, cy, text, ha="center", va="center",
                fontsize=fontsize, color=text_color,
                zorder=zorder + 1, linespacing=1.3)

    def diamond_shape(cx, cy, hw, hh, fill_gray, text, fontsize=9, zorder=2):
        pts = [[cx - hw, cy], [cx, cy + hh], [cx + hw, cy], [cx, cy - hh]]
        ax.add_patch(plt.Polygon(pts, closed=True, lw=1.2,
                                 edgecolor="black", facecolor=str(fill_gray), zorder=zorder))
        ax.text(cx, cy, text, ha="center", va="center",
                fontsize=fontsize, zorder=zorder + 1, linespacing=1.3)

    # Positions
    cy_main = 0.50
    x_start = 0.09
    x_diam  = 0.31
    x_bend  = 0.52     # vertical routing column
    x_term  = 0.79

    box_w   = 0.14
    box_h   = 0.30
    diam_hw = 0.100
    diam_hh = 0.34
    term_w  = 0.175
    term_h  = 0.22

    y_top   = 0.78
    y_mid   = 0.50
    y_bot   = 0.20

    # Start box
    rounded_box(x_start, cy_main, box_w, box_h, 0.88, "Feature to\nclassify")

    # Arrow: start box → diamond
    ax.annotate("", xy=(x_diam - diam_hw, cy_main),
                xytext=(x_start + box_w / 2, cy_main),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2), zorder=5)

    # Decision diamond
    diamond_shape(x_diam, cy_main, diam_hw, diam_hh, 1.0, "Kano\ncategory?")

    # Route: from right tip of diamond, go right to x_bend at cy_main,
    # then draw vertical line from y_top to y_bot at x_bend,
    # then horizontal arrows from x_bend to each terminal box.
    x_right_tip = x_diam + diam_hw
    x_term_l    = x_term - term_w / 2

    # Horizontal line from diamond right tip to x_bend
    ax.plot([x_right_tip, x_bend], [cy_main, cy_main], color="black", lw=1.2, zorder=5)

    # Vertical routing line at x_bend from y_bot to y_top
    ax.plot([x_bend, x_bend], [y_bot, y_top], color="black", lw=1.2, zorder=5)

    # Three branch arrows (horizontal from x_bend to terminal boxes)
    branches = [
        (y_top, "Delighter /\nUncertain", 0.25, "PROTOTYPE\nit", "white"),
        (y_mid, "Performance\n(understood)", 0.55, "PROTOTYPE\nif uncertain", "black"),
        (y_bot, "Threshold /\nIndifferent", 0.85, "SPECIFY-AND-\nTRUST it", "black"),
    ]

    for y_br, blabel, fill, txt, tc in branches:
        # Arrow from x_bend to terminal box left edge
        ax.annotate("", xy=(x_term_l, y_br), xytext=(x_bend, y_br),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2), zorder=5)
        # Branch label: placed left of x_bend, slightly above/below the horizontal
        lbl_y = y_br + 0.07 if y_br != cy_main else y_br + 0.07
        ax.text(x_bend - 0.01, lbl_y, blabel,
                ha="right", va="bottom", fontsize=8, color="black")
        # Terminal box
        rounded_box(x_term, y_br, term_w, term_h, fill, txt,
                    fontsize=9, text_color=tc)

    # Bottom note
    ax.text(0.5, 0.03, "Re-evaluate if no validated prior art exists",
            ha="center", va="bottom", fontsize=8, color="0.4",
            transform=ax.transAxes)

    fig.tight_layout(pad=0.3)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Run all
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    out = os.path.dirname(os.path.abspath(__file__))

    fig1 = make_fig01()
    save(fig1, os.path.join(out, "fig_01_stagegate"))
    plt.close(fig1)

    fig2 = make_fig02()
    save(fig2, os.path.join(out, "fig_02_kano_map"))
    plt.close(fig2)

    fig3 = make_fig03()
    save(fig3, os.path.join(out, "fig_03_kano_csds"))
    plt.close(fig3)

    fig4 = make_fig04()
    save(fig4, os.path.join(out, "fig_04_scope_decision"))
    plt.close(fig4)

    print("All figures generated.")

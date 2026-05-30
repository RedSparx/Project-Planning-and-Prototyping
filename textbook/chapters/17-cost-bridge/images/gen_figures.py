"""
gen_figures.py — Chapter 17: Cost Analysis & the Bridge to Project II
Generates all three figures for Chapter 17.
Run from the images/ directory:  python gen_figures.py
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.6,
    "savefig.bbox": "tight",
})

GRAYS = ["0.0", "0.35", "0.55", "0.75"]

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def save(fig, stem):
    path_pdf = os.path.join(OUT_DIR, f"{stem}.pdf")
    path_png = os.path.join(OUT_DIR, f"{stem}.png")
    fig.savefig(path_pdf)
    fig.savefig(path_png, dpi=200)
    print(f"  Saved {stem}.pdf and {stem}.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Cost Projection — C_unit(N) vs N (log scale)
# ─────────────────────────────────────────────────────────────────────────────

def fig_01_cost_projection():
    fig, ax = plt.subplots(figsize=(8, 2.8))

    N = np.logspace(0, np.log10(600), 1200)
    C = 8000.0 / N + 480.0

    ax.plot(N, C, color="black", lw=1.6, zorder=3)
    ax.set_xscale("log")

    # --- Horizontal dashed line: c_var = $480
    ax.axhline(480, color="black", lw=1.2, ls="--", zorder=2, label=r"$c_\mathrm{var}=\$480$")
    ax.text(1.3, 455, r"$c_\mathrm{var}=\$480$", fontsize=9, va="top", ha="left", color="black")

    # --- Horizontal dashed line: price p = $1,200
    ax.axhline(1200, color="0.4", lw=1.2, ls="--", zorder=2)
    ax.text(1.3, 1240, r"$p=\$1{,}200$", fontsize=9, va="bottom", ha="left", color="0.4")

    # --- Vertical dashed line: N* = 14.3 (process break-even from Ch.12)
    ax.axvline(14.3, color="0.55", lw=1.2, ls="--", zorder=2)
    ax.text(14.3 * 1.07, 7500, r"$N^*=14.3$", fontsize=9, va="top", ha="left", color="0.55")

    # --- Annotated points — all text placed above the p=$1,200 line to avoid
    #     crowding in the compressed $480-$1,200 band at the bottom.
    data_pts = [(1,   8480),
                (15,  8000/15 + 480),
                (50,  640),
                (500, 496)]
    for (nx, cy) in data_pts:
        ax.scatter([nx], [cy], color="black", s=28, zorder=5)

    # N=1 — upper-left quadrant, plenty of room
    ax.annotate("N=1\n\\$8,480", xy=(1, 8480), xytext=(2.2, 6200),
                fontsize=9, va="bottom", ha="left",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))

    # N=15 — just left of the N* dashed line, text high up
    ax.annotate("N=15\n\\$1,013", xy=(15, 1013), xytext=(5.5, 4000),
                fontsize=9, va="bottom", ha="center",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))

    # N=50 — text to the right of N=15, above p line, include GM%
    ax.annotate("N=50: \\$640\nGM 46.7%", xy=(50, 640), xytext=(90, 3000),
                fontsize=9, va="bottom", ha="left",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))

    # N=500 — far right, text also above p line
    ax.annotate("N=500: \\$496\nGM 58.7%", xy=(500, 496), xytext=(300, 2000),
                fontsize=9, va="bottom", ha="left",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))

    ax.set_xlabel("Production Volume  N  (log scale)", fontsize=10)
    ax.set_ylabel(r"Unit Cost  $C_\mathrm{unit}$  (CAD)", fontsize=10)
    ax.set_xlim(0.8, 750)
    ax.set_ylim(300, 11500)
    ax.set_title("Unit-Cost Projection: Sorting Subsystem", fontsize=10, pad=4)

    import matplotlib.ticker as ticker
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"\\${x:,.0f}"))

    fig.tight_layout(pad=0.4)
    save(fig, "fig_01_cost_projection")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Prototype vs Production — paired horizontal bar chart
# ─────────────────────────────────────────────────────────────────────────────

def fig_02_proto_vs_prod():
    fig, ax = plt.subplots(figsize=(8, 2.8))

    scenarios = ["N = 1\n(Prototype)", "N = 50\n(Production)", "N = 500\n(Production)"]
    proto_cost = [8124.85, 8124.85, 8124.85]
    prod_cost  = [8124.85,  640.00,  496.00]

    y = np.arange(len(scenarios))
    bar_h = 0.32

    bars_proto = ax.barh(y + bar_h/2, proto_cost, height=bar_h,
                         color="0.35", label="Prototype cost/unit", zorder=3)
    bars_prod  = ax.barh(y - bar_h/2, prod_cost,  height=bar_h,
                         color="0.75", label="Production cost/unit", zorder=3)

    # Label each bar
    for bar, val in zip(bars_proto, proto_cost):
        ax.text(bar.get_width() + 40, bar.get_y() + bar.get_height()/2,
                f"\\${val:,.2f}", va="center", ha="left", fontsize=9)

    for bar, val in zip(bars_prod, prod_cost):
        x_pos = bar.get_width() + 40
        ax.text(x_pos, bar.get_y() + bar.get_height()/2,
                f"\\${val:,.2f}", va="center", ha="left", fontsize=9)

    ax.set_yticks(y)
    ax.set_yticklabels(scenarios, fontsize=10)
    ax.set_xlabel("Unit Cost (CAD)", fontsize=10)
    ax.set_title("Prototype Cost vs. Production Cost per Unit", fontsize=10, pad=4)
    ax.set_xlim(0, 10800)
    ax.legend(fontsize=9, loc="lower right", framealpha=1.0,
              edgecolor="black", fancybox=False)
    ax.grid(axis="x", alpha=0.3, linewidth=0.5)
    ax.grid(axis="y", alpha=0.0)

    import matplotlib.ticker as ticker
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"\\${x:,.0f}"))

    fig.tight_layout(pad=0.4)
    save(fig, "fig_02_proto_vs_prod")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: Gate 3 Readiness — two-column table as figure
# ─────────────────────────────────────────────────────────────────────────────

def fig_03_gate3_readiness():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.axis("off")

    left_header = "Project I Delivers"
    right_header = "Project II Must Resolve"

    left_items = [
        r"Proven sort accuracy ($\leq$100 ms latency)",
        "Validated power budget (50.5 days)",
        r"SF$\geq$2 for bracket (SF=5.29)",
        "AI inference working end-to-end",
        r"Costed BOM (\$124.85)",
        "Version-controlled DHF",
    ]
    right_items = [
        "Production-grade firmware (OTA update)",
        "Regulatory certification (FCC/ISED)",
        "Injection-moulded housing",
        "Supply-chain qualification",
        r"Cost reduction below $N_\mathrm{be}=12$",
        "Customer pilot program",
    ]

    n_rows = len(left_items)
    col_left_x  = 0.01
    col_right_x = 0.51
    col_w = 0.48
    header_h = 0.88
    row_h = (header_h - 0.06) / n_rows  # height per data row in axes fraction

    dark_gray_hdr  = "0.20"
    mid_gray_hdr   = "0.45"
    row_light      = "0.94"
    row_white      = "1.00"

    # Draw header boxes
    for (x, color, label) in [(col_left_x, dark_gray_hdr, left_header),
                               (col_right_x, mid_gray_hdr, right_header)]:
        rect = mpatches.FancyBboxPatch(
            (x, header_h - 0.02), col_w, 0.12,
            boxstyle="square,pad=0", linewidth=0.8,
            edgecolor="black", facecolor=color,
            transform=ax.transAxes, clip_on=False
        )
        ax.add_patch(rect)
        ax.text(x + col_w/2, header_h + 0.04, label,
                transform=ax.transAxes, fontsize=10, fontweight="bold",
                color="white", ha="center", va="center")

    # Draw alternating row backgrounds and text
    for i, (litem, ritem) in enumerate(zip(left_items, right_items)):
        row_y = header_h - 0.02 - (i + 1) * row_h
        face = row_light if i % 2 == 0 else row_white

        for x in [col_left_x, col_right_x]:
            rect = mpatches.FancyBboxPatch(
                (x, row_y), col_w, row_h,
                boxstyle="square,pad=0", linewidth=0.5,
                edgecolor="0.7", facecolor=face,
                transform=ax.transAxes, clip_on=False
            )
            ax.add_patch(rect)

        ax.text(col_left_x + 0.01, row_y + row_h/2, litem,
                transform=ax.transAxes, fontsize=9, va="center", ha="left")
        ax.text(col_right_x + 0.01, row_y + row_h/2, ritem,
                transform=ax.transAxes, fontsize=9, va="center", ha="left")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Gate 3 Readiness: What Was Proved vs. What Remains",
                 fontsize=10, pad=6)

    fig.tight_layout(pad=0.4)
    save(fig, "fig_03_gate3_readiness")
    plt.close(fig)


if __name__ == "__main__":
    print("Generating Chapter 17 figures …")
    fig_01_cost_projection()
    fig_02_proto_vs_prod()
    fig_03_gate3_readiness()
    print("Done.")

"""
gen_figures.py
Generate 3 figures for Chapter 12: Low-Volume Production Economics.
All figures are grayscale, 200 dpi PNG + PDF.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Shared style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.linewidth": 1.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "xtick.minor.width": 0.75,
    "ytick.minor.width": 0.75,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "lines.linewidth": 2.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

DPI = 200


def save(fig, stem):
    for ext in ("pdf", "png"):
        path = os.path.join(OUT_DIR, f"{stem}.{ext}")
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        print(f"  Saved {path}")


# ── Figure 1 — Unit Cost Curve ────────────────────────────────────────────────
def fig_unit_cost():
    fig, ax = plt.subplots(figsize=(7, 2.8))

    # Use log x-axis so the full hyperbola shape (from N=1) is visible
    N = np.logspace(0, np.log10(500), 1000)   # 1 … 500
    C = 8000 / N + 480

    ax.plot(N, C, color="black", lw=2, zorder=3)
    ax.set_xscale("log")

    # Asymptote dashed line
    ax.axhline(480, color="black", lw=1.5, ls="--", zorder=2)

    # Data points — N=1, 10, 50, 100, 500
    pts_N = [1, 10, 50, 100, 500]
    pts_C = [8000 / n + 480 for n in pts_N]
    ax.scatter(pts_N, pts_C, color="black", s=30, zorder=5)

    # Annotations — each placed at a distinct vertical/horizontal position
    # N=1: C=8480 — text below and right
    ax.annotate("N=1\n≈\$8,480",
                xy=(1, 8480), xytext=(3, 7200),
                fontsize=9, va="top", ha="left",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))
    # N=10: C=1280 — text right and above
    ax.annotate("N=10\n≈\$1,280",
                xy=(10, 1280), xytext=(14, 2200),
                fontsize=9, va="bottom", ha="left",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))
    # N=50: C=640 — text above
    ax.annotate("N=50: ≈\$640",
                xy=(50, 640), xytext=(50, 1400),
                fontsize=9, va="bottom", ha="center",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))
    # N=500: C=496 — text above dot, well separated from asymptote label
    ax.annotate("N=500: ≈\$496",
                xy=(500, 496), xytext=(500, 850),
                fontsize=9, va="bottom", ha="center",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))

    # Asymptote label placed left of N=500 annotation to avoid crowd
    # (draw after annotations so it renders on top)
    ax.text(1.2, 430, r"Asymptote: $c_\mathrm{var}$ = \$480",
            va="top", ha="left", fontsize=9.5)

    ax.set_xlabel("Production Volume  N  (log scale)", fontsize=10)
    ax.set_ylabel("Unit Cost  $C_{\\mathrm{unit}}$ (CAD)", fontsize=10)
    ax.set_xlim(0.8, 700)
    ax.set_ylim(300, 11000)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:g}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"\${x:,.0f}"))
    ax.set_title("Unit Cost vs. Production Volume", fontsize=10, pad=5)

    fig.tight_layout(pad=0.5)
    save(fig, "fig_01_unit_cost_curve")
    plt.close(fig)


# ── Figure 2 — Break-Even Analysis ───────────────────────────────────────────
def fig_breakeven():
    fig, ax = plt.subplots(figsize=(7, 2.8))

    N = np.linspace(0, 30, 300)
    C1 = 640 * N          # 3D-printing
    C2 = 8000 + 80 * N    # Injection moulding
    N_star = 8000 / (640 - 80)   # ≈14.286

    ax.plot(N, C1, color="black", lw=2, ls="-",  zorder=3, label="3D-printing")
    ax.plot(N, C2, color="black", lw=2, ls="--", zorder=3, label="Injection moulding")

    # N* vertical dotted line
    C_star = 640 * N_star
    ax.axvline(N_star, color="black", lw=1.2, ls=":", zorder=2)
    ax.scatter([N_star], [C_star], color="black", s=40, zorder=5)
    # Annotation: text above and left of crossing point
    ax.annotate(f"$N^*$ ≈ 14",
                xy=(N_star, C_star),
                xytext=(N_star - 6, C_star + 2500),
                fontsize=9,
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8),
                va="bottom", ha="center")

    # Region labels — keep inside the plot area, away from lines
    ax.text(5, 18000, "Print cheaper", fontsize=9, ha="center",
            color="black", style="italic")
    ax.text(24, 3500, "Mould cheaper", fontsize=9, ha="center",
            color="black", style="italic")

    # Line-end labels (right edge, shifted to avoid overlap with each other)
    ax.text(30.3, 640 * 30,       "3D-printing",       fontsize=9, va="center", ha="left")
    ax.text(30.3, 8000 + 80 * 30, "Injection moulding", fontsize=9, va="center", ha="left")

    ax.set_xlabel("Production Volume  N", fontsize=10)
    ax.set_ylabel("Total Cost (CAD)", fontsize=10)
    ax.set_xlim(-0.5, 36)
    ax.set_ylim(-500, 22000)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"\${x:,.0f}"))
    ax.set_title("Break-Even Analysis: 3D-Printing vs. Injection Moulding", fontsize=10, pad=5)
    # No legend box; labels are inline

    fig.tight_layout(pad=0.5)
    save(fig, "fig_02_breakeven")
    plt.close(fig)


# ── Figure 3 — Cost Committed vs. Cost Incurred ───────────────────────────────
def fig_cost_committed():
    fig, ax = plt.subplots(figsize=(7, 2.6))

    phases = ["Concept", "Design", "Prototype", "Production", "Field"]
    committed = [25, 75, 85, 95, 100]
    incurred  = [ 2,  8, 20,  60, 100]
    x = np.arange(len(phases))

    ax.plot(x, committed, color="black", lw=2, ls="-",  marker="o",
            markersize=5, label="Cost committed", zorder=3)
    ax.plot(x, incurred,  color="black", lw=2, ls="--", marker="s",
            markersize=5, label="Cost incurred",  zorder=3)

    # Fill between for visual emphasis
    ax.fill_between(x, committed, incurred, color="0.85", zorder=1)

    # Callout annotation at Design stage (index 1)
    # Place text box in the lower-right area (below Production line, above x-axis)
    ax.annotate("Design decisions lock in\n~75% of cost by end of Stage 2",
                xy=(1, committed[1]),
                xytext=(2.6, 38),
                fontsize=9,
                arrowprops=dict(arrowstyle="->", color="black", lw=0.9,
                                connectionstyle="arc3,rad=-0.2"),
                va="center", ha="left",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.8))

    ax.set_xticks(x)
    ax.set_xticklabels(phases, fontsize=9.5)
    ax.set_ylabel("Cumulative % of Total Cost", fontsize=10)
    ax.set_xlim(-0.4, 4.4)
    ax.set_ylim(-5, 115)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_title("Cost Committed vs. Cost Incurred by Project Phase", fontsize=10, pad=5)
    ax.legend(fontsize=9, loc="upper left", framealpha=1.0,
              edgecolor="black", fancybox=False)

    fig.tight_layout(pad=0.5)
    save(fig, "fig_03_cost_committed")
    plt.close(fig)


if __name__ == "__main__":
    print("Generating figures …")
    fig_unit_cost()
    fig_breakeven()
    fig_cost_committed()
    print("Done.")

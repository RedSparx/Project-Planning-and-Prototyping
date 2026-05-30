"""
gen_figures.py — Chapter 14: Validation & Test Procedure Design
Generates all four figures for Chapter 14 of the Project Planning & Prototyping textbook.
Run from:  textbook/chapters/14-validation/images/
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

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
    "image.cmap": "gray",
})
GRAYS = ["0.0", "0.35", "0.55", "0.75"]


def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    print(f"  Saved {stem}.pdf and {stem}.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 — Test Flow Flowchart
# ─────────────────────────────────────────────────────────────────────────────
def fig_01_test_flow():
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.6)
    ax.axis("off")
    ax.grid(False)

    # Node layout: x centres, y centre = 1.3
    y = 1.3
    step_fill = "0.85"
    dec_fill  = "0.65"
    lw = 1.5

    def rect(ax, cx, cy, w, h, label, fontsize=10):
        x0 = cx - w / 2
        y0 = cy - h / 2
        box = mpatches.FancyBboxPatch(
            (x0, y0), w, h,
            boxstyle="round,pad=0.05",
            linewidth=lw,
            edgecolor="black",
            facecolor=step_fill,
        )
        ax.add_patch(box)
        ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize, fontweight="bold")

    def diamond(ax, cx, cy, w, h, label, fontsize=9.5):
        dx, dy = w / 2, h / 2
        pts = [(cx, cy + dy), (cx + dx, cy), (cx, cy - dy), (cx - dx, cy)]
        poly = mpatches.Polygon(pts, closed=True, linewidth=lw,
                                edgecolor="black", facecolor=dec_fill)
        ax.add_patch(poly)
        ax.text(cx, cy, label, ha="center", va="center", fontsize=fontsize, fontweight="bold")

    def arrow(ax, x0, y0, x1, y1, label="", lbl_offset=(0, 0.15)):
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(arrowstyle="-|>", color="black",
                            lw=lw, mutation_scale=12),
        )
        if label:
            mx = (x0 + x1) / 2 + lbl_offset[0]
            my = (y0 + y1) / 2 + lbl_offset[1]
            ax.text(mx, my, label, ha="center", va="bottom", fontsize=9)

    bw = 1.1   # box width
    bh = 0.65  # box height

    # Nodes: Setup, Measure, Record, Pass/Fail, Done, Iterate
    nodes = {
        "setup":   1.0,
        "measure": 2.6,
        "record":  4.1,
        "dec":     5.7,
        "done":    7.5,
        "iter":    5.7,
    }

    rect(ax, nodes["setup"],   y,      bw, bh, "Setup")
    rect(ax, nodes["measure"], y,      bw, bh, "Measure")
    rect(ax, nodes["record"],  y,      bw, bh, "Record")
    diamond(ax, nodes["dec"],  y,     1.05, 0.85, "Pass?")
    rect(ax, nodes["done"],    y,      bw, bh, "Done", fontsize=10)
    rect(ax, nodes["iter"],    0.38,  bw, 0.50, "Iterate", fontsize=9.5)

    # Arrows
    arrow(ax, nodes["setup"]  + bw/2, y, nodes["measure"] - bw/2, y)
    arrow(ax, nodes["measure"] + bw/2, y, nodes["record"]  - bw/2, y)
    arrow(ax, nodes["record"]  + bw/2, y, nodes["dec"]     - 1.05/2, y)
    # Pass → Done
    arrow(ax, nodes["dec"] + 1.05/2, y, nodes["done"] - bw/2, y, "Pass", (0, 0.15))
    # Fail → down to Iterate
    ax.annotate("", xy=(nodes["dec"], 0.38 + 0.25),
                xytext=(nodes["dec"], y - 0.85/2),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=lw, mutation_scale=12))
    ax.text(nodes["dec"] + 0.12, 0.85, "Fail", ha="left", va="center", fontsize=9)
    # Iterate → left → back up to Measure
    ax.annotate("", xy=(nodes["measure"], y - bh/2),
                xytext=(nodes["measure"], 0.38 - 0.25),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=lw, mutation_scale=12))
    ax.plot([nodes["iter"] - bw/2, nodes["measure"], nodes["measure"]],
            [0.38, 0.38, 0.38 - 0.25 + 0.01],
            color="black", lw=lw)

    fig.tight_layout(pad=0.2)
    save(fig, "fig_01_test_flow")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 — Tolerance Band Scatter Plot
# ─────────────────────────────────────────────────────────────────────────────
def fig_02_tolerance_band():
    measurements = [98.2, 99.1, 97.8, 100.3, 98.9, 99.7, 98.5, 100.1, 99.4, 98.6]
    LSL = 96.0
    USL = 104.0
    xbar = np.mean(measurements)   # 99.06

    x = np.arange(1, 11)

    fig, ax = plt.subplots(figsize=(8, 2.8))

    # Shaded tolerance band
    ax.axhspan(LSL, USL, alpha=0.12, color="0.4", linewidth=0, label="Tolerance band")

    # Limit lines
    ax.axhline(LSL,  color="0.2", lw=1.5, ls="--", label=f"LSL = {LSL} ms")
    ax.axhline(USL,  color="0.2", lw=1.5, ls="--", label=f"USL = {USL} ms")
    ax.axhline(xbar, color="0.0", lw=1.5, ls="-.", label=fr"$\bar{{x}}$ = {xbar:.2f} ms")

    # Data points
    ax.scatter(x, measurements, color="0.0", s=40, zorder=5, marker="o")

    # Label x-bar on the right
    ax.text(10.25, xbar, fr"$\bar{{x}}$", va="center", ha="left", fontsize=10)

    # Annotations for LSL / USL on right
    ax.text(10.25, LSL, "LSL", va="center", ha="left", fontsize=9)
    ax.text(10.25, USL, "USL", va="center", ha="left", fontsize=9)

    ax.set_xlabel("Sample index", fontsize=10)
    ax.set_ylabel("Latency (ms)", fontsize=10)
    # No in-figure title — LaTeX caption handles it
    ax.set_xticks(x)
    ax.set_xlim(0.3, 11.0)
    ax.set_ylim(94.5, 106.0)
    ax.tick_params(labelsize=9)

    fig.tight_layout(pad=0.3)
    save(fig, "fig_02_tolerance_band")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 — Normal Distribution Curve
# ─────────────────────────────────────────────────────────────────────────────
def fig_03_distribution():
    xbar = 99.06
    s    = 0.77
    LSL  = 96.0
    USL  = 104.0

    x = np.linspace(xbar - 4.5*s, xbar + 4.5*s, 500)
    y = (1 / (s * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - xbar) / s) ** 2)

    fig, ax = plt.subplots(figsize=(8, 2.8))

    # ±3σ shaded region
    mask3 = (x >= xbar - 3*s) & (x <= xbar + 3*s)
    ax.fill_between(x, y, where=mask3, color="0.75", alpha=0.7,
                    label=r"$\pm 3\sigma$ region")

    # Curve
    ax.plot(x, y, color="0.0", lw=1.8)

    y_top = y.max()

    def vline(val, label, ls, ymax_frac=0.90, offset_x=0.0, va="bottom"):
        yv = (1/(s*np.sqrt(2*np.pi))) * np.exp(-0.5*((val - xbar)/s)**2)
        ax.axvline(val, color="0.2", lw=1.2, ls=ls, alpha=0.85)
        ax.text(val + offset_x, y_top * ymax_frac, label,
                ha="center", va=va, fontsize=8.5, rotation=90)

    vline(xbar,        r"$\bar{x}$",      "-",  0.88,  0.07)
    vline(xbar + s,    r"$\bar{x}+s$",    "--", 0.70,  0.07)
    vline(xbar - s,    r"$\bar{x}-s$",    "--", 0.70, -0.07)
    vline(xbar + 3*s,  r"$\bar{x}+3s$",   ":",  0.55,  0.07)
    vline(xbar - 3*s,  r"$\bar{x}-3s$",   ":",  0.55, -0.07)
    vline(LSL,         "LSL",             "-.",  0.38,  0.07)
    vline(USL,         "USL",             "-.",  0.38, -0.07)

    ax.set_xlabel("Latency (ms)", fontsize=10)
    ax.set_ylabel("Probability density", fontsize=10)
    # No in-figure title — LaTeX caption handles it
    ax.set_ylim(bottom=0)
    ax.tick_params(labelsize=9)
    ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%.2f"))

    fig.tight_layout(pad=0.3)
    save(fig, "fig_03_distribution")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 4 — Fault Tree Diagram
# ─────────────────────────────────────────────────────────────────────────────
def fig_04_fault_tree():
    fig, ax = plt.subplots(figsize=(9, 3.0))
    ax.set_xlim(0, 9)
    ax.set_ylim(-0.25, 2.8)
    ax.axis("off")
    ax.grid(False)

    lw_box  = 1.4
    lw_line = 1.3
    box_fill = "0.88"
    gate_fill = "0.65"

    def event_box(cx, cy, w, h, lines):
        """Draw event box with multi-line text."""
        x0 = cx - w/2
        y0 = cy - h/2
        rect = mpatches.FancyBboxPatch((x0, y0), w, h,
                                        boxstyle="round,pad=0.04",
                                        linewidth=lw_box,
                                        edgecolor="black", facecolor=box_fill)
        ax.add_patch(rect)
        text = "\n".join(lines)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=8.5,
                linespacing=1.3, fontweight="bold")

    def or_gate(cx, cy, size=0.28):
        """Draw OR gate (triangle shape)."""
        pts = [(cx - size, cy - size*0.6),
               (cx + size, cy - size*0.6),
               (cx, cy + size*0.9)]
        poly = mpatches.Polygon(pts, closed=True, linewidth=lw_box,
                                edgecolor="black", facecolor=gate_fill)
        ax.add_patch(poly)
        ax.text(cx, cy - size*0.1, "OR", ha="center", va="center",
                fontsize=7.5, fontweight="bold")

    def and_gate(cx, cy, size=0.25):
        """Draw AND gate (flat arc/D shape)."""
        # Draw as a rectangle with rounded top
        rect = mpatches.FancyBboxPatch((cx - size, cy - size*0.6),
                                       2*size, size*1.3,
                                       boxstyle="round,pad=0.03",
                                       linewidth=lw_box,
                                       edgecolor="black", facecolor=gate_fill)
        ax.add_patch(rect)
        ax.text(cx, cy, "AND", ha="center", va="center",
                fontsize=7.0, fontweight="bold")

    def line(x0, y0, x1, y1):
        ax.plot([x0, x1], [y0, y1], color="black", lw=lw_line)

    def arrow_down(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="black",
                                   lw=lw_line, mutation_scale=10))

    # ── Layout constants ──────────────────────────────────────────────────────
    # Top event
    top_cx, top_cy = 4.5, 2.35
    event_box(top_cx, top_cy, 2.0, 0.55, ["Sort failure", "P = 0.0511"])

    # OR gate below top event
    or_cx, or_cy = 4.5, 1.72
    or_gate(or_cx, or_cy, 0.26)
    line(top_cx, top_cy - 0.275, or_cx, or_cy + 0.26*0.9)

    # Left sub-event: Sensor error
    sen_cx, sen_cy = 2.2, 1.05
    event_box(sen_cx, sen_cy, 1.9, 0.52, ["Sensor error", "P = 0.05"])

    # Right sub-event: Actuator jam (AND result)
    act_cx, act_cy = 6.8, 1.05
    event_box(act_cx, act_cy, 1.9, 0.52, ["Actuator jam", "P = 0.0012"])

    # Lines from OR gate to sub-events
    line(or_cx, or_cy - 0.26*0.6, or_cx, 1.45)
    # Branch left
    line(or_cx, 1.45, sen_cx, 1.45)
    arrow_down(sen_cx, 1.45, sen_cx, sen_cy + 0.26)
    # Branch right
    line(or_cx, 1.45, act_cx, 1.45)
    arrow_down(act_cx, 1.45, act_cx, act_cy + 0.26)

    # AND gate below actuator jam
    and_cx, and_cy = act_cx, 0.68
    and_gate(and_cx, and_cy, 0.23)
    line(act_cx, act_cy - 0.26, and_cx, and_cy + 0.23*0.7)

    # Leaf events under AND gate
    mech_cx, mech_cy = 6.0, 0.22
    elec_cx, elec_cy = 7.6, 0.22

    event_box(mech_cx, mech_cy, 1.55, 0.38, ["Mech. jam", "P_mech = 0.03"])
    event_box(elec_cx, elec_cy, 1.55, 0.38, ["Elec. fault", "P_elec = 0.04"])

    # Lines from AND gate to leaf events
    line(and_cx, and_cy - 0.23*0.6, and_cx, 0.42)
    line(and_cx, 0.42, mech_cx, 0.42)
    arrow_down(mech_cx, 0.42, mech_cx, mech_cy + 0.19)
    line(and_cx, 0.42, elec_cx, 0.42)
    arrow_down(elec_cx, 0.42, elec_cx, elec_cy + 0.19)

    fig.tight_layout(pad=0.1)
    save(fig, "fig_04_fault_tree")
    plt.close(fig)


# ─── Run all ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Chapter 14 figures...")
    fig_01_test_flow()
    fig_02_tolerance_band()
    fig_03_distribution()
    fig_04_fault_tree()
    print("Done.")

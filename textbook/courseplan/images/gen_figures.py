"""
gen_figures.py — Course Plan figures
Generates two figures for the standalone Course Plan document.
Run from the images/ directory:  python gen_figures.py
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "savefig.bbox": "tight",
})

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def save(fig, stem):
    path_pdf = os.path.join(OUT_DIR, f"{stem}.pdf")
    path_png = os.path.join(OUT_DIR, f"{stem}.png")
    fig.savefig(path_pdf)
    fig.savefig(path_png, dpi=200)
    print(f"  Saved {stem}.pdf and {stem}.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Stage-Gate course context (horizontal stages, course shaded)
# ─────────────────────────────────────────────────────────────────────────────

def fig_01_stagegate_course():
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.axis("off")
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 1)

    stages = [
        ("Stage 0\nDiscovery",           0.25, 1.25),
        ("Stage 1\nScoping",             1.5,  2.5),
        ("Stage 2\nBuild Business\nCase",2.75, 4.25),
        ("Stage 3\nDevelopment",         4.5,  6.5),
        ("Stage 4\nTesting &\nValidation",6.75, 8.25),
    ]

    # Gate x-positions at the right edge of each stage box
    gates = [1.25, 2.5, 4.25, 6.5, 8.25]

    # Horizontal flow arrow runs BELOW the boxes (at y=0.22)
    flow_y = 0.22
    ax.annotate("", xy=(8.9, flow_y), xytext=(0.0, flow_y),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2))

    # Gate diamond markers sit on the flow line
    gate_labels = ["G0", "G1", "G2", "G3", "G4"]
    for gx, gl in zip(gates, gate_labels):
        ax.plot([gx], [flow_y], marker="D", color="black",
                markersize=6, zorder=5)
        ax.text(gx, flow_y - 0.14, gl, fontsize=8, ha="center", va="center",
                color="black")

    # Stage boxes sit ABOVE the flow line
    box_y0 = flow_y + 0.04
    box_h  = 0.52
    for (label, x0, x1) in stages:
        in_course = "Stage 2" in label or "Stage 3" in label
        face = "0.78" if in_course else "0.94"
        lw   = 1.4   if in_course else 0.8
        rect = mpatches.FancyBboxPatch(
            (x0, box_y0), x1 - x0, box_h,
            boxstyle="round,pad=0.03", linewidth=lw,
            edgecolor="black", facecolor=face
        )
        ax.add_patch(rect)
        ax.text((x0 + x1) / 2, box_y0 + box_h / 2, label,
                fontsize=8.5, ha="center", va="center")

    # Brace showing course scope between G2 and G3
    g2x, g3x = gates[2], gates[3]
    brace_y = box_y0 + box_h + 0.07
    ax.annotate("", xy=(g3x, brace_y), xytext=(g2x, brace_y),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax.text((g2x + g3x) / 2, brace_y + 0.10,
            "This course  (Gate 2 → Gate 3)",
            fontsize=9, ha="center", va="center", fontstyle="italic")

    ax.set_title("Stage-Gate Context: Where This Course Fits",
                 fontsize=10, pad=4)
    fig.tight_layout(pad=0.3)
    save(fig, "fig_01_stagegate_course")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: 12-week milestone timeline
# ─────────────────────────────────────────────────────────────────────────────

def fig_02_milestone_timeline():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.axis("off")
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(0, 1)

    weeks = list(range(1, 13))

    # Background shading: three phases
    phase_spans = [
        (0.5, 6.5, "Phase 1: Design\n(Ch. 1–10)", "0.92"),
        (6.5, 9.5, "Phase 2: Build &\nVerify (Ch. 11–14)", "0.80"),
        (9.5, 12.5, "Phase 3: Close\n(Ch. 15–17)", "0.68"),
    ]
    for (x0, x1, label, gray) in phase_spans:
        rect = mpatches.FancyBboxPatch(
            (x0, 0.30), x1 - x0, 0.40,
            boxstyle="square,pad=0", linewidth=0.6,
            edgecolor="0.5", facecolor=gray
        )
        ax.add_patch(rect)
        ax.text((x0 + x1) / 2, 0.50, label,
                fontsize=8, ha="center", va="center")

    # Week tick marks and numbers
    for w in weeks:
        ax.plot([w, w], [0.28, 0.32], color="black", lw=0.8)
        ax.text(w, 0.20, str(w), fontsize=8, ha="center", va="center",
                color="0.3")

    ax.text(0.0, 0.20, "Wk", fontsize=8, ha="center", va="center", color="0.3")

    # Horizontal baseline
    ax.plot([0.5, 12.5], [0.30, 0.30], color="black", lw=1.0)

    # Milestone markers
    milestones = [
        (6,  0.80, "M1\nSpec. Review"),
        (9,  0.80, "M2\nBuild Review"),
        (12, 0.80, "M3\nGate 3\nPresentation"),
    ]
    for (wx, wy, label) in milestones:
        ax.plot([wx], [0.30], marker="^", color="black", markersize=9, zorder=5)
        ax.plot([wx, wx], [0.30, wy - 0.08], color="black", lw=0.8, ls="--")
        ax.text(wx, wy, label, fontsize=8.5, ha="center", va="bottom",
                fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="black", linewidth=0.8))

    ax.set_title("12-Week Course Timeline and Milestones", fontsize=10, pad=4)
    fig.tight_layout(pad=0.3)
    save(fig, "fig_02_milestone_timeline")
    plt.close(fig)


if __name__ == "__main__":
    print("Generating Course Plan figures ...")
    fig_01_stagegate_course()
    fig_02_milestone_timeline()
    print("Done.")

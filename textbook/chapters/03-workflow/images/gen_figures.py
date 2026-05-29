"""
gen_figures.py  —  Chapter 2 figure generator (self-contained)

Figures produced
----------------
fig_01_workflow        : Horizontal 7-stage Prototype Development Cycle  (9 × 2.5 in)
fig_02_fidelity_ladder : Effort vs fidelity ladder                        (7 × 2.8 in)
fig_03_value           : Intrinsic vs extrinsic prototype value           (6 × 2.8 in)

All figures satisfy: H ≤ 3.0 in, W/H ≥ 1.6.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrowPatch
import numpy as np
import os

IMGDIR = os.path.dirname(os.path.abspath(__file__))

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "axes.grid": False,
    "grid.alpha": 0.3,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.6,
    "savefig.bbox": "tight",
    "image.cmap": "gray",
})


def save(fig, stem):
    fig.savefig(os.path.join(IMGDIR, f"{stem}.pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(IMGDIR, f"{stem}.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {stem}.pdf + .png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: fig_01_workflow  — horizontal 7-stage Prototype Development Cycle
# ─────────────────────────────────────────────────────────────────────────────
print("Generating fig_01_workflow ...")

stages = [
    "1. Specification\n& Risk",
    "2. Scoping\n& Planning",
    "3. Architecture",
    "4. Subsystem\nDesign",
    "5. Build &\nIntegration",
    "6. Validate\n& Measure",
    "7. Compile\n& Economics",
]
n = len(stages)

fig1, ax1 = plt.subplots(figsize=(9, 2.5))
ax1.set_axis_off()
ax1.set_xlim(0, 9)
ax1.set_ylim(-1.5, 2.5)
ax1.grid(False)

# Box geometry (in data coords — axes is 9 wide, 4 tall)
box_w = 1.05          # box width
box_h = 1.05          # box height
row_y_centre = 1.05   # y-centre of each box row

# Evenly space 7 boxes across [0.25, 8.75]
margin = 0.25
total_span = 9.0 - 2 * margin
step = total_span / (n - 1)   # centre-to-centre spacing
centres_x = [margin + i * step for i in range(n)]

stage_shades = [0.20, 0.40] * 4   # alternating; slice to 7

box_centres = []  # (cx, cy) for arrowheads

for i, (label, cx) in enumerate(zip(stages, centres_x)):
    shade = stage_shades[i % 2]
    x0 = cx - box_w / 2
    y0 = row_y_centre - box_h / 2
    rect = mpatches.FancyBboxPatch(
        (x0, y0), box_w, box_h,
        boxstyle="round,pad=0.06",
        facecolor=str(shade), edgecolor="black", linewidth=1.2,
        clip_on=False,
        zorder=3,
    )
    ax1.add_patch(rect)
    text_color = "white"   # both 0.20 and 0.40 are dark enough for white text
    ax1.text(
        cx, row_y_centre, label,
        ha="center", va="center",
        fontsize=8.5, color=text_color, fontweight="bold",
        zorder=4,
    )
    box_centres.append((cx, row_y_centre))

# Right-pointing arrows between consecutive boxes
for i in range(n - 1):
    cx_left  = centres_x[i] + box_w / 2
    cx_right = centres_x[i + 1] - box_w / 2
    mid_x = (cx_left + cx_right) / 2
    ax1.annotate(
        "",
        xy=(cx_right, row_y_centre),
        xytext=(cx_left, row_y_centre),
        arrowprops=dict(
            arrowstyle="-|>",
            color="black",
            lw=1.4,
            mutation_scale=10,
        ),
        zorder=5,
    )

# ── Iterate loop: curved arrow BELOW the row from Stage 6 back to Stage 4 ──
# Stage indices (0-based): Stage 4 = index 3, Stage 6 = index 5
idx_design   = 3   # Subsystem Design
idx_validate = 5   # Validate & Measure

cx_d = centres_x[idx_design]
cx_v = centres_x[idx_validate]

y_box_bottom = row_y_centre - box_h / 2  # bottom edge of boxes

# FancyArrowPatch in data coordinates — curves downward (rad=-0.5)
arrow_loop = FancyArrowPatch(
    posA=(cx_v, y_box_bottom),   # start: bottom of Stage 6
    posB=(cx_d, y_box_bottom),   # end:   bottom of Stage 4
    connectionstyle="arc3,rad=-0.5",
    arrowstyle="-|>",
    color="0.20",
    linewidth=1.5,
    mutation_scale=11,
    zorder=2,
)
ax1.add_patch(arrow_loop)

# Label: centred below the arc
label_x = (cx_d + cx_v) / 2
label_y = y_box_bottom - 0.82   # below the arc
ax1.text(
    label_x, label_y,
    "Iterate if needed",
    ha="center", va="center",
    fontsize=8.5, fontstyle="italic", color="0.20",
)

# Title
ax1.set_title(
    "Prototype Development Cycle",
    fontsize=11, fontweight="bold", pad=4,
)

fig1.tight_layout(pad=0.3)
save(fig1, "fig_01_workflow")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: fig_02_fidelity_ladder  — effort vs fidelity level
# Resized to (7, 2.8); content identical to original
# ─────────────────────────────────────────────────────────────────────────────
print("Generating fig_02_fidelity_ladder ...")

# Restore grid for this figure
mpl.rcParams.update({"axes.grid": True})

labels_f = [
    "Sketch /\nSimulation",
    "Proof-of-\nconcept",
    "Functional\nprototype",
    "Looks-like /\nWorks-like",
    "Pre-production\npilot",
]
x = np.array([1, 2, 3, 4, 5])
effort = np.array([1.0, 3.0, 8.5, 22.0, 55.0])

qa_x = 2
qa_effort = effort[1]   # effort at PoC

fig2, ax2 = plt.subplots(figsize=(7, 2.8))

# Shaded saved-effort region
x_dense = np.linspace(qa_x, x[-1], 300)
effort_dense = np.interp(x_dense, x, effort)
ax2.fill_between(
    x_dense, qa_effort, effort_dense,
    color="0.82", hatch="///", edgecolor="0.50",
    linewidth=0.6, label="Effort saved",
)

# Main curve
ax2.plot(x, effort, color="black", lw=2.0, marker="o",
         markersize=6, markerfacecolor="black", zorder=5)

# Horizontal dashed threshold
ax2.axhline(qa_effort, color="0.30", lw=1.4, linestyle="--",
            label='"Question answered" threshold')

# Annotation arrow
ax2.annotate(
    "Question answered here",
    xy=(qa_x, qa_effort),
    xytext=(qa_x - 0.15, qa_effort * 5.0),
    fontsize=9,
    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2),
    ha="left", va="center",
)

# Label for shaded region
ax2.text(
    4.1, 10.0,
    "Effort saved\nby stopping early",
    ha="center", va="center",
    fontsize=8.5, fontstyle="italic", color="0.25",
)

ax2.set_xticks(x)
ax2.set_xticklabels(labels_f, fontsize=9)
ax2.set_ylabel("Relative Effort / Cost (log scale)", fontsize=9.5)
ax2.set_xlabel("Fidelity Level", fontsize=9.5)
ax2.set_yscale("log")
ax2.set_xlim(0.5, 5.5)
ax2.set_ylim(0.5, 120)
ax2.set_title("Fidelity Ladder: Effort Rises Steeply with Fidelity",
              fontsize=10, fontweight="bold")
ax2.legend(fontsize=8.5, loc="upper left")
ax2.grid(True, which="both", alpha=0.3, linewidth=0.5)

fig2.tight_layout(pad=0.4)
save(fig2, "fig_02_fidelity_ladder")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: fig_03_value  — Intrinsic vs Extrinsic value
# Resized to (6, 2.8); content identical to original
# ─────────────────────────────────────────────────────────────────────────────
print("Generating fig_03_value ...")

categories = ["Low-Fidelity\nPrototype", "High-Fidelity\nPrototype"]
intrinsic = [0.82, 0.72]
extrinsic = [0.22, 0.78]

x_pos = np.array([0, 1])
bar_w = 0.30
sep   = 0.05

fig3, ax3 = plt.subplots(figsize=(6, 2.8))

# Intrinsic bars
bars_i = ax3.bar(
    x_pos - bar_w / 2 - sep / 2, intrinsic, bar_w,
    facecolor="0.25", hatch="///", edgecolor="black", linewidth=1.0,
    label="Intrinsic value\n(knowledge gained, risk reduced)",
)

# Extrinsic bars
bars_e = ax3.bar(
    x_pos + bar_w / 2 + sep / 2, extrinsic, bar_w,
    facecolor="0.65", hatch="\\\\\\", edgecolor="black", linewidth=1.0,
    label="Extrinsic value\n(artifact quality, stakeholder confidence)",
)

ax3.set_xticks(x_pos)
ax3.set_xticklabels(categories, fontsize=10)
ax3.set_ylabel("Relative Value (0 – 1 scale)", fontsize=9.5)
ax3.set_ylim(0, 1.25)
ax3.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.28),
           ncol=2, frameon=True)

ax3.set_title("Intrinsic vs Extrinsic Prototype Value",
              fontsize=10, fontweight="bold", pad=4)

# Annotation in data-coords near top of plot area, above all bars (max bar = 0.82)
ax3.text(
    0.5, 1.17,
    "Risk reduction is similar; artifact quality is not.",
    ha="center", va="center",
    fontsize=8.5, fontstyle="italic", color="0.35",
)

# Value labels on bars
for bar in list(bars_i) + list(bars_e):
    h = bar.get_height()
    ax3.text(
        bar.get_x() + bar.get_width() / 2, h + 0.015,
        f"{h:.2f}", ha="center", va="bottom", fontsize=8, color="black",
    )

ax3.grid(True, axis="y", alpha=0.3, linewidth=0.5)
ax3.set_axisbelow(True)

fig3.tight_layout(pad=0.4)
save(fig3, "fig_03_value")

print("\nAll figures generated successfully.")

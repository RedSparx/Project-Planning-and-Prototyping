import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.grid": False,
    "savefig.bbox": "tight"
})

OUT = "/home/user/Project-Planning-and-Prototyping/textbook/chapters/08-ai/images"

def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    plt.close(fig)


# ─────────────────────────────────────────────
# FIGURE 1 — fig_01_hitl_loop
# ─────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(8, 2.6))
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis("off")

# Box layout: 4 boxes evenly spaced, centered vertically
box_w = 0.17
box_h = 0.38
box_y = 0.52   # bottom of boxes (top half of figure)
gap = 0.055    # gap between boxes
total_span = 4 * box_w + 3 * gap
x_start = (1 - total_span) / 2

boxes = [
    {"label": "AI Tool\nProposes",   "fc": "0.75"},
    {"label": "Engineer\nVerifies",  "fc": "0.60"},
    {"label": "Accept or\nReject",   "fc": "0.75"},
    {"label": "Document\n& Commit",  "fc": "0.50"},
]

centers = []
for i, b in enumerate(boxes):
    x = x_start + i * (box_w + gap)
    rect = FancyBboxPatch((x, box_y), box_w, box_h,
                          boxstyle="round,pad=0.01",
                          fc=b["fc"], ec="0.30", lw=1.0)
    ax1.add_patch(rect)
    cx = x + box_w / 2
    cy = box_y + box_h / 2
    centers.append((cx, cy))
    ax1.text(cx, cy, b["label"], ha="center", va="center",
             fontsize=10, color="black", linespacing=1.4)

# Forward arrows between consecutive boxes
arrow_kw = dict(arrowstyle="-|>", color="0.20", lw=1.2,
                mutation_scale=12, connectionstyle="arc3,rad=0")
for i in range(3):
    x0 = x_start + i * (box_w + gap) + box_w
    x1 = x_start + (i + 1) * (box_w + gap)
    mid_y = box_y + box_h / 2
    ax1.annotate("", xy=(x1, mid_y), xytext=(x0, mid_y),
                 arrowprops=dict(arrowstyle="-|>", color="0.20", lw=1.2,
                                 mutation_scale=12))

# Curved "Reject → revise prompt" arc below boxes, from box3 bottom to box1 bottom
# Use a negative rad to curve BELOW the anchor points
x_from = centers[2][0]   # center-x of "Accept or Reject"
x_to   = centers[0][0]   # center-x of "AI Tool Proposes"
y_base = box_y            # bottom edge of boxes

from matplotlib.patches import FancyArrowPatch

arc_patch = FancyArrowPatch(
    posA=(x_from, y_base),
    posB=(x_to, y_base),
    arrowstyle="-|>",
    color="0.30",
    lw=1.1,
    mutation_scale=12,
    connectionstyle="arc3,rad=-0.5"   # negative rad → bulges downward
)
ax1.add_patch(arc_patch)

# Label below the arc midpoint
label_x = (x_from + x_to) / 2
label_y = y_base - 0.22
ax1.text(label_x, label_y, "Reject → revise prompt",
         ha="center", va="top", fontsize=9, color="0.25", style="italic")

fig1.tight_layout(pad=0.3)
save(fig1, f"{OUT}/fig_01_hitl_loop")
print("Figure 1 saved.")


# ─────────────────────────────────────────────
# FIGURE 2 — fig_02_trust_matrix
# ─────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(7, 2.8))
ax2.set_xlim(0, 2)
ax2.set_ylim(0, 2)

# Draw 4 quadrants as filled rectangles
quads = [
    # (x, y, w, h, fc, label)
    (0, 1, 1, 1, "0.85", "Use with\nspot-check"),           # top-left
    (1, 1, 1, 1, "0.65", "Verify\nindependently"),           # top-right
    (0, 0, 1, 1, "0.75", "Accept with\ncaution"),            # bottom-left
    (1, 0, 1, 1, "0.45", "Do not use without\nfull verification"),  # bottom-right
]

for (x, y, w, h, fc, label) in quads:
    rect = mpatches.Rectangle((x, y), w, h, fc=fc, ec="0.25", lw=1.2)
    ax2.add_patch(rect)
    # text color: white for dark quadrant (0.45), black for others
    tc = "white" if float(fc) < 0.55 else "black"
    ax2.text(x + w/2, y + h/2, label,
             ha="center", va="center",
             fontsize=9.5, color=tc, linespacing=1.4)

# Grid lines
ax2.axhline(1, color="0.25", lw=1.2)
ax2.axvline(1, color="0.25", lw=1.2)

# Axis labels
ax2.set_xlabel("Consequence of Error", fontsize=10, labelpad=4)
ax2.set_ylabel("AI Confidence", fontsize=10, labelpad=4)

# Custom tick labels
ax2.set_xticks([0.5, 1.5])
ax2.set_xticklabels(["Low", "High"], fontsize=9)
ax2.set_yticks([0.5, 1.5])
ax2.set_yticklabels(["Low", "High"], fontsize=9)

ax2.tick_params(length=0)
for spine in ax2.spines.values():
    spine.set_linewidth(1.2)
    spine.set_edgecolor("0.25")

fig2.tight_layout(pad=0.4)
save(fig2, f"{OUT}/fig_02_trust_matrix")
print("Figure 2 saved.")

print("All figures generated successfully.")

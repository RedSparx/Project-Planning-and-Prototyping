"""
gen_figures.py
Generates 3 figures for Chapter 11: Bill of Materials & Procurement.
All figures: grayscale only, H <= 3 inches, text >= 9pt, lines >= 1pt.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def save_fig(fig, name):
    pdf_path = os.path.join(OUT_DIR, f"{name}.pdf")
    png_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
    fig.savefig(png_path, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"  Saved {name}.pdf and {name}.png")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 — fig_01_doc_chain
# Horizontal procurement document chain with feedback arc
# ─────────────────────────────────────────────────────────────────────────────
def make_fig1():
    fig, ax = plt.subplots(figsize=(9, 2.2))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.2)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    labels = ["BOM", "Purchase\nList", "Supplier\nQuote", "Purchase\nOrder",
              "Receipt /\nInvoice", "As-Built\nBOM"]
    n = len(labels)

    box_w = 1.18
    box_h = 0.58
    # Distribute boxes evenly across the 9-inch width with margins
    total_margin = 9 - n * box_w
    gap = total_margin / (n + 1)
    box_y = 0.38  # bottom of box (centred vertically in lower half)
    box_centers_x = [gap + i * (box_w + gap) + box_w / 2 for i in range(n)]

    FILL = 0.75
    for i, (label, cx) in enumerate(zip(labels, box_centers_x)):
        rect = FancyBboxPatch(
            (cx - box_w / 2, box_y), box_w, box_h,
            boxstyle="square,pad=0.02",
            linewidth=1.0,
            edgecolor='black',
            facecolor=str(FILL)
        )
        ax.add_patch(rect)
        ax.text(cx, box_y + box_h / 2, label,
                ha='center', va='center', fontsize=9, fontweight='bold',
                color='black', linespacing=1.3)

    # Forward arrows between boxes
    for i in range(n - 1):
        x_start = box_centers_x[i] + box_w / 2
        x_end   = box_centers_x[i + 1] - box_w / 2
        y_mid   = box_y + box_h / 2
        ax.annotate("", xy=(x_end, y_mid), xytext=(x_start, y_mid),
                    arrowprops=dict(arrowstyle="-|>", color='black',
                                   lw=1.5, mutation_scale=12))

    # Feedback arc: As-Built BOM -> BOM (curved arc ABOVE boxes)
    x_from = box_centers_x[-1]  # As-Built BOM centre (right)
    x_to   = box_centers_x[0]   # BOM centre (left)
    # Arc goes from top of As-Built BOM box upward and back to top of BOM box
    # Use rad > 0 so arc bows upward when going right-to-left
    style = "arc3,rad=0.5"
    ax.annotate("",
                xy=(x_to, box_y + box_h),        # arrow tip: top of BOM box
                xytext=(x_from, box_y + box_h),   # tail: top of As-Built BOM box
                arrowprops=dict(
                    arrowstyle="-|>",
                    color='black',
                    lw=1.5,
                    mutation_scale=12,
                    connectionstyle=style
                ))

    # Label "Reconciliation" above midpoint of arc
    mid_x = (x_from + x_to) / 2
    ax.text(mid_x, 1.90, "Reconciliation", ha='center', va='bottom',
            fontsize=9, fontstyle='italic', color='black')

    save_fig(fig, "fig_01_doc_chain")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 — fig_02_bom_tree
# Multi-level BOM tree (hierarchical top-down)
# ─────────────────────────────────────────────────────────────────────────────
def make_fig2():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    GRAY = {0: '0.35', 1: '0.55', 2: '0.80'}
    TEXT_COLOR = {0: 'white', 1: 'white', 2: 'black'}

    box_h = 0.44
    # Level y-positions (top of box): L0=top, L2=bottom
    # figsize height = 2.8 inches; need room for boxes and connectors
    y_top = {0: 2.25, 1: 1.55, 2: 0.72}

    # ── Level 0 ──
    l0 = [{"label": "Sorter\nSystem", "x": 4.5}]

    # ── Level 1 ──
    l1 = [
        {"label": "Control\nSubsystem",     "x": 1.55},
        {"label": "Actuation\nSubsystem",   "x": 4.50},
        {"label": "Enclosure\n& HW",        "x": 7.45},
    ]

    # ── Level 2 (children list aligned per L1 parent) ──
    l2_groups = [
        # under Control
        [{"label": "MCU Board", "x": 0.65},
         {"label": "MQTT\nRadio",  "x": 1.55},
         {"label": "Motor\nDriver","x": 2.45}],
        # under Actuation
        [{"label": "Sort Gate\nActuator",  "x": 3.50},
         {"label": "Conveyor\nMotor",      "x": 4.50},
         {"label": "Sensors\n(×2)",        "x": 5.50}],
        # under Enclosure
        [{"label": "Acrylic\nPanels",      "x": 6.80},
         {"label": "Fasteners",            "x": 7.80}],
    ]

    bw_l0 = 1.35
    bw_l1 = 1.35
    bw_l2 = 0.88

    def draw_box(cx, y_top_val, w, level, label):
        rect = FancyBboxPatch(
            (cx - w / 2, y_top_val - box_h), w, box_h,
            boxstyle="square,pad=0.02",
            linewidth=1.0,
            edgecolor='black',
            facecolor=GRAY[level]
        )
        ax.add_patch(rect)
        ax.text(cx, y_top_val - box_h / 2, label,
                ha='center', va='center',
                fontsize=9, color=TEXT_COLOR[level],
                linespacing=1.25)

    def draw_connector(x1, y1, x2, y2):
        """Draw L-shaped connector: vertical down from (x1,y1) to mid, horizontal to (x2, mid), vertical to (x2,y2)."""
        mid_y = (y1 + y2) / 2
        ax.plot([x1, x1], [y1, mid_y], color='black', lw=1.2)
        ax.plot([x1, x2], [mid_y, mid_y], color='black', lw=1.2)
        ax.plot([x2, x2], [mid_y, y2], color='black', lw=1.2)

    # Draw L0
    for node in l0:
        draw_box(node['x'], y_top[0], bw_l0, 0, node['label'])

    # Draw L1 + connectors from L0
    for node in l1:
        draw_box(node['x'], y_top[1], bw_l1, 1, node['label'])
        # connector: bottom of L0 box to top of L1 box
        draw_connector(l0[0]['x'], y_top[0] - box_h,
                       node['x'],  y_top[1])

    # Draw L2 + connectors from L1
    for gi, (parent, children) in enumerate(zip(l1, l2_groups)):
        px = parent['x']
        for child in children:
            draw_box(child['x'], y_top[2], bw_l2, 2, child['label'])
            draw_connector(px,        y_top[1] - box_h,
                           child['x'], y_top[2])

    save_fig(fig, "fig_02_bom_tree")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 — fig_03_cost_rollup
# Horizontal bar chart: BOM cost by subsystem
# ─────────────────────────────────────────────────────────────────────────────
def make_fig3():
    fig, ax = plt.subplots(figsize=(7, 2.4))
    fig.patch.set_facecolor('white')

    subsystems = ["Enclosure & HW", "Actuation\nSubsystem", "Control\nSubsystem"]
    costs = [28, 86, 112]
    y_pos = np.arange(len(subsystems))

    bars = ax.barh(y_pos, costs, color='0.55', edgecolor='black',
                   linewidth=1.0, height=0.5)

    # Cost labels at bar end
    labels_str = ["$28", "$86", "$112"]
    for bar, lbl in zip(bars, labels_str):
        x_val = bar.get_width()
        ax.text(x_val + 1.5, bar.get_y() + bar.get_height() / 2,
                lbl, va='center', ha='left', fontsize=9, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(subsystems, fontsize=9)
    ax.set_xlabel("Extended Cost (CAD)", fontsize=9)
    ax.set_xlim(0, 140)
    ax.set_xticks([0, 25, 50, 75, 100, 125])
    ax.tick_params(axis='both', labelsize=9)

    # Light gray grid on x-axis only
    ax.xaxis.grid(True, color='0.82', linewidth=0.8, linestyle='--')
    ax.set_axisbelow(True)
    ax.yaxis.grid(False)

    # Spines: keep bottom and left only
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.0)
    ax.spines['left'].set_linewidth(1.0)

    # Total annotation — placed below x-axis label to avoid overlap
    ax.text(0.98, -0.28, r"$C_{\mathrm{BOM}}$ = \$226 CAD",
            transform=ax.transAxes,
            ha='right', va='top', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='0.88',
                      edgecolor='black', linewidth=0.8))

    fig.tight_layout(pad=0.5)
    save_fig(fig, "fig_03_cost_rollup")


if __name__ == "__main__":
    print("Generating figures for Chapter 11: BOM & Procurement...")
    make_fig1()
    make_fig2()
    make_fig3()
    print("Done.")

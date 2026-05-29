"""
gen_figures.py
Generates all three figures for Chapter 5 "System Architecture & Interface Definition"
of the textbook "Project Planning & Prototyping".

Figures:
  fig_01_block_diagram   — IoT robotic sorting subsystem block diagram (graphviz)
  fig_02_interface_budget — 5 ms timing budget bar chart (matplotlib)
  fig_03_boundary_failure — Interface mismatch two-block conceptual diagram (matplotlib)
"""

import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------------------------------------------------------------------
# Mandatory rcParams preamble
# ---------------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "axes.grid": False,
    "lines.linewidth": 1.6,
    "savefig.bbox": "tight",
})

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    plt.close(fig)
    print(f"  Saved {stem}.pdf and {stem}.png")


# ===========================================================================
# FIGURE 1 — fig_01_block_diagram
# System block diagram using graphviz (horizontal flow)
# ===========================================================================
def make_fig1():
    print("Generating Figure 1: Block Diagram...")
    try:
        import graphviz

        stem = os.path.join(OUT_DIR, "fig_01_block_diagram")

        dot = graphviz.Digraph(
            "block_diagram",
            graph_attr={
                "rankdir": "LR",
                "size": "8,2.5",
                "dpi": "200",
                "bgcolor": "white",
                "margin": "0.2",
                "nodesep": "0.35",
                "ranksep": "0.55",
            },
            node_attr={
                "shape": "box",
                "style": "filled",
                "fillcolor": "#cccccc",
                "fontsize": "11",
                "fontname": "Helvetica",
                "height": "0.55",
                "width": "1.4",
                "margin": "0.12,0.06",
            },
            edge_attr={
                "fontsize": "9",
                "fontname": "Helvetica",
                "labeldistance": "1.5",
                "labelangle": "0",
            },
        )

        # Rank 1 — sensors
        with dot.subgraph() as s:
            s.attr(rank="same")
            s.node("sensor", "Sensor Array")
            s.node("camera", "Camera /\nVision")

        # Rank 2 — AI
        with dot.subgraph() as s:
            s.attr(rank="same")
            s.node("ai", "AI Inference\nEngine")

        # Rank 3 — MCU
        with dot.subgraph() as s:
            s.attr(rank="same")
            s.node("mcu", "MCU Firmware")

        # Rank 4 — actuators
        with dot.subgraph() as s:
            s.attr(rank="same")
            s.node("sort", "Sort Actuator")
            s.node("conveyor", "Conveyor\nController")

        # Rank 5 — cloud
        with dot.subgraph() as s:
            s.attr(rank="same")
            s.node("mqtt", "MQTT Broker")
            s.node("cloud", "Cloud\nDashboard")

        # Edges with labels
        dot.edge("sensor", "ai", label="item features")
        dot.edge("camera", "ai", label="image frame")
        dot.edge("ai", "sort", label="sort cmd")
        dot.edge("ai", "mcu", label="classif. result")
        dot.edge("mcu", "conveyor", label="speed/stop")
        dot.edge("mcu", "mqtt", label="status msg")
        dot.edge("mqtt", "cloud", label="telemetry")

        # Render to PDF (graphviz handles this natively)
        dot.render(filename="fig_01_block_diagram", directory=OUT_DIR,
                   format="pdf", cleanup=True)
        dot.render(filename="fig_01_block_diagram", directory=OUT_DIR,
                   format="png", cleanup=True)

        # Rename: graphviz appends the format extension to the filename
        import shutil
        pdf_src = os.path.join(OUT_DIR, "fig_01_block_diagram.pdf")
        png_src = os.path.join(OUT_DIR, "fig_01_block_diagram.png")
        # graphviz render() produces: <filename>.<format>
        # The cleanup=True removes the intermediate .gv file
        if os.path.exists(pdf_src):
            print(f"  Saved {pdf_src}")
        if os.path.exists(png_src):
            print(f"  Saved {png_src}")

    except Exception as e:
        print(f"  graphviz failed ({e}), falling back to matplotlib")
        _make_fig1_matplotlib()


def _make_fig1_matplotlib():
    """Fallback: draw fig1 using matplotlib rectangles and arrows."""
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 2.8)
    ax.axis("off")

    gray = 0.8  # fill gray

    def draw_box(ax, cx, cy, w, h, label, fontsize=10):
        x0, y0 = cx - w / 2, cy - h / 2
        rect = FancyBboxPatch((x0, y0), w, h,
                              boxstyle="square,pad=0.05",
                              linewidth=1.2, edgecolor="black",
                              facecolor=str(gray))
        ax.add_patch(rect)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=fontsize, fontfamily="sans-serif", wrap=True)

    def draw_arrow(ax, x0, y0, x1, y1, label="", fontsize=8):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="black",
                                   lw=1.4))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + 0.12
        if label:
            ax.text(mx, my, label, ha="center", va="bottom",
                    fontsize=fontsize, fontfamily="sans-serif",
                    style="italic")

    bw, bh = 1.3, 0.55

    # Positions: x ranks
    xs = [0.85, 2.5, 4.1, 5.7, 7.3, 8.5]
    # Sensor Array, Camera/Vision
    draw_box(ax, xs[0], 2.0, bw, bh, "Sensor\nArray")
    draw_box(ax, xs[0], 0.9, bw, bh, "Camera /\nVision")
    # AI
    draw_box(ax, xs[2], 1.45, bw, bh, "AI Inference\nEngine")
    # MCU
    draw_box(ax, xs[3], 1.45, bw, bh, "MCU\nFirmware")
    # Sort, Conveyor
    draw_box(ax, xs[4], 2.15, bw, bh, "Sort\nActuator")
    draw_box(ax, xs[4], 0.75, bw, bh, "Conveyor\nCtrl")
    # MQTT, Cloud
    draw_box(ax, xs[5], 1.45, bw, bh, "MQTT\nBroker")
    # Cloud — shift right
    # Re-do x positions with wider spacing
    # Already drawn above; add Cloud
    # (This fallback is approximate)

    draw_arrow(ax, xs[0] + bw / 2, 2.0, xs[2] - bw / 2, 1.6,
               "item features")
    draw_arrow(ax, xs[0] + bw / 2, 0.9, xs[2] - bw / 2, 1.3,
               "image frame")
    draw_arrow(ax, xs[2] + bw / 2, 1.55, xs[3] - bw / 2, 1.55, "")
    draw_arrow(ax, xs[3] + bw / 2, 1.6, xs[4] - bw / 2, 2.15, "")
    draw_arrow(ax, xs[3] + bw / 2, 1.3, xs[4] - bw / 2, 0.75, "")
    draw_arrow(ax, xs[4] + bw / 2, 1.45, xs[5] - bw / 2, 1.45, "")

    fig.tight_layout()
    stem = os.path.join(OUT_DIR, "fig_01_block_diagram")
    save(fig, stem)


# ===========================================================================
# FIGURE 2 — fig_02_interface_budget
# 5 ms timing budget stacked bar + horizontal limit line
# ===========================================================================
def make_fig2():
    print("Generating Figure 2: Interface Timing Budget...")

    fig, ax = plt.subplots(figsize=(6, 2.8))

    labels = ["Sensor Read", "AI Classifier", "Actuator Cmd"]
    times = [1.0, 2.0, 2.0]
    x = range(len(labels))

    bar_width = 0.5
    gray_fill = 0.72  # gray level for bars

    bars = ax.bar(x, times, width=bar_width,
                  color=[str(gray_fill)] * 3,
                  edgecolor="black", linewidth=1.2)

    # Annotate each bar with its value
    for bar, t in zip(bars, times):
        bx = bar.get_x() + bar.get_width() / 2
        by = bar.get_height()
        ax.text(bx, by + 0.08, f"{int(t)} ms",
                ha="center", va="bottom", fontsize=10,
                fontfamily="sans-serif", fontweight="bold")

    # Horizontal dashed limit line at T_budget = 5 ms
    ax.axhline(y=5.0, color="black", linestyle="--", linewidth=1.6,
               label="$T_{budget}$ = 5 ms")

    # Label the limit line at the right edge
    ax.text(len(labels) - 0.5 + bar_width / 2 + 0.15, 5.0 + 0.12,
            "$T_{budget}$ = 5 ms",
            ha="left", va="bottom", fontsize=10,
            fontfamily="sans-serif")

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel("Latency (ms)", fontsize=10)
    ax.set_ylim(0, 6.2)
    ax.set_xlim(-0.5, len(labels) - 0.5 + bar_width)

    ax.tick_params(axis="both", labelsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    stem = os.path.join(OUT_DIR, "fig_02_interface_budget")
    save(fig, stem)


# ===========================================================================
# FIGURE 3 — fig_03_boundary_failure
# Interface mismatch conceptual two-block diagram
# ===========================================================================
def make_fig3():
    print("Generating Figure 3: Boundary Failure Diagram...")

    fig, ax = plt.subplots(figsize=(8, 2.6))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 2.6)
    ax.axis("off")

    light_gray = 0.85  # fill for blocks

    # -----------------------------------------------------------------------
    # Helper: draw a labelled block
    # -----------------------------------------------------------------------
    def draw_block(cx, cy, w, h, title, body, fontsize_title=11,
                   fontsize_body=10):
        x0, y0 = cx - w / 2, cy - h / 2
        rect = FancyBboxPatch((x0, y0), w, h,
                              boxstyle="square,pad=0.0",
                              linewidth=1.5, edgecolor="black",
                              facecolor=str(light_gray))
        ax.add_patch(rect)
        # Title (top, bold)
        ax.text(cx, cy + h * 0.22, title, ha="center", va="center",
                fontsize=fontsize_title, fontfamily="sans-serif",
                fontweight="bold")
        # Body (smaller, inside)
        ax.text(cx, cy - h * 0.18, body, ha="center", va="center",
                fontsize=fontsize_body, fontfamily="sans-serif",
                linespacing=1.4)

    # Block dimensions
    bw, bh = 2.0, 1.4
    left_cx, right_cx = 1.6, 6.4
    block_cy = 1.6

    draw_block(left_cx, block_cy, bw, bh,
               "MCU Firmware",
               "Output: 3.3 V UART\n115200 baud")

    draw_block(right_cx, block_cy, bw, bh,
               "Motor Driver",
               "Input: 5 V UART\n9600 baud")

    # -----------------------------------------------------------------------
    # Arrow from left block to right block (with gap in center for the X)
    # -----------------------------------------------------------------------
    arr_y = block_cy
    left_end = left_cx + bw / 2      # right edge of left block
    right_end = right_cx - bw / 2    # left edge of right block
    mid_x = (left_end + right_end) / 2

    gap = 0.38  # gap around the X symbol

    # Left segment of arrow
    ax.annotate("", xy=(mid_x - gap, arr_y),
                xytext=(left_end + 0.05, arr_y),
                arrowprops=dict(arrowstyle="-", color="black", lw=1.6))

    # Right segment with arrowhead
    ax.annotate("", xy=(right_end - 0.05, arr_y),
                xytext=(mid_x + gap, arr_y),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6,
                                mutation_scale=14))

    # "INTERFACE" label above the arrow
    ax.text(mid_x, arr_y + 0.28, "INTERFACE",
            ha="center", va="bottom", fontsize=10,
            fontfamily="sans-serif", style="italic")

    # -----------------------------------------------------------------------
    # Large X at the center (mismatch indicator)
    # -----------------------------------------------------------------------
    x_size = 0.26
    lw_x = 2.4
    ax.plot([mid_x - x_size, mid_x + x_size],
            [arr_y - x_size, arr_y + x_size],
            color="black", lw=lw_x, solid_capstyle="round")
    ax.plot([mid_x - x_size, mid_x + x_size],
            [arr_y + x_size, arr_y - x_size],
            color="black", lw=lw_x, solid_capstyle="round")

    # -----------------------------------------------------------------------
    # Mismatch annotation boxes below the X
    # -----------------------------------------------------------------------
    ann_y_top = arr_y - 0.52
    ann_y_bot = arr_y - 0.95

    def draw_ann_box(cx, cy, text, fontsize=9.5):
        """Draw a small annotation box with white fill."""
        t = ax.text(cx, cy, text, ha="center", va="center",
                    fontsize=fontsize, fontfamily="sans-serif",
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.25",
                              facecolor="white",
                              edgecolor="black",
                              linewidth=1.2))
        return t

    draw_ann_box(mid_x, ann_y_top, "Voltage: 3.3 V → 5 V")
    draw_ann_box(mid_x, ann_y_bot, "Baud rate: 115200 → 9600")

    fig.tight_layout()
    stem = os.path.join(OUT_DIR, "fig_03_boundary_failure")
    save(fig, stem)


# ===========================================================================
# Main
# ===========================================================================
if __name__ == "__main__":
    print(f"Output directory: {OUT_DIR}")
    make_fig1()
    make_fig2()
    make_fig3()
    print("\nAll figures generated successfully.")

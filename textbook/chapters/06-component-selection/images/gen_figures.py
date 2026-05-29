"""
gen_figures.py
Generates three figures for Chapter 6 "Component Selection & Datasheet Literacy"
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

mpl.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.edgecolor": "black", "axes.linewidth": 1.0,
    "axes.grid": False, "lines.linewidth": 1.6,
    "savefig.bbox": "tight",
})

OUTDIR = "/home/user/Project-Planning-and-Prototyping/textbook/chapters/06-component-selection/images"


def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────
# FIGURE 1 — Datasheet Anatomy
# ─────────────────────────────────────────────────────────────
def make_fig1():
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Outer page rectangle
    page_x, page_y = 0.02, 0.03
    page_w, page_h = 0.52, 0.94
    outer = mpatches.FancyBboxPatch(
        (page_x, page_y), page_w, page_h,
        boxstyle="square,pad=0",
        linewidth=1.5, edgecolor="black", facecolor="0.95",
        transform=ax.transAxes, zorder=1
    )
    ax.add_patch(outer)

    # Zone definitions top-to-bottom: (label, fill_gray, fraction of height)
    zones = [
        ("Absolute Maximum Ratings",        0.80, 0.20),
        ("Recommended Operating Conditions", 0.70, 0.25),
        ("Electrical Characteristics & Timing", 0.60, 0.35),
        ("Application Circuit / Packaging",  0.75, 0.20),
    ]

    annotations = [
        "⚠ NEVER operate here",
        "Design target operating range",
        "Check $D_f$ and margin here",
        "Footprint + second-source check",
    ]
    ann_styles = ["bold", "normal", "normal", "normal"]

    # Draw zones top-down: start from top of page (page_y + page_h) and work down
    heights = [page_h * f for _, _, f in zones]
    # y-coordinate of TOP of each zone in axes coords
    zone_tops = []
    cur_top = page_y + page_h
    for h in heights:
        zone_tops.append(cur_top)
        cur_top -= h

    for i, ((label, gray, frac), h, yt) in enumerate(zip(zones, heights, zone_tops)):
        yb = yt - h  # bottom of this zone
        rect = mpatches.FancyBboxPatch(
            (page_x, yb), page_w, h,
            boxstyle="square,pad=0",
            linewidth=0.8, edgecolor="black", facecolor=str(gray),
            transform=ax.transAxes, zorder=2
        )
        ax.add_patch(rect)
        # Zone label inside, centered vertically
        ax.text(
            page_x + page_w / 2, yb + h / 2, label,
            ha="center", va="center", fontsize=9,
            color="black" if gray > 0.4 else "white",
            fontweight="normal",
            transform=ax.transAxes, zorder=3
        )

    # Annotation arrows on the right side, aligned to each zone center
    text_x = page_x + page_w + 0.03

    for i, (ann_text, ann_style, yt, h) in enumerate(
        zip(annotations, ann_styles, zone_tops, heights)
    ):
        y_center = yt - h / 2
        ax.annotate(
            ann_text,
            xy=(page_x + page_w, y_center),
            xytext=(text_x, y_center),
            xycoords="axes fraction",
            textcoords="axes fraction",
            fontsize=9,
            fontweight=ann_style,
            va="center", ha="left",
            arrowprops=dict(
                arrowstyle="-|>",
                color="black",
                lw=1.2,
                connectionstyle="arc3,rad=0.0"
            ),
            zorder=5
        )

    save(fig, f"{OUTDIR}/fig_01_datasheet_anatomy")
    print("Fig 1 saved.")


# ─────────────────────────────────────────────────────────────
# FIGURE 2 — Derating Curve
# ─────────────────────────────────────────────────────────────
def make_fig2():
    fig, ax = plt.subplots(figsize=(7, 2.8))

    # Raw data points
    xd = np.array([0.0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0])
    yd = np.array([0.02, 0.05, 0.1, 0.2, 0.5, 1.5, 8.0, 25.0, 100.0])

    # Smooth interpolation in log space
    x_fine = np.linspace(0.0, 1.0, 500)
    log_yd = np.log10(yd)
    log_y_fine = np.interp(x_fine, xd, log_yd)
    y_fine = 10 ** log_y_fine

    ax.semilogy(x_fine, y_fine, color="black", linewidth=1.8, zorder=3)

    # Shade stress region D_f > 0.80
    mask = x_fine >= 0.80
    ax.fill_between(
        x_fine[mask], 0.005, y_fine[mask],
        facecolor="0.75", hatch="///", alpha=0.45,
        edgecolor="0.4", linewidth=0.5, zorder=2,
        label="Stress region"
    )

    # Vertical dashed line at D_f = 0.80
    ax.axvline(x=0.80, color="black", linestyle="--", linewidth=1.4, zorder=4)

    # Label the vertical line — position above the curve
    ax.text(
        0.795, 30, "Design target\n$D_f = 0.80$",
        ha="right", va="top", fontsize=9,
        fontstyle="normal",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.8)
    )

    # Axes labels
    ax.set_xlabel(r"Derating Factor $D_f = V_{\mathrm{applied}} / V_{\mathrm{rated}}$", fontsize=10)
    ax.set_ylabel("Normalized Failure Rate\n(log scale)", fontsize=10)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.01, 100)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # Legend for hatch region
    hatch_patch = mpatches.Patch(
        facecolor="0.75", hatch="///", edgecolor="0.4",
        linewidth=0.5, label="Stress region"
    )
    ax.legend(handles=[hatch_patch], loc="upper left", fontsize=9,
              framealpha=0.9, edgecolor="black")

    ax.tick_params(axis="both", which="major", labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    save(fig, f"{OUTDIR}/fig_02_derating_curve")
    print("Fig 2 saved.")


# ─────────────────────────────────────────────────────────────
# FIGURE 3 — Component Lifecycle Timeline
# ─────────────────────────────────────────────────────────────
def make_fig3():
    fig, ax = plt.subplots(figsize=(9, 2.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    phases = [
        ("Active", 0.85, "black"),
        ("NRND", 0.65, "black"),
        ("Last-Time Buy", 0.45, "black"),
        ("Obsolete", 0.25, "white"),
    ]

    risk_notes = [
        "Normal design use",
        "Stop new designs;\nfind alternate",
        "Final order\nwindow",
        "No supply;\nrespin required",
    ]

    n = len(phases)
    # Timeline spans from x=0.04 to x=0.96
    tl_left = 0.04
    tl_right = 0.96
    tl_width = tl_right - tl_left

    # Phase box geometry
    box_top = 0.72
    box_bottom = 0.30
    box_h = box_top - box_bottom

    # Arrow head width & gap between boxes
    arrow_w = 0.025
    gap = 0.005
    phase_w = (tl_width - (n - 1) * (arrow_w + gap * 2)) / n

    box_positions = []
    cur_x = tl_left
    for i, (label, gray, txt_color) in enumerate(phases):
        bx = cur_x
        box_positions.append(bx)

        # Draw filled rectangle
        rect = mpatches.FancyBboxPatch(
            (bx, box_bottom), phase_w, box_h,
            boxstyle="square,pad=0",
            linewidth=1.2, edgecolor="black", facecolor=str(gray),
            transform=ax.transAxes, zorder=2
        )
        ax.add_patch(rect)

        # Phase label inside box
        ax.text(
            bx + phase_w / 2, (box_top + box_bottom) / 2, label,
            ha="center", va="center", fontsize=10,
            fontweight="bold", color=txt_color,
            transform=ax.transAxes, zorder=3
        )

        # Risk annotation below
        ax.text(
            bx + phase_w / 2, box_bottom - 0.06,
            risk_notes[i],
            ha="center", va="top", fontsize=9,
            color="black",
            transform=ax.transAxes, zorder=3
        )

        # Draw arrow to next phase (not after last)
        if i < n - 1:
            arrow_x = bx + phase_w + gap
            arrow_cx = arrow_x + arrow_w / 2
            mid_y = (box_top + box_bottom) / 2
            ax.annotate(
                "",
                xy=(arrow_x + arrow_w, mid_y),
                xytext=(arrow_x, mid_y),
                xycoords="axes fraction",
                textcoords="axes fraction",
                arrowprops=dict(
                    arrowstyle="-|>",
                    color="black",
                    lw=1.4,
                    mutation_scale=14,
                )
            )
        cur_x = bx + phase_w + gap * 2 + arrow_w

    # Annotation above NRND→Last-Time Buy transition (between index 1 and 2)
    # Position: over the arrow between phase 1 and phase 2
    nrnd_right = box_positions[1] + phase_w
    ltb_left = box_positions[2]
    mid_arrow_x = (nrnd_right + ltb_left) / 2

    ann_y = box_top + 0.06
    ax.annotate(
        "~12–24 months\nnotice typical",
        xy=(mid_arrow_x, box_top),
        xytext=(mid_arrow_x, ann_y + 0.10),
        xycoords="axes fraction",
        textcoords="axes fraction",
        fontsize=9,
        ha="center", va="bottom",
        arrowprops=dict(
            arrowstyle="-|>",
            color="black",
            lw=1.1,
        ),
        zorder=5
    )

    save(fig, f"{OUTDIR}/fig_03_lifecycle")
    print("Fig 3 saved.")


if __name__ == "__main__":
    make_fig1()
    make_fig2()
    make_fig3()
    print("All figures generated successfully.")

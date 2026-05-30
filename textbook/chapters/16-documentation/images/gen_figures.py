"""
gen_figures.py — Chapter 16: Documentation & Portfolio Assembly
Generates all three figures for Chapter 16.
Run from the images/ directory:  python gen_figures.py
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.edgecolor": "black",
    "axes.linewidth": 1.0,
    "axes.grid": False,
    "savefig.bbox": "tight",
})


def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    print(f"Saved {stem}.pdf and {stem}.png")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: Stage-Gate phases with parallel documentation artifacts
# ─────────────────────────────────────────────────────────────────────────────

def fig_01_doc_parallel():
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.axis("off")

    # Stage-Gate phases
    phases = ["Concept", "Scoping", "Development", "Testing", "Launch"]
    # Artifacts aligned under phases (spanning as needed)
    # We'll place 4 artifact boxes spanning across the 5 phases
    artifact_data = [
        # (start_phase_idx, end_phase_idx, label)
        (0, 1, "Project Brief\n/ Kano"),
        (2, 2, "Spec + Architecture\n+ BOM"),
        (3, 3, "Test Procedure\n+ FTA"),
        (4, 4, "Portfolio +\nIP Checklist"),
    ]

    n = len(phases)
    box_w = 1.0 / n  # fraction of axis width per phase
    margin = 0.01
    phase_y_top = 0.72
    phase_y_bot = 0.48
    art_y_top = 0.32
    art_y_bot = 0.04
    phase_h = phase_y_top - phase_y_bot
    art_h = art_y_top - art_y_bot

    light_gray = "#D8D8D8"
    dark_gray = "#555555"
    art_gray = "#EBEBEB"

    for i, phase in enumerate(phases):
        x0 = i * box_w + margin
        x1 = (i + 1) * box_w - margin
        cx = (x0 + x1) / 2
        rect = mpatches.FancyBboxPatch(
            (x0, phase_y_bot), x1 - x0, phase_h,
            boxstyle="round,pad=0.01",
            linewidth=1.0, edgecolor="black", facecolor=light_gray,
            transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(rect)
        ax.text(
            cx, (phase_y_top + phase_y_bot) / 2, phase,
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            transform=ax.transAxes, color="black",
        )

    # Arrows between phases (→)
    for i in range(n - 1):
        x_arrow = (i + 1) * box_w
        ax.annotate(
            "", xy=(x_arrow + margin * 0.4, (phase_y_top + phase_y_bot) / 2),
            xytext=(x_arrow - margin * 0.4, (phase_y_top + phase_y_bot) / 2),
            xycoords="axes fraction", textcoords="axes fraction",
            arrowprops=dict(arrowstyle="->", color=dark_gray, lw=1.2),
        )

    # Header label
    ax.text(
        0.0, phase_y_top + 0.06, "Stage-Gate Phases:",
        ha="left", va="bottom", fontsize=9, fontstyle="italic",
        transform=ax.transAxes, color=dark_gray,
    )
    ax.text(
        0.0, art_y_top + 0.06, "Documentation Artifacts:",
        ha="left", va="bottom", fontsize=9, fontstyle="italic",
        transform=ax.transAxes, color=dark_gray,
    )

    # Artifact boxes
    for (s, e, label) in artifact_data:
        x0 = s * box_w + margin * 1.5
        x1 = (e + 1) * box_w - margin * 1.5
        cx = (x0 + x1) / 2
        art_cx = cx  # horizontal center of the artifact box
        art_phase_cx = (s * box_w + (e + 1) * box_w) / 2  # center of phases spanned

        rect = mpatches.FancyBboxPatch(
            (x0, art_y_bot), x1 - x0, art_h,
            boxstyle="round,pad=0.01",
            linewidth=1.0, edgecolor="black", facecolor=art_gray,
            transform=ax.transAxes, clip_on=False,
        )
        ax.add_patch(rect)
        ax.text(
            cx, (art_y_top + art_y_bot) / 2, label,
            ha="center", va="center", fontsize=9, transform=ax.transAxes,
            color="black", linespacing=1.3,
        )
        # Vertical connector line
        ax.annotate(
            "", xy=(art_phase_cx, art_y_top),
            xytext=(art_phase_cx, phase_y_bot),
            xycoords="axes fraction", textcoords="axes fraction",
            arrowprops=dict(arrowstyle="-", color=dark_gray, lw=1.0,
                            linestyle="dashed"),
        )

    save(fig, "fig_01_doc_parallel")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: Traceability matrix
# ─────────────────────────────────────────────────────────────────────────────

def fig_02_traceability():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.axis("off")

    rows = [
        "R1: Sort latency ≤104 ms",
        "R2: MQTT delivery ≤200 ms",
        "R3: Battery life ≥30 days",
        "R4: SF ≥ 2 (sort-gate bracket)",
    ]
    cols = ["T1", "T2", "T3", "T4"]

    # Links: (row_idx, col_idx) — filled circle
    links = {(0, 0), (1, 1), (2, 2), (3, 3)}
    # Gap: R2 should also link to T1 but doesn't — leave (1,0) empty

    n_rows = len(rows)
    n_cols = len(cols)

    # Table layout in axes coords
    left = 0.38   # left edge of data columns
    right = 0.98
    top = 0.92
    bottom = 0.04
    row_h = (top - bottom) / (n_rows + 1)  # +1 for header
    col_w = (right - left) / n_cols
    label_right = left - 0.01

    light_gray = "#EBEBEB"
    dark_gray = "#555555"
    header_gray = "#555555"

    # Header row
    header_y = top - row_h
    ax.add_patch(mpatches.Rectangle(
        (left, header_y), right - left, row_h,
        linewidth=0, facecolor=header_gray, transform=ax.transAxes,
    ))
    for j, col in enumerate(cols):
        cx = left + (j + 0.5) * col_w
        ax.text(cx, header_y + row_h / 2, col,
                ha="center", va="center", fontsize=9.5, fontweight="bold",
                color="white", transform=ax.transAxes)

    # Column header label
    ax.text(label_right, header_y + row_h / 2, "Requirement \\ Test Case",
            ha="right", va="center", fontsize=8.5, fontstyle="italic",
            color=dark_gray, transform=ax.transAxes)

    # Data rows
    for i, row_label in enumerate(rows):
        row_y = top - (i + 2) * row_h
        shade = light_gray if i % 2 == 0 else "white"

        # Row background (full width incl. label area)
        ax.add_patch(mpatches.Rectangle(
            (0.0, row_y), 1.0, row_h,
            linewidth=0, facecolor=shade, transform=ax.transAxes,
        ))

        # Row label
        ax.text(label_right, row_y + row_h / 2, row_label,
                ha="right", va="center", fontsize=9, transform=ax.transAxes,
                color="black")

        # Cells
        for j in range(n_cols):
            cx = left + (j + 0.5) * col_w
            cy = row_y + row_h / 2
            # Cell border
            ax.add_patch(mpatches.Rectangle(
                (left + j * col_w, row_y), col_w, row_h,
                linewidth=0.8, edgecolor="#999999", facecolor="none",
                transform=ax.transAxes,
            ))
            if (i, j) in links:
                # Filled circle marker
                ax.plot(cx, cy, "o", markersize=10,
                        color="black", transform=ax.transAxes,
                        markeredgecolor="black", markerfacecolor="#222222",
                        zorder=5)
            else:
                # Show gap annotation for (1, 0) — R2 should link to T1
                if i == 1 and j == 0:
                    ax.text(cx, cy, "gap", ha="center", va="center",
                            fontsize=7.5, color="#888888",
                            fontstyle="italic", transform=ax.transAxes)

    # Outer border
    ax.add_patch(mpatches.Rectangle(
        (left, bottom), right - left, top - bottom,
        linewidth=1.0, edgecolor="black", facecolor="none",
        transform=ax.transAxes,
    ))

    # Coverage annotation
    ax.text(0.5, 0.01,
            "Coverage: 4 / 5 linked pairs = 80%  |  Gap: R2 → T1 missing",
            ha="center", va="bottom", fontsize=8.5, color=dark_gray,
            transform=ax.transAxes, fontstyle="italic")

    save(fig, "fig_02_traceability")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3: Portfolio map (14-row table)
# ─────────────────────────────────────────────────────────────────────────────

def fig_03_portfolio_map():
    fig, ax = plt.subplots(figsize=(9, 3.0))
    ax.axis("off")

    sections = [
        ("1  Project Context Brief",     "Ch. 1"),
        ("2  Kano Analysis",             "Ch. 2"),
        ("3  Specifications & Risk",     "Ch. 4"),
        ("4  Architecture",              "Ch. 5"),
        ("5  Component Selection",       "Ch. 6"),
        ("6  DFX Review",                "Ch. 7"),
        ("7  AI Use Log",                "Ch. 8"),
        ("8  IoT / Safety Records",      "Ch. 9"),
        ("9  Schedule & Risk Register",  "Ch. 10"),
        ("10 BOM",                       "Ch. 11"),
        ("11 Cost Analysis",             "Ch. 12"),
        ("12 Git / DHF",                 "Ch. 13"),
        ("13 Test Results",              "Ch. 14"),
        ("14 IP Checklist",              "Ch. 15"),
    ]

    n = len(sections)
    left = 0.03
    split = 0.74   # dividing line between section name and chapter
    right = 0.97
    top = 0.97
    bottom = 0.05
    total_h = top - bottom
    header_h = total_h / (n + 1) * 1.15
    row_h = (total_h - header_h) / n

    light_gray = "#EBEBEB"
    header_bg = "#444444"
    dark_gray = "#555555"

    # Header
    ax.add_patch(mpatches.Rectangle(
        (left, top - header_h), right - left, header_h,
        linewidth=0, facecolor=header_bg, transform=ax.transAxes,
    ))
    ax.text((left + split) / 2, top - header_h / 2,
            "Portfolio Section", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="white",
            transform=ax.transAxes)
    ax.text((split + right) / 2, top - header_h / 2,
            "Source Chapter", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="white",
            transform=ax.transAxes)
    # Divider in header
    ax.plot([split, split], [top - header_h, top], color="white",
            lw=0.8, transform=ax.transAxes)

    # Data rows
    for i, (section, chapter) in enumerate(sections):
        row_y = top - header_h - (i + 1) * row_h
        shade = light_gray if i % 2 == 0 else "white"

        ax.add_patch(mpatches.Rectangle(
            (left, row_y), right - left, row_h,
            linewidth=0, facecolor=shade, transform=ax.transAxes,
        ))

        # Section name
        ax.text(left + 0.01, row_y + row_h / 2, section,
                ha="left", va="center", fontsize=9, transform=ax.transAxes,
                color="black")

        # Chapter reference
        ax.text((split + right) / 2, row_y + row_h / 2, chapter,
                ha="center", va="center", fontsize=9, transform=ax.transAxes,
                color=dark_gray, fontweight="bold")

        # Horizontal divider
        ax.plot([left, right], [row_y, row_y], color="#BBBBBB",
                lw=0.5, transform=ax.transAxes)

        # Vertical divider
        ax.plot([split, split], [row_y, row_y + row_h], color="#BBBBBB",
                lw=0.8, transform=ax.transAxes)

    # Outer border
    ax.add_patch(mpatches.Rectangle(
        (left, bottom), right - left, top - bottom,
        linewidth=1.0, edgecolor="black", facecolor="none",
        transform=ax.transAxes,
    ))

    save(fig, "fig_03_portfolio_map")
    plt.close(fig)


if __name__ == "__main__":
    fig_01_doc_parallel()
    fig_02_traceability()
    fig_03_portfolio_map()
    print("All figures generated.")

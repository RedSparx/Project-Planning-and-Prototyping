"""
gen_figures.py — Generate figures for Chapter 15: Intellectual Property Basics
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

mpl.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.edgecolor": "black", "axes.linewidth": 1.0,
    "axes.grid": False, "savefig.bbox": "tight",
})

GRAYS = ["0.0", "0.35", "0.55", "0.75", "0.90"]

DPI = 200


def save(fig, stem):
    fig.savefig(f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(f"{stem}.png", dpi=DPI, bbox_inches="tight")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1: IP Types Comparison Table
# ─────────────────────────────────────────────────────────────────────────────
def make_fig1():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.axis("off")

    # Table data
    col_headers = ["Protection\nMechanism", "Duration", "Registration\nRequired",
                   "Disclosure\nTrade-off"]
    row_headers = ["Patent", "Trade Secret", "Copyright", "Trademark"]

    cell_data = [
        # Patent
        ["Government-granted\nexclusive right to\nexclude others",
         "20 years from\nfiling date",
         "Yes — patent\napplication required",
         "Full public\ndisclosure of\ninvention"],
        # Trade Secret
        ["Confidentiality\n(NDAs, access\ncontrols)",
         "Indefinite while\nsecrecy maintained",
         "No — protection\nis automatic",
         "No disclosure;\nlost if secret\nis revealed"],
        # Copyright
        ["Exclusive right to\ncopy, distribute,\nderive",
         "Life + 70 years\n(author); 95 years\n(work for hire)",
         "No — automatic\non creation",
         "Work must be\nexpressed and\nobservable"],
        # Trademark
        ["Brand identifier\n(name, logo,\nslogan)",
         "Indefinite with\ncontinued use\n& renewal",
         "Optional but\nstrongly\nrecommended",
         "Public use\nrequired to\nmaintain rights"],
    ]

    n_rows = len(row_headers)
    n_cols = len(col_headers)

    # Layout parameters
    left = 0.01
    top = 0.97
    col_widths = [0.13, 0.24, 0.21, 0.21, 0.21]  # row header + 4 data cols
    row_height = 0.195
    header_height = 0.13

    # Header row background
    header_y = top - header_height
    ax.add_patch(mpatches.FancyBboxPatch(
        (left, header_y), 1.0 - left, header_height,
        boxstyle="square,pad=0", transform=ax.transAxes,
        facecolor="0.75", edgecolor="0.4", lw=0.8, clip_on=False, zorder=2
    ))

    # Draw header text (row-header column is blank)
    x_cursor = left + col_widths[0]
    for i, ch in enumerate(col_headers):
        cx = x_cursor + col_widths[i + 1] / 2
        cy = header_y + header_height / 2
        ax.text(cx, cy, ch, transform=ax.transAxes,
                ha="center", va="center", fontsize=9,
                color="white", fontweight="bold")
        x_cursor += col_widths[i + 1]

    # Data rows
    for r, (rh, row) in enumerate(zip(row_headers, cell_data)):
        row_y = top - header_height - (r + 1) * row_height
        shade = "0.92" if r % 2 == 0 else "1.0"

        # Row background
        ax.add_patch(mpatches.FancyBboxPatch(
            (left, row_y), 1.0 - left, row_height,
            boxstyle="square,pad=0", transform=ax.transAxes,
            facecolor=shade, edgecolor="0.65", lw=0.6, clip_on=False, zorder=1
        ))

        # Row header cell (darker)
        ax.add_patch(mpatches.FancyBboxPatch(
            (left, row_y), col_widths[0], row_height,
            boxstyle="square,pad=0", transform=ax.transAxes,
            facecolor="0.82", edgecolor="0.55", lw=0.6, clip_on=False, zorder=2
        ))
        ax.text(left + col_widths[0] / 2, row_y + row_height / 2, rh,
                transform=ax.transAxes,
                ha="center", va="center", fontsize=9,
                fontweight="bold", color="0.05")

        # Data cells
        x_cursor = left + col_widths[0]
        for c, val in enumerate(row):
            cx = x_cursor + col_widths[c + 1] / 2
            cy = row_y + row_height / 2
            ax.text(cx, cy, val, transform=ax.transAxes,
                    ha="center", va="center", fontsize=9, color="0.05",
                    linespacing=1.25)
            x_cursor += col_widths[c + 1]

    # Outer border
    ax.add_patch(mpatches.FancyBboxPatch(
        (left, top - header_height - n_rows * row_height),
        1.0 - left, header_height + n_rows * row_height,
        boxstyle="square,pad=0", transform=ax.transAxes,
        facecolor="none", edgecolor="0.3", lw=1.2, clip_on=False, zorder=5
    ))

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    stem = "/home/user/Project-Planning-and-Prototyping/textbook/chapters/15-ip/images/fig_01_ip_types"
    save(fig, stem)
    plt.close(fig)
    print("Figure 1 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2: IP Consideration Timeline
# ─────────────────────────────────────────────────────────────────────────────
def make_fig2():
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(-2.8, 1.4)
    ax.axis("off")

    # ── Stage-gate phases across the top ──
    phases = [
        (1.0,  "Stage 1\nConcept"),
        (3.0,  "Gate 2"),
        (5.0,  "Stage 3\nDevelopment"),
        (7.0,  "Gate 3"),
        (9.0,  "Launch"),
    ]
    phase_types = ["stage", "gate", "stage", "gate", "stage"]

    y_timeline = 0.8

    # Draw the main timeline arrow
    ax.annotate("", xy=(9.8, y_timeline), xytext=(0.2, y_timeline),
                arrowprops=dict(arrowstyle="-|>", color="0.1", lw=1.5))

    # Phase markers
    for (x, label), ptype in zip(phases, phase_types):
        if ptype == "gate":
            # Diamond gate marker
            hw, hh = 0.18, 0.22
            pts = np.array([[x, y_timeline + hh],
                            [x + hw, y_timeline],
                            [x, y_timeline - hh],
                            [x - hw, y_timeline]])
            from matplotlib.patches import Polygon
            poly = Polygon(pts, closed=True, facecolor="0.25",
                           edgecolor="0.05", lw=1.2, zorder=4)
            ax.add_patch(poly)
        else:
            ax.plot(x, y_timeline, "o", ms=9, color="0.45",
                    mec="0.1", mew=1.2, zorder=4)

        # Label above
        va = "bottom"
        ax.text(x, y_timeline + 0.30, label, ha="center", va=va,
                fontsize=9, color="0.05", linespacing=1.2)

    # ── IP annotations below timeline ──
    # Each entry: (x_start, x_end, y_level, label, note)
    # y_level goes negative (below timeline)
    # Use bracket spans or single-point arrows

    annotations = [
        # (x_centre, y_row, label_text, span from x0 to x1 or None)
        dict(xc=1.0,  x0=None, x1=None, y=-0.35,
             label="Patent search\nbefore design commit", arrow=True),
        dict(xc=2.0,  x0=1.3,  x1=2.7,  y=-1.0,
             label="File provisional patent\nbefore Gate 2 or disclosure"),
        dict(xc=4.0,  x0=3.2,  x1=4.8,  y=-1.65,
             label="NDA before sharing\nwith suppliers"),
        dict(xc=5.0,  x0=0.3,  x1=9.5,  y=-2.20,
             label="Copyright: automatic on creation — covers all source files, schematics, docs"),
        dict(xc=5.0,  x0=1.5,  x1=8.5,  y=-2.75,
             label="Trade secret: access controls and NDAs in force throughout development"),
    ]

    for ann in annotations:
        y = ann["y"]
        # Vertical line from timeline to bracket level
        if ann.get("arrow"):
            xc = ann["xc"]
            ax.annotate("", xy=(xc, y_timeline - 0.12), xytext=(xc, y + 0.22),
                        arrowprops=dict(arrowstyle="->", color="0.3", lw=1.2))
        elif ann["x0"] is not None:
            x0, x1, xc = ann["x0"], ann["x1"], ann["xc"]
            # Bracket: vertical bars at ends + horizontal bar
            ax.plot([x0, x0], [y_timeline - 0.12, y + 0.14], color="0.45", lw=1.0)
            ax.plot([x1, x1], [y_timeline - 0.12, y + 0.14], color="0.45", lw=1.0)
            ax.plot([x0, x1], [y + 0.14, y + 0.14], color="0.45", lw=1.0)

        # Label text
        ax.text(ann["xc"], y, ann["label"], ha="center", va="center",
                fontsize=8.5, color="0.05", linespacing=1.2,
                bbox=dict(boxstyle="round,pad=0.18", facecolor="0.93",
                          edgecolor="0.55", lw=0.8))

    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    stem = "/home/user/Project-Planning-and-Prototyping/textbook/chapters/15-ip/images/fig_02_ip_timeline"
    save(fig, stem)
    plt.close(fig)
    print("Figure 2 saved.")


if __name__ == "__main__":
    make_fig1()
    make_fig2()
    print("All figures generated.")

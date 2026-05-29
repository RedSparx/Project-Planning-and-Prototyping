#!/usr/bin/env python3
"""Generate all four figures for Chapter 1 — Overview."""

import os
import subprocess
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

IMGDIR = os.path.dirname(os.path.abspath(__file__))

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
GRAYS = [0.0, 0.30, 0.55, 0.78]
HATCH = ["", "///", "\\\\\\", "xxx", "...", "+++"]


def save(fig, stem):
    pdf_path = os.path.join(IMGDIR, f"{stem}.pdf")
    png_path = os.path.join(IMGDIR, f"{stem}.png")
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {stem}.pdf  +  {stem}.png")


# ═══════════════════════════════════════════════════════════════════════════════
# FIG 01 — Concept → Project I → Project II → Market  (horizontal pipeline)
# ═══════════════════════════════════════════════════════════════════════════════
def make_fig01_pipeline():
    fig, ax = plt.subplots(figsize=(8.5, 2.8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    BW, BH = 2.0, 1.05   # box width / height
    boxes = [
        (1.3,  2.0, "Concept\n& Idea",             0.10),
        (4.5,  2.0, "Project I\n(Prototype)",       0.35),
        (8.2,  2.0, "Project II\n(Product Dev.)",   0.62),
        (11.8, 2.0, "Market",                        0.82),
    ]

    for cx, cy, lbl, fc in boxes:
        rect = mpatches.FancyBboxPatch(
            (cx - BW / 2, cy - BH / 2), BW, BH,
            boxstyle="round,pad=0.12",
            facecolor=str(fc), edgecolor="black", linewidth=1.4, zorder=3,
        )
        ax.add_patch(rect)
        txt_col = "white" if fc < 0.52 else "black"
        ax.text(cx, cy, lbl, ha="center", va="center", fontsize=9.5,
                fontweight="bold", color=txt_col, zorder=4,
                multialignment="center")

    # Arrows (from right edge to left edge of next box)
    arrow_kw = dict(
        arrowstyle="->", color="black", lw=1.7, mutation_scale=14
    )
    segs = [
        (boxes[0][0] + BW / 2, boxes[1][0] - BW / 2),
        (boxes[1][0] + BW / 2, boxes[2][0] - BW / 2),
        (boxes[2][0] + BW / 2, boxes[3][0] - BW / 2),
    ]
    for x1, x2 in segs:
        ax.annotate(
            "", xy=(x2, 2.0), xytext=(x1, 2.0),
            arrowprops=arrow_kw, zorder=2,
        )

    # Annotation blocks above each arrow
    annot = [
        ((segs[0][0] + segs[0][1]) / 2, "Idea +\nrequirements\nbrief"),
        ((segs[1][0] + segs[1][1]) / 2, "Proven prototype\ndocumentation\nrisk register"),
        ((segs[2][0] + segs[2][1]) / 2, "Certified product\nsupply chain\nproduction docs"),
    ]
    for ax_x, lbl in annot:
        ax.text(ax_x, 3.55, lbl, ha="center", va="center", fontsize=7.5,
                fontstyle="italic", color="0.15", multialignment="center",
                bbox=dict(
                    boxstyle="round,pad=0.25", facecolor="0.91",
                    edgecolor="0.55", linewidth=0.7,
                ))
        ax.annotate(
            "", xy=(ax_x, 2.55), xytext=(ax_x, 3.05),
            arrowprops=dict(arrowstyle="-", color="0.5", lw=0.8,
                            linestyle="dashed"),
        )

    fig.tight_layout()
    save(fig, "fig_01_pipeline")


# ═══════════════════════════════════════════════════════════════════════════════
# FIG 02 — Two-track course map (Theory + Lab/Practice) over 12 weeks
# ═══════════════════════════════════════════════════════════════════════════════
def make_fig02_course_map():
    fig, ax = plt.subplots(figsize=(11, 3.0))

    # Y layout: theory top, lab bottom, milestones above theory
    THEORY_Y = 2.55   # center of theory swim lane
    LAB_Y    = 1.15   # center of lab swim lane
    ROW_H    = 0.72   # height of each swim lane cell
    BAND_BOT = LAB_Y - ROW_H / 2 - 0.06
    BAND_TOP = THEORY_Y + ROW_H / 2 + 0.06
    BAND_H   = BAND_TOP - BAND_BOT

    # X layout: week 1 centered at x=1, week 12 at x=12
    ax.set_xlim(0.3, 12.7)
    ax.set_ylim(0.0, 4.0)
    ax.axis("off")

    # ── Stage-Gate phase background bands ──────────────────────────────────
    # Stage 2 Scoping: weeks 1–3  (x: 0.5 to 3.5)
    # Stage 3 Development: weeks 4–10 (x: 3.5 to 10.5)
    # Stage 4 Testing: weeks 11–12 (x: 10.5 to 12.5)
    phase_bands = [
        (0.5,  3.5,  "Stage 2\nScoping",     0.92),
        (3.5,  10.5, "Stage 3\nDevelopment", 0.82),
        (10.5, 12.5, "Stage 4\nTesting",     0.72),
    ]
    for x0, x1, lbl, fc in phase_bands:
        rect = mpatches.Rectangle(
            (x0, BAND_BOT), x1 - x0, BAND_H,
            facecolor=str(fc), edgecolor="none", zorder=0,
        )
        ax.add_patch(rect)
        # Phase label centered in band, above the theory row
        mid_x = (x0 + x1) / 2
        ax.text(mid_x, THEORY_Y + ROW_H / 2 + 0.22, lbl,
                ha="center", va="bottom", fontsize=7, color="0.30",
                fontstyle="italic", multialignment="center", zorder=1)

    # Gate transition dashed vertical lines
    for gate_x in [3.5, 10.5]:
        ax.plot([gate_x, gate_x], [BAND_BOT, BAND_TOP],
                color="0.45", lw=1.1, linestyle="--", zorder=2)

    # ── Track lane outlines (light border around each full row) ─────────────
    for cy in [THEORY_Y, LAB_Y]:
        band = mpatches.Rectangle(
            (0.5, cy - ROW_H / 2), 12.0, ROW_H,
            facecolor="none", edgecolor="0.55", linewidth=1.0, zorder=1,
        )
        ax.add_patch(band)

    # Track side labels
    ax.text(0.45, THEORY_Y, "Theory", ha="right", va="center",
            fontsize=8, fontweight="bold", color="0.20")
    ax.text(0.45, LAB_Y, "Lab /\nPractice", ha="right", va="center",
            fontsize=7.5, fontweight="bold", color="0.20",
            multialignment="right")

    # ── Per-week data ────────────────────────────────────────────────────────
    # theory_rows: (week, theory_text, lab_text)
    week_data = [
        (1,  "Ch.1-2\nOvrvw/S-G",   "Proj brief\nKano survey"),
        (2,  "Ch.3-4\nWkflw/Specs",  "Risk matrix\nwrkshp"),
        (3,  "Ch.4\nSpecs cont.",    "Proposal\nwriting"),
        (4,  "Ch.5\nArchitecture",   "Arch.\nworkshop"),
        (5,  "Ch.6\nComponents",     "Comp sel.\nBOM start"),
        (6,  "Ch.7\nDFX",            "DFX review"),
        (7,  "Ch.8-9\nAI/IoT/Safe",  "Subsystem\ndesign"),
        (8,  "Ch.10-11\nPlan/BOM",   "Procure.\nGantt"),
        (9,  "Ch.12\nEconomics",     "Cost\nanalysis"),
        (10, "Ch.13\nVer. Control",  "Build;\ngit setup"),
        (11, "Ch.14\nValidation",    "Test proc.\nFTA"),
        (12, "Ch.15-17\nIP/Docs/Cst","Portfolio\nassembly"),
    ]

    CW = 0.88   # cell width
    CH = ROW_H - 0.10  # cell height (slightly inset from row)

    for wk, t_lbl, l_lbl in week_data:
        # Theory cell — gray 0.88 for stage 2 weeks, 0.80 for stage 3, 0.70 for stage 4
        if wk <= 3:
            t_fc = "0.86"
        elif wk <= 10:
            t_fc = "0.76"
        else:
            t_fc = "0.66"

        # Theory cell
        rect = mpatches.FancyBboxPatch(
            (wk - CW / 2, THEORY_Y - CH / 2),
            CW - 0.06, CH,
            boxstyle="round,pad=0.04",
            facecolor=t_fc, edgecolor="0.35", linewidth=1.0, zorder=3,
        )
        ax.add_patch(rect)
        ax.text(wk - 0.03, THEORY_Y, t_lbl, ha="center", va="center",
                fontsize=7, multialignment="center", zorder=4,
                linespacing=1.15)

        # Lab cell — slightly lighter
        if wk <= 3:
            l_fc = "0.90"
        elif wk <= 10:
            l_fc = "0.84"
        else:
            l_fc = "0.78"

        rect = mpatches.FancyBboxPatch(
            (wk - CW / 2, LAB_Y - CH / 2),
            CW - 0.06, CH,
            boxstyle="round,pad=0.04",
            facecolor=l_fc, edgecolor="0.45", linewidth=1.0, zorder=3,
        )
        ax.add_patch(rect)
        ax.text(wk - 0.03, LAB_Y, l_lbl, ha="center", va="center",
                fontsize=7, multialignment="center", zorder=4,
                linespacing=1.15)

    # ── Milestone markers ───────────────────────────────────────────────────
    milestones = [
        (4,  "M1"),
        (10, "M2"),
        (12, "M3"),
    ]
    for wk, lbl in milestones:
        # Vertical line drawn at zorder=2, behind cells (zorder=3),
        # so cell boxes and text paint over it — no text/line overlap
        ax.plot([wk, wk],
                [LAB_Y - ROW_H / 2 - 0.04, THEORY_Y + ROW_H / 2 + 0.04],
                color="black", lw=1.8, linestyle="-", zorder=2)
        # Diamond above the theory row (above cells)
        ax.plot(wk, THEORY_Y + ROW_H / 2 + 0.28, marker="D",
                ms=7, color="black", zorder=6, markeredgewidth=1.2)
        # Label above diamond
        ax.text(wk, THEORY_Y + ROW_H / 2 + 0.52, lbl,
                ha="center", va="bottom", fontsize=8, fontweight="bold",
                zorder=6)

    # ── Week-number x-axis ──────────────────────────────────────────────────
    for wk in range(1, 13):
        ax.text(wk, LAB_Y - ROW_H / 2 - 0.18, f"Wk {wk}",
                ha="center", va="top", fontsize=7, color="0.25")

    fig.tight_layout(pad=0.4)
    save(fig, "fig_02_course_map")


# ═══════════════════════════════════════════════════════════════════════════════
# FIG 03 — Firm-size spectrum vs process formality & documentation weight
# ═══════════════════════════════════════════════════════════════════════════════
def make_fig03_firm_spectrum():
    fig, ax = plt.subplots(figsize=(7, 2.8))

    firms = ["Small /\nStart-up", "Medium\n(SME)", "Large\nEnterprise"]
    metrics = [
        ("Process Formality",      [1.5, 4.5, 8.5], "///", 0.75),
        ("Documentation Weight",   [1.0, 3.5, 8.0], "\\\\\\", 0.50),
        ("Approval Layers",        [0.5, 2.5, 7.0], "xxx",  0.30),
    ]

    x = np.arange(len(firms))
    n = len(metrics)
    bar_w = 0.22
    offsets = np.linspace(-(n - 1) * bar_w / 2, (n - 1) * bar_w / 2, n)

    for i, (label, values, hatch, fc) in enumerate(metrics):
        bars = ax.bar(
            x + offsets[i], values, width=bar_w,
            facecolor=str(fc), edgecolor="black", linewidth=0.9,
            hatch=hatch, label=label,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(firms, fontsize=10)
    ax.set_ylabel("Relative level (illustrative scale)", fontsize=9)
    ax.set_ylim(0, 11)
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.set_yticklabels(["Low", "2", "4", "6", "8", "High"], fontsize=8)
    ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
    ax.set_title(
        "Firm size vs. engineering process overhead",
        fontsize=9.5, pad=6,
    )

    # Gradient-hinted arrow along x-axis
    ax.annotate(
        "Increasing firm size →",
        xy=(2.45, -1.4), fontsize=8, fontstyle="italic", color="0.3",
        ha="right", va="top",
    )

    ax.grid(axis="y", alpha=0.3, linewidth=0.5)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "fig_03_firm_spectrum")


# ═══════════════════════════════════════════════════════════════════════════════
# FIG 04 — Business-model tree (graphviz)
# ═══════════════════════════════════════════════════════════════════════════════
def make_fig04_business_models():
    import graphviz

    dot = graphviz.Digraph(
        "business_models",
        format="pdf",
        graph_attr=dict(
            rankdir="LR",
            splines="ortho",
            nodesep="0.12",
            ranksep="0.40",
            bgcolor="white",
            fontname="Helvetica",
            fontsize="11",
        ),
        node_attr=dict(
            shape="box",
            style="filled,rounded",
            fontname="Helvetica",
            fontsize="10",
            margin="0.08,0.04",
            penwidth="1.2",
            width="1.2",
            height="0.30",
        ),
        edge_attr=dict(
            arrowsize="0.7",
            penwidth="1.0",
            color="black",
        ),
    )

    # Root
    dot.node("root",
             "Validated\nPrototype",
             fillcolor="#000000",
             fontcolor="white",
             fontsize="11",
             fontname="Helvetica-Bold")

    # Level 1 branches
    branch_style = dict(fillcolor="#555555", fontcolor="white",
                        fontname="Helvetica-Bold", fontsize="9.5")
    leaf_style   = dict(fillcolor="#BBBBBB", fontcolor="black", fontsize="9")
    mid_style    = dict(fillcolor="#888888", fontcolor="white",
                        fontname="Helvetica-Bold", fontsize="9")

    # Branch A: Direct Product Sale → B2C / B2B
    dot.node("sale",  "Product Sale\n(Direct)",         **branch_style)
    dot.node("b2c",   "Business-to-Consumer\n(B2C)",    **leaf_style)
    dot.node("b2b",   "Business-to-Business\n(B2B)",    **leaf_style)

    # Branch B: HaaS
    dot.node("haas",  "Hardware-as-a-Service\n(IoT / Subscription)", **branch_style)

    # Branch C: Licensing
    dot.node("lic",   "Technology\nLicensing",          **branch_style)

    # Branch D: Build-to-Order
    dot.node("bto",   "Build-to-Order\n(Contract Mfg.)", **branch_style)

    # Branch E: Volume strategy → Low-vol / High-vol
    dot.node("vol",   "Volume Strategy",                **mid_style)
    dot.node("lowv",  "Specialty Low-Volume\n(high margin, niche)", **leaf_style)
    dot.node("highv", "Commodity High-Volume\n(low margin, mass)",  **leaf_style)

    # Edges
    for child in ["sale", "haas", "lic", "bto", "vol"]:
        dot.edge("root", child)
    dot.edge("sale", "b2c")
    dot.edge("sale", "b2b")
    dot.edge("vol",  "lowv")
    dot.edge("vol",  "highv")

    # Render PDF
    pdf_out = os.path.join(IMGDIR, "fig_04_business_models")
    dot.render(pdf_out, cleanup=True)   # produces fig_04_business_models.pdf

    # Also render PNG at 200 dpi via dot -Tpng
    dot_src = pdf_out + ".gv" if os.path.exists(pdf_out + ".gv") else None
    # graphviz render with cleanup=True removes the .gv; use format='png' pass
    dot_png = graphviz.Digraph(
        "business_models",
        format="png",
        graph_attr=dot.graph_attr,
        node_attr=dot.node_attr,
        edge_attr=dot.edge_attr,
    )
    dot_png.body = dot.body   # copy all node/edge definitions
    dot_png.graph_attr["dpi"] = "200"
    png_out = os.path.join(IMGDIR, "fig_04_business_models")
    dot_png.render(png_out, cleanup=True)
    # rename: graphviz appends extension
    raw_png = png_out + ".png"
    if os.path.exists(raw_png):
        print(f"  saved fig_04_business_models.pdf  +  fig_04_business_models.png")
    else:
        print(f"  saved fig_04_business_models.pdf  (PNG not generated separately)")


# ═══════════════════════════════════════════════════════════════════════════════
# Run all
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating Chapter 1 figures …")
    make_fig01_pipeline()
    make_fig02_course_map()
    make_fig03_firm_spectrum()
    make_fig04_business_models()
    print("Done.")

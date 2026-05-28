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
    fig, ax = plt.subplots(figsize=(10, 4.0))
    ax.set_xlim(0.5, 12.5)
    ax.set_ylim(-0.3, 5.2)
    ax.axis("off")
    mpl.rcParams["axes.grid"] = False

    # Track centers
    THEORY_Y = 3.7
    LAB_Y    = 1.6
    ROW_H    = 0.85

    # Track background bands
    for cy, label in [(THEORY_Y, "Theory\nTrack"), (LAB_Y, "Lab /\nPractice")]:
        band = mpatches.FancyBboxPatch(
            (0.6, cy - ROW_H / 2 - 0.05), 11.8, ROW_H + 0.1,
            boxstyle="round,pad=0.05",
            facecolor="0.94", edgecolor="0.65", linewidth=0.8,
        )
        ax.add_patch(band)
        ax.text(0.1, cy, label, ha="right", va="center", fontsize=8,
                fontweight="bold", multialignment="center")

    # Theory: one cell per chapter/week grouping
    theory_cells = [
        (1,  1,  "Ch.1\nOverview",          0.88),
        (2,  1,  "Ch.2–3\nWorkflow",        0.88),
        (3,  1,  "Ch.4\nSpec & Risk",       0.75),
        (4,  1,  "Ch.5\nArchitecture",      0.75),
        (5,  1,  "Ch.6\nAI Tools",          0.88),
        (6,  1,  "Ch.7\nIoT & Safety",      0.88),
        (7,  1,  "Ch.8\nPlanning",          0.88),
        (8,  1,  "Ch.9\nBOM",               0.88),
        (9,  1,  "Ch.10\nEconomics",        0.75),
        (10, 1,  "Ch.11\nValidation",       0.88),
        (11, 1,  "Ch.12\nDocumentation",    0.88),
        (12, 1,  "Ch.13\nCost Bridge",      0.75),
    ]
    CW = 0.88   # cell width
    for wk, span, lbl, fc in theory_cells:
        rect = mpatches.FancyBboxPatch(
            (wk - CW * span / 2, THEORY_Y - ROW_H / 2 + 0.04),
            CW * span - 0.06, ROW_H - 0.08,
            boxstyle="round,pad=0.05",
            facecolor=str(fc), edgecolor="black", linewidth=0.7,
        )
        ax.add_patch(rect)
        ax.text(wk, THEORY_Y, lbl, ha="center", va="center",
                fontsize=6.5, multialignment="center")

    # Lab track: workflow stages as coloured spans
    stage_gray = [0.20, 0.32, 0.44, 0.56, 0.66, 0.76, 0.86]
    stages = [
        # (start_wk, end_wk, label, gray_idx)
        (2.0, 3.5, "① Specification\n& Risk",         0),
        (3.5, 4.8, "② Scope\n& Plan",                 1),
        (4.8, 5.8, "③ Architecture",                  2),
        (5.8, 7.5, "④ Subsystem\nDesign",             3),
        (7.5, 9.2, "⑤ Build &\nIntegrate",            4),
        (9.2, 11.0, "⑥ Validate\n& Measure",          5),
        (11.0, 12.5, "⑦ Compile &\nEconomics",        6),
    ]
    for s_wk, e_wk, lbl, gi in stages:
        fc = str(stage_gray[gi])
        rect = mpatches.FancyBboxPatch(
            (s_wk - 0.45, LAB_Y - ROW_H / 2 + 0.04),
            (e_wk - s_wk) - 0.06, ROW_H - 0.08,
            boxstyle="round,pad=0.05",
            facecolor=fc, edgecolor="black", linewidth=0.7,
        )
        ax.add_patch(rect)
        txt_col = "white" if stage_gray[gi] < 0.52 else "black"
        mid = (s_wk + e_wk) / 2 - 0.22
        ax.text(mid, LAB_Y, lbl, ha="center", va="center",
                fontsize=6.5, color=txt_col, fontweight="bold",
                multialignment="center")

    # Week 1 intro label
    rect = mpatches.FancyBboxPatch(
        (0.6, LAB_Y - ROW_H / 2 + 0.04), 0.88, ROW_H - 0.08,
        boxstyle="round,pad=0.05",
        facecolor="0.90", edgecolor="black", linewidth=0.7,
    )
    ax.add_patch(rect)
    ax.text(1.05, LAB_Y, "Intro", ha="center", va="center", fontsize=6.5,
            multialignment="center")

    # Week axis
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([f"Wk {w}" for w in range(1, 13)], fontsize=7.5)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="x", length=0, pad=2)
    ax.xaxis.set_tick_params(labelbottom=True)
    ax.set_yticks([])

    # Reposition the x-tick labels at the bottom
    ax.set_xlabel("")

    # Milestone markers (diamond + label above the figure)
    milestones = [
        (4,  "M1\nProposal"),
        (9,  "M2\nDesign Review"),
        (12, "M3\nFinal Portfolio"),
    ]
    for wk, lbl in milestones:
        # Vertical dashed line through both tracks
        ax.plot([wk, wk], [LAB_Y - ROW_H / 2, THEORY_Y + ROW_H / 2],
                color="black", lw=1.2, linestyle="--", zorder=5)
        # Diamond marker
        ax.plot(wk, THEORY_Y + ROW_H / 2 + 0.15, marker="D",
                ms=6, color="black", zorder=6)
        ax.text(wk, THEORY_Y + ROW_H / 2 + 0.45, lbl,
                ha="center", va="bottom", fontsize=7, fontweight="bold",
                multialignment="center")

    # Track labels on left
    ax.text(0.55, THEORY_Y + ROW_H / 2 + 0.05, "THEORY", ha="center",
            va="bottom", fontsize=6.5, color="0.4", fontstyle="italic")
    ax.text(0.55, LAB_Y + ROW_H / 2 + 0.05, "LAB", ha="center",
            va="bottom", fontsize=6.5, color="0.4", fontstyle="italic")

    fig.tight_layout()
    save(fig, "fig_02_course_map")


# ═══════════════════════════════════════════════════════════════════════════════
# FIG 03 — Firm-size spectrum vs process formality & documentation weight
# ═══════════════════════════════════════════════════════════════════════════════
def make_fig03_firm_spectrum():
    fig, ax = plt.subplots(figsize=(7, 3.6))

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
            rankdir="TB",
            splines="ortho",
            nodesep="0.35",
            ranksep="0.55",
            bgcolor="white",
            fontname="Helvetica",
            fontsize="11",
        ),
        node_attr=dict(
            shape="box",
            style="filled,rounded",
            fontname="Helvetica",
            fontsize="10",
            margin="0.12,0.06",
            penwidth="1.2",
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

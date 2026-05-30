"""
gen_figures.py — Generate 3 figures for Chapter 13: Version Control & Design History
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

DPI = 200

# ──────────────────────────────────────────────────────────────────────────────
# Figure 1: Git Flow Branching Diagram
# ──────────────────────────────────────────────────────────────────────────────
def make_fig1():
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')

    # Branch y-positions (top to bottom)
    y_hotfix  = 3.0
    y_main    = 2.0
    y_develop = 1.0
    y_feature = 0.0

    branch_color = '0.15'
    merge_color  = '0.35'

    # ── Branch labels (left side) ──
    for y, label in [(y_hotfix, 'hotfix'), (y_main, 'main'),
                     (y_develop, 'develop'), (y_feature, 'feature/mqtt-tls')]:
        ax.text(-0.1, y, label, ha='right', va='center', fontsize=9,
                fontstyle='italic', color='0.1')

    # ── Commit positions ──
    # main commits: x=1 (initial), x=5.5 (merge from develop), x=8 (v1.0-gate3)
    main_commits = [1.0, 5.5, 8.0]
    # develop: branches off main at x=1, commits at 2.5, 4.5, merges to main at 5.5
    develop_commits = [2.5, 4.5]
    develop_start = 1.0   # branches from main x=1
    develop_merge = 5.5   # merges to main x=5.5
    # feature: branches from develop at x=2.5, commits at 3.5, merges at 4.5
    feature_commits = [3.5]
    feature_start = 2.5
    feature_merge = 4.5
    # hotfix: branches from main at x=5.5, commit at 6.8, merges to main at 8.0
    hotfix_commits = [6.8]
    hotfix_start = 5.5
    hotfix_merge = 8.0

    # ── Draw branch lines ──
    # main: from x=0.8 to x=9.5
    ax.plot([0.8, 9.5], [y_main, y_main], color=branch_color, lw=2, zorder=2)
    # develop: from branch point to merge point
    ax.plot([develop_start, develop_merge], [y_develop, y_develop],
            color=branch_color, lw=2, zorder=2)
    # feature: from branch to merge
    ax.plot([feature_start, feature_merge], [y_feature, y_feature],
            color=branch_color, lw=2, zorder=2)
    # hotfix: from branch to merge
    ax.plot([hotfix_start, hotfix_merge], [y_hotfix, y_hotfix],
            color=branch_color, lw=2, zorder=2)

    # ── Merge / diverge diagonal lines (dashed) ──
    lw_merge = 1.5
    ls_merge = (0, (4, 3))  # dashed

    # develop branches from main at x=1
    ax.plot([develop_start, develop_start], [y_main, y_develop],
            color=merge_color, lw=lw_merge, linestyle='--', zorder=1)
    # develop merges to main at x=5.5
    ax.plot([develop_merge, develop_merge], [y_develop, y_main],
            color=merge_color, lw=lw_merge, linestyle='--', zorder=1)

    # feature branches from develop at x=2.5
    ax.plot([feature_start, feature_start], [y_develop, y_feature],
            color=merge_color, lw=lw_merge, linestyle='--', zorder=1)
    # feature merges to develop at x=4.5
    ax.plot([feature_merge, feature_merge], [y_feature, y_develop],
            color=merge_color, lw=lw_merge, linestyle='--', zorder=1)

    # hotfix branches from main at x=5.5
    ax.plot([hotfix_start, hotfix_start], [y_main, y_hotfix],
            color=merge_color, lw=lw_merge, linestyle='--', zorder=1)
    # hotfix merges to main at x=8.0
    ax.plot([hotfix_merge, hotfix_merge], [y_hotfix, y_main],
            color=merge_color, lw=lw_merge, linestyle='--', zorder=1)

    # ── Draw commits as filled circles ──
    dot_size = 60  # scatter s value (~5pt radius equivalent)
    dot_color = '0.2'
    dot_edge  = '0.05'

    ax.scatter(main_commits, [y_main]*len(main_commits),
               s=dot_size, color=dot_color, edgecolors=dot_edge, lw=0.8, zorder=5)
    ax.scatter(develop_commits, [y_develop]*len(develop_commits),
               s=dot_size, color=dot_color, edgecolors=dot_edge, lw=0.8, zorder=5)
    ax.scatter(feature_commits, [y_feature]*len(feature_commits),
               s=dot_size, color=dot_color, edgecolors=dot_edge, lw=0.8, zorder=5)
    ax.scatter(hotfix_commits, [y_hotfix]*len(hotfix_commits),
               s=dot_size, color=dot_color, edgecolors=dot_edge, lw=0.8, zorder=5)

    # Also mark the branch/merge points on main as commits
    ax.scatter([5.5, 8.0], [y_main, y_main],
               s=dot_size, color='0.5', edgecolors=dot_edge, lw=0.8, zorder=5)

    # ── Milestone annotations ──
    # "v1.0-gate3" tag above main at x=8.0 — annotate from well above to the dot
    ax.annotate('v1.0-gate3', xy=(8.0, y_main + 0.08),
                xytext=(8.0, y_main + 0.60),
                ha='center', va='bottom', fontsize=9, color='0.1',
                arrowprops=dict(arrowstyle='->', color='0.4', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.25', fc='0.88', ec='0.45', lw=1.0),
                zorder=10)

    # "Gate 3 design review" below main at x=8.0, with enough gap below hotfix merge line
    ax.text(8.0, y_main - 0.42, 'Gate 3 design review',
            ha='center', va='top', fontsize=9, color='0.2', style='italic')

    # "Hotfix: pull-up R value" above hotfix branch, centered on the hotfix commit
    ax.text(6.8, y_hotfix + 0.32, 'Hotfix: pull-up R value',
            ha='center', va='bottom', fontsize=9, color='0.2')

    # ── Time axis arrow at bottom ──
    ax.annotate('', xy=(9.6, -0.38), xytext=(0.6, -0.38),
                arrowprops=dict(arrowstyle='->', color='0.5', lw=1.2))
    ax.text(5.1, -0.48, 'time', ha='center', va='top', fontsize=9, color='0.4')

    plt.tight_layout(pad=0.3)
    base = '/home/user/Project-Planning-and-Prototyping/textbook/chapters/13-version-control/images/fig_01_git_flow'
    fig.savefig(base + '.pdf', dpi=DPI, bbox_inches='tight')
    fig.savefig(base + '.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('Figure 1 saved.')


# ──────────────────────────────────────────────────────────────────────────────
# Figure 2: DHF Tree Diagram
# ──────────────────────────────────────────────────────────────────────────────
def draw_box(ax, cx, cy, w, h, gray, text, fontsize=9, text_color='white'):
    """Draw a centered rounded rectangle with text."""
    x = cx - w / 2
    y = cy - h / 2
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle='round,pad=0.02',
                         facecolor=str(gray), edgecolor='0.1', lw=1.2, zorder=3)
    ax.add_patch(box)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, zorder=4, wrap=False)


def connect(ax, x1, y1, x2, y2, lw=1.5):
    ax.plot([x1, x2], [y1, y2], color='0.2', lw=lw, zorder=2)


def make_fig2():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(-0.1, 9.1)
    ax.set_ylim(-0.25, 2.85)
    ax.axis('off')

    # Row y positions
    y_root   = 2.5
    y_l1     = 1.7
    y_l2     = 0.85
    y_output = 0.1

    bh = 0.38   # box height

    # ── Root ──
    draw_box(ax, 4.5, y_root, 2.8, bh, 0.35, 'Design History File (DHF)', fontsize=9, text_color='white')

    # ── Level 1 ──
    l1_items = [
        (1.5,  'Design\nRecords'),
        (4.5,  'Test\nRecords'),
        (7.5,  'Approval\nRecords'),
    ]
    bw_l1 = 2.2
    bh_l1 = 0.48
    for cx, label in l1_items:
        connect(ax, 4.5, y_root - bh/2, cx, y_l1 + bh_l1/2)
        draw_box(ax, cx, y_l1, bw_l1, bh_l1, 0.55, label, fontsize=9, text_color='white')

    # ── Level 2 ──
    # Under Design Records (cx=1.5): 4 items spread
    dr_items = [
        (0.18, 'Specifications\n(Ch.4)'),
        (1.05, 'Architecture\n(Ch.5)'),
        (1.90, 'BOM\n(Ch.11)'),
        (2.75, 'ECO Log'),
    ]
    bw_dr = 0.82
    for cx2, label in dr_items:
        connect(ax, 1.5, y_l1 - bh_l1/2, cx2, y_l2 + bh/2)
        draw_box(ax, cx2, y_l2, bw_dr, bh, 0.80, label, fontsize=8.5, text_color='0.05')

    # Under Test Records (cx=4.5): 3 items
    tr_items = [
        (3.75, 'Bench Test\nReports'),
        (4.5,  'Integration\nTest'),
        (5.25, 'Acceptance\nTest'),
    ]
    bw_tr = 0.70
    for cx2, label in tr_items:
        connect(ax, 4.5, y_l1 - bh_l1/2, cx2, y_l2 + bh/2)
        draw_box(ax, cx2, y_l2, bw_tr, bh, 0.80, label, fontsize=8.5, text_color='0.05')

    # Under Approval Records (cx=7.5): 2 items
    ar_items = [
        (7.0,  'Gate 3\nChecklist'),
        (8.0,  'Sign-offs'),
    ]
    bw_ar = 0.90
    for cx2, label in ar_items:
        connect(ax, 7.5, y_l1 - bh_l1/2, cx2, y_l2 + bh/2)
        draw_box(ax, cx2, y_l2, bw_ar, bh, 0.80, label, fontsize=8.5, text_color='0.05')

    # ── Output node ──
    out_cx = 4.5
    # Draw a horizontal collector line at y = y_output + bh/2 + 0.15
    y_collect = y_output + bh / 2 + 0.18
    # Lines from each L2 subtree center down to collector level
    for sub_cx in [1.5, 4.5, 7.5]:
        ax.plot([sub_cx, sub_cx], [y_l2 - bh/2 - 0.02, y_collect], color='0.2', lw=1.5, zorder=2)
    ax.plot([1.5, 7.5], [y_collect, y_collect], color='0.2', lw=1.5, zorder=2)
    ax.plot([out_cx, out_cx], [y_collect, y_output + bh/2], color='0.2', lw=1.5, zorder=2)
    draw_box(ax, out_cx, y_output, 3.2, bh, 0.35,
             '→  Gate 3 Submission Package', fontsize=9, text_color='white')

    plt.tight_layout(pad=0.3)
    base = '/home/user/Project-Planning-and-Prototyping/textbook/chapters/13-version-control/images/fig_02_dhf_structure'
    fig.savefig(base + '.pdf', dpi=DPI, bbox_inches='tight')
    fig.savefig(base + '.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('Figure 2 saved.')


# ──────────────────────────────────────────────────────────────────────────────
# Figure 3: ECO Flow Diagram
# ──────────────────────────────────────────────────────────────────────────────
def make_fig3():
    fig, ax = plt.subplots(figsize=(9, 2.8))
    ax.set_xlim(-0.3, 9.3)
    ax.set_ylim(-0.3, 2.8)
    ax.axis('off')

    # ── Helper functions ──
    def oval(cx, cy, w, h, gray, text, fontsize=9):
        el = mpatches.Ellipse((cx, cy), w, h,
                              facecolor=str(gray), edgecolor='0.1', lw=1.5, zorder=3)
        ax.add_patch(el)
        tc = 'white' if gray < 0.55 else '0.05'
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
                color=tc, zorder=4)

    def rect(cx, cy, w, h, gray, text, fontsize=9):
        x = cx - w/2
        y = cy - h/2
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle='round,pad=0.03',
                             facecolor=str(gray), edgecolor='0.1', lw=1.2, zorder=3)
        ax.add_patch(box)
        tc = 'white' if gray < 0.55 else '0.05'
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
                color=tc, zorder=4)

    def diamond(cx, cy, w, h, gray, text, fontsize=9):
        hw = w/2; hh = h/2
        pts = np.array([
            [cx,      cy + hh],
            [cx + hw, cy     ],
            [cx,      cy - hh],
            [cx - hw, cy     ],
        ])
        from matplotlib.patches import Polygon
        poly = Polygon(pts, closed=True,
                       facecolor=str(gray), edgecolor='0.1', lw=1.5, zorder=3)
        ax.add_patch(poly)
        tc = 'white' if gray < 0.55 else '0.05'
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
                color=tc, zorder=4)

    def arrow(x1, y1, x2, y2, label=None, label_side='top'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='0.1', lw=1.5),
                    zorder=2)
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            offset = 0.13 if label_side == 'top' else -0.13
            ax.text(mx, my + offset, label, ha='center', va='center',
                    fontsize=8.5, color='0.1', zorder=5)

    # ── Layout (left-to-right, two-row for YES branches) ──
    # Row layout:
    #   Top row (y=2.2): Start → D1 → upper YES path
    #   Middle row (y=1.4): D1 NO → D2 → middle YES path
    #   Bottom row (y=0.6): D2 NO path
    #   End row (y=0.15): End oval

    # All rows at y values:
    y_top = 2.2
    y_mid = 1.4
    y_bot = 0.62
    y_end = 0.1

    bw = 1.25  # rect width
    bh = 0.40  # rect height
    dw = 1.40  # diamond width
    dh = 0.52  # diamond height
    ow = 1.15  # oval width
    oh = 0.38  # oval height

    # ── Start oval ──
    x_start = 0.75
    oval(x_start, y_top, ow, oh, 0.35, 'Change\nidentified', fontsize=8.5)

    # ── Diamond 1: Safety/regulatory? ──
    x_d1 = 2.3
    arrow(x_start + ow/2, y_top, x_d1 - dw/2, y_top)
    diamond(x_d1, y_top, dw, dh, 0.65, 'Safety /\nreg. impact?', fontsize=8.5)

    # YES path (top row, going right)
    x_eco_req  = 4.0
    x_eco_rev  = 5.45
    x_upd_dhf  = 6.95
    arrow(x_d1 + dw/2, y_top, x_eco_req - bw/2, y_top, label='YES')
    rect(x_eco_req,  y_top, bw, bh, 0.80, 'Formal ECO\nrequired', fontsize=8.5)
    arrow(x_eco_req + bw/2,  y_top, x_eco_rev - bw/2, y_top)
    rect(x_eco_rev,  y_top, bw, bh, 0.80, 'ECO review\nboard', fontsize=8.5)
    arrow(x_eco_rev + bw/2,  y_top, x_upd_dhf - bw/2, y_top)
    rect(x_upd_dhf,  y_top, bw, bh, 0.80, 'Update DHF\n+ re-verify', fontsize=8.5)

    # NO path — drop from D1 to D2 (middle row)
    x_d2 = 2.3
    arrow(x_d1, y_top - dh/2, x_d2, y_mid + dh/2, label='NO', label_side='top')
    diamond(x_d2, y_mid, dw, dh, 0.65, 'Gate deliv.\nor BOM?', fontsize=8.5)

    # YES path (middle row)
    x_inf_eco  = 4.0
    x_upd_bom  = 5.45
    arrow(x_d2 + dw/2, y_mid, x_inf_eco - bw/2, y_mid, label='YES')
    rect(x_inf_eco, y_mid, bw, bh, 0.80, 'Informal ECO\nrecord', fontsize=8.5)
    arrow(x_inf_eco + bw/2, y_mid, x_upd_bom - bw/2, y_mid)
    rect(x_upd_bom, y_mid, bw, bh, 0.80, 'Update BOM /\nschematic+log', fontsize=8.5)

    # NO path — drop from D2 to bottom row
    x_inplace  = 4.0
    x_log_msg  = 5.45
    arrow(x_d2, y_mid - dh/2, x_d2, y_bot + bh/2, label='NO', label_side='top')
    # horizontal arrow to in-place fix
    arrow(x_d2 + 0.0, y_bot, x_inplace - bw/2, y_bot)
    # Actually: NO arrow exits left side of d2 at y_bot — let's draw a corner
    # Redraw: vertical down then horizontal right
    # Remove the direct arrow, draw L-shape
    # (Already drew the vertical; now horizontal)
    rect(x_inplace, y_bot, bw, bh, 0.80, 'In-place\nfix', fontsize=8.5)
    arrow(x_inplace + bw/2, y_bot, x_log_msg - bw/2, y_bot)
    rect(x_log_msg, y_bot, bw, bh, 0.80, 'Log commit\nmessage only', fontsize=8.5)

    # ── End oval — collect all paths ──
    x_end = 8.45
    oval(x_end, y_mid, ow, oh, 0.35, 'Change\ncomplete', fontsize=8.5)

    # Connect YES top path to end
    arrow(x_upd_dhf + bw/2, y_top, x_end, y_top)
    # Vertical line from top-right corner down to end oval (mid level)
    ax.plot([x_end, x_end], [y_top, y_mid + oh/2], color='0.1', lw=1.5, zorder=2)

    # Connect YES mid path to end
    arrow(x_upd_bom + bw/2, y_mid, x_end - ow/2, y_mid)

    # Connect NO bot path to end
    arrow(x_log_msg + bw/2, y_bot, x_end, y_bot)
    ax.plot([x_end, x_end], [y_bot, y_mid - oh/2], color='0.1', lw=1.5, zorder=2)

    plt.tight_layout(pad=0.3)
    base = '/home/user/Project-Planning-and-Prototyping/textbook/chapters/13-version-control/images/fig_03_eco_flow'
    fig.savefig(base + '.pdf', dpi=DPI, bbox_inches='tight')
    fig.savefig(base + '.png', dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('Figure 3 saved.')


if __name__ == '__main__':
    make_fig1()
    make_fig2()
    make_fig3()
    print('All figures generated.')

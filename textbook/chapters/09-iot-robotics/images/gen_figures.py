"""
Generate three figures for Chapter 9: IoT, Robotics & Safety as a Design Obligation.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.grid": False,
    "savefig.bbox": "tight",
})


def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
    plt.close(fig)


OUT = "/home/user/Project-Planning-and-Prototyping/textbook/chapters/09-iot-robotics/images"

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — fig_01_attack_surface
# Three-layer IoT architecture with attack surface labels on the right
# ─────────────────────────────────────────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(9, 2.8))
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 3)
ax1.axis("off")

layer_colors = [0.85, 0.70, 0.55]
layer_labels = [
    "Device Layer\n(Firmware / Hardware)",
    "Communication Layer\n(MQTT / BLE / CoAP)",
    "Management Layer\n(OTA updates / Admin interface)",
]
layer_heights = [0, 1, 2]  # bottom y of each band
band_h = 0.90  # height of each band

# Draw bands (only up to x=6.8 to leave room for annotations on right)
band_right = 6.8
for i, (y, color, label) in enumerate(zip(layer_heights, layer_colors, layer_labels)):
    rect = mpatches.FancyBboxPatch(
        (0.1, y + 0.05), band_right - 0.1, band_h,
        boxstyle="round,pad=0.02",
        linewidth=1.2,
        edgecolor="0.3",
        facecolor=str(color),
    )
    ax1.add_patch(rect)
    ax1.text(
        band_right / 2, y + 0.05 + band_h / 2,
        label,
        ha="center", va="center",
        fontsize=11, fontweight="bold",
        color="0.15",
    )

# Attack surface annotations on the right
# Boundaries: bottom/middle at y=1.0, middle/top at y=2.0, above top at y=3.0
attack_surfaces = [
    (1.0,  "Attack Surface 1:\nConnectivity"),
    (2.0,  "Attack Surface 2:\nProtocol"),
    (2.95, "Attack Surface 3:\nManagement"),
]

x_line_start = band_right + 0.15
x_label = band_right + 0.35
x_arrow_tip = band_right + 0.12

for y_bound, label in attack_surfaces:
    # Small horizontal tick line at boundary
    ax1.plot([x_line_start, x_line_start + 0.12], [y_bound, y_bound],
             color="0.2", lw=1.5, clip_on=False)
    # Vertical bracket line extending slightly
    ax1.plot([x_line_start, x_line_start], [y_bound - 0.05, y_bound + 0.05],
             color="0.2", lw=1.2, clip_on=False)
    # Arrow pointing left toward the band boundary
    ax1.annotate(
        "",
        xy=(x_arrow_tip, y_bound),
        xytext=(x_line_start + 0.13, y_bound),
        arrowprops=dict(arrowstyle="-|>", color="0.2", lw=1.2),
        annotation_clip=False,
    )
    # Label text
    ax1.text(
        x_label + 0.15, y_bound,
        label,
        ha="left", va="center",
        fontsize=9.5,
        color="0.15",
        clip_on=False,
    )

save(fig1, f"{OUT}/fig_01_attack_surface")
print("Figure 1 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — fig_02_power_budget
# Duty-cycled current profile
# ─────────────────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(8, 2.8))

# Build the current waveform
pulses = [(0.5, 0.7), (3.5, 3.7), (6.5, 6.7)]
I_sleep = 0.05
I_active = 80.0
I_avg = 1.649

# Dense time array
t_all = np.linspace(0, 10, 50000)
I_all = np.full_like(t_all, I_sleep)
for t_start, t_end in pulses:
    mask = (t_all >= t_start) & (t_all <= t_end)
    I_all[mask] = I_active

ax2.plot(t_all, I_all, color="0.15", lw=1.4)

# I_avg dashed line
ax2.axhline(I_avg, color="0.3", lw=1.5, linestyle="--")
ax2.text(
    9.85, I_avg + 3.0,
    r"$I_{\mathrm{avg}} = 1.65$ mA",
    ha="right", va="bottom",
    fontsize=10, color="0.15",
)

# Annotate active peak — place label above the first pulse
ax2.annotate(
    "Active: 80 mA",
    xy=(0.6, 80),
    xytext=(1.6, 76),
    fontsize=10,
    color="0.15",
    arrowprops=dict(arrowstyle="-|>", color="0.3", lw=1.2),
    va="center",
)

# Annotate sleep floor
ax2.text(
    5.0, 0.05 + 3.5,
    "Sleep: 0.05 mA",
    ha="center", va="bottom",
    fontsize=10, color="0.15",
)

ax2.set_xlim(0, 10)
ax2.set_ylim(0, 85)
ax2.set_xlabel("Time (duty cycle period)", fontsize=11)
ax2.set_ylabel("Current (mA)", fontsize=11)
ax2.tick_params(labelsize=10)
for spine in ax2.spines.values():
    spine.set_linewidth(1.2)

save(fig2, f"{OUT}/fig_02_power_budget")
print("Figure 2 saved.")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3 — fig_03_robot_safety
# Top-down workspace diagram
#
# Coordinate system: x 0-9, y 0-2.8
# Key layout decisions (all text positions verified to be non-overlapping):
#   - Workspace fills most of the figure: x=0.15..8.85, y=0.15..2.65
#   - Robot box: x=0.55..2.55, y=0.55..2.10  (tall left block)
#   - Guarded zone (dashed): x=0.38..2.72, y=0.38..2.27
#   - E-STOP circle: at bottom-left of workspace, x=0.75, y=0.27 (below robot)
#   - E-STOP label: to the right of circle
#   - Arrow: from E-STOP diagonally up-right to robot bottom edge
#   - Arrow label: placed to the right of E-STOP label, in the bottom strip
#   - "Guarded zone" label: ABOVE the dashed box, y~2.30, within workspace top strip
#   - "Robot workspace boundary" label: top-right corner
#   - Safe zone: right portion x~4.5-8.5, y~1.4
# ─────────────────────────────────────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(9, 2.8))
ax3.set_xlim(0, 9)
ax3.set_ylim(0, 2.8)
ax3.axis("off")

# ── Workspace outer boundary ───────────────────────────────────────────────
ws_x, ws_y = 0.15, 0.15
ws_w, ws_h = 8.70, 2.50
workspace = mpatches.FancyBboxPatch(
    (ws_x, ws_y), ws_w, ws_h,
    boxstyle="square,pad=0", linewidth=1.5,
    edgecolor="0.45", facecolor="0.95",
)
ax3.add_patch(workspace)
# Workspace label: top-right, inside
ax3.text(
    ws_x + ws_w - 0.14, ws_y + ws_h - 0.10,
    "Robot workspace boundary",
    ha="right", va="top", fontsize=9, color="0.35",
)

# ── Safe zone label ────────────────────────────────────────────────────────
ax3.text(
    6.20, 1.40,
    "Safe zone\n(no personnel during operation)",
    ha="center", va="center", fontsize=9, color="0.30",
)

# ── Robot box ─────────────────────────────────────────────────────────────
robot_x, robot_y = 0.55, 0.55
robot_w, robot_h = 2.00, 1.55
robot_rect = mpatches.FancyBboxPatch(
    (robot_x, robot_y), robot_w, robot_h,
    boxstyle="round,pad=0.06", linewidth=1.5,
    edgecolor="0.25", facecolor="0.70",
)
ax3.add_patch(robot_rect)
ax3.text(
    robot_x + robot_w / 2, robot_y + robot_h * 0.70,
    "Robot\n(sort actuator)",
    ha="center", va="center",
    fontsize=9.5, fontweight="bold", color="0.10",
)
ax3.text(
    robot_x + robot_w / 2, robot_y + robot_h * 0.24,
    "Fail-safe state:\nActuator de-energised",
    ha="center", va="center",
    fontsize=9, color="0.20", style="italic",
)

# ── Guarded zone dashed border (slightly larger than robot box) ───────────
gd = 0.17  # margin
guard_x = robot_x - gd
guard_y_v = robot_y - gd
guard_w = robot_w + 2 * gd
guard_h = robot_h + 2 * gd
guarded = mpatches.FancyBboxPatch(
    (guard_x, guard_y_v), guard_w, guard_h,
    boxstyle="square,pad=0", linewidth=1.5,
    edgecolor="0.30", facecolor="none", linestyle="--",
)
ax3.add_patch(guarded)
# Guarded zone label: ABOVE dashed box top, in the clear strip between
# guard top (y~2.27) and workspace top (y~2.65)
ax3.text(
    guard_x + guard_w / 2, guard_y_v + guard_h + 0.07,
    "Guarded zone (physical barrier)",
    ha="center", va="bottom", fontsize=9, color="0.25",
)

# ── E-STOP circle: at bottom-centre of workspace, x=3.0, below robot zone ─
# Place it right of robot/guard zone, in clear space at the bottom strip
# Workspace bottom y=0.15, guard bottom y~0.38  => strip height ~0.23
# That's very thin for a circle r=0.16 plus label. Use x=3.2, y=0.27 (centre)
estop_cx, estop_cy = 3.20, 0.27
estop_r = 0.13
estop_circle = plt.Circle(
    (estop_cx, estop_cy), estop_r,
    linewidth=1.5, edgecolor="0.15", facecolor="0.20", zorder=6,
)
ax3.add_patch(estop_circle)
# E-STOP label to the right of the circle
ax3.text(
    estop_cx + estop_r + 0.10, estop_cy,
    "E-STOP",
    ha="left", va="center",
    fontsize=9, fontweight="bold", color="0.15",
)

# Arrow: from E-STOP circle top → bottom of robot box (tip on robot face, not guard border)
ax3.annotate(
    "",
    xy=(robot_x + robot_w * 0.50, robot_y + 0.06),
    xytext=(estop_cx - 0.02, estop_cy + estop_r + 0.03),
    arrowprops=dict(arrowstyle="-|>", color="0.25", lw=1.3),
)

# Arrow label: to the right of the E-STOP label, on the same bottom strip
# E-STOP label ends approximately at x = estop_cx + estop_r + 0.10 + text_width
# "E-STOP" at 8.5pt ~ 0.55 units wide => label ends ~x=4.1
# Place arrow label at x=4.2, same y as E-STOP centre
ax3.text(
    4.25, estop_cy,
    "Cuts motor power (NC relay)",
    ha="left", va="center",
    fontsize=9, color="0.20",
)

save(fig3, f"{OUT}/fig_03_robot_safety")
print("Figure 3 saved.")

print("All figures generated successfully.")

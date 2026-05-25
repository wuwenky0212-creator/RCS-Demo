"""RCS-Demo brand mark — canvas render.

Philosophy: 'Doppia Partita'  — paired truth, the ledger fold, mirror balance.
Outputs:
  * brand/RCS-MARK-CONSTRUCTION.png   (1600 x 2000 — type-specimen sheet)
  * brand/rcs-mark.svg                (the working mark, drop-in for the app)
"""
from __future__ import annotations
import os, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle, Circle
import matplotlib.lines as mlines

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/sessions/nice-lucid-planck/mnt/.claude/skills/canvas-design/canvas-fonts"

# ---------------------------------------------------------------------------
# Type registration
# ---------------------------------------------------------------------------
fonts = {
    "serif":         os.path.join(FONT_DIR, "IBMPlexSerif-Regular.ttf"),
    "serif_bold":    os.path.join(FONT_DIR, "IBMPlexSerif-Bold.ttf"),
    "serif_italic":  os.path.join(FONT_DIR, "IBMPlexSerif-Italic.ttf"),
    "mono":          os.path.join(FONT_DIR, "GeistMono-Regular.ttf"),
    "mono_bold":     os.path.join(FONT_DIR, "GeistMono-Bold.ttf"),
}
fp = {k: font_manager.FontProperties(fname=v) for k, v in fonts.items()}

# ---------------------------------------------------------------------------
# Palette  (single ink + bone + a single carmine hairline)
# ---------------------------------------------------------------------------
INK     = "#1B2A4E"
INK_2   = "#2A3960"
PAGE    = "#EFEAE0"
RULE    = "#B7AE9E"
CARMINE = "#A8323A"

# ---------------------------------------------------------------------------
# THE MARK — geometric R, built on a 12 x 9 unit grid
# ---------------------------------------------------------------------------
def build_R_path(stem_x=0.0, baseline=0.0, height=12.0, stem_w=1.7,
                 bowl_h=6.6, bowl_extent=7.4):
    H, SW, BH, BX = height, stem_w, bowl_h, bowl_extent
    bowl_top, bowl_bot = baseline + H, baseline + H - BH
    bowl_cy = (bowl_top + bowl_bot) / 2.0
    bowl_outer_r = BH / 2.0
    bowl_outer_cx = stem_x + SW + (BX - SW - bowl_outer_r)
    bowl_inner_r = bowl_outer_r - SW * 0.92

    leg_top_y = bowl_cy
    leg_bot_x = stem_x + BX + 0.05
    leg_bot_y = baseline
    leg_w     = SW * 0.95
    K = 0.5522847498

    verts, codes = [], []
    def M(x, y): verts.append((x, y)); codes.append(Path.MOVETO)
    def L(x, y): verts.append((x, y)); codes.append(Path.LINETO)
    def C(c1, c2, p):
        verts.extend([c1, c2, p]); codes.extend([Path.CURVE4]*3)
    def Z(): verts.append((0, 0)); codes.append(Path.CLOSEPOLY)

    # Outer
    M(stem_x, baseline)
    L(stem_x, bowl_top)
    L(bowl_outer_cx, bowl_top)
    cx, cy, r = bowl_outer_cx, bowl_cy, bowl_outer_r
    C((cx + r*K, cy + r), (cx + r, cy + r*K), (cx + r, cy))
    C((cx + r, cy - r*K), (cx + r*K, cy - r), (cx, cy - r))
    L(stem_x + SW, bowl_bot)
    L(stem_x + SW, leg_top_y - 0.05)
    L(stem_x + SW + leg_w * 0.7, leg_top_y - 0.05)
    L(leg_bot_x + leg_w/2, leg_bot_y)
    L(leg_bot_x - leg_w/2, leg_bot_y)
    L(stem_x + SW, leg_top_y + 0.55)
    L(stem_x + SW, baseline)
    Z()

    # Inner counter
    icx, icy, ir = bowl_outer_cx, bowl_cy, bowl_inner_r
    inner_top = bowl_top - SW * 0.85
    inner_bot = bowl_bot + SW * 0.85
    M(stem_x + SW, inner_top)
    L(icx, inner_top)
    C((icx + ir*K, icy + ir), (icx + ir, icy + ir*K), (icx + ir, icy))
    C((icx + ir, icy - ir*K), (icx + ir*K, icy - ir), (icx, icy - ir))
    L(stem_x + SW, inner_bot)
    L(stem_x + SW, inner_top)
    Z()
    return Path(verts, codes)


# ---------------------------------------------------------------------------
# CANVAS
# ---------------------------------------------------------------------------
W, H = 8.0, 10.0  # 1600 x 2000 at 200 dpi
fig = plt.figure(figsize=(W, H), dpi=200, facecolor=PAGE)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100); ax.set_ylim(0, 125)
ax.set_aspect("equal"); ax.axis("off")
ax.set_facecolor(PAGE)

# ---- top & bottom register hairlines
ax.add_line(mlines.Line2D([6, 94], [120.5, 120.5], color=INK, linewidth=0.55))
ax.add_line(mlines.Line2D([6, 94], [4.5, 4.5],     color=INK, linewidth=0.55))

# ---- top register text
ax.text(6, 122.2, "RCS-Demo  ·  BRAND  SYSTEM  ·  PLATE  01",
        fontproperties=fp["mono"], fontsize=6.2, color=INK, va="bottom", ha="left")
ax.text(94, 122.2, "DOPPIA  PARTITA  ·  1494 — 2026",
        fontproperties=fp["mono"], fontsize=6.2, color=INK, va="bottom", ha="right")

# ---- bottom register text
ax.text(6, 2.6, "VERIFIED  ·  BALANCED  ·  CLOSED",
        fontproperties=fp["mono"], fontsize=6.2, color=INK, va="bottom", ha="left")
ax.text(94, 2.6, "N°  001  /  R",
        fontproperties=fp["mono"], fontsize=6.2, color=INK, va="bottom", ha="right")

# ---- corner registration crosses
def reg_cross(x, y, s=1.6, c=INK, lw=0.5):
    ax.add_line(mlines.Line2D([x - s, x + s], [y, y], color=c, linewidth=lw))
    ax.add_line(mlines.Line2D([x, x], [y - s, y + s], color=c, linewidth=lw))
    ax.add_patch(Circle((x, y), s * 0.5, fill=False, edgecolor=c, linewidth=lw))
for (cx, cy) in [(6, 6), (94, 6), (6, 119), (94, 119)]:
    reg_cross(cx, cy)

# ---- header block
ax.text(8.5, 113.6, "01", fontproperties=fp["serif_bold"], fontsize=16, color=INK)
ax.add_line(mlines.Line2D([13.4, 16.0], [114.4, 114.4], color=INK, linewidth=0.7))
ax.text(16.6, 114.0, "THE  MARK",
        fontproperties=fp["serif"], fontsize=10.5, color=INK, va="baseline")
ax.text(16.6, 111.4, "CONSTRUCTED  ON  A  TWELVE-UNIT  GRID",
        fontproperties=fp["mono"], fontsize=5.4, color=INK_2, va="baseline")

ax.text(91.5, 114.0, "RCS / 5.0",
        fontproperties=fp["serif_italic"], fontsize=10.5, color=INK,
        va="baseline", ha="right")
ax.text(91.5, 111.4, "RECONCILIATION  ·  CLEARING  ·  SETTLEMENT",
        fontproperties=fp["mono"], fontsize=5.4, color=INK_2,
        va="baseline", ha="right")

# ---------------------------------------------------------------------------
# Construction zone — the hero R
# ---------------------------------------------------------------------------
GRID_W, GRID_H = 9, 12
SCALE   = 5.0
zone_h  = GRID_H * SCALE        # 60
ZX0 = 50 - GRID_W * SCALE / 2   # centred horizontally
ZY0 = 30                         # baseline of grid
gx0 = ZX0
gy0 = ZY0
gx1 = ZX0 + GRID_W * SCALE
gy1 = ZY0 + GRID_H * SCALE       # → 90

# faint construction grid (dotted)
for i in range(GRID_W + 1):
    x = gx0 + i * SCALE
    ax.add_line(mlines.Line2D([x, x], [gy0, gy1], color=RULE, linewidth=0.22,
                              linestyle=(0, (1, 2.5))))
for i in range(GRID_H + 1):
    y = gy0 + i * SCALE
    ax.add_line(mlines.Line2D([gx0, gx1], [y, y], color=RULE, linewidth=0.22,
                              linestyle=(0, (1, 2.5))))

# corner ticks (architectural-drawing feel)
def corner_tick(x, y, dx, dy, length=1.8, lw=0.7):
    ax.add_line(mlines.Line2D([x, x + dx*length], [y, y], color=INK, linewidth=lw))
    ax.add_line(mlines.Line2D([x, x], [y, y + dy*length], color=INK, linewidth=lw))
for (x, y, dx, dy) in [(gx0, gy0, +1, +1), (gx1, gy0, -1, +1),
                       (gx0, gy1, +1, -1), (gx1, gy1, -1, -1)]:
    corner_tick(x, y, dx, dy)

# Mirror axis ("the ledger fold") — single carmine hairline.
# Label sits BELOW the grid, well clear of the dimension callout.
mirror_x = gx0 + GRID_W * SCALE / 2.0
ax.add_line(mlines.Line2D([mirror_x, mirror_x], [gy0 - 3.5, gy1 + 1.6],
                          color=CARMINE, linewidth=0.55, alpha=0.95))
ax.text(mirror_x + 1.0, gy0 - 2.6, "fold",
        fontproperties=fp["serif_italic"], fontsize=5.0, color=CARMINE, va="center")

# Outer ledger column rules — the pair of running rules
ax.add_line(mlines.Line2D([gx0 - 3.2, gx0 - 3.2], [gy0 - 0.4, gy1 + 0.4],
                          color=INK, linewidth=0.5))
ax.add_line(mlines.Line2D([gx1 + 3.2, gx1 + 3.2], [gy0 - 0.4, gy1 + 0.4],
                          color=INK, linewidth=0.5))

# Build & draw the principal R + ghost (mirrored / paired entry)
mark_path = build_R_path(stem_x=0, baseline=0, height=GRID_H,
                         stem_w=1.7, bowl_h=6.6, bowl_extent=7.4)

def transformed(p, sx, tx, ty):
    return Path([(vx * sx * SCALE + tx, vy * SCALE + ty) for (vx, vy) in p.vertices],
                p.codes)

R_OFFSET_X = 0.7    # left-flush within grid
ghost_path = transformed(mark_path, sx=-1,
                         tx=gx0 + GRID_W * SCALE - R_OFFSET_X * SCALE,
                         ty=gy0)
real_path  = transformed(mark_path, sx=+1,
                         tx=gx0 + R_OFFSET_X * SCALE,
                         ty=gy0)

ax.add_patch(PathPatch(ghost_path, facecolor="none",
                       edgecolor=INK, linewidth=0.45, alpha=0.16))
ax.add_patch(PathPatch(real_path, facecolor=INK, edgecolor="none", linewidth=0))

# Dimension callouts
def dim_h(x0, x1, y, txt, offset=1.6):
    ax.add_line(mlines.Line2D([x0, x1], [y, y], color=INK_2, linewidth=0.4))
    ax.add_line(mlines.Line2D([x0, x0], [y - 0.55, y + 0.55], color=INK_2, linewidth=0.4))
    ax.add_line(mlines.Line2D([x1, x1], [y - 0.55, y + 0.55], color=INK_2, linewidth=0.4))
    ax.text((x0 + x1) / 2, y + offset, txt, fontproperties=fp["mono"],
            fontsize=4.6, color=INK_2, ha="center", va="bottom")

def dim_v(x, y0, y1, txt, offset=1.6):
    ax.add_line(mlines.Line2D([x, x], [y0, y1], color=INK_2, linewidth=0.4))
    ax.add_line(mlines.Line2D([x - 0.55, x + 0.55], [y0, y0], color=INK_2, linewidth=0.4))
    ax.add_line(mlines.Line2D([x - 0.55, x + 0.55], [y1, y1], color=INK_2, linewidth=0.4))
    ax.text(x - offset, (y0 + y1) / 2, txt, fontproperties=fp["mono"],
            fontsize=4.6, color=INK_2, ha="right", va="center", rotation=90)

dim_h(gx0, gx1, gy1 + 2.6, "9 u")
dim_v(gx0 - 5.5, gy0, gy1, "12 u")

# Proof markers at provable construction junctions
key_pts = [
    (gx0 + R_OFFSET_X * SCALE, gy0),                                # bottom-left of stem
    (gx0 + R_OFFSET_X * SCALE, gy1),                                # top of stem
    (gx0 + (R_OFFSET_X + 1.7) * SCALE, gy0 + 5.4 * SCALE),          # bowl midline / stem
    (gx0 + (R_OFFSET_X + 7.4) * SCALE, gy0 + 8.7 * SCALE),          # bowl right midline
]
for (px, py) in key_pts:
    ax.add_patch(Circle((px, py), 0.55, facecolor=PAGE, edgecolor=INK_2, linewidth=0.4))

# ---------------------------------------------------------------------------
# WORDMARK — single, clean line below the mark
# Centered, well-letterspaced, RCS in serif + 5.0 in mono, with thin separator
# ---------------------------------------------------------------------------
WY = 19
# Hairline rule above wordmark zone
ax.add_line(mlines.Line2D([30, 70], [25.5, 25.5], color=RULE, linewidth=0.4))

# Manually typeset the wordmark for tight kerning + mixed type
ax.text(50 - 11.5, WY, "R", fontproperties=fp["serif_bold"], fontsize=28, color=INK,
        ha="left", va="baseline")
ax.text(50 - 4.0, WY,  "C", fontproperties=fp["serif_bold"], fontsize=28, color=INK,
        ha="left", va="baseline")
ax.text(50 + 4.0, WY,  "S", fontproperties=fp["serif_bold"], fontsize=28, color=INK,
        ha="left", va="baseline")

# A short separator dot
ax.text(50 + 13.5, WY + 1.2, "·", fontproperties=fp["serif_bold"], fontsize=20, color=CARMINE,
        ha="center", va="baseline")

ax.text(50 + 17.0, WY,  "5.0", fontproperties=fp["mono"], fontsize=16, color=INK_2,
        ha="left", va="baseline")

# tag line below wordmark
ax.text(50, 14.0, "RECONCILIATION   ·   CLEARING   ·   SETTLEMENT",
        fontproperties=fp["mono"], fontsize=5.0, color=INK_2,
        ha="center", va="baseline")

# A single small carmine seal — the equals sign IS the doppia partita's
# balance affirmation: debits = credits, the books reconcile.
ax.add_patch(Circle((85, 17), 1.7, fill=False, edgecolor=CARMINE, linewidth=0.55))
ax.text(85, 17.0, "=", fontproperties=fp["mono_bold"], fontsize=7, color=CARMINE,
        ha="center", va="center")
ax.text(85, 13.4, "PAR",
        fontproperties=fp["mono"], fontsize=4.2, color=CARMINE,
        ha="center", va="center")

# ---------------------------------------------------------------------------
# Save canvas
# ---------------------------------------------------------------------------
out_png = os.path.join(HERE, "RCS-MARK-CONSTRUCTION.png")
fig.savefig(out_png, dpi=200, facecolor=PAGE)
print("WROTE", out_png)


# ---------------------------------------------------------------------------
# Export the same R as a clean working SVG (favicon + header logo)
# Walk the path verts/codes and emit SVG path commands (y is flipped: SVG y-down).
# ---------------------------------------------------------------------------
def emit_svg(path: Path, height: float):
    out = []
    i = 0
    verts, codes = path.vertices, path.codes
    while i < len(verts):
        c = codes[i]
        x, y = verts[i]
        sy = height - y
        if c == Path.MOVETO:
            out.append(f"M{x:.4f} {sy:.4f}")
            i += 1
        elif c == Path.LINETO:
            out.append(f"L{x:.4f} {sy:.4f}")
            i += 1
        elif c == Path.CURVE4:
            x1, y1 = verts[i];     sy1 = height - y1
            x2, y2 = verts[i + 1]; sy2 = height - y2
            x3, y3 = verts[i + 2]; sy3 = height - y3
            out.append(f"C{x1:.4f} {sy1:.4f} {x2:.4f} {sy2:.4f} {x3:.4f} {sy3:.4f}")
            i += 3
        elif c == Path.CLOSEPOLY:
            out.append("Z")
            i += 1
        else:
            i += 1
    return " ".join(out)


# Build the canonical mark on a 0..9 x 0..12 unit grid
mark = build_R_path(stem_x=0, baseline=0, height=12,
                    stem_w=1.7, bowl_h=6.6, bowl_extent=7.4)
d = emit_svg(mark, height=12.0)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 14" role="img" aria-label="RCS mark">
  <title>RCS · Doppia Partita</title>
  <!-- the ledger fold — single carmine hairline, the brand's signature accent -->
  <line x1="6" y1="0.2" x2="6" y2="13.8" stroke="{CARMINE}" stroke-width="0.12" opacity="0.95"/>
  <!-- the principal R, sitting flush left within a 9u column -->
  <g transform="translate(1.5 1.0)">
    <path d="{d}" fill="{INK}" fill-rule="evenodd"/>
  </g>
</svg>
'''
out_svg = os.path.join(HERE, "rcs-mark.svg")
with open(out_svg, "w") as f:
    f.write(svg)
print("WROTE", out_svg)

# Tiny favicon variant — square 16x16 viewBox, no fold line
svg_fav = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" role="img" aria-label="RCS">
  <rect width="16" height="16" rx="2.4" fill="{INK}"/>
  <g transform="translate(3.2 2.3) scale(0.79)">
    <path d="{d}" fill="{PAGE}" fill-rule="evenodd"/>
  </g>
  <line x1="8" y1="2" x2="8" y2="14" stroke="{CARMINE}" stroke-width="0.18" opacity="0.85"/>
</svg>
'''
out_fav = os.path.join(HERE, "favicon.svg")
with open(out_fav, "w") as f:
    f.write(svg_fav)
print("WROTE", out_fav)

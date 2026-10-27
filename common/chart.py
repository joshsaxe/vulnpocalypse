"""The chart kit used by every chart script: Economist-style scaffolding for landscape charts.

Every chart is drawn on a 6.5-in-wide canvas and must come out wider than it is tall. Substack shows images at
728 px in its column, where 9-pt labels render at about 14 px, the 14-pt title at about 22 px and the source line at
about 11 px. Layout, top to bottom: a red tag with the chart number, a one-clause title that states the finding, a
subtitle saying what is plotted and in what units, the plot, then the note and the source line in small print.

Colours follow the entity, the same in every chart:
    FRAUD blue   HACK red (attackers)   AI amber   DEF green (defenders)   GOV purple   PRIV cyan   GREY neutral
Text never wears a data colour; a coloured mark sits beside ink text. Labels that may cross data get a white halo.
Model uncertainty has three looks only: a shaded band (time series), a light thick square-ended bar behind a dot
(dot plots) and a thin dark whisker (bar charts). Ranges reported in the data are hairlines with end ticks
(data_range). Hollow markers mean only 'projected' or 'so far'. Nothing inside a plot is set below MIN (8 pt).
"""
from __future__ import annotations

import textwrap

import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextToPath
from matplotlib import font_manager as _fm
from pathlib import Path

# Inter (SIL Open Font License) is bundled in figures/fonts, so the charts lay out the same on every machine.
_FONT_DIR = Path(__file__).resolve().parents[1] / "figures" / "fonts"
for _f in sorted(_FONT_DIR.glob("Inter-*.otf")):
    _fm.fontManager.addfont(str(_f))
# If another copy of Inter is installed on the system, make the bundled files win ties, so layouts are reproducible.
_fm.fontManager.ttflist.sort(key=lambda e: 0 if str(_FONT_DIR) in e.fname else 1)
try:
    _fm.fontManager._findfont_cached.cache_clear()
except AttributeError:      # a matplotlib without that cache: nothing to clear
    pass

FRAUD = "#006BA2"
HACK = "#DB444B"
AI = "#D08E00"
AI_LIGHT = "#F2D9A6"
DEF = "#00876C"
GOV = "#8A4FA8"
PRIV = "#0FA3C7"
GREY = "#758D99"
LIGHT = "#C9D3D9"
PALE = "#E6EBEE"
TAG_RED = "#E3120B"
INK = "#121212"
SECOND = "#4D5358"
MUTED = "#6B7378"
GRID = "#D3DADF"
AXIS = "#3A3F44"
BG = "#FFFFFF"

FONT = "Inter"
W_IN = 6.5
MAX_ASPECT = 0.80   # height / width; every chart must be clearly landscape
TICK = 9.0
LABEL = 9.0
SMALL = 8.0
TITLE = 14.0
SUB = 10.0
SRC = 7.2
MIN = 8.0

mpl.rcParams.update({
    "font.family": FONT,
    "font.size": LABEL,
    "text.color": INK,
    "axes.edgecolor": AXIS,
    "axes.labelcolor": SECOND,
    "axes.linewidth": 0.8,
    "axes.facecolor": BG,
    "figure.facecolor": BG,
    "xtick.color": SECOND,
    "ytick.color": SECOND,
    "xtick.labelsize": TICK,
    "ytick.labelsize": TICK,
    "xtick.major.size": 3,
    "xtick.major.width": 0.8,
    "ytick.major.size": 0,
    "legend.frameon": False,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "axes.unicode_minus": False,
    "text.hinting": "no_hinting",     # set explicitly: the layouts were drawn unhinted, whatever matplotlibrc says
    "svg.hashsalt": "vulnpocalypse",  # fixed, so the SVG files are byte-for-byte reproducible
})

HALO = [pe.withStroke(linewidth=2.6, foreground="white")]
_EM = 0.53


_TP = TextToPath()


def text_width_in(s: str, fontsize: float, bold: bool = False) -> float:
    """Measured width of a string in inches (escaped dollars count as one glyph)."""
    prop = FontProperties(family=FONT, size=fontsize, weight="bold" if bold else "normal")
    w, _, _ = _TP.get_text_width_height_descent(s.replace("\\$", "$"), prop, ismath=False)
    return w / 72


def wrap(text: str, width_in: float, fontsize: float, bold: bool = False) -> list[str]:
    """Greedy word wrap to a physical width (inches) at a font size (points), using measured glyph widths."""
    out: list[str] = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = word if not line else line + " " + word
            if line and text_width_in(trial, fontsize, bold) > width_in:
                out.append(line)
                line = word
            else:
                line = trial
        out.append(line)
    return out


def wrap_balanced(text: str, width_in: float, fontsize: float, bold: bool = False) -> list[str]:
    """Wrap into as few lines as greedy wrapping needs, but with lines of similar length (no one-word widows)."""
    lines = wrap(text, width_in, fontsize, bold)
    if len(lines) < 2:
        return lines
    lo, hi = 0.3 * width_in, width_in
    for _ in range(30):
        mid = (lo + hi) / 2
        if len(wrap(text, mid, fontsize, bold)) <= len(lines):
            hi = mid
        else:
            lo = mid
    return wrap(text, hi, fontsize, bold)


class Chart:
    """Header (tag + chart number, title, subtitle), a plot region and a footer (note, sources, author)."""

    def __init__(self, number: int, title: str, subtitle: str, source: str, *, plot_h_in: float = 3.0,
                 note: str | None = None, width_in: float = W_IN, footer_right: str = "",
                 tag: str | None = None):
        self.width_in = width_in
        side = 0.12
        text_w = width_in - 2 * side
        title_lines = wrap_balanced(title, text_w, TITLE, bold=True)
        sub_lines = wrap_balanced(subtitle, text_w, SUB) if subtitle else []
        note_lines = wrap(note, text_w, SRC) if note else []
        src_lines = wrap(source, text_w, SRC)
        credit_w = (text_width_in(footer_right, SRC, bold=True) + 0.15) if footer_right else 0.0
        if text_width_in(src_lines[-1], SRC) > text_w - credit_w:   # the credit sits at the right of the last line
            src_lines = src_lines[:-1] + wrap(src_lines[-1], text_w - credit_w, SRC)
        tag_h, t_lh, s_lh, f_lh = 0.25, 0.238, 0.176, 0.122
        header_h = tag_h + t_lh * len(title_lines) + s_lh * len(sub_lines) + 0.16
        footer_h = 0.16 + f_lh * (len(src_lines) + len(note_lines)) + (0.04 if note_lines else 0)
        self.H = header_h + plot_h_in + footer_h
        self.fig = plt.figure(figsize=(width_in, self.H), dpi=100)
        fig, H = self.fig, self.H
        fig.add_artist(Rectangle((side / width_in, 1 - 0.07 / H), 0.36 / width_in, 0.07 / H,
                                 transform=fig.transFigure, color=TAG_RED, lw=0))
        fig.text((side + 0.44) / width_in, 1 - 0.07 / H, tag if tag is not None else f"Chart {number}",
                 fontsize=8.0, color=SECOND, fontweight="bold", ha="left", va="center")
        y = 1 - tag_h / H
        for ln in title_lines:
            y -= t_lh / H
            fig.text(side / width_in, y + 0.045 / H, ln, fontsize=TITLE, fontweight="bold", color=INK, ha="left",
                     va="baseline")
        for ln in sub_lines:
            y -= s_lh / H
            fig.text(side / width_in, y + 0.035 / H, ln, fontsize=SUB, color=INK, ha="left", va="baseline")
        self.region = (side / width_in, footer_h / H, text_w / width_in, plot_h_in / H)
        yb = footer_h - 0.13
        for ln in note_lines:
            fig.text(side / width_in, yb / H, ln, fontsize=SRC, color=SECOND, ha="left", va="baseline")
            yb -= f_lh
        if note_lines:
            yb -= 0.04
        for ln in src_lines:
            fig.text(side / width_in, yb / H, ln, fontsize=SRC, color=SECOND, ha="left", va="baseline")
            yb -= f_lh
        if footer_right:
            fig.text(1 - side / width_in, (yb + f_lh) / H, footer_right, fontsize=SRC, color=SECOND, ha="right",
                     va="baseline", fontweight="bold")

    def axes(self, rect=(0.0, 0.0, 1.0, 1.0), **kw):
        L, B, W, Hh = self.region
        l, b, w, h = rect
        return self.fig.add_axes((L + l * W, B + b * Hh, w * W, h * Hh), **kw)

    def text(self, x, y, s, **kw):
        L, B, W, Hh = self.region
        return self.fig.text(L + x * W, B + y * Hh, s, **kw)

    def save(self, path_stem: str, dpi: int = 250):
        ratio = self.H / self.width_in
        print(f"{Path(path_stem).name}: {self.width_in:.2f} x {self.H:.2f} in, height/width {ratio:.2f}")
        if ratio > MAX_ASPECT:
            raise SystemExit(f"not landscape enough: height/width {ratio:.2f} > {MAX_ASPECT}")
        self.fig.savefig(path_stem + ".png", dpi=dpi, facecolor=BG)
        self.fig.savefig(path_stem + ".svg", facecolor=BG, metadata={"Date": None})   # no timestamp: reproducible bytes
        plt.close(self.fig)


def style_axis(ax, *, ygrid=True, xgrid=False, bottom_spine=True, yright=True):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_visible(bottom_spine)
    ax.spines["bottom"].set_color(AXIS)
    ax.spines["bottom"].set_linewidth(1.0)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, lw=0.7, zorder=0)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=2)
    if yright:
        ax.yaxis.tick_right()
    return ax


def labels_above_gridlines(ax, pad_pts: float = 1.5):
    """Economist look: y labels sit at the right edge, inside the plot, on top of their gridlines."""
    ax.tick_params(axis="y", pad=-pad_pts, labelright=True, labelleft=False, direction="in")
    for lab in ax.get_yticklabels():
        lab.set_verticalalignment("bottom")
        lab.set_horizontalalignment("right")
        lab.set_path_effects(HALO)


def hbar_axis(ax, xgrid=True):
    """For horizontal dot/bar charts: vertical hairlines, no box, category labels on the left."""
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0, pad=6)
    return ax


def key(ax, x, y, label, color, *, kind="line", transform=None, size=SMALL, lw=2.4, gap=0.014, ms=6.5,
        alpha=1.0, hollow=False, ec=None):
    """A legend entry where we want it: a short coloured line, patch or dot, then ink text."""
    tr = transform or ax.transAxes
    if kind == "line":
        ax.plot([x, x + 0.05], [y, y], color=color, lw=lw, transform=tr, solid_capstyle="butt", clip_on=False,
                alpha=alpha)
        tx = x + 0.05 + gap
    elif kind == "patch":
        ax.add_patch(Rectangle((x, y - 0.016), 0.034, 0.032, transform=tr, facecolor=color, lw=0.8 if ec else 0,
                               edgecolor=ec or color, clip_on=False, alpha=alpha))
        tx = x + 0.034 + gap
    else:
        ax.plot([x + 0.01], [y], "o", color=color, ms=ms, transform=tr, clip_on=False,
                mfc="white" if hollow else color, mec=color if hollow else "white", mew=1.6 if hollow else 1.0,
                alpha=alpha)
        tx = x + 0.022 + gap
    ax.text(tx, y, label, transform=tr, fontsize=size, color=INK, va="center", ha="left")


def data_range(ax, lo, hi, y, color, tick=0.13, vertical=False, lw=1.1, zorder=2):
    """A range reported in the data (not model uncertainty): a hairline with end ticks."""
    if vertical:
        ax.plot([y, y], [lo, hi], color=color, lw=lw, solid_capstyle="butt", zorder=zorder)
        for v in (lo, hi):
            ax.plot([y - tick, y + tick], [v, v], color=color, lw=lw, solid_capstyle="butt", zorder=zorder)
    else:
        ax.plot([lo, hi], [y, y], color=color, lw=lw, solid_capstyle="butt", zorder=zorder)
        for v in (lo, hi):
            ax.plot([v, v], [y - tick, y + tick], color=color, lw=lw, solid_capstyle="butt", zorder=zorder)


def model_bar(ax, lo, hi, y, color, lw=5.0, alpha=0.35, vertical=False, zorder=2):
    """A model interval behind a dot: a light, thick bar with square ends."""
    if vertical:
        ax.plot([y, y], [lo, hi], color=color, lw=lw, alpha=alpha, solid_capstyle="butt", zorder=zorder)
    else:
        ax.plot([lo, hi], [y, y], color=color, lw=lw, alpha=alpha, solid_capstyle="butt", zorder=zorder)


def halo_text(ax, x, y, s, **kw):
    kw.setdefault("path_effects", HALO)
    return ax.text(x, y, s, **kw)

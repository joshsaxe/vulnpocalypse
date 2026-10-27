"""Where things live. Every script finds the repository root from its own location, so nothing is hard-coded."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"            # the compiled tables (CSV) every model starts from
RESULTS = ROOT / "results"      # numbers and posterior draws the scripts write
FIGURES = ROOT / "figures"      # the charts (PNG and SVG) and the bundled font

RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


def dump_json(obj, path):
    """Write results the same way everywhere (indent 1, no trailing newline)."""
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)

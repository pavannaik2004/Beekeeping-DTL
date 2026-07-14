"""Engineering drawing sheets — one A3-style SVG per unique part with
front / side / top hidden-line orthographic views, overall dimensions and a
title block.

Run:  python -m hive_twin.drawings
"""

import re
import time
from datetime import date
from pathlib import Path

from build123d import Compound, ExportSVG, LineType

from . import assembly

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "exports" / "drawings"

SHEET_W, SHEET_H = 420.0, 297.0          # A3 landscape, mm
MARGIN = 12.0
VIEW_W, VIEW_H = 186.0, 118.0            # view cell size
DIST = 100000.0                           # far viewpoint ≈ orthographic

# (label, camera direction, up vector, which bbox axes the view spans)
VIEWS = [
    ("FRONT (X-Y)", (0, 0, DIST), (0, 1, 0), ("X", "Y")),
    ("SIDE (Z-Y)", (DIST, 0, 0), (0, 1, 0), ("Z", "Y")),
    ("TOP (X-Z)", (0, DIST, 0), (0, 0, -1), ("X", "Z")),
]

# duplicate parts share one sheet (quantity noted instead)
SKIP = {f"ff{i}_{h}" for i in range(1, 7) for h in ("fixed", "moving")}
QTY = {"ff0_fixed": 7, "ff0_moving": 7}


def _view_svg(part, origin, up) -> tuple[str, float, float]:
    """Project the part and return (inner svg markup, width mm, height mm)."""
    visible, hidden = part.project_to_viewport(
        viewport_origin=origin, viewport_up=up)
    exp = ExportSVG(scale=1.0, line_weight=0.35)
    exp.add_layer("visible")
    exp.add_layer("hidden", line_color=(120, 120, 120),
                  line_type=LineType.ISO_DASH, line_weight=0.2)
    # add edge-by-edge: degenerate projected arcs (start == end) crash the
    # exporter (svgpathtools assertion) — drop them, they are invisible anyway
    for edges, layer in ((visible, "visible"), (hidden, "hidden")):
        for e in edges or []:
            try:
                if e.length > 0.02:
                    exp.add_shape(e, layer=layer)
            except Exception:
                pass
    tmp = OUT / "_tmp_view.svg"
    exp.write(str(tmp))
    text = tmp.read_text()
    m = re.search(r'width="([\d.]+)mm".*?height="([\d.]+)mm"', text, re.S)
    w, h = float(m.group(1)), float(m.group(2))
    text = re.sub(r"^<\?xml[^>]*\?>\s*", "", text)
    # strip the original width/height so the outer placement attrs win
    text = re.sub(r'\s(?:width|height)="[\d.]+mm"', "", text, count=2)
    return text, w, h


def _dim(x0, y0, x1, y1, label, vertical=False) -> str:
    """A dimension line with arrowheads and centred text."""
    tx, ty = (x0 + x1) / 2, (y0 + y1) / 2
    if vertical:
        txt = (f'<text x="{tx + 4.5:.1f}" y="{ty:.1f}" font-size="4.2" '
               f'text-anchor="middle" transform="rotate(90 {tx + 4.5:.1f} {ty:.1f})">{label}</text>')
    else:
        txt = f'<text x="{tx:.1f}" y="{ty - 1.6:.1f}" font-size="4.2" text-anchor="middle">{label}</text>'
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
            f'stroke="#444" stroke-width="0.25" marker-start="url(#arr)" '
            f'marker-end="url(#arr)"/>{txt}')


def sheet(name: str, part, meta: dict, idx: int, total: int) -> None:
    group, mat = assembly.part_meta(name)
    mat_label = assembly.MATERIALS[mat][0]
    bb = part.bounding_box()
    dims = {"X": bb.size.X, "Y": bb.size.Y, "Z": bb.size.Z}

    # scale: all three views share the largest-fit scale for consistency
    needed = []
    for _, _, _, (ax, ay) in VIEWS:
        needed.append(min((VIEW_W - 30) / max(dims[ax], 1e-6),
                          (VIEW_H - 26) / max(dims[ay], 1e-6)))
    scale = min(needed + [2.0])

    cells = [(MARGIN, 14), (MARGIN + VIEW_W + 8, 14),
             (MARGIN, 14 + VIEW_H + 10)]
    body = []
    for (label, origin, up, (ax, ay)), (cx, cy) in zip(VIEWS, cells):
        inner, w, h = _view_svg(part, origin, up)
        vw, vh = w * scale, h * scale
        px = cx + (VIEW_W - vw) / 2
        py = cy + (VIEW_H - vh) / 2
        body.append(f'<rect x="{cx}" y="{cy}" width="{VIEW_W}" height="{VIEW_H}" '
                    f'fill="none" stroke="#bbb" stroke-width="0.2"/>')
        body.append(f'<text x="{cx + 3}" y="{cy + 6}" font-size="4.6" '
                    f'fill="#666">{label}</text>')
        body.append(f'<svg x="{px:.1f}" y="{py:.1f}" width="{vw:.1f}" '
                    f'height="{vh:.1f}" {inner[4:]}')  # reuse full svg tag body
        # overall dimensions under and beside the view
        body.append(_dim(px, py + vh + 6, px + vw, py + vh + 6,
                         f"{dims[ax]:.1f}"))
        body.append(_dim(px + vw + 6, py, px + vw + 6, py + vh,
                         f"{dims[ay]:.1f}", vertical=True))

    # title block
    tb_x, tb_y = MARGIN + VIEW_W + 8, 14 + VIEW_H + 10
    tb_w, tb_h = VIEW_W, VIEW_H
    rows = [
        ("PART", name.upper()),
        ("PROJECT", "BEEHIVE DIGITAL TWIN 1:1 (ISI + FLOW SUPER)"),
        ("MATERIAL", mat_label.upper()),
        ("QTY", str(QTY.get(name, 1))),
        ("BBOX (mm)", f"{dims['X']:.1f} x {dims['Y']:.1f} x {dims['Z']:.1f}"),
        ("SCALE", f"1:{1 / scale:.1f}" if scale < 1 else f"{scale:.1f}:1"),
        ("UNITS", "mm  |  FITS: SLIDE 0.4, STATIC 0.2"),
        ("SHEET", f"{idx} / {total}   {date.today().isoformat()}"),
    ]
    body.append(f'<rect x="{tb_x}" y="{tb_y}" width="{tb_w}" height="{tb_h}" '
                f'fill="none" stroke="#333" stroke-width="0.5"/>')
    rh = tb_h / len(rows)
    for i, (k, v) in enumerate(rows):
        y = tb_y + rh * i
        body.append(f'<line x1="{tb_x}" y1="{y:.1f}" x2="{tb_x + tb_w}" '
                    f'y2="{y:.1f}" stroke="#999" stroke-width="0.2"/>')
        body.append(f'<text x="{tb_x + 3}" y="{y + rh / 2 + 1.6:.1f}" '
                    f'font-size="3.6" fill="#777">{k}</text>')
        body.append(f'<text x="{tb_x + 34}" y="{y + rh / 2 + 1.6:.1f}" '
                    f'font-size="4.4" font-weight="bold">{v}</text>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}mm" height="{SHEET_H}mm"
 viewBox="0 0 {SHEET_W} {SHEET_H}" font-family="Arial, sans-serif" fill="#111">
<defs><marker id="arr" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5"
 markerHeight="5" orient="auto-start-reverse">
 <path d="M0,0 L6,3 L0,6 z" fill="#444"/></marker></defs>
<rect width="{SHEET_W}" height="{SHEET_H}" fill="white"/>
<rect x="4" y="4" width="{SHEET_W - 8}" height="{SHEET_H - 8}" fill="none"
 stroke="#333" stroke-width="0.6"/>
<text x="{MARGIN}" y="11" font-size="6" font-weight="bold">{name}</text>
<text x="{SHEET_W - MARGIN}" y="11" font-size="4.5" text-anchor="end"
 fill="#666">Beekeeping DTL - Digital Twin - third-angle projection</text>
{''.join(body)}
</svg>"""
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def run() -> None:
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    parts = assembly.build_parts()
    todo = [(n, p) for n, p in parts.items() if n not in SKIP]
    for i, (name, part) in enumerate(todo, 1):
        sheet(name, part, {}, i, len(todo))
        print(f"  [{i:2d}/{len(todo)}] {name}")
    tmp = OUT / "_tmp_view.svg"
    if tmp.exists():
        tmp.unlink()
    print(f"done in {time.time() - t0:.1f}s -> {OUT}")


if __name__ == "__main__":
    run()

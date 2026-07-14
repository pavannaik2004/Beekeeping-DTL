"""Bill of materials — exports/BOM.md and exports/BOM.csv.

Quantities/materials for building the hive for real, plus consumables the
CAD model represents implicitly (screws, sealant, paint).

Run:  python -m hive_twin.bom
"""

import csv
import time
from pathlib import Path

from . import assembly

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"

# extra rows that are not solids in the model
CONSUMABLES = [
    ("wood screws SS 4x40", 1, "Stainless steel", "box corners, cleats, rails", "~60 pcs"),
    ("silicone sealant (food grade)", 1, "Silicone", "window acrylic + shutter seal beads", "1 tube"),
    ("frame spacer blocks", 2, "Pine wood", "fill 57.5 mm gap each side of the 7 frames", "55 x 20 x 385"),
    ("exterior paint / linseed oil", 1, "-", "weather protection, outside faces only", "0.5 L"),
    ("union coupling 1/2 inch", 1, "Stainless steel", "manifold stub to tap pipe", "-"),
]


def rows() -> list[tuple]:
    parts = assembly.build_parts()
    seen: dict[str, list] = {}
    for name, solid in parts.items():
        # collapse the 7 identical frames into two rows
        key = ("ff_fixed" if name.startswith("ff") and name.endswith("_fixed")
               else "ff_moving" if name.startswith("ff") and name.endswith("_moving")
               else name)
        group, mat = assembly.part_meta(name)
        mat_label = assembly.MATERIALS[mat][0]
        bb = solid.bounding_box()
        stock = f"{bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f}"
        if key in seen:
            seen[key][1] += 1
        else:
            seen[key] = [key, 1, mat_label,
                         assembly.GROUPS[group][1], stock,
                         solid.volume / 1000.0]
    out = []
    for key, (n, qty, mat, grp, stock, vol) in seen.items():
        out.append((n, qty, mat, grp, stock, f"{vol:.0f}"))
    return out


def run() -> None:
    t0 = time.time()
    EXPORTS.mkdir(exist_ok=True)
    data = rows()

    with open(EXPORTS / "BOM.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["part", "qty", "material", "module", "bbox mm", "volume cm3"])
        w.writerows(data)
        w.writerow([])
        w.writerow(["consumable", "qty", "material", "used for", "size", ""])
        for c in CONSUMABLES:
            w.writerow([c[0], c[1], c[2], c[3], c[4], ""])

    lines = [
        "# Bill of Materials — Beehive Digital Twin (1:1, all mm)",
        "",
        f"Machined / printed parts: {sum(q for _, q, *_ in data)} "
        f"({len(data)} unique). Generated from `hive_twin` parametric model.",
        "",
        "| Part | Qty | Material | Module | Bounding box (mm) | Volume (cm³) |",
        "|---|---|---|---|---|---|",
    ]
    for n, qty, mat, grp, stock, vol in data:
        lines.append(f"| {n} | {qty} | {mat} | {grp} | {stock} | {vol} |")
    lines += [
        "",
        "## Consumables / hardware",
        "",
        "| Item | Qty | Material | Used for | Size |",
        "|---|---|---|---|---|",
    ]
    for c in CONSUMABLES:
        lines.append(f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]} |")
    (EXPORTS / "BOM.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"BOM.md + BOM.csv written in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    run()

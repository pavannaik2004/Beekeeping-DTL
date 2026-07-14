# 06 — Digital Twin (1:1 Parametric CAD Model)

A precise, manufacturable **1:1 digital twin** of the upgraded beehive shown in
the Three.js visualiser on the `gh-pages` branch. Every dimension comes from
that model's "ISI STANDARD DIMENSIONS" block; on top of it this twin adds the
engineering layer that makes the design physically buildable: rabbet joinery,
fit tolerances, a real slotted queen excluder, and a working flow-frame cam
mechanism.

Built with [build123d](https://build123d.readthedocs.io/) (Python + the
OpenCascade BREP kernel — the same math commercial CAD uses).

## Quick start

```bash
cd 06-digital-twin
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # (Linux/mac: .venv/bin/pip)

.venv/Scripts/python -m hive_twin.checks     # engineering verification
.venv/Scripts/python -m hive_twin.export     # STEP + STL + GLB + manifest
.venv/Scripts/python -m hive_twin.drawings   # dimensioned SVG sheets
.venv/Scripts/python -m hive_twin.bom        # BOM.md / BOM.csv

python -m http.server 8000                   # then open
# http://localhost:8000/viewer/              # interactive 3D viewer
```

## Deliverables

| Where | What |
|---|---|
| `exports/step/` | Per-part STEP + `beehive_assembly.step` (FreeCAD/Fusion/SolidWorks) |
| `exports/stl/` | Per-part STL, all watertight and 3D-printable |
| `exports/glb/hive.glb` | Merged model with named parts + materials (for the viewer) |
| `exports/drawings/` | A3 drawing sheet per unique part: front/side/top hidden-line views, overall dims, title block |
| `exports/BOM.md` / `.csv` | Bill of materials incl. consumables |
| `viewer/index.html` | Interactive digital twin: slide both shutters, turn the flow key, exploded view, per-module toggles, hover part info. Pose via URL too, e.g. `?ex=1&sl=150&hv=1` |
| `screenshots/` | Rendered verification shots (closed pose, exploded harvest pose) |

## Structure

- `hive_twin/params.py` — **single source of truth**: every dimension (mm),
  tolerance and stack height. Change a value, re-run export: the whole model,
  drawings and BOM update.
- `hive_twin/parts/*.py` — one module per component (49 solids total).
- `hive_twin/assembly.py` — part registry, materials, viewer actions.
- `hive_twin/checks.py` — verification: Y-stack, fits, and boolean
  interference checks across 34 mating part pairs.

## The engineering layer (what makes it "work")

- **Coordinates**: X width, Y height (up), Z depth (front +Z) — identical to
  the Three.js scene. Units mm.
- **Tolerances**: sliding fits 0.4 mm total (shutters, flow key), static fits
  0.2 mm (acrylic panes, box tongues), telescoping roof 2 mm/side.
- **Joinery**: boxes are four interlocking boards with 10×10 mm rabbets —
  printable or cuttable, self-squaring.
- **Bee space** (9 mm) respected at the frame rests and top-bar gap.
- **Queen excluder**: 4.2 mm slots between 2 mm bars — workers pass, the
  queen cannot (real apiary spec).
- **Flow-frame cam**: the key blade is 3.2 mm lying flat and 13.2 mm upright;
  turning it 90° inside the frame lifts the moving cell-columns exactly
  (13.2 − 3.2)/2 = **5.0 mm**, opening the cells so honey drains:
  columns → frame trough → front spout → external manifold → tap → hose → jar.
- **Windows**: 5 mm acrylic in a rebated MDF ring; 3 mm shutter riding in
  3.4 mm grooves with 150 mm travel and a stop pin.

## Documented deviations from the Three.js visualiser

The visualiser is a *visual* model; three of its choices are physically
impossible and were engineered around (everything else matches 1:1):

1. **Manifold** — shown *inside* the super, 6 mm below its floor (where the
   queen excluder is). The twin mounts it externally on the front wall, fed
   by a Ø7 spout from each frame.
2. **Tap/hose/jar at Z = 277.5** — would pass through the landing board.
   Moved to Z = 300 (75 mm → 97.5 mm in front of the box).
3. **Telescoping roof** — drawn floating above the cover. The twin's roof
   board rests on the inner cover with the rim skirting 10 mm down around
   the super (that is what "telescoping" means).

If 3D-printing at 1:1 note the biggest boards exceed a 250 mm bed and must be
sectioned (or print at reduced scale: every STL is watertight so slicers can
scale freely). For a real hive, build the wooden parts from the drawings and
print only the flow frames, excluder, feeder and plumbing.

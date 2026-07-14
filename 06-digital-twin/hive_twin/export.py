"""Export the digital twin: STEP + STL per part, assembly STEP, merged GLB
with named nodes for the web viewer, and the viewer manifest.

Run:  python -m hive_twin.export
"""

import json
import time
from pathlib import Path

import numpy as np
import trimesh
from build123d import export_step, export_stl

from . import assembly, params as P

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"


def _hex_to_rgba(color: str, opacity: float) -> list[int]:
    c = color.lstrip("#")
    return [int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16),
            int(round(opacity * 255))]


def export_all() -> None:
    t0 = time.time()
    step_dir = EXPORTS / "step"
    stl_dir = EXPORTS / "stl"
    glb_dir = EXPORTS / "glb"
    for d in (step_dir, stl_dir, glb_dir):
        d.mkdir(parents=True, exist_ok=True)

    parts = assembly.build_parts()
    print(f"built {len(parts)} parts in {time.time() - t0:.1f}s")

    # ---------------- per-part STEP + STL
    bad = []
    for name, solid in parts.items():
        export_step(solid, str(step_dir / f"{name}.step"))
        export_stl(solid, str(stl_dir / f"{name}.stl"),
                   tolerance=0.05, angular_tolerance=0.2)
        m = trimesh.load(stl_dir / f"{name}.stl")
        ok = m.is_watertight
        if not ok:
            bad.append(name)
        print(f"  {name:22s} STEP+STL  watertight={ok}")

    # ---------------- assembly STEP
    asm = assembly.build_assembly(parts)
    export_step(asm, str(step_dir / "beehive_assembly.step"))
    print("assembly STEP written")

    # ---------------- merged GLB with named nodes + materials
    scene = trimesh.Scene()
    for name in parts:
        m = trimesh.load(stl_dir / f"{name}.stl")
        group, mat = assembly.part_meta(name)
        label, color, opacity = assembly.MATERIALS[mat]
        rgba = _hex_to_rgba(color, opacity)
        m.visual = trimesh.visual.TextureVisuals(
            material=trimesh.visual.material.PBRMaterial(
                name=mat,
                baseColorFactor=[v / 255 for v in rgba],
                metallicFactor=0.1 if mat not in ("steel", "tin", "red") else 0.7,
                roughnessFactor=0.75,
                alphaMode="BLEND" if opacity < 1.0 else "OPAQUE",
            ))
        scene.add_geometry(m, node_name=name, geom_name=name)
    scene.export(glb_dir / "hive.glb")
    print(f"GLB written ({(glb_dir / 'hive.glb').stat().st_size / 1e6:.1f} MB)")

    # ---------------- viewer manifest
    manifest = {
        "title": "Beehive Digital Twin — 1:1 (all dimensions mm)",
        "units": "mm",
        "parts": [
            {
                "name": name,
                "group": assembly.part_meta(name)[0],
                "group_label": assembly.GROUPS[assembly.part_meta(name)[0]][1],
                "material": assembly.MATERIALS[assembly.part_meta(name)[1]][0],
                "color": assembly.MATERIALS[assembly.part_meta(name)[1]][1],
                "opacity": assembly.MATERIALS[assembly.part_meta(name)[1]][2],
                "explode_y": assembly.GROUPS[assembly.part_meta(name)[0]][0],
            }
            for name in parts
        ],
        "actions": assembly.ACTIONS,
    }
    (glb_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("manifest written")

    if bad:
        raise SystemExit(f"NON-WATERTIGHT parts: {bad}")
    print(f"done in {time.time() - t0:.1f}s — all {len(parts)} parts watertight")


if __name__ == "__main__":
    export_all()

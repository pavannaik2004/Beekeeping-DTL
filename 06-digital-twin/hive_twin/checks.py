"""Engineering verification: stack heights, fit clearances and interference
checks between mating parts (boolean intersection volume must be ~0).

Run:  python -m hive_twin.checks
"""

import math
import time

from . import assembly, params as P


# pairs that mate/slide/touch -- intersection volume must be < TOL mm^3
INTERFERENCE_PAIRS = [
    ("brood_wall_left", "shutter_left"),
    ("brood_wall_left", "window_frame_left"),
    ("brood_wall_left", "acrylic_left"),
    ("brood_wall_left", "stop_pin_left"),
    ("brood_wall_back", "shutter_back"),
    ("brood_wall_back", "window_frame_back"),
    ("brood_wall_back", "stop_pin_back"),
    ("window_frame_left", "acrylic_left"),
    ("acrylic_left", "shutter_left"),
    ("insulation_left", "brood_wall_left"),
    ("insulation_left", "window_frame_left"),
    ("ff0_fixed", "ff0_moving"),
    ("ff3_fixed", "ff3_moving"),
    ("ff3_fixed", "flow_key"),
    ("ff3_moving", "flow_key"),
    ("super_wall_front", "flow_key"),
    ("super_wall_front", "ff0_fixed"),
    ("super_wall_front", "ff3_fixed"),
    ("super_wall_front", "manifold"),
    ("ff0_fixed", "manifold"),
    ("ff0_fixed", "ff1_fixed"),
    ("ff0_moving", "ff1_fixed"),
    ("manifold", "harvest_tap"),
    ("roof_body", "super_wall_front"),
    ("roof_body", "super_wall_left"),
    ("roof_body", "inner_cover"),
    ("inner_cover", "ff0_fixed"),
    ("queen_excluder", "brood_wall_front"),
    ("queen_excluder", "super_wall_front"),
    ("feeder_funnel", "super_wall_right"),
    ("feeder_tray", "super_wall_right"),
    ("feeder_funnel", "roof_tin"),
    ("harvest_hose", "floor_board"),
    ("collection_jar", "stand_platform"),
]

TOL = 0.5  # mm^3 -- boolean noise threshold


def run() -> None:
    t0 = time.time()
    parts = assembly.build_parts()
    print(f"built {len(parts)} parts in {time.time() - t0:.1f}s\n")
    failures: list[str] = []

    # ---------------- stack heights
    print("-- Y-stack --")
    for label, expect in [
        ("Y_FLOOR", 230), ("Y_BROOD", 250), ("Y_QE", 495),
        ("Y_SUPER", 498), ("Y_COVER", 648), ("Y_ROOF", 658),
    ]:
        got = getattr(P, label)
        ok = math.isclose(got, expect)
        print(f"  {label:8s} = {got:6.1f}  (expect {expect})  {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(label)

    # ---------------- derived fits
    print("\n-- fits --")
    fits = [
        ("shutter side clearance", (3.4 - P.SHUTTER_T) / 2, 0.2),
        ("roof telescoping clearance/side",
         (P.ROOF_W - 2 * ((P.ROOF_W - P.SUPER_W - 2 * P.ROOF_CLEAR) / 2)
          - P.SUPER_W) / 2, 2.0),
        ("key cam lift", (P.KEY_BLADE_H - P.KEY_BLADE_W) / 2, P.FF_SPLIT_SHIFT),
        ("key rotation envelope < wall bearing",
         P.KEY_HOLE_R_WALL - math.hypot(P.KEY_BLADE_H / 2, P.KEY_BLADE_W / 2),
         None),
        ("frame bar gap", P.FF_PITCH - (P.FF_PITCH - 0.2), 0.2),
    ]
    for label, got, expect in fits:
        if expect is None:
            ok = got > 0
            print(f"  {label:38s} = {got:5.2f}  (must be > 0)  {'OK' if ok else 'FAIL'}")
        else:
            ok = math.isclose(got, expect, abs_tol=1e-6)
            print(f"  {label:38s} = {got:5.2f}  (expect {expect})  {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(label)

    # ---------------- assembly bounding box
    print("\n-- overall --")
    asm = assembly.build_assembly(parts)
    bb = asm.bounding_box()
    print(f"  bbox {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm "
          f"(X: width, Y: height, Z: depth)")

    # ---------------- interference
    print("\n-- interference (intersection volume, mm^3) --")
    for a, b in INTERFERENCE_PAIRS:
        inter = parts[a].intersect(parts[b])
        if inter is None:
            v = 0.0
        elif hasattr(inter, "volume"):
            v = inter.volume
        else:  # ShapeList of intersection fragments
            v = sum(getattr(s, "volume", 0.0) for s in inter)
        ok = v < TOL
        print(f"  {a:20s} x {b:20s} = {v:10.4f}  {'OK' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"{a}^{b}")

    print(f"\n{time.time() - t0:.1f}s total")
    if failures:
        raise SystemExit(f"FAILURES: {failures}")
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    run()

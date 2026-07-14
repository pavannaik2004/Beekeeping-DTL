"""Assembly — collects every part (already modelled in world coordinates),
attaches metadata (group, material, colour, explode offset) and the
articulation actions used by the export manifest and the web viewer.
"""

from build123d import Compound, Part

from .parts import (
    stand, floor_board, brood_box, insulation, windows, queen_excluder,
    super_box, flow_frame, flow_key, feeder, inner_cover, roof, plumbing,
)
from . import params as P

# group -> (explode Y offset, display label)
GROUPS = {
    "stand":     (0,   "Stand + water ring"),
    "floor":     (40,  "Floor board"),
    "brood":     (80,  "Brood box"),
    "insulation": (80, "Insulation (XPS)"),
    "windows":   (80,  "Inspection windows"),
    "excluder":  (130, "Queen excluder"),
    "super":     (180, "Flow super"),
    "frames":    (180, "Flow frames"),
    "feeder":    (180, "Top feeder"),
    "plumbing":  (180, "Harvest plumbing"),
    "ground":    (0,   "Hose + jar"),
    "cover":     (240, "Inner cover"),
    "roof":      (300, "Telescoping roof"),
}

# material name, css colour, opacity
MATERIALS = {
    "pine":     ("Pine wood 20 mm",        "#c89b5f", 1.0),
    "pine_drk": ("Pine wood (roof/floor)", "#a87b4a", 1.0),
    "mdf":      ("MDF",                    "#8a6b46", 1.0),
    "ply":      ("Plywood shutter 3 mm",   "#6b4a2b", 1.0),
    "acrylic":  ("Clear acrylic 5 mm",     "#9fd8ff", 0.35),
    "xps":      ("XPS foam 10 mm",         "#f2b8c6", 1.0),
    "pp_food":  ("Food-grade PP",          "#f5e6c8", 1.0),
    "pp_move":  ("Food-grade PP (moving)", "#e0c896", 1.0),
    "steel":    ("Stainless steel",        "#9aa2a9", 1.0),
    "tin":      ("Galvanised tin 2 mm",    "#b9c0c7", 1.0),
    "plastic":  ("HDPE / plastic",         "#e8e8e8", 1.0),
    "silicone": ("Food-grade silicone",    "#f0f0f0", 0.7),
    "glass":    ("Glass",                  "#cfe8f0", 0.4),
    "concrete": ("Concrete / dense wood",  "#7d8288", 1.0),
    "red":      ("Painted steel (key)",    "#cc4444", 1.0),
    "blue":     ("HDPE (water ring)",      "#4aa3df", 1.0),
}

# part-name (or prefix, for ff*) -> (group, material)
PART_META = {
    "stand_foot": ("stand", "concrete"),
    "stand_pole": ("stand", "pine_drk"),
    "stand_platform": ("stand", "pine_drk"),
    "water_ring": ("stand", "blue"),
    "floor_board": ("floor", "pine_drk"),
    "brood_wall_front": ("brood", "pine"),
    "brood_wall_back": ("brood", "pine"),
    "brood_wall_left": ("brood", "pine"),
    "brood_wall_right": ("brood", "pine"),
    "insulation_left": ("insulation", "xps"),
    "insulation_right": ("insulation", "xps"),
    "insulation_back": ("insulation", "xps"),
    "window_frame_left": ("windows", "mdf"),
    "acrylic_left": ("windows", "acrylic"),
    "shutter_left": ("windows", "ply"),
    "stop_pin_left": ("windows", "steel"),
    "window_frame_back": ("windows", "mdf"),
    "acrylic_back": ("windows", "acrylic"),
    "shutter_back": ("windows", "ply"),
    "stop_pin_back": ("windows", "steel"),
    "queen_excluder": ("excluder", "steel"),
    "super_wall_front": ("super", "pine"),
    "super_wall_back": ("super", "pine"),
    "super_wall_left": ("super", "pine"),
    "super_wall_right": ("super", "pine"),
    "flow_key": ("frames", "red"),
    "feeder_funnel": ("feeder", "plastic"),
    "feeder_tray": ("feeder", "plastic"),
    "inner_cover": ("cover", "pine"),
    "roof_body": ("roof", "pine_drk"),
    "roof_tin": ("roof", "tin"),
    "manifold": ("plumbing", "steel"),
    "harvest_tap": ("plumbing", "steel"),
    "harvest_hose": ("ground", "silicone"),
    "collection_jar": ("ground", "glass"),
}


def part_meta(name: str) -> tuple[str, str]:
    if name in PART_META:
        return PART_META[name]
    if name.startswith("ff") and name.endswith("_fixed"):
        return ("frames", "pp_food")
    if name.startswith("ff") and name.endswith("_moving"):
        return ("frames", "pp_move")
    raise KeyError(name)


# Articulation actions consumed by the web viewer (axes in three.js space).
ACTIONS = [
    {
        "id": "shutter_left",
        "label": "Left shutter",
        "type": "translate",
        "nodes": ["shutter_left"],
        "axis": [0, 0, 1],
        "range": [0, P.SHUTTER_TRAVEL],
    },
    {
        "id": "shutter_back",
        "label": "Back shutter",
        "type": "translate",
        "nodes": ["shutter_back"],
        "axis": [-1, 0, 0],
        "range": [0, P.SHUTTER_TRAVEL],
    },
    {
        "id": "harvest",
        "label": "Flow key (harvest)",
        "type": "harvest",  # coupled: key rotates 90°, moving halves lift 5
        "key_node": "flow_key",
        "key_axis_point": [0, P.Y_SUPER + P.KEY_AXIS_Y_OFF, 0],
        "key_axis": [0, 0, 1],
        "key_angle_deg": 90,
        "lift_nodes": [f"ff{i}_moving" for i in range(P.NUM_FF)],
        "lift": P.FF_SPLIT_SHIFT,
        "range": [0, 1],
    },
    {
        "id": "explode",
        "label": "Exploded view",
        "type": "explode",
        "range": [0, 1],
    },
]


def build_parts() -> dict[str, Part]:
    """Every part of the hive, keyed by name, in world coordinates."""
    parts: dict[str, Part] = {}
    for mod in (stand, floor_board, brood_box, insulation, windows,
                queen_excluder, super_box, flow_frame, flow_key, feeder,
                inner_cover, roof, plumbing):
        for name, solid in mod.build().items():
            assert name not in parts, f"duplicate part name {name}"
            parts[name] = solid
    return parts


def build_assembly(parts: dict[str, Part] | None = None) -> Compound:
    """Labelled Compound of the whole hive (closed pose) for STEP export."""
    parts = parts or build_parts()
    children = []
    for name, solid in parts.items():
        solid.label = name
        children.append(solid)
    asm = Compound(label="beehive_digital_twin", children=children)
    return asm

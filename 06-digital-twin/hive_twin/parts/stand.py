"""Stand — single centre pole with ground foot, top platform and the
donut water ring that doubles as an ant barrier and bee waterer.

Parts returned (world coordinates):
    stand_foot      cast-concrete / heavy timber ground foot
    stand_pole      centre pole (tapered, like the Three.js model)
    stand_platform  plate the floor board rests on
    water_ring      trough that clamps around the pole (ants can't cross water)
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_y, cone_y, torus_y


def build() -> dict[str, Part]:
    parts: dict[str, Part] = {}

    # Ground foot — truncated cone, wide base for stability
    parts["stand_foot"] = cone_y(
        P.STAND_FOOT_R_BOT, P.STAND_FOOT_R_TOP, P.STAND_FOOT_H, 0, 0, 0
    )

    # Centre pole — slight taper (bottom +3 mm) exactly like the visualiser
    pole_h = P.STAND_H - P.STAND_PLAT_T - 12
    parts["stand_pole"] = cone_y(P.STAND_POLE_R + 3, P.STAND_POLE_R, pole_h, 0, 12, 0)

    # Platform plate the floor board sits on
    parts["stand_platform"] = box(
        P.FLOOR_W + 2 * P.STAND_PLAT_OH,
        P.STAND_PLAT_T,
        P.FLOOR_D + 2 * P.STAND_PLAT_OH,
        0,
        P.STAND_H - P.STAND_PLAT_T / 2,
        0,
    )

    # Water ring: sleeve that hugs the pole + annular floor + torus rim,
    # forming a real trough an ant cannot walk around.
    ring_y = 150.0
    sleeve = cyl_y(P.STAND_POLE_R + 4.0, 30, 0, ring_y - 5, 0) - cyl_y(
        P.STAND_POLE_R + 0.5, 32, 0, ring_y - 5, 0
    )
    floor_plate = cyl_y(
        P.WATER_RING_R + P.WATER_RING_TUBE, 6, 0, ring_y - 17, 0
    ) - cyl_y(P.STAND_POLE_R + 0.5, 8, 0, ring_y - 17, 0)
    rim = torus_y(P.WATER_RING_R, P.WATER_RING_TUBE, 0, ring_y - 10, 0)
    parts["water_ring"] = sleeve + floor_plate + rim

    return parts

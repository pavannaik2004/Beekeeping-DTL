"""Inspection windows: LEFT wall (200 x 140) and BACK wall (180 x 120).

Construction per window (identical scheme, different orientation):
  * a through-opening in the wall, aperture + 12 mm recess all round
  * an MDF recess ring glued into the opening; its outer face carries a
    5.2 mm deep rebate that seats the 5 mm acrylic pane (0.2 mm static fit)
  * two grooved rails screwed to the OUTER wall face, above and below the
    opening; a 3 mm shutter panel slides in the 3.4 mm grooves
    (0.2 mm clearance each side) with 150 mm of travel
  * a 3 mm stop pin through the top rail arrests the shutter at full open

This module provides:
  cut_left_wall(wall) / cut_back_wall(wall)  — machine the brood-box walls
  build()                                     — the loose parts (rings,
                                                acrylic, shutters, pins)
plus the opening geometry constants used by insulation.py.
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_y

# ------------------------------------------------------------------ geometry
# LEFT window — outer wall face at x = -BROOD_W/2; shutter slides along +Z.
LWIN_CY = P.Y_BROOD + P.WIN_FROM_BOTTOM + P.WIN_H / 2          # 375
LWIN_CZ = -70.0            # opening shifted rearward so the shutter can open
LOPEN_H = P.WIN_H + 2 * P.RECESS_D                             # 164
LOPEN_W = P.WIN_W + 2 * P.RECESS_D                             # 224 (along Z)
LFACE_X = -P.BROOD_W / 2                                       # -252.5

# BACK window — outer wall face at z = -BROOD_D/2; shutter slides along -X.
BWIN_CX = P.BWIN_OFFSET_X                                      # +80
BWIN_CY = P.Y_BROOD + P.BWIN_FROM_BOTTOM + P.BWIN_H / 2        # 375
BOPEN_H = P.BWIN_H + 2 * P.RECESS_D                            # 144
BOPEN_W = P.BWIN_W + 2 * P.RECESS_D                            # 204 (along X)
BFACE_Z = -P.BROOD_D / 2                                       # -202.5

RAIL_SECT = 15.0           # rail projection off the wall face
RAIL_H = 12.0              # rail height (across the slide direction)
GROOVE_D = 6.0             # groove depth into the rail
GROOVE_OFF = 1.5           # groove offset from the wall face
# groove width = shutter + total slide fit (0.2 mm per side)
GROOVE_W = P.SHUTTER_T + P.FIT_SLIDE                           # 3.4

# rails: opening + overhang each side + travel on the opening side
LRAIL_LEN = LOPEN_W + 2 * P.CHANNEL_OVERHANG + P.SHUTTER_TRAVEL  # 394
LRAIL_CZ = LWIN_CZ + (P.SHUTTER_TRAVEL) / 2                      # +5
BRAIL_LEN = BOPEN_W + 2 * P.CHANNEL_OVERHANG + P.SHUTTER_TRAVEL  # 374
BRAIL_CX = BWIN_CX - (P.SHUTTER_TRAVEL) / 2                      # +5

# shutters: cover opening + 5 mm overlap, ride 5 mm deep in each groove
LSHUT_W = LOPEN_W + 10.0                                       # 234 (along Z)
LSHUT_H = LOPEN_H + 10.0                                       # 174
BSHUT_W = BOPEN_W + 10.0                                       # 214 (along X)
BSHUT_H = BOPEN_H + 10.0                                       # 154
# shutters ride centred in the grooves (0.2 mm clearance each side)
SHUT_X = LFACE_X - GROOVE_OFF - GROOVE_W / 2                   # -255.7
BSHUT_Z = BFACE_Z - GROOVE_OFF - GROOVE_W / 2                  # -205.7


def _left_rails(wall: Part) -> Part:
    """Add the two grooved rails (fused: they are screwed on) + pin hole."""
    rail_x = LFACE_X - RAIL_SECT / 2
    for y0, groove_up in ((LWIN_CY - LOPEN_H / 2 - RAIL_H, True),
                          (LWIN_CY + LOPEN_H / 2, False)):
        rail = box(RAIL_SECT, RAIL_H, LRAIL_LEN, rail_x, y0 + RAIL_H / 2, LRAIL_CZ)
        gy = y0 + RAIL_H - GROOVE_D / 2 if groove_up else y0 + GROOVE_D / 2
        rail -= box(GROOVE_W, GROOVE_D + 0.1, LRAIL_LEN + 2,
                    LFACE_X - GROOVE_OFF - GROOVE_W / 2, gy, LRAIL_CZ)
        wall += rail
    # stop-pin hole through the top rail near the front end
    wall -= cyl_y(P.STOP_PIN_R + 0.05, RAIL_H + 4, SHUT_X,
                  LWIN_CY + LOPEN_H / 2 + RAIL_H / 2, LRAIL_CZ + LRAIL_LEN / 2 - 3)
    return wall


def _back_rails(wall: Part) -> Part:
    rail_z = BFACE_Z - RAIL_SECT / 2
    for y0, groove_up in ((BWIN_CY - BOPEN_H / 2 - RAIL_H, True),
                          (BWIN_CY + BOPEN_H / 2, False)):
        rail = box(BRAIL_LEN, RAIL_H, RAIL_SECT, BRAIL_CX, y0 + RAIL_H / 2, rail_z)
        gy = y0 + RAIL_H - GROOVE_D / 2 if groove_up else y0 + GROOVE_D / 2
        rail -= box(BRAIL_LEN + 2, GROOVE_D + 0.1, GROOVE_W,
                    BRAIL_CX, gy, BFACE_Z - GROOVE_OFF - GROOVE_W / 2)
        wall += rail
    # stop-pin hole through the top rail near the far (left) end
    wall -= cyl_y(P.STOP_PIN_R + 0.05, RAIL_H + 4,
                  BRAIL_CX - BRAIL_LEN / 2 + 3,
                  BWIN_CY + BOPEN_H / 2 + RAIL_H / 2, BSHUT_Z)
    return wall


def cut_left_wall(wall: Part) -> Part:
    """Machine the brood-box LEFT wall: opening + rails + pin hole."""
    wall -= box(P.WALL + 2, LOPEN_H, LOPEN_W, LFACE_X + P.WALL / 2, LWIN_CY, LWIN_CZ)
    return _left_rails(wall)


def cut_back_wall(wall: Part) -> Part:
    """Machine the brood-box BACK wall: opening + rails + pin hole."""
    wall -= box(BOPEN_W, BOPEN_H, P.WALL + 2, BWIN_CX, BWIN_CY, BFACE_Z + P.WALL / 2)
    return _back_rails(wall)


def build() -> dict[str, Part]:
    parts: dict[str, Part] = {}
    fit = P.FIT_STATIC

    # ---------------- LEFT window loose parts
    # MDF recess ring: fits the opening, rebated on the outer face for acrylic
    ring = box(P.WALL, LOPEN_H - fit, LOPEN_W - fit,
               LFACE_X + P.WALL / 2, LWIN_CY, LWIN_CZ)
    ring -= box(P.WALL + 2, P.WIN_H, P.WIN_W,
                LFACE_X + P.WALL / 2, LWIN_CY, LWIN_CZ)          # aperture
    ring -= box(P.ACRYLIC_T + 0.2, P.WIN_H + 10, P.WIN_W + 10,
                LFACE_X + (P.ACRYLIC_T + 0.2) / 2, LWIN_CY, LWIN_CZ)  # rebate
    parts["window_frame_left"] = ring

    parts["acrylic_left"] = box(
        P.ACRYLIC_T, P.WIN_H + 10 - fit, P.WIN_W + 10 - fit,
        LFACE_X + P.ACRYLIC_T / 2, LWIN_CY, LWIN_CZ)

    parts["shutter_left"] = box(P.SHUTTER_T, LSHUT_H, LSHUT_W,
                                SHUT_X, LWIN_CY, LWIN_CZ)

    parts["stop_pin_left"] = cyl_y(
        P.STOP_PIN_R, 25, SHUT_X,
        LWIN_CY + LOPEN_H / 2 + RAIL_H / 2 + 2, LRAIL_CZ + LRAIL_LEN / 2 - 3)

    # ---------------- BACK window loose parts
    ring = box(BOPEN_W - fit, BOPEN_H - fit, P.WALL,
               BWIN_CX, BWIN_CY, BFACE_Z + P.WALL / 2)
    ring -= box(P.BWIN_W, P.BWIN_H, P.WALL + 2,
                BWIN_CX, BWIN_CY, BFACE_Z + P.WALL / 2)
    ring -= box(P.BWIN_W + 10, P.BWIN_H + 10, P.ACRYLIC_T + 0.2,
                BWIN_CX, BWIN_CY, BFACE_Z + (P.ACRYLIC_T + 0.2) / 2)
    parts["window_frame_back"] = ring

    parts["acrylic_back"] = box(
        P.BWIN_W + 10 - fit, P.BWIN_H + 10 - fit, P.ACRYLIC_T,
        BWIN_CX, BWIN_CY, BFACE_Z + P.ACRYLIC_T / 2)

    parts["shutter_back"] = box(BSHUT_W, BSHUT_H, P.SHUTTER_T,
                                BWIN_CX, BWIN_CY, BSHUT_Z)

    parts["stop_pin_back"] = cyl_y(
        P.STOP_PIN_R, 25, BRAIL_CX - BRAIL_LEN / 2 + 3,
        BWIN_CY + BOPEN_H / 2 + RAIL_H / 2 + 2, BSHUT_Z)

    return parts

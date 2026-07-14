"""Brood box — 505 x 405 x 245, four rabbeted walls (separate boards).

  * front wall: 365 x 10 entrance slot at the bottom + lifting cleat
  * left wall: inspection window opening + grooved shutter rails
  * back wall: inspection window opening + grooved shutter rails + cleat
  * kept empty inside (no brood frames), as in the visualiser
"""

from build123d import Part

from .. import params as P
from ..helpers import box
from . import windows
from .joinery import rabbeted_walls

HANDLE_W = 80.0   # lifting cleat, fused to the wall (glued + screwed IRL)
HANDLE_H = 25.0
HANDLE_D = 15.0


def _cleat(wall: Part, y: float, z_face: float, sgn: int) -> Part:
    """Fuse a lifting cleat onto a front/back wall outer face."""
    return wall + box(HANDLE_W, HANDLE_H, HANDLE_D,
                      0, y, sgn * (z_face + HANDLE_D / 2))


def build() -> dict[str, Part]:
    walls = rabbeted_walls(P.BROOD_W, P.BROOD_D, P.BROOD_H, P.Y_BROOD)

    # ---- front: entrance slot low in the wall
    front = walls["front"]
    front -= box(P.ENTRANCE_W, P.ENTRANCE_H, P.WALL + 2,
                 0, P.Y_BROOD + P.ENTRANCE_H / 2, (P.BROOD_D - P.WALL) / 2)
    front = _cleat(front, P.Y_BROOD + P.BROOD_H - 20, P.BROOD_D / 2, 1)

    # ---- left: window machining; back: window machining + cleat
    left = windows.cut_left_wall(walls["left"])
    back = windows.cut_back_wall(walls["back"])
    back = _cleat(back, P.Y_BROOD + P.BROOD_H - 20, P.BROOD_D / 2, -1)

    # ---- right: plain wall with a side cleat
    right = walls["right"] + box(
        HANDLE_D, HANDLE_H, HANDLE_W,
        P.BROOD_W / 2 + HANDLE_D / 2, P.Y_BROOD + P.BROOD_H - 20, 0)

    return {
        "brood_wall_front": front,
        "brood_wall_back": back,
        "brood_wall_left": left,
        "brood_wall_right": right,
    }

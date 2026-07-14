"""Flow super — 505 x 405 x 150, four rabbeted walls.

  * front & back walls: frame-rest rabbet along the top inner edge so the
    flow-frame top bars hang with their tops 5 mm below the box top
  * front wall: per-frame Ø10 drain-spout hole (feeds the external manifold)
    and a Ø14.5 key bearing hole per frame
  * right wall: Ø12.4 pass-through for the feeder tube
  * lifting cleats on front and back
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_x, cyl_z
from .joinery import rabbeted_walls

HANDLE_W = 80.0
HANDLE_H = 22.0
HANDLE_D = 15.0

KEY_AXIS_Y = P.Y_SUPER + P.KEY_AXIS_Y_OFF          # 626.4
FRAME_XS = [(i - (P.NUM_FF - 1) / 2) * P.FF_PITCH for i in range(P.NUM_FF)]


def _frame_rest(wall: Part, sgn: int) -> Part:
    """Cut the 10 x 10 frame-rest rabbet along the top inner edge."""
    return wall - box(
        P.SUPER_W - 2 * P.WALL - 0.5,
        P.FRAME_REST,
        P.FRAME_REST,
        0,
        P.Y_COVER - P.FRAME_REST / 2,
        sgn * (P.SUPER_D / 2 - P.WALL + P.FRAME_REST / 2),
    )


def build() -> dict[str, Part]:
    walls = rabbeted_walls(P.SUPER_W, P.SUPER_D, P.SUPER_H, P.Y_SUPER)
    zf = (P.SUPER_D - P.WALL) / 2          # front wall centre plane

    # ---- front wall: rests + spout holes + key bearing holes + cleat
    front = _frame_rest(walls["front"], 1)
    for x in FRAME_XS:
        front -= cyl_z(P.HARVEST_SPOUT_R + 0.2, P.WALL + 2, x, P.SPOUT_Y, zf)
        front -= cyl_z(P.KEY_HOLE_R_WALL, P.WALL + 2, x, KEY_AXIS_Y, zf)
    front += box(HANDLE_W, HANDLE_H, HANDLE_D,
                 0, P.Y_SUPER + 55, P.SUPER_D / 2 + HANDLE_D / 2)

    # ---- back wall: rests + cleat
    back = _frame_rest(walls["back"], -1)
    back += box(HANDLE_W, HANDLE_H, HANDLE_D,
                0, P.Y_SUPER + P.SUPER_H - 35, -(P.SUPER_D / 2 + HANDLE_D / 2))

    # ---- right wall: feeder tube pass-through + side cleat
    right = walls["right"]
    right -= cyl_x(P.FEED_TUBE_R + 0.2, P.WALL + 2,
                   (P.SUPER_W - P.WALL) / 2, P.Y_SUPER + 127, 0)
    # cleat sits LOW on this wall — the feeder tube/bracket occupies the top
    right += box(HANDLE_D, HANDLE_H, HANDLE_W,
                 P.SUPER_W / 2 + HANDLE_D / 2, P.Y_SUPER + 55, 0)

    # ---- left wall: side cleat
    left = walls["left"] + box(
        HANDLE_D, HANDLE_H, HANDLE_W,
        -(P.SUPER_W / 2 + HANDLE_D / 2), P.Y_SUPER + P.SUPER_H - 35, 0)

    return {
        "super_wall_front": front,
        "super_wall_back": back,
        "super_wall_left": left,
        "super_wall_right": right,
    }

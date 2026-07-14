"""Shared joinery: the classic rabbeted 4-wall hive-box construction.

Front and back walls span the full box width and carry a RABBET x RABBET
step at each end; the side walls fit between them and carry matching tongues,
so the four boards interlock exactly like a real (or 3D-printed) hive box.

All boxes are centred on X = Z = 0 in world coordinates.
"""

from build123d import Part

from .. import params as P
from ..helpers import box


def rabbeted_walls(W: float, D: float, H: float, y0: float) -> dict[str, Part]:
    """Return the four interlocking wall boards of a W x D box (height H,
    bottom at y0) as separate solids: keys 'front', 'back', 'left', 'right'.
    """
    yc = y0 + H / 2
    R = P.RABBET
    fit = P.FIT_STATIC

    walls: dict[str, Part] = {}

    # ---- front / back walls: full width, rabbet steps cut at each end
    for name, sgn in (("front", 1), ("back", -1)):
        w = box(W, H, P.WALL, 0, yc, sgn * (D - P.WALL) / 2)
        for xs in (1, -1):
            # cut the step on the inner face at each end
            w -= box(
                R,
                H + 2,
                R,
                xs * (W - R) / 2,
                yc,
                sgn * (D / 2 - P.WALL + R / 2),
            )
        walls[name] = w

    # ---- side walls: body between the front/back walls + corner tongues
    body_len = D - 2 * P.WALL - fit
    for name, xs in (("left", -1), ("right", 1)):
        w = box(P.WALL, H, body_len, xs * (W - P.WALL) / 2, yc, 0)
        for zs in (1, -1):
            # tongue that fills the rabbet (minus a static fit clearance);
            # extended 5 mm inward so it fuses with the wall body
            w += box(
                R - fit,
                H,
                R - fit + 5,
                xs * (W - (R - fit)) / 2,
                yc,
                zs * (D / 2 - P.WALL + (R - fit - 5) / 2),
            )
        walls[name] = w

    return walls

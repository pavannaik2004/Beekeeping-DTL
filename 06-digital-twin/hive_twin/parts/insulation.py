"""Insulation — 10 mm XPS foam panels lining the brood box inside on the
left, right and back walls only (front left clear for entrance ventilation,
exactly as in the visualiser). Window zones are cut out so the inspection
windows stay usable.
"""

from build123d import Part

from .. import params as P
from ..helpers import box
from . import windows


def build() -> dict[str, Part]:
    h = P.BROOD_H - 4
    yc = P.Y_BROOD + 2 + h / 2
    inner_w = P.BROOD_W - 2 * P.WALL          # 465
    inner_d = P.BROOD_D - 2 * P.WALL          # 365

    # left panel — cut the window opening free
    left = box(P.INSUL_T, h, inner_d, -inner_w / 2 + P.INSUL_T / 2, yc, 0)
    left -= box(P.INSUL_T + 2, windows.LOPEN_H, windows.LOPEN_W,
                -inner_w / 2 + P.INSUL_T / 2, windows.LWIN_CY, windows.LWIN_CZ)

    # right panel — plain
    right = box(P.INSUL_T, h, inner_d, inner_w / 2 - P.INSUL_T / 2, yc, 0)

    # back panel — spans between the side panels, window opening cut free
    back = box(inner_w - 2 * P.INSUL_T, h, P.INSUL_T,
               0, yc, -inner_d / 2 + P.INSUL_T / 2)
    back -= box(windows.BOPEN_W, windows.BOPEN_H, P.INSUL_T + 2,
                windows.BWIN_CX, windows.BWIN_CY, -inner_d / 2 + P.INSUL_T / 2)

    return {
        "insulation_left": left,
        "insulation_right": right,
        "insulation_back": back,
    }

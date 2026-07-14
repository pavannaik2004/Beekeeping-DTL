"""Queen excluder — 505 x 405 x 3 plate with a real working grid:
4.2 mm slots between 2 mm bars (worker bees pass, the queen cannot),
inside a 25 mm solid rim that carries the super's weight.
"""

from build123d import Part

from .. import params as P
from ..helpers import box


def build() -> dict[str, Part]:
    y = P.Y_QE + P.QE_T / 2
    plate = box(P.BROOD_W, P.QE_T, P.BROOD_D, 0, y, 0)

    grid_w = P.BROOD_W - 2 * P.QE_RIM         # 455 slot field across X
    grid_d = P.BROOD_D - 2 * P.QE_RIM         # 355 slot length along Z

    pitch = P.QE_SLOT + P.QE_BAR              # 6.2
    n = int((grid_w - P.QE_BAR) // pitch)     # bars between all slots
    span = n * pitch - P.QE_BAR               # total width actually used
    x0 = -span / 2 + P.QE_SLOT / 2
    for i in range(n):
        plate -= box(P.QE_SLOT, P.QE_T + 2, grid_d, x0 + i * pitch, y, 0)

    return {"queen_excluder": plate}

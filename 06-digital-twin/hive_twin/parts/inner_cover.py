"""Inner cover — 501 x 10 x 401 board resting on the super, with a Ø30
central bee-escape / ventilation hole (standard apiary practice; the
telescoping roof's inner board rests on this cover).
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_y


def build() -> dict[str, Part]:
    cover = box(P.SUPER_W - 4, P.COVER_T, P.SUPER_D - 4,
                0, P.Y_COVER + P.COVER_T / 2, 0)
    cover -= cyl_y(15.0, P.COVER_T + 2, 0, P.Y_COVER + P.COVER_T / 2, 0)
    return {"inner_cover": cover}

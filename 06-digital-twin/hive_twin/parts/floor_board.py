"""Floor board (bottom board) with integrated landing board.

One solid: the 555 x 455 x 20 base plate plus the sloping landing strip that
projects 60 mm forward under the hive entrance.
"""

from build123d import Part

from .. import params as P
from ..helpers import box


def build() -> dict[str, Part]:
    # Main board
    board = box(P.FLOOR_W, P.FLOOR_T, P.FLOOR_D, 0, P.Y_FLOOR + P.FLOOR_T / 2, 0)

    # Landing board — top flush with the floor top so bees walk straight in.
    land_t = P.FLOOR_T * 0.6
    landing = box(
        P.ENTRANCE_W + 60,
        land_t,
        P.LANDING_EXT,
        0,
        P.Y_FLOOR + P.FLOOR_T - land_t / 2,
        P.FLOOR_D / 2 + P.LANDING_EXT / 2,
    )

    return {"floor_board": board + landing}

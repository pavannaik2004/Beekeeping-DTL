"""Telescoping roof — 535 x 435 x 70.

  roof_body  four 13 mm rim walls + inner board. The inner board rests on the
             inner cover; the rim skirts 10 mm down AROUND the super with
             2 mm clearance per side (that is the "telescoping").
  roof_tin   2 mm galvanised tin cap with 15 mm bent-down edges.
"""

from build123d import Part

from .. import params as P
from ..helpers import box

RIM_T = (P.ROOF_W - P.SUPER_W - 2 * P.ROOF_CLEAR) / 2   # 13 (checks both axes)
Y_BOT = P.Y_ROOF - 10.0                                 # rim skirts 10 mm down
Y_TOP = Y_BOT + P.ROOF_H                                # 718


def build() -> dict[str, Part]:
    yc = (Y_BOT + Y_TOP) / 2

    # rim ring: outer box minus inner opening
    body = box(P.ROOF_W, P.ROOF_H, P.ROOF_D, 0, yc, 0)
    body -= box(P.ROOF_W - 2 * RIM_T, P.ROOF_H + 2, P.ROOF_D - 2 * RIM_T, 0, yc, 0)
    # inner board, fused into the rim, resting on the inner cover
    body += box(P.ROOF_W - 2 * RIM_T, 10, P.ROOF_D - 2 * RIM_T,
                0, P.Y_ROOF + 5, 0)

    # tin cap: top plate + four bent edges hanging 15 mm over the rim
    tin = box(P.ROOF_W + 6, P.TIN_T, P.ROOF_D + 6, 0, Y_TOP + P.TIN_T / 2, 0)
    bend_h = 15.0
    yb = Y_TOP - bend_h / 2
    for zs in (1, -1):
        tin += box(P.ROOF_W + 6, bend_h, P.TIN_T,
                   0, yb, zs * (P.ROOF_D + 6 - P.TIN_T) / 2)
    for xs in (1, -1):
        tin += box(P.TIN_T, bend_h, P.ROOF_D + 6,
                   xs * (P.ROOF_W + 6 - P.TIN_T) / 2, yb, 0)

    return {"roof_body": body, "roof_tin": tin}

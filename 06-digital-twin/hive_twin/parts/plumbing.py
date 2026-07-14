"""Harvest plumbing — external manifold on the super's front wall collects
honey from all 7 frame spouts and feeds a single tap; a drop hose fills the
jar on the ground. (Engineering deviation from the visualiser: see params.py.)

Parts: manifold, harvest_tap, harvest_hose, collection_jar.
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_x, cyl_y, cyl_z

FRAME_XS = [(i - (P.NUM_FF - 1) / 2) * P.FF_PITCH for i in range(P.NUM_FF)]

TAP_BODY_Z = P.TAP_Z                    # 300
TAP_TOP_Y = P.SPOUT_Y + 14.0
TAP_BOT_Y = P.SPOUT_Y - 24.0            # 486 nozzle exit


def build() -> dict[str, Part]:
    parts: dict[str, Part] = {}

    # ---------------- manifold: Ø20 tube across the front wall, Ø16 bore,
    # with an integral Ø18 outlet stub the tap pipe couples onto
    man = cyl_x(P.MANIFOLD_R, P.MANIFOLD_L, 0, P.SPOUT_Y, P.MAN_Z)
    man += cyl_z(9.0, 20, 0, P.SPOUT_Y, P.MAN_Z + 3 + 10)      # outlet stub
    man -= cyl_x(P.MANIFOLD_BORE, P.MANIFOLD_L - 6, 0, P.SPOUT_Y, P.MAN_Z)
    for x in FRAME_XS:                  # spout inlets on the wall side
        man -= cyl_z(P.HARVEST_SPOUT_R + 0.1, 13, x, P.SPOUT_Y, P.MAN_Z - 6.5)
    man -= cyl_z(P.PIPE_BORE, 22, 0, P.SPOUT_Y, P.MAN_Z + 12)  # outlet bore
    parts["manifold"] = man

    # ---------------- tap: forward pipe + valve body + nozzle + T-handle stem
    # pipe butts against the manifold stub (union coupling IRL)
    pipe_z0 = P.MAN_Z + 23.5
    tap = cyl_z(P.PIPE_R, TAP_BODY_Z - pipe_z0, 0, P.SPOUT_Y,
                (pipe_z0 + TAP_BODY_Z) / 2)
    tap += cyl_y(P.TAP_BODY_R, TAP_TOP_Y - TAP_BOT_Y, 0,
                 (TAP_TOP_Y + TAP_BOT_Y) / 2, TAP_BODY_Z)
    tap += cyl_y(4.0, 22, 0, TAP_TOP_Y + 11, TAP_BODY_Z)        # valve stem
    tap += box(50, 8, 12, 0, TAP_TOP_Y + 24, TAP_BODY_Z)        # handle
    tap -= cyl_z(P.PIPE_BORE, TAP_BODY_Z - P.MAN_Z + 4, 0, P.SPOUT_Y,
                 (P.MAN_Z + TAP_BODY_Z) / 2)                    # horizontal bore
    tap -= cyl_y(P.TAP_NOZZLE_R, P.SPOUT_Y - TAP_BOT_Y + 2, 0,
                 (P.SPOUT_Y + TAP_BOT_Y) / 2, TAP_BODY_Z)       # down bore
    parts["harvest_tap"] = tap

    # ---------------- drop hose (food-grade silicone tube)
    hose = cyl_y(P.HOSE_R, TAP_BOT_Y - P.HOSE_BOT_Y, 0,
                 (TAP_BOT_Y + P.HOSE_BOT_Y) / 2, TAP_BODY_Z)
    hose -= cyl_y(P.HOSE_BORE, TAP_BOT_Y - P.HOSE_BOT_Y + 2, 0,
                  (TAP_BOT_Y + P.HOSE_BOT_Y) / 2, TAP_BODY_Z)
    parts["harvest_hose"] = hose

    # ---------------- collection jar on the ground
    jar = cyl_y(P.JAR_R, P.JAR_H, 0, P.JAR_H / 2, TAP_BODY_Z)
    jar -= cyl_y(P.JAR_R - P.JAR_T, P.JAR_H, 0, P.JAR_T + P.JAR_H / 2, TAP_BODY_Z)
    parts["collection_jar"] = jar

    return parts

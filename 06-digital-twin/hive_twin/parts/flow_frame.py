"""Flow frame — the harvesting heart of the hive. 7 frames, 50 mm pitch.

Each frame is TWO solids:

FIXED half ("ff{i}_fixed"):
  * top bar 49.8 x 5 x 380 — hangs on the super's frame-rest rabbets
  * front/back end plates 48 x 135 x 8; the front one carries a Ø14 key
    bearing hole and the drain spout
  * bottom drain trough with a Ø10 internal channel that exits through the
    spout into the external manifold
  * 14 fixed cell columns (every even position, 12 mm pitch)

MOVING half ("ff{i}_moving"):
  * 13 moving cell columns (odd positions, 1 mm side clearance)
  * a top link rail joined to every column by twin cheek straps that
    straddle the key-blade sweep
  * at rest it sits on the trough; the flow key's flat blade lies under the
    link rail. Turning the key 90° stands the blade upright and lifts the
    whole moving half exactly 5 mm, breaking the cells open so honey drains
    down the column gaps into the trough -> spout -> manifold -> tap.
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_z

# ---- vertical stations (world Y)
Y_BODY_BOT = P.Y_SUPER + 5.0                   # 503 frame body bottom
Y_TROUGH_TOP = Y_BODY_BOT + 16.0               # 519
Y_COL_TOP = 617.0                              # columns 519..617
Y_RAIL_BOT = 623.0                             # link rail 623..631
Y_RAIL_TOP = 631.0
Y_BAR_BOT = P.Y_COVER - P.FRAME_REST           # 638 rests ledge
Y_BAR_TOP = Y_BAR_BOT + P.FF_TOPBAR_T          # 643 (5 below super top)
KEY_AXIS_Y = P.Y_SUPER + P.KEY_AXIS_Y_OFF      # 621.4 blade axis

# ---- length stations (Z)
Z_PLATE = 166.0                                # end plate centres +/-166
Z_BAR = 380.0                                  # top bar length
SPOUT_Z0, SPOUT_Z1 = 168.0, 209.0              # spout reaches into manifold

FRAME_XS = [(i - (P.NUM_FF - 1) / 2) * P.FF_PITCH for i in range(P.NUM_FF)]

# 27 cell-column stations, 12 mm pitch, centred: even = fixed, odd = moving
N_COL = 27
COL_Z = [-156.0 + 12.0 * i for i in range(N_COL)]

# The key blade (13.2 wide, centred on the frame axis) sweeps a Ø13.2 zone
# under the rail; the straps joining each moving column to the rail are twin
# side cheeks that straddle that sweep with 0.4 mm clearance.
CHEEK_X0 = P.KEY_BLADE_H / 2 + 0.4             # 7.0 from frame axis
CHEEK_W = 20.0 - CHEEK_X0                      # out to the rail edge (x 20)


def _fixed_half(xc: float) -> Part:
    w = P.FF_W                                                 # 48
    # top bar (49.8 wide: 0.2 clearance to the neighbouring bar)
    p = box(P.FF_PITCH - 0.2, P.FF_TOPBAR_T, Z_BAR,
            xc, (Y_BAR_BOT + Y_BAR_TOP) / 2, 0)
    # end plates (503 .. 638)
    for zs in (1, -1):
        p += box(w, Y_BAR_BOT - Y_BODY_BOT, P.FF_END_PLATE_T,
                 xc, (Y_BODY_BOT + Y_BAR_BOT) / 2, zs * Z_PLATE)
    # drain trough
    p += box(w, Y_TROUGH_TOP - Y_BODY_BOT, 2 * Z_PLATE,
             xc, (Y_BODY_BOT + Y_TROUGH_TOP) / 2, 0)
    # fixed cell columns (even stations)
    for i in range(0, N_COL, 2):
        p += box(w, Y_COL_TOP - Y_TROUGH_TOP, P.FF_COL_W,
                 xc, (Y_TROUGH_TOP + Y_COL_TOP) / 2, COL_Z[i])
    # drain spout out the front
    p += cyl_z(P.HARVEST_SPOUT_R, SPOUT_Z1 - SPOUT_Z0,
               xc, P.SPOUT_Y, (SPOUT_Z0 + SPOUT_Z1) / 2)

    # ---- machining
    # trough channel (Ø10) + top slot so honey falls into the channel
    p -= cyl_z(5.0, 312, xc, P.SPOUT_Y, 0)
    p -= box(8.0, 12.0, 300, xc, Y_TROUGH_TOP, 0)
    # drain bore through front cap, end plate and spout (Ø7)
    p -= cyl_z(P.HARVEST_SPOUT_BORE, 62, xc, P.SPOUT_Y, 180)
    # key bearing hole in the front end plate
    p -= cyl_z(P.KEY_HOLE_R_PLATE, P.FF_END_PLATE_T + 2, xc, KEY_AXIS_Y, Z_PLATE)
    return p


def _moving_half(xc: float) -> Part:
    w = P.FF_W - 2.0                                           # 46: 1 mm/side
    parts = None
    for i in range(1, N_COL, 2):
        c = box(w, Y_COL_TOP - Y_TROUGH_TOP, P.FF_COL_W,
                xc, (Y_TROUGH_TOP + Y_COL_TOP) / 2, COL_Z[i])
        parts = c if parts is None else parts + c
    # link rail under the top bar (320 long: 2 mm clearance to each end plate)
    parts += box(40.0, Y_RAIL_TOP - Y_RAIL_BOT, 320.0,
                 xc, (Y_RAIL_BOT + Y_RAIL_TOP) / 2, 0)
    # twin cheek straps join EVERY moving column to the rail, straddling
    # the key-blade sweep zone
    for i in range(1, N_COL, 2):
        for xs in (1, -1):
            parts += box(CHEEK_W, Y_RAIL_BOT - Y_COL_TOP, P.FF_COL_W,
                         xc + xs * (CHEEK_X0 + CHEEK_W / 2),
                         (Y_COL_TOP + Y_RAIL_BOT) / 2, COL_Z[i])
    return parts


def build() -> dict[str, Part]:
    out: dict[str, Part] = {}
    for i, xc in enumerate(FRAME_XS):
        out[f"ff{i}_fixed"] = _fixed_half(xc)
        out[f"ff{i}_moving"] = _moving_half(xc)
    return out

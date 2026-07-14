"""Top feeder — external funnel on the super's right wall feeding an internal
syrup tray through a Ø12 tube, so the keeper never opens the hive to feed.

Parts:
  feeder_funnel  funnel cone + elbow + feed tube + wall bracket (one weldment)
  feeder_tray    open 120 x 60 x 20 tray + hanging brackets (food-grade PP)
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_x, cyl_y, cone_y, torus_y

TUBE_Y = P.Y_SUPER + 127.0             # 625 — matches hole in super right wall
WALL_X = P.SUPER_W / 2                 # 252.5 outer face of right wall
ELBOW_X = WALL_X + 65.0                # 317.5 funnel axis


def build() -> dict[str, Part]:
    parts: dict[str, Part] = {}

    # ---------------- funnel + tube weldment
    # feed tube: from inside the super (over the tray) out through the wall
    f = cyl_x(P.FEED_TUBE_R, ELBOW_X - (WALL_X - 27.5),
              (ELBOW_X + WALL_X - 27.5) / 2, TUBE_Y, 0)
    # elbow riser under the funnel
    f += cyl_y(P.FEED_TUBE_R, 16, ELBOW_X, TUBE_Y + 8, 0)
    # funnel cone shell (2 mm wall), open top
    f += cone_y(P.FUNNEL_R_BOT, P.FUNNEL_R_TOP, P.FUNNEL_H, ELBOW_X, TUBE_Y + 14, 0)
    f += torus_y(P.FUNNEL_R_TOP, 2.0, ELBOW_X, TUBE_Y + 14 + P.FUNNEL_H, 0)
    f -= cone_y(P.FUNNEL_R_BOT - 2, P.FUNNEL_R_TOP - 2, P.FUNNEL_H + 0.1,
                ELBOW_X, TUBE_Y + 14.05, 0)
    # bores through funnel throat, elbow and tube
    f -= cyl_y(4.0, 40, ELBOW_X, TUBE_Y + 10, 0)
    f -= cyl_x(4.0, ELBOW_X - (WALL_X - 29.5) + 2,
               (ELBOW_X + WALL_X - 29.5) / 2, TUBE_Y, 0)
    # wall bracket: vertical plate on the wall + arm under the elbow
    f += box(3, 30, 40, WALL_X + 1.5, TUBE_Y - 5, 0)
    f += box(ELBOW_X - WALL_X, 6, 20, (ELBOW_X + WALL_X) / 2, TUBE_Y - 17, 0)
    f += cyl_y(P.FEED_TUBE_R + 2, 6, ELBOW_X, TUBE_Y - 17, 0)
    parts["feeder_funnel"] = f

    # ---------------- internal tray (hangs on the wall below the tube mouth)
    t = P.FEEDER_TRAY_T
    x1 = P.SUPER_W / 2 - P.WALL        # 232.5 inner wall face
    x0 = x1 - P.FEEDER_TRAY_W          # 112.5
    y0 = TUBE_Y - 25.0                 # 600 tray bottom
    tray = box(P.FEEDER_TRAY_W, P.FEEDER_TRAY_H, P.FEEDER_TRAY_D,
               (x0 + x1) / 2, y0 + P.FEEDER_TRAY_H / 2, 0)
    tray -= box(P.FEEDER_TRAY_W - 2 * t, P.FEEDER_TRAY_H, P.FEEDER_TRAY_D - 2 * t,
                (x0 + x1) / 2, y0 + t + P.FEEDER_TRAY_H / 2, 0)
    # hanging brackets: two hooks up the inner wall face
    for z in (-20, 20):
        tray += box(4, 45, 12, x1 - 2, y0 + P.FEEDER_TRAY_H + 2.5, z)
    parts["feeder_tray"] = tray

    return parts

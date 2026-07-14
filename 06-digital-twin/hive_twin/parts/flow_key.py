"""Flow key — cam blade + T-handle.

Inserted flat through the Ø14.5 bearing hole in the super front wall into the
Ø14 hole in the frame's front end plate. The 13.2 x 3.2 blade lies flat under
the moving half's link rail; turning it 90° stands it upright and lifts the
rail exactly (13.2 - 3.2) / 2 = 5 mm. One key serves all 7 frames; it is
modelled parked in the centre frame.
"""

from build123d import Part

from .. import params as P
from ..helpers import box, cyl_z

KEY_AXIS_Y = P.Y_SUPER + P.KEY_AXIS_Y_OFF      # 621.4
BLADE_Z0 = 207.0                               # blade back end (at the boss)
BLADE_Z1 = BLADE_Z0 - P.KEY_BLADE_L            # 57: tip clears the straps


def build() -> dict[str, Part]:
    # blade, lying flat (13.2 wide x 3.2 tall)
    key = box(P.KEY_BLADE_H, P.KEY_BLADE_W, P.KEY_BLADE_L,
              0, KEY_AXIS_Y, (BLADE_Z0 + BLADE_Z1) / 2)
    # boss outside the wall
    key += cyl_z(6.5, 10, 0, KEY_AXIS_Y, BLADE_Z0 + 5)
    # T-handle
    key += box(P.KEY_HANDLE_L, 10, 8, 0, KEY_AXIS_Y, BLADE_Z0 + 14)
    return {"flow_key": key}

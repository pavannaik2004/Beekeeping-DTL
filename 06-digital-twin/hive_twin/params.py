"""Single source of truth for every dimension of the beehive digital twin.

All values are millimetres, extracted 1:1 from the Three.js visualiser on the
gh-pages branch (index.html, "ISI STANDARD DIMENSIONS" block), plus the
engineering layer (tolerances, joinery, mechanism specs) that makes the design
physically buildable.

Coordinate convention (matches the Three.js scene):
    X = width  (left/right),  Y = height (up),  Z = depth (front = +Z)
"""

# ---------------------------------------------------------------- floor board
FLOOR_W = 555.0
FLOOR_D = 455.0
FLOOR_T = 20.0
LANDING_EXT = 60.0          # landing board extends this far forward of floor

# ----------------------------------------------------------------- brood box
BROOD_W = 505.0             # outer width
BROOD_D = 405.0             # outer depth
BROOD_H = 245.0             # wall height
WALL = 20.0                 # wall thickness (all boxes)
ENTRANCE_W = 365.0          # entrance slot in front wall
ENTRANCE_H = 10.0
BEE_SPACE = 9.0             # sacred bee space — clearances bees will not seal

# ---------------------------------------------------------------- insulation
INSUL_T = 10.0              # XPS panels inside left/right/back walls only

# ------------------------------------------------------------ queen excluder
QE_T = 3.0                  # overall thickness
QE_SLOT = 4.2               # slot gap: workers pass, queen cannot (apiary std)
QE_BAR = 2.0                # bar width between slots
QE_RIM = 25.0               # solid perimeter rim width

# ---------------------------------------------------------------------- super
SUPER_W = 505.0
SUPER_D = 405.0
SUPER_H = 150.0

# ---------------------------------------------------------------- inner cover
COVER_T = 10.0

# ------------------------------------------------------------ telescoping roof
ROOF_W = 535.0              # outer rim width  (telescopes over super)
ROOF_D = 435.0
ROOF_H = 70.0
TIN_T = 2.0                 # galvanised tin cap thickness
ROOF_RIM_T = 15.0           # rim wall thickness (from three.js rimT)

# ------------------------------------- left-wall inspection window + shutter
WIN_W = 200.0               # acrylic viewing aperture width  (along Z)
WIN_H = 140.0               # aperture height
WIN_FROM_BOTTOM = 55.0      # aperture bottom above brood box bottom
ACRYLIC_T = 5.0
RECESS_D = 12.0             # MDF recess frame width around aperture
SHUTTER_T = 3.0             # sliding shutter panel thickness
CHANNEL_W = 4.0             # channel groove width (SHUTTER_T + 2*slide fit)
CHANNEL_OVERHANG = 10.0     # channel extends past aperture each side
SHUTTER_TRAVEL = 150.0      # how far the shutter slides open
STOP_PIN_R = 1.5

# ------------------------------------------------ back-wall inspection window
BWIN_W = 180.0
BWIN_H = 120.0
BWIN_FROM_BOTTOM = 65.0
BWIN_OFFSET_X = 80.0        # aperture centre offset toward right side

# ----------------------------------------------------------------- top feeder
FUNNEL_R_TOP = 25.0
FUNNEL_R_BOT = 8.0
FUNNEL_H = 40.0
FEED_TUBE_R = 6.0
FEED_TUBE_L = 80.0
FEEDER_TRAY_W = 120.0
FEEDER_TRAY_D = 60.0
FEEDER_TRAY_H = 20.0
FEEDER_TRAY_T = 2.0         # tray wall thickness (food-grade plastic)

# ----------------------------------------------------------------- flow frames
FF_W = 48.0                 # frame body width (three.js value)
FF_PITCH = 50.0             # frame pitch: 50 mm so 48 mm top bars nearly touch
FF_L = 340.0                # frame length (along Z)
FF_H = 140.0                # frame height
NUM_FF = 7
FF_TOPBAR_T = 5.0           # top bar thickness
FF_CELL_PITCH = 12.0        # cell column pitch along Z (6 mm column + 6 gap)
FF_COL_W = 6.0              # cell column thickness along Z
FF_SPLIT_SHIFT = 5.0        # moving half lift when key turned 90° (harvest)
FF_END_PLATE_T = 8.0        # front/back end plates of the frame body
HARVEST_SPOUT_R = 4.8       # per-frame drain spout outer radius
HARVEST_SPOUT_BORE = 3.5

# ------------------------------------------------------------------- flow key
# Cam principle: the blade lying flat is 3.2 mm tall; rotated upright it is
# 13.2 mm tall, lifting the moving half exactly (13.2 - 3.2) / 2 = 5.0 mm.
# The blade turns inside round bearing holes in the super front wall and the
# frame's front end plate.
KEY_BLADE_W = 3.2           # blade thickness (flat height)
KEY_BLADE_H = 13.2          # blade width (upright height)
KEY_BLADE_L = 150.0
KEY_HANDLE_L = 80.0
KEY_HANDLE_R = 6.0
KEY_HOLE_R_WALL = 7.25      # Ø14.5 bearing hole in super front wall
KEY_HOLE_R_PLATE = 7.0      # Ø14.0 bearing hole in frame front end plate
KEY_AXIS_Y_OFF = 123.4      # blade axis above super bottom (-> y = 621.4)

# ---------------------------------------------------------------------- stand
STAND_H = 230.0             # ground to underside of floor board
STAND_FOOT_R_TOP = 80.0
STAND_FOOT_R_BOT = 105.0
STAND_FOOT_H = 18.0
STAND_POLE_R = 30.0         # top radius (bottom flares +3, from three.js)
STAND_PLAT_T = 16.0         # platform plate under floor board
STAND_PLAT_OH = 15.0        # platform overhang beyond floor each side
WATER_RING_R = 55.0         # torus centre radius (ant barrier / bee waterer)
WATER_RING_TUBE = 14.0      # torus tube radius

# ---------------------------------------------------- harvest plumbing (front)
# NOTE — engineering deviation from the visualiser: the three.js file puts the
# manifold INSIDE the super 6 mm below its floor (impossible: the queen
# excluder is there) and drops the hose at Z = 277.5 (through the landing
# board). The twin mounts the manifold EXTERNALLY on the front wall, fed by a
# spout from each frame, and moves the tap/hose/jar to Z = 300, clear of the
# landing board.
MANIFOLD_R = 10.0           # manifold tube outer radius
MANIFOLD_BORE = 8.0
MANIFOLD_L = 360.0          # spans all 7 spouts
PIPE_R = 8.0                # forward pipe outer radius
PIPE_BORE = 6.0
TAP_BODY_R = 12.0
TAP_NOZZLE_R = 6.0
HOSE_R = 8.0
HOSE_BORE = 5.0
HOSE_BOT_Y = 150.0          # hose lower end (above jar mouth)
JAR_R = 55.0
JAR_H = 130.0
JAR_T = 3.0

# ------------------------------------------------------------------ tolerances
FIT_SLIDE = 0.4             # total clearance for sliding fits (shutter, key)
FIT_STATIC = 0.2            # press/static fits (acrylic in recess)
ROOF_CLEAR = 2.0            # telescoping roof inner clearance per side

# --------------------------------------------------------------------- joinery
RABBET = 10.0               # 10 x 10 mm rabbet joints on box corners
FRAME_REST = 10.0           # frame-rest rabbet in super front/back walls

# --------------------------------------------------------------------- Y stack
Y_FLOOR = STAND_H                       # floor board bottom
Y_BROOD = Y_FLOOR + FLOOR_T             # brood box bottom
Y_QE = Y_BROOD + BROOD_H                # queen excluder bottom
Y_SUPER = Y_QE + QE_T                   # super bottom
Y_COVER = Y_SUPER + SUPER_H             # inner cover bottom
Y_ROOF = Y_COVER + COVER_T              # roof rim bottom

# ------------------------------------------------- harvest plumbing positions
SPOUT_Y = Y_SUPER + 12.0                # spout / wall-hole / manifold axis height
MAN_Z = SUPER_D / 2 + 10.5              # manifold axis: hugs front wall outside
TAP_Z = 300.0                           # tap + hose + jar Z (clear of landing)

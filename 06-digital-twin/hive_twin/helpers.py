"""Small geometry helpers shared by all part modules.

Coordinate convention (matches the Three.js scene on gh-pages):
    X = width (left/right), Y = height (up), Z = depth (front = +Z).
All parts are built directly in WORLD coordinates so the assembly is just the
union of everything and per-part exports stay consistent with the drawings.
"""

from build123d import Box, Cylinder, Cone, Torus, Pos, Rot, Part


def box(w: float, h: float, d: float, x: float = 0, y: float = 0, z: float = 0) -> Part:
    """Axis-aligned box, w along X, h along Y, d along Z, centred at (x, y, z)."""
    return Pos(x, y, z) * Box(w, h, d)


def box_yz(w: float, h: float, d: float, x: float, y0: float, z: float) -> Part:
    """Box whose BOTTOM face is at y0 (often more natural than the centre)."""
    return box(w, h, d, x, y0 + h / 2, z)


def cyl_y(r: float, h: float, x: float = 0, y: float = 0, z: float = 0) -> Part:
    """Cylinder with vertical (Y) axis, centred at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def cyl_x(r: float, h: float, x: float = 0, y: float = 0, z: float = 0) -> Part:
    """Cylinder with X axis, centred at (x, y, z)."""
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def cyl_z(r: float, h: float, x: float = 0, y: float = 0, z: float = 0) -> Part:
    """Cylinder with Z axis (front/back), centred at (x, y, z)."""
    return Pos(x, y, z) * Cylinder(r, h)


def cone_y(r_bot: float, r_top: float, h: float, x: float, y_bot: float, z: float) -> Part:
    """Cone with vertical axis, base at y_bot."""
    return Pos(x, y_bot + h / 2, z) * Rot(-90, 0, 0) * Cone(r_bot, r_top, h)


def torus_y(r_major: float, r_minor: float, x: float, y: float, z: float) -> Part:
    """Torus lying flat (axis vertical), centred at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Torus(r_major, r_minor)

"""Monocoque hull generator.

The hull is modeled as a shell lofted through circular stations whose
radius follows an ellipsoidal profile along the vehicle's long axis (Z),
then hollowed to ``wall_thickness_m``. This is the simplest closed
monocoque shape that gives nozzles, ribs, and mounts a well-defined outer
surface -- swap the station profile for a different hull shape once
aero/structural sweeps (``optimization/``) favor one.
"""

from __future__ import annotations

import math

from cad._cq import cq, require_cadquery
from cad.parameters import HullParameters


def _station_radius(t: float, max_radius_m: float) -> float:
    """Ellipsoidal radius profile at normalized station position t in [0, 1]."""
    return max_radius_m * math.sqrt(max(0.0, 1.0 - (2.0 * t - 1.0) ** 2))


def build_hull(params: HullParameters, num_stations: int = 16):
    """Return a hollow monocoque hull shell as a cadquery Workplane solid."""
    require_cadquery()

    max_radius_m = params.max_diameter_m / 2.0
    station_spacing_m = params.length_m / num_stations

    wp = cq.Workplane("XY")
    for i in range(num_stations + 1):
        t = i / num_stations
        radius_m = max(_station_radius(t, max_radius_m), 1e-4)
        wp = (
            wp.circle(radius_m)
            if i == 0
            else wp.workplane(offset=station_spacing_m).circle(radius_m)
        )

    outer_solid = wp.loft(ruled=True)
    return outer_solid.shell(-params.wall_thickness_m)

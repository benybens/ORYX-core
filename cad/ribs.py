"""Structural ribs stiffening the hull shell.

Modeled as flat radial fins evenly spaced around the hull's long axis,
spanning a fixed axial height centered on the hull midpoint. A minimal
structural placeholder pending a real structural sizing study
(``docs/research_log.md``).
"""

from __future__ import annotations

import math

from cad._cq import cq, require_cadquery
from cad.parameters import HullParameters, RibParameters


def build_ribs(hull_params: HullParameters, rib_params: RibParameters):
    """Return a compound of ``rib_params.count`` radial stiffening ribs."""
    require_cadquery()

    max_radius_m = hull_params.max_diameter_m / 2.0
    z_center_m = hull_params.length_m / 2.0

    ribs = None
    for i in range(rib_params.count):
        theta = 2.0 * math.pi * i / rib_params.count
        rib = (
            cq.Workplane("XY")
            .center(0, 0)
            .transformed(rotate=(0, 0, math.degrees(theta)))
            .rect(rib_params.thickness_m, max_radius_m * 2.0, centered=(True, False))
            .extrude(rib_params.height_m)
            .translate((0, 0, z_center_m - rib_params.height_m / 2.0))
        )
        ribs = rib if ribs is None else ribs.union(rib)
    return ribs

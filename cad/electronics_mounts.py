"""Electronics support structure: a standoff plate for avionics/battery stacks."""

from __future__ import annotations

import math

from cad._cq import cq, require_cadquery
from cad.parameters import ElectronicsMountParameters


def build_electronics_mount(params: ElectronicsMountParameters):
    """Return a mounting plate on standoffs, centered on the local XY origin."""
    require_cadquery()

    plate = (
        cq.Workplane("XY")
        .circle(params.plate_diameter_m / 2.0)
        .extrude(params.plate_thickness_m)
        .translate((0, 0, params.standoff_height_m))
    )

    standoff_radius_m = params.plate_diameter_m / 2.0 * 0.8
    standoffs = None
    for i in range(params.standoff_count):
        theta = 2.0 * math.pi * i / params.standoff_count
        x = standoff_radius_m * math.cos(theta)
        y = standoff_radius_m * math.sin(theta)
        post = (
            cq.Workplane("XY", origin=(x, y, 0))
            .circle(params.plate_thickness_m)
            .extrude(params.standoff_height_m)
        )
        standoffs = post if standoffs is None else standoffs.union(post)

    return plate.union(standoffs) if standoffs is not None else plate

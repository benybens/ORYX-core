"""Internal plenum (pressure vessel) generator.

Modeled as a sphere sized to hold ``volume_l`` -- the simplest
pressure-efficient shape, and propulsion-technology-agnostic since the
plenum's job here is purely to distribute fluid to the nozzle array, not
to generate it. Positioned at the hull center; callers translate/scale as
needed once hull interference checks (``cad.build``) require it.
"""

from __future__ import annotations

import math

from cad._cq import cq, require_cadquery
from cad.parameters import PlenumParameters


def build_plenum(params: PlenumParameters):
    """Return a hollow spherical plenum shell sized to ``volume_l``."""
    require_cadquery()

    volume_m3 = params.volume_l / 1000.0
    inner_radius_m = (3.0 * volume_m3 / (4.0 * math.pi)) ** (1.0 / 3.0)
    outer_radius_m = inner_radius_m + params.wall_thickness_m

    outer = cq.Workplane("XY").sphere(outer_radius_m)
    return outer.shell(-params.wall_thickness_m)


def plenum_outer_radius_m(params: PlenumParameters) -> float:
    """Outer radius of the plenum, for hull-interference checks in cad.build."""
    volume_m3 = params.volume_l / 1000.0
    inner_radius_m = (3.0 * volume_m3 / (4.0 * math.pi)) ** (1.0 / 3.0)
    return inner_radius_m + params.wall_thickness_m

"""Generic propulsion mounting interface: a bolt-circle flange.

This is the mechanical contract between the airframe and *any* propulsion
module (see ``propulsion.base.PropulsionCellBase``): a flange face with a
bolt circle at each nozzle position/orientation. Because it is
deliberately technology-agnostic, this interface should not need to
change when the propulsion technology behind it does -- only the module
bolted to it changes.
"""

from __future__ import annotations

import math

import numpy as np

from cad._cq import cq, require_cadquery
from cad.nozzle_array import NozzlePose
from cad.parameters import PropulsionInterfaceParameters


def _orientation_from_z(direction: np.ndarray) -> tuple[float, float, float]:
    """Return a cadquery-compatible normal vector to build a Workplane aligned to ``direction``."""
    d = direction / np.linalg.norm(direction)
    return (float(d[0]), float(d[1]), float(d[2]))


def build_propulsion_interface(pose: NozzlePose, params: PropulsionInterfaceParameters):
    """Return a bolt-circle flange solid positioned and oriented at ``pose``."""
    require_cadquery()

    normal = _orientation_from_z(pose.thrust_direction)
    origin = tuple(pose.position_m.tolist())

    flange = (
        cq.Workplane(cq.Plane(origin=origin, normal=normal))
        .circle(params.bolt_circle_diameter_m / 2.0 + params.bolt_hole_diameter_m)
        .extrude(params.flange_thickness_m)
    )

    bolt_positions = []
    for i in range(params.bolt_count):
        theta = 2.0 * math.pi * i / params.bolt_count
        bolt_positions.append(
            (
                (params.bolt_circle_diameter_m / 2.0) * math.cos(theta),
                (params.bolt_circle_diameter_m / 2.0) * math.sin(theta),
            )
        )

    holes = (
        cq.Workplane(cq.Plane(origin=origin, normal=normal))
        .pushPoints(bolt_positions)
        .circle(params.bolt_hole_diameter_m / 2.0)
        .extrude(params.flange_thickness_m * 2.0)
    )

    return flange.cut(holes)


def build_propulsion_interfaces(poses: list[NozzlePose], params: PropulsionInterfaceParameters):
    """Return a compound of one propulsion mounting flange per nozzle pose."""
    require_cadquery()

    interfaces = None
    for pose in poses:
        flange = build_propulsion_interface(pose, params)
        interfaces = flange if interfaces is None else interfaces.union(flange)
    return interfaces

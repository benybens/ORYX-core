"""Distributed nozzle array placement.

Produces bore geometry and the body-frame mounting pose (position +
thrust direction) of each nozzle -- the same
:class:`propulsion.base.PropulsionCellSpec` geometry fields flight control
and simulation use, so a nozzle layout can be fed directly into
``flight_control.ThrustAllocator`` for allocation studies before any
propulsion hardware exists.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from cad._cq import cq, require_cadquery
from cad.parameters import HullParameters, NozzleArrayParameters


@dataclass
class NozzlePose:
    """Body-frame position and outward thrust direction of one nozzle."""

    index: int
    position_m: np.ndarray
    thrust_direction: np.ndarray


def nozzle_poses(
    hull_params: HullParameters, nozzle_params: NozzleArrayParameters
) -> list[NozzlePose]:
    """Compute the body-frame pose of each nozzle in an equally spaced ring.

    The ring sits at ``band_latitude_deg`` above/below the hull equator,
    on the hull surface; each nozzle points radially outward, canted aft
    by ``cant_angle_deg`` to add a net component of thrust along the
    vehicle's long axis in addition to the radial component.
    """
    max_radius_m = hull_params.max_diameter_m / 2.0
    lat_rad = math.radians(nozzle_params.band_latitude_deg)
    cant_rad = math.radians(nozzle_params.cant_angle_deg)

    band_radius_m = max_radius_m * math.cos(lat_rad)
    axial_position_m = (hull_params.length_m / 2.0) * math.sin(lat_rad) + hull_params.length_m / 2.0

    poses = []
    for i in range(nozzle_params.count):
        theta = 2.0 * math.pi * i / nozzle_params.count
        position_m = np.array(
            [band_radius_m * math.cos(theta), band_radius_m * math.sin(theta), axial_position_m]
        )
        radial_direction = np.array([math.cos(theta), math.sin(theta), 0.0])
        axial_direction = np.array([0.0, 0.0, 1.0])
        thrust_direction = (
            math.cos(cant_rad) * radial_direction + math.sin(cant_rad) * axial_direction
        )
        thrust_direction /= np.linalg.norm(thrust_direction)
        poses.append(NozzlePose(index=i, position_m=position_m, thrust_direction=thrust_direction))
    return poses


def build_nozzle_bores(hull_params: HullParameters, nozzle_params: NozzleArrayParameters):
    """Return a compound of cylindrical nozzle bore solids, one per pose.

    Intended to be cut from the hull (``bore_solid - hull``) once
    ``cad.build`` composes the full assembly.
    """
    require_cadquery()

    bores = None
    for pose in nozzle_poses(hull_params, nozzle_params):
        direction = tuple(pose.thrust_direction.tolist())
        origin = tuple(pose.position_m.tolist())
        bore = (
            cq.Workplane(cq.Plane(origin=origin, normal=direction))
            .circle(nozzle_params.diameter_m / 2.0)
            .extrude(hull_params.wall_thickness_m * 3.0)
        )
        bores = bore if bores is None else bores.union(bore)
    return bores

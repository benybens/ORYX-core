"""Feed channels connecting the plenum to each nozzle.

Routed as straight tubes for now -- curved/optimized routing (to minimize
pressure loss, see ``simulation.generic_propulsion``'s
``pressure_loss_fraction``) is future work once a propulsion technology
and its acceptable loss budget are known.
"""

from __future__ import annotations

import numpy as np

from cad._cq import cq, require_cadquery
from cad.nozzle_array import NozzlePose
from cad.parameters import ChannelParameters


def build_channel(start_m: np.ndarray, end_m: np.ndarray, params: ChannelParameters):
    """Return a straight tube solid from ``start_m`` to ``end_m`` (body frame, meters)."""
    require_cadquery()

    start_m = np.asarray(start_m, dtype=float)
    end_m = np.asarray(end_m, dtype=float)
    length_m = float(np.linalg.norm(end_m - start_m))
    if length_m == 0:
        raise ValueError("channel start and end points must differ")

    outer = (
        cq.Workplane("XY", origin=tuple(start_m.tolist()))
        .circle(params.diameter_m / 2.0 + params.wall_thickness_m)
        .extrude(length_m)
    )
    inner = (
        cq.Workplane("XY", origin=tuple(start_m.tolist()))
        .circle(params.diameter_m / 2.0)
        .extrude(length_m)
    )
    return outer.cut(inner)


def build_channels(
    plenum_center_m: np.ndarray, nozzle_poses: list[NozzlePose], params: ChannelParameters
):
    """Return a compound of one feed channel per nozzle pose, from the plenum center."""
    require_cadquery()

    channels = None
    for pose in nozzle_poses:
        channel = build_channel(plenum_center_m, pose.position_m, params)
        channels = channel if channels is None else channels.union(channel)
    return channels

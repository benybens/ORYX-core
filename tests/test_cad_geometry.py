"""CAD geometry generation tests -- skipped where cadquery is not installed.

cadquery is a conda-managed optional dependency (see environment.yml); CI
does not install it (see .github/workflows/ci.yml), so these tests only
run in a local dev environment with the ``cad`` extra installed.
"""

from __future__ import annotations

import pytest

cq = pytest.importorskip("cadquery")

from cad.hull import build_hull  # noqa: E402
from cad.nozzle_array import nozzle_poses  # noqa: E402
from cad.parameters import VehicleParameters  # noqa: E402


def test_build_hull_has_positive_volume():
    params = VehicleParameters()
    hull = build_hull(params.hull)
    assert hull.val().Volume() > 0


def test_nozzle_poses_count_and_unit_directions():
    params = VehicleParameters()
    poses = nozzle_poses(params.hull, params.nozzles)
    assert len(poses) == params.nozzles.count
    for pose in poses:
        assert abs(1.0 - (pose.thrust_direction**2).sum() ** 0.5) < 1e-9

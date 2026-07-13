"""Tests for the generic thrust allocation framework."""

from __future__ import annotations

import numpy as np

from flight_control.allocator import ThrustAllocator
from flight_control.wrench import Wrench


def test_zero_wrench_yields_zero_thrust(quad_vertical_cell_specs):
    allocator = ThrustAllocator(quad_vertical_cell_specs)
    result = allocator.allocate(Wrench())
    assert all(cmd.thrust_fraction == 0.0 for cmd in result.commands.values())
    assert result.saturated_cells == []


def test_symmetric_layout_distributes_pure_lift_equally(quad_vertical_cell_specs):
    allocator = ThrustAllocator(quad_vertical_cell_specs)
    result = allocator.allocate(Wrench(fz=-8.0))  # -Z = up, 2 N per thruster if shared equally
    thrusts = list(result.thrust_n.values())
    assert np.allclose(thrusts, thrusts[0], atol=1e-9)
    assert np.isclose(sum(thrusts), 8.0, atol=1e-6)


def test_unsaturated_allocation_reproduces_achievable_wrench(quad_vertical_cell_specs):
    allocator = ThrustAllocator(quad_vertical_cell_specs)
    # Fz + Mx are within this layout's achievable subspace (no yaw/lateral authority).
    requested = Wrench(fz=-6.0, mx=0.1)
    result = allocator.allocate(requested)
    assert result.saturated_cells == []
    assert np.isclose(result.error.norm(), 0.0, atol=1e-6)


def test_saturation_clips_to_cell_limits(quad_vertical_cell_specs):
    allocator = ThrustAllocator(quad_vertical_cell_specs)
    # 4 cells x 5 N max = 20 N max lift; ask for far more.
    result = allocator.allocate(Wrench(fz=-100.0))
    assert len(result.saturated_cells) == 4
    for fraction in result.commands.values():
        assert np.isclose(fraction.thrust_fraction, 1.0)
    assert result.error.norm() > 0


def test_effectiveness_matrix_shape(quad_vertical_cell_specs):
    allocator = ThrustAllocator(quad_vertical_cell_specs)
    assert allocator.effectiveness_matrix.shape == (6, 4)

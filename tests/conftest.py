"""Shared pytest fixtures: propulsion cell layouts used across test modules."""

from __future__ import annotations

import numpy as np
import pytest

from propulsion.base import PropulsionCellSpec


@pytest.fixture
def quad_vertical_cell_specs() -> list[PropulsionCellSpec]:
    """Four identical vertical thrusters at the corners of a square.

    Body frame is +Z down, so thrust_direction (0, 0, -1) produces lift.
    Symmetric enough to hand-verify allocator behavior for Fz and roll/pitch.
    """
    offsets = [(0.1, 0.1), (0.1, -0.1), (-0.1, 0.1), (-0.1, -0.1)]
    return [
        PropulsionCellSpec(
            cell_id=f"cell_{i}",
            position_m=np.array([x, y, 0.0]),
            thrust_direction=np.array([0.0, 0.0, -1.0]),
            max_thrust_n=5.0,
        )
        for i, (x, y) in enumerate(offsets)
    ]

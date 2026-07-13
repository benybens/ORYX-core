"""Tests for the generic propulsion simulation surrogate."""

from __future__ import annotations

import numpy as np

from propulsion.base import PropulsionCellSpec, PropulsionCommand
from simulation.generic_propulsion import GenericPropulsionCell, GenericPropulsionParams


def _spec() -> PropulsionCellSpec:
    return PropulsionCellSpec(
        cell_id="a", position_m=[0, 0, 0], thrust_direction=[0, 0, -1], max_thrust_n=10.0
    )


def test_thrust_converges_to_commanded_value():
    cell = GenericPropulsionCell(_spec(), GenericPropulsionParams(response_time_s=0.05))
    cell.command(PropulsionCommand(thrust_fraction=1.0))
    state = None
    for _ in range(500):
        state = cell.step(0.01)
    assert np.isclose(state.actual_thrust_n, 10.0, atol=1e-2)


def test_pressure_loss_derates_asymptotic_thrust():
    cell = GenericPropulsionCell(
        _spec(), GenericPropulsionParams(response_time_s=0.05, pressure_loss_fraction=0.2)
    )
    cell.command(PropulsionCommand(thrust_fraction=1.0))
    state = None
    for _ in range(500):
        state = cell.step(0.01)
    assert np.isclose(state.actual_thrust_n, 8.0, atol=1e-2)


def test_power_draw_scales_with_thrust():
    params = GenericPropulsionParams(power_per_newton_w=100.0)
    cell = GenericPropulsionCell(_spec(), params)
    cell.command(PropulsionCommand(thrust_fraction=0.5))
    state = None
    for _ in range(500):
        state = cell.step(0.01)
    assert np.isclose(state.power_draw_w, 5.0 * 100.0, atol=1.0)


def test_reset_zeros_internal_state():
    cell = GenericPropulsionCell(_spec())
    cell.command(PropulsionCommand(thrust_fraction=1.0))
    cell.step(1.0)
    cell.reset()
    state = cell.step(1e-9)
    assert state.actual_thrust_n == 0.0

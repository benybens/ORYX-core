"""Tests for the propulsion plugin interface and registry."""

from __future__ import annotations

import numpy as np
import pytest

import propulsion.cells  # noqa: F401 - registers plugins
from propulsion.base import PropulsionCellBase, PropulsionCellSpec, PropulsionCommand
from propulsion.registry import available, create, get, register


def test_cell_spec_normalizes_thrust_direction():
    spec = PropulsionCellSpec(
        cell_id="a",
        position_m=[0, 0, 0],
        thrust_direction=[0, 0, -3.0],
        max_thrust_n=10.0,
    )
    assert np.isclose(np.linalg.norm(spec.thrust_direction), 1.0)
    assert np.allclose(spec.thrust_direction, [0, 0, -1.0])


def test_cell_spec_rejects_zero_direction():
    with pytest.raises(ValueError):
        PropulsionCellSpec(
            cell_id="a", position_m=[0, 0, 0], thrust_direction=[0, 0, 0], max_thrust_n=1.0
        )


def test_cell_spec_rejects_bad_thrust_bounds():
    with pytest.raises(ValueError):
        PropulsionCellSpec(
            cell_id="a", position_m=[0, 0, 0], thrust_direction=[0, 0, 1], max_thrust_n=-1.0
        )


def test_command_rejects_out_of_range_fraction():
    with pytest.raises(ValueError):
        PropulsionCommand(thrust_fraction=1.5)


def test_registry_has_all_documented_technologies():
    expected = {"compressed_gas", "edf", "plasma", "combustion", "ion"}
    assert expected.issubset(set(available()))


def test_registry_create_and_get_roundtrip():
    spec = PropulsionCellSpec(
        cell_id="a", position_m=[0, 0, 0], thrust_direction=[0, 0, -1], max_thrust_n=5.0
    )
    cell = create("compressed_gas", spec)
    assert isinstance(cell, get("compressed_gas"))
    assert cell.spec.cell_id == "a"


def test_registry_unknown_technology_raises():
    with pytest.raises(KeyError):
        get("warp_drive")


def test_stub_technologies_raise_not_implemented_for_physics():
    spec = PropulsionCellSpec(
        cell_id="a", position_m=[0, 0, 0], thrust_direction=[0, 0, -1], max_thrust_n=5.0
    )
    for name in ("compressed_gas", "edf", "plasma", "combustion", "ion"):
        cell = create(name, spec)
        with pytest.raises(NotImplementedError):
            cell.command(PropulsionCommand(thrust_fraction=0.5))


def test_register_rejects_non_subclass():
    with pytest.raises(TypeError):

        @register("not_a_cell")
        class NotACell:
            pass


def test_generic_propulsion_cell_satisfies_interface():
    from simulation.generic_propulsion import GenericPropulsionCell

    spec = PropulsionCellSpec(
        cell_id="a", position_m=[0, 0, 0], thrust_direction=[0, 0, -1], max_thrust_n=5.0
    )
    cell = GenericPropulsionCell(spec)
    assert isinstance(cell, PropulsionCellBase)

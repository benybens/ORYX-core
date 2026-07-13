"""Tests for CAD parameter dataclasses (no cadquery dependency required)."""

from __future__ import annotations

from cad.parameters import HullParameters, VehicleParameters


def test_default_construction():
    params = VehicleParameters()
    assert params.hull.length_m > 0
    assert params.nozzles.count >= 1


def test_round_trip_dict():
    params = VehicleParameters(hull=HullParameters(length_m=0.9))
    restored = VehicleParameters.from_dict(params.to_dict())
    assert restored.hull.length_m == 0.9
    assert restored == params


def test_round_trip_yaml(tmp_path):
    params = VehicleParameters(hull=HullParameters(length_m=1.2, max_diameter_m=0.5))
    path = tmp_path / "params.yaml"
    params.to_yaml(path)
    restored = VehicleParameters.from_yaml(path)
    assert restored == params

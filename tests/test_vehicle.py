"""End-to-end test wiring rigid body + allocator + generic propulsion + logging."""

from __future__ import annotations

import numpy as np

from flight_control.wrench import Wrench
from simulation.rigid_body import RigidBodyParams
from simulation.vehicle import Vehicle, VehicleConfig


def test_vehicle_hover_step_runs_and_logs(quad_vertical_cell_specs):
    config = VehicleConfig(
        rigid_body_params=RigidBodyParams(mass_kg=1.0, inertia_kg_m2=np.eye(3) * 0.01),
        cell_specs=quad_vertical_cell_specs,
    )
    vehicle = Vehicle(config)

    hover_wrench = Wrench(fz=-config.rigid_body_params.mass_kg * 9.80665)
    for _ in range(20):
        vehicle.step(hover_wrench, dt=0.01)

    df = vehicle.logger.to_dataframe()
    assert len(df) == 20
    assert "total_power_w" in df.columns
    assert (df["total_power_w"] >= 0).all()
    assert vehicle.energy.total_energy_j > 0

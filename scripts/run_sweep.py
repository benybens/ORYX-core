"""Example end-to-end parameter sweep: mass and propulsion response time vs.
hover performance metrics, using the generic propulsion surrogate (no real
propulsion technology exists yet).

Run with: python scripts/run_sweep.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from flight_control.wrench import Wrench
from optimization.objectives import thrust_to_weight_ratio
from optimization.parameter_space import ParameterSpace, ParameterSpec
from optimization.sweep import SweepRunner
from propulsion.base import PropulsionCellSpec
from simulation.generic_propulsion import GenericPropulsionParams
from simulation.rigid_body import RigidBodyParams
from simulation.vehicle import Vehicle, VehicleConfig

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "experiments" / "runs" / "example_sweep" / "results.csv"

GRAVITY_M_S2 = 9.80665
CELL_OFFSETS_M = [(0.1, 0.1), (0.1, -0.1), (-0.1, 0.1), (-0.1, -0.1)]


@dataclass
class SweepConfig:
    mass_kg: float = 1.0
    response_time_s: float = 0.05
    max_thrust_per_cell_n: float = 5.0


def _build_vehicle(config: SweepConfig) -> Vehicle:
    cell_specs = [
        PropulsionCellSpec(
            cell_id=f"cell_{i}",
            position_m=np.array([x, y, 0.0]),
            thrust_direction=np.array([0.0, 0.0, -1.0]),
            max_thrust_n=config.max_thrust_per_cell_n,
        )
        for i, (x, y) in enumerate(CELL_OFFSETS_M)
    ]
    vehicle_config = VehicleConfig(
        rigid_body_params=RigidBodyParams(mass_kg=config.mass_kg, inertia_kg_m2=np.eye(3) * 0.01),
        cell_specs=cell_specs,
        propulsion_params=GenericPropulsionParams(response_time_s=config.response_time_s),
    )
    return Vehicle(vehicle_config)


def objective(config: SweepConfig) -> dict[str, float]:
    """Simulate 2 s of hover and report steady-state tracking + energy metrics."""
    vehicle = _build_vehicle(config)
    hover_wrench = Wrench(fz=-config.mass_kg * GRAVITY_M_S2)
    dt = 0.01
    for _ in range(200):
        vehicle.step(hover_wrench, dt)

    total_max_thrust_n = config.max_thrust_per_cell_n * len(vehicle.cells)
    df = vehicle.logger.to_dataframe()
    return {
        "thrust_to_weight": thrust_to_weight_ratio(total_max_thrust_n, config.mass_kg),
        "settled_wrench_error_n": float(df["wrench_error_n"].iloc[-1]),
        "total_energy_j": vehicle.energy.total_energy_j,
    }


def main() -> None:
    base_config = SweepConfig()
    space = ParameterSpace(
        specs=[
            ParameterSpec("mass_kg", [0.8, 1.0, 1.2]),
            ParameterSpec("response_time_s", [0.02, 0.05, 0.1]),
        ]
    )
    runner = SweepRunner(base_config, space, objective)
    results = runner.run_grid()

    SweepRunner.save(results, OUTPUT_PATH)
    print(f"Ran {len(results)} sweep points -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

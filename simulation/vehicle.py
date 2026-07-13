"""Top-level simulation loop tying rigid body dynamics, thrust allocation,
propulsion cells, energy, and thermal models together.

This is the single place that composes the other simulation modules; it
holds no physics of its own. Swap ``cells`` for real ``propulsion.cells``
plugins once they exist -- everything else here is unaffected because it
only ever talks to :class:`propulsion.base.PropulsionCellBase`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from flight_control.allocator import ThrustAllocator
from flight_control.wrench import Wrench
from propulsion.base import PropulsionCellBase, PropulsionCellSpec
from simulation.energy import EnergyTracker
from simulation.environment import Environment
from simulation.generic_propulsion import GenericPropulsionCell, GenericPropulsionParams
from simulation.logger import SimulationLogger
from simulation.rigid_body import RigidBody6DOF, RigidBodyParams, RigidBodyState
from simulation.thermal import ThermalNode


@dataclass
class VehicleConfig:
    rigid_body_params: RigidBodyParams
    cell_specs: list[PropulsionCellSpec]
    environment: Environment = field(default_factory=Environment)
    propulsion_params: GenericPropulsionParams = field(default_factory=GenericPropulsionParams)


class Vehicle:
    """A simulated vehicle: rigid body + a set of propulsion cells + allocator."""

    def __init__(
        self, config: VehicleConfig, cells: list[PropulsionCellBase] | None = None
    ) -> None:
        self.config = config
        self.rigid_body = RigidBody6DOF(config.rigid_body_params)
        self.allocator = ThrustAllocator(config.cell_specs)
        self.cells = cells or [
            GenericPropulsionCell(spec, config.propulsion_params) for spec in config.cell_specs
        ]
        self._cells_by_id = {cell.spec.cell_id: cell for cell in self.cells}
        self.energy = EnergyTracker()
        self.thermal_nodes = {spec.cell_id: ThermalNode() for spec in config.cell_specs}
        self.logger = SimulationLogger()
        self.time_s = 0.0

    def step(self, desired_wrench: Wrench, dt: float) -> RigidBodyState:
        """Advance the simulation by ``dt`` seconds toward ``desired_wrench``."""
        allocation = self.allocator.allocate(desired_wrench)

        force_body_n = np.zeros(3)
        torque_body_n_m = np.zeros(3)
        values: dict[str, float] = {}

        for spec in self.config.cell_specs:
            cell = self._cells_by_id[spec.cell_id]
            cell.command(allocation.commands[spec.cell_id])
            state = cell.step(dt)

            thrust_vector_n = state.actual_thrust_n * spec.thrust_direction
            force_body_n += thrust_vector_n
            torque_body_n_m += np.cross(spec.position_m, thrust_vector_n)

            self.energy.accumulate(spec.cell_id, state.power_draw_w, dt)
            temperature_k = self.thermal_nodes[spec.cell_id].step(
                state.power_draw_w, self.config.environment.ambient_temperature_k, dt
            )

            values[f"{spec.cell_id}_thrust_n"] = state.actual_thrust_n
            values[f"{spec.cell_id}_power_w"] = state.power_draw_w
            values[f"{spec.cell_id}_temp_k"] = temperature_k

        new_state = self.rigid_body.step(
            force_body_n, torque_body_n_m, dt, self.config.environment.gravity_m_s2
        )
        self.time_s += dt

        total_power_w = sum(v for k, v in values.items() if k.endswith("_power_w"))
        values.update(
            pos_x_m=new_state.position_m[0],
            pos_y_m=new_state.position_m[1],
            pos_z_m=new_state.position_m[2],
            wrench_error_n=allocation.error.norm(),
            total_power_w=total_power_w,
        )
        self.logger.log(self.time_s, **values)
        return new_state

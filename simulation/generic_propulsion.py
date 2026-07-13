"""Idealized, technology-agnostic propulsion surrogate for early simulation.

Real propulsion technologies (``propulsion.cells``) are unimplemented by
design -- see propulsion/README or module docstrings. This module lets
flight control, rigid-body, and optimization studies proceed *now* by
modeling thrust response as a generic first-order lag with a configurable
pressure-loss derate and linear power-per-thrust scaling, all driven by
parameters rather than any specific hardware. Swap a real
``propulsion.cells`` plugin in once it exists; nothing above this layer
needs to change since both satisfy ``PropulsionCellBase``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from propulsion.base import (
    PropulsionCellBase,
    PropulsionCellSpec,
    PropulsionCommand,
    PropulsionState,
)


@dataclass
class GenericPropulsionParams:
    """Sweep-friendly parameters standing in for real propulsion characterization."""

    response_time_s: float = 0.05
    power_per_newton_w: float = 150.0
    pressure_loss_fraction: float = 0.0  # fraction of commanded thrust lost to ducting/plumbing


class GenericPropulsionCell(PropulsionCellBase):
    """First-order-lag propulsion surrogate driven purely by :class:`GenericPropulsionParams`."""

    def __init__(
        self, spec: PropulsionCellSpec, params: GenericPropulsionParams | None = None
    ) -> None:
        super().__init__(spec)
        self.params = params or GenericPropulsionParams()
        self._commanded_thrust_n = 0.0
        self._actual_thrust_n = 0.0

    def command(self, cmd: PropulsionCommand) -> None:
        self._commanded_thrust_n = cmd.thrust_fraction * self.spec.max_thrust_n

    def step(self, dt: float) -> PropulsionState:
        tau = max(self.params.response_time_s, 1e-9)
        alpha = 1.0 - np.exp(-dt / tau)
        target = self._commanded_thrust_n * (1.0 - self.params.pressure_loss_fraction)
        self._actual_thrust_n += alpha * (target - self._actual_thrust_n)
        power_w = self._actual_thrust_n * self.params.power_per_newton_w
        return PropulsionState(
            actual_thrust_n=self._actual_thrust_n,
            power_draw_w=power_w,
            mass_flow_kg_s=0.0,
            temperature_k=288.15,
        )

    def response_time_s(self) -> float:
        return self.params.response_time_s

    def rated_power_w(self) -> float:
        return self.spec.max_thrust_n * self.params.power_per_newton_w

    def reset(self) -> None:
        self._commanded_thrust_n = 0.0
        self._actual_thrust_n = 0.0

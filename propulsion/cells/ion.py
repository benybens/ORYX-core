"""Ion propulsion.

Included for architectural completeness and long-horizon research (e.g.
low-pressure/high-altitude regimes); not expected to be viable at
sea-level atmospheric density in the near term.

Open research questions (see docs/research_log.md):
    - Thrust density at atmospheric (vs. vacuum) pressure.
    - Power supply mass vs. achievable thrust-to-weight.

Not implemented: no physics is modeled yet.
"""

from __future__ import annotations

from propulsion.base import (
    PropulsionCellBase,
    PropulsionCellSpec,
    PropulsionCommand,
    PropulsionState,
)
from propulsion.registry import register


@register("ion")
class IonPropulsion(PropulsionCellBase):
    """Ion thruster cell (research placeholder)."""

    def __init__(self, spec: PropulsionCellSpec, beam_voltage_v: float = 1000.0) -> None:
        super().__init__(spec)
        self.beam_voltage_v = beam_voltage_v

    def command(self, cmd: PropulsionCommand) -> None:
        raise NotImplementedError("ion source command model not yet implemented")

    def step(self, dt: float) -> PropulsionState:
        raise NotImplementedError("ion thrust model not yet implemented")

    def response_time_s(self) -> float:
        raise NotImplementedError("ion source response time not yet characterized")

    def rated_power_w(self) -> float:
        raise NotImplementedError("ion source power draw not yet characterized")

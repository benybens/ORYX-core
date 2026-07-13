"""Combustion gas generator propulsion.

Open research questions (see docs/research_log.md):
    - Throttling range and response time of a small monopropellant/hybrid
      gas generator feeding a distributed nozzle array.
    - Thermal management of nozzles and adjacent structure.
    - Fuel/oxidizer mass fraction budget vs. mission duration.

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


@register("combustion")
class CombustionPropulsion(PropulsionCellBase):
    """Gas generator feeding one or more distributed nozzles."""

    def __init__(
        self,
        spec: PropulsionCellSpec,
        propellant_mass_kg: float = 1.0,
        chamber_pressure_pa: float = 1e6,
    ) -> None:
        super().__init__(spec)
        self._propellant_mass_kg = propellant_mass_kg
        self.chamber_pressure_pa = chamber_pressure_pa

    def command(self, cmd: PropulsionCommand) -> None:
        raise NotImplementedError("throttle valve model not yet implemented")

    def step(self, dt: float) -> PropulsionState:
        raise NotImplementedError("combustion/nozzle thrust model not yet implemented")

    def response_time_s(self) -> float:
        raise NotImplementedError("throttle response time not yet characterized")

    def rated_power_w(self) -> float:
        raise NotImplementedError("igniter/valve power draw not yet characterized")

    def propellant_mass_kg(self) -> float | None:
        return self._propellant_mass_kg

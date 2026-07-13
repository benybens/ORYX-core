"""Compressed gas / compressed CO2 propulsion (cold gas thruster).

Open research questions (see docs/research_log.md):
    - Tank pressure decay model as a function of draw rate and temperature.
    - Nozzle discharge coefficient and choked-flow regime transitions.
    - Regulator/valve response time as a function of duty cycle.

Not implemented: no physics is modeled yet. This class only fixes the
constructor signature and interface shape so flight control, simulation,
and CAD (propulsion interface mounts) can be developed against it before
the physics exists.
"""

from __future__ import annotations

from propulsion.base import (
    PropulsionCellBase,
    PropulsionCellSpec,
    PropulsionCommand,
    PropulsionState,
)
from propulsion.registry import register


@register("compressed_gas")
class CompressedGasPropulsion(PropulsionCellBase):
    """Cold gas thruster fed from a shared or local compressed gas reservoir."""

    def __init__(
        self,
        spec: PropulsionCellSpec,
        tank_volume_l: float = 1.0,
        tank_pressure_pa: float = 20e6,
        propellant: str = "N2",
    ) -> None:
        super().__init__(spec)
        self.tank_volume_l = tank_volume_l
        self.tank_pressure_pa = tank_pressure_pa
        self.propellant = propellant

    def command(self, cmd: PropulsionCommand) -> None:
        raise NotImplementedError("compressed gas valve/regulator model not yet implemented")

    def step(self, dt: float) -> PropulsionState:
        raise NotImplementedError("compressed gas flow/thrust model not yet implemented")

    def response_time_s(self) -> float:
        raise NotImplementedError("valve response time not yet characterized")

    def rated_power_w(self) -> float:
        raise NotImplementedError("valve/solenoid power draw not yet characterized")

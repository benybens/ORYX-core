"""Plasma / electrohydrodynamic (EHD) propulsion.

Open research questions (see docs/research_log.md):
    - Achievable thrust-to-power ratio at atmospheric pressure vs. altitude.
    - High-voltage supply mass and corona/arcing safety margins.
    - Ionic wind velocity profile and its coupling to airframe geometry.

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


@register("plasma")
class PlasmaPropulsion(PropulsionCellBase):
    """Electrohydrodynamic (corona wind) thrust cell."""

    def __init__(
        self,
        spec: PropulsionCellSpec,
        electrode_gap_m: float = 0.02,
        supply_voltage_v: float = 20000.0,
    ) -> None:
        super().__init__(spec)
        self.electrode_gap_m = electrode_gap_m
        self.supply_voltage_v = supply_voltage_v

    def command(self, cmd: PropulsionCommand) -> None:
        raise NotImplementedError("HV supply command model not yet implemented")

    def step(self, dt: float) -> PropulsionState:
        raise NotImplementedError("EHD thrust model not yet implemented")

    def response_time_s(self) -> float:
        raise NotImplementedError("HV supply response time not yet characterized")

    def rated_power_w(self) -> float:
        raise NotImplementedError("EHD power draw not yet characterized")

"""Electric ducted fan (EDF) propulsion, and the mounting point for future
ejector-amplified or fluidic-amplifier augmentation of a base EDF/fan stage.

Open research questions (see docs/research_log.md):
    - Motor/ESC torque-speed response as the latency-dominant term.
    - Duct + ejector amplification factor vs. mass/complexity tradeoff.
    - Battery C-rate limits under distributed multi-cell simultaneous demand.

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


@register("edf")
class EDFPropulsion(PropulsionCellBase):
    """Electric ducted fan cell, optionally with ejector/fluidic amplification."""

    def __init__(
        self,
        spec: PropulsionCellSpec,
        rated_power_w: float = 500.0,
        duct_diameter_m: float = 0.06,
        ejector_amplification: float = 1.0,
    ) -> None:
        super().__init__(spec)
        self._rated_power_w = rated_power_w
        self.duct_diameter_m = duct_diameter_m
        self.ejector_amplification = ejector_amplification

    def command(self, cmd: PropulsionCommand) -> None:
        raise NotImplementedError("motor/ESC command model not yet implemented")

    def step(self, dt: float) -> PropulsionState:
        raise NotImplementedError("fan aero/thrust model not yet implemented")

    def response_time_s(self) -> float:
        raise NotImplementedError("motor spool-up time not yet characterized")

    def rated_power_w(self) -> float:
        return self._rated_power_w

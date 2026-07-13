"""First-order lumped thermal model, independent of propulsion technology.

Each propulsion cell is treated as a single thermal mass exchanging heat
with the ambient environment by a linear conductance. This is a
placeholder precise enough to flag gross thermal design problems (e.g. a
cell that would clearly cook itself under sustained full thrust) without
requiring a technology-specific thermal model. Replace with a proper
transient FEA/CFD-informed model once a technology is selected and its
duty cycle is known (see docs/research_log.md).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ThermalParams:
    thermal_mass_j_per_k: float = 50.0
    ambient_conductance_w_per_k: float = 0.5


@dataclass
class ThermalNode:
    """Lumped thermal state of a single propulsion cell."""

    params: ThermalParams = field(default_factory=ThermalParams)
    temperature_k: float = 288.15

    def step(self, heat_input_w: float, ambient_temperature_k: float, dt: float) -> float:
        heat_loss_w = self.params.ambient_conductance_w_per_k * (
            self.temperature_k - ambient_temperature_k
        )
        d_temperature_k = (heat_input_w - heat_loss_w) / self.params.thermal_mass_j_per_k * dt
        self.temperature_k += d_temperature_k
        return self.temperature_k

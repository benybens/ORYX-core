"""Energy consumption tracking, independent of propulsion technology.

Integrates whatever ``power_draw_w`` each cell's :class:`~propulsion.base.PropulsionState`
reports -- it does not care whether that power is electrical, or a proxy
for propellant chemical energy.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EnergyTracker:
    """Accumulates energy draw per cell and in total over a simulation run."""

    energy_j_by_cell: dict[str, float] = field(default_factory=dict)

    def accumulate(self, cell_id: str, power_draw_w: float, dt: float) -> None:
        self.energy_j_by_cell[cell_id] = self.energy_j_by_cell.get(cell_id, 0.0) + power_draw_w * dt

    @property
    def total_energy_j(self) -> float:
        return sum(self.energy_j_by_cell.values())

    def total_energy_wh(self) -> float:
        return self.total_energy_j / 3600.0

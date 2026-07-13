"""Generic objective/metric helpers for sweep evaluation.

These operate on plain numbers so they apply regardless of propulsion
technology or vehicle configuration -- they are the shared vocabulary a
sweep's ``objective_fn`` reports back through
:class:`optimization.sweep.SweepResult.metrics`.
"""

from __future__ import annotations

GRAVITY_M_S2 = 9.80665


def thrust_to_weight_ratio(total_max_thrust_n: float, mass_kg: float) -> float:
    if mass_kg <= 0:
        raise ValueError("mass_kg must be positive")
    return total_max_thrust_n / (mass_kg * GRAVITY_M_S2)


def specific_energy_wh_per_kg(energy_wh: float, propellant_or_battery_mass_kg: float) -> float:
    if propellant_or_battery_mass_kg <= 0:
        raise ValueError("propellant_or_battery_mass_kg must be positive")
    return energy_wh / propellant_or_battery_mass_kg


def hover_endurance_s(energy_capacity_wh: float, hover_power_w: float) -> float:
    if hover_power_w <= 0:
        raise ValueError("hover_power_w must be positive")
    return energy_capacity_wh * 3600.0 / hover_power_w

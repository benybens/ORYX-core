"""Ambient environment model, decoupled from vehicle and propulsion state."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Environment:
    """Ambient conditions the vehicle operates in.

    Deliberately simplistic (constant, uniform field) for now -- this is
    the seam where a future atmosphere/wind/turbulence model, or a CFD
    coupling, would plug in without changing any other simulation code.
    """

    gravity_m_s2: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 9.80665]))
    air_density_kg_m3: float = 1.225
    ambient_temperature_k: float = 288.15
    ambient_pressure_pa: float = 101_325.0

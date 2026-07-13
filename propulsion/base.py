"""Technology-agnostic propulsion cell interface.

Every propulsion technology ORYX ever tries -- compressed gas, EDF, plasma,
combustion gas generator, ion, ejector amplification, fluidic amplifiers, or
whatever comes after -- must be expressible through this interface and
nothing more. If a new technology needs to add a method here, that is a sign
the abstraction is leaking hardware-specific assumptions and should be
reconsidered.

Design rule: nothing outside ``propulsion/`` may import a concrete cell
implementation directly. Flight control, simulation, and optimization only
ever see ``PropulsionCellBase``, ``PropulsionCellSpec``, ``PropulsionCommand``,
and ``PropulsionState``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass
class PropulsionCellSpec:
    """Static configuration of a single propulsion cell mounted on the hull.

    Positions and directions are expressed in the vehicle body frame
    (origin at center of mass, +X forward, +Y right, +Z down), which is the
    same frame the flight control allocator and rigid body simulation use.
    This is the one piece of geometry every propulsion technology and every
    consumer of this module must agree on.
    """

    cell_id: str
    position_m: np.ndarray  # shape (3,): mounting position in body frame
    thrust_direction: np.ndarray  # shape (3,): unit vector, thrust direction in body frame
    max_thrust_n: float
    min_thrust_n: float = 0.0
    dry_mass_kg: float = 0.0
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.position_m = np.asarray(self.position_m, dtype=float).reshape(3)
        direction = np.asarray(self.thrust_direction, dtype=float).reshape(3)
        norm = np.linalg.norm(direction)
        if norm == 0:
            raise ValueError(f"cell {self.cell_id!r}: thrust_direction must be nonzero")
        self.thrust_direction = direction / norm
        if self.max_thrust_n <= 0:
            raise ValueError(f"cell {self.cell_id!r}: max_thrust_n must be positive")
        if self.min_thrust_n < 0 or self.min_thrust_n > self.max_thrust_n:
            raise ValueError(f"cell {self.cell_id!r}: min_thrust_n out of range")


@dataclass
class PropulsionCommand:
    """Command issued to a cell by the flight control allocator.

    ``thrust_fraction`` is normalized to [0, 1] of ``max_thrust_n`` so the
    allocator never needs to know how a fraction maps to a valve position,
    a voltage, or a mixture ratio -- that mapping is entirely internal to
    each propulsion technology.
    """

    thrust_fraction: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.thrust_fraction <= 1.0:
            raise ValueError("thrust_fraction must be within [0, 1]")


@dataclass
class PropulsionState:
    """Technology-agnostic measured/estimated state of a cell.

    Every field is something the simulation, energy model, and thermal
    model can consume without knowing which technology produced it. A
    technology that has no meaningful value for a field (e.g. an ion
    thruster has no ``mass_flow_kg_s`` in the combustion sense) reports 0.0
    rather than omitting the field, so downstream code never has to
    special-case missing data.
    """

    actual_thrust_n: float
    power_draw_w: float
    mass_flow_kg_s: float
    temperature_k: float
    propellant_remaining_kg: float | None = None


class PropulsionCellBase(ABC):
    """Base class every propulsion technology plugin must implement.

    Lifecycle per simulation/control step:

    1. ``command(cmd)`` records the desired thrust fraction.
    2. ``step(dt)`` advances the cell's internal state by ``dt`` seconds,
       honoring whatever latency/lag/spool-up physics the technology has,
       and returns the resulting :class:`PropulsionState`.

    Splitting command from step lets the simulation model propulsion
    latency uniformly across technologies (see ``simulation.propulsion_model``)
    without every plugin re-implementing its own latency handling -- though
    a plugin is free to add additional internal latency on top.
    """

    def __init__(self, spec: PropulsionCellSpec) -> None:
        self.spec = spec

    @abstractmethod
    def command(self, cmd: PropulsionCommand) -> None:
        """Record a new commanded thrust fraction for the next ``step``."""

    @abstractmethod
    def step(self, dt: float) -> PropulsionState:
        """Advance internal state by ``dt`` seconds and report the result."""

    @abstractmethod
    def response_time_s(self) -> float:
        """Characteristic time constant (s) from command to ~63% of commanded thrust."""

    @abstractmethod
    def rated_power_w(self) -> float:
        """Peak electrical/other power draw (W) at max commanded thrust."""

    def propellant_mass_kg(self) -> float | None:
        """Remaining onboard propellant mass, or ``None`` if not propellant-limited."""
        return None

    def reset(self) -> None:  # noqa: B027 - intentional no-op default, not required to override
        """Reset internal state to a cold/idle condition. Override as needed."""

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{type(self).__name__}(cell_id={self.spec.cell_id!r})"

"""Body-frame force/torque wrench used as the flight controller's I/O contract."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Wrench:
    """A 6-DOF force + torque demand or measurement, in the vehicle body frame."""

    fx: float = 0.0
    fy: float = 0.0
    fz: float = 0.0
    mx: float = 0.0
    my: float = 0.0
    mz: float = 0.0

    def as_vector(self) -> np.ndarray:
        return np.array([self.fx, self.fy, self.fz, self.mx, self.my, self.mz], dtype=float)

    @classmethod
    def from_vector(cls, vec: np.ndarray) -> Wrench:
        vec = np.asarray(vec, dtype=float).reshape(6)
        return cls(*vec.tolist())

    def __sub__(self, other: Wrench) -> Wrench:
        return Wrench.from_vector(self.as_vector() - other.as_vector())

    def norm(self) -> float:
        return float(np.linalg.norm(self.as_vector()))

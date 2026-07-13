"""Generic 6-DOF rigid body dynamics.

Frame convention: body frame is +X forward, +Y right, +Z down, origin at
the center of mass -- the same convention used by
``propulsion.base.PropulsionCellSpec`` and ``flight_control``. World frame
is a fixed inertial frame with +Z down (gravity positive along +Z).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial.transform import Rotation


@dataclass
class RigidBodyParams:
    """Mass properties of the vehicle. Center of mass is the body-frame origin."""

    mass_kg: float
    inertia_kg_m2: np.ndarray  # 3x3 body-frame inertia tensor


@dataclass
class RigidBodyState:
    """Instantaneous kinematic state of the vehicle."""

    position_m: np.ndarray  # world frame
    velocity_m_s: np.ndarray  # world frame
    orientation: Rotation  # body-to-world rotation
    angular_velocity_rad_s: np.ndarray  # body frame


def initial_state() -> RigidBodyState:
    return RigidBodyState(
        position_m=np.zeros(3),
        velocity_m_s=np.zeros(3),
        orientation=Rotation.identity(),
        angular_velocity_rad_s=np.zeros(3),
    )


class RigidBody6DOF:
    """Semi-implicit Euler integrator for a rigid body under body-frame force/torque.

    Semi-implicit (symplectic) Euler is used rather than RK4 for its
    stability with the fixed, typically small simulation step sizes used
    for control-loop-rate studies, and because it keeps the integrator
    trivially cheap for large parameter sweeps. Swap in a higher-order
    integrator here if sweep results show integration error dominating.
    """

    def __init__(self, params: RigidBodyParams, state: RigidBodyState | None = None) -> None:
        self.params = params
        self.state = state or initial_state()
        self._inertia_inv = np.linalg.inv(params.inertia_kg_m2)

    def step(
        self,
        force_body_n: np.ndarray,
        torque_body_n_m: np.ndarray,
        dt: float,
        gravity_m_s2: np.ndarray,
    ) -> RigidBodyState:
        """Advance the state by ``dt`` seconds under a constant body-frame wrench."""
        s = self.state
        force_world = s.orientation.apply(force_body_n) + self.params.mass_kg * gravity_m_s2
        accel_world = force_world / self.params.mass_kg

        omega = s.angular_velocity_rad_s
        gyroscopic = np.cross(omega, self.params.inertia_kg_m2 @ omega)
        angular_accel = self._inertia_inv @ (torque_body_n_m - gyroscopic)

        new_velocity = s.velocity_m_s + accel_world * dt
        new_position = s.position_m + new_velocity * dt
        new_omega = omega + angular_accel * dt
        new_orientation = s.orientation * Rotation.from_rotvec(new_omega * dt)

        self.state = RigidBodyState(
            position_m=new_position,
            velocity_m_s=new_velocity,
            orientation=new_orientation,
            angular_velocity_rad_s=new_omega,
        )
        return self.state

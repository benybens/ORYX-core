"""Tests for generic 6-DOF rigid body dynamics."""

from __future__ import annotations

import numpy as np

from simulation.rigid_body import RigidBody6DOF, RigidBodyParams


def _params() -> RigidBodyParams:
    return RigidBodyParams(mass_kg=1.0, inertia_kg_m2=np.eye(3) * 0.01)


def test_free_fall_matches_kinematics():
    body = RigidBody6DOF(_params())
    gravity = np.array([0.0, 0.0, 9.80665])
    dt = 0.01
    steps = 100
    for _ in range(steps):
        body.step(np.zeros(3), np.zeros(3), dt, gravity)

    t = dt * steps
    expected_velocity_z = gravity[2] * t
    assert np.isclose(body.state.velocity_m_s[2], expected_velocity_z, rtol=1e-3)
    assert body.state.position_m[2] > 0  # fell downward (+Z)


def test_thrust_balances_gravity_at_hover():
    params = _params()
    body = RigidBody6DOF(params)
    gravity = np.array([0.0, 0.0, 9.80665])
    hover_force = np.array([0.0, 0.0, -params.mass_kg * gravity[2]])
    dt = 0.01
    for _ in range(50):
        body.step(hover_force, np.zeros(3), dt, gravity)

    assert np.allclose(body.state.velocity_m_s, 0.0, atol=1e-9)
    assert np.allclose(body.state.position_m, 0.0, atol=1e-9)


def test_torque_induces_angular_velocity():
    body = RigidBody6DOF(_params())
    torque = np.array([0.01, 0.0, 0.0])
    body.step(np.zeros(3), torque, 0.1, np.zeros(3))
    assert body.state.angular_velocity_rad_s[0] > 0
    assert np.isclose(body.state.angular_velocity_rad_s[1], 0.0, atol=1e-9)

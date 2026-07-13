"""Hardware-independent simulation of the vehicle's rigid body dynamics,
propulsion latency/losses, energy consumption, and thermal state.

Nothing in this package imports a concrete propulsion technology from
``propulsion.cells``. Where a propulsion model is needed but no
technology-specific plugin exists yet, use
:class:`simulation.generic_propulsion.GenericPropulsionCell` -- an
idealized, parametrized surrogate for early-stage control and optimization
studies.
"""

from simulation.environment import Environment
from simulation.rigid_body import RigidBody6DOF, RigidBodyParams, RigidBodyState
from simulation.vehicle import Vehicle, VehicleConfig

__all__ = [
    "Environment",
    "RigidBody6DOF",
    "RigidBodyParams",
    "RigidBodyState",
    "Vehicle",
    "VehicleConfig",
]

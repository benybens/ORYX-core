"""Parameter sweep and design-space exploration framework.

Every design parameter (hull geometry, nozzle layout, mass, pressure,
battery/fuel, center of gravity, ...) is exposed as a
:class:`~optimization.parameter_space.ParameterSpec` and swept via
:class:`~optimization.sweep.SweepRunner`, which is agnostic to what the
underlying config object or objective function actually model.
"""

from optimization.parameter_space import ParameterSpace, ParameterSpec
from optimization.sweep import SweepResult, SweepRunner

__all__ = ["ParameterSpace", "ParameterSpec", "SweepResult", "SweepRunner"]

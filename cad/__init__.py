"""Parametric CAD generation (CadQuery-based).

Every geometry generator here takes a dataclass from :mod:`cad.parameters`
and returns a cadquery solid/assembly -- there are no hardcoded dimensions.
``cadquery`` itself is an optional dependency (see ``cad._cq``); import
this package freely even where cadquery is not installed, but calling any
``build_*`` function without it installed raises a clear ``RuntimeError``.
"""

from cad.parameters import VehicleParameters

__all__ = ["VehicleParameters"]

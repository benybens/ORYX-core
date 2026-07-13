"""Propulsion plugin framework.

This package defines the technology-agnostic propulsion interface
(:mod:`propulsion.base`) and a plugin registry (:mod:`propulsion.registry`)
that concrete propulsion technologies register themselves against.

No propulsion technology is implemented here. See ``propulsion/cells`` for
skeletons that define the *shape* of each future implementation without
committing to its physics.
"""

from propulsion.base import (
    PropulsionCellBase,
    PropulsionCellSpec,
    PropulsionCommand,
    PropulsionState,
)
from propulsion.registry import available, create, get, register

__all__ = [
    "PropulsionCellBase",
    "PropulsionCellSpec",
    "PropulsionCommand",
    "PropulsionState",
    "available",
    "create",
    "get",
    "register",
]

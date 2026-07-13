"""Generic, propulsion-technology-agnostic thrust allocation framework.

Given a desired body-frame wrench (force + torque), :class:`ThrustAllocator`
computes a per-cell command using only cell geometry (position + thrust
direction) and saturation limits from :class:`propulsion.base.PropulsionCellSpec`.
It never inspects *which* propulsion technology a cell uses.
"""

from flight_control.allocator import AllocationResult, ThrustAllocator
from flight_control.wrench import Wrench

__all__ = ["AllocationResult", "ThrustAllocator", "Wrench"]

"""Generic thrust allocation: desired wrench -> per-cell propulsion commands.

The allocator only needs each cell's mounting position, thrust direction,
and thrust limits (:class:`propulsion.base.PropulsionCellSpec`). It is
deliberately ignorant of propulsion technology: a fleet of compressed-gas
cells, EDFs, or a mix of both are allocated identically.

Method: build a 6xN effectiveness matrix ``B`` where column ``i`` is the
wrench produced by 1 N of thrust from cell ``i``:

    B[:, i] = [ thrust_direction_i ; position_i x thrust_direction_i ]

Allocation solves the linear least-squares problem ``min ||B x - w||`` via
the (optionally weighted) Moore-Penrose pseudo-inverse of ``B``, then clips
each cell's thrust to its ``[min_thrust_n, max_thrust_n]`` range. This is a
standard control-allocation approach (cf. marine/aerospace thruster
allocation literature) chosen specifically because it has no dependency on
actuator physics -- only geometry.

Known limitation, tracked as a research item (docs/research_log.md): naive
clipping after the pseudo-inverse solve does not redistribute unmet demand
to non-saturated cells. A redistributed/weighted or QP-based allocator is a
likely future replacement once real saturation behavior matters; this
version exists to unblock end-to-end simulation now.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from flight_control.wrench import Wrench
from propulsion.base import PropulsionCellSpec, PropulsionCommand


@dataclass
class AllocationResult:
    """Output of one allocation solve."""

    commands: dict[str, PropulsionCommand]  # keyed by cell_id
    requested_wrench: Wrench
    achieved_wrench: Wrench  # wrench actually produced after saturation
    thrust_n: dict[str, float]  # unsaturated-solve thrust per cell, before clipping
    saturated_cells: list[str]

    @property
    def error(self) -> Wrench:
        return self.requested_wrench - self.achieved_wrench


class ThrustAllocator:
    """Maps a desired :class:`Wrench` to per-cell :class:`PropulsionCommand`."""

    def __init__(
        self, cell_specs: list[PropulsionCellSpec], weights: np.ndarray | None = None
    ) -> None:
        if not cell_specs:
            raise ValueError("ThrustAllocator requires at least one propulsion cell")
        self.cell_specs = list(cell_specs)
        self._ids = [spec.cell_id for spec in self.cell_specs]
        self.effectiveness_matrix = self._build_effectiveness_matrix()
        self._pinv = self._build_pseudo_inverse(weights)

    def _build_effectiveness_matrix(self) -> np.ndarray:
        columns = []
        for spec in self.cell_specs:
            force = spec.thrust_direction
            moment = np.cross(spec.position_m, spec.thrust_direction)
            columns.append(np.concatenate([force, moment]))
        return np.stack(columns, axis=1)  # shape (6, N)

    def _build_pseudo_inverse(self, weights: np.ndarray | None) -> np.ndarray:
        b = self.effectiveness_matrix
        if weights is None:
            return np.linalg.pinv(b)
        w = np.asarray(weights, dtype=float)
        if w.shape != (len(self.cell_specs),):
            raise ValueError(f"weights must have shape ({len(self.cell_specs)},)")
        w_inv = np.diag(1.0 / w)
        # Weighted pseudo-inverse: favors low-weight (e.g. lower-cost) cells.
        return w_inv @ b.T @ np.linalg.pinv(b @ w_inv @ b.T)

    def allocate(self, wrench: Wrench) -> AllocationResult:
        """Solve for per-cell thrust and saturate to each cell's limits."""
        w = wrench.as_vector()
        thrust_n = self._pinv @ w

        clipped = np.empty_like(thrust_n)
        saturated = []
        for i, spec in enumerate(self.cell_specs):
            lo, hi = spec.min_thrust_n, spec.max_thrust_n
            clipped[i] = np.clip(thrust_n[i], lo, hi)
            if thrust_n[i] < lo or thrust_n[i] > hi:
                saturated.append(spec.cell_id)

        achieved = self.effectiveness_matrix @ clipped

        commands = {}
        thrust_n_map = {}
        for i, spec in enumerate(self.cell_specs):
            fraction = 0.0 if spec.max_thrust_n == 0 else float(clipped[i] / spec.max_thrust_n)
            commands[spec.cell_id] = PropulsionCommand(thrust_fraction=fraction)
            thrust_n_map[spec.cell_id] = float(thrust_n[i])

        return AllocationResult(
            commands=commands,
            requested_wrench=wrench,
            achieved_wrench=Wrench.from_vector(achieved),
            thrust_n=thrust_n_map,
            saturated_cells=saturated,
        )

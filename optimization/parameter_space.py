"""Sweepable parameter space definition, addressed by dotted attribute path.

Deliberately generic: a :class:`ParameterSpace` doesn't know or care
whether it's sweeping CAD dimensions (``cad.parameters.VehicleParameters``),
propulsion surrogate parameters (``simulation.generic_propulsion.GenericPropulsionParams``),
or anything else -- it only needs attribute paths and candidate values.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from itertools import product
from typing import Any

import numpy as np


@dataclass
class ParameterSpec:
    """One sweepable design variable.

    ``path`` is a dotted attribute path resolved against the base config
    object, e.g. ``"hull.length_m"`` for ``VehicleParameters.hull.length_m``.
    """

    path: str
    values: list[Any]


@dataclass
class ParameterSpace:
    specs: list[ParameterSpec] = field(default_factory=list)

    def grid(self) -> list[dict[str, Any]]:
        """Full factorial grid: every combination of every spec's values."""
        if not self.specs:
            return [{}]
        paths = [spec.path for spec in self.specs]
        combinations = product(*(spec.values for spec in self.specs))
        return [dict(zip(paths, combo, strict=True)) for combo in combinations]

    def random_sample(self, n: int, rng: np.random.Generator | None = None) -> list[dict[str, Any]]:
        """``n`` random points, each parameter drawn independently and uniformly from its values."""
        rng = rng if rng is not None else np.random.default_rng()
        samples = []
        for _ in range(n):
            sample = {}
            for spec in self.specs:
                index = int(rng.integers(0, len(spec.values)))
                sample[spec.path] = spec.values[index]
            samples.append(sample)
        return samples


def set_by_path(obj: Any, path: str, value: Any) -> None:
    """Set a (possibly nested) attribute on ``obj`` given a dotted path."""
    parts = path.split(".")
    target = obj
    for part in parts[:-1]:
        target = getattr(target, part)
    setattr(target, parts[-1], value)


def apply_values(obj: Any, values: dict[str, Any]) -> Any:
    """Return a deep copy of ``obj`` with each dotted-path value applied."""
    new_obj = copy.deepcopy(obj)
    for path, value in values.items():
        set_by_path(new_obj, path, value)
    return new_obj

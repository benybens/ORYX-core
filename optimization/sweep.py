"""Parameter sweep runner.

Evaluates a caller-supplied ``objective_fn`` at every point in a
:class:`~optimization.parameter_space.ParameterSpace`, over a grid or a
random sample, and produces a results table. This is the engine behind
"automatic parameter sweeps" (mass, hull dimensions, nozzle count/angle,
pressure, etc.) -- it holds no domain knowledge itself, since that lives
in whatever ``objective_fn`` (typically a simulation run) is passed in.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from optimization.parameter_space import ParameterSpace, apply_values


@dataclass
class SweepResult:
    values: dict[str, Any]
    metrics: dict[str, float]


class SweepRunner:
    """Evaluates ``objective_fn(config)`` across a :class:`ParameterSpace`."""

    def __init__(
        self,
        base_config: Any,
        space: ParameterSpace,
        objective_fn: Callable[[Any], dict[str, float]],
    ) -> None:
        self.base_config = base_config
        self.space = space
        self.objective_fn = objective_fn

    def run_grid(self) -> list[SweepResult]:
        return self._run(self.space.grid())

    def run_random(self, n: int, rng: np.random.Generator | None = None) -> list[SweepResult]:
        return self._run(self.space.random_sample(n, rng))

    def _run(self, points: list[dict[str, Any]]) -> list[SweepResult]:
        results = []
        for values in points:
            config = apply_values(self.base_config, values)
            metrics = self.objective_fn(config)
            results.append(SweepResult(values=values, metrics=metrics))
        return results

    @staticmethod
    def to_dataframe(results: list[SweepResult]) -> pd.DataFrame:
        return pd.DataFrame([{**r.values, **r.metrics} for r in results])

    @staticmethod
    def save(results: list[SweepResult], path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        SweepRunner.to_dataframe(results).to_csv(path, index=False)

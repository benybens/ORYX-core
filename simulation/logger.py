"""Timeseries data logging for simulation runs.

Every experiment must produce measurable engineering data (see
docs/research_log.md and experiments/README.md) -- this is the shared
mechanism simulation, optimization sweeps, and (eventually) hardware
telemetry all funnel through so results are comparable across runs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass
class SimulationLogger:
    """Collects one row of named scalar values per simulation step."""

    _rows: list[dict] = field(default_factory=list)

    def log(self, time_s: float, **values: float) -> None:
        self._rows.append({"time_s": time_s, **values})

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self._rows)

    def to_csv(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.to_dataframe().to_csv(path, index=False)

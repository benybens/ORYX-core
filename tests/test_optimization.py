"""Tests for the parameter sweep framework."""

from __future__ import annotations

from dataclasses import dataclass

from optimization.parameter_space import ParameterSpace, ParameterSpec, apply_values, set_by_path
from optimization.sweep import SweepRunner


@dataclass
class _Inner:
    value: float = 1.0


@dataclass
class _Config:
    inner: _Inner
    scale: float = 2.0


def test_grid_produces_full_factorial():
    space = ParameterSpace(specs=[ParameterSpec("a", [1, 2]), ParameterSpec("b", [10, 20, 30])])
    grid = space.grid()
    assert len(grid) == 6
    assert {"a": 1, "b": 10} in grid


def test_random_sample_count_and_membership():
    space = ParameterSpace(specs=[ParameterSpec("a", [1, 2, 3])])
    samples = space.random_sample(5)
    assert len(samples) == 5
    assert all(s["a"] in {1, 2, 3} for s in samples)


def test_set_by_path_nested_attribute():
    config = _Config(inner=_Inner())
    set_by_path(config, "inner.value", 42.0)
    assert config.inner.value == 42.0


def test_apply_values_does_not_mutate_base():
    base = _Config(inner=_Inner())
    updated = apply_values(base, {"inner.value": 5.0, "scale": 9.0})
    assert base.inner.value == 1.0
    assert updated.inner.value == 5.0
    assert updated.scale == 9.0


def test_sweep_runner_grid_evaluates_all_points():
    base = _Config(inner=_Inner())
    space = ParameterSpace(specs=[ParameterSpec("inner.value", [1.0, 2.0, 3.0])])

    def objective(config: _Config) -> dict[str, float]:
        return {"doubled": config.inner.value * config.scale}

    runner = SweepRunner(base, space, objective)
    results = runner.run_grid()
    assert len(results) == 3
    df = SweepRunner.to_dataframe(results)
    assert set(df["doubled"]) == {2.0, 4.0, 6.0}

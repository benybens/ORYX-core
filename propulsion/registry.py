"""Plugin registry for propulsion technologies.

Concrete propulsion technologies register themselves with :func:`register`
and are instantiated by name via :func:`create`. This is the only supported
way to construct a propulsion cell outside of tests -- callers should never
import a concrete cell class directly, so that swapping propulsion
technology is a config change, not a code change.
"""

from __future__ import annotations

from propulsion.base import PropulsionCellBase, PropulsionCellSpec

_REGISTRY: dict[str, type[PropulsionCellBase]] = {}


def register(name: str):
    """Class decorator registering a :class:`PropulsionCellBase` subclass under ``name``."""

    def decorator(cls: type[PropulsionCellBase]) -> type[PropulsionCellBase]:
        if not issubclass(cls, PropulsionCellBase):
            raise TypeError(f"{cls!r} must subclass PropulsionCellBase to be registered")
        if name in _REGISTRY and _REGISTRY[name] is not cls:
            raise ValueError(
                f"propulsion technology {name!r} is already registered to {_REGISTRY[name]!r}"
            )
        _REGISTRY[name] = cls
        return cls

    return decorator


def get(name: str) -> type[PropulsionCellBase]:
    """Look up a registered propulsion cell class by name."""
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(
            f"unknown propulsion technology {name!r}; available: {sorted(_REGISTRY)}"
        ) from exc


def create(name: str, spec: PropulsionCellSpec, **kwargs) -> PropulsionCellBase:
    """Instantiate a registered propulsion cell by technology name."""
    return get(name)(spec, **kwargs)


def available() -> list[str]:
    """List all registered propulsion technology names."""
    return sorted(_REGISTRY)

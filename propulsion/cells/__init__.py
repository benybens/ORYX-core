"""Concrete propulsion technology plugins.

Importing this package registers every plugin defined in it (each module
below calls :func:`propulsion.registry.register` at import time). No physics
is implemented yet -- see each module's docstring for what remains open.

Usage::

    import propulsion.cells  # noqa: F401  (registers all plugins)
    from propulsion import create, available

    print(available())
    cell = create("compressed_gas", spec)
"""

from propulsion.cells import (  # noqa: F401
    combustion,
    compressed_gas,
    edf,
    ion,
    plasma,
)

__all__ = ["combustion", "compressed_gas", "edf", "ion", "plasma"]

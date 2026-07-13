"""Internal shim isolating the optional ``cadquery`` dependency.

cadquery ships prebuilt OpenCascade (OCP) bindings that are far more
reliable via conda (see ``environment.yml``) than pip, so it is kept
optional (``pip install -e ".[cad]"`` or the conda environment) rather
than a hard dependency of the rest of ORYX. Every public ``cad.*`` build
function calls :func:`require_cadquery` first so a missing install fails
with a clear message instead of an ``ImportError`` deep inside a loft.
"""

from __future__ import annotations

try:
    import cadquery as cq
except ImportError:  # pragma: no cover - exercised only when cadquery is absent
    cq = None  # type: ignore[assignment]


def require_cadquery() -> None:
    if cq is None:  # pragma: no cover - exercised only when cadquery is absent
        raise RuntimeError(
            "cadquery is required for CAD generation but is not installed. "
            "Install it via `conda env create -f environment.yml` (recommended) "
            "or `pip install -e '.[cad]'`."
        )

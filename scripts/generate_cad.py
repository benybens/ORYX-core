"""Generate the default parametric vehicle CAD assembly and export STEP/STL.

Requires cadquery -- see environment.yml (conda, recommended) or
`pip install -e ".[cad]"`.

Run with: python scripts/generate_cad.py
"""

from __future__ import annotations

from pathlib import Path

from cad.build import build_vehicle, export_step, export_stl
from cad.parameters import VehicleParameters

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "cad" / "output"


def main() -> None:
    params = VehicleParameters()
    assembly = build_vehicle(params)

    export_step(assembly, OUTPUT_DIR / "vehicle.step")
    export_stl(assembly, OUTPUT_DIR / "vehicle.stl")
    print(f"Exported vehicle CAD to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

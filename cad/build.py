"""Assembles hull, plenum, nozzle array, channels, ribs, mounts, and
propulsion interfaces from one :class:`~cad.parameters.VehicleParameters`
into a single cadquery Assembly, and exports it to STEP/STL.
"""

from __future__ import annotations

from pathlib import Path

from cad._cq import cq, require_cadquery
from cad.channels import build_channels
from cad.electronics_mounts import build_electronics_mount
from cad.hull import build_hull
from cad.nozzle_array import build_nozzle_bores, nozzle_poses
from cad.parameters import VehicleParameters
from cad.propulsion_interface import build_propulsion_interfaces
from cad.ribs import build_ribs

OUTPUT_DIR = Path(__file__).parent / "output"


def build_vehicle(params: VehicleParameters):
    """Return a cadquery Assembly of the full parametric vehicle."""
    require_cadquery()

    poses = nozzle_poses(params.hull, params.nozzles)
    plenum_center_m = [0.0, 0.0, params.hull.length_m / 2.0]

    hull = build_hull(params.hull).cut(build_nozzle_bores(params.hull, params.nozzles))
    ribs = build_ribs(params.hull, params.ribs)
    channels = build_channels(plenum_center_m, poses, params.channels)
    mount = build_electronics_mount(params.electronics_mount)
    interfaces = build_propulsion_interfaces(poses, params.propulsion_interface)

    assembly = cq.Assembly()
    assembly.add(hull, name="hull")
    assembly.add(ribs, name="ribs")
    assembly.add(channels, name="channels")
    assembly.add(mount, name="electronics_mount")
    assembly.add(interfaces, name="propulsion_interfaces")
    return assembly


def export_step(assembly, path: str | Path) -> None:
    require_cadquery()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    assembly.save(str(path))


def export_stl(assembly, path: str | Path, tolerance: float = 1e-3) -> None:
    require_cadquery()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    combined = assembly.toCompound()
    cq.exporters.export(combined, str(path), tolerance=tolerance)

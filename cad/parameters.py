"""Parametric design variables for every CAD subsystem.

Every dimension ORYX's CAD generates traces back to a field here. This is
also the schema the optimization sweep framework (``optimization/``) reads
and writes -- a sweep is nothing more than instantiating many
:class:`VehicleParameters` and calling ``cad.build.build_vehicle`` on each.

All units are SI (meters, radians unless suffixed ``_deg``, kilograms).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class HullParameters:
    """Outer monocoque shell, modeled as an ellipsoid-of-revolution."""

    length_m: float = 0.6
    max_diameter_m: float = 0.3
    wall_thickness_m: float = 0.003


@dataclass
class PlenumParameters:
    """Internal pressure vessel that distributes propulsion fluid to nozzles."""

    volume_l: float = 2.0
    wall_thickness_m: float = 0.002
    radial_standoff_m: float = 0.02  # gap from plenum wall to inner hull wall


@dataclass
class NozzleArrayParameters:
    """Distributed nozzle ring, technology-agnostic (bore geometry only)."""

    count: int = 8
    diameter_m: float = 0.012
    cant_angle_deg: float = 15.0
    band_latitude_deg: float = 0.0  # 0 = hull equator, +90 = nose, -90 = tail


@dataclass
class ChannelParameters:
    """Feed channels connecting the plenum to each nozzle."""

    diameter_m: float = 0.008
    wall_thickness_m: float = 0.0015


@dataclass
class RibParameters:
    """Radial structural ribs stiffening the hull shell."""

    count: int = 6
    thickness_m: float = 0.004
    height_m: float = 0.05


@dataclass
class ElectronicsMountParameters:
    """Standoff plate for avionics/battery/flight controller stack."""

    plate_diameter_m: float = 0.08
    plate_thickness_m: float = 0.003
    standoff_height_m: float = 0.02
    standoff_count: int = 4


@dataclass
class PropulsionInterfaceParameters:
    """Generic bolt-circle mounting interface every propulsion module attaches to.

    This is the mechanical contract between the airframe and *any*
    propulsion technology -- deliberately as simple as a bolt circle and a
    flange face so it never has to change when the propulsion technology
    behind it does.
    """

    bolt_circle_diameter_m: float = 0.03
    bolt_count: int = 4
    bolt_hole_diameter_m: float = 0.003
    flange_thickness_m: float = 0.004


@dataclass
class VehicleParameters:
    """Full parametric design vector for one vehicle configuration."""

    hull: HullParameters = field(default_factory=HullParameters)
    plenum: PlenumParameters = field(default_factory=PlenumParameters)
    nozzles: NozzleArrayParameters = field(default_factory=NozzleArrayParameters)
    channels: ChannelParameters = field(default_factory=ChannelParameters)
    ribs: RibParameters = field(default_factory=RibParameters)
    electronics_mount: ElectronicsMountParameters = field(
        default_factory=ElectronicsMountParameters
    )
    propulsion_interface: PropulsionInterfaceParameters = field(
        default_factory=PropulsionInterfaceParameters
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VehicleParameters:
        return cls(
            hull=HullParameters(**data.get("hull", {})),
            plenum=PlenumParameters(**data.get("plenum", {})),
            nozzles=NozzleArrayParameters(**data.get("nozzles", {})),
            channels=ChannelParameters(**data.get("channels", {})),
            ribs=RibParameters(**data.get("ribs", {})),
            electronics_mount=ElectronicsMountParameters(**data.get("electronics_mount", {})),
            propulsion_interface=PropulsionInterfaceParameters(
                **data.get("propulsion_interface", {})
            ),
        )

    def to_yaml(self, path: str | Path) -> None:
        Path(path).write_text(yaml.safe_dump(self.to_dict(), sort_keys=False))

    @classmethod
    def from_yaml(cls, path: str | Path) -> VehicleParameters:
        return cls.from_dict(yaml.safe_load(Path(path).read_text()))

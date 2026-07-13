# Decision Log

Architecture Decision Records (ADRs) for choices that would be expensive to
reverse or non-obvious to a future contributor. Append new entries; do not
edit past ones except to add a superseding link -- the point is to show
*why* a decision was made at the time, even if it's later reversed.

---

## ADR-0001: Propulsion as a registered plugin, not a class hierarchy consumers import directly

**Status:** Accepted (2026-07-13)

**Context:** The propulsion technology is explicitly undefined and must
stay swappable indefinitely.

**Decision:** `propulsion.base.PropulsionCellBase` defines the interface;
concrete technologies register themselves with
`propulsion.registry.register` and are constructed only via
`propulsion.registry.create(name, spec)`. Callers never import a concrete
class (`CompressedGasPropulsion`, etc.) directly.

**Consequence:** Swapping propulsion technology is a config/string change,
not a code change, anywhere outside `propulsion/`. The cost is one extra
layer of indirection (registry lookup) for a very small number of call
sites.

---

## ADR-0002: Thrust allocation via least-squares pseudo-inverse + clipping

**Status:** Accepted (2026-07-13)

**Context:** Need a thrust allocator that works for *any* cell layout and
*any* propulsion technology, usable before real actuator saturation
behavior is known.

**Decision:** Build a 6xN effectiveness matrix from cell geometry alone
(`flight_control.allocator.ThrustAllocator`), solve with
`numpy.linalg.pinv`, then clip to each cell's `[min_thrust_n,
max_thrust_n]`.

**Consequence:** Zero dependency on actuator physics, but no redistribution
of unmet demand to non-saturated cells when saturated. Tracked as a known
limitation in `flight_control/allocator.py` and `docs/research_log.md`; a
weighted or QP-based allocator is the likely replacement once saturation
behavior matters in practice.

---

## ADR-0003: cadquery is an optional, conda-preferred dependency

**Status:** Accepted (2026-07-13)

**Context:** cadquery depends on OpenCascade (OCP) bindings that are
substantially more reliable to install via conda-forge than via pip
wheels, especially on Windows.

**Decision:** `environment.yml` (conda) is the primary path for CAD work.
`pyproject.toml` also exposes a `cad` extra (`pip install -e ".[cad]"`) for
environments where conda isn't used. All `cad.*` modules guard the import
(`cad._cq`) and raise a clear `RuntimeError` if called without cadquery
installed, rather than failing at import time -- so the rest of the
codebase (propulsion, flight control, simulation, optimization) never
requires cadquery to import or test.

**Consequence:** CI (`.github/workflows/ci.yml`) runs the full test suite
without cadquery; `tests/test_cad_geometry.py` self-skips via
`pytest.importorskip("cadquery")`. Geometry-generation bugs are only
caught in environments with cadquery installed -- this is a real coverage
gap, accepted for now.

---

## ADR-0004: Mixed top-level package layout instead of `src/oryx/`

**Status:** Accepted (2026-07-13)

**Context:** The project brief specifies a literal top-level directory
list (`cad/`, `simulation/`, `propulsion/`, `flight_control/`,
`optimization/`, `firmware/`, `electronics/`, `docs/`, `research/`,
`experiments/`, `scripts/`, `tests/`, `assets/`, `unreal/`).

**Decision:** Honor that layout literally: the Python packages are
top-level directories, not nested under `src/oryx/`.
`pyproject.toml`'s `[tool.setuptools.packages.find]` explicitly includes
just the five Python package names.

**Consequence:** Package names (`cad`, `simulation`, etc.) are generic and
could collide with unrelated packages in a shared Python environment. Not
a concern for a project developed in its own virtualenv/conda env, but
worth knowing before adding this project as a dependency of something
else.

---

## ADR-0005: Repository identity -- ORYX, not AETHRA

**Status:** Accepted (2026-07-13)

**Context:** The project was initially scoped under the working name
"AETHRA." The repository already existed as `ORYX-core`
("Omnidirectional Reaction sYstem eXperiment").

**Decision:** "AETHRA" was a naming mistake; the project is ORYX. All
docs, package metadata, and this scaffold use ORYX.

**Consequence:** Any external references to "AETHRA" from early scoping
conversations do not apply to this repository.

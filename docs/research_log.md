# Research Log

An append-only, dated log of what was tried, what was measured, and what
was concluded. Unlike [decision_log.md](decision_log.md) (which records
*architecture* decisions), this log tracks *research* findings --
including negative results. Per [philosophy.md](philosophy.md), a
hypothesis that fails is a completed, useful entry, not something to
omit.

Each entry should have enough detail that someone could reproduce the
result from the repository state at that date. Prefer linking to a
committed `experiments/<name>/` record over inlining large amounts of
data here.

## Entry template

```markdown
## YYYY-MM-DD -- <short title>

**Hypothesis:** what was being tested, and why.

**Method:** what was run (script, sweep, bench test), against what
configuration/commit.

**Data:** key measured results, or a link to `experiments/<name>/`.

**Conclusion:** validated / rejected / inconclusive, and what changes as
a result (a new hypothesis, a design change, a module marked for rework).
```

---

## 2026-07-13 -- Framework bootstrap

**Hypothesis:** A propulsion-technology-agnostic framework (plugin
interface, generic thrust allocator, hardware-independent simulation,
parametric CAD, sweep runner) can be built and internally consistent
before any propulsion technology is selected.

**Method:** Implemented `propulsion/`, `flight_control/`, `simulation/`,
`cad/`, `optimization/` and a pytest suite (`tests/`) exercising: cell spec
validation, the plugin registry, allocator behavior (zero-wrench,
symmetric distribution, unsaturated wrench reproduction, saturation
clipping), rigid body free-fall and hover-thrust cases, the generic
propulsion surrogate's first-order lag and pressure-loss derating, an
end-to-end `Vehicle` hover simulation, and the sweep/parameter-space
machinery. 31 tests, run against Python 3.14 in a local venv (cadquery not
installed, so CAD geometry tests self-skip via
`pytest.importorskip("cadquery")`; CAD parameter/serialization tests still
run).

**Data:** All 31 non-CAD-geometry tests pass. No propulsion technology
physics is implemented (by design -- see `propulsion/cells/*` docstrings
for the specific open questions each technology needs answered before
implementation).

**Conclusion:** Validated for this phase's narrow claim (the abstraction
is buildable and internally consistent). Does **not** yet validate that
the abstraction is the *right* one for real propulsion hardware -- that
can only be tested once Phase 1 (see `roadmap.md`) produces real
single-cell bench data to implement a `propulsion.cells` plugin against.
Known open gap: no cadquery-based geometry test has actually executed
(environment lacks cadquery); flagged in ADR-0003.

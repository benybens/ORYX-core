# ORYX

*Omnidirectional Reaction sYstem eXperiment*

ORYX is a long-term research platform for a new class of aerial vehicle: a
monocoque airframe with **distributed fluid propulsion**, instead of a
handful of discrete rotors. The propulsion technology behind that thrust --
compressed gas, CO2, electric ducted fans with ejector amplification,
plasma/electrohydrodynamic propulsion, ion propulsion, combustion gas
generation, fluidic amplifiers, or something not yet identified -- is
intentionally undefined and stays that way by design. Every module in this
repository is built so that decision can be made later, informed by
measured data, without rewriting the rest of the system.

See [docs/philosophy.md](docs/philosophy.md) for the project's guiding
principles and research methodology, and [docs/roadmap.md](docs/roadmap.md)
for where this is headed.

## Status

**Phase 0: framework.** No propulsion technology is implemented yet. What
exists is the abstraction every future propulsion technology, flight
control strategy, and hull design will be built against: a propulsion
plugin interface, a generic thrust allocator, a hardware-independent
simulation, parametric CAD, and a parameter sweep framework. See
[docs/research_log.md](docs/research_log.md) for the current state in
detail.

## Repository structure

```
cad/              Parametric CadQuery geometry generation
simulation/       Hardware-independent physics simulation
propulsion/       Propulsion plugin interface + registry (no tech implemented)
flight_control/   Generic thrust allocation (wrench -> per-cell command)
optimization/      Parameter sweep framework
firmware/         Future: embedded control code
electronics/      Future: wiring harness / PCB design assets
docs/             Philosophy, roadmap, architecture, decision/research logs
research/         Open hypotheses and research questions
experiments/       Dated experiment records with measured data
scripts/          Runnable entry points
tests/            pytest suite
assets/           Static reference assets
unreal/           Future: Unreal Engine visualization project
```

See [docs/architecture.md](docs/architecture.md) for module boundaries,
data flow, and the key interfaces that must stay stable as technologies
are swapped in and out.

## Getting started

### Environment setup

CAD generation depends on `cadquery`, whose OpenCascade bindings install
far more reliably via conda than pip:

```bash
conda env create -f environment.yml
conda activate oryx
pip install -e ".[dev]"
```

Without CAD work, a plain virtualenv is enough:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Running the tests

```bash
pytest
```

CAD geometry tests self-skip if `cadquery` isn't installed; everything
else (propulsion, flight control, simulation, optimization) has no such
dependency.

### Running a parameter sweep

```bash
python scripts/run_sweep.py
```

### Generating CAD (requires the `cad` extra / conda environment)

```bash
python scripts/generate_cad.py
```

### Starting a new experiment record

```bash
python scripts/new_experiment.py "my experiment name"
```

See [experiments/README.md](experiments/README.md) for the expected
record format.

## Contributing principles

- No module may assume a specific propulsion technology.
- Every subsystem should be replaceable independently of the others.
- Every experiment must produce measurable engineering data -- see
  [docs/research_log.md](docs/research_log.md).
- Prefer measured data over intuition; avoid confirmation bias by design
  (see [docs/philosophy.md](docs/philosophy.md)).
- Record architecturally significant decisions in
  [docs/decision_log.md](docs/decision_log.md), with the reasoning, not
  just the outcome.

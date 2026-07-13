# Project Philosophy

## What ORYX is

ORYX is a long-term deep-tech research platform for a new class of aerial
vehicle: a monocoque airframe with **distributed fluid propulsion**, rather
than a small number of discrete rotors. "Fluid propulsion" is left
deliberately open -- compressed gas, compressed air, CO2, electrohydrodynamic
(plasma), ion, combustion gas generation, ejector amplification, fluidic
amplifiers, and technologies not yet identified are all in scope, and none
of them is assumed to be the answer.

## What ORYX is not

ORYX is not a quadcopter project, and it is not a bet on any single
propulsion technology. Every abstraction in this repository exists to keep
that true as the project evolves.

## The one rule everything else follows

**No module may assume a specific propulsion technology.** Flight control
allocates a wrench (force + torque) to abstract propulsion cells. Simulation
models rigid-body dynamics, latency, and losses generically. CAD generates
mounting interfaces, not propulsion hardware. If a design decision would
require breaking this rule, that is a signal to reconsider the decision, not
the rule.

## Research methodology

- **Never assume the initial concept is correct.** Distributed fluid
  propulsion on a monocoque hull is the hypothesis this whole project
  exists to test, not a foregone conclusion. It may turn out to be
  inferior to alternatives for reasons not yet understood -- that is a
  valid, useful outcome.
- **Every subsystem must be replaceable.** Propulsion technology, thrust
  allocation strategy, hull shape, and simulation fidelity should each be
  swappable without rewriting the rest of the system. See
  [architecture.md](architecture.md) for the module boundaries that
  enforce this.
- **Every experiment must produce measurable engineering data.** A test
  that only produces an opinion ("it feels more efficient") is not a
  completed experiment. See [research_log.md](research_log.md) and
  `experiments/README.md` for the expected record format.
- **Avoid confirmation bias.** Design a test that could show the current
  favored approach is wrong, not just one that confirms it. When a result
  contradicts expectations, trust the data and update the hypothesis, not
  the other way around.
- **Prefer measured data over intuition.** Simulation and bench data
  outrank engineering intuition when they disagree. Intuition is what
  generates hypotheses to test, not a substitute for testing them.
- **This repository is the digital twin of the project.** Parameters,
  geometry, simulated performance, and (eventually) real flight/bench data
  should all trace back to the same parametric model
  (`cad.parameters.VehicleParameters` and its simulation/optimization
  analogues), so results are always reproducible and comparable across
  time.

## Decision-making

Architecturally significant decisions and the reasoning behind them are
recorded in [decision_log.md](decision_log.md) so future contributors (and
future us) can see *why*, not just *what*.

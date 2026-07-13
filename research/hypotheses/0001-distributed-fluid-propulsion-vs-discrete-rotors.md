# 0001 - Distributed fluid propulsion vs. discrete rotors

**Status:** open
**Opened:** 2026-07-13

## Question

For a small aerial vehicle, can a monocoque hull with distributed fluid
propulsion (many small thrust-producing cells fed from a shared or
distributed fluid source) match or beat a conventional discrete-rotor
(quadcopter-class) vehicle on thrust-to-weight, controllability, and
survivability -- for *some* propulsion technology and hull configuration --
or does every candidate technology lose on at least one axis badly enough
to make the approach impractical?

## Why it matters

This is the foundational bet of the ORYX project (see
`docs/philosophy.md`). Every module in this repository is built to make
this question answerable with data rather than assumed true; the project
roadmap's entire Phase 1-2 (see `docs/roadmap.md`) exists to test it.

## What would validate this

At least one candidate propulsion technology, integrated into a subscale
CAD-designed hull, achieves:

- Thrust-to-weight ratio >= 1.5 in simulation
  (`optimization.objectives.thrust_to_weight_ratio`) using bench-measured
  (not assumed) per-cell thrust and mass.
- Closed-loop hover stability in simulation using
  `flight_control.ThrustAllocator` with realistic (bench-measured) cell
  response time.
- No thermal or energy result that rules out a useful flight duration
  (see `simulation.thermal`, `simulation.energy`).

## What would reject this

Every candidate technology characterized in Phase 1 bench tests fails to
clear a thrust-to-weight ratio of 1.2 once real (not assumed) mass,
power-supply mass, and response time are included, **or** the achievable
allocator bandwidth (limited by real cell response time) is too slow for
stable hover control in simulation.

## Experiments

None yet -- Phase 1 bench characterization (see `docs/roadmap.md`) has not
started.

## Current answer

Open. Next step: bench-characterize at least one candidate technology
(see `propulsion/cells/*` module docstrings for the specific open
questions per technology) and run it through
`optimization.objectives.thrust_to_weight_ratio` with real numbers.

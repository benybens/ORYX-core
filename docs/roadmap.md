# Roadmap

This roadmap describes *phases of learning*, not a fixed delivery schedule.
Per [philosophy.md](philosophy.md), each phase exists to test a hypothesis;
a phase can end with "this approach is wrong" as a valid, useful result
that reshapes the next phase.

## Phase 0 -- Framework (current)

**Hypothesis under test:** a propulsion-agnostic abstraction (plugin
propulsion interface, generic thrust allocator, hardware-independent
simulation, parametric CAD, sweep-driven optimization) is buildable and
usable before any propulsion technology is chosen.

- [x] Propulsion plugin interface + registry (no technology implemented)
- [x] Generic thrust allocation (wrench -> per-cell command)
- [x] Rigid body simulation + generic propulsion surrogate (latency,
      pressure loss, energy, thermal)
- [x] Parametric CAD skeleton (hull, plenum, nozzles, channels, ribs,
      mounts, propulsion interface)
- [x] Parameter sweep framework
- [x] Test suite covering the above
- [ ] First real parameter sweep exercising the full stack end-to-end
      (tracked in `experiments/`)

## Phase 1 -- Propulsion technology screening

**Hypothesis under test:** at least one of the candidate propulsion
technologies (compressed gas, CO2, EDF + ejector amplification, plasma/EHD,
combustion gas generator, ion) can plausibly meet a bench-testable
thrust-to-weight and endurance target for a small distributed-propulsion
vehicle.

- Bench-characterize each candidate technology's thrust, response time,
  and specific power/energy in isolation (single-cell rig, not integrated
  into an airframe).
- Record results in `experiments/`, evaluate against
  `optimization.objectives` (thrust-to-weight, specific energy, hover
  endurance).
- Down-select to 1-2 technologies for integration, or conclude none of
  the current candidates clear the bar and revisit the candidate list.

## Phase 2 -- Single-technology integrated bench prototype

- Implement one real `propulsion.cells` plugin against the down-selected
  technology's actual bench data (replacing
  `simulation.generic_propulsion.GenericPropulsionCell` for that
  technology).
- Build a subscale CAD assembly (`cad.build.build_vehicle`) sized for that
  technology's cell count/geometry.
- Validate `flight_control.ThrustAllocator` against a tethered/bench rig:
  commanded wrench vs. measured wrench.

## Phase 3 -- Subscale free-flight validation

- Close the loop: real sensors -> estimated state -> allocator -> real
  propulsion cells, on a tethered or safety-netted subscale vehicle.
- Compare simulated vs. flown dynamics; feed discrepancies back into
  `simulation.rigid_body` and `simulation.generic_propulsion` fidelity.

## Phase 4 -- Design space exploration at scale

- Run broad `optimization` sweeps (hull size, nozzle count/angle, plenum
  volume, mass budget, propellant/battery split) against validated
  simulation fidelity from Phase 3.
- Use results to drive a second-generation hull/propulsion configuration.

## Explicitly out of scope for now

- `firmware/` and `electronics/` implementation -- placeholders only until
  a propulsion technology and control architecture are chosen.
- `unreal/` visualization -- placeholder until there is simulation output
  worth visualizing in real time.

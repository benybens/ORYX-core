# Firmware

Placeholder. No embedded control code exists yet -- see
[docs/roadmap.md](../docs/roadmap.md) Phase 2/3. Once a propulsion
technology and control hardware are selected, this directory will hold the
embedded implementation of `flight_control.ThrustAllocator`'s allocation
logic and the propulsion command interface, ported from the Python
reference implementation in `flight_control/` and `propulsion/`.

Keep the same principle as the rest of the project: firmware should
implement the same technology-agnostic interfaces (`PropulsionCellBase`,
`Wrench`), not hardcode a specific propulsion technology.

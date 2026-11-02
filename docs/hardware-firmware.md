# Hardware and firmware conventions

Place KiCad projects under `hardware/kicad/`. Generated Gerbers, drill files, and
assembly exports belong in `hardware/fabrication/` and are ignored by Git except
for its directory marker.

Firmware is intentionally target-neutral until the SoC selection is recorded.
Add a board package under `firmware/boards/<target>/` containing startup code,
linker script, and peripheral configuration. Keep reusable C/C++ interfaces in
`firmware/include/` and implementation in `firmware/src/`.

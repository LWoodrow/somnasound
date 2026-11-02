# Work package: first mechanical and PCB floorplan

Status: `VERIFIED`

## Decision context

- Accepted decision records: D-003, D-004, D-005, D-006, D-052, D-053, D-062, D-063, D-064.
- Question this work answers: can the agreed calm, shallow bedside form contain one main board while maintaining a credible separation between audio/power, RF/sensing and the user-facing controls?
- Evidence that will change the decision: full-size print/handling review; selected component mechanical drawings; thermal/RF/audio layout review; real banana-plug and cable-clearance mock-up.

## Objective

Create a reproducible, reviewable first-draft enclosure and KiCad board floorplan that establishes physical interfaces without pretending that the design is ready to fabricate or electrically route.

## Inputs and interfaces

- Existing files: `docs/product-plan.md`, `docs/decision-register.md`, and `docs/concepts/front-panel-concept-v1.png`.
- Interfaces that must remain stable: 24 V external power; four independent BTL speaker terminals; red 3.37-inch PMOLED envelope; radar/thermal sensor detail; one main-board intent; rear-only enclosure fasteners.

## In scope

- Parametric FreeCAD model for front, base, rear spine, apertures, connection-bay envelope, board envelope and mounting concept.
- KiCad project containing board outline, named placement zones, connector/sensor keep-outs and a mechanical mounting map.
- STEP/STL exports for physical/review use and a board render.
- Documentation of assumptions and the next measurements required.

## Out of scope

- Schematic, component selection, electrical routing, impedance control, audio/RF/thermal sign-off, DFM, EMC, safety, or production release.
- Declaring dimensions final or ordering a populated PCB.

## Acceptance criteria

- [x] FreeCAD source regenerates a native model plus STEP and STL exports without GUI interaction.
- [x] KiCad parses the placement-study PCB and its outline is 200 x 112 mm.
- [x] The board study explicitly separates audio/power, deterministic sensing, connectivity/RF and front-panel zones.
- [x] Documentation records all provisional dimensions and concrete blockers to production layout.

## Verification commands or procedure

```text
& 'C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe' hardware/cad/somnasound_enclosure_draft.py
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' pcb drc hardware/kicad/somnasound-floorplan.kicad_pcb
& 'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe' pcb render -o hardware/kicad/output/somnasound-floorplan.png hardware/kicad/somnasound-floorplan.kicad_pcb
```

## Deliverables

- `hardware/cad/somnasound_enclosure_draft.py` and generated native/exchange outputs.
- `hardware/kicad/somnasound-floorplan.kicad_pcb` and project metadata.
- `hardware/cad/README.md` and `hardware/kicad/README.md`.

## Handoff

- Results: FreeCAD 1.1.4 created the native model, STEP and STL. KiCad 10.0.8 reported zero DRC violations, unconnected pads or footprint errors; the rendered board preview was also created. The final first-pass envelope is 200 x 112 mm, not the initial 205 x 118 mm, because the latter did not leave credible wall/standoff tolerance inside a 220 mm-wide enclosure.
- Deviations: this is deliberately a no-footprint/no-net placement study. A KiCad DRC pass therefore validates file integrity and outline only, not an electrical design.
- Remaining risks: real display/module depth, encoder/button mechanisms, sensor fields of view, binding-post/plug envelope and heat/RF/audio interactions are unproven. The board size is an envelope, not a committed PCB dimension.
- Recommended decision update: none until physical mock-up and component selection evidence exist.

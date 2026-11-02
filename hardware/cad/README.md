# Somnasound enclosure CAD draft

`somnasound_enclosure_draft.py` is the reproducible parametric source for the
first enclosure study. Run it with FreeCAD 1.1.4; it creates a native `.FCStd`
model and STEP/STL exchange files under `output/`.

It models the agreed architectural features only: 15-degree calm landscape front,
wider base, rear-parallel service spine, display and sensor apertures, two wheel
openings, tactile-button envelopes, hidden rear fastener concept and the lower
connection-bay envelope. It is **not print-ready**. The apertures and all component
dimensions are provisional until the exact Palm display, sensor modules, encoders,
buttons, terminals, DC inlet and rubber feet are selected from mechanical drawings.

The generated model includes a translucent 200 x 112 mm board envelope to make the
KiCad/FreeCAD boundary visible. That is an interface check, not a claim that the
floorplan is electrically complete.

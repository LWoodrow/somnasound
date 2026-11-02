# Somnasound KiCad floorplan

`somnasound-floorplan.kicad_pcb` is a **mechanical placement study**, not a
schematic or a fabrication board. It establishes the tentative 200 x 112 mm main
board envelope and the intended physical separation of:

- 24 V input / high-current Class-D audio;
- deterministic audio and sensing;
- connectivity/RF; and
- front-interface, compute and rear-I/O harness areas.

The zones are deliberately drawings rather than component footprints. The next
revision must use real parts, real keep-outs and an actual stack-up before any
routing begins. In particular, it must preserve the Wi-Fi antenna keep-out, radar
field of view, thermal aperture/heat separation, microphone acoustic placement,
BTL speaker-return isolation and the audio/power noise boundary.

Open the `.kicad_pro` file in KiCad 10.0.8. A generated preview is written to
`output/` by the work-package verification command.

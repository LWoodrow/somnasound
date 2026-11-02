# Work package: red display and front-panel production validation

Status: `DRAFT`

## Decision context

- Accepted records: D-002 dark-room behaviour, D-023 front panel, D-030 non-touch
  interaction, D-032 automatic blackout, and D-033 finished-device delivery.
- Proposed dependency: D-027 operating-state separation and D-031 display hardware.
  Accepted dependency: D-032 automatic blackout.
- Question this work answers: which red display size and physical control layout is
  readable by day, usable without looking, and guaranteed dark during sleep?

## Objective

Validate production-intent front-panel mock-ups and display samples before schematic
or enclosure dimensions freeze. These samples retire risk for the one finished device;
they are not alternate consumer products.

## Inputs and interfaces

- Required content: source, volume, procedural mode/richness, timer, track/artist,
  network/setup state, and short fault messages.
- Required actions: immediate volume reduction/mute, power/standby, play/pause,
  source, sound mode, previous/next, timer, and display-off.
- Use only red visible output in normal operation; basic controls must remain usable
  with the display unpowered.

## In scope

- The red monochrome variant in Palm's PTOG2412□-A0 3.37-inch 240 x 128 PMOLED family
  as the accessibility target and only red-output alternatives that can meet identical
  display evidence.
- A Bourns PEC11L-class 20-detent/20-pulse push encoder and alternate tactile button
  grouping mock-ups; touchscreen comparison is not required.
- Hardware-default-off display load switch; default 30-second hold plus two-second
  fade and power-off; 10/20-second shorter settings; immediate display-off.
- Daylight, across-room, bedside, glasses-off, and fully dark usability checks.
- Burn-in mitigation, boot/update/crash/fault behaviour, and basic accessibility.
- Preliminary local-library metadata and localisation fit using representative files.

## Out of scope

- Final industrial design, production tooling, capacitive touchscreen, companion app,
  and final production certification.

## Acceptance criteria

- [ ] A sleeping-room power cycle, processor reset, firmware crash simulation, and
      display timeout all leave the display and every indicator electrically dark.
- [ ] The lowest non-zero setting is readable at bedside without objectionable glow;
      full off is measured separately from software blanking.
- [ ] Primary bedside state/value text has at least 16 mm capital height, secondary
      text is 9–12 mm, and sparse across-room status is 25–30 mm; essential
      instructions do not depend on scrolling.
- [ ] A user can mute or reduce volume, start/stop playback, select a soundscape, and
      extinguish the display without a phone or manual.
- [ ] Normal encoder turn changes volume and push toggles mute; menu turn highlights
      and push selects, with no ambiguous mode or missed/reversed steps.
- [ ] Source and common metadata remain legible at the agreed daytime distance.
- [ ] No essential action depends only on colour, a long press, or an illuminated
      label; proposed long presses have a discoverable short-press behaviour.
- [ ] The selected direction records supply status, lifetime, interface, optical
      window, power, EMC, and replacement risks.
- [ ] The proposed 3.37-inch panel is not frozen until its exact red order code,
      supply rails, FPC, UK/EU availability, MOQ, lifecycle, spectral output,
      daylight brightness, enclosure impact, and sample performance are verified.
- [ ] After inactivity, every display pixel and visible indicator follows the fade
      policy and the display rail powers down; no boot, fault, update, network, or
      standby state can leave a bedroom light on indefinitely.

## Verification commands or procedure

Run a scripted task test with older and reduced-vision participants as well as at
least three representative users. Photograph the panel at fixed exposure in daylight,
low light, and a dark-adapted bedroom at the agreed bedside/across-room distances.
Measure display-rail voltage/current in on, fading, blanked, timed-out, reset, and
unpowered states.

## Deliverables

- Mock-up files, button map, state sketches, measurements, and decision note under
  `hardware/front-panel/` and `docs/ui/`.

## Handoff

- Results:
- Deviations:
- Remaining risks:
- Recommended decision update:

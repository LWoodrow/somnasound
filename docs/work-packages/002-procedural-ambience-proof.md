# Work package: procedural rain and storm proof

Status: `DRAFT`

## Decision context

- Accepted records: D-003 audio quality and D-022 procedural sound engine.
- Open dependencies: D-005 processor and D-026 adaptive masking.
- Question this work answers: can a portable real-time C++ engine create an
  evolving rain/storm scene with no audible loop, boundary artefact, or unsafe peak?
- Prerequisite: verified output from work package 001.

## Objective

Extend the portable audio library with one representative layered rain/storm mode
that proves the state, scheduling, mixing, and long-duration test architecture needed
by later ocean, waterfall, wind, fan, and fireplace modes.

## Inputs and interfaces

- Reuse the 48 kHz interleaved-stereo render interface from work package 001.
- Preserve deterministic seeded rendering and the no-allocation render contract.
- Use newly synthesized events or assets carrying documented commercial
  redistribution rights; do not import audio from either reference repository.

## In scope

- Stateful multi-band rain bed with stereo decorrelation and slow modulation.
- Stochastic droplet and thunder-event scheduler with intensity and
  `calm / natural / vivid` richness controls.
- Smooth parameter changes, headroom allocation, and limiter integration.
- Optional storm-distance parameter affecting delay, filtering, and level.
- Eight-hour offline render and automated periodicity, click, peak, DC, and tonal
  artefact analysis.
- CPU, memory, state-size, and render-time measurements on the host.

## Out of scope

- Front-panel UI, adaptive room-volume control, hardware drivers, production EQ,
  local media/network playback, visual lightning, and the remaining soundscape
  families.

## Acceptance criteria

- [ ] Identical seed and controls produce byte-identical output.
- [ ] Rendering allocates no memory after initialization and preserves filter and
      envelope state across every block boundary.
- [ ] No finite ambience bed is replayed and the event schedule does not repeat
      during an eight-hour render.
- [ ] Automated scans find no discontinuity over the declared fade/smoothing bound,
      no clipping, and no unexplained fixed-period or tonal component.
- [ ] Intensity and richness transitions are click-free and bounded in loudness.
- [ ] A listening record compares at least three seeds at low sleep volume and
      normal daytime volume, documenting artificial or fatiguing characteristics.
- [ ] Source and asset provenance is recorded beside every retained dependency.
- [ ] Existing CTest, npm lint, and TypeScript checks pass.

## Verification commands or procedure

```text
cmake --preset bare-metal -S firmware
cmake --build firmware/build/bare-metal
ctest --test-dir firmware/build/bare-metal --output-on-failure
npm run lint
npm run typecheck
```

Render eight continuous hours for `calm`, `natural`, and `vivid`; retain statistics
and short representative excerpts rather than committing full renders.

## Deliverables

- Portable source and tests under `firmware/`.
- Algorithm, measurement, and asset-provenance notes under `docs/audio/`.

## Handoff

- Results:
- Deviations:
- Remaining risks:
- Recommended decision update:

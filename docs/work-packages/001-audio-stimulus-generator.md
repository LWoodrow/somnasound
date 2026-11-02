# Work package: portable sleep-audio stimulus generator

Status: `APPROVED`

## Decision context

- Accepted records: D-003 audio quality, D-016 custom-board production direction,
  D-018 external 24 V power, D-019 Monitor Audio Silver 1 output, and D-022
  procedural sound engine.
- Question this work answers: can the core noise generator produce controlled,
  repeatable, click-free test material independently of the eventual processor?
- Evidence that changes later decisions: spectral measurements, listening results,
  or inability to meet deterministic real-time constraints.

## Objective

Implement a portable C++20 audio-stimulus library and host test executable that
generate repeatable white, pink, and brown noise for acoustic and amplifier tests.

## Inputs and interfaces

- Extend the existing `firmware/` CMake project.
- Keep the DSP library independent of an operating system, hardware abstraction
  layer, audio driver, and processor SDK.
- Use interleaved stereo 48 kHz samples with a documented floating-point reference
  interface; fixed-point optimization is a later work package.

## In scope

- Deterministic seeded generators for white, pink, and brown noise.
- Brown-noise DC control so the random walk cannot drift into clipping.
- Independent-channel and linked-mono operation.
- Gain control, configurable fade-in/fade-out, and a bounded limiter.
- A host executable that writes standard PCM WAV fixtures.
- CTest tests and a small analysis command that report peak level, RMS, DC offset,
  discontinuities, and fitted spectral slope.
- Short documentation explaining the algorithms, parameters, and limitations.

## Out of scope

- Hardware I2S/SAI drivers, amplifier control, Bluetooth, UI, medical inference,
  adaptive echo cancellation, EQ for the Silver 1, and production tuning.
- Third-party DSP dependencies unless a need is demonstrated in the handoff.

## Acceptance criteria

- [ ] A clean checkout configures and builds through CMake/CTest on the host.
- [ ] Identical seed and parameters produce byte-identical WAV output.
- [ ] Every generated sample is finite and remains within the documented range.
- [ ] Steady-state DC offset is below -60 dBFS for every noise colour in a 10-minute
      fixture.
- [ ] Start and stop transitions contain no single-sample discontinuity greater
      than the configured fade step.
- [ ] Spectral analysis documents tolerances and verifies white near 0 dB/octave,
      pink near -3 dB/octave, and brown near -6 dB/octave over the declared valid
      band.
- [ ] Rendering performs no heap allocation after initialization.
- [ ] Existing npm lint and type-check commands continue to pass.

## Verification commands or procedure

```text
cmake --preset bare-metal -S firmware
cmake --build firmware/build/bare-metal
ctest --test-dir firmware/build/bare-metal --output-on-failure
npm run lint
npm run typecheck
```

Generate at least 10 minutes of each noise colour, inspect the reported statistics,
and retain only short representative WAV fixtures in Git.

## Deliverables

- Portable library under `firmware/src/audio/` and public headers under
  `firmware/include/somnasound/audio/`.
- Host tool under `firmware/tools/audio/`.
- Tests under `firmware/tests/`.
- Algorithm note under `docs/audio/`.

## Handoff

- Results:
- Deviations:
- Remaining risks:
- Recommended decision update:

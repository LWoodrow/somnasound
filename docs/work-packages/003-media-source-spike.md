# Work package: local media, web control, and Wi-Fi spike

Status: `DRAFT`

## Decision context

- Accepted record: D-021 daytime audio role.
- Accepted records: D-024 local music sources and D-028 local web interface.
- Revisited/proposed records: D-025 media architecture and D-029 Wi-Fi onboarding.
- Question this work answers: can one coherent media/control design browse and play
  SD and read-only network libraries while providing reliable BT-style home-Wi-Fi
  setup and matching physical/web controls?

## Objective

Prototype the deep media-library, playback-engine, control-model, and
network-provisioner interfaces, then recommend single- or split-processor placement
from measured concurrency, security, RF/audio, lifecycle, and cost evidence.

## Inputs and interfaces

- Use section 7 of `docs/streaming-and-procedural-audio-research.md` as the starting
  evidence and D-024 as the fixed source scope.
- Provide host adapters/fakes for storage and networking so module tests use the same
  interfaces as hardware implementations.
- Use a versioned 48 kHz PCM/playback-reference seam if media and real-time audio are
  placed on separate processors.

## In scope

- SD-card WAV/FLAC/MP3 indexing and playback with long filenames, Unicode metadata,
  folder view, album view, track/disc ordering, queue persistence, and seeded shuffle.
- Read-only SMB 2/3 library adapter with credential handling, reconnect, timeout,
  network-loss, missing-file, and index-refresh behaviour.
- One control model used by a minimal responsive local web adapter and a simulated
  physical-panel adapter; no duplicated playback state.
- Temporary setup-network/captive-page prototype with a unique displayed WPA2 key,
  known-good credential rollback, DHCP, mDNS `somnasound-XXXX.local`, and IP-address
  fallback.
- WPA2/WPA3 and 2.4/5 GHz platform assessment against representative BT Smart Hub
  generations or equivalent configurations.
- Single-versus-split processor benchmark including concurrent indexing, FLAC decode,
  web requests, Wi-Fi reconnect, procedural audio, and representative sensing load.
- Secure boot/update, credential encryption/redaction, LAN-only HTTP exposure and
  access control, RF/EMC, privacy, boot, idle-power, supply, BOM, lifecycle, and
  support comparison.

## Out of scope

- Spotify Connect, AirPlay, cloud accounts, Bluetooth audio, writable network shares,
  destructive media operations, production silicon selection, and final PCB layout.

## Acceptance criteria

- [ ] SD playback and all library controls work without Wi-Fi or internet access.
- [ ] Folder order is stable, album order honours valid disc/track tags, and a fixed
      shuffle seed produces the same permutation without repeating a track early.
- [ ] Removing SD or dropping SMB during playback causes no crash, unbounded block,
      click/burst, or loss of access to procedural audio.
- [ ] The temporary setup network remains recoverable after a wrong password, missing
      DHCP, router reboot, same-name dual bands, and failed WPA2/WPA3 association.
- [ ] Front-panel and web actions produce identical control-model state and conflict
      resolution under an automated command-sequence test.
- [ ] No web asset requires a CDN or internet connection; no raw camera/audio stream,
      WAN listener, cloud relay, UPnP mapping, or returned credential is exposed.
- [ ] LAN report access uses the chosen local pairing/PIN or physical-confirmation
      flow and passes IPv4/IPv6 exposure, session, redaction, and reset tests.
- [ ] The processor comparison includes a recoverable update path and at least five
      years of component/software support evidence.
- [ ] Any cross-processor seam covers PCM/clock ownership, metadata, control, boot,
      update, crash, and network-loss behaviour.
- [ ] The prototype delivers clean 48 kHz stereo without underruns or source-switch
      transients during the declared worst-case concurrent workload.
- [ ] D-024 and D-025 receive a specific recommended status update.

## Verification commands or procedure

Run module tests with host fakes, then repeat the same behavioural suite on candidate
hardware. Execute the router matrix on a BT Smart Hub 2/3 or equivalent WPA2/WPA3,
same-SSID, dual-band configurations. Retain timing, underrun, RF/audio, power, and
recovery evidence before accepting processor placement.

## Deliverables

- Dated platform/router/security comparison under `docs/media/`.
- Media-library, playback-engine, control-model, and provisioner interface proposal
  under `docs/interfaces/`.
- Host prototype/tests plus target adapter spike under `firmware/` or an explicitly
  justified separate application directory.
- Recommended decision-register changes.

## Handoff

- Results:
- Deviations:
- Remaining risks:
- Recommended decision update:

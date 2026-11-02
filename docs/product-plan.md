# Somnasound product plan

Status: **DRAFT FOR REVIEW**

This is the planning source of truth. It separates desired outcomes from proposed
implementations so components can change without losing the product intent.

## Product intent

Somnasound is a bedside sleep and everyday audio device that should:

- operate without disturbing sleep;
- play genuinely pleasant, clean masking audio;
- play local and home-network music during the day at normal
  television-to-moderate listening levels;
- play local music libraries and evolving, non-repeating procedural soundscapes;
- infer useful sleep-related events locally without retaining raw bedroom audio or
  imagery by default;
- expose understandable metrics rather than unsupported medical conclusions; and
- remain serviceable as sensing, compute, and integration choices evolve.

The first product direction is wellness-first and future-medical-ready. Engineering
may measure respiration and identify candidate breathing interruptions, but the
product must not diagnose sleep apnoea or present a clinical AHI without the
appropriate evidence, intended-use review, and conformity route. A disclaimer does
not determine regulatory classification.

## Non-negotiable experience requirements

### Dark-room behaviour

- Sleep mode has no visible indicator light by default.
- Any user-visible night indicator is red, dimmable to off, and opt-in.
- Debug, charging, module, and boot LEDs must be electrically controllable or
  physically obscured in the production design.
- A sensing system that requires visibly glowing 850 nm emitters does not meet the
  requirement. A 940 nm system still needs camera-sensitivity, thermal, optical,
  and eye-safety validation.

### Audio quality

- Silence, mute, startup, shutdown, and volume changes produce no audible hiss,
  whine, clicks, pops, or radio interference at the sleeping position.
- Playback quality is judged end to end: waveform generation, clocking, amplifier,
  power supply, PCB layout, transducer, enclosure, vents, and DSP calibration.
- Speaker playback must not invalidate microphone measurements. Physical isolation
  and an electrical playback reference are planned; adaptive echo cancellation is
  evaluated rather than assuming a baffle is sufficient.
- Acceptance thresholds will be fixed after measuring the intended speaker,
  enclosure volume, listening distance, and room noise floor. Until then, “no
  hiss” is a test objective, not a component claim.
- Playback is stereo through two external passive bookshelf speakers. The device
  provides four red/black five-way binding posts for banana plugs, spades, or bare
  wire; it does not contain a speaker enclosure.
- The Class-D channels are bridge-tied outputs. Each speaker uses its own `+` and
  `-` pair; the black terminals are not common ground and must not be joined.
- Daytime playback must remain clean at ordinary television volume and somewhat
  above it. Maximum party or hi-fi demonstration volume is not a requirement.
- Source changes, codec changes, network dropouts, seeking, pausing, and transitions
  between music and generated sounds must not create clicks, bursts, or unsafe
  volume jumps.

### Daytime music and source handling

- The baseline is deliberately local: no Spotify Connect, AirPlay, cloud music
  account, or remote service is required.
- Support MP3, FLAC, and WAV from an SD card and a read-only home-network library.
  Evaluate AAC/M4A, ALAC, Ogg Vorbis, and Opus against real files, decoder licences,
  memory, and metadata needs. Bluetooth audio and USB storage are future options,
  not baseline requirements.
- Use SMB 2/3 as the first network-share candidate because it matches common Windows
  and NAS folder libraries. Compare UPnP/DLNA only if it materially improves setup
  or browsing; never require the internet to play local music.
- Provide both **Folders** and **Albums** views. A folder/album can play in track order,
  repeat, or shuffle; the complete library can also shuffle. Use embedded track/disc
  tags where valid, then natural filename order as a predictable fallback.
- Preserve queues and resume position across a normal restart. If a network library
  disappears, stop or skip cleanly and leave SD/procedural audio available rather
  than blocking the device.
- Basic browsing and playback must work from the front panel. The local web interface
  provides richer browsing, search, queue editing, library setup, and configuration
  without requiring a touchscreen or cloud account.
- Preserve one controlled digital audio path from every source through sample-rate
  conversion, volume, EQ, limiter, mute, and the stereo power amplifier.

### Local web interface and home Wi-Fi

- Serve a responsive web interface directly from the device with no external CDN or
  internet dependency. The physical controls and browser are adapters over the same
  control model, so they cannot disagree about source, queue, volume, timer, sleep
  state, or procedural settings.
- First-time setup uses a deliberate physical action to start a temporary,
  time-limited `SomnaSound-XXXX` setup network protected by a unique, temporary WPA2
  key shown on the red display. A captive setup page scans nearby networks, accepts
  the home password, tests the connection, and keeps the setup network available
  until the new credentials work.
- Production Wi-Fi should support 2.4 and 5 GHz, WPA2-Personal and WPA3-Personal,
  DHCP, and routers that use one SSID with band steering. WPS may be evaluated as a
  physical convenience fallback but is not the only or primary setup route.
- After joining the home network, advertise `somnasound-XXXX.local` using mDNS and show
  the assigned IP address on demand on the red display. Configuration must remain
  recoverable when mDNS, captive-portal detection, or the router internet connection
  is unavailable.
- Store Wi-Fi and network-share credentials encrypted, never display them again, and
  provide physical-confirmation flows for replacing credentials, factory reset, and
  exposing sensitive reports. The accepted baseline is HTTP on the trusted home LAN,
  with no cloud relay, WAN listener, automatic port forwarding, UPnP exposure, or raw
  sensor stream. Wi-Fi and share credentials are entered only during a physically
  initiated, time-limited setup session and are never returned by the normal web UI.
  Report access still requires a local pairing/PIN or physical-confirmation design;
  HTTP is a conscious appliance trade-off, not permission to leave reports open to
  every device on the network.

### Clock and timekeeping

- Use a hardware real-time clock while powered for sleep windows, reports and history.
  Do not fit a backup battery: after full power loss, synchronise from NTP at startup
  when network/internet access is available or let the user set time from the front
  panel/local web interface. Support configurable time zone and British Summer Time
  behaviour.
- The red clock is available on demand and may remain visible in a user-enabled
  daytime mode. During a sleep state it follows the ordinary 30-second fade and
  hardware-off rule; there is no always-on bedroom clock light.

### Local sleep history and optional Garmin context

- Show a large plain-language morning summary first, with a detailed on-device and
  paired local-web timeline available on demand. Retain a local history so the user
  can compare nights without an external account. Retain derived nightly details and
  trend history indefinitely unless the user deletes them; do not retain raw bedroom
  audio or imagery. Provide per-night, date-range, all-history, and factory-reset
  deletion paths.
- After a report finalises, maintain a plain, versioned, integrity-checked portable
  backup of that derived history on the SD card. It has no password, encryption, or
  device lock-in and imports directly to a future Somnasound; anyone with physical
  access to the card can read it. A missing, full, or corrupt card cannot interrupt
  an active sleep session; report the backup condition after waking instead.
- Provide an explainable personal trend score rather than a health or medical score.
  It compares estimated sleep opportunity, continuity/interruptions, candidate-event
  burden only where signal quality is adequate, and selected optional Garmin context
  against the user's own rolling baseline. Each score shows why it changed and can
  say “not enough reliable data.”
- Garmin Connect Personal API is an optional user-owned pull integration. The user
  supplies/revokes their own credentials locally and selects the data to use; Garmin
  sleep/health context is a comparison input, never required for core operation or
  presented as clinical truth. Internet, Garmin token, or Garmin-sync failure leaves
  Somnasound fully functional and marks that comparison unavailable.

### Firmware updates

- Version 1 updates are user-initiated from an SD card only. The device does not poll
  GitHub, download firmware from the internet, retain GitHub credentials, or install
  updates automatically.
- Verify the update's intended hardware model, version, integrity, and release
  signature before installing it to an inactive internal firmware slot. Retain the
  known-good slot and roll back automatically after a failed update or interrupted
  boot. SD update media cannot interrupt an active sleep session.
- Boot firmware, operating configuration, active report history and the local web
  interface run from internal non-volatile storage. SD storage is removable
  convenience media for music, portable history backup and update files; its removal
  or failure cannot stop core playback, sensing, timekeeping or local control.

### Procedural soundscapes

- Soundscapes must evolve continuously without an audible short recording loop.
  Use stateful synthesis, filtered noise, slow modulation, stochastic event
  scheduling, spatial variation, and legally sourced one-shot recordings where
  synthesis alone is unconvincing.
- Initial mode families are white, pink, and brown noise; fan/air; rainfall;
  thunderstorm; ocean; waterfall/stream; wind; and fireplace. The architecture must
  allow additional modes without changing the real-time audio interface.
- Each nature mode should expose a small number of meaningful controls such as
  intensity and richness rather than a large synthesizer-style parameter menu.
- Thunder, wave impacts, drips, gusts, and similar events must vary in timing, level,
  filtering, stereo position, and selection. One-shot assets require provenance and
  redistribution rights; an open-source engine licence does not automatically cover
  its bundled or externally hosted recordings.
- Procedural generation must be deterministic from an optional seed for repeatable
  tests while choosing a fresh seed for normal listening.
- An optional adaptive-masking mode may react slowly to room noise, but must have a
  user-set maximum volume and must be validated against respiratory sensing and
  microphone echo cancellation before it can be accepted for sleep use.

### Front panel and display

- Use a non-touch front panel. The leading full-size mock-up places the display
  above two lower black-aluminium wheels: a left detented push-rotary menu/select
  control with Back above, and a right turn-only volume control with Mute above.
  This keeps volume permanently direct rather than mode-dependent and reduces the
  leverage of a selection press. Compare it with the display-between-wheels layout
  before PCB layout. Make wheels and buttons tactilely distinct; keep sound actions
  in the on-screen menu. Provide dedicated tactile Sleep and Sound buttons: Sleep
  starts saved sleep-session preferences directly, while its active-session stop
  behaviour must be explicit rather than an undiscoverable long press. Sound plays/
  pauses music and mutes/unmutes procedural sleep sound without ending monitoring;
  the display reports the precise action in plain language. Essential actions must
  not depend on a long press.
- The front display is red-only in normal operation, continuously dimmable, and
  electrically switchable fully off. Sleep mode defaults to display off; a control
  press may wake it briefly at the saved low brightness.
- The finished device requires red-only visible output or no visible output. The
  preferred display is the red monochrome variant in Palm Technology's 3.37-inch,
  240 x 128 PTOG2412□-A0 PMOLED family over SPI, powered through a hardware-default-
  off load switch. Its approximately 76 x 40 mm active area is taller than the
  standard 5.5-inch 256 x 64 wide-format alternative and can show genuinely larger
  text in a smaller enclosure. The exact red order suffix requires written vendor
  confirmation. Any alternate display is acceptable only if it passes the same
  red-emission, legibility, blackout, supply, lifetime, and availability evidence;
  no non-red screen is a product option.
- Thirty seconds after the last interaction, begin a two-second perceptual fade to
  black, then remove display power. Every user-visible light follows the same policy;
  there is no permanent standby, network, or breathing LED. Shorter 10- and 20-second
  timeouts remain available, but sleep mode never has an always-on setting. A dedicated
  control extinguishes everything immediately.
- The display should show source, volume, procedural mode/settings, timer, fault/setup
  prompts, and track/artist metadata when supplied. It must not require always-on
  status LEDs. Select its size and character set using real filenames and metadata,
  including long names and non-ASCII characters.
- Use conventional high-contrast sans-serif text. Primary bedside state and changed
  values target at least 16 mm capital height, with 9–12 mm secondary text. A sparse
  across-room view targets 25–30 mm primary text at 2–3 m. No essential instruction
  may depend on scrolling text. Validate from lying and standing angles with older
  and reduced-vision participants.
- Boot, network, fault, and standby behaviour must never produce an uncontrolled
  bright display or non-red light in the bedroom.

### Proposed operating states

- **Standby:** amplifier hardware-muted, sensing inactive, display and all visible
  indicators off; network wake behaviour remains an explicit user setting.
- **Day music:** selected local or network source active; front controls and red
  display available; sleep sensing and microphones are inactive.
- **Soundscape:** procedural audio active with intensity/richness controls; sensing
  remains inactive unless the user separately starts a sleep session.
- **Sleep session:** brown-noise playback may continue; radar, thermal sensing, and
  two microphones are active for report capture. Microphones stay off for every
  other playback mode. When the user enables sleep fade, sustained high-confidence
  sleep-like conditions may gradually fade brown noise to silence; sensing and
  report capture continue after audio stops. Poor confidence leaves the sound
  unchanged; silent brown noise never resumes automatically, including after an
  overnight return to bed. The display defaults fully off and the configured maximum volume
  applies. A configured sleep-opportunity window distinguishes an overnight wake or
  sustained out-of-bed interval from morning wake: within the window it is recorded
  as a candidate interruption/out-of-bed episode, not labelled with an unknowable
  cause such as a toilet trip, and the session continues. Clear continued activity
  is recorded as awake-like/wind-down rather than sleep, but the device does not
  claim it knows whether the cause is TV, a tablet, reading, or another activity.
  Only after the window may
  a conservative sustained awake-like state end the session and finalise the morning
  report; a brief wake, movement, or signal dropout does not. Physical Stop remains
  available.
- **Setup/diagnostic:** red prompts may remain visible; raw diagnostic capture still
  requires an explicit development build and operator action.

Transitions must preserve a single safe volume model, use click-free fades, and make
the active privacy state understandable without requiring a bright always-on lamp.

### Power and construction

- Use a black 3D-printed, softened-corner rectangular clamshell rather than a round
  router-like body. Prefer ASA or equivalent heat-capable engineering material over
  PLA, with heat-set threaded inserts and broad silicone/rubber feet. Keep plain
  unfilled plastic windows over the antenna/radar paths; do not metallise or paint
  those windows with conductive coating.
- Form the enclosure as a clamshell with a raised rear service spine/plinth. Its
  recessed, downward-facing connection bay contains the left/right red-black binding
  posts, 24 V DC input, SD access, and any required service connection. Cables plug
  upward into the underside of the rear overhang and route through a hidden rear gap,
  keeping the main body shallow and avoiding a wall-facing cluster of rearward plugs.
- The connection bay must be mocked up with the actual banana plugs, speaker cable,
  DC connector and SD card before the enclosure is frozen. It needs enough hand and
  bend clearance, positive strain relief, tactile labelling, thermal clearance and
  physical/RF separation from the display, microphones, antenna and amplifier.
- Use a calm, softened-corner landscape front panel, visually like an iPad mini on
  a stand: a shallow rectangular face rests at roughly 15° above a flat, slightly
  wider high-grip base. Centre the flush red display on that front. A compact
  rectangular rear service/power module supports it; its lower downward-facing bay
  accepts the 24 V and four speaker banana plugs bottom-up, so cables route through
  a hidden rear gap instead of projecting backward. The leading control layout puts a
  compact Back, Sleep and Sound row beneath the display and above lower left menu/
  select and right direct-volume wheels; compare this with the display-between-
  wheels layout in a full-size mock-up before enclosure CAD is committed.
- Use passive cooling only: conceal adequately sized inlet/outlet slots on the
  underside and rear service-plinth area, with a proven low-to-high natural airflow
  path. Keep the front and top unvented. Internal baffles must prevent boot/fault
  light from escaping through vents. Do not add a fan unless worst-case thermal
  evidence proves passive cooling inadequate.
- The product contains no mains-voltage circuitry. It receives safety-extra-low
  voltage DC from an external certified power supply.
- The selected power architecture is a 24 V external brick sized from measured
  amplifier demand, with input fuse/eFuse, reverse-polarity protection, surge and
  over-voltage protection, filtering, temperature monitoring, and hardware mute.
- A 19–20 V laptop-style supply remains viable at reduced amplifier headroom.
  USB-C Power Delivery is an option only if its usability benefit justifies the
  negotiation, connector, cable, and conducted-noise complexity.
- The production goal is a custom PCB containing compute, memory, radio, sensing,
  power conversion, and audio amplification. Development kits are allowed only as
  temporary feasibility tools. A small camera or microphone board is allowed when
  lens alignment or acoustic placement makes it mechanically superior.

Somnasound is being designed as one finished personal device, not as a sequence of
consumer prototypes. Engineering samples and a factory first article are verification
artifacts for this same final architecture: they prove audio, thermal, RF, optical,
safety, and manufacturing evidence before irreversible enclosure, PCB, and BOM
commitments.

The manufacturing route is selected from matched, production-intent quotes rather
than assumed from board price. Quote PCBWay as the overseas partial-turnkey benchmark
alongside UK/EU contract manufacturers, starting with Newbury Electronics. The
selected supplier fabricates the board, sources approved standard parts, performs
SMT/THT assembly, programming, and the agreed functional test. The owner may consign
the specialist red OLED for installation and sources the external certified 24 V UK
power brick separately. No component substitute is permitted without written approval
against the approved BOM.

The reference speakers are the Monitor Audio Silver 1 pair (2014 generation).
Published specifications list a nominal 8-ohm load, 87 dB sensitivity, a 45 Hz to
35 kHz frequency response, and a recommended amplifier range of 40 to 100 W. The
24 V TAS5825M-class amplifier baseline provides enough clean headroom for both sleep
audio and the requested daytime television-to-moderate listening levels; it does not
target the speaker's maximum output. Verify the rear labels, measure DC resistance,
and test the final supply before fixing limiter and protection settings.

### Respiratory-event ambition

- Measure respiratory movement, sound, gross motion, and signal quality with
  synchronized timestamps.
- Detect and record candidate breathing pauses or irregular patterns for wellness
  review in a morning report; the device does not issue real-time breathing alarms
  and is not a life-safety monitor.
- Distinguish “no detected movement” from “no airflow.” Obstructive events can
  retain breathing effort, so radar/camera chest movement alone cannot establish
  that airflow stopped.
- Version 1 includes a low-cost MLX90640 32 x 24 thermal array as an additional
  nose/mouth heat-pattern and signal-quality input. It is an airflow proxy only;
  it neither proves airflow nor changes the wellness, non-diagnostic claim.
- The MLX90640 must pass a defined bedside signal-quality test in its final
  enclosure/window. If it does not, retain the evidence and consider FLIR Lepton
  only as a Version 2 board redesign; do not burden Version 1 with Lepton's cost
  and video-interface complexity on specification alone.
- Preserve consented research-mode data and model/version traceability so candidate
  algorithms can later be compared with appropriate reference equipment and a
  future regulated pathway is not designed out.

### Privacy and trust

- Raw sensor streams remain in volatile processing buffers and are not persisted or
  transmitted in normal operation.
- Debug capture requires an explicit development build and visible operator action.
- Stored events use a documented schema, retention policy, and user-controlled
  deletion path.
- “Zero knowledge” is reserved for a protocol with a cryptographic proof; local
  processing and buffer zeroisation are described literally.

## Candidate system directions

### A. Radar-first

Use 60 GHz radar for presence, movement, and respiration candidates, plus digital
microphones for acoustic events. This best matches darkness and bedroom privacy,
but must prove that it can extract the desired sleep metrics through bedding and at
real bedside geometry. It cannot be assumed to provide camera-level pose detail.

### B. Future-only NIR vision

Do not include a camera, NIR illuminator, camera window, or camera-processing path
in Version 1. A 940 nm-sensitive camera might provide richer posture and movement
features in a later redesign, but it adds optical safety, heat, privacy perception,
image-pipeline, enclosure-window, and regulatory complexity. Reopen it only when
measured benefit justifies that cost.

### Version 1 sensing baseline

Use synchronized 60 GHz radar, the MLX90640 thermal array, and two local digital
microphones. Radar provides chest-movement/effort candidates; thermal sensing adds
a coarse nose/mouth heat-pattern proxy; microphones add snore, breath and cough
context. Playback reference and echo-cancellation evaluation are mandatory because
the same product drives external speakers.

NIR remains an optional future signal for posture, movement, occlusion, and
confidence, not an assumed substitute for thermal airflow proxy. It is only added
after it demonstrates material value and passes its optical, dark-room, privacy,
thermal, and integration evidence.

### C. Low-cost integration prototype

Use an ESP32-S3-class module to prove Slack/gateway flows, basic audio, and sensor
plumbing. This is a software and integration prototype, not evidence that the same
processor meets final inference or audio requirements.

The first feasibility phase should compare A and B using development kits before a
custom PCB. It should not combine every sensor into one board until the minimum
sensing set is supported by recorded data.

### D. Local media and control modules

Keep three deep modules independent of processor placement:

- the **media library** hides SD, network-share discovery, indexing, metadata, folder
  ordering, album views, queue creation, seeded shuffle, reconnects, and missing files;
- the **playback engine** hides decoding, buffering, sample-rate conversion, gapless
  transitions where supported, volume, limiter, mute, and the playback reference; and
- the **control model** owns observable device state and commands used by both the
  front-panel and web-interface adapters.

A fourth **network provisioner** module owns temporary setup Wi-Fi, credential
replacement, reconnect policy, DHCP, and local discovery.

Production uses two processor domains on the custom PCB:

- the **deterministic audio/sensing domain** owns the master audio clock,
  brown-noise generation, amplifier feed, radar, thermal array, microphones,
  immediate mute/safe states, and local signal-quality processing; and
- the **connectivity/media domain** owns Wi-Fi, provisioning, HTTP UI, SD/SMB
  browsing/indexing, music decoding, and updates.

They communicate through a deliberately narrow, buffered private interface. The
connectivity/media domain may request state changes and supply buffered PCM, but it
does not own a live audio clock, raw microphone data, or the hardware mute path.
This prevents Wi-Fi/file-system bursts and network faults from compromising quiet
playback or sensing. Exact processors remain subject to workload, lifecycle,
security, RF-noise, thermal, power, and cost measurements. Production remains a
custom PCB rather than a Raspberry Pi or wired development-board assembly.

During a sleep session, brown-noise generation, the audio clock, amplifier control,
radar, thermal sensing, microphones, and safe volume state remain operational if the
connectivity/media domain crashes, restarts, loses Wi-Fi, loses the web interface, or
cannot reach a music library. The fault is recorded and that domain recovers in the
background with no audible gap, click, unsafe volume change, or visible light. Music
from an unavailable SD/network source may instead stop cleanly.

A full power loss, unplug, or power cycle is different: it starts a fresh silent
state. Amplifier mute is asserted, sensing and microphones are off, and no prior
audio, timer, queue, sleep session, or volume resumes automatically. Wi-Fi and
library recovery may occur silently in the background, but playback or a sleep
session requires a new deliberate action.

## Staged plan and gates

### Gate 0 — intended use and claims

Define a general-wellness first release that reports measured breathing-pattern
irregularities without diagnosing apnoea, while preserving a future medical route.
Complete when intended users, claimed outputs, explicit non-claims, escalation
language, and a regulatory review of that wording are recorded.

### Gate 1 — sensing feasibility

Capture consented development datasets with radar and, if acceptable, NIR vision.
Define ground truth and compare event accuracy, failure modes, darkness, heat,
privacy perception, and compute load. Complete when one minimum sensor set meets
agreed metrics across representative bedrooms.

### Gate 2 — acoustic proof

Build amplifier/bookshelf-speaker and microphone test rigs around the accepted
TAS5825M baseline. Measure idle noise,
tonal spurs, frequency response, maximum clean level, clicks/pops, EMC coupling,
and microphone contamination during brown-noise sleep playback. Complete when the
chosen signal chain passes numeric and listening tests at the intended bed distance
and at the requested daytime listening level.

### Gate 3 — compute and connectivity

Benchmark the actual sensing and audio pipelines on candidates for the two selected
domains. Decide the exact processors, their private interface, memory, secure boot,
update strategy, and power tree from measurements. Complete when worst-case CPU/NPU,
RAM, thermal, latency, radio coexistence, SD/network-library indexing, codec,
web-interface, update margins, clock ownership, and fault containment are recorded.

### Gate 4 — modular engineering validation

Integrate proven sensing and audio modules with a development carrier. Implement
the event schema, local storage policy, Wi-Fi provisioning, SD/network media library,
and local web interface. Complete after overnight reliability, recovery, privacy,
LAN-isolation/access-control, and acoustic tests pass. Include a physical front-panel
mock-up and a continuous 24-hour playback
test that switches between SD files, a network share, and procedural modes while the
web interface and front controls remain consistent.

### Gate 5 — custom electronics and enclosure

Create the KiCad design, acoustic enclosure, thermal model, compliance pre-scan,
manufacturing test points, and board bring-up plan. Complete after schematic/layout
reviews and first-article validation; only then freeze a production BOM.

### Gate 6 — integrations and product validation

Validate SD and network-library management, Wi-Fi onboarding across representative UK
home routers, local-web security, accessibility, recovery, and offline behaviour.
Separately, add Apple Health through a permissioned Apple-platform app and Garmin
through its approved developer program only if those integrations remain desired.
Validate claims, update obligations, and longitudinal performance before release.

## Current engineering principle

Evaluation boards and measurement fixtures are disposable learning tools. The
production architecture remains revisitable until the relevant gate has objective
evidence and an `ACCEPTED` decision record.

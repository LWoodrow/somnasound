# Streaming, procedural ambience, and front-panel research

Date: 2026-11-01  
Status: **RESEARCH — not an accepted architecture decision**

Owner update, 2026-11-01: Spotify Connect and AirPlay are no longer product
requirements. Sections discussing them remain as decision history. The accepted media
baseline is SD card plus a read-only home-network library and a local web interface;
see section 7 and D-024/D-028.

This note evaluates the newly requested daytime music, local music, procedural
ambience, physical controls, and red display. It deliberately separates sourced
facts from engineering inferences and recommendations.

## Executive conclusion

The requested product is feasible without changing the 24 V amplifier baseline.
The Monitor Audio Silver 1 speakers need only a fraction of the TAS5825M's available
power at ordinary television-like listening levels.

The selected media scope is now SD card and a read-only home-network library, with no
Spotify Connect or AirPlay requirement. This removes the commercial streaming-SDK
constraint and makes a capable MCU plausible again. Processor placement remains open
until SD/SMB indexing, decoding, web serving, Wi-Fi recovery, procedural audio, and
sensing have been benchmarked concurrently.

The two linked GitHub projects are useful inspiration, but neither is a complete
procedural sound engine. Somnasound should build a new real-time C++ DSP engine and
use only recordings with documented commercial rights.

## 1. Sound+Sleep reference product

### Verified facts

The linked Amazon item is the Adaptive Sound Technologies Sound+Sleep ASM1002. Its
listing describes 30 environments, adaptive response to room noise, a 30/60/90/120
minute timer, automatically dimmed panel lighting, and a 3.5 mm output
([Amazon listing](https://www.amazon.co.uk/Adaptive-Sound-Technologies-Global-Machine/dp/B002SMJQT4)).

The manufacturer's manual gives the more useful interaction model:

- a rotary selector for ten categories: train, city, meadow, rainfall, ocean, brook,
  fireplace, meditation, white noise, and waterfall;
- separate volume, power, display, timer, adaptive, and richness controls;
- three richness levels that dynamically add occasional details; and
- a display-off function where changing a setting wakes the panel for 15 seconds
  before it goes dark again.

The reference product's panel indicators are orange, so its lighting should not be
copied. The control pattern and temporary display wake-up are useful references.
([Sound+Sleep owner's manual, pp. 4–8](https://www.soundofsleep.com/wp-content/uploads/2016/06/SOUND-SLEEP-User-Manual.pdf))

### Engineering inference

"Richness" is a useful user concept: one mode can range from steady and unobtrusive
to a more eventful soundscape without creating a long list of near-duplicate modes.
It is also safer than adaptive volume as a default. Automatic gain changes could
disturb sleep and contaminate microphone measurements unless their rate, maximum
level, and sensing interaction are tightly constrained.

### Recommendation

Retain a `calm / natural / vivid` richness control, but make adaptive volume opt-in
and bounded. Sleep mode remains fully dark; touching a control may show a very dim
red status for a configurable short period, including an `always off` choice.

## 2. Audit of the linked procedural-audio repositories

### Verified facts: `panmona/stormsimulator`

The repository is an archived browser application, not a synthesized audio engine
([pinned revision](https://github.com/panmona/stormsimulator/tree/b48740a77d18bfa314db2046668ef185b8404170)).

- Rain is one decoded `rain.wav` with `loop = true`
  ([source](https://github.com/panmona/stormsimulator/blob/b48740a77d18bfa314db2046668ef185b8404170/js/rainSound.js#L18-L55)).
- Thunder randomly selects one of seven WAV recordings
  ([source](https://github.com/panmona/stormsimulator/blob/b48740a77d18bfa314db2046668ef185b8404170/js/thunder.js#L44-L64)).
- Its useful procedural elements are randomized storm timing, flash intensity, and a
  distance-based delay before thunder
  ([lightning](https://github.com/panmona/stormsimulator/blob/b48740a77d18bfa314db2046668ef185b8404170/js/lightning.js#L27-L43),
  [distance delay](https://github.com/panmona/stormsimulator/blob/b48740a77d18bfa314db2046668ef185b8404170/js/thunder.js#L83-L99)).
- The code is MIT licensed, but the audio is deliberately absent because its author
  did not have permission to redistribute it
  ([README](https://github.com/panmona/stormsimulator/blob/b48740a77d18bfa314db2046668ef185b8404170/README.md#L60-L73),
  [license](https://github.com/panmona/stormsimulator/blob/b48740a77d18bfa314db2046668ef185b8404170/LICENSE)).

Its recordings therefore cannot be reused. The timing, distance, and layer-control
ideas can be independently reimplemented in C++.

### Verified facts: `azuletto/rain_generator`

This is a Python/Pygame desktop prototype using NumPy, SciPy, `sounddevice`, and
threads
([pinned source](https://github.com/azuletto/rain_generator/blob/fa2142555d8fb31cf69efb12db04cedcc0ed3349/thunderstorm_simulator.py)).

- Its continuous rain bed is genuinely generated: Gaussian noise is passed through
  an eighth-order 1.8 kHz Butterworth low-pass filter and clipped
  ([source](https://github.com/azuletto/rain_generator/blob/fa2142555d8fb31cf69efb12db04cedcc0ed3349/thunderstorm_simulator.py#L101-L110)).
- It creates independent one-second blocks and does not preserve the filter state
  between them
  ([source](https://github.com/azuletto/rain_generator/blob/fa2142555d8fb31cf69efb12db04cedcc0ed3349/thunderstorm_simulator.py#L134-L153)).
- The droplet layer is commented/dead, while thunder randomly plays ten WAV files
  ([droplet code](https://github.com/azuletto/rain_generator/blob/fa2142555d8fb31cf69efb12db04cedcc0ed3349/thunderstorm_simulator.py#L107-L137),
  [thunder playback](https://github.com/azuletto/rain_generator/blob/fa2142555d8fb31cf69efb12db04cedcc0ed3349/thunderstorm_simulator.py#L217-L224)).
- The repository is MIT licensed, but provides no provenance or separate rights
  record for the included thunder WAVs
  ([license](https://github.com/azuletto/rain_generator/blob/fa2142555d8fb31cf69efb12db04cedcc0ed3349/LICENSE),
  [sounds directory](https://github.com/azuletto/rain_generator/tree/fa2142555d8fb31cf69efb12db04cedcc0ed3349/sounds)).

The top-level licence does not establish that the contributor owned every recording.
Treat those samples as unusable commercially unless their provenance is independently
proved.

### Engineering inference

Reinitialising a high-order filter for every one-second block can create periodic
transients. The prototype also lacks parameter smoothing, stereo decorrelation,
headroom management, a limiter, and real-time tests. Python/SciPy/Pygame are not the
right production dependencies, although the underlying
`PRNG -> persistent filters -> mixer` pattern ports cleanly to embedded C++.

### Recommendation: new Somnasound ambience engine

Build a small, deterministic C++ audio graph rather than porting either project:

```text
seeded PRNGs ─┬─ coloured/filter banks ─┬─ slow modulation ─┐
              ├─ droplet/wave events ───┤                   ├─ stereo mix
owned assets ─┴─ rare natural events ───┴─ spatialisation ──┤
                                                            └─ limiter -> I2S
```

The generator should preserve all filter and envelope state across small audio
blocks, smooth every user parameter, prevent DC and clipping, and use separate PRNG
streams for left/right decorrelation and events. A fixed seed must reproduce a test;
a fresh seed must create a new listening session.

Candidate mode families are:

- coloured noise: white, pink, brown, and user-EQ'd masking noise;
- mechanical: fan and ventilation;
- water: light rain, heavy rain, storm, ocean, brook, and waterfall;
- natural ambience: wind, forest/night, meadow, and fireplace.

Ocean, waterfall, and rain need distinct models rather than differently equalised
copies of one noise source. Thunder can be synthesized from shaped noise, resonators,
delays, and long reverberant envelopes. A hybrid engine using commissioned or
properly licensed one-shots will probably sound more natural, but every asset must
have a provenance record and redistribution rights.

"Non-looping" should be an acceptance test: no finite ambience bed is replayed and
no audible periodicity, boundary click, repeating event pattern, or tonal artefact is
detected in long-duration renders. It need not forbid occasional reuse of a licensed
one-shot when its timing, pitch, gain, stereo position, and processing vary.

## 3. Music sources and commercial constraints

### Verified facts

#### Spotify Connect

Spotify accepts commercial-hardware applications from companies rather than
individuals, recommends using an approved systems integrator, and provides its
embedded SDK only after the application, evaluation agreement, and NDA
([onboarding](https://developer.spotify.com/documentation/commercial-hardware/onboarding)).
Hardware partners must use the embedded SDK rather than the Web API
([FAQ](https://developer.spotify.com/documentation/commercial-hardware/implementation/faqs)).
Commercial release requires Spotify certification and a signed distribution
agreement
([technical requirements](https://developer.spotify.com/documentation/commercial-hardware/implementation/requirements/technical),
[launch process](https://developer.spotify.com/documentation/commercial-hardware/launch)).

The embedded SDK supplies a C API and compressed audio for the product to decode. A
target build depends on the selected chipset/toolchain, and the product needs mDNS,
HTTP/ZeroConf, credential-blob storage, and the required source-selection behaviour.
([implementation](https://developer.spotify.com/documentation/commercial-hardware/implementation),
[technical requirements](https://developer.spotify.com/documentation/commercial-hardware/implementation/requirements/technical))

#### Apple Music, iTunes, and AirPlay

AirPlay audio is an MFi licensed technology. MFi supplies private specifications,
certification tools, and components; royalties are disclosed only after licence
approval
([MFi FAQ](https://mfi.apple.com/en/faqs),
[programme process](https://mfi.apple.com/en/how-it-works)). Apple documents sending
audio from iPhone, iPad, or Mac to an AirPlay-compatible speaker on the same network
([Apple Support](https://support.apple.com/en-gb/105068)).

Public MusicKit targets Apple-platform apps, Android, and the web; it is not a public
general-purpose embedded receiver SDK
([MusicKit](https://developer.apple.com/musickit/)). Therefore a standalone custom
device should plan on licensed AirPlay or a licensed integration partner rather than
assuming that MusicKit can be placed in bare-metal firmware.

Current iTunes Store songs are DRM-free 256 kbit/s AAC, while older protected
purchases have device/authorisation restrictions
([Apple usage rights](https://support.apple.com/en-ie/guide/music/mus3e2346c2/1.6/mac/26)).
Supporting those DRM-free local files still means implementing AAC. Via LA states
that manufacturers of end-user AAC encoder/decoder products need an AAC patent
licence
([AAC licensing](https://www.via-la.com/licensing-programs/aac/)).

#### Bluetooth audio

Standard Bluetooth profiles do not require MFi
([MFi FAQ](https://mfi.apple.com/en/faqs)). A Somnasound receiver would use A2DP sink
for audio and AVRCP for transport/metadata controls. Bluetooth SIG says every
Bluetooth product must complete its qualification process before sale; an existing
qualified module/design can reduce testing but does not remove the product maker's
submission
([qualification](https://www.bluetooth.com/develop-with-bluetooth/qualify/),
[process guide](https://www.bluetooth.com/bluetooth-qualification-process-quick-start-guide/)).
The published adopter qualification fee is USD 12,000 from 1 March 2026
([fee schedule](https://www.bluetooth.com/fee-schedule/)).

Bluetooth is the broadest first input because the phone performs Spotify, Apple
Music, internet radio, or local-library playback. Apple notes that Bluetooth audio is
not lossless
([Apple lossless guidance](https://support.apple.com/en-euro/guide/iphone/iph14e213417/26/ios/26)).

#### Local files

FLAC's codec libraries use Xiph's BSD licence and are explicitly suitable for
commercial firmware
([FLAC downloads and licensing](https://xiph.org/flac/download.html)). The single-file
C/C++ `dr_flac`, `dr_mp3`, and `dr_wav` decoders are public-domain or permissively
licensed candidates
([dr_libs](https://github.com/mackron/dr_libs)). Vorbis and its embedded fixed-point
Tremor decoder are royalty-free, with BSD-style libraries
([Xiph Vorbis](https://www.xiph.org/vorbis/)).

### Engineering inference

Direct Spotify Connect and AirPlay materially increase software lifecycle, security,
business, and certification work. They also make the current small-MCU shortlist a
poor place to force the complete media stack. A maintained partner module is likely
to cost more per unit but avoids creating an unsupported DRM/network-audio platform.

Bluetooth is an excellent compatibility input but not the highest-quality path.
Local FLAC/WAV and network lossless playback are the cleanest paths; MP3 remains
useful for library compatibility. AAC/M4A should be an explicit commercial decision,
not silently added through an open-source decoder.

### Recommendation

Use three staged source classes:

1. **First proof:** Bluetooth A2DP/AVRCP and local WAV/FLAC/MP3 from removable or
   internal storage.
2. **Production streaming evaluation:** Spotify Connect and AirPlay through an
   approved integration partner.
3. **Optional formats/services:** AAC/M4A, Vorbis/Opus, UPnP/local-network libraries,
   and other services only after demand and licensing are recorded.

As one concrete candidate, StreamUnlimited's solder-down Stream210 integrates Linux,
Wi-Fi 6, Bluetooth, I2S, USB host/device, SDIO, display/control interfaces, secure
boot, and OTA support on a 25.4 x 27.5 mm SMT module
([Stream210](https://www.streamunlimited.com/stream210/)). Its vendor offers Spotify
Connect and AirPlay through StreamSDK
([StreamSDK](https://www.streamunlimited.com/streamsdk/)). This fits the requirement
for a custom main PCB; it is not a Raspberry Pi or a loose wired development board.
It remains a candidate until commercial terms, minimum order, lifecycle, service
certification, power, boot time, RF noise, and audio performance are known.

The preferred signal boundary is digital:

```text
Bluetooth / network module ─┐
local file decoders ────────┼─ source manager -> SRC/mixer -> limiter -> TAS5825M
procedural sound engine ────┘                         └──────> mic/AEC reference
```

Keep the procedural sleep engine available offline. Permit the radio/media module to
power down in local sleep mode to reduce RF activity, heat, and power, while retaining
an explicit option to stream overnight.

## 4. Front controls and red display

### Verified facts

True-red monochrome graphic OLEDs exist. Palm Technology's PTOG1206-A6 is a 1.3-inch
128 x 64 module offered in red, driven by SH1106G over parallel, SPI, or I2C
([manufacturer product page](https://www.palmtech.com.tw/product/oled-module/ptog1206-a6-series),
[datasheet](https://www.palmtech.com.tw/archive/product/item/files/oled/PTOG1206%E2%96%A1-A6.pdf)).
SH1106-family modules provide display-off and contrast control; a representative
module specification documents the power-down sequence and display-off command
([module specification](https://admin.osptek.com/uploads/OED_130_12864_W101_C30_12dfb6ffb3.pdf)).

Availability must be treated cautiously. For example, Newhaven's red 16 x 2
NHD-0216CW-AR3 is already marked end-of-life
([product page](https://newhavendisplay.com/2x16-character-red-slim-oled-module/)).

### Engineering inference

A 1.3-inch panel can show source, mode, volume, timer, and abbreviated track metadata,
but may be too small to read across a bedroom. OLED controller `display off` is not as
strong a guarantee as removing display power; a firmware crash can leave pixels lit.
OLED also needs burn-in mitigation if it is left on throughout the day.

### Recommendation

Prototype at least two true-red OLED sizes and evaluate them at the real viewing
distance. Use a smoked-red window, minimum contrast appropriate to darkness, pixel
shifting/daytime screen changes, and no white/blue status LEDs.

Power the display through a load switch whose hardware default is off. Sleep mode
should power-gate it after the timeout, not merely send a software blank command.
Boot, update, crash, and fault states must remain dark unless the user explicitly
wakes the display.

Recommended physical controls:

- a large tactile rotary encoder for volume, with push for play/pause or confirm;
- dedicated `source`, `sound/mode`, `previous`, `next`, and `timer/display` controls;
- a hardware mute path and a clearly distinguishable power/sleep control; and
- tactile shapes/spacing that remain usable without looking or illuminating labels.

The display should expose the active source, track/artist when permitted by the
source licence, procedural mode and richness, volume, timer, network state, and brief
fault/setup messages. It should never be required for the basic action of lowering
volume or muting playback.

## 5. Amplifier and 24 V power reassessment

### Verified facts

The speaker record is 8 ohms nominal and 87 dB sensitivity
([Monitor Audio Silver 1 specification supplied by the owner](https://www.hifispecs.com/monitor-audio-silver-1/)).
At 24 V, TI specifies the TAS5825M at 2 x 30 W into 8 ohms at 1% THD+N. It accepts
common sample rates from 32 to 192 kHz, includes an asynchronous sample-rate
converter, and specifies at least 110 dB A-weighted SNR and no more than 35 uV RMS
integrated noise
([TI TAS5825M](https://www.ti.com/product/TAS5825M)).

### Engineering estimate

Using the published sensitivity as 87 dB SPL at 1 m for 1 W, ideal free-field maths
gives the following approximate stereo levels:

| Electrical level | Two speakers at 1 m | Two speakers at 2.5 m |
|---|---:|---:|
| 0.1 W/channel | about 80 dB | about 72 dB |
| 1 W/channel | about 90 dB | about 82 dB |
| 30 W/channel | about 105 dB | about 97 dB |

This assumes both speakers contribute roughly +3 dB and distance contributes
`20 log10(distance)` loss. Rooms, placement, programme crest factor, speaker impedance,
and the meaning of the sensitivity specification will change actual measurements.
The estimate nevertheless shows that television-like daytime playback uses far less
than 30 W/channel on average and leaves useful transient headroom.

### Recommendation

Keep the 24 V TAS5825M as the quality baseline. Do not increase amplifier power merely
for this new requirement. Instead, validate low-level gain structure, hiss, radio
breakthrough, and volume-step behaviour, because most listening will occur below
1 W/channel.

Recalculate brick current after selecting the streaming/compute module. At maximum
clean stereo output, 60 W of speaker power corresponds to roughly 67 W from the
supply at 90% amplifier efficiency, before compute, radios, sensors, USB storage,
and design margin. A certified 24 V, 4–5 A brick is a plausible test range, not yet
a frozen rating. Conducted-noise and burst-load testing remain mandatory.

## 6. Decisions and proof work still needed

Current decisions and proof work are:

1. Daytime music playback and genuinely non-looping procedural ambience are accepted
   product requirements.
2. SD and a read-only home-network library are the accepted source baseline; Spotify
   Connect and AirPlay are out of scope.
3. Compare one capable processor with a split connectivity/media and sensing/audio
   design; the prior licensed streaming-module preference is withdrawn.
4. Prove SD filesystem behaviour, read-only SMB 2/3, MP3/FLAC/WAV, ordering, metadata,
   shuffle, recovery, and offline operation before adding optional sources or codecs.
5. Prototype the red-display size, optical filter, controls, and hardware blackout.
6. Define procedural-mode quality tests: long renders, blind repetition checks,
   click/pop and clipping scans, spectral/tonal analysis, CPU/memory limits, and
   overnight stability.
7. Repeat Gate 2 audio testing with Wi-Fi active, SD/network decoding under load,
   display switching, and the actual 24 V brick. Measure at the speaker terminals and
   bed, and record the playback reference supplied to sensing algorithms.

The work packages are: `procedural ambience DSP proof`, `local media, web control,
and Wi-Fi spike`, and `front-panel/display prototype`. None should freeze the final
processor or PCB until its acceptance evidence is complete.

## 7. Local-only media and UK home-Wi-Fi addendum

### Owner direction

The selected product baseline is local MP3/FLAC/WAV from SD card or a home-network
location, with folder/album browsing, ordered play, repeat, and shuffle. Spotify
Connect and AirPlay are out of scope. The procedural engine remains a new stateful
C++ implementation; the linked repositories remain references only.

### Verified BT-router facts

BT documents Smart Hub 2 as dual-band Wi-Fi 5 using WPA2 on both bands and Smart Hub
3 as dual-band Wi-Fi 6 using WPA3. BT hubs commonly use one SSID for both 2.4 and
5 GHz and steer capable clients between them. BT also documents WPS support, but a
SomnaSound design cannot assume users enable or understand it.
([BT hub comparison](https://cdn.storefront.btc.digital-cms.bt.com/help/broadband/learn-about-broadband/different-types-of-bt-hub),
[BT hub security](https://www.bt.com/help/broadband/learn-about-broadband/security-on-the-bt-hub),
[BT band settings](https://www.business.bt.com/help/guides/smart-hub-guide/smart-hub-using/how-to-change-smart-hubs-wireless-settings/))

### Recommended onboarding experience

1. A deliberate button hold starts a temporary, time-limited
   `SomnaSound-XXXX` setup network protected by a unique temporary WPA2 key; the red
   display shows that key and setup state without exposing saved credentials.
2. A phone or computer joins that network and receives a captive setup page. A fixed
   fallback such as `http://192.168.4.1` remains documented because captive-portal
   detection differs between operating systems.
3. The page scans both bands, the user selects the normal BT-style SSID and enters
   the Wi-Fi password, and SomnaSound attempts the new connection while keeping the
   setup network recoverable.
4. Credentials replace the previous known-good set only after association and DHCP
   succeed. Failure returns a specific reason and does not strand the device.
5. On the home LAN the device advertises collision-resistant
   `somnasound-XXXX.local` with mDNS. The front
   display can show its DHCP address if local discovery fails.

Production hardware should support 2.4 and 5 GHz plus WPA2-Personal and
WPA3-Personal. A 2.4-only prototype is useful, but accepting it for production would
need evidence that shared-SSID/band-steering routers do not create support failures.
WPS push-button setup may be an optional fallback, never the only route.

### Media and control seams

Use four deep modules with narrow interfaces:

- **media library:** SD and read-only SMB adapters, indexing, tags, folder/album
  views, natural order, queues, seeded shuffle, reconnect, and missing-file policy;
- **playback engine:** decoder selection, buffers, source-rate conversion, gapless
  transitions where possible, gain, limiter, mute, and the sensing playback reference;
- **control model:** the authoritative source, queue, state, volume, timer, display,
  soundscape, and sleep-session commands/status; and
- **network provisioner:** setup network, scanning, credential validation/storage,
  reconnects, DHCP, mDNS, and reset.

The physical panel and HTTP server are adapters over the control-model seam. SD and
SMB are adapters internal to the media-library implementation. This gives both user
interfaces identical behaviour and allows processor placement to change without
rewriting callers.

### Accepted local-web security boundary

The owner accepts HTTP for this internal appliance. A publicly trusted certificate
would require a real public DNS name plus automated validation and renewal
([Let's Encrypt certificate lifetimes](https://letsencrypt.org/ca/docs/cert-lifetimes/));
the CA/Browser Forum requirements prohibit publicly trusted certificates for internal
names such as `.local`
([Baseline Requirements](https://cabforum.org/working-groups/server/baseline-requirements/requirements/)).
A self-signed certificate would add browser warnings and local trust-store work
without removing maintenance.

The baseline is therefore HTTP on the trusted home LAN, with a narrow exposure
boundary: no cloud relay, WAN service, automatic router port forwarding, UPnP/NAT
traversal, or raw camera/audio stream. Wi-Fi and network-share secrets are entered
only during a physically initiated, time-limited setup session, stored encrypted,
redacted from logs, and never returned by the normal UI. Reports use a local
pairing/PIN or physical-confirmation control so LAN membership alone does not grant
unlimited access. Test IPv4 and IPv6 exposure and document that users must not
manually forward the service to the internet.

## 8. Display and physical-control selection

### Verified facts: legibility and the 2.42-inch baseline

The US Access Board's visual-sign rules are not a product-display requirement, but
they are a useful conservative reference for reduced-vision sizing. They specify a
16 mm minimum character height below 1.83 m viewing distance, then add 3.2 mm for
each additional 305 mm of distance. They also require a non-glare, high-contrast
light-on-dark or dark-on-light presentation, conventional letterforms, stroke width
of 10–30% of character height, and line spacing of 135–170%
([ADA Standards, section 703.5](https://www.access-board.gov/guidelines-and-standards/buildings-and-sites/about-the-ada-standards/ada-standards/),
[Access Board guide](https://www.access-board.gov/ada/guides/chapter-7-signs/)). The
standard is written for installed signs at specified mounting heights, so it should
be treated as a design proxy, not as a claim that Somnasound is ADA-compliant.

Palm Technology's 1.54-inch PTOG1206-A4 is a 128 x 64 native-red PMOLED option with
a 35.04 x 17.51 mm active area, SSD1309Z controller, and SPI/I2C/parallel interfaces
([manufacturer page](https://www.palmtech.com.tw/product/oled-module/ptog1206-a4-series)).
Its whole active height is only slightly greater than the 16 mm proxy minimum, so it
is not a reduced-vision target.

SAEF lists a 2.42-inch 128 x 64 PMOLED family with an approximately 55 x 27.5 mm
active area and SPI interface, with red among the available colour variants
([manufacturer page](https://www.saefdisplay.com/sale-43950110-2-42-inch-yellow-oled-display-128x64-dots-resolution-7-header-pin-spi-interface.html),
[family specification](https://www.saefdisplay.com/photo/saefdisplay/document/98846/SFOM242YZ7-12864WBYG-01%20Specification.pdf)). A comparable Winstar 2.42-inch panel
confirms the geometry: 55.01 x 27.49 mm, 0.43 mm pixel pitch, SSD1309, 3 V logic, and
6800/8080/SPI/I2C interfaces, but its listed colours omit red
([Winstar](https://www.winstar.com.tw/products/oled-module/graphic-oled-display/2_42-oled.html)).
Raystar likewise lists mature 2.42-inch families without a standard red option
([Raystar](https://www.raystar-optronics.com/oled-graphic-display-module/2.42-oled.html)).

At 0.43 mm pitch, a 40-pixel-high glyph is about 17.2 mm and a 48-pixel glyph about
20.6 mm. This is a calculation from the verified panel pitch, not a manufacturer
legibility claim. It means the 2.42-inch panel can meet the 16 mm sign-derived proxy
for one sparse, large bedside value, but doing so consumes most of its 64-pixel
height. It cannot also present comfortable multi-line track/setup text at that size.
The same proxy rises to about 18 mm at 2 m and 28 mm at 3 m, beyond a practical
margin-respecting glyph on this panel. Thus **2.42 inches is adequate for a close
bedside glance, but not a defensible across-room reduced-vision interface**.

### Verified facts: larger custom-PCB candidates

| Candidate | Verified active area and format | Interface / supply facts | Red and lifecycle caveat |
|---|---|---|---|
| Palm PTOG1206-B3, 2.70-inch PMOLED | 61.41 x 30.69 mm, 128 x 64, 0.48 mm pitch | Parallel, SPI, I2C; SSD1327ZC | Red is listed. The public product page does not state supply rails, guaranteed lifetime, MOQ, or production-longevity terms; obtain the exact red datasheet and written supply status before layout ([manufacturer page](https://www.palmtech.com.tw/product/oled-module/oled-module-ptog1206-b3-series)). |
| Palm PTOG2412-A0, 3.37-inch PMOLED | 75.58 x 40.30 mm, 240 x 128, approximately 0.315 mm pitch | Parallel or SPI; SSD1322Z2 | Red is listed, but the catalogue does not establish a stocked suffix or production guarantee. It has the best native-red active height found in the current Palm standard range ([manufacturer catalogue](https://www.palmtech.com.tw/product/oled-module?page=5)). |
| Display Visions EA DOGXL160-7 LCD plus EA LED78X64-R | 69.265 x 42.833 mm, 160 x 104; separate 73 x 47 mm backlight active area | 2.6–3.3 V LCD; SPI variants or I2C; red backlight requires current limiting and the complete assembly is through-hole, not reflow | A red backlight is an orderable manufacturer option and is specified for 100,000 hours, but its optical result with the black FSTN-negative glass must be bench-checked; the manufacturer's combination table does not specifically recommend red for that glass ([manufacturer datasheet](https://www.lcd-module.de/eng/pdf/grafik/dogxl160-7e.pdf)). |
| Winstar WEX/WEN025664D, 5.5-inch PMOLED | 135.65 x 33.89 mm, 256 x 64, 0.53 mm pitch | 3 V; 6800, 8080, or SPI; SSD1322 | Current standard colours are white, yellow, and green, not red. A deep-red window would need measured leakage, brightness, uniformity, and off-state tests; the large diagonal mainly adds width, not the 40 mm active height of the 3.37-inch Palm ([manufacturer page](https://www.winstar.com.tw/products/oled-module/graphic-oled-display/wen025664d.html)). |

The Palm 2.70-inch 256 x 64 and 3.12-inch 256 x 64 families may sound larger, but
their published active heights are only 16.61 and 19.18 mm respectively. They do not
solve the large-character problem; diagonal alone is a misleading selection metric
([Palm catalogue](https://www.palmtech.com.tw/product/oled-module?page=5)). No cited
manufacturer promises a fixed multi-year production life for the proposed exact
OLED ordering codes. A redesign-compatible FPC/connector strategy, last-time-buy
policy, or qualified second source is therefore still required.

### Recommendation and decision gates

Do not use a touchscreen. It duplicates the richer browser UI, is harder to operate
by feel, increases accidental bedside activation and fingerprints, and makes a
dark-by-default panel harder to navigate.

Set two explicit readability targets:

- **close bedside (roughly 0.5–1.5 m):** 16 mm minimum cap height for the primary
  value or state, with 9–12 mm secondary labels only where the same information is
  available in the browser UI; and
- **across room (roughly 2–3 m):** 25–30 mm primary cap height, one short status at
  a time, with no dependence on scrolling metadata.

Use conventional, non-condensed sans-serif glyphs, strong but not filled-in strokes,
generous spacing, native red on black where possible, and a matte/non-glare front
window. Essential states must not depend on colour alone. These are recommendations
informed by the Access Board criteria, not verified performance for any panel or any
individual user's vision.

For production-intent display validation, use the 3.37-inch Palm red panel as the
preferred finished-device candidate. It can render an approximately 25–30 mm glyph
at 80–96 pixels while preserving some vertical margin. The 2.42-inch panel is a
measurement baseline only, not a preferred product choice. Any alternative is
acceptable only if it provides red-only visible output and satisfies identical
legibility, blackout, supply, lifetime, and availability gates.

Before schematic freeze, test both sizes with the intended matte red window at 0.5,
1, 2, and 3 m, from lying and standing angles, using at least one older or
reduced-vision participant. Record the smallest reliably read font, minimum usable
night brightness, spectral leakage, off-state blackness, and whether long labels
truncate. Also require written vendor confirmation of the exact red suffix, sample
availability, logic/display rails, FPC drawing, MOQ, rated luminance/lifetime, and
change/end-of-life notification policy. These are unresolved procurement gates, not
properties established by the catalogue pages.

The sleep behaviour remains dark by default. After a deliberate control action, hold
the display for 30 seconds, fade perceptually over two seconds, then remove
display/backlight power through a hardware-default-off load switch so reset, update,
crash, and sleep are truly dark rather than merely showing black pixels. Provide
10- and 20-second shorter options, plus `always dark` and immediate display-off
controls; sleep mode has no always-on setting and network traffic or notifications do
not wake the display. These timeout/fade values are product recommendations to
validate in sleep trials, not standards. The existing Sound+Sleep reference's
15-second temporary wake remains a useful precedent
([owner's manual, pp. 4–8](https://www.soundofsleep.com/wp-content/uploads/2016/06/SOUND-SLEEP-User-Manual.pdf)).

Bourns specifies the 11 mm PEC11L contacting encoder with push switch for 100,000
rotational cycles and 100,000 switch actuations
([product page](https://www.bourns.com/products/encoders/details/contacting-encoders/pec11l),
[datasheet](https://www.bourns.com/docs/Product-Datasheets/PEC11L.pdf)). Use a
PEC11L-class 20-detent/20-pulse encoder with hardware/firmware debouncing, subject to
the mechanical mock-up. Normal turn changes volume and push toggles mute; menus use
turn-to-highlight and push-to-select. Dedicated tactile controls cover
power/standby, play/pause, back, source/sound, previous/next, and timer/display.

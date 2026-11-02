# Somnasound architecture review research

Status: evidence review for planning, not an approved architecture  
Reviewed: 2026-11-01  
Source policy: first-party datasheets, vendor documentation/source repositories, standards bodies, and UK regulator guidance only.

## Executive finding

The product idea is feasible as a staged prototype, but the architecture currently commits too early to components, terminology, performance claims, and a cloud path that does not exist as written.

The most defensible plan is:

1. Keep normal sleep operation completely dark. Evaluate camera-free 60 GHz radar first. If the required outputs genuinely need vision, use 940 nm illumination with a camera/module whose 940 nm response and lack of an IR-cut filter are verified; retain 850 nm only as a measured fallback.
2. Prove the sensing algorithms and audio performance on development hardware before choosing the production processor or drawing a monolithic PCB.
3. Use ESP32-S3 for the fastest integrated camera/audio/BLE proof of concept, and benchmark the same representative inference workload on STM32N657. Select ESP32-S3 only if it meets the measured model, frame-rate, memory, and privacy requirements; otherwise use STM32N657 plus a separate BLE/Wi-Fi radio.
4. Reject K210 for new product work. Its official FreeRTOS SDK says it is no longer maintained and is not recommended for product development.
5. Treat MAX98357A and a current digital MEMS microphone as evaluation choices, not locked production choices. The amplifier is credible for a first prototype, but “no audible hiss” must be tested with the final speaker, gain, supply, layout, and enclosure.
6. Replace “zero-knowledge” with “data-minimised local processing,” and specify exactly where raw buffers can exist, how they are overwritten, what diagnostics may retain, and how firmware and telemetry are secured.
7. Put a phone or local gateway between BLE and internet services. Apple HealthKit requires an Apple-platform app with user authorization; Garmin Health API access requires approval and commercial use has a licence fee. Slack should be a planning/notification surface, not the primary store for identifiable health telemetry.
8. Remove the `<50 ms` product boot requirement until it has a user-centred definition. Secure boot, model loading, camera settling, and radio readiness make it a poor top-level target.

## 1. Compute and platform choices

### Facts

| Platform | Relevant first-party facts | Consequence |
|---|---|---|
| ESP32-S3 | Dual 240 MHz Xtensa LX7, 512 KB internal SRAM, external flash/PSRAM support, DVP camera interface, I2S, Wi-Fi and Bluetooth LE 5. Espressif describes vector instructions for NN/DSP acceleration, not a dedicated NPU. Secure boot and flash encryption are supported. ([product page](https://www.espressif.com/en/products/socs/esp32-s3), [datasheet](https://documentation.espressif.com/esp32_s3_datasheet_en.pdf)) | Lowest-friction single-chip prototype and potentially a product solution for small quantised models. Internal RAM is tight and camera/model buffers will normally rely on external PSRAM. |
| STM32H747 | Cortex-M7 up to 480 MHz plus Cortex-M4 up to 240 MHz, up to 2 MB flash and 1 MB RAM, camera interface and audio peripherals. The feature list does not include Bluetooth or a neural accelerator. ([ST product family](https://www.st.com/en/microcontrollers-microprocessors/stm32h747-757.html), [datasheet](https://www.st.com/resource/en/datasheet/stm32h747bi.pdf)) | Strong conventional MCU/DSP, but needs an external radio and performs ML on CPU. It should not be selected merely because “STM32H7” sounds production-grade. |
| STM32H7R7/H7S7 | 600 MHz Cortex-M7, 620 KB SRAM and only 64 KB boot flash; DCMIPP accepts a parallel camera but has no MIPI CSI-2 or full ISP pipelines. ([ST camera-interface note](https://www.st.com/content/st_com/en/technical-documents/an6211-introduction-to-digital-camera-interface-pixel-pipeline-for-stm32-mcus-stmicroelectronics.html), [product family](https://www.st.com/en/microcontrollers-microprocessors/stm32h7r7-7s7/products.html)) | Newer than classic H7, but still no NPU or integrated radio. External code/data memory is part of the design. It is an awkward middle option for this product. |
| Kendryte K210 | Dual 64-bit RISC-V cores, KPU CNN accelerator, DVP, I2S and audio/FFT functions are documented. ([official datasheet repository](https://github.com/kendryte/kendryte-doc-datasheet/blob/master/en/001.md?plain=1)) The official K210 FreeRTOS SDK explicitly states: “This project is no longer maintained. Not recommended for product development.” ([official SDK](https://github.com/kendryte/kendryte-freertos-sdk)) No integrated BLE is documented. | Historical capability is attractive, but lifecycle and software support make it a poor new-product foundation. |
| STM32N657 | 800 MHz Cortex-M55 with Helium, 4.2 MB contiguous SRAM, 600 GOPS Neural-ART NPU, parallel and two-lane MIPI CSI-2, ISP, H.264/JPEG, SAI/I2S and PDM filtering, secure boot; production status is active. ([product page](https://www.st.com/en/microcontrollers-microprocessors/stm32n657x0.html), [series overview](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html), [datasheet](https://www.st.com/resource/en/datasheet/stm32n657b0.pdf)) The listed connectivity does not include Bluetooth or Wi-Fi. | Best-supported current candidate here for serious local vision/audio ML, but it requires external flash and a separate radio and raises PCB/package, power, software, and boot complexity. |
| NXP i.MX RT700 | Up to 7.5 MB on-chip SRAM, Cortex-M33 compute and sense cores, HiFi 4 and HiFi 1 audio DSPs, an eIQ Neutron NPU, a digital microphone interface for up to eight channels, SAI, and secure provisioning. Its feature list does not include an integrated Bluetooth/Wi-Fi radio. ([NXP product page](https://www.nxp.com/products/i.MX-RT700)) | Strong paper candidate for a radar-plus-audio architecture where always-on DSP and microphone handling matter more than a full camera ISP; it still requires a radio and workload/toolchain validation. |
| Renesas RA8P1 | 1 GHz Cortex-M85, optional 250 MHz M33, 256 GOPS Ethos-U55 NPU, 2 MB SRAM, MRAM/external-flash options, parallel and MIPI CSI-2 camera interfaces, PDM/I2S audio and secure boot. It is available with an evaluation kit. ([Renesas announcement](https://www.renesas.com/en/about/newsroom/renesas-sets-new-mcu-performance-bar-1-ghz-ra8p1-devices-ai-acceleration), [vision application note](https://www.renesas.com/en/document/apn/building-vision-ai-application-using-ra8p1-mcu-ethos-u55-npu)) Its feature list does not include an integrated BLE radio. | Credible challenger to STM32N6, especially if Ethos-U tooling or on-package flash is valuable. It is worth a paper evaluation, not a third parallel prototype unless STM32N6 hits a blocker. |

ESP32-S3 camera support is real but bounded: Espressif's current camera component notes that 2 MP on S3 is only possible for still JPEG output, while current ESP-WHO examples include smaller vision models and supported S3 camera/audio boards. ([camera component](https://github.com/espressif/esp-video-components/blob/master/esp_cam_sensor/README.md), [ESP-WHO](https://github.com/espressif/esp-who)) STM32N6 has first-party object/face-detection, pose-estimation and audio-event/speech-enhancement examples, including both bare-metal and FreeRTOS builds. ([STM32 model zoo](https://github.com/STMicroelectronics/stm32ai-modelzoo), [N6 audio example](https://github.com/STMicroelectronics/STM32N6-GettingStarted-Audio))

ESP32-P4 is another current camera-rich device with MIPI CSI-2, ISP and H.264, but Espressif requires an external ESP32-C5/C6 for Wi-Fi/Bluetooth; it has AI acceleration instructions rather than the class of NPU in STM32N6/RA8P1. ([ESP32-P4 datasheet](https://documentation.espressif.com/esp32-p4_datasheet_en.html), [getting started](https://docs.espressif.com/projects/esp-idf/en/latest/esp32p4/get-started/index.html)) It does not simplify this architecture enough to lead the shortlist.

ESP-IDF itself is FreeRTOS-based: Espressif says all ESP-IDF applications and many components are written on its integrated FreeRTOS implementation. ([ESP-IDF FreeRTOS overview](https://docs.espressif.com/projects/esp-idf/en/release-v5.3/esp32s3/api-reference/system/freertos.html)) Therefore “ESP32-S3 plus no RTOS” means abandoning much of the supported stack, not merely choosing a simpler scheduler.

### Engineering inference

- The actual selection is not “K210 versus STM32H7.” That comparison is obsolete and underspecified.
- There are two sensible architecture levels: an integrated, low-cost ESP32-S3 solution if the measured workload fits; or an ML-focused STM32N657/RA8P1 plus radio companion if it does not.
- A processor cannot be selected responsibly until the input resolution, frame rate, model graph, quantisation, accuracy target, memory peak, and simultaneous audio/radio load are known.
- Tiny-YOLOv2 or generic MobileNet is not yet a product algorithm. Object detection is not automatically the right primitive for bed occupancy, movement vectors, respiratory motion, pose, or sleep/wake inference.
- “Bare metal” is a means, not a product requirement. The supported SDK, drivers, security updates, fault isolation, and reproducible timing matter more. A small RTOS task graph can still be deterministic.

### Recommendation

- **Reject K210 now.**
- **Do not select a generic STM32H7 now.** Reconsider it only if the proven algorithm is CPU/DSP-sized and an external radio is already acceptable.
- **Prototype track A:** ESP32-S3-WROOM module with octal PSRAM, DVP camera, digital mic and I2S amplifier. This tests the integrated low-cost ceiling.
- **Prototype track B:** STM32N6570-DK with its supported camera and the same representative model/data. This tests the higher-performance route.
- Make the product silicon decision at the benchmark gate below. Keep RA8P1 as the fallback challenger if STM32N6 tooling, supply, package or model support fails.
- Use vendor SDKs and an RTOS where that is the supported route. Preserve portability through application interfaces and board-specific adapters, not through a target-neutral empty CMake project.

### Unknowns to resolve

- What exact output is needed: occupancy, gross movement, pose, respiration proxy, snore events, or a clinically meaningful sleep metric?
- What minimum night-time frame rate and resolution meet that output?
- What measured accuracy, false-alarm rate and latency are acceptable?
- Is BLE sufficient for morning summaries, or is Wi-Fi required for updates/support?
- Is one SoC mandatory, or is an ML processor plus certified radio module acceptable?

## 2. Audio quality, hiss, interference and simultaneous sensing

### Facts

The MAX98357A is not inherently a poor audio part. Its current datasheet specifies 22.8 µV RMS A-weighted output noise, 103.5 dB dynamic range, 0.013% typical THD+N at 0.5 W into 8 ohms, selectable gains down to 3 dB, spread-spectrum Class-D switching, click/pop suppression and I2S input without MCLK. ([MAX98357A datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX98357A-MAX98357B.pdf)) Its evaluation-board guide recommends optional ferrite/capacitor EMI filtering when speaker leads exceed about 12 inches. ([evaluation guide](https://www.analog.com/media/en/technical-documentation/data-sheets/max98357devwlp-max98357evsyswlp.pdf))

A lower-noise, more controllable smart amplifier exists: MAX98390 specifies 10 µV output noise, 116 dB dynamic range, I2S/I2C control, integrated speaker current/voltage sensing, EQ/dynamics, click/pop suppression and 5.1 W at 1% THD+N. It is also a substantially more complex WLP device with an integrated boost converter. ([MAX98390 product page](https://www.analog.com/en/products/MAX98390.html)) MAX98389 is a simpler current alternative with 14.5 µV RMS output noise and digital input. ([MAX98389 product page](https://www.analog.com/en/products/MAX98389.html))

Output-noise voltage alone does not determine audible hiss. Speaker sensitivity, listening distance, amplifier analogue gain, available full-scale output, acoustic enclosure, power noise and layout all contribute. TI's gain guidance says the DAC signal should be as large as practical and amplifier gain as low as practical, because excess amplifier gain amplifies the noise floor and reduces dynamic range. ([TI gain application report](https://www.ti.com/lit/an/sloa105a/sloa105a.pdf))

For input, the older SPH0645/ICS-43434 class is no longer the obvious default. TDK's production T5848 provides I2S, 24-bit output, 68 dBA SNR, 133 dB SPL acoustic overload point and a 27 Hz to 18 kHz response in high-quality mode. ([product page](https://www.invensense.tdk.com/en-us/products/microphone/t5848), [datasheet](https://invensense.tdk.com/wp-content/uploads/2024/04/DS-000479-T5848-Datasheet-v1.0.pdf)) T5838 provides the same stated 68 dBA SNR/133 dB SPL class with PDM output. ([T5838 product page](https://www.invensense.tdk.com/en-us/products/microphone/t5838)) A newer higher-SNR option is Infineon's active-and-preferred IM72D128V: PDM, 71.5 dBA SNR, 128 dB SPL overload, and 11 Hz low-frequency roll-off. ([IM72D128V product page](https://www.infineon.com/part/IM72D128V), [datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-im72d128v-datasheet-en.pdf)) STM32N6 includes hardware intended to filter and decimate PDM microphones. ([ST MDF application note](https://www.st.com/content/st_com/en/technical-documents/an5795-how-to-use-multifunction-digital-filter-mdf-to-capture-sound-on-stm32-mcus-stmicroelectronics.html))

Digital microphones avoid a vulnerable board-level analogue signal, but they do not remove acoustic self-noise, supply coupling, clock/data radiation, port turbulence, mechanical vibration, enclosure resonances, or direct speaker sound. TDK requires close 0.1 µF decoupling with short, via-free connections and documents that the PCB/housing sound path changes microphone response. ([T5848 decoupling section](https://invensense.tdk.com/wp-content/uploads/2024/04/DS-000479-T5848-Datasheet-v1.0.pdf), [mounting note](https://invensense.tdk.com/wp-content/uploads/2015/02/Recommendations-for-Mounting-and-Connecting-InvenSense-MEMS-Microphones1.pdf))

Class-D power loops and outputs are fast switching nodes. TI recommends short strong power/ground connections, local bypassing, multiple ground vias and keeping output traces from coupling to other nets. ([TI Class-D layout guide](https://www.ti.com/lit/an/slaa902/slaa902.pdf)) General mixed-signal guidance favours a continuous ground reference with physical partitioning and controlled return-current paths; blindly split ground planes can increase EMI and crosstalk. ([TI reference-plane guidance](https://www.ti.com/lit/an/scea042/scea042.pdf), [Analog Devices mixed-signal guidance](https://www.analog.com/en/resources/analog-dialogue/articles/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html))

### Engineering inference

- MAX98357A is suitable for an acoustic prototype. Its 22.8 µV noise may or may not be audible with a sensitive speaker beside a quiet bed; a datasheet cannot settle that.
- Brown/pink noise playback will mask some amplifier hiss while playing, but hiss and clicks remain relevant during fades, silence and low-volume use.
- The speaker and enclosure will probably dominate perceived tonal quality. A high-quality amplifier cannot repair a resonant plastic cavity, port noise, under-sized driver or clipping.
- A physical “acoustic trench” is not enough for simultaneous playback and snore/ambient analysis. Direct airborne sound, enclosure vibration and playback spectrum will enter the microphone. The system needs mechanical isolation plus a known digital playback reference and likely acoustic echo/noise cancellation. Some measurements may need scheduled quiet windows.
- Radio bursts, IR LED current edges, camera clocks, PSRAM traffic and Class-D switching are all plausible interference sources. The risk is reduced by floorplanning, power design and scheduling, then confirmed by measurement.

### Recommendation

Use the following as the evaluation architecture, not yet the production BOM:

- 48 kHz, 24-bit internal audio path; deterministic waveform generation; click-free fades; limiter; lowest viable analogue amplifier gain.
- A/B test MAX98357A against one lower-noise I2C-controlled part such as MAX98390 or MAX98389 using the **same** speaker, power supply, level, enclosure and 20–30 cm listening distance.
- Compare T5848 where direct I2S simplifies the prototype with IM72D128V where a strong PDM filter path can exploit its lower self-noise. Evaluate two microphones only if the algorithm has a concrete beamforming/noise-cancellation use; two poor placements are not automatically better than one good placement.
- Give the microphone a sealed gasketed acoustic path, put it away from the speaker and enclosure vibration maxima, and add mechanical isolation/baffling.
- Route a digital playback reference into the capture DSP. Test microphone metrics with playback off, at normal playback, and worst-case playback.
- Use at least a four-layer PCB with a continuous ground plane. Partition RF/camera/mic/amp/LED-driver zones; keep Class-D output and LED-current loops short; keep them away from mic clock/data and the antenna; place local ceramic plus bulk decoupling at the amplifier; provide optional ferrite/LC footprints; and schedule bulk radio transfer after the sound session where possible.
- Provide hardware shutdown/mute so the amplifier is electrically quiet when not playing. Ensure boot and reset pin states keep it muted.

### Audio acceptance gate

Define and record before schematic lock:

- target SPL range at the pillow and at 1 m;
- no audible hiss, tones, ticks or pops in the intended quiet room at the sleeping position, assessed both by listeners and microphone/spectrum capture;
- output noise and spurious-tone spectrum with radio, camera and IR illumination independently on/off;
- THD+N and frequency response through the production-intent speaker/enclosure;
- captured snore/test-signal SNR with playback off and on;
- no clipping, thermal foldback or supply droop at maximum allowed level;
- graceful mute/fade through power-up, reset, OTA update and fault paths.

## 3. Sleep-compatible illumination

### Camera-free sensing option

Infineon lists sleeping monitoring, health care, heart monitoring, range, speed and
angle-of-arrival among the targets/capabilities of its active-and-preferred
BGT60TR13C 60 GHz radar sensor. It integrates three receive antennas and one
transmit antenna and is controlled over SPI. ([product page](https://www.infineon.com/part/BGT60TR13C),
[datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-bgt60tr13c-datasheet-en.pdf))
Radar requires no optical emitter and produces no bedroom imagery. Those are strong
fits for darkness and privacy, but the vendor capability list is not proof of
Somnasound's required sleep-event accuracy. Bedding, subject orientation, multiple
people, pets, fans, distance, and room geometry need representative testing.

**Recommendation:** evaluate radar before committing to a camera. Retain NIR vision
only if radar cannot provide a specifically required output, such as sufficiently
detailed pose or limb movement. This makes illumination an avoidable subsystem
rather than an assumed one.

### Facts

ams OSRAM states the core tradeoff directly: 850 nm gives higher CMOS camera sensitivity but can show a red glow; at 940 nm that glow is largely suppressed. Its application material says the perceived glow can be roughly 50–100 times lower at 940 nm and recommends 940 nm when faint glow is unacceptable. ([wavelength comparison](https://look.ams-osram.com/m/5cf0d1ee20a15031/original/Emitters-and-detectors-for-infrared-IR-touchscreens.pdf), [IR selection brochure](https://look.ams-osram.com/m/39974ab4771efcd2/original/aO-IRED-Brochure-112023.pdf))

The camera must be matched to the wavelength. OMNIVISION markets newer Nyxel devices specifically for high 940 nm quantum efficiency; its OG01A1B documentation calls out high NIR response at both 940 and 850 nm, while Nyxel2 reports 50% QE at 940 nm for the referenced pixel technology. ([OG01A1B](https://www.ovt.com/products/og01a1b/), [Nyxel2 announcement](https://www.ovt.com/press-releases/omnivision-unveils-nyxel-2-technology-extends-lead-in-no-light-near-infrared-cmos-image-sensing-performance-for-machine-and-night-vision)) The OV2640 was introduced in 2005 as a 2 MP mobile-camera sensor; current first-party material does not establish a guaranteed 940 nm system response. ([OV2640 announcement](https://www.ovt.com/press-releases/omnivision-takes-lead-in-mobile-cameras-with-new-2-megapixel-sensor/)) Module-level IR-cut filters can also block the desired illumination regardless of bare-sensor response.

Invisible does not mean intrinsically eye-safe. IEC 62471 covers LED photobiological hazards from 200–3000 nm, and ams OSRAM says final-product classification is the manufacturer's responsibility. ([IEC 62471](https://webstore.iec.ch/en/publication/7076), [OSRAM eye-safety note](https://look.ams-osram.com/m/563d74f4395107c7/original/Eye-safety-of-IREDs-used-in-lamp-applications.pdf))

### Engineering inference

- 940 nm is aligned with a dark bedroom, but will need more optical power or a more NIR-sensitive sensor than 850 nm for equivalent image quality.
- A cheap OV2640 module may work for an early motion experiment, but its old sensor, uncertain IR filter and uncharacterised 940 nm performance make it a poor production default.
- Pulsing IR synchronised to camera exposure can reduce average heat/power, but creates high current edges and can produce rolling-shutter banding if timing is wrong.

### Recommendation

- **Normal sleep mode: all visible emitters off.** This includes development-board LEDs, charger indicators, camera-module LEDs and accidental boot GPIO states.
- **Setup/interaction only:** if visible status is genuinely needed, use a deeply dimmed, baffled red LED under explicit user control and automatically extinguish it before monitoring. Do not use a continuously glowing red indicator as the default.
- **If night imaging remains necessary:** use 940 nm constant-current illumination, wide enough for uniform bed coverage, with a verified no-IR-cut camera and measured 940 nm response.
- Test 850 nm only as a fallback if 940 nm cannot meet image quality, heat and power limits. Any visible red points would then be a conscious product compromise.
- Select the camera after a dark-room comparison using candidate modules at the actual distance, lens/FOV, bedding reflectance and desired frame rate. Prefer a current monochrome/NIR-capable sensor when colour is not needed.
- Include an ambient-light sensor only if it drives a defined control policy; it must not be the sole safety control. Make IR current bounded in hardware and fail-off on reset/watchdog.
- Complete IEC 62471 assessment on the assembled optical system, including worst-case firmware current/duty cycle and close-range viewing.

### Optical acceptance gate

- no visible glow or status light detectable by a dark-adapted user from the bed in normal mode;
- required subject/bed coverage and movement-detection accuracy at 940 nm;
- acceptable image SNR at dark-room worst case and with different bedding/skin reflectance;
- acceptable LED/driver/enclosure temperature over an overnight run;
- no camera banding and no measurable audio interference from the LED drive;
- documented photobiological risk classification for the final optics/current/duty cycle.

## 4. Privacy, telemetry and external integrations

### Facts

Health telemetry and deliberate health inferences are special-category data under UK GDPR. ICO guidance explicitly includes fitness-tracker data and profiling that infers health status. ([ICO health-data guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data/))

Apple HealthKit is a repository on iPhone/Apple Watch. An app must add the HealthKit capability, request fine-grained user authorization, and access the store through `HKHealthStore`; users can restrict or revoke access. ([HealthKit overview](https://developer.apple.com/documentation/healthkit), [authorization](https://developer.apple.com/documentation/HealthKit/authorizing-access-to-health-data)) This is not a generic server-side Apple Health webhook for a Slack service.

Garmin says its Connect APIs are cloud-to-cloud; the Health API supplies JSON after the user's Garmin device sync and initial consent. Access follows approval, and commercial use requires a licence fee. ([program overview](https://developer.garmin.com/gc-developer-program/), [Health API](https://developer.garmin.com/gc-developer-program/health-api/))

BLE GATT connects a client and server locally. Slack's Web API is an internet HTTPS API at `https://slack.com/api/...`. A BLE device therefore needs a phone, computer, or gateway with both BLE and internet connectivity before data can reach Slack. ([Bluetooth LE primer](https://www.bluetooth.com/bluetooth-le-primer/), [Slack Web API](https://docs.slack.dev/apis/web-api/), [Bluetooth internet-gateway model](https://www.bluetooth.com/wp-content/uploads/2019/03/InternetGateways_WP_v01.pdf))

### Engineering inference

- “Zero-knowledge volatile SRAM privacy” is incorrect terminology. Zero knowledge has a specific cryptographic meaning; local processing and deletion are data-minimisation controls, not a mathematical proof that no party learns anything.
- Raw data is not “permanently destroyed” merely because a buffer goes out of scope. Copies may exist in PSRAM, DMA buffers, caches, crash dumps, debug streams, test fixtures or logs. The enforceable claim is that production firmware never intentionally persists or transmits raw media, buffers are bounded and overwritten, and diagnostic builds are separately controlled.
- Slack channels are a poor default location for identifiable sleep/health records: channel membership, retention, exports, third-party apps and broad bot scopes increase the data surface. Slack can still be useful for development coordination and low-sensitivity notifications.
- Security features do not create privacy on their own, but signed firmware, encrypted external memory where supported, debug lockout, authenticated updates, per-device identity and encrypted transport are prerequisites for credible local-processing claims.

### Recommendation

Adopt this data path:

```text
device sensors
  -> volatile raw buffers
  -> local feature/inference pipeline
  -> bounded numeric event store
  -> authenticated BLE GATT
  -> companion phone/local gateway
       -> Apple HealthKit locally (iOS only, with permission)
       -> Garmin cloud API (after program approval and consent)
       -> optional backend/report store
       -> Slack notification or pseudonymous summary, not raw health history
```

Create a threat model and data inventory before telemetry code. For every field record purpose, precision, retention, storage location, access, deletion and whether it can identify a person. Define separate production, consented diagnostic and development modes. Production should disable raw-media logging, core dumps containing raw buffers and unauthenticated debug access.

Use secure boot and firmware verification even if boot becomes slower. On ESP32-S3, secure boot and flash encryption are first-party features. ([ESP32-S3 security](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32s3/security/security.html)) On STM32N6 the ROM establishes a secure-boot chain and can authenticate/decrypt the first-stage loader. ([STM32N6 boot ROM](https://www.st.com/resource/en/user_manual/um3234-how-to-proceed-with-boot-rom-on-stm32n6-mcus-stmicroelectronics.pdf))

Decide the intended use early. MHRA guidance says general wellbeing monitoring is usually not a medical purpose, while automated calculation/interpretation used for diagnosis, prognosis or treatment may be a medical device. ([MHRA software flowchart](https://assets.publishing.service.gov.uk/media/64a7d22d7a4c230013bba33c/Medical_device_stand-alone_software_including_apps__including_IVDMDs_.pdf)) Avoid “sleep study,” diagnosis, sleep-stage, apnoea or treatment claims until evidence and the regulatory route support them.

### Unknowns to resolve

- Is the initial product strictly personal wellness, a research instrument, or intended to make medical claims?
- Is an iOS/Android companion app acceptable and who will maintain it?
- Does any telemetry need to leave the home, and if so why?
- Is Slack development-only, an internal operational alert surface, or a customer-facing report surface?
- What is the lawful basis/Article 9 condition, consent flow, retention period and deletion mechanism for any cloud health data?
- Has Garmin program access and likely commercial licensing been validated before it enters the critical path?

## 5. Boot, cost and production claims

### Facts

Espressif measures about 319 ms from power-on to `app_main` for an unoptimised ESP32-S3 test and about 27 ms after multiple optimisations. Those optimisations include suppressing logs, skipping image validation and calibration changes; ESP-IDF separately warns that skipping power-on validation prevents safe detection/fallback from flash corruption and that skipping secure-boot validation is a security compromise. ([startup experiment](https://docs.espressif.com/projects/esp-techpedia/en/latest/esp-friends/advanced-development/performance/reduce-boot-time.html), [ESP-IDF startup guidance](https://docs.espressif.com/projects/esp-idf/en/v5.2/esp32s3/api-guides/performance/speed.html)) This timing stops at application entry, not camera exposure settling, model readiness, clean audio output or BLE/Internet connectivity.

ST reports a typical 58 ms minimum for its STM32N6 OEM root-of-trust to reach a 128 KB application executing from external flash, increasing with application size. This excludes application peripheral/model readiness. ([STM32N6 OEMuRoT timing](https://wiki.st.com/stm32mcu/wiki/Security%3AOEMuRoT_for_STM32N6))

JLCPCB's official assembly pricing is a sum of setup, stencil, solder-joint, component, feeder/extended-part, inspection and other charges; shipping is calculated separately and import taxes can be additional. Exact assembly and component cost appears only after Gerber/BOM/CPL processing and part selection. ([assembly pricing](https://jlcpcb.com/help/article/pcb-assembly-price), [assembly FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs), [shipping](https://jlcpcb.com/help/article/shipping-methods-and-delivery-time))

### Engineering inference

- `<50 ms boot` is possible only under a narrow definition on some configurations, and can conflict with security/reliability. It is not credible as “fully sensing, audio-clean and connected” for the present architecture.
- A mains-powered bedside unit gains little user value from an extreme cold-boot target. Quiet, safe, deterministic recovery is more important.
- The claimed £95–£135 for five fully assembled custom boards plus enclosure is not evidence-backed. BGA/x-ray work, camera, optics, speaker, connectors, power, radio certification strategy, extended parts, assembly, rework, enclosure, shipping, VAT and yield are unknown. A volume £20–£25 unit cost is also premature without a BOM, manufacturing test, packaging, compliance and volume definition.

### Recommendation

Replace `<50 ms boot` with measured milestones:

- reset-to-safe hardware state (amp muted, visible LEDs and IR off);
- reset-to-first clean audio sample;
- reset-to-first valid sensor frame;
- reset-to-inference-ready;
- reset-to-local BLE connection;
- reset-to-cloud/report readiness.

Set targets only after prototype measurement. Do not weaken secure boot or image validation to win a marketing number.

Treat cost as a gate, not a promise. After schematic/BOM revision A and a placement draft, generate real quotes at 5, 50, 500 and intended production quantity, including assembly, modules, enclosure, speaker, power supply, test/programming, scrap allowance, shipping, VAT/duty and compliance amortisation.

## 6. Recommended decision gates

### Gate 0 — intended use and measurable product outputs

Decide wellness versus medical/research intent. Write one sentence for each output the device will produce and how a user acts on it. Remove unsupported “sleep study,” “sleep stages,” “HRV,” “SpO2,” “treatment” and diagnostic wording from the product requirement unless supplied by an authorised wearable source and clearly attributed.

**Exit evidence:** approved intended-purpose statement; output/data dictionary; top-level acceptance metrics; privacy/data-flow diagram.

### Gate 1 — algorithm feasibility before embedded optimisation

Collect consented representative test recordings offline using a conventional camera/microphone rig. Compare simple baselines (frame differencing/optical flow/audio DSP) with candidate ML models. Determine the smallest input/model that meets the defined output. Generic Tiny-YOLO/MobileNet should not be assumed.

**Exit evidence:** labelled dataset protocol; held-out metrics; failure analysis; model graph/weights; input resolution/rate; peak working memory; estimated operations; exact numeric feature output.

### Gate 2 — optical and audio bench prototypes

Run a radar feasibility test first. If vision remains necessary, run the 940-versus-850 camera test. In parallel, run the MAX98357A-versus-low-noise-amplifier test with production-intent speaker/enclosure geometry. Include RF, camera/IR where applicable, and simultaneous playback/capture interference tests.

**Exit evidence:** spectra, waveforms, dark-room images/video, thermal log, listener test, camera/mic raw test data retained only under explicit diagnostic consent.

### Gate 3 — compute benchmark and silicon selection

Build the same representative pipeline on ESP32-S3 and STM32N657 development kits. Measure accuracy parity, frame rate, end-to-end latency, internal/external memory peaks, audio underruns, radio coexistence, boot milestones, thermal behaviour and power.

Select:

- **ESP32-S3** if it passes with margin and integrated BLE meaningfully lowers product complexity;
- **STM32N657 plus certified radio module** if the proven model needs its NPU/camera pipeline;
- **RA8P1 evaluation** only if STM32N6 fails a named toolchain, package, security, performance or sourcing requirement.

**Exit evidence:** reproducible benchmark firmware, logs and decision record with margins, not peak marketing numbers.

### Gate 4 — integration and privacy proof

Prototype device BLE -> phone/gateway -> report flow. Prove HealthKit locally on iOS and apply for Garmin access before depending on it. Keep Slack limited to development coordination or deliberately minimised notifications.

**Exit evidence:** authenticated GATT schema; companion-app spike; consent and deletion flow; threat model; Garmin access result; Slack data classification.

### Gate 5 — custom electronics

Only now lock the processor, camera, mic, amplifier, speaker, power tree and radio module. Draw schematic/layout with measurement points and option footprints. Build separate functional blocks or a modular carrier first if the acoustic/optical mechanics are still changing.

**Exit evidence:** reviewed schematic, stack-up/floorplan, power and thermal budget, BOM lifecycle check, DFM/DFT review, real prototype quotes.

### Gate 6 — product validation

Validate overnight reliability, updates/rollback, watchdog/fault darkness, audio acceptance, RF/EMC, IR eye safety, privacy controls and algorithm performance across people/rooms before any claim or volume estimate is frozen.

## 7. Decisions safe to make now

- Normal sleep mode is fully dark; red is setup-only. Radar is the first camera-free sensing candidate, and 940 nm is the fallback illumination default only if vision proves necessary.
- Raw camera/audio is not intentionally stored or transmitted by production firmware.
- K210 is out.
- Silicon, camera sensor and production amplifier remain open pending measured gates.
- MAX98357A is allowed for prototype A/B testing, not declared hiss-free.
- T5848 I2S and IM72D128V PDM are the starting microphone candidates.
- Strict “no RTOS” and `<50 ms boot` are removed as architecture axioms.
- BLE reaches Slack only through a phone/gateway and an internet service.
- Apple Health requires a companion Apple-platform app; Garmin is conditional on program approval/licensing.
- Slack is the planner/notification interface, not the authoritative health-data store.

These choices preserve momentum without forcing the expensive decisions before the evidence exists.

## 8. Owner constraints recorded after the review

The owner confirmed a wellness-first product that should identify concerning
breathing interruptions without claiming a medical diagnosis, permits local-only
camera processing, requires two external passive bookshelf speakers, excludes
mains voltage from the device, and wants production electronics integrated onto a
custom PCB rather than a Raspberry Pi-class computer.

The owner subsequently selected a morning report with no real-time respiratory
alarm, identified the speakers as the Monitor Audio Silver 1 (2014 generation),
and accepted a 24 V external DC brick. The supplied speaker specification lists a
nominal 8-ohm impedance, 87 dB sensitivity, 45 Hz to 35 kHz response, and a 40 to
100 W recommended amplifier range. The rear label and measured DC resistance
should still confirm the physical pair before protection limits are fixed.
([speaker specification](https://www.hifispecs.com/monitor-audio-silver-1/))

### Consequences

- The desired respiratory feature remains a regulatory boundary, not something a
  disclaimer resolves. MHRA states that a manufacturer's “not a medical device”
  disclaimer does not automatically determine classification, and products that
  identify or monitor apnoea can meet the medical-device definition. ([MHRA patient
  guidance](https://www.gov.uk/guidance/medical-devices-information-for-users-and-patients),
  [MHRA intended-use guidance](https://www.gov.uk/government/publications/medical-devices-that-need-a-clinical-investigation/determining-if-a-clinical-investigations-is-required))
- Respiratory effort and airflow are different. AASM definitions describe
  obstructive apnoea as absent airflow with continuing effort, and central apnoea
  as absent airflow without effort. A camera/radar movement channel therefore
  cannot, by itself, establish all event types. ([AASM definitions](https://aasm.org/wp-content/uploads/2017/07/PP_Polysomnography.pdf))
- A cleared home-study example records nasal airflow, respiratory effort, pulse,
  oxygen saturation, snoring, and body position. This is a useful future validation
  reference, not a requirement to copy its contact sensors into the first product.
  ([FDA ApneaLink Air summary](https://www.accessdata.fda.gov/cdrh_docs/pdf14/K143272.pdf))
- MAX98357A no longer fits the output-power requirement. TI positions TAS5805M for
  bookshelf stereo and specifies 2 x 23 W into 8 ohms at 21 V with 1% THD+N,
  107 dB A-weighted SNR, and under 40 uV RMS noise. ([TAS5805M
  datasheet](https://www.ti.com/lit/ds/symlink/tas5805m.pdf)) TAS5825M is the
  higher-performance comparison: active, 2 x 30 W into 8 ohms at 24 V and 1%
  THD+N, at least 110 dB A-weighted SNR, no more than 35 uV RMS integrated noise,
  output monitoring useful for echo cancellation, and integrated EQ, limiting, and
  speaker protection. ([TAS5825M product page](https://www.ti.com/product/TAS5825M))
- The Silver 1's 40 to 100 W amplifier recommendation is compatibility guidance,
  not a 40 W continuous-power requirement. A clean 30 W/channel corresponds to a
  theoretical single-speaker level of roughly 102 dB SPL at 1 m from the published
  87 dB sensitivity, before room and distance effects. That is ample headroom for
  sleep playback. Keep the TAS5825M/24 V path as the quality baseline, use a
  conservative limiter, and revisit power only if room-filling music becomes a
  product requirement.
- Both amplifiers are bridge-tied stereo outputs. Four binding posts are required
  and the two black speaker terminals must not be connected together.
- A certified external 24 V DC supply provides the best initial bookshelf-speaker
  headroom while keeping mains outside the enclosure. USB-C PD can supply up to
  100 W and has firmware-free sink-controller options, but adds negotiation, cable,
  connector, and power-path complexity. ([TI USB-C PD controller overview](https://www.ti.com/product-category/interface/usb-ics/type-c-pd-controllers/overview.html))

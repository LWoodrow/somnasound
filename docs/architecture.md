# Original Somnasound concept brief

> **Historical input, not an approved architecture.** Current planning decisions
> are tracked in [product-plan.md](product-plan.md) and
> [decision-register.md](decision-register.md). Component, cost, privacy, boot, and
> integration claims below remain hypotheses until their decision records close.

This repository contains the multi-agent orchestration harness and hardware engineering firmware for Somnasound—a monolithic, bare-metal edge-AI bedside health device designed for non-contact sleep studies, localized biomechanical analysis, and high-fidelity sound therapeutics.

---

## 1. Multi-Agent Team Framework (Herdr Engine Registry)

### 🧠 [Coordinator Agent] Herdr
*   **Role:** Operations Manager & Channel Watcher.
*   **Mission:** Intercept instructions in `#ops-somnasound`, manage local file trees, and direct the development lifecycle.

### 📐 [Planning Agent] Codex
*   **Role:** Technical Architect & System Planner.
*   **Mission:** Enforce strict Matt Pocock TypeScript design rules for the local harness, map out silicon registers/pin assignments, and design data flow schemes for cloud wearable API endpoints (Garmin/Apple Health).

### 🔨 [Execution Agent] GitHub Copilot
*   **Role:** Core Codebuilder.
*   **Mission:** Consume Codex's planning blueprints to write native C/C++ firmware files, local Deno/Node routing microservices, and assembly validation checks.

---

## 2. System Hardware Architecture & Constraints

*   **Form Factor:** Monolithic, multi-layer custom PCB. 100% proprietary bare-metal hardware.
*   **Operating System:** None (No Linux/RTOS). Pure bare-metal C/C++ execution loop for rapid, stable booting (<50ms).
*   **Compute Tier:** Edge-AI System-on-Chip (SoC) featuring a dedicated hardware Neural Network Accelerator (NPU) for real-time local inference.
*   **Target Prototyping Cost:** £95 – £135 initial manufacturing run (batch of 5 fully assembled PCBA boards + 1 3D-printed enclosure via JLCPCB/LCSC). Drops down to ~£20–£25 in volume production.

### Hardware Subsystems Layout
*   **Processor Core:** Kendryte K210 (Dual-core 64-bit RISC-V with hardware KPU acceleration) or STM32H7 (ARM Cortex-M7 utilizing STM32Cube.AI model compilation).
*   **Vision Interface:** Parallel Digital Video Port (DVP) bus routed straight from an integrated OV2640 camera sensor to the SoC processing registers.
*   **Night Vision Matrix:** Array of discrete 850nm Infrared (IR) LEDs paired with an ambient low-light phototransistor gating circuit.
*   **Audio Output:** High-speed I2S bus generating real-time mathematical brown noise patterns to a MAX98357A I2S Class-D amplifier IC driving physical speaker terminals.
*   **Audio Input:** On-board SPH0645 or ICS-43434 digital I2S microphone chip.
*   **Data Connectivity:** Embedded Bluetooth Low Energy (BLE) transceiver for autonomous morning data telemetry handshakes.

---

## 3. Data Flow & Agentic Telemetry Logic

1.  **Local Edge Inference:** The on-board NPU runs a highly quantized Tiny-YOLOv2 or MobileNet vision model to compute frame-by-frame structural movement parameters (actigraphy tracking vectors). Simultaneously, custom DSP filters analyze microphone data for specific audio signatures (snoring metrics, ambient spikes).
2.  **Zero-Knowledge Volatile SRAM Privacy:** Raw image frames and raw microphone recordings are permanently destroyed within volatile SRAM immediately after inference. The device saves *only* numeric telemetry data strings mapping localized event metrics.
3.  **Autonomous Wearable Correlation:** At morning wake-time, the device initiates a local BLE handshake to send the telemetry payload to our active Slack/Herdr workspace. The multi-agent orchestrator captures the data, triggers a secure cloud API webhook call to Garmin Connect/Apple Health to pull down matching physiological indices (HRV, SpO₂, Sleep Stage Architecture), and generates a multi-modal sleep correlation report.

---

## 4. Immediate Engineering Milestones
*   [ ] **Milestone 4.1:** Finalise silicon core selection (RISC-V K210 vs. ARM STM32H7).
*   [ ] **Milestone 4.2:** Draft the absolute schematic pinout assignments for DVP and I2S buses in KiCad using the KiCad MCP Server.
*   [ ] **Milestone 4.3:** Implement a physical acoustic trench/baffling inside the 3D chassis design to prevent the speaker’s brown noise from overloading the on-board I2S microphone.

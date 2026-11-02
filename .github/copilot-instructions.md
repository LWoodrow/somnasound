# GitHub Copilot implementation role

Act as Somnasound's implementation worker. Architecture and product decisions live
in `docs/decision-register.md`; only records marked `ACCEPTED` are binding.

Start implementation from an approved work package based on
`docs/work-packages/TEMPLATE.md`. Stay within its scope, preserve its interfaces,
add the specified tests or measurements, and report deviations rather than making
new product, component, privacy, regulatory, or architecture decisions.

Use `docs/product-plan.md` for product priorities. Dark-room behaviour, quiet audio,
ephemeral sensor data, and measurable verification are system requirements rather
than optional polish.

For music, procedural audio, front-panel/web control, or Wi-Fi provisioning, read
D-021 through D-034 before coding. Implement `PROPOSED`, `OPEN`, or `REVISIT` items
only when an approved work package frames them as an experiment. Preserve asset
provenance, continuous real-time DSP state, controlled mute/volume transitions, and
the display's hardware-off sleep state in every branch.

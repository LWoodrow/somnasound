# Somnasound working agreement

Read `docs/product-plan.md` and `docs/decision-register.md` before changing product
behaviour, firmware, electronics, sensing, audio, connectivity, or product claims.

Only `ACCEPTED` decision records are architectural constraints. Treat `PROPOSED`,
`OPEN`, and `REVISIT` records as questions; surface the trade-off instead of
embedding one option in code or hardware.

Planning work produces a bounded work package from
`docs/work-packages/TEMPLATE.md`. Implementation work follows that package,
verifies every acceptance criterion, and reports evidence and remaining risks.

Keep raw sensor data ephemeral by default, preserve dark-room operation, and make
audio-quality changes measurable. Product or medical claims require an accepted
intended-use decision and supporting validation evidence.

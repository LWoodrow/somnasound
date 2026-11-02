# Work package: contract-manufacturing handoff

Status: `DRAFT`

## Decision context

- Accepted decision records: D-003 audio quality, D-016 product construction,
  D-031 red display hardware, D-032 automatic blackout, and D-033 finished-device
  delivery. Revisited decision: D-034 contract manufacture.
- Question this work answers: which supplier can deliver the production-intent
  electronics with the owner supplying only the specialist red OLED and external
  power brick at the best total landed, accepted cost?
- Evidence that will change the decision: matched supplier DFM/DFT reviews, quotes,
  assembly constraints, first-article test records, and final acceptance results.

## Objective

Produce a complete, reproducible manufacturing package for one finished Somnasound
device and select a supplier from matched partial-turnkey quotes with no unapproved
component substitutions.

## Inputs and interfaces

- Production-intent KiCad fabrication files, stack-up, impedance notes, panelisation
  preference, BOM with manufacturer part numbers, AVL, pick-and-place data, assembly
  drawings, polarity/orientation notes, and test points.
- Firmware release image, programming method, serial-number convention, and functional
  test procedure/fixture specification.
- Red OLED exact manufacturer order code, datasheet, original packaging, placement/
  handling instructions, and agreed overage quantity.
- External certified 24 V UK power brick specification, connector, polarity, current
  rating, cable length, and incoming-inspection criteria.
- Stable interfaces: red-OLED connector/pinout, 24 V DC input, speaker binding-post
  wiring, programming/debug access, and functional-test pads.

## In scope

- Matched partial-turnkey quotes from PCBWay, Newbury Electronics, Axiom, Jaltek, and
  Eurocircuits for 1, 3, and 10 units, with PCBWay treated as overseas and Newbury as
  the first UK route.
- Fabrication, approved standard-part sourcing, SMT/THT assembly, firmware
  programming, AOI/electrical inspection, and agreed functional test by the selected
  supplier.
- Partial-turnkey build with the owner consigning the specialist red OLED if the
  selected supplier cannot source the exact approved red variant.
- Quote factory installation of the consigned display as part of box build; preserve a
  keyed connector and documented local-install path if that operation is declined.
- A locked BOM/AVL and a written “no substitutions without owner approval” rule.
- Factory functional tests for rail currents, boot, firmware identity, controls,
  display red/blackout behaviour, audio output into safe dummy loads, and basic Wi-Fi
  provisioning health.
- Final owner acceptance for audible hiss/interference, overnight reliability,
  dark-room blackout, enclosure fit, and safe operation with the external brick.

## Out of scope

- Mains circuitry inside the product, uncertified power supplies, unapproved display
  colours, automated substitution of parts, and production release before the exact
  red display order code is confirmed.

## Acceptance criteria

- [ ] Each candidate quote separates PCB, parts, NRE, assembly, programming, fixture,
      test, freight, VAT/import/brokerage assumptions, box build, and rework path.
- [ ] The chosen supplier confirms partial-turnkey assembly and identifies every
      supplied versus consigned part before order placement.
- [ ] The manufacturing package passes the chosen supplier's DFM/DFT review with all
      test points, panel/assembly constraints, programming, and display installation
      resolved.
- [ ] Every line in the BOM has manufacturer part number, approved source, lifecycle
      status, and an explicit approval rule for any substitute.
- [ ] Consigned OLEDs are shipped in original ESD-safe packaging with a packing list,
      BOM line number, manufacturer part number, quantity, and agreed spare quantity.
- [ ] The factory functional-test record accompanies the assembled board.
- [ ] Final owner acceptance confirms clean audio at the bed, no unwanted visible
      light after the 30-second timeout, correct red display output, and safe 24 V
      external-brick operation.

## Verification commands or procedure

```text
1. Send one revision-controlled package to PCBWay, Newbury, Axiom, Jaltek, and
   Eurocircuits for 1/3/10-unit DFM/DFT and partial-turnkey quotations.
2. Score total landed accepted cost, no-substitution control, OLED handling, test
   ownership, lead time, UK/EU/overseas logistics, and rework path before selection.
3. Reconcile every selected-supplier-sourced or proposed-substitute component against
   the locked BOM before approving purchase.
4. Send consigned display units with the packing list and agreed overage.
5. Review assembly and functional-test records for the first article.
6. Run the owner final-acceptance checklist in the intended bedroom and daytime setup.
```

## Deliverables

- `hardware/kicad/` fabrication, assembly, and test files.
- `hardware/bom/` locked BOM, AVL, and approved-substitute record.
- `firmware/` release image and programming/test procedure.
- `docs/manufacturing/` PCBWay quote, DFM/DFT findings, consignment list, first-article
  inspection, and final-acceptance record.

## Handoff

- Results:
- Deviations:
- Remaining risks:
- Recommended decision update:

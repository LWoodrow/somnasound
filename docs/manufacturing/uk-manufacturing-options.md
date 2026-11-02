# UK-oriented manufacturing options

Status: `RESEARCH — quote before selection`  
Date: 2026-11-01

This note compares realistic contract-manufacturing routes for the one finished
Somnasound device: a 4–6-layer mixed SMT/THT PCBA, customer-supplied specialist
red OLED if necessary, external certified UK 24 V supply, controlled BOM, firmware
programming, functional test, and optional enclosure assembly. It does **not** make a
price claim. At this quantity, price, lead time, test ownership, and rework exposure
are quote-specific.

## Correction: PCBWay is not a US manufacturer

PCBWay describes production bases in Shenzhen, Guangdong, Xinfeng and Shangrao,
China, and identifies Hangzhou as its head-office location. Its public contact
details use a Chinese telephone number and GMT+8 service hours. It has a French
company/service presence, but the published information does not establish UK PCBA
production. Treat it as an overseas/China manufacturing route for freight, import,
communications, and returns planning—not as a US or UK factory.

Sources: [PCBWay OEM locations](https://www.pcbway.com/oem/about-oem/),
[PCBWay contact details](https://www.pcbway.com/contact), and
[PCBWay shipping FAQ](https://www.pcbway.com/rapid-prototyping/cnc-faq.html).

## Capability comparison

| Route | What its official material substantiates | Fit for Somnasound | Questions that remain before selection |
|---|---|---|---|
| **PCBWay — China/overseas** | Partial-turnkey, customer-supplied parts, SMT/THT hybrid assembly, low minimum quantity, and functional testing following the customer's procedure. PCBWay also advertises programming/software services and box/product assembly. | A credible cost/turnaround benchmark, especially if the OLED is consigned. | Exact China-to-UK landed cost, VAT/import handling, handling of the delicate OLED/FPC, written no-substitution workflow, fixture ownership, programming method, test execution/report, and overseas rework turnaround. |
| **Newbury Electronics / PCB Train — Berkshire, UK** | UK fabrication and assembly; no batch too small; SMT/THT, 1–12 layer board capability, customer-supplied/free-issue kits, test to customer procedures, and box build. Its assembly process describes first-off checking, AOI/X-ray, traceability, and electrical testing when required. | **Best first UK quote.** The strongest documented direct match for low-volume board build, owner-supplied OLED, through-hole binding posts, and a practical first article. | Confirm firmware flashing, test-fixture support, complete enclosure build, exact test-report deliverables, customer approval of all alternates, and whether the final screen is installed only after a defined inspection step. |
| **Axiom Manufacturing Services — Newport, UK** | UK low-to-medium-volume bespoke PCBA manufacture, test development, supply chain, and box build. Its test offering includes in-circuit, flying-probe and functional testing. | Strong candidate when test engineering, traceability, and eventual finished-product build matter more than the lowest one-off quote. | Confirm it will take a very low-volume personal-device NPI; consigned/display installation policy; minimum/NRE; firmware programming; BOM change-control; enclosure scope; and timing. |
| **Jaltek — Luton, UK** | UK manufacturer focused on low-to-medium-volume/high-mix work; official material describes SMT/THT assembly, DFM/DFT, functional/environmental testing, and full electrical box build. | Strong second UK CEM quote, particularly if we want an enclosure assembly path and production test support. | Confirm willingness to handle the small first run, free-issued red OLED and binding posts, programming/calibration, written substitute control, and first-article/audio test support. |
| **Eurocircuits — European facilities** | Prototype/small-series PCBA from 1–50 pieces, mixed SMT/THT, 3/5/7/10-day assembly options, customer parts when it cannot source them, and inspection. It only assembles boards that it fabricates. | Good European fast-turn/buildability comparison for board assembly, particularly during the final DFM iteration. | Treat programming, detailed functional testing, no-substitution policy, specialised screen installation, and enclosure build as explicit quote questions—not established by the published assembly capability. |

Capability sources: [PCBWay assembly capabilities](https://www.pcbway.com/assembly-capabilities.html),
[PCBWay test/programming](https://www.pcbway.com/pcb-assembly/pcb-assembly-testing.html),
[Newbury CEM capability](https://www.newburyelectronics.co.uk/the-complete-cem/),
[Newbury supplied kits and testing](https://www.newburyelectronics.co.uk/supportive-services/about-component-kits-and-data/),
[Newbury assembly process](https://www.newburyelectronics.co.uk/printed-circuit-board-assembly/our-pcb-assembly-process/),
[Axiom manufacture/test](https://www.axiom-ms.com/),
[Axiom test service](https://www.axiom-ms.com/solutions/test/),
[Jaltek manufacturing scope](https://www.jaltek.com/manufacturing/sectors/defence),
[Jaltek box build](https://www.jaltek.com/manufacturing/solutions/box-build),
[Eurocircuits assembly capability](https://www.eurocircuits.com/services/pcb-assembly-capabilities/),
and [Eurocircuits component sourcing](https://www.eurocircuits.com/technical-guidelines/assembly-manufacturing-technology/component-sourcing/).

## Recommendation

Do not replace PCBWay with a UK house on assumption alone. Obtain matched quotes in
parallel from **Newbury, Axiom, Jaltek, Eurocircuits, and PCBWay**, using the same
revision-controlled package and three quantities: **1 first article, 3 verification
units, and 10 finished units**. Newbury is the first UK route to investigate; Axiom
and Jaltek are higher-touch UK CEM checks; Eurocircuits is the European small-series
benchmark; PCBWay remains the overseas cost/turnaround comparator.

Select the supplier only after a scored manufacturing review. The decisive total is
the landed, accepted unit cost—not the bare-PCB price. Include PCB fabrication,
components, assembly set-up/NRE, test-fixture/NRE, programming, inspection, shipped
consigned OLEDs, freight, VAT/duty/brokerage, yield allowance, rework/return cost,
and the cost of any onsite/remote first-article support. Component availability and
life-cycle also matter: a cheap assembly quote is not useful if a critical part is
unobtainable or a supplier silently changes it.

## Quote package to give every supplier

- Gerbers/ODB++ or native KiCad release, drill files, stack-up/controlled-impedance
  requirements, board outline, panel preference, and assembly drawings.
- Locked BOM and AVL: manufacturer part number, approved distributor(s), lifecycle
  status, package, do-not-substitute flag, and explicit spare/attrition quantity.
- Pick-and-place/centroid file, reference-designator drawings, polarity/orientation
  information, and a through-hole build drawing for binding posts, buttons, encoder,
  display connector, and other mechanical parts.
- Red OLED data sheet, exact colour/order suffix, FPC/pin-one drawing, ESD/handling
  rules, mating/retention instruction, shipping/consignment packing list, and spares.
- Firmware image, programming interface/pinout, cryptographic signing/key handling
  plan, version label, and recovery method. Never send production private keys unless
  the agreed process and supplier controls justify it.
- Factory test specification: safe 24 V input source, initial power-up current limit,
  display/red-only/blackout test, buttons/encoder, Wi-Fi setup, SD/network media,
  audio output/absence of audible faults, binding-post polarity, thermal soak, and
  pass/fail serial-number record.
- Inspection expectations: first article, AOI/X-ray where relevant, visual standard,
  FCT record, non-conformance photos, and explicit acceptance before the balance is
  built.

## RFI / quote questions

1. Will you quote 1, 3, and 10 identical boards, separating PCB, parts, assembly,
   NRE, programming, fixture, test, shipping, taxes/import, and any box-build line?
2. Can you build this mixed SMT/THT 4–6-layer board, including high-current audio
   terminals and a fragile consigned OLED/FPC? State your exact installation and
   rework procedure.
3. Can the owner consign the red OLED and any other scarce part? State ESD, incoming
   inspection, storage, attrition/overage, liability, return-of-surplus, and packing
   requirements.
4. Will you accept a locked AVL and **make no component, manufacturer, package,
   firmware, process, or test substitution without written owner approval**? Describe
   the deviation/NCR workflow and how it is recorded against the serial number.
5. Which parts will you source, from which authorised channels, and how will you
   report lifecycle risk, date/lot traceability, counterfeit controls, and shortages?
6. Can you flash the supplied signed image, preserve the device identity/serial
   number, and provide a programming record? Who owns the fixture and source files?
7. Can you execute the supplied functional test and deliver a pass/fail record per
   serial number? What fixture/test-development NRE and engineering support are
   required? What can you measure for audio noise, RF, display blackout and thermal
   soak, and what must remain an owner acceptance test?
8. Can you support a first-article review before the rest of the batch, and can the
   build be paused pending written approval?
9. Can you perform enclosure/display/control fit, final assembly, labelling and
   packing later? If not, what interfaces/fixtures should the PCB design provide now?
10. For the UK quote: state VAT treatment, domestic freight, and rework lead time.
    For the overseas quote: state Incoterm, exporter/importer of record, duty/VAT and
    brokerage assumptions, shipping insurance, and return/rework process.

## Decision gate

`D-034` currently accepts PCBWay as the primary route. This research does not change
that accepted decision. Re-open it only after matched written quotes, a supplier DFM
review, and a documented comparison of total landed cost, no-substitution control,
test ownership, OLED handling, lead time, and rework path. A UK route may be worth a
premium for easier first-article collaboration and returns; it is not automatically
cheaper, and PCBWay is not automatically cheaper either.

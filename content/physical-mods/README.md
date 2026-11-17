# Physical mods and upgrades

Printed parts, bought parts, and chamber work - the hardware side. Community
research, October-November 2026; links go to the models. One framing note
first: the Plus 5 already fixed the things that made the Plus 4 a mod platform
(linear rail on X, load-cell nozzle probe, 9 mm belts, padded walls, camera
moved off the printhead park, better door). The list of *necessary* mods is
short; most of this page is quality-of-life.

## Before the first multicolour job: a purge chute or bin

The Box purges inside the chamber and it piles up as spiral cones next to the
plate ([why](../box-reliability/README.md)). Options made for the Plus 5:

- [QIDI Plus 5 Poop Chute (Cults3D)](https://cults3d.com/en/3d-model/tool/qidi-plus-5-poop-chute)
- [Plus5 waste/purge/poop bin - two designs (Creality Cloud, free)](https://www.crealitycloud.com/model-detail/qidi-plus5-waste-purge-bin-designs)
- The [Cults3D "qidi" tag](https://cults3d.com/en/tags/qidi) also carries a
  free snap-in purge bin and new designs appear weekly - check it before
  printing anything from another printer's page (Plus 4 chutes mount
  differently).

## Filament path

- **PTFE guide clip** - the tube from the Box scrapes the top glass on stock
  routing; it's a wear item. [Q2/Plus 4 clip on
  Printables](https://www.printables.com/model/1462946-qidi-q2qidi-plus-4-ptfe-guide-clip)
  (may fit; [Q2 remix for newer printheads](https://cults3d.com/en/3d-model/tool/qidi-q2-ptfe-guide-clip-remixed-from-little-apollo)
  exists). Zero-cost version: a spare clip in the cable chain holding the
  tube lower.
- **Box jam-resistant filament guide** - feeds, not the head:
  [Printables 1386069](https://www.printables.com/model/1386069-qidi-box-jam-resistant-filament-guide/comments)
  (context on [the reliability page](../box-reliability/README.md)). The hub
  wants 50 mm of straight tube before entry - this fixes the commonest feed
  failure.
- **Capricorn-style tubing** for the Box runs - same story, less friction.

## The riser ecosystem (D3P)

If you're adding a Box, dryers or a cooler on top,
[the D3P riser for Plus 5](https://cults3d.com/en/3d-model/tool/d3p-riser-for-qidi-plus-5)
(Cults3D, paid, 3MF with print settings) is the de facto standard: a modular
20.5 cm riser with drawers, build-plate storage, LED channels, front/side
vents - and a shelf system that grows with you. Free/cheap add-ons in the
same family: Box extension shelves, single/dual dryer shelves, QIDI Cooler
base and shelves, cable management + PSU holder, Multiboard adapter,
[top-mount TPU spool holder](https://cults3d.com/en/3d-model/tool/qidi-plus-5-d3p-top-mount-tpu-spool-holder),
[side-mounted build-plate holder (8
plates)](https://cults3d.com/en/3d-model/tool/side-mount-build-plate-holder-for-qidi-plus-5-d3p-riser).
Author's material call: PETG or ASA for the riser (PLA only if it'll never
sit near a dryer or the heated chamber exhaust).

## Chamber and filtration

- **Seal the chamber** for stable high temps and fewer fumes: close the long
  strip opening in the back wall, tape the hinge side of the door. Cheap,
  reversible, and it makes ABS/ASA more consistent.
- **Bento Box activated-carbon filter**: the standard community answer for
  enclosed ABS/ASA. The [Plus 4 duct (Printables
  1214344)](https://www.printables.com/model/1214344) needs adaptation for
  the Plus 5's geometry - check makes/remixes before printing.
- **External venting**: rear-port adapters exist with a 2" NPT thread + 3"
  nipple for hose or pipe ([on the Cults3D
  tag](https://cults3d.com/en/tags/qidi)). Note the stock HEPA/carbon filter
  is restrictive; owners running external venting often remove it.
- **Chamber heater intake**: the build plate can block the intake on taller
  prints - enlarging it improves airflow and lowers housing temperature.
- The stock 3-in-1 filter (G3 + H12 HEPA + carbon) is the maintenance item;
  see [the maintenance page](../maintenance/README.md).

## Cooling: the Polar Cooler

PLA/PETG with the door closed is the one thing this printer genuinely doesn't
like ([the numbers](../print-quality-tuning/README.md)). QIDI's official
answer is the **Polar Cooler** add-on - a powered aux cooler for printing PLA
with the chamber sealed. Buy it; don't hack a fan into the chamber unless you
enjoy re-tuning every temperature sensor relationship you have.

## Build plates (320 x 320 - non-standard)

- Stock: [QIDI dual-sided textured PEI](https://qidi3d.com/products/plus5-dual-sided-pei-plate),
  [Smooth PEI Plate Pro](https://qidi3d.com/products/plus5-dual-sided-smooth-plate-pro)
- [R3men real carbon-fiber plate](https://r3men.com/products/real-carbon-fiber-build-plate-for-qidi-plus-5) -
  CF laminate on 1 mm steel, community-tested from PLA through PPS-CF; good
  adhesion, clean release, no glue
- Custom-cut textured/smooth PEI from Juupine / ENERGETIC on AliExpress
- **Don't fit**: Plus 4 plates (305 x 305), BIQU CryoGrip Pro (300 x 300
  max), and the generic "QIDI" 280/300 plates that are really for the older
  X-series

## Box internals

- **Desiccant capacity**: stock trays are small - there's a cottage industry
  of printed large-capacity desiccant modules ([the drying
  page](../qidi-box-drying/README.md) has the numbers). Print them in ABS or
  anything that survives 65 C, because that's what drying cycles run at.
- **The Box clicks** on every load - community grease mods exist for the
  feeders. Cosmetic, not functional.

## Official and QIDI-published

- **Height-increasing frame** - QIDI's own extender,
  [model files on Google Drive](https://drive.google.com/drive/folders/1FleBuFFs7bZrR7mrICKuHLSsbolAhDHi)
  (from the official wiki).
- [Box + spool holder on QIDI Maker](https://www.qidimaker.com/en/models/detail/2095854431347748865),
  also on Printables.
- **Purge/waste**: see the top of this page.
- Box and spool holder also exists as an ASA-CF profile on Maker.

## What you probably *don't* need

Fixed from the Plus 4: X linear rail, load-cell probe (no cartographer/Beacon
needed for 99% of uses), belt upgrades, camera reposition, door handle. If
you find yourself modding those, something else is wrong - start with
[the bed page](../bed-mesh-vs-printable-area/README.md) and
[the print-quality page](../print-quality-tuning/README.md) instead.

---

*Everything here is community-published with links to the source models;
availability moves, the Cults3D tag and r/QidiTech3D are where new parts
surface first. Print chamber-adjacent parts in PETG minimum, ASA if they live
near the exhaust or a dryer. Corrections and your own makes welcome.*

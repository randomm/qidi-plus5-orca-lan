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
- [Qidi Plus 5 Poop Chute/Poop Bin/Bucket (Technix AM, on QIDI
  Maker)](https://www.qidimaker.com/en/home) - same designer as the free riser
  below
- [Qidi Plus 5 Waste Bin (Kramer, Printables)](https://www.printables.com/model/1811886) -
  magnetically attached purge catcher on the *rear* waste chute (8x 20x10x5
  neodymium magnets, epoxy, print in ASA; bracket reuses the chute's three
  existing screws)
- The [Cults3D "qidi" tag](https://cults3d.com/en/tags/qidi) also carries a
  free snap-in purge bin and new designs appear weekly - check it before
  printing anything from another printer's page (Plus 4 chutes mount
  differently).

## Filament path

- **PTFE guide clip** - the tube from the Box scrapes the top glass on stock
  routing; it's a wear item. [Q2/Plus 4 clip on
  Printables](https://www.printables.com/model/1462946-qidi-q2qidi-plus-4-ptfe-guide-clip)
  (may fit; [Q2 remix for newer printheads](https://cults3d.com/en/3d-model/tool/qidi-q2-ptfe-guide-clip-remixed-from-little-apollo)
  exists, and Kapral001's Q2 tube guide is on [QIDI
  Maker](https://www.qidimaker.com/en/home)). Zero-cost version: a spare clip
  in the cable chain holding the tube lower.
- **Box jam-resistant filament guide** - feeds, not the head:
  [Printables 1386069](https://www.printables.com/model/1386069-qidi-box-jam-resistant-filament-guide/comments)
  (context on [the reliability page](../box-reliability/README.md)). The hub
  wants 50 mm of straight tube before entry - this fixes the commonest feed
  failure.
- **PTFE/cable management clip set** - bundles the Box tubes with a gradual
  sweep into the hub instead of tight bends (25 mm clips closest to the hub,
  separators for multi-box runs):
  [Qidi Box clip set (Printables 1526810)](https://www.printables.com/model/1526810).
  Same disease as the jam guide, prevention side.
- **Capricorn-style tubing** for the Box runs - same story, less friction.

## Risers: paid standard, free alternative

If you're adding a Box, dryers or a cooler on top, there are two mature
options:

**[D3P riser for Plus 5](https://cults3d.com/en/3d-model/tool/d3p-riser-for-qidi-plus-5)**
(Cults3D, paid, 3MF with print settings) - the de facto standard: a modular
20.5 cm riser with drawers, build-plate storage, LED channels, front/side
vents - and a shelf system that grows with you. Free/cheap add-ons in the
same family: Box extension shelves, single/dual dryer shelves, QIDI Cooler
base and shelves, cable management + PSU holder, Multiboard adapter,
[top-mount TPU spool holder](https://cults3d.com/en/3d-model/tool/qidi-plus-5-d3p-top-mount-tpu-spool-holder),
[side-mounted build-plate holder (8
plates)](https://cults3d.com/en/3d-model/tool/side-mount-build-plate-holder-for-qidi-plus-5-d3p-riser).

**[Technix AM's Plus 5 riser](https://makerworld.com/en/models/3259910-qidi-plus-5-riser-by-technix-am)**
(MakerWorld, **free** - boost the author if it serves you well) - screw-free
assembly (only the front roller frame needs 4x M3x16), an integrated LED
strip that keeps the top glass sliding, two storage drawers, full access to
the original USB port, and detachable rollers for the TPU spool mount (688
bearings). **STEP/CAD files included** for remixing, plus a QIDI Studio slice
file. ~3.1 kg of filament and 80+ print hours - the author says print the
test block first and check contour compensation; ABS/ASA or PETG/PETG-CF
recommended.

Material call either way: PETG or ASA for anything living near a dryer or the
chamber exhaust (PLA only if it never will).

Going **under** instead of up: [TPU riser feet
(XRasher)](https://www.printables.com/model/1884566) press onto the stock
feet, damp vibration, and lift the printer ~22 mm - exactly enough for the
matching [under-printer organizer](https://www.printables.com/model/1884581)
to slide underneath. Prints in TPU, two walls, 10% infill.

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
- **Aftermarket 320 x 320 is a rare size.** The old Energetic 320x320
  listings (Tevo Nereus era) are gone; current AliExpress stock runs
  320x310 or 350x320. Live routes:
  [AliExpress search for 320x320 PEI](https://www.aliexpress.com/w/wholesale-energetic-pei-magnetic-sheet-320x-320.html),
  the [Energetic3D storefront](https://www.aliexpress.com/store/1101427698)
  (their older listings advertised customized sizes - worth a store message),
  or [Aurarum's double-sided 320x320 with magnetic
  base](https://aurarum.com.au/shop/double-sided-pei-flexible-bed-with-magnetic-base-320x320)
  (Australian store). Energetic 330x330 sheets are live but overhang the
  stock platform by 5 mm a side - unverified fit.
- **Don't fit**: Plus 4 plates (305 x 305), BIQU CryoGrip Pro (300 x 300
  max), and the generic "QIDI" 280/300 plates that are really for the older
  X-series

## Box internals

- **Desiccant capacity**: stock trays are small. The standard upgrade is
  [R985's high-capacity desiccant bin](https://www.printables.com/model/1386559)
  (original hardware, no modification, narrower slots in the updated
  revision) with [GoodHope's top cap](https://www.printables.com/model/1430915)
  - print in ABS; [the drying page](../qidi-box-drying/README.md) has the
  numbers on why capacity matters.
- **The Box clicks** on every load, and the fix is mechanical:
  [weav's spool driven gear with an HF0306 one-way
  bearing](https://www.printables.com/model/1571032) replaces the
  pen-spring stock gear - reliable spool rewind, no more click-click (4x
  HF0306 bearings + M3 washers; six months in and out of beta by July 2026).
  Fully reversible.
- **Spare cutter arm**: [Filament Cutter Arm QIDI Plus 5
  (AP)](https://www.printables.com/model/1824360) - a printable replacement
  for the Box's cutter arm, trivially easy print.
- **Automated filament cutting in the Box**: [RVfan's AMS 2 Pro Saver / Snag
  Cutter base plate](https://www.printables.com/model/1483937) adapts
  Hexavalent's Bambu-AMS cutter system into the QIDI Box. Needs 4 Bambu
  replacement filament cutters plus PTFE offcuts from the Box install kit;
  PETG/ASA, Arachne walls, supports required.

## Q2 compatibility: what carries over

The Plus 5 and Q2 are the same generation - same Box hardware lineage, same
SSH setup, same QIDILink tunnel, same firmware family - so when a Plus
5-specific part doesn't exist, the Q2 shelf is the first place to look (and
Q2 owners should be raiding this page right back). Rough guide:

- **Usually transferable**: chamber-internal small parts (PTFE guides, exhaust
  ducts, filter holders), Box accessories (spool drive upgrades, clip sets,
  desiccant bins - the Box is shared across the generation), camera and
  light mounts, hand tools. Check screw positions before committing filament.
- **Confirmed shared, no checking needed**: QIDI sells the bimetal nozzles,
  tungsten-carbide nozzles, hotend and model cooling fans, hotend silicone
  socks, cutter blades, the 3-in-1 air filter and the camera as single
  "PLUS5/Q2/Q2C" SKUs in the official
  [accessories store](https://qidi3d.com/collections/plus5-accessories) -
  Q2 spares are literally Plus 5 spares. That settles the nozzle-storage
  question above: trays sized for Q2 nozzles fit Plus 5 nozzles, because
  they are the same nozzle.
- **Maybe, with checking**: other toolhead parts - close family, not
  identical twins. The hotend *assembly* is a Plus5-only part in the store
  (so Q2 hotend-sized storage is still measure-first), and the Q2 PTFE clip
  needed a remix for a newer printhead, which tells you the geometry moved
  between revisions.
- **No**: anything sized to the machine - build plates (the Q2 bed is
  smaller), risers and external furniture (different footprints), bed-adjacent
  parts, chute mounts.
- The Q2 even has its own D3P riser from the same author as the Plus 5 one,
  if you run both machines.

Same logic one generation back: Plus 4 and Max 4 *parts* don't carry over
(different beds and frames), but the [Max 4 community
wiki's](https://github.com/thelegendtubaguy/QidiMax4CommunityWiki) hardware
findings - bed screws, fan maps, power usage - carry over almost verbatim.

## Official and QIDI-published

- **Height-increasing frame** - QIDI's own extender,
  [model files on Google Drive](https://drive.google.com/drive/folders/1FleBuFFs7bZrR7mrICKuHLSsbolAhDHi)
  (from the official wiki).
- [Box + spool holder on QIDI Maker](https://www.qidimaker.com/en/models/detail/2095854431347748865),
  also on Printables.
- [The Plus5 accessories store](https://qidi3d.com/collections/plus5-accessories) -
  the official spares catalogue. Worth knowing: several parts are **shared
  SKUs across the generation** - nozzles (bimetal and tungsten-carbide),
  cooling fans, silicone socks, cutter blades, the 3-in-1 air filter and the
  camera are "PLUS5/Q2/Q2C" parts; wiper silicone cases, waste-bin pusher
  plates and nozzle wipers are "PLUS5/Max4"; the Polar Cooler spans all
  three. Plus5-only: hot end, extruder, build plates, screen, boards and
  cables. Practical upshot: if a part shows out of stock under its Plus5
  listing, check the same SKU under the Q2 or Max4 collection.
- **Purge/waste**: see the top of this page.

## What you probably *don't* need

Fixed from the Plus 4: X linear rail, load-cell probe (no cartographer/Beacon
needed for 99% of uses), belt upgrades, camera reposition, door handle. If
you find yourself modding those, something else is wrong - start with
[the bed page](../bed-mesh-vs-printable-area/README.md) and
[the print-quality page](../print-quality-tuning/README.md) instead.

## Curated collections

If you'd rather browse than read:

- [Qidi Plus 5 - Printables collection](https://www.printables.com/@TaiHeng_4155107/collections/3862322) -
  "made for or might work with the Qidi Plus 5":
  - Made for the Plus 5:
    - [Filament Cutter Arm (AP)](https://www.printables.com/model/1824360) -
      spare Box cutter arm (see Box internals)
    - [TPU Riser Feet (XRasher)](https://www.printables.com/model/1884566) -
      vibration damping + 22 mm lift (see Risers)
    - [Under Organizer (XRasher)](https://www.printables.com/model/1884581) -
      slides into the riser-feet gap (see Risers)
    - [Z-axis motor dust cover (Nolan Summers)](https://www.printables.com/model/1846289)
    - [Waste Bin (Kramer)](https://www.printables.com/model/1811886) -
      magnetic purge catcher on the rear chute (see purge section)
    - [D3P riser for Plus 5 (Darren3dPrint, paid)](https://cults3d.com/en/3d-model/tool/d3p-riser-for-qidi-plus-5) -
      see Risers
  - Q2 parts that may carry over (see the compatibility section):
    - [Q2 Hot Bed Nut Wrench (gasdocscott)](https://www.printables.com/model/1572093) -
      tapered remix that actually grips the bed leveling nuts - the Q2
      shares the Plus 5's bed-nut arrangement
    - [Q2 Toolhead Cover sets (ricrom)](https://www.printables.com/model/1445446) -
      magnet-mounted covers; lid wants ASA, and they predate the Polar
      Cooler (fit conflict noted by the author)
    - [Q2 Nozzle Storage Box (deusdara, MakerWorld)](https://makerworld.com/models/3431512) -
      hinged 8-slot box, two of each size, snap clips sized to the Q2
      nozzle's 4.75 mm smooth section
    - [Q2 nozzle gridfinity bin, 4 nozzles (TheSpyWhoLovedToBake)](https://www.printables.com/model/1834022)
    - [Q2 Gridfinity Hot End bin (Gu1tarzan)](https://www.printables.com/model/1736722) -
      2x2, for a spare hotend
    - [Gridfinity Q2 Nozzle Box (_Storch_, Cults3D)](https://cults3d.com/en/3d-model/tool/gridfinity-qidi-q2-nozzelbox)
    - [Toolbox for Q2 tools (Dmitry)](https://www.printables.com/model/1638608)
    - [D3P Custom Inserts for Qidi Q2 (Cults3D)](https://cults3d.com/en/3d-model/tool/d3p-custom-inserts-for-qidi-q2) -
      drawer inserts for the D3P riser: hotend, silicone sock, lubricant,
      thermal grease, fuses, wiper roller/brush, cutter, wrench, hex keys,
      screwdriver, glue stick
    - [Q2 Nozzle Inserts for D3P Riser (Moobien, Cults3D)](https://cults3d.com/en/3d-model/tool/q2-nozzle-inserts-for-d3d-riser) -
      nozzle drawer inserts for the same riser system
  - One generation back (concept transfers, inserts don't):
    - [Spare Parts/Toolbox rugged box for the Plus 4 (ECF)](https://www.printables.com/model/1229572) -
      the spare-parts + tools organization idea, Plus 4-shaped
- [Qidi box - Printables collection](https://www.printables.com/@TaiHeng_4155107/collections/3866381) -
  5 models:
  - [Qidi Box clip set - PTFE tubing and cable management (Joe the Builder)](https://www.printables.com/model/1526810) -
    bundled tubes, gradual sweep into the hub (see Filament path above)
  - [Spool driven gear, HF0306 one-way bearing (weav)](https://www.printables.com/model/1571032) -
    the click and rewind fix (see Box internals above)
  - [High-capacity desiccant bin, updated (R985)](https://www.printables.com/model/1386559) -
    the desiccant upgrade (see Box internals above)
  - [Top cap for the desiccant bin (GoodHope)](https://www.printables.com/model/1430915) -
    companion cap for the bin above
  - [AMS 2 Pro Saver / Snag Cutter base plate (RVfan)](https://www.printables.com/model/1483937) -
    automated cutting in the Box (see Box internals above)

---

*Everything here is community-published with links to the source models;
availability moves, the [Cults3D tag](https://cults3d.com/en/tags/qidi),
[QIDI Maker](https://www.qidimaker.com/en/home) and r/QidiTech3D are where new
parts surface first. Print chamber-adjacent parts in PETG minimum, ASA if they
live near the exhaust or a dryer. Corrections and your own makes welcome.*

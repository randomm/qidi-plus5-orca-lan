# Just arrived: a checklist for a new X-Plus 5

Things worth verifying on a new unit, roughly in the order you'll hit them. Every
item links the page that goes deeper. None of this is mandatory - but each one is
something that either bit someone or quietly ships in a state worth knowing
about.

## First boot

- [ ] Let the first-boot self-calibration finish (~10-15 min: motion, fans,
  heaters, input shaping). After that the bed is probed before every print -
  there is no separate bed-leveling step to do by hand.
- [ ] It weighs ~29 kg. Two people, sturdy table.
- [ ] Wash the build plate before the first print - warm water and dish soap.
  Textured PEI ships with a manufacturing film/residue that IPA alone spreads
  around more than it removes.
- [ ] Note the **firmware version** (Settings → About, or the changelog line on
  the screen). Several things on this wiki are firmware-dependent - the bed-mesh
  bounds and the Box's filament format both moved between 2026 releases - so
  "which firmware" is the first thing anyone will ask when you report something.

## Before the first real print

- [ ] Check what your bed mesh actually covers vs the 320x320 printable area,
  and keep parts inside the probed region until you've dealt with it:
  [the 15 mm band](../bed-mesh-vs-printable-area/README.md). Read-only query on
  that page; the stock mesh on some firmware leaves a 15-25 mm unprobed strip
  that the slicer will happily print into.
- [ ] Look at the mesh heightmap, not just the variance: a **hill** (centre
  raised) is common out of the box, 0.3-0.6 mm. Print a large first-layer test
  first - if it's even, compensation is handling it. If it's patchy, tram the
  bed with the wrench model in the printer's internal storage:
  [tramming section on the bed-mesh
  page](../bed-mesh-vs-printable-area/README.md#if-the-bed-itself-is-a-hill-tram-it-by-hand).
- [ ] **Calibrate flow first**, before temperature towers or pressure advance.
  The stock `filament_flow_ratio: 0.98` is a blanket default inherited by every
  material, not a measured PLA value - one unit measured 0.94 (4% over-extrusion,
  the classic cause of pronounced layer lines and blobby corners). A PA value
  measured against wrong flow is a wrong PA value:
  [print-quality page](../print-quality-tuning/README.md).
- [ ] While you're in there, know the two stock-profile traps: `0` acceleration
  fields silently inherit 10000 mm/s², and the volumetric cap makes most of the
  speed tiers fiction - same
  [print-quality page](../print-quality-tuning/README.md).
- [ ] First-layer speed 15-25 mm/s is safer for adhesion than the defaults.

## Software setup

- [ ] **OrcaSlicer 2.5.1 or newer** - not for the profiles, for the Box: 2.4.x
  crashes on "Sync filaments" against October-2026 firmware. Profiles shipped in
  2.5.0 stable. [Which version and why](../orcaslicer-profiles/README.md).
- [ ] If you'll print through the Box, enable the printer agent
  (Preferences → Developer → **Use printer agents instead of print hosts**) so
  you get the per-filament slot picker:
  [box-colour mapping](../qidi-box-colour-mapping/README.md).
- [ ] Check SSH works while you're at it: `qidi` / `qiditech`, and the old
  `mks` / `makerbase` login is dead on this generation:
  [SSH access](../ssh-access/README.md). Don't point kiauh or any git-based
  updater at it - QIDI strips the `.git` from klipper/moonraker.
- [ ] Decide whether you want QIDI's cloud tunnel (QIDILink) running. The LAN
  switch on the screen disables it; there's a hard-lock option too:
  [LAN mode and the QIDILink tunnel](../lan-mode-and-qidilink/README.md).

## If it came with a QIDI Box

- [ ] Expect the Control Box panel in the printer's web UI to show **`?`** for
  every slot on 2026 firmware. That's a known breakage, not your unit - and QIDI
 's own changelog says manage Box filament from Studio/touchscreen, not Fluidd:
  [the Fluidd panel page](../qidi-box-fluidd-panel/README.md).
- [ ] Check the desiccant packs actually exist in the rear trays (at least one
  Plus 4 owner's box shipped without them), and treat drying cycles with the
  rear vent **open**: [the box does not vent itself](../qidi-box-drying/README.md).
- [ ] Don't feed PLA or PETG while the box is hot - PLA is locked out of both
  drying modes for a reason (heater elements reach 85 °C against a 40 °C air
  setpoint; there's a sticker inside the box saying the same).

## Small hardware niggles worth catching in week one

- [ ] The PTFE tube from the Box/toolhead scrapes the top glass on stock
  routing - add a clip to the cable chain to hold it lower before it wears a
  groove.
- [ ] PLA with the door closed: don't. The chamber holds ~39 °C with every fan
  at 100% already; Q2 owners report chamber-temperature clogs. Open the door for
  PLA, or look at the Polar Cooler add-on.
- [ ] Consider `driver_SLOPE_CONTROL: 2` on the `[tmc2240 stepper_x]` /
  `[stepper_y]` sections (the stock config ships it commented out). Klipper
  defaults `0` = hottest current-rise slope; `2` measurably cools the driver
  chips at a small high-speed torque cost
  ([Klipper PR #6771](https://github.com/Klipper3d/klipper/pull/6771)).
- [ ] Belts should twang like a low guitar string; loose 9 mm belts are the
  usual suspect if you start seeing layer shifts.

## First prints, in order

1. **Benchy** (one is on the printer's internal storage) - your baseline. Look
   for ringing, layer lines, overhangs.
2. **Flow rate calibration** - Orca's Calibration menu. Before anything else.
3. **Temperature tower** for the filament you'll actually use.
4. **Pressure advance** (PA Pattern, not PA Tower, for fine sweeps) - only after
   flow is right.
5. **Tolerance/dimensional test** - verifies the tuning landed.
6. **Purge chute or waste bin** - practical, and you'll want it before any
   multicolour job: the Box purges inside the chamber and it piles up as spiral
   cones next to the plate.

## Mac users, two specific prompts

- [ ] The first "Test" of the OrcaSlicer connection will fail while macOS pops
  its "wants to find devices on your local network" dialog - grant it, test
  again. Dismissed it? System Settings → Privacy & Security → Local Network.
- [ ] If the browser ever says `ERR_ADDRESS_UNREACHABLE` for the printer while
  `curl` works from the same Mac, it's the same Local Network permission, this
  time for the browser. Quit fully (Cmd+Q) and reopen after toggling.

---

*Compiled November 2026 from the pages of this wiki plus the field notes they
came from. Your unit will differ - that's what the checkboxes are for. Corrections
welcome, that's the whole point of a community wiki.*

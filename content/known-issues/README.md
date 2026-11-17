# Known issues: a symptom-first index

What breaks, and where the fix lives. Entries either link the wiki page that
goes deep, or carry the short version inline (with sources) when nothing else
covers them. Built from this wiki's pages, the [printer-hub.ru 40-issue
roundup](https://printer-hub.ru/en/posts/qidi-plus5-known-issues), QIDI's own
wiki and r/QidiTech3D, October-November 2026. For balance: Smartzone ran one
unit 14 days / ~220 h / 6 kg with zero printer-caused failures, and Tom's
Hardware gave it 4.5/5 - most of what follows is early-firmware, Box-material
or config stuff that stops biting once you know it.

## Bed and first layer

- **The bed is a hill (0.3-0.6 mm mesh range out of the box).** Common,
  often survivable - test before touching anything, tram with the included
  wrench if the first layer is patchy:
  [the tramming section](../bed-mesh-vs-printable-area/README.md#if-the-bed-itself-is-a-hill-tram-it-by-hand).
- **Parts near the edge print on unmeasured bed.** The probed mesh is
  smaller than the printable area:
  [the 15 mm band](../bed-mesh-vs-printable-area/README.md).
- **Poor adhesion unless "bed leveling" runs before every print.** Real and
  reproduced: unchecked in QIDI Studio = poor adhesion, checked = excellent.
  Support's answer is keep it checked; quick pre-print leveling runs ~6 min
  (KAMP probes only the model area, so small parts start faster). For
  full-plate models QIDI says disabling KAMP can be more consistent (`#` the
  KAMP lines in `printer.cfg`, advanced users). Note a manual mesh isn't
  stored until `SAVE_CONFIG`.
- **First layer welded on / white streaks, or gaps between lines.** Both
  extremes get reported - the textured PEI runs grippy until it's washed and
  the Z-offset is a hair higher. Adjust live: More -> Z on the screen, 0.05
  steps (finer: 0.025/0.01/0.005); the buttons move the bed with ~1 s delay,
  don't tap repeatedly.
- **Uneven bed temperature; ASA warps at the edges.** Unit-dependent:
  measured spreads of 8.6 C at a 60 C setpoint (up to 17 C at 90 C) on one
  reviewer's machine, center hottest. Preheat the chamber to profile
  temperature before ABS/ASA, place large parts toward the middle, IR-check
  your own bed at center and edges.
- **The lower-left 9 x 13 mm corner refuses parts.** That's the filament
  cutter's parking zone (`bed_exclude_area` in the profile). QIDI says remove
  the cutter for full-plate printing (two screws on the Q2; no Plus 5 guide
  yet), and re-install it before using the Box again.

## Hot end and extrusion

- **PLA/PETG goes mushy and jams with the lid closed.** Heat creep in the
  39 C-plus chamber; the print then continues with nothing coming out.
  PLA and TPU: slide the top glass back (QIDI's own PLA guide says door open,
  top cover off). PETG is brand-dependent - start open. Numbers and the
  chamber discussion: [the print-quality page](../print-quality-tuning/README.md);
  the official answer is the [Polar Cooler](../physical-mods/README.md).
  Already jammed: magnetic cover off, heat to 280 C, push the plug down with
  the thinnest hex key - about 10 minutes.
- **The print keeps going after a jam.** Without the Box there is no jam or
  tangle detection - the standalone sensor is end-of-filament only. Watch the
  camera on long PLA jobs, and enable spaghetti detection as a partial net
  (limits below).
- **TPU clogs on the stock profile.** The TPU-95 profile has shipped broken
  speeds (200-300 mm/s). Set speeds by hand - Orca's Q2 TPU profile is a
  known-good baseline - use 95A or harder, feed from the external holder,
  lid open.
- **Cutter doesn't fully cut TPU, and the error aborts bed leveling.** The
  start macro cuts before leveling. Press the cutter lever by hand before
  pulling TPU out; failing that, comment out `CUT_FILAMENT_1` in
  `[gcode_macro PRINT_START]` (`gcode_macro.cfg`). Documented on the
  Chinese-only [QIDI TPU page](https://wiki.qidi3d.com/zh/Plus5/tpu-printing-Plus5).
- **200+ mm purge before every print.** Slicer-side, cuttable to ~30 mm:
  [the QoL page](../qol-gcode/README.md).
- **`QDE_002_002` hotend fan speed check error on a new unit.** Assembly
  fault: fan cable pinched under a screw. Check the fan spins when commanded,
  then the cable routing: [the maintenance page's spares
  note](../maintenance/README.md).

## Cooling, chamber, smell

- **Weak part cooling in a hot chamber.** One auxiliary fan, and QIDI's FAQ
  admits a hotter chamber reduces part-cooling efficiency (overhangs,
  bridges). Keep the chamber ~10 C below the filament's softening point; for
  PLA/PETG, chamber heating off and lid open.
- **The smell comes back when you open the lid for PLA.** The 3-layer filter
  only scrubs closed-chamber air - open the lid and you're venting like an
  open-frame printer. Carbon layer is rated 1440 print hours; ventilate the
  room for open-lid PLA.
- **PTFE tube scrapes the top glass** - wear item, clips exist:
  [the physical-mods page](../physical-mods/README.md).

## QIDI Box

- **"Filament failed to enter the extruder" (`QDC_100_005_000_001`).** The
  big one: causes and fixes ranked:
  [the reliability page](../box-reliability/README.md) (50 mm straight tube
  before the hub, the jam-resistant guide, box beside the printer rather than
  on top, ring-dented tubes from the holder springs).
- **A Plus 4 or Q2 Box won't connect directly.** Compatibility tiers: a
  **Max4** Box plugs straight into the Plus 5; **Plus4/Q2** Boxes need the
  separately sold Hub and Signal Cable for PLUS5 (the Plus 4 cable is 4-pin,
  Q2 is 5-pin - don't mix); several Boxes additionally need the Expansion
  Kit. Per [QIDI's FAQ and Box wiki](https://wiki.qidi3d.com/en/QIDIBOX).
- **Box refuses TPU, cardboard spools, brittle composites.** By design: no
  TPU/TPE/PVA, no CF/GF-heavy and brittle filaments, spools must be 50-72 mm
  wide and 195-202 mm diameter. The Box needs its own mains power. Ignore
  the 100% humidity reading for the first seconds after power-on.
- **Box clicks on every load; a colour change costs ~4 min and ~1 g.**
  Economics and the mechanical fix (one-way bearing gear):
  [reliability](../box-reliability/README.md) and
  [physical mods](../physical-mods/README.md).
- **Wrong slot, `?` panel, enable_box**:
  [box-colour mapping](../qidi-box-colour-mapping/README.md) and
  [the Fluidd panel page](../qidi-box-fluidd-panel/README.md).

## Squeaks, clicks and knocks

- **Squeaking during motion.** Ranked by how often the fix works, from
  reports across the QIDI family (Q1 Pro, Plus 4 and the Q2, which shares
  this generation's motion parts):
  1. **A belt riding up the idler pulley's flange.** The Q2 case: the belt
     walks up and down the pulley and squeaks against the flange when it
     rides up - fix is belt tension, per [QIDI's own belt-tension
     guide](https://drive.google.com/file/d/1DtAEVT7H-6fVL1ZpZgguUZqdC-jRw0mG/view?usp=sharing).
     Caveat from the Q1 world: the self-adjusting tensioners have a
     reputation for running chronically loose.
     ([r/QIDI Q2 thread](https://www.reddit.com/r/QIDI/comments/1r2yqmx/q2_y_axis_belt_moving_squeeking_against_pulley/))
  2. **Dry idler pulley bearings.** The Q1 Pro fix: silicone oil on the
     pulleys - all of them, because the culprit is hard to isolate by ear.
  3. **Dry Z lead screws** - the Plus 4 "screech near the top of the screws"
     case: clean them and use **grease, not oil** (NLGI 2):
     [the maintenance page](../maintenance/README.md).
  4. **Dry linear shafts** - the 2-4 week oiling cadence, same page.
  5. **Speed-and-height-specific resonance.** At least one owner's screech
     only happens at one motion speed and height, the tone shifts when you
     touch the rods, and nothing fixes it - he lives with it. Check your
     input-shaper results before chasing a ghost.
- **The belt walks a crooked pulley, rubbing both flanges.** QC issue, not
  maintenance: a crooked X-axis idler out of the box, belt touching both
  flanges, support calling it "within the normal working range". Film it,
  push for a replacement while you're in the return window - belt tensioning
  won't straighten a pulley. ([September
  thread](https://www.reddit.com/r/QidiTech3D/comments/1wf86gv/qidi_plus5_issue_with_pulley_and_bed_leveling/);
  a second owner reported a crooked lower-left idler fresh out of the box.)
- **Knocking on the top glass** - the PTFE tube catching the lid handle
  screws: [the physical-mods page](../physical-mods/README.md).
- **Clicking from the Box on every load** - the one-way gear fix:
  [physical mods](../physical-mods/README.md).

## Slicer and software

- **OrcaSlicer 2.4.x: no profile, sync crashes, wrong slots.** All fixed by
  2.5.1: [the profiles page](../orcaslicer-profiles/README.md). Also check
  PA profiles for a non-zero chamber temperature - early X-Plus 5 PA
  profiles never heated the chamber (fixed by Orca
  [PR #15556](https://github.com/OrcaSlicer/OrcaSlicer/pull/15556)).
- **QIDI Studio on the bundled USB stick has no Plus 5.** It ships an old
  build - install from [GitHub releases](https://github.com/QIDITECH/QIDIStudio/releases)
  (Plus 5 support from 02.07.02.60). Known profile warts: Generic ABS has
  chamber 0 C (ABS Rapido uses 55 C), no ASA profile, 0.24 mm layer cap noted
  on 0.4; and the 02.07.02.60 release has open bugs (won't launch #216,
  macOS crash #219, reprint-from-plate #227, spiral Z-hop "Move out of
  range" #225).
- **Purge waste on the floor behind the printer.** Chutes and bins:
  [the physical-mods page](../physical-mods/README.md).

## Firmware and system

- **Outdated firmware out of the box.** Expect to update on day one
  (notification `QDC_100_005_005_001`). Offline USB method: `QD_Update`
  folder in the drive root, firmware zip unextracted, Settings -> Firmware
  -> Offline update, 10-15 minutes. Back up edited `.cfg` files first -
  updates reset configs to stock. What changed per release:
  [the release history](https://wiki.qidi3d.com/en/Plus5/firmware-release-history)
  and the [community tracker](https://github.com/thelegendtubaguy/Qidi-Plus5-Defaults).
- **Black screen after a firmware update (MASKROM).** UI-only failure: rename
  `QD_Plus5_UI` to `mksscreen.recovery` on the USB stick, power cycle; then
  the SOC package as `mksclient.recovery`. A device showing in RKDevTool as
  MASKROM needs the non-public `KLP_IMG_QD_PLUS5` system image from QIDI -
  email support (and karl@qd3dprinter.com, who runs the wiki). Per QIDI's
  [update page](https://wiki.qidi3d.com/en/Plus5/firmware-update) and a
  September brick thread.
- **Fluidd blank after an update; SSH login "fails".** The wiki's
  `mks`/`makerbase` credentials are stale - this generation is
  `qidi`/`qiditech`: [SSH access](../ssh-access/README.md), and
  [the Fluidd panel page](../qidi-box-fluidd-panel/README.md) for the
  post-update panel breakage.
- **Printer unbound from QIDI Maker after an update, no QR code anywhere.**
  Log out in the *printer's own* user settings (not the app) - the QR
  binding screen comes back.
- **Maker app shows IDLE and 0 C while the printer is printing.** App desync;
  restart both, update to 01.01.01.06+, and use Fluidd on the LAN for
  reliable status. Trust the slicer's time estimate over the screen's.
- **Kiauh or the update buttons bricked it.** Why, and every recovery path:
  [the klipper-mods page](../klipper-mods/README.md).

## Camera and detection

- **Timelapses save at 640x480.** Fix in `crowsnest.conf`:
  [the QoL page](../qol-gcode/README.md).
- **Spaghetti detection false-pauses, or misses failures.** Requirements:
  light-coloured filament, the gold PEI plate, chamber LED on. Medium
  sensitivity when attended, low overnight; small support remnants go
  unnoticed; `QDC_500_005_005_002` ("defect detected in stir-fried
  noodles") infill-pattern false alarms can be ignored. Per
  [QIDI's detection page](https://wiki.qidi3d.com/en/Plus5/Spaghetti_detection).
- **Power loss recovery.** No resume from the first layer; the nozzle stops
  instantly and can leave a blob the resume run hits; a visible resume seam
  is normal on ABS/ASA. Default pause limit 72 h (edit `TIMEOUT` in
  `gcode_macro.cfg` if you must) - the mechanics of that window:
  [the runout page](../runout-and-pause-timeouts/README.md).

---

*Sources: this wiki's pages, the [printer-hub.ru 40-issue
roundup](https://printer-hub.ru/en/posts/qidi-plus5-known-issues) (where most
of the uncovered entries above come from, with links to the original threads),
QIDI's wiki, and r/QidiTech3D. Single-owner reports are marked as such in the
roundup - treat those as leads, not law. New issue? The answer to "has anyone
else seen this" is usually a week-old Reddit thread.*

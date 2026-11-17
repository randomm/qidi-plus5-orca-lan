# How reliable is the QIDI Box, really (and what Orca version you need)

Everything here is community-reported, gathered from r/QidiTech3D, r/QIDI,
OrcaSlicer's issue tracker and independent reviews, October-November 2026. Not
my unit - treat it as a survey, and add your own data point if you have one.
The fix mechanics (Fluidd patch, Orca agent, macros) live on
[their own page](../qidi-box-fluidd-panel/README.md); this one is about what
real users report working and breaking.

## The short version

- **Orca-side (software):** was the flakiest piece through 2.4.x - sync
  crashes, wrong slot loads. Solid since **OrcaSlicer 2.5.0 (2026-11-07)**
  (per-filament slot picker + Plus 5 profiles in stable) and **2.5.1
  (2026-11-14)** (sync crash + material-mapping fixes). **Use 2.5.1 or newer** -
  it is mandatory on October-2026 QIDI firmware.
- **Box-side (hardware):** the *dominant* failure source regardless of slicer -
  PTFE friction and routing, feed failures near the head, box-vs-slicer
  material matching. Most "the Box is unreliable" posts are this, not Orca.
- **Single colour through the Box + auto-refill:** good - near set-and-forget
  once slots are configured box-side and refill spools match brand/type/colour.
- **Multi-colour:** works, but slow and wasteful by design (single nozzle:
  roughly 2-4 min and ~1 g per change). Reliable attended; keep QIDI Studio
  as the fallback for long unattended jobs.

## The OrcaSlicer Box-support timeline

| Version | Date | State |
|---|---|---|
| < 2.3.2 | pre-Feb 2026 | No Box support. Any print (even single colour) could fail with `The value 'Slot-1' is invalid for SLOT` (stale `saved_variables.cfg`); manual macro hacks required ([#11671](https://github.com/OrcaSlicer/OrcaSlicer/issues/11671)) |
| 2.3.2 | Feb 2026 | First official filament sync via QidiPrinterAgent ([#12086](https://github.com/OrcaSlicer/OrcaSlicer/pull/12086)) |
| 2.4.x | 2026 H2 | Sync works but crash-prone ([#12293](https://github.com/OrcaSlicer/OrcaSlicer/issues/12293), [#13949](https://github.com/OrcaSlicer/OrcaSlicer/issues/13949)) and **wrong-slot loads**: colours imported but no tool-to-slot mapping written, so prints loaded a stale slot ([#14599](https://github.com/OrcaSlicer/OrcaSlicer/issues/14599)) |
| 2.5.0-alpha | Oct 2026 | October QIDI firmware changed the box API (`color_slot` to array) -> Orca crashes on "Sync filaments"; Plus 5 and Max 4 explicitly affected ([#16660](https://github.com/OrcaSlicer/OrcaSlicer/issues/16660)) |
| nightly >= Oct 21 / 2.5.0-rc | Oct 2026 | Sync-format fix [#16679](https://github.com/OrcaSlicer/OrcaSlicer/pull/16679) merged; slot picker [#16723](https://github.com/OrcaSlicer/OrcaSlicer/pull/16723) merged Oct 27 |
| **2.5.0 stable** | **2026-11-07** | First stable with Plus 5 profiles + per-filament slot picking in the print dialog (needs *Preferences -> Developer -> Use printer agents instead of print hosts*) + Klipper wipe-tower M400 fix (#17246, was costing ~30 min per 247 tool changes) |
| **2.5.1** | **2026-11-14** | Sync keeps each slot's material (#17089, no more PLA-mapping-everything); more sync/connectivity crash fixes. **Current recommendation** |

## What actually breaks, ranked by report volume

1. **Feed failures - `QDC_100_005_000_001`, "filament failed to enter the
   extruder."** The single biggest multi-colour complaint. Filament stalls
   past the buffer ~13 cm short of the head, and won't unload either. Causes
   seen: PTFE bends too tight near the hub (the hub wants 50 mm perfectly
   straight *before* entry), tube holders denting the tube, heat-deformed
   tube at the extruder end, defective hub clamp, brittle/wet filament snapping
   in the tube, cardboard spools. Fixes reported: re-route tubes via the
   riser hole, a short low-friction tube, a printed jam-resistant filament
   guide ([Printables 1386069](https://www.printables.com/model/1386069-qidi-box-jam-resistant-filament-guide/comments)),
   Capricorn-style tubing.
2. **Wrong slot / stale colour (Orca < 2.5.0 only)** - fixed by the slot
   picker; see
   [the box-colour page](../qidi-box-colour-mapping/README.md). Don't keep
   using the start-gcode identity-map hack on 2.5.x - it breaks runout and
   manual remapping.
3. **Sync and UI crashes (2.4.x era)** - crash on "Sync filaments", crash when
   changing a synced profile, slots mapped to wrong materials (ABS/PC to
   eSUN PLA+). Largely fixed across 2.5.0/2.5.1; #13949 was still open as of
   October.
4. **`enable_box` never touched by Orca** - an external-spool print right
   after a Box print fails ("filament missing 1D") because Orca doesn't flip
   the Box off; QIDI Studio does
   ([#17227](https://github.com/OrcaSlicer/OrcaSlicer/issues/17227)). Console
   workaround: `SAVE_VARIABLE VARIABLE=enable_box VALUE=0` before external
   prints.
5. **Box communication dropouts** - `Lost communication with MCU 'mcu_box1'`,
   worse at 65 C chamber than 55 C and when syncing during preheat.
   Workarounds: reseat internal/external cables, delay Box heating until the
   print starts.
6. **Material matching** - if the slicer filament type doesn't match the Box
   slot type, the printer refuses with a cryptic error
   ([3druck.com Box review](https://3druck.com/en/printers-and-products/qidi-box-in-the-test-mechanically-convincing-but-with-significant-room-for-improvement-00158614/)).
   PLA through the Box is fine; PC is painful (no ready profile,
   under-extrusion with PC/ABS-FR). On 2026 firmware keep slot *identity* in
   QIDI Studio / touchscreen (or patched Fluidd) per QIDI's official position.

## Reports in the other direction

- **Auto-refill works, including over Orca** - multiple users confirm
  generic-filament changeover works (one specifically on OrcaSlicer),
  *provided* slots are configured on the Box/screen side with the same
  brand/type/colour as the pairing candidate. One saved a 23-hour helmet
  print by running out with ~40 layers left and swapping seamlessly.
- **The Plus 5's Box is the Max4-style revision** - on-demand feeding (no
  constant feed like the Q2), faster loading, supports CF/GF filaments, adds a
  bottom access panel for maintenance.
- **QIDI's Plus 5 public tester** printed a model requiring many swaps of
  **PA6-CF + ABS supports** - the exact scenario that lost steps on his Plus
  4 - and the Plus 5 + Box "handled it quite well".
- **3dwork.io review** (Plus 5 + Box combo): weeks across PLA/PETG/ABS/ASA -
  "consistent, no unpleasant surprises".
- **One forced-runout test failed** (Q2): cut the spool mid-print to test
  auto-refill, it air-printed; others can't reproduce. Auto-refill is
  *usually* fine, not guaranteed - don't bet an unattended final layer on it.

## The economics of multi-colour (any slicer)

- One timer measured a colour change at **~4 min and ~1 g** of filament. A
  part that's 1 h 20 / 20 g single-colour becomes ~10 h / ~200 g multicolour.
- Purge piles up **inside the chamber** as spiral cones - print a bin or chute
  before the first multicolour job.
- The Box clicks loudly on every load (community grease mods exist).

## Decision guide

| Use case | Verdict |
|---|---|
| Single colour via Box + auto-refill (Orca >= 2.5.1) | **Good.** Configure slots box-side; same brand/type/colour refill pairs; plastic spools |
| Attended multi-colour, Orca >= 2.5.1 | **Works** - budget ~4 min + ~1 g per change; watch purge waste; re-sync after slot changes |
| Long unattended multi-colour | **Caution.** Feed failures are real and material-matching quirks persist; QIDI Studio is the standing fallback |
| CF/GF technical filaments through the Box | **Mixed.** Supported on paper; friction makes failures likelier - bias to the direct rack feed |
| External spool while Box is attached | **Manual step needed** ([#17227](https://github.com/OrcaSlicer/OrcaSlicer/issues/17227)): flip `enable_box` in the console |
| Orca < 2.5.1 on Oct-2026+ firmware | **Don't** - crashes on filament sync |

## Recommended setup (Nov 2026)

1. OrcaSlicer **2.5.1 or newer**; nothing older on current firmware.
2. Preferences -> Developer -> **Use printer agents instead of print hosts** -
   pick the Qidi agent (Moonraker on 7125 still does the upload).
3. Sync filaments from the printer after physical slot changes; verify slot
   materials match the chips.
4. Set slot *identity* in QIDI Studio / touchscreen / Maker app - or the
   patched Fluidd - per QIDI's position
   ([the Fluidd panel page](../qidi-box-fluidd-panel/README.md)).
5. Pick per-filament **Box slots in the print dialog** (the #16723 feature) -
   don't rely on filament-list order matching slots.
6. Auto-refill on: enable in Box settings, and put the backup spool in
   another slot with identical brand/type/colour.

## Sources

- Orca issues: [#16660](https://github.com/OrcaSlicer/OrcaSlicer/issues/16660),
  [#14599](https://github.com/OrcaSlicer/OrcaSlicer/issues/14599),
  [#13949](https://github.com/OrcaSlicer/OrcaSlicer/issues/13949),
  [#17227](https://github.com/OrcaSlicer/OrcaSlicer/issues/17227)
- [printer-hub.ru - 40 Plus 5 known issues](https://printer-hub.ru/en/posts/qidi-plus5-known-issues)
- [3druck.com Box review](https://3druck.com/en/printers-and-products/qidi-box-in-the-test-mechanically-convincing-but-with-significant-room-for-improvement-00158614/)
- [3dwork.io Plus 5 review](https://3dwork.io/en/qidi-plus-5-review/)
- r/QidiTech3D threads:
  [Box + Orca](https://www.reddit.com/r/QidiTech3D/comments/1poeqqn/qidi_box_and_orcaslicer/),
  [auto-refill](https://www.reddit.com/r/QidiTech3D/comments/1qp5b0w/qidi_box_autorefill_what_happened/),
  [box issues](https://www.reddit.com/r/QidiTech3D/comments/1s05a44/qidi_box_issues),
  [Plus 5 + Box experience](https://www.reddit.com/r/QidiTech3D/comments/1x5r34g/qidi_plus5_with_the_qidi_box_my_experience_so_far/)

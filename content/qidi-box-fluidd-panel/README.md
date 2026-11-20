# The stock Fluidd panel, the 2026 firmware, and the `?` slots

If you open the printer's web UI (the bundled Fluidd) and look at the Control Box
panel on October-2026 firmware, you will see every slot showing **`?`** instead of
its filament. Try to edit a slot and the dropdowns write values the firmware
treats as "not set" - a legacy write to the external spool can reset it to
"PLA Basic". With the Box disabled, the print dialog refuses to start anything:
*"No filament detected. Please insert the external filament."* - even with
filament loaded. The external spool's Load / Unload buttons are greyed out by
construction.

None of that is your unit being broken. The firmware changed; the bundled Fluidd
didn't.

## What actually changed

After the 2026 firmware update (v01.01.02.01 on my unit), each slot's filament is
stored as a **QIDI filament ID** (e.g. `QFA02`) plus a **hex colour**, with the
box state in `multi_color_controller`. The Fluidd build QIDI ships (v1.30.5,
pinned to the firmware and never updated) was written for the old numeric
format: it runs `parseInt` on `QFA02`, gets `NaN`, and renders `?`. Its print
gate reads `box_extras` fields the firmware no longer publishes. It can't be
fixed by config - the panel's JavaScript is simply talking to a data format
that no longer exists.

Same root cause as the box-colour mapping page, opposite end: that page is the
slicer side (OrcaSlicer never writing `value_t`); this one is the printer-side
web UI.

## QIDI's official position

The v01.01.02.01 changelog (2026-10-19) says it outright: manage Box filament in
**QIDI Studio, the touchscreen, or the Maker app - not Fluidd**. Editing via
Fluidd can throw `QDC_100_005_000_001`; QIDI's documented recovery is unload
everything, factory settings, reconfigure the Box filament. Worth knowing before
you click anything in that panel.

## The three ways to fix it

### 1. Patch the bundled Fluidd in place

[Jonathall/qidi-plus5-fluidd-box-fix](https://github.com/Jonathall/qidi-plus5-fluidd-box-fix)
repairs QIDI's own Fluidd build so the panel speaks the new format: slot identity
read/write as QF filament IDs + hex colours (Fluidd and the printer screen agree),
external spool (slot 16) end to end, vendor-filtered dropdowns, a print gate that
reads `filament_switch_sensor` (where the firmware actually publishes presence
now), contextual Load/Unload, and buttons that lock during load/unload operations.
Current build V9.4 (2026-11-11) - slot colours are no longer limited to the
24-entry stock palette, there's a full colour picker, and off-palette hexes write
correctly. Field-tested on the author's printer; I haven't installed it (yet),
so read his README before you start. Shape of it:

- **Verify first**: `~/fluidd/assets/index-DlFvHGAh.js` must MD5 to
  `b9bc4faaf367d0603d92d7217476c57a` (the reference stock bundle, 1,778,604
  bytes). If yours differs, stop - your build isn't the one the patch targets.
- **Two files, two exact locations**: rename both originals to `.orig`, then
  upload the patched bundle to `~/fluidd/assets/index-DlFvHGAh.js` and the
  56-filament catalog (`officiall_filas_list.cfg`) to
  `~/printer_data/config/`. SFTP as `qidi` / `qiditech`
  ([SSH access](../ssh-access/README.md)).
- **Hard-refresh** Fluidd afterwards (Cmd+Shift+R on macOS) - the service worker
  will happily keep serving the old bundle from cache.
- The patcher script (`--check` / `--dry-run` / `--restore`) applies the same
  fix as 16 anchored replacements and refuses to touch a bundle whose anchors
  don't match. On the reference bundle it reproduces the drop-in file byte for
  byte (MD5 `3a4a3f3123154bd0a30983a345263fd5`).

Caveats from the repo: **reapply after every QIDI firmware update** (updates
overwrite the bundle). RFID flows and multi-Box chains are untested. **Never
start a print while a load/unload is running** - stacking the two crashed
Klipper in the author's testing ("Macro G28 called recursively"). The Max 4 and
Q2 have their own patches (Assur92 and Jonathall again) - don't cross-apply.

### 2. Route around it: print from OrcaSlicer, not Fluidd

OrcaSlicer talks to Moonraker directly and never loads the Fluidd UI. With the
printer agent enabled (OrcaSlicer >= 2.5.0, see
[the box-colour page](../qidi-box-colour-mapping/README.md)), the "No filament
detected" gate doesn't apply to you: that gate lives in the Fluidd print dialog,
not Moonraker. External-spool prints sent from Orca work fine on a completely
unpatched printer. This is the zero-touch option if you don't actually need the
web panel.

### 3. Script around it: macros + a PC dashboard

[jcazares76/Qidi-Plus-5-Mods](https://github.com/jcazares76/Qidi-Plus-5-Mods)
doesn't touch any QIDI-owned file. It adds `box_slots.cfg` (one `[include]` line
in `printer.cfg`) with macros that write the same `save_variables` the
touchscreen uses - `SET_SLOT_FILAMENT SLOT=3 FILAMENT=PLA_BASIC COLOR=2850FF`,
`LIST_SLOT_FILAMENTS`, `LIST_FILAMENT_TYPES` - plus a Fluidd-style dashboard
that runs from your PC over Moonraker's API (port 7125, LAN-trusted, no API
key, no SSH needed). Firmware updates replace `printer.cfg` but keep extra
files, so the worst case after an update is re-adding one include line.

## Which one

- You want the web panel to just work, in the browser, on the printer's own UI:
  **option 1**.
- You slice in OrcaSlicer and never open Fluidd's box panel: **option 2**, and
  you're arguably already done.
- You want something scriptable (SSH, console, automation) or you don't want to
  patch vendor files at all: **option 3**.

They coexist: 2 uses neither of the others; 1 and 3 both write the same
`save_variables`, so pick one to *edit* slot identity through and use the other
to read. And whatever you do: per QIDI's own changelog, treat QIDI Studio /
touchscreen as the source of truth when something disagrees.

One separate wart: QIDI Studio itself (since 2.07.02.73) can't start
external-spool prints either - a PC-side Studio bug, not this. Printing from
Fluidd, the touchscreen or Orca is unaffected.

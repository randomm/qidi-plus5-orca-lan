# OrcaSlicer contribution — QIDI X-Plus 5: box tool→slot mapping is never written, so the box loads a stale slot

> **OUTCOME (2026-09-13):** The profile PR (#15663) was opened and passed CI, then
> **withdrawn** after maintainer-community feedback (thelegendtubaguy): the box
> persists `value_t{n}` by design (runout/auto-feed remap + manual remap), so a
> blanket identity reset in the *shared* profile is the wrong layer. Kept as a
> **personal-preset** workaround on our machine; the correct upstream fix is for
> `QidiPrinterAgent` to *write* the user's AMS-chosen mapping per slice (it already
> reads the box). This doc is retained for the analysis + as the basis for that
> C++-agent argument.
>
> Working source for (1) a GitHub **bug issue** and (2) a minimal **profile PR** to
> github.com/OrcaSlicer/OrcaSlicer. Neutral technical register. Per-unit identifiers
> (IP, serials) are placeholders.
>
> **Verification status:** single-colour slot control via `value_t{n}` is VERIFIED on
> hardware (setting `value_t0='slot1'` made a single-colour print load white end-to-end).
> The identity-mapping workaround for *multi-colour* is pending a hardware test — the
> `## Tests` section is marked TODO until that's done.
>
> **Attribution / transparency (goes in both the issue and PR body):**
> *Authored with AI assistance (Claude); reviewed, tested on real QIDI X-Plus 5 hardware,
> and submitted by Janni Turunen, who takes responsibility for the change.*
> Commit trailer: `Co-authored-by: Claude <noreply@anthropic.com>` (git author = Janni).

---

# Part 1 — Bug issue (template: bug_report.yml)

**Title:** QIDI X-Plus 5 + QIDI Box: OrcaSlicer never writes the tool→slot mapping, so prints load a stale/wrong box slot

**Checkboxes:** ✅ verified reproducible on the latest nightly · ✅ searched existing issues

**OrcaSlicer Version:** 2.5.0-dev (nightly, macOS universal)
**OS:** macOS · **OS Version:** 26.x · **Printer:** QIDI X-Plus 5 (0.4 nozzle), 4-slot QIDI Box

**How to reproduce**
1. QIDI X-Plus 5 with the QIDI Box, connected to OrcaSlicer via Host Type **Moonraker (Klipper)**.
2. Load distinct colours in slots 0/1/2 (e.g. red/white/black). Use OrcaSlicer's "Sync filament
   colours from AMS" — the colours import correctly, in slot order.
3. Slice any single-colour model and choose a colour that is **not** the box's currently
   loaded/last slot.
4. Print.

**Actual results**
The print loads whatever physical slot the printer's `value_t{n}` saved variable already
points at, regardless of the colour chosen in OrcaSlicer. On this unit `value_t0` was stuck
at `slot2` (black), so every single-colour print came out black. Manually pre-loading a
different slot on the printer does not help — the print's start sequence reloads from
`value_t{n}`.

**Expected results**
The print uses the slot corresponding to the filament chosen in OrcaSlicer.

**Root cause (verified on-device)**
The QIDI Box resolves tool→slot from Klipper `save_variables`. The `T0`..`T15` macros read
`value_t{n}` and load that slot (`printer_data/config/box.cfg`):
```
[gcode_macro T0]
gcode:
    {% set slot = printer.save_variables.variables.value_t0|default('slot0') %}
    {% if printer.save_variables.variables.enable_box == 1 %}
        EXTRUDER_LOAD SLOT={slot}
    {% endif %}
```
(`T1`→`value_t1|default('slot1')`, etc.) The macro **default is already identity**
(`value_t0`→`slot0`, ...), so the box's native behaviour is tool N → slot N. The bug is that
something wrote `value_t0='slot2'` and it persists as stale state, and **OrcaSlicer never
writes `value_t{n}`**, so the stale value wins. Note the slot is the box's *electronic*
address (each slot has its own motor + RFID; the box tells the combiner which slot feeds) —
not a physical tube position.

OrcaSlicer's Moonraker path (`src/slic3r/Utils/QidiPrinterAgent.cpp`) is a **read-only sync**:
`fetch_slot_info()` reads `color_slot{n}` / `filament_slot{n}` from `save_variables` to
populate the filament list (this works — colours import in slot order,
`filament_colour=#FF362D;#FAFAFA;#060606` = red;white;black). It never **writes** a tool→slot
mapping and injects nothing into gcode. OrcaSlicer's own AMS-sync tooltip states it plainly:
*"Filament type and color information have been synchronized, but slot information is not
included."* That missing slot binding is the bug.

The generated start-gcode contains only `BOX_PRINT_START EXTRUDER=[initial_tool]` and expands
to e.g. `BOX_PRINT_START EXTRUDER=0` — no `value_t{n}`, no mapping command.

**Project file & logs:** [attach zipped .3mf project + debug log zip]

---

# Part 2 — Profile PR

**Title:** Fix QIDI X-Plus 5 box loading a stale slot: reset tool→slot mapping in start g-code

**Target:** `main` · from fork · label `profile` (comment `/bot add-label profile` after opening)

## Description

`Closes #<issue>`.

On the QIDI X-Plus 5 with the QIDI Box, OrcaSlicer never writes the box's tool→slot mapping
(`value_t{n}` saved variables), so prints load whatever slot the printer's persisted
`value_t{n}` happens to hold — commonly a stale value from a previous job — instead of the
slot matching the chosen filament. See the linked issue for the full root-cause analysis.

This is a minimal, profile-only mitigation: prepend an identity reset of the tool→slot
mapping to the X-Plus 5 `machine_start_gcode`, immediately before `BOX_PRINT_START`. It
restores the box macros' own native default (`value_t{n}` → `slot{n}`) at the start of every
print, so tool N deterministically loads slot N and the user's OrcaSlicer filament order (in
slot order, as the AMS sync already imports it) drives the physical colour.

The deeper, complete fix belongs in `QidiPrinterAgent.cpp` (write the user's actual AMS
mapping back, not just read it). This profile change is a low-risk stopgap that makes the
shipped X-Plus 5 profile behave correctly today; happy to close it if you'd prefer to solve
it entirely in the C++ agent layer.

### The change (2 files)

1. `resources/profiles/Qidi/machine/Qidi X-Plus 5 0.4 nozzle.json` — prepend to
   `machine_start_gcode`, inside the `;===== BOX_PREPAR =====` block, immediately before
   `BOX_PRINT_START`:
   ```
   SAVE_VARIABLE VARIABLE=value_t0 VALUE="'slot0'"
   SAVE_VARIABLE VARIABLE=value_t1 VALUE="'slot1'"
   SAVE_VARIABLE VARIABLE=value_t2 VALUE="'slot2'"
   SAVE_VARIABLE VARIABLE=value_t3 VALUE="'slot3'"
   ```
   (The 0.2/0.6/0.8 nozzle profiles inherit this `machine_start_gcode`, so one edit covers
   all four variants. Values are literal — no gcode placeholders — so `validate_slice` is
   unaffected.)
2. `resources/profiles/Qidi.json` — bump `version` `02.04.00.12` → `02.04.00.13`
   (per AGENTS.md: profile changes must bump the sibling vendor bundle version).

## Tests

Verified on a real QIDI X-Plus 5 + QIDI Box (4 slots: 0 red, 1 white, 2 black, 3 orange),
OrcaSlicer 2.5.0-dev, Moonraker (Klipper) LAN connection. The mapping was applied as a
user-preset `machine_start_gcode` override (identical content to this PR's profile edit) and
each slice inspected + printed:

- [x] **Single-colour, filament 2 (white):** sliced gcode contained the four `SAVE_VARIABLE`
      lines and `BOX_PRINT_START EXTRUDER=1`; the print loaded slot 1 (Moonraker
      `slot_sync=slot1`, `last_load_slot=slot1`) and printed white.
- [x] **Single-colour, filament 4 (orange):** gcode `BOX_PRINT_START EXTRUDER=3`; print loaded
      slot 3 (`slot_sync=slot3`) and printed orange. Slot 3 is neither the macro default nor the
      stale slot the bug fell back to (slot 2), so this is a decisive arbitrary-slot result.
- [x] **Mapping persists:** after the prints, `value_t0..t3` read `slot0..slot3` (identity) —
      the closed `BOX_PRINT_START` does not overwrite them.
- [x] `scripts/check_profile.sh -v Qidi` — **all five checks PASS locally** with the patch
      (extra_json_check, validate_system, validate_slice, validate_filament_subtypes,
      validate_custom; diff = 2 files, 2 insertions, 2 deletions). Re-run whole-tree before
      final submission.
- [ ] Full multi-colour print with mid-print `T0→T1` changes not run at time of writing. The
      per-tool lookup is identical for tool changes (each `TN` reads `value_t{n}`), and two
      distinct tools (T1, T3) were verified individually, so it is expected to work; noting it
      honestly as not-yet-exercised end-to-end.

Confirms: OrcaSlicer's filament number → tool index → `value_t{n}` → physical slot, once the
identity mapping is written. Painting the plate with filament 2 emits `T1`, filament 4 emits
`T3`, etc.

## Compliance checklist (AGENTS.md; no CONTRIBUTING/CoC/DCO/CLA exist)

- [ ] Fork → branch → target `main`; PR from fork.
- [ ] 2-file change; no duplicate JSON keys; do not touch `scripts/`, `.github/`, build files.
- [ ] `version` bumped in `resources/profiles/Qidi.json`.
- [ ] `scripts/check_profile.sh` passes locally (5 checks: extra_json_check, validate_system,
      validate_slice, validate_filament_subtypes, validate_custom).
- [ ] PR body: `# Description` with `Closes #<issue>`, `## Tests`, keep artifact link.
- [ ] Transparency line + `Co-authored-by: Claude <noreply@anthropic.com>`, git author = Janni.
- [ ] After opening, comment `/bot add-label profile`.

---

# Notes on scope (accurate upstream status)

- **#11671 "Qidi box support"** — CLOSED/completed. It added the read-side sync
  (`QidiPrinterAgent.cpp`, via PR #12086) and fixed the earlier `Slot-1` hyphen bug. The
  current nightly emits **no** hyphenated slot tokens, so hyphen normalisation is **not**
  needed here.
- **#13236 "AMS/AFC filament sync broken for Moonraker/pull-mode"** — CLOSED/fixed
  (PR #13330 + #13255): a nozzle-diameter default broke preset matching for Moonraker.
- **#13202** — the only open box-related PR (C++: vendor-aware filament matching + Moonraker
  sync). No profile/gcode changes.
- Upstream direction is to handle box/AMS in the C++ printer-agent layer over Moonraker. The
  **write-back of the tool→slot mapping is the remaining gap** — the read path exists, the
  write path does not. This PR is a profile-level stopgap for that gap on the X-Plus 5.

## References

- #11671 — Qidi box support (closed): https://github.com/OrcaSlicer/OrcaSlicer/issues/11671
- #13236 — Moonraker/AMS colour-sync regression (closed): https://github.com/OrcaSlicer/OrcaSlicer/issues/13236
- #13202 — vendor-aware filament matching (open, C++): https://github.com/OrcaSlicer/OrcaSlicer/pull/13202
- `src/slic3r/Utils/QidiPrinterAgent.cpp` — the read-only box sync
- `AGENTS.md`, `scripts/check_profile.sh`, `.github/workflows/check_profiles.yml`

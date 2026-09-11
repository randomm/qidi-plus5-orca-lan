# OrcaSlicer issue draft — QIDI X-Plus 5: box slot mapping not written to gcode (single- and multi-colour load wrong slot)

> Draft for submission to github.com/OrcaSlicer/OrcaSlicer. Neutral technical
> report. Per-unit identifiers (IP, serials) are placeholders.
> Related: #11671 (Qidi box support, closed), #13236 (Moonraker AMS colour-sync regression, open).

## Summary

On a QIDI X-Plus 5 (new 2026 Klipper model) with the 4-slot QIDI Box, connected
to OrcaSlicer via **Host Type: Moonraker (Klipper)**, prints always load the
**wrong physical box slot**. The colour selected in OrcaSlicer has no effect on
which slot is used; the printer loads whichever slot its `value_t{n}` saved
variable already points at. OrcaSlicer does not write the tool→slot mapping into
the generated gcode, so the box uses stale state.

This reproduces the core of #11671 on a printer whose shipped profile does not
appear to carry the box fixes, and is compounded by the colour-sync path in
#13236.

## Environment

- Printer: QIDI X-Plus 5, QIDI Box (4 slots), stock firmware (mid-2026 image,
  Debian 11, Klipper + Moonraker, version strings stripped by QIDI)
- Slicer: OrcaSlicer 2.5.0-dev (nightly, macOS universal)
- Connection: Moonraker (Klipper), bare IP (nginx on :80 proxies Moonraker),
  no API key
- Box sync: OrcaSlicer's AMS auto-sync **does** read the box and shows the three
  loaded colours correctly (red/white/black). So the read path works; the
  write/mapping path is the problem.

## Symptom

- Box slots (left→right): slot0 red, slot1 white, slot2 black, slot3 empty.
- Any single-colour print, regardless of the filament colour chosen in Orca,
  prints from **slot2 (black)**.
- Manually pre-loading a different slot on the printer does not help: the print's
  start sequence cuts it and loads slot2 anyway.

## Root cause (verified on-device)

On the QIDI Box, tool→slot is resolved by Klipper `save_variables`:

`printer_data/config/box.cfg`:
```
[gcode_macro T0]
gcode:
    {% set slot = printer.save_variables.variables.value_t0|default('slot0') %}
    {% if printer.save_variables.variables.enable_box == 1 %}
        EXTRUDER_LOAD SLOT={slot}
    {% endif %}
```
(T1→`value_t1|default('slot1')`, etc.)

`printer_data/config/saved_variables.cfg`:
```
value_t0 = 'slot2'
```
Nothing in any user-visible config writes `value_t0`; it is set by QIDI's closed
box module and persists as stale state. Live Moonraker query during a print:
```
value_t0      = slot2   (black)
slot_sync     = slot2
last_load_slot= slot2
```

The OrcaSlicer-generated gcode contains:
```
BOX_PRINT_START EXTRUDER=0 HOTENDTEMP=240
; filament: 1
; physical_extruder_map = 0
; filament_map = 1
; filament_colour = #26A69A     (cosmetic default; not the physical colour)
```
i.e. Orca writes the logical extruder/filament mapping and a cosmetic colour, but
**never sets `value_t{n}` → `slot{n}`**, and never calls QIDI's mapping command.
So `BOX_PRINT_START EXTRUDER=0` resolves through the stale `value_t0 = slot2`.

The X-Plus 5 registers QIDI mapping commands `MULTI_COLOR_INIT_MAPPING` and
`MULTI_COLOR_INIT_RFID` (via `/printer/gcode/help`), which are the intended hooks
for a slicer to declare the tool→slot mapping — Orca does not invoke them.

## Reproduction

1. QIDI X-Plus 5 + Box, connect Orca via Moonraker (Klipper).
2. Load distinct colours in slots 0/1/2. Auto-sync AMS in Orca (colours appear).
3. Slice any single-colour model; set the filament colour to white.
4. Print. Output is whatever slot `value_t0` points at (here slot2/black), not
   white.

## Proposed fix

1. For QIDI-box printers, emit the tool→slot mapping into the generated gcode —
   either `SAVE_VARIABLE VARIABLE=value_t{n} VALUE='slot{m}'` for each mapped
   tool, or a single `MULTI_COLOR_INIT_MAPPING` call carrying the AMS mapping.
2. Normalise slot tokens to `slot\d+` (lowercase, no hyphen) — #11671 documents
   Orca emitting `Slot-1`, which the box macros reject.
3. Fix the Moonraker AMS colour-sync path (#13236) so filament colours round-trip
   for pull-mode (Klipper/Moonraker) printers.
4. Ensure the shipped **X-Plus 5** machine profile carries whatever box wiring
   #11671 added for Q2/Plus4 (it currently appears not to).

## Workaround (no source changes)

Add to the printer's **Machine Start G-code** in Orca, before the print body, an
identity mapping:
```
SAVE_VARIABLE VARIABLE=value_t0 VALUE="'slot0'"
SAVE_VARIABLE VARIABLE=value_t1 VALUE="'slot1'"
SAVE_VARIABLE VARIABLE=value_t2 VALUE="'slot2'"
SAVE_VARIABLE VARIABLE=value_t3 VALUE="'slot3'"
```
Then arrange Orca's filament list in physical slot order (filament 1 = slot 0,
filament 2 = slot 1, ...). Paint the model by filament; tool N → slot N loads the
matching physical colour. Verified mechanism; matches the #11671 community
workaround.

## References

- OrcaSlicer #11671 — Qidi box support: https://github.com/OrcaSlicer/OrcaSlicer/issues/11671
- OrcaSlicer #13236 — Moonraker/AMS colour-sync regression: https://github.com/OrcaSlicer/OrcaSlicer/issues/13236
- OrcaSlicer commit 9d69d37 (Q2 preset box fixes)
- QIDIStudio commit 1957136 (box support; `//w42` markers)

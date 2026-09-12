# Getting the QIDI Box to print the right colour from OrcaSlicer

Short version: out of the box, it doesn't. If you slice in OrcaSlicer over a
Moonraker connection and print with the QIDI Box, the printer ignores the colour
you picked and loads whatever slot it feels like. For me that was slot 2 (black),
every single time, no matter what I selected. Cost me a few black prints I wanted
white before I worked out why.

This is a known OrcaSlicer gap, not you doing something wrong. It's tracked as
[OrcaSlicer #11671](https://github.com/OrcaSlicer/OrcaSlicer/issues/11671).

## Why it happens

The box decides which slot to load from a Klipper saved variable, `value_t0`
(and `value_t1`, `value_t2`... for the other tools). The `T0` macro literally
reads `printer.save_variables.variables.value_t0` and loads that slot. You can
see it yourself in `box.cfg`.

The problem: **OrcaSlicer never writes those variables.** It sends
`BOX_PRINT_START EXTRUDER=0` and trusts `value_t0` to already be right. It isn't -
it holds whatever slot was used last (mine was stuck on slot 2), so every print
loads that.

And here's the subtle bit I got wrong at first: it's NOT that Orca ignores your
colour. If you sync from the box, Orca pulls the real colours in slot order (I
checked the gcode: `filament_colour=#FF362D;#FAFAFA;#060606` = red;white;black).
Orca even tells you, if you hover a synced filament chip: *"Filament type and color
information have been synchronized, but slot information is not included."* That's
the whole bug in one sentence - the colours come through, the slot binding doesn't.
So Orca knows white exists; it just never tells the printer that white = slot 1.
QIDIStudio writes that mapping; Orca doesn't yet.

You can confirm your own value with a read-only Moonraker query:
```
curl "http://<printer-ip>:7125/printer/objects/query?save_variables" | grep value_t0
```

## The fix that works today

Give Orca the mapping yourself, once, in the printer profile. Printer settings,
Machine G-code, **Machine start G-code** - paste these four lines at the very top,
before everything else:

```
SAVE_VARIABLE VARIABLE=value_t0 VALUE="'slot0'"
SAVE_VARIABLE VARIABLE=value_t1 VALUE="'slot1'"
SAVE_VARIABLE VARIABLE=value_t2 VALUE="'slot2'"
SAVE_VARIABLE VARIABLE=value_t3 VALUE="'slot3'"
```

That resets a clean identity mapping on every print: tool 0 to slot 0, tool 1 to
slot 1, and so on. Now the physical slot follows your Orca filament order.

Then set your filament list in Orca to match the box slot order. Mine is:

- filament 1 = red (slot 0)
- filament 2 = white (slot 1)
- filament 3 = black (slot 2)

One thing worth knowing: a "slot" here is the box's electronic address, not a tube
position. Each slot has its own motor and RFID reader, and the box tells the
combiner which slot is feeding - so the tubes can be plugged into the four-into-one
in any order and slot 1 is still slot 1. Match your Orca filament order to the slot
numbers (which the AMS sync already reports), not to which tube goes where.

Paint the model by filament and it comes out in the matching physical colour.
Single colour white? Paint the whole thing with filament 2. Multi-colour? Paint
with 1/2/3/4 however you like. The colours now come from Orca, which is the whole
point.

Does it actually work? Yes, tested it. Painted a cube with filament 4 (orange),
sliced, printed - the printer loaded slot 3 and out came orange. Painted another
with filament 2 (white) - loaded slot 1, white. Slot 3 is a slot the old bug never
touched, so that one's a proper confirmation, not luck. One gotcha to keep in your
head: the filament *number* picks the slot, not the colour swatch. Recolouring a
chip does nothing to the physical slot - repaint the region onto the filament
number whose slot you actually want.

> Heads up: this only works if your filament list order matches the physical slot
> order. Swap a spool, reorder the list to match. And it won't repaint a print
> that's already running - a single-colour job loads once at the start.

## Is it a hack?

A bit, yeah. Four lines in your start gcode isn't how it should be. The real fix
belongs upstream in OrcaSlicer: write the `value_t{n}` mapping (or call QIDI's own
`MULTI_COLOR_INIT_MAPPING` command, which the Plus 5 does have) so this just works
with no start-gcode edits.

The upstream state, for the record: the box issues everyone points at (#11671 and
[#13236](https://github.com/OrcaSlicer/OrcaSlicer/issues/13236)) are both closed and
fixed. What they fixed is the *read* side - Orca's `QidiPrinterAgent` now reads the
box and imports the colours. What's still missing is the *write* side: it never
sends the tool->slot mapping back. That's the gap these four lines paper over, and
it's what a profile PR (or a proper fix in the C++ agent) should close. Until then,
the four lines get you printing the colours you actually asked for...

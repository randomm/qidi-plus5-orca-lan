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

## The trade-off (read this before you commit to it)

There's a catch, and it's a good one - raised by thelegendtubaguy on the OrcaSlicer
PR, and he's right. The box keeps that `value_t{n}` mapping on purpose. Two cases
where that matters:

- **Runout / auto-feed:** if a slot runs dry mid-print, the box can switch that tool
  to another slot holding the same filament and rewrite `value_t{n}`, so you carry on
  (or reprint) without reslicing. Handy.
- **Manual remap:** you can deliberately point a tool at a different slot from the
  printer screen.

The four-line reset stamps identity back over both, at the start of every print. So
if you lean on runout-resume, or you like remapping slots by hand, this workaround
will fight you. If you (like me) just load your colours in slot order and drive
colour from Orca, it's exactly what you want.

That's why it lives in your **personal** printer preset, not in the shared OrcaSlicer
profile: it's a personal policy, not a universal fix.

### How to undo it
Delete the four `SAVE_VARIABLE` lines from Machine start G-code and save. The box
goes back to managing `value_t{n}` itself (and you're back to picking the slot on
the printer before you print).

### How to check it's working
Slice, then look at the gcode (or query the printer read-only):
```
curl "http://<printer-ip>:7125/printer/objects/query?save_variables" | grep value_t
```
During/after a print, `value_t{n}` should read `slot{n}`, and Moonraker's
`slot_sync` shows the slot actually loaded.

## Is it a hack?

Yeah. Four lines in your start gcode isn't how it should be. The real fix belongs
upstream in OrcaSlicer's `QidiPrinterAgent`: it already *reads* the box and imports
the colours, it just never *writes* the tool->slot mapping back. If it wrote the
mapping you actually picked in the AMS dialog for that slice, you'd get the right
colours with no start-gcode edits - and it would respect runout/manual remaps
instead of stamping over them.

Upstream state, for the record: the box issues everyone cites (#11671 and
[#13236](https://github.com/OrcaSlicer/OrcaSlicer/issues/13236)) are both closed -
they fixed the *read* side. The *write* side is the remaining gap. I proposed a
profile-level version of this fix as OrcaSlicer
[PR #15663](https://github.com/OrcaSlicer/OrcaSlicer/pull/15663) but withdrew it
after the runout/remap feedback above: forcing a mapping in the *shared* profile is
the wrong layer. The write-back belongs in the C++ agent, per-slice, from your AMS
selection. Until that exists, the four lines get you printing the colours you asked
for - as a personal choice, with the trade-off above.

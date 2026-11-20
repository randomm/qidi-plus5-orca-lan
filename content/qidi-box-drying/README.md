# The QIDI Box does not vent itself, and other things I wish I had known

Soo... I had been printing for days assuming the QIDI Box was keeping my filament
dry. That is what a sealed box with a heater and a humidity sensor is for, right?

Then I actually read the sensor. **43% RH.** Which is just room humidity. The box
had been doing precisely nothing.

Here is what I found out, with numbers from my own unit.

## The headline: it recirculates

QIDI's own drying wiki tells you to close the top cover so the box heats properly,
and then says this:

> After an hour or two with the heating on, it's good to open the hole at the back
> of the box for a while to let the humidity out, but then you have to keep in mind
> to close it when the drying is finished at the latest.

That is QIDI telling you the box **recirculates moist air unless a human opens the
rear port**. It is a sealed box. Sealed is great for storage and actively bad for
drying, because the water you pull out of the filament has nowhere to go.

If you have ever run a drying cycle and watched the humidity barely move, that is
why.

## What that looks like in actual numbers

I heated my box to 38 C with the filament still in it and watched the sensor:

| | temp | RH |
|---|---|---|
| before heating | 25.6 C | 43% |
| after ~1 h | 39.7 C | 31% |

31% looks like progress! It is not. Relative humidity is relative to temperature,
so you have to convert to actual water vapour pressure (Magnus formula):

```
25.6 C, 43%  ->  1.409 kPa
39.7 C, 31%  ->  2.250 kPa
```

There is **1.6x more water in the box air than when I started**. That is the
filament outgassing, which is exactly what drying is supposed to do. But it is
still sealed in there with the spools.

Cool that back down to 25 C with the moisture trapped and you get **69% RH**. Worse
than the 43% I started at, because the water has moved out of the plastic and into
the air, and on cooldown it goes straight back in.

So: **open the back vent while it is hot**. This is not a nice-to-have, it is the
entire mechanism.

The vent is a rubberized plug at the back of the box. Nothing dramatic happens when
you pull it, no water runs out, and it should not: this is water vapour, it leaves
invisibly as humid air. The sensor is how you see it. Mine, within minutes of
opening it:

```
sealed, peak : 2.250 kPa water vapour
vent open    : 1.850 kPa   (-17.8%)
```

Projected cooldown RH went from 69% to 59% on that alone, and kept going. That is
the whole fix, and it costs nothing.

Fair warning on how much this matters: a controlled comparison on a Sunlu dryer
found lid-open vs lid-closed came out "within the margin of error". Venting counts
most for long cycles and genuinely wet spools. Mine was a genuinely wet spool.

## PLA is locked out of both of the good modes

This one is not obvious until you go looking.

- **Drying while printing**: officially supported, set in the slicer. But
  "When box recognized PLA filament was placed. You can't use this function."
- **Manual temperature setting**: also disabled with PLA loaded, and QIDI gives the
  reason: the spool does not rotate, so it may heat unevenly.

The automatic program rotates the tray every 5 minutes specifically to prevent
localized overheating. Manual mode does not rotate.

And that matters more than I expected, because the box has three temperature
sensors, not one:

```
heater_box1 (air)     max 40.2 C
heater_temp_a_box1    max 85.8 C
heater_temp_b_box1    max 76.8 C
```

**The heating elements hit 85.8 C while the air sat at 40.** PLA goes soft around
60. With the spool rotating that averages out. Without rotation, you are relying on
the fans and on luck.

I did bypass the block, and a day later it cost me a jam and about three hours of
recovery. See the next section. Do not do this.

## What actually happens if you ignore that block

I ran the box at 38 C for a couple of hours with PLA loaded, using the console
command below. Nothing melted, the print finished, and I thought that was that.

The next day the black filament would not feed. It would not push forward, and the
box could only retract it about 15 cm before stalling. Every eject attempt failed
the same way.

When I finally got the piece out, this is what the end looked like:

```
     thick        necked      thick      necked        thin
   =======<<<<<<<=======<<<<<<<<======<<<<<<<<<<<<<<<<<<<
```

A repeating series of constrictions and bulges, glossy, drawn down well below
1.75 mm. That is **necking**, and it is what a polymer does when you stretch it
past its yield point while it is still ductile. It was pulled like taffy.

This matters because it is the opposite of what I expected. I had assumed brittle
filament snapping. Brittle PLA breaks square and a bit chalky, it does not stretch.
The filament at the failure point was **soft**, not brittle.

So the mechanism is:

1. The box heats a section of filament sitting near the elements. Remember the air
   sensor reads 40 C while the elements are at 85 C.
2. That section goes soft.
3. The feeder pulls. Instead of moving, the filament stretches and necks down.
4. Now you have a thin wavy section with no column strength. It **buckles** instead
   of pushing forward, so it will not feed.
5. And it is too thin for the gears to grip properly, so it will not retract either.

Both failure directions at once, from one soft section.

The moisture was real too, but it did something different. The part of the spool
that was never heated had gone brittle from sitting in a 43% RH box, and crumbled
when I bent it by hand. Two failure modes, two locations, one spool. Do not confuse
them the way I did.

The Q2 manual says it in one line: **do not feed PLA or PETG while the box is hot.**
There is also a sticker inside my box saying the same. Believe them.

### Getting it out again

What worked, in order:

1. **Read the sensors first.** `runout_N`, `b_endstop_state`, `e_endstop_state` and
   the toolhead filament sensor between them tell you which segment the stub is in.
   In my case all of them read empty, which located the piece in the one stretch
   with no sensor coverage: the clear tube between the feeder and the toolhead.
2. **Release the PTFE tubes** at the feeder and at the box. Push-to-connect collets:
   press the tube *inward* first to unload the collet, then press and hold the
   collar down and pull. Collar first, always. This is routine maintenance, not
   disassembly, and it does not require opening anything.
3. **Push the fragment out of the tube with a fresh straight length of filament.**
   This is QIDI's own documented technique for pieces you cannot reach.
4. A ~3 cm stub was left in one slot's feed hole, flush, ungrippable. That came out
   with patient mechanical persuasion.

Things I looked for and which **do not exist**: there is no manual release lever or
idler disengage on the box slot feeders. QIDI's toolhead extruder has one and the
docs tell you to use it, but the box feeders have no equivalent. I also tried
`SET_STEPPER_ENABLE STEPPER="box_stepper slot2" ENABLE=0` to drop the holding
torque, and Klipper rejected it: `Invalid stepper`. The feeder motor, driven from
the UI, is the only grip you have.

Do **not** start by opening things. The 4-in-1 hub is 4 screws and is the serviceable
spot where broken pieces usually end up. The slot feeder gear train is 24+ screws
and at least one owner reports damaging theirs getting in. On a week-old unit,
message support first and get the answer in writing.

QIDI publishes a [QDE error code list](https://wiki.qidi3d.com/en/QIDIBOX/qde-code)
which is worth checking before guessing. QDE_004_002 is the hub already detecting
filament, 004_003 and 004_004 are unload failing to exit the feed port, and 004_009
is filament not exiting the hub.

### The state machine gets stuck too

Worth knowing, because it makes the symptom confusing. The box records where it is
in a load or unload sequence in `saved_variables`, and if a sequence dies partway
the flags stay set:

```
slot2          = -2       (fault; healthy slots read 0, or 2/3 when loaded)
retry_step     = EXTRUDER_UNLOAD2_2
load_retry_num = 5001
extrude_state  = 2        (healthy: -1)
```

Repeated eject attempts resume that same failed sequence. Mine did advance through
steps as I retried, so it is not a hard loop, but it looks like one. Once the
physical obstruction was gone and filament was reloaded, the slot went back to a
normal positive value on its own and the leftover flags stopped mattering.

If you ever do need to reset them, the healthy values are
`retry_step = None`, `load_retry_num = 0`, `extrude_state = -1`.

### Every spool in the box got the same treatment

Obvious in hindsight, and worth saying out loud: only one of my four spools jammed,
but all four were sitting in the same heated box. The black one failed because it
happened to be the loaded one, so it was the only filament under tension. Necking
needs tension, which is why the other three came out looking fine.

That does not mean they are fine. They all got warmed, and the sections closest to
the elements and inside the feeders got the worst of it.

What I would do, and did:

- Pull off and bin a generous length from each spool, 30 to 50 cm. The end that was
  sitting in the feeder is the most suspect part.
- Look at what you unwind. Anything glossy, thinned, oval, flattened or wavy goes in
  the bin, not the extruder.
- Watch the first print of each colour. A section that drew slightly but not enough
  to snap will show up as under-extrusion before it becomes a jam.
- Dry the spools properly before trusting them, in a cycle with the vent open, not
  by holding the box at temperature with filament loaded.

## You cannot set the box heater from Fluidd

The Target field rejects every value and shows "Min or 0". That is not you doing it
wrong.

Query what Klipper reports as its config and there is **no `[heater_generic
heater_box1]` section at all**:

```
config sections mentioning box:
  mcu mcu_box1, box_config box0, box_extras, box_autofeed
```

The heater object is created **at runtime** by `[box_config box0]`, QIDI's closed
module. Fluidd validates a target against `min_temp`/`max_temp` from the config
file, finds nothing, and so rejects everything non-zero.

Same family of problem as the box colour mapping: QIDI's closed box module creates
Klipper objects the standard web UIs have no metadata for.

Console works, because it skips the UI validation:

```
SET_HEATER_TEMPERATURE HEATER="heater_box1" TARGET=40
SET_HEATER_TEMPERATURE HEATER="heater_box1" TARGET=0
```

The two box fans are tied to that heater with `heater_temp 35` in `box.cfg`, so
they start on their own once it is warm. But this is a raw heater set: no timer, no
auto-stop, no rotation, and no `box_drying_state` tracking. Use the touchscreen
program for real drying.

There are also two registered G-code commands for this:

```
MULTI_COLOR_DRY      控制材料烘干    (box drying, what the touchscreen calls)
SET_FILAMENT_DRY     设置耗腔室干燥   (chamber drying)
```

Both come from the closed `multi_color_controller` `.so`. I could not find their
parameters documented anywhere public, and nothing in the visible config calls
them.

## Check your desiccant actually exists

The box has desiccant slots at the **rear trays**. QIDI sells refills, small white
and yellow indicating beads, 4 packs for about $5.

Two things worth knowing:

- At least one Plus 4 owner reported **QIDI forgot to include the packs entirely**.
  So check rather than assume. The basket takes 5 g packs and measures about
  1.75 x 2 inches.
- The stock capacity is small. There is a whole cottage industry of printed
  large-capacity desiccant modules for this box, which is its own kind of verdict.
  If you print one, **print it in ABS** or something else that survives above 65 C,
  because that is what drying cycles run at.

QIDI says refresh "every few months or as indicated by colour change". Disciplined
AMS users do it weekly. Take from that what you will.

## What good actually looks like

Numbers to calibrate against, from people with sensors in their boxes:

| | RH |
|---|---|
| well-maintained new PLA in a sealed box | 11-12% |
| QIDI passive box, desiccant only | around 25% |
| old spool after 4.5 h at 50 C | 21% |
| my box, untouched | 43% |

The 4.5 hour number is the useful one. Only reaching 21% after all that implies
**6-8 hours minimum** for filament that has been sitting out.

The temperatures in the config, for reference. Box drying for PLA is 40 C, taken
from `filament_dev_ams_drying_temperature` in the filament profile, which is
deliberately gentle: the same profile puts PLA softening at 40 C and vitrification
at 45 C. Chamber drying, which is the other method and uses the printer itself, is
in `drying.conf` on the printer:

```
;type    bed   chamber   minutes
PLA      70    55        720
PETG     90    60        720
ABS      90    60        720
```

720 minutes. Twelve hours. Think overnight, not an afternoon.

## If you want to automate it

There is no ready-made scheduled-drying macro that I could find. Two hooks if you
want to build one:

`[delayed_gcode]` gives the raw heater the timer it is missing:

```
[gcode_macro BOX_DRY]
description: Dry box at TEMP for MINUTES, then auto-off
gcode:
    {% set t = params.TEMP|default(40)|float %}
    {% set m = params.MINUTES|default(360)|int %}
    SET_HEATER_TEMPERATURE HEATER="heater_box1" TARGET={t}
    UPDATE_DELAYED_GCODE ID=_BOX_DRY_OFF DURATION={m * 60}

[delayed_gcode _BOX_DRY_OFF]
gcode:
    SET_HEATER_TEMPERATURE HEATER="heater_box1" TARGET=0
```

And the Qidi-Q2-Box-Happy-Hare project shows how to read the box humidity sensor
from Klipper, which is what you would trigger on.

Caveats: it is an edit to `printer.cfg` that a firmware update may overwrite, it
still does not rotate the spool, and for PLA you are working around a block that
exists for a reason. A macro will not save you from dead desiccant either.

## Reading your own box

All read-only, no SSH needed:

```
curl "http://<printer-ip>:7125/printer/objects/query?aht20_f%20heater_box1"
```

gives you temperature and humidity. And:

```
curl "http://<printer-ip>:7125/printer/objects/query?box_extras"
```

gives you `box_drying_state` with `dry_state` and `end_time`, so you can tell
whether a cycle has ever actually run. Mine read `dry_state: 0, end_time: 0`, which
is how I found out the answer was never.

---

*One X-Plus 5 with a 4-slot box, September 2026. Temperatures and humidity are from
my unit, the config values and QIDI's own wiki quotes should apply to any Plus 5,
Q2, Plus 4 or Max 4 with this box. Corrections very welcome.*

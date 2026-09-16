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

I did bypass the block (see below) and nothing melted at 38 C for a couple of
hours. But I would not make it a habit, and now I know why the block is there.

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

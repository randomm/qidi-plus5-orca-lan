# The 15 mm band at the edge of the bed that will eat your print

Soo... this one cost me a whole catapult, a night of printing, and a gantry that
ended up 6.35 mm out of level. Worth writing down, because nothing in the slicer
warns you about it.

Short version: **OrcaSlicer thinks the bed is 320 x 320. The printer only probes
15,15 to 305,305.** Anything you place in that 15 mm band around the edge gets
printed on bed height the machine never measured.

## The numbers

From the Orca machine profile:

```
printable_area  : 0x0, 320x0, 320x320, 0x320
```

From `printer.cfg` on the printer itself:

```
[bed_mesh]
mesh_min: 15,15
mesh_max: 305,305
probe_count: 7,7
```

So there is a 15 mm strip along every edge that is inside the printable area and
outside the probed area. Klipper does not refuse to print there. It extrapolates
the mesh outward from the last probed point and carries on.

And the bed genuinely is not flat. On my unit, from a single print's mesh: the
Y=111.7 row sits around -0.05 mm, Y=160 around +0.01, Y=208.3 around +0.11. That
is a steady rise of roughly 0.16 mm per 97 mm. Extrapolate that out to Y=311 and
you are guessing at another 0.17 mm or so. Guess the sign wrong and your first
layer is either smeared into the plate or barely touching it.

## What it actually did to me

I printed a small catapult plus five "boulders" as ammo. Orca placed the boulders
in a neat row across the back of the plate. Their bounding boxes:

| Object | X range | Y range |
|---|---|---|
| Catapult | 82.2 - **317.7** | 41.3 - 278.8 |
| Rock x5 | 120.6 - **314.1** | 283.1 - **311.6** |

Every rock reaches Y=311.6. That is 6.6 mm past the last probed point. The
catapult reaches X=317.7, which is 12.7 mm past it.

What I found in the morning: half a print, spaghetti everywhere, and the bed
visibly tilted. My guess is a rock let go early, the nozzle started ploughing
into it, and the collisions forced one side of the Z down.

Two things made it worse than it needed to be.

**The printer had no idea anything was wrong.** The job is logged as `completed`
in Moonraker's history. It ran the G-code to the very end, extruding into air the
whole time. There is no failure detection here: no filament-motion check that
catches this, no "is the part still there" check. A print that turns into
spaghetti at 2am looks exactly like a successful one in the job list.

**And the Z axis cannot tell you it skipped.** Both Z steppers ship with:

```
stealthchop_threshold: 9999999999
```

That is permanent stealthChop. Quieter, yes, but you give up torque headroom and
you give up stall detection. When the collisions drove the Z down, nothing logged
an error. Nothing could.

The damage showed up the next morning when I reset the machine and ran calibration
by hand:

```
Retries: 0/4 Probed points range: 6.346719 tolerance: 0.050000
Retries: 1/4 Probed points range: 0.224219 tolerance: 0.050000
Retries: 2/4 Probed points range: 0.010234 tolerance: 0.050000
```

**6.35 mm out**, against a 0.05 mm tolerance. That is about 1.25 degrees across the
bed, which is very much visible to the eye. Credit where it is due: `Z_TILT_ADJUST`
walked it back to 10 microns in three passes without complaint. The compensation
works fine. The problem is that it only runs at print start, so if something moves
mid-print, nothing catches it until the next one.

## What I do now

**Keep everything inside X/Y 305.** That is it. It costs nothing and it is the
actual preventable cause. Orca will happily let you drop a part at Y=311 and say
nothing, so it has to be a habit rather than a warning you wait for.

If you really need the full plate, you can raise `mesh_max` in `printer.cfg`, but
check the probe can physically reach that far first. I have not tried this, so I
cannot tell you where it stops.

Brim on anything near the edges is cheap insurance too.

## Checking your own machine

Read-only, no SSH needed:

```
curl "http://<printer-ip>:7125/printer/objects/query?bed_mesh" | grep -o '"mesh_m[ai][xn]":\[[^]]*\]'
```

And if you want to see whether your gantry is drifting, the tilt error at every
print start is sitting in `klippy.log`:

```
grep "Probed points range" ~/printer_data/logs/klippy.log
```

On a healthy print start mine reads 0.007 mm. Anything in the hundreds of microns
means something moved since last time, and that is worth a look at the Z leadscrew
couplers before you blame the slicer for anything.

---

*Measured on one X-Plus 5 in September 2026, OrcaSlicer 2.5.0-dev. The mesh and
printable-area values come from the stock profile and stock `printer.cfg`, so they
should apply to every Plus 5 until QIDI changes them. Corrections very welcome.*

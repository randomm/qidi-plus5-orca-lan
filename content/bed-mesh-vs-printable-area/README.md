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

(Those bounds are what this page was written against, September 2026. Firmware
v01.01.02.01 ships different stock values - `mesh_min: 25,10`, `mesh_max:
315,315`, `probe_count: 9,9` - a 25 mm unprobed strip on the left, 10 mm at the
front, thin margins on the other two sides. Different shape, same point: the
probed area is smaller than the printable area. Query your own before editing -
read-only command at the bottom of this page.)

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

If you really need the full plate, expand the mesh. Update from a second unit on
firmware v01.01.02.01 (November 2026), where stock ships `mesh_min: 25,10`,
`mesh_max: 315,315`, `probe_count: 9,9` - this edit, applied and verified on that
unit:

```
[bed_mesh]
mesh_min: 10,10
mesh_max: 315,315
probe_count: 11,11
```

- `mesh_min` 25,10 -> **10,10** recovers the left and front strips.
  `mesh_max` was already 315,315 on that firmware.
- `probe_count` 9,9 -> **11,11** keeps the centre point probed and covers the
  wider span (121 points).
- Result: about 305 x 305 mm probed, ~7.5 mm safety margin per side. The
  lower-left 9 x 13 mm cutter zone stays non-printable regardless.
- If the nozzle cannot physically reach 10,10 (probe-out-of-range on mesh
  start), bump `mesh_min` to 15,15 and live with it.
- Leave the other `[bed_mesh]` values (`speed`, `horizontal_move_z`, `algorithm`,
  `bicubic_tension`, `mesh_pps`) stock.

Edit via Fluidd (Configuration -> `printer.cfg` -> Save & Restart). Same caveat as
every `printer.cfg` edit: a firmware update replaces the file - QIDI keeps the old
one as `printer-<date>.cfg` - so re-apply after updates and re-check the probe
still reaches.

Brim on anything near the edges is cheap insurance too.

## If the bed itself is a hill: tram it by hand

The mesh above is about *probed* vs *printable* area. The other half of "my
first layer is bad on a stock machine" is the **shape** of the bed: out of the
box, Plus 5 mesh ranges of 0.3-0.6 mm get reported routinely, and the common
shape is a hill - the centre sits high. One owner's brand-new unit read 0.51 mm
(mostly a back-to-front tilt); an early reviewer measured 0.47 mm with a patchy
first layer; a QIDI program tester's unit read 0.6063 mm. Community-reported
numbers - links at the bottom of this section.

First, decide whether it matters. That tester printed three consecutive full
315 x 315 mm first layers - SUNLU ABS, bed 90 C, chamber 55 C - on the 0.6 mm
bed and called the compensation "surprisingly well". So: **print a large
first-layer test before you touch anything.** If it goes down even and solid,
the mesh is doing its job and tramming is optional.

If the first layer is patchy (wavy gaps, unfilled stripes), tram it:

- The bed mounts to a square frame on carriages either side; the four corner
  screws under it carry **nylon nuts** - and on the Plus 5 there is no locknut,
  the nylon nut is the whole adjuster. Loosening and tightening them pulls the
  plate flatter.
- **Print the wrench first.** QIDI ships a `Hot bed nut wrench` model in the
  printer's own internal files (touchscreen -> Internal), and support will
  email it on request. The nuts are too stiff for fingers.
- The on-screen **Platform calibration** walks the procedure (QIDI calls the
  nuts the "coarse" adjustment). One owner took 0.51 mm down to 0.282 mm this
  way; an early reviewer went 0.47 -> 0.33 mm and got a near-flawless first
  layer after. Rotate in **very small increments** - with no locknut the nut
  holds by friction alone, and it is easy to overshoot.
- Community wrenches exist too, designed for the Plus 4's adjusters (same
  family - check the fit against your nuts): [Kameo's bed adjustment
  wrench](https://www.printables.com/model/1041612-qidi-plus-4-bed-adjustment-wrench)
  is the popular one; [OrbiterNeptune's bed screw adjustment
  wrench](https://www.printables.com/model/1062894-qidi-4-plus-bed-screw-adjustment-wrench)
  and [dsieradzki's two-part tramming tool with 30-degree
  markers](https://cults3d.com/en/3d-model/tool/qidi-plus-4-bed-tramming-tool)
  are alternatives. The last one's markers line up with Fluidd's hour:minute
  screw-adjust notation, which makes repeatable small turns easier.
- Push down on the corner you're adjusting to unload the nut - documented with
  photos for the Max 4, whose bed uses the same arrangement:
  [Max 4 community wiki - Heated Bed
  Screws](https://github.com/thelegendtubaguy/QidiMax4CommunityWiki/blob/main/docs/heated_bed_screws.md).
- Some beds don't tram flat. One owner was still at 0.6-0.8 mm after adjusting
  (and claims the plate is 3 mm thick vs 6 on the Plus 4 - unconfirmed).
  Fallbacks: shim low spots with Kapton tape, or contact support
  (Plus5support@qidi3d.com) if first layers still fail at that range.

Threads worth reading, all r/QidiTech3D:
["QIDI PLUS 5 Poor First Impressions"](https://www.reddit.com/r/QidiTech3D/comments/1vri70p/qidi_plus_5_poor_first_impressions/)
(the "bed is a hill" origin, Aug 2026),
["Bed mesh on new qidi plus 5 - mostly back to front tilt"](https://www.reddit.com/r/QidiTech3D/comments/1wk5o9l/bed_mesh_on_new_qidi_plus_5_mostly_back_to_front/)
(the 0.51 -> 0.282 mm tramming walkthrough + the no-locknut detail), and for
the sibling generation,
["QIDI Q2 warped heated bed - 0.405 mm hump"](https://www.reddit.com/r/QidiTech3D/comments/1uitv8z/qidi_q2_warped_heated_bed_0405_mm_hump_transfers/).
The [printer-hub.ru Plus 5 known-issues
roundup](https://printer-hub.ru/en/posts/qidi-plus5-known-issues) collects
the numbers with sources.

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

*Measured on one X-Plus 5 in September 2026, OrcaSlicer 2.5.0-dev; the mesh
expansion above verified on a second unit on firmware v01.01.02.01, November
2026. The stock mesh values are firmware-dependent - check yours with the query
above before editing. Corrections very welcome.*

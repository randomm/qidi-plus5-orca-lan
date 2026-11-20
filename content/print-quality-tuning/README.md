# Things in the stock X-Plus 5 profile that are worth knowing before you tune

Started with a simple complaint: distinct layer lines and slightly uneven vertical
walls on big prints. Short version of where it landed: **it was over-extrusion**,
from a flow ratio default that is not a PLA value at all. Ended up digging through the actual sliced job, `klippy.log`
and the profile chain to find out why. A few of the things I found are about my
spool and my machine and are useless to you. A few are baked into QIDI's shipped
profile and apply to everyone.

This page is the second kind.

Setup throughout: `0.20mm Standard @X-Plus 5` + `Generic PLA @Qidi X-Plus 5 0.4
nozzle`, 0.2 mm layers, OrcaSlicer 2.5.0-dev.

## Your inner walls are printing at 10000 mm/s2 and you did not choose that

In QIDI's process profiles:

```
inner_wall_acceleration : 0
default_acceleration    : 10000
outer_wall_acceleration : 5000
```

`0` does not mean "no acceleration limit". In Orca it means **inherit
`default_acceleration`**. So your inner walls run at 10000 mm/s2 unless you set
the field explicitly.

That matters because the outer wall gets extruded onto the inner wall. Print the
substrate at 10000 and the nice slow 5000 outer wall is being laid onto something
already rippled.

Now check what your machine actually supports. Mine, from the `SAVE_CONFIG` block:

```
shaper_type_x = ei   shaper_freq_x = 54.4
shaper_type_y = mzv  shaper_freq_y = 36.2
```

36.2 Hz on Y is low for a CoreXY. Shaper smoothing scales with accel over
frequency squared, so a 36.2 Hz axis tolerates roughly (36.2/54.4)2 = 44% of what
the X axis does. Meanwhile `printer.cfg` allows `max_accel: 20000`.

I dropped outer wall to 2500, inner wall to 3000, normal printing to 6000. Flat
walls came out visibly better on the very next print. Not perfect, but clearly
better, and the time cost was small because on a subdivided part the outer wall
already averages about 134 mm/s against 189 commanded: corner deceleration
dominates long before the acceleration ceiling does.

**Do run `SHAPER_CALIBRATE` and use the `max_accel` it gives you** rather than my
numbers. And if your Y frequency comes out in the 30s like mine, that is the thing
actually capping everything, so belt tension is worth a look.

## The speed tiers in the profile are largely fiction

`Generic PLA` sets:

```
filament_max_volumetric_speed : 14
```

Orca models an extrusion bead as a rectangle with rounded ends. For 0.42 mm wide
at 0.2 mm tall:

```
area = 0.2 x (0.42 - 0.2) + pi x 0.1^2 = 0.0754 mm2
14 / 0.0754                            = 185.64 mm/s
```

So **185.64 mm/s is the ceiling**, whatever the speed fields say. At 0.2 mm layers
that gives you:

| Feature | Profile says | Actually runs |
|---|---|---|
| Outer wall | 200 | ~186 |
| Inner wall | 300 | 172 |
| Solid infill | 250 | ~186 |
| Sparse infill | 350 | 172 |

Everything collapses into a narrow band and your outer wall gets infill-grade
treatment. Worth knowing before you spend an evening tuning speed fields that are
not in charge.

If you see the number `185.6372` show up in your Speed tab, that is not a
coincidence: that is this cap, to four decimals.

Raise the volumetric limit only after a flow calibration. And if you do, watch out
for any hard-coded speed values you left behind, because they then become the new
ceiling.

## Step zero: extruder calibration, before any of this

The flow-ratio tuning below assumes the extruder feeds what it's told. If
100 mm commanded isn't 100 mm fed, every calibration after it - flow,
pressure advance, retraction - is measuring a lie. The mark-and-measure
method takes ten minutes:
[Ellis' Print Tuning Guide - extruder
calibration](https://ellis3dp.com/Print-Tuning-Guide/articles/extruder_calibration.html).
(Ellis' note applies here too: rule out a partial clog or extruder tension
issue first - they masquerade as calibration error.)

The corrected value lands in the `[extruder]` section's `rotation_distance`
in `printer.cfg` - which a firmware update replaces, so re-check yours
after updates (stock ships `rotation_distance: 53.1` with a `1517:170`
gear ratio, per the
[firmware tracker](https://github.com/thelegendtubaguy/Qidi-Plus5-Defaults)).

## Flow ratio 0.98 is a blanket default, not a PLA value

> OrcaSlicer's built-in filament calibration places [pressure advance
> before flow](https://www.orcaslicer.com/wiki/guides/calibration_guide) -
> PA is more often wrong out of the box, and cleaner corners from tuned PA
> make the flow test easier to read. The ordering below is what worked on
> *this* machine, measured with the numbers that follow; both orders
> converge if you re-check PA after a big flow change.

This turned out to be the big one, so it goes first.

Every filament ships with:

```
filament_flow_ratio : 0.98
```

Follow the inheritance chain and you find out where that comes from:

```
fdm_filament_common  ->  Generic PLA  ->  Generic PLA @Qidi X-Plus 5 0.4 nozzle
   filament_flow_ratio: 0.98
```

It is set on **`fdm_filament_common`**, the base that ABS, PETG, PLA, TPU and
everything else inherits from. Neither `Generic PLA` nor the nozzle variant
overrides it. So 0.98 was never a PLA number, let alone a measured one. It is one
value for every material QIDI ships.

I ran Orca's flow calibration (Calibration - Flow rate - YOLO Recommended) and
measured **0.94** on my spool. That is 4% less material in every single line.

Reading the YOLO test, since the labels are not obvious: the objects inside
`Orca-LinearFlow.3mf` are named `flowrate_0`, `flowrate_0.01` up to
`flowrate_0.05`, plus `flowrate_m0.01` down to `flowrate_m0.05` (m = minus). So
the numbers are **absolute offsets**, not percentages, and:

```
new flow ratio = current + offset
```

Mine went bad at -0.02 and stayed smooth from -0.03 to -0.05, so the transition
sits just under 0.95 and I took -0.04 for margin.

**Why this matters more than it sounds:** 4% over-extrusion puts a slightly too
wide bead on every layer, each one bulging past the one below. That is the
classic cause of pronounced layer lines, which was my original complaint. It also
piles up material at direction changes, which looks exactly like blobby corners.

## Pressure advance: QIDI's stated floor did not hold on my machine

Stock value in the filament profile:

```
pressure_advance : 0.034
```

QIDI's own pressure advance guidance says direct-drive machines like theirs sit
near the low end of Klipper's typical **0.050 to 1.000** range, which makes 0.034
look too low, below the bottom of the range they themselves quote.

**I measured it, and that is not what my machine wants.** Running the PA Pattern
test (0 to 0.10, step 0.005, DDE) with flow already corrected to 0.94, everything
at 0.04 and below looked good, and above 0.04 the corners started separating,
which is the too-high signature. So the usable top on this unit is about **0.04**,
and the shipped 0.034 was already close to right.

I am leaving this here rather than quietly deleting it, because I went down this
path for a while: the shipped value being below a vendor's own published range
looks like a smoking gun, and it was not one. Print the test.

Do note the PA Pattern step matters. 0 to 0.10 at 0.002 gives you 51 patterns
crammed together and hard to read. 0.005 gives 21 and is fine.

And **do not use PA Tower for a fine sweep**. The tower changes PA every 5 mm of
height (QIDI's own formula: `PA = k_start + floor(height/5) * k_step`), so 0 to
0.10 at 0.002 steps is 50 bands = **250 mm of tall thin tower**. It also greys out
"Print numbers", so you measure height with calipers and do arithmetic. The
pattern is flat, fast, labelled, and cannot topple.

### The corner test, and why it fooled me

Worth knowing, because I read it wrong at first.

On a box, look at all four vertical corners. Mine were **three blobby, one clean**,
the clean one as good as the flat sidewall.

The mechanism for the odd one out: with `retract_when_changing_layer` on plus a Z
hop, the nozzle retracts and lifts at the seam corner, which relieves the pressure
sitting in the melt zone. That corner escapes whatever the other three suffer.

Here is the part I got wrong. **Over-extrusion and low pressure advance produce
nearly identical corner blobs**, and the seam corner masks both of them the same
way. So 3+1 tells you the fault is extrusion-side rather than mechanical, but it
does **not** tell you which of the two. In my case it was flow, not PA.

Still useful as a discriminator against mechanical causes:

- **3 blobby + 1 clean, or 4 blobby** : extrusion side. Calibrate flow first, then PA.
- **Rounded and thinned instead of blobby, corners separating** : PA too high.
- **Ripples that fade as they travel away from the corner** : ringing, not extrusion.
  Input shaping and belt tension.

The clean corner is genuinely useful as a control sample: it proves the machine
*can* lay down a sharp corner, so the fault is not mechanics. That part held up.

**Order matters:** flow first, then PA. A PA value measured against wrong flow is
a wrong PA value, and you will do it twice.

## The chamber runs hot and the exhaust is already flat out

Measured off `klippy.log` over a full print, PLA, bed at 60:

- **Chamber held a flat 39 C for five hours** with the exhaust fan already at 100%.
- Leaving the door open brought it to **31.6 C**.

For reference Orca's own `temperature_vitrification` for Generic PLA is 45 C. So
39 C is not catastrophic, but it is close enough to matter, and the slicer has
nothing left to give you: part fan, auxiliary fan and exhaust were all at 100% for
the entire print. The only lever left is the door.

QIDI owners on the Q2 report chamber-temperature clogs running PLA with the door
and lid closed, so this is not just my unit.

One counterintuitive bit though: a colder chamber makes layer lines **more**
distinct, not less, because the previous layer is stiffer when the next one lands.
So the door helps stringing and clogs and works against layer definition. Pick your
problem.

## Long layer times plus a fan pinned at 100% is why big prints look ribbed

`fdm_filament_common.json` ships `fan_min_speed` and `fan_max_speed` both at 100.
There is no modulation at all: the part fan goes to full at layer 2 and stays there.

On my large parts (224 x 167 mm footprint) each layer took **42 to 48 seconds**.
The nozzle does not come back to the same spot for three quarters of a minute, and
meanwhile the fan is blasting. Every layer is stone cold before the next one lands,
which is exactly how you get crisp, individually readable layer lines and weaker Z
bonding.

Also worth noting: `slow_down_layer_time` is 8 seconds. At 42 to 48 second layers
that threshold never comes anywhere near triggering, so if you were blaming
cooling slowdown for banding on a big part, it is not that.

## Things I ruled out, so you do not have to

All measured on this machine, on the actual failing print:

- **The slicer.** The G-code was behaviourally identical for layers 26 to 187 on a
  wall whose geometry does not change (outer wall constant at 189.4 mm/s, layer
  time 47 to 48 s, no in-layer variation). Identical input, banded output. Not the
  slice.
- **Hotend PID.** Over 20000 log samples at target 220: standard deviation 0.38 C,
  not one sample off by more than 2 C.
- **Cooling slowdown.** See above, 8 s threshold against 48 s layers.
- **Timelapse.** `timelapse_type = 0`, so the per-layer wipe-tower dance never ran.
  Worth checking on yours though, because when it is on it does a retract, spiral
  lift, trip to the trash bin and re-prime on **every single layer**.
- **Geometry.** Outer wall dimensions unchanged from layer 7 to layer 266.

## Still open on my machine

Being honest about what is not settled:

- **Horizontal banding.** Survived everything above. If it is the Z leadscrew it
  should repeat at exactly 4.00 mm (`rotation_distance: 4`). I tried measuring the
  spacing off photos by autocorrelation and the signal was too weak to call.
  Calipers next.
- **Gantry drift between prints.** Tilt error at print start went from 0.007 mm in
  the morning to 0.584 mm the same evening, with no crash in between, just a large
  part levered off the plate. One observation, cause unknown. Checking the
  leadscrew couplers.
- **The fan change.** Still untested, because I opened the door instead and that
  pushes the opposite way.

Early days on this machine tho...

---

*One X-Plus 5, September 2026. The profile values are from QIDI's shipped profiles
and should apply to any Plus 5. The measurements are from my unit and yours will
differ. Flow ratio and pressure advance numbers are deliberately not published here
because they are per-spool and copying mine would make your prints worse.*

# Maintenance: what to lube, when, and with what

Condensed from QIDI's [official maintenance
manual](https://wiki.qidi3d.com/en/Plus5/Maintenance-Manual) plus what the
community adds. The official page is short on the "which product" question, so
that part is spelled out here.

## Schedule

| Interval | Task | Details |
|---|---|---|
| Every print | Build plate check | Quick IPA wipe only if fingerprints/dust or a material change. Adhesion slipping (corners lifting) = wash now, warm water + dish soap. Don't just IPA every print - it leaves its own residue and over-soaking degrades coated PEI. Never acetone. |
| Every 2-4 weeks | X/Y linear shafts | Wipe with an IPA-soaked cloth, then a light coat of ~68 cSt machine oil (Super Lube 51008 synthetic, sewing machine oil, 3-in-1). Move the printhead around to spread it. More often at high chamber temps. |
| Every 1-3 months | Z-axis lead screws | Clean old grease + debris (cloth/toothbrush + IPA), apply a thin coat of NLGI 2 grease, run the bed up/down to spread, wipe excess at the nuts. |
| Monthly | Fan inspection | Four fans: hotend cooling (left of toolhead), part cooling (behind toolhead), aux part cooling (right chamber wall), chamber heater fan (left chamber wall). Compressed air while holding blades still. |
| Every 3-6 months | Belt tension | The 9 mm belts should twang like a low guitar string. Loose belts cause layer shifts. Never lubricate belts. |
| Every 3-6 months | Idler pulley bearings | Clean flanges + bearing faces, apply a drop of light machine oil. Access via back panel or needle applicator (see Pulley bearings section). Squeaking is more often belt alignment than dry bearings — check belt tracking on the pulley first. |
| Every 6 months | Screw check | Frame, gantry, toolhead - vibration loosens things. |
| As needed | Nozzle | Torque 1.5-2.0 N-m, always while heated to printing temp. [Replacement guide](https://wiki.qidi3d.com/en/Plus5/Replace-nozzle). |
| Condition-based | Thermal grease | High-temp printing accelerates loss - see below. [QIDI guide](https://wiki.qidi3d.com/en/Plus5/Replace-silicone-grease). |
| When it degrades | Chamber filter | G3 + H12 HEPA + carbon, 3-in-1. Replace on smell breakthrough during ABS/ASA. |
| When surface wears | Build plate | Light sanding (1000+ grit) refreshes PEI; replace when worn through. |

## Products (the "which grease" answer)

- **Z lead screws - NLGI 2 grease:** Super Lube 21030, Lucas LUC10533 white
  lithium, Lucas 10005 Red 'N' Tacky. QIDI's own manual links exactly these.
- **X/Y shafts - ~68 cSt oil, no additives:** Super Lube 52008, or TSI
  Supercool synthetic vacuum-pump oil (QIDI's second link). Sewing machine /
  3-in-1 oil works but needs re-applying more often.
- Note for Canada: Super Lube 52008/52004 aren't stocked at Home Depot Canada,
  Canadian Tire or Lee Valley - it's Amazon.ca or Motion Canada. The grease
  (21030) is easier to find locally.

## Pulley bearings (idler & motor)

The official Plus 5 maintenance manual doesn't cover pulley bearings — this
section is adapted from QIDI's [Plus 4 pulley
guide](https://wiki.qidi3d.com/en/X-Plus4/Manual/Maintenance-Manual#cleaning-and-lubricating-the-pulley)
and community experience across the QIDI family.

### Which pulleys

- **Motor pulleys** — the toothed pulleys on the A/B stepper motor shafts
  (rear of the printer). These are the easiest to reach.
- **Idler pulleys** — the smooth pulleys in the top corners of the frame
  that the belts turn around. These are the ones that typically develop
  squeaks and are harder to access.

### Before you lubricate — rule out belt alignment

Community reports consistently say idler noise on the Plus 5 / Plus 4 / Q1
Pro generation is more often belt misalignment than dry bearings. Check whether
the belt is tracking centered on the idler pulley. If it's riding up one
flange and squeaking against it, **belt tension** is the fix — not oil. A
walking belt will also wear its edge prematurely.

### Access

The idler pulleys sit in the top corners, boxed in by the side and top
panels. Options ranked by effort:

1. **Needle applicator from above (least invasive).** With the top glass
   removed, angle a long metal needle-nosed oil bottle or a syringe with a
   blunt needle down into the gap between the bearing shield and the pulley
   body. You may need to release belt tension to get enough clearance (see
   #3).
2. **Remove the back panel (best access).** The rear panel comes off with
   its perimeter screws. This exposes the motor pulleys directly and gives
   you a straight shot at the rear idlers. Front idlers are still tight but
   more reachable with the back open.
3. **Release the auto-tensioner (for the stubborn ones).** Power OFF, loosen
   the tensioner screws, then tug the belt gently — this pulls the tensioner
   back and exposes more of the bearing face for a needle applicator.
   Re-tension after. Be careful not to let the belt slip off other pulleys
   while it's loose.

### What to use

- **Clean first:** WD-40 on a q-tip or cloth to wipe grime off the pulley
  flanges and the bearing's outer face. Don't spray — you don't want
  overspray on the belts.
- **Lubricate the bearing:** Same light machine oil as the X/Y shafts
  (~68 cSt, Super Lube 52008 or equivalent). A single drop at the gap
  between the bearing's shield and inner race is enough. These are shielded
  ball bearings (not fully sealed), so oil can penetrate.
- **Motor pulleys:** QIDI's Plus 4 guide shows applying WD-40 directly to
  the motor pulley's toothed surface and bearing to clean it — but this is
  for cleaning accumulated dust, not ongoing lubrication. Follow with a
  light machine oil on the bearing only.
- **Never** get oil or WD-40 on the belt itself or the toothed surface that
  drives it.

### When to replace instead

If a pulley bearing is grinding, has lateral play, or won't quiet down after
cleaning + oil, the bearing is failing — replace the pulley assembly rather
than trying to force oil into a damaged bearing. The idler pulleys use
standard flanged bearings; the exact size isn't published by QIDI but
community reports on the Plus 4 suggest 625ZZ (5×16×5 mm) or similar — verify
before ordering.

### Related: QIDI's Plus 4 pulley videos

QIDI's official Plus 4 maintenance page links to [a Google Drive
folder](https://drive.google.com/drive/folders/1k6UTJ3Xz-aTdcCfHDZss4vN01yzP4014)
with two videos showing the noise before/after WD-40 and exactly where to
apply it on the motor pulley. The motion system is shared with the Plus 5
generation, so the same technique applies.

## Thermal grease - the one that actually matters for hot printers

QIDI doesn't publish a fixed interval - "high temperature printing will
accelerate the loss." Signs it's time: heater errors, slower heat-up, white
crusty powder around the ceramic heater under the silicone sock, temperature
swings mid-print.

Rough intervals by what you print:

| Filament temps | Materials | Reapply |
|---|---|---|
| <=250 C | PLA, PETG, TPU | 6-12 months |
| 250-280 C | ABS, ASA, nylon | 3-6 months |
| 280-330 C | PC, PPS, PPA-CF | Inspect every 50-100 h; replace by 100-200 h |

At 320-330 C the paste dries out aggressively - users report ceramic heater
failures within 100-200 hours. Keep a spare hotend, or at least grease and a
spare ceramic heater, if you live up there.

**What to use:** boron nitride paste (Slice Engineering, Partsbuilt) - the
community go-to for sustained high temps. The sachet in QIDI's accessory kit is
silicone-based and fine for lower temps; standard CPU paste is not rated for
300 C+.

## Spares worth owning

- 0.4 and 0.6 hardened nozzles (stock bimetal wears with CF/GF)
- Spare PEI plate ([QIDI, $39.99](https://qidi3d.com/products/plus5-dual-sided-pei-plate))
- PTFE tubing, 4x2 and 4x3 mm - the tube rubs the top glass; it's a wear item
- Hotend assembly (bimetal, ~$39.99) - known failure: fan cable pinched
  under a screw (QDE_002_002)
- Chamber heater fan, fuses (one ships in the kit)
- Boron nitride paste

## Don'ts

- Never lubricate belts.
- Never acetone on textured PEI.
- Never change the nozzle cold.
- Never let compressed air spin a fan.

---

*Intervals are QIDI's; the failure-mode details are community-reported. Your
usage decides the real cadence - check early, check often. Corrections welcome.*

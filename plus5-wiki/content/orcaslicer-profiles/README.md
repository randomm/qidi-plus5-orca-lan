# X-Plus 5 profiles in OrcaSlicer

Good news first: you don't need to build these by hand. OrcaSlicer already ships
X-Plus 5 profiles. They landed in `main` on 2026-08-07,
[PR #15163](https://github.com/OrcaSlicer/OrcaSlicer/pull/15163).

The catch: that merge is newer than the last stable release (v2.4.2, 2026-07-07).
So a stable build won't have them yet.

## Getting them

Use a nightly. Grab `OrcaSlicer_..._nightly` from the
[nightly-builds release](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/nightly-builds).
First run: add printer, QIDI, X-Plus 5, pick your nozzle (0.2 / 0.4 / 0.6 / 0.8,
0.4 is the default). That's it.

Once a stable ships after August 2026 it'll fold these in and this stops being a
nightly-only thing.

Staying on stable for now? You can copy the X-Plus 5 files from
`resources/profiles/Qidi/` on OrcaSlicer's `main` into your install and add the
model to `Qidi.json`. Doable, but fiddlier than just running the nightly.

## Are the shipped profiles any good?

I actually checked instead of assuming. Flattened OrcaSlicer's 0.4-nozzle machine
profile and compared it against QIDIStudio's own: 46 of 48 core machine
parameters match exactly. Bed 320 x 320, 300 tall. CoreXY. Speeds, accelerations,
jerk, retraction, the bed exclude area, all of it.

The two that differ are deliberate and correct, not sloppiness:

- OrcaSlicer uses `chamber_temperature` where QIDIStudio's Bambu-fork uses
  `chamber_temperatures`. Different naming between the forks. Using QIDIStudio's
  spelling in Orca would just silently do nothing, so this had to be translated.
- The filament-change G-code is wrapped in `{if current_extruder != next_extruder}`
  so a same-tool "change" becomes a no-op.

Per-nozzle deltas (layer-height range, retraction length, the 0.8's longer
tool-change retract) are all carried across. So: faithful port. No reason to
hand-roll your own, and I say that as someone who was about to.

## Connecting Orca to the printer

Point Orca at the printer's IP over Moonraker, port 7125. On the stock image
Moonraker is open on the LAN with no API key, so upload and monitoring just work.
Convenient, and also worth knowing about if you care who else on your network can
drive the printer...

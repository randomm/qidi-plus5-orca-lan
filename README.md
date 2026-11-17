# QIDI Community X-Plus 5 Wiki

Notes and fixes for the QIDI X-Plus 5, in the same spirit as the community
[Plus 4](https://github.com/qidi-community/Plus4-Wiki) and
[Q2](https://github.com/qidi-community/q2-wiki) wikis.

The Plus 5 sits close to the Q2/Max-4 generation, so a lot of their pages carry
over. But a couple of things did change - the SSH account, the cloud tunnel - and
that's mostly what these pages are here to catch.

## Official QIDI wiki

[QIDI X-Plus 5 support page](https://wiki.qidi3d.com/en/Plus5)

---

## Getting in and set up

### [Just arrived: a checklist for a new unit](./content/getting-started/README.md)
First boot, first print, first week - what to verify on a new X-Plus 5, roughly
in order, with the page that explains each item.

### [SSH access](./content/ssh-access/README.md)
`qidi` / `qiditech`. The old `mks` / `makerbase` doesn't work anymore.

### [X-Plus 5 profiles in OrcaSlicer](./content/orcaslicer-profiles/README.md)
Already shipped in OrcaSlicer. Use a nightly until the next stable, and yes, they
turned out to be a faithful port.

### [LAN mode and the QIDILink cloud tunnel](./content/lan-mode-and-qidilink/README.md)
What LAN mode actually does under the hood, and how to shut the cloud tunnel off
properly. The Plus 5 uses `frp` now, not the Plus 4's `udp_server`, so the disable
steps are different.

### [Getting the QIDI Box to print the right colour from OrcaSlicer](./content/qidi-box-colour-mapping/README.md)
Out of the box it loads the wrong slot every time. Why (a stale `value_t0`
variable Orca never writes), and the four-line start-gcode fix that makes colour
selection actually work.

### [The stock Fluidd panel, the 2026 firmware, and the `?` slots](./content/qidi-box-fluidd-panel/README.md)
Every box slot shows `?`, the external spool resets to "PLA Basic", and the print
dialog refuses with "No filament detected". Not your unit - the bundled Fluidd was
never updated for the QF-ID format change. Patch it, route around it, or script it.

---

## Printing well, and not wrecking things

### [The 15 mm band at the edge of the bed that will eat your print](./content/bed-mesh-vs-printable-area/README.md)
Orca thinks the bed is 320x320. The printer only probes to 305x305. Parts placed in
between get printed on bed height nobody measured. Cost me a print and 6.35 mm of
gantry tilt.

### [Things in the stock profile worth knowing before you tune](./content/print-quality-tuning/README.md)
Inner walls silently running at 10000 mm/s2, a volumetric cap that makes the speed
tiers meaningless, a flow ratio that is a blanket default for every material, and
the corner test that tells you which defect you are looking at.

### [Slicing multi-colour jobs completely headless (CLI lane)](./content/headless-colour-slicing/README.md)
**Separate use case:** no GUI at all — `orca-slicer` CLI over SSH, Moonraker
upload/start, QIDI Box swaps. The assemble-list path that actually works, the
per-object `auto_drop` trap, per-job `value_t` bindings, and what really
controls thin-film quality. Read only if you're scripting the slicer.

### [The QIDI Box does not vent itself](./content/qidi-box-drying/README.md)
Mine sat at 43% RH for days doing nothing. Why a sealed box is bad at drying, why
PLA is locked out of both drying modes, why the heater elements hit 85 C, and how
to drive it from the console when Fluidd refuses.

### [How reliable is the QIDI Box, really](./content/box-reliability/README.md)
Community evidence, Oct-Nov 2026: the OrcaSlicer version timeline (2.5.1 is
mandatory on current firmware), what actually breaks ranked by report volume,
feed-failure causes and fixes, auto-refill reports, the economics of
single-nozzle colour changes, and a decision guide.

### [Runout, pause timeouts, and the real spool-refill window](./content/runout-and-pause-timeouts/README.md)
The 12 h `[idle_timeout]` in printer.cfg is not your refill window - QIDI's
PAUSE macro overrides it to 72 h in RAM, the hotend dies instantly on runout,
and here's what actually happens to a job that sits paused past the line.

### [Maintenance: what to lube, when, and with what](./content/maintenance/README.md)
The schedule, the specific greases and oils (NLGI 2 for the Z screws, ~68 cSt
for the shafts), thermal-grease intervals by filament temperature, spares
worth owning, and the don'ts.

### [Quality-of-life G-code and macro changes](./content/qol-gcode/README.md)
Skip the end-of-print unload, 1080p timelapses, a 30 mm start purge instead of
200+, UPS-safe sequential heating, heating the Box during Orca prints, the
`enable_box` console flip, and cooler stepper drivers.

### [Box and printer internals: commands, variables, and traps](./content/box-internals/README.md)
The `save_variables` schema (0-based slots, `slot16` = external), load/unload/
eject commands and their timings, dryer commands, the Moonraker endpoints
worth knowing, and the traps - `M106 P3` killing chamber heating, the
`SLOT=99` Klipper shutdown, `#` in macro code.

### [Klipper mods: what you can change, what breaks, and going mainline](./content/klipper-mods/README.md)
Why kiauh and the update buttons brick QIDI machines (a fork with closed
modules), how people recover, what's safe to mod at the config level, and the
full mainline Kalico/Katapult conversions documented for the Plus 4 and Q2 -
not yet the Plus 5.

### [Physical mods and upgrades](./content/physical-mods/README.md)
Purge chutes and bins, the filament-path fixes (PTFE guide clip,
jam-resistant guide), the D3P riser ecosystem, chamber sealing and filtration,
the Polar Cooler, 320x320 build plates that actually fit, and what you
*don't* need to mod on this generation.

### [Community resources for the Plus 5](./content/community-resources/README.md)
The sibling wikis (Plus 4, Q2, Max 4), the firmware tracker, the fix and tool
repos, the official pages, and where the discussion actually happens.

---

## LAN-only setup — this repo's origin

These pages started as field notes from running one X-Plus 5 **LAN-only with
OrcaSlicer, no QIDI cloud**. The full write-up — profile map, flattened machine
parameters, the upstream comparison, and the read-only printer recon (SSH, the
closed `.so` modules, the QIDILink tunnel and how to disable it) — lives in
[lan-only/](./lan-only/README.md), with the profile tooling
([tools/flatten.py](./tools/flatten.py)) and the Orca profile patches
([contrib/](./contrib/)) alongside.

---

*All of this started from poking at one X-Plus 5 read-only over SSH. Verified vs
inferred is called out where it matters. Corrections and additions very welcome -
that's the whole point of a community wiki...*

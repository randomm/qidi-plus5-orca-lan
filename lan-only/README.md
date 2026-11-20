# QIDI X-Plus 5 — OrcaSlicer + LAN-only notes

Field notes from getting a **QIDI X-Plus 5** (Klipper-based, ~Aug 2026) running
LAN-only with OrcaSlicer, no QIDI cloud. Written against QIDIStudio 02.07.02.60
and OrcaSlicer `main` in September 2026.

Part of the [X-Plus 5 community wiki](../README.md) — this section holds the
full field notes; the wiki pages at the repo root are the distilled,
shareable versions.

## TL;DR

- **OrcaSlicer already ships X-Plus 5 profiles.** They landed in `main` on
  2026-08-07 (commit `b216813b`, PR #15163) and are **byte-for-byte faithful**
  to QIDIStudio's (46/48 critical machine params identical; the 2 diffs are
  deliberate schema fixes). They are **not** in stable v2.4.2 (released before
  that commit) — use a **nightly** build, or copy the 21 machine/process files
  from `main` into a stable install. No hand-porting needed.
- **The printer runs fully LAN-only.** The only thing that reaches QIDI's
  servers is a `frpc` reverse tunnel ("QIDILink") exposing the local Fluidd UI.
  It can be turned off from the printer's LAN switch or hard-disabled via
  systemd. Everything else (slicing, printing, webcam, multi-colour box, mesh)
  is local.
- **SSH default for this generation is `qidi` / `qiditech`** (the older
  `mks` / `makerbase` no longer works on the X-5/Q2/Max-4 generation).
- **The QIDI Box can load the wrong colour** over OrcaSlicer/Moonraker: Orca
  imports the box colours but never writes the tool→slot mapping, so a fresh slice
  can load a stale slot. A four-line `SAVE_VARIABLE` identity map in the machine
  start G-code fixes it for a personal, slot-ordered setup (verified on hardware) —
  but it overrides the box's runout/manual remap, so it's a **personal-preset**
  choice, not for the shared profile (an OrcaSlicer profile PR was proposed and
  withdrawn on that basis). The real fix belongs in Orca's `QidiPrinterAgent`. See
  the [box-colour wiki page](../content/qidi-box-colour-mapping/README.md).
- **Two things in the stock profile will bite you.** Orca's printable area
  (320x320) is larger than the printer's probed bed mesh (305x305), so parts
  placed in that 15 mm band print on *extrapolated* bed height - that cost one
  print and left the gantry 6.35 mm out of level, and Moonraker still logged the
  job as `completed`. And `inner_wall_acceleration: 0` silently inherits
  `default_acceleration` = 10000 mm/s2 on a machine whose measured Y resonance is
  36.2 Hz. Both are profile-level, not unit-specific.
- **The stock flow ratio is a blanket default, and it over-extrudes.**
  `filament_flow_ratio: 0.98` is set on `fdm_filament_common`, the base every
  material inherits - it is not a PLA value and not a measured one. Calibrated
  on this unit: **0.94**, i.e. 4% too much material in every line, which is the
  classic cause of pronounced layer lines. Calibrate flow *before* pressure
  advance: PA measured against wrong flow is wrong. (QIDI's docs put direct-drive
  PA near the low end of 0.050-1.000, which made the shipped 0.034 look too low -
  but measured on this machine the usable top is ~0.04, so 0.034 was fine. That
  hypothesis is recorded as tested and wrong.) See the
  [print-quality wiki page](../content/print-quality-tuning/README.md).

- **The QIDI Box is a sealed box, which makes it good for storage and bad at
  drying.** QIDI's own wiki tells you to open the rear vent by hand during a cycle,
  and the measurement backs it: heating a loaded box moved 1.6x more water into the
  box air, which would have gone straight back into the filament on cooldown (69% RH
  projected, from a 43% start). PLA is additionally locked out of both drying modes,
  because the spool does not rotate and the heater elements reach 85.8 C against a
  40 C air setpoint. Ignoring that block cost me a jam: the filament went soft,
  **necked** under feeder tension down to well below 1.75 mm, and then would neither
  feed (no column strength, it buckles) nor retract (too thin for the gears to
  grip). Recovery needed the PTFE tubes released at both ends and a 3 cm stub worked
  out of a feed hole by hand. There is no manual release lever on the box feeders.
  And `heater_box1` cannot be set from Fluidd at all: it has no config section,
  being created at runtime by QIDI's closed box module. See the
  [box-drying wiki page](../content/qidi-box-drying/README.md).

## What's here

- **[NOTES.md](./NOTES.md)** — the full write-up: profile map, flattened machine
  params, the upstream comparison, and the read-only printer recon (LAN/cloud,
  SSH, closed `.so` modules, QIDILink tunnel + how to disable it). Findings are
  tagged `[VERIFIED]` / `[READ]` / `[UNCONFIRMED]`.
- **The community wiki** — the distilled pages written for other Plus 5 owners
  now live at the repo root: [README](../README.md) covers SSH access,
  OrcaSlicer profiles, LAN mode + the QIDILink tunnel, QIDI Box colour mapping,
  the bed-mesh/printable-area trap, and stock-profile tuning.
- **[tools/flatten.py](../tools/flatten.py)** — resolves QIDIStudio/Orca
  `inherits` chains into a flattened effective config. Usage:
  `flatten.py <bundle-dir> <preset-name>`.

## Not included (by design)

To keep this shareable, the repo excludes (see [`.gitignore`](../.gitignore)):
QIDI's copyrighted profile bundle, this printer's live config (serial numbers,
network IDs, QIDI's proprietary macros), a GPL cache of Orca's profiles, and
QIDI-derived flattened JSON/G-code. Per-unit identifiers (IP, serials, MAC, the
tunnel's private subdomain) have been redacted from the notes.

The `qidi`/`qiditech` SSH default and the QIDILINK server hostname are retained:
both are fleet-wide values already documented publicly by the QIDI community,
not secrets specific to one printer.

## Credits / sources

X-Plus 5 support in OrcaSlicer: the OrcaSlicer project (PR #15163). SSH
credential for this generation: QIDI community (r/QidiTech3D, the Qidi-Max-4
community repos, QIDITECH/QIDI_PLUS4 issue #21). This repo redistributes none of
their code or profile data.

## License

Apache License 2.0 — see [`LICENSE`](../LICENSE) and [`NOTICE`](../NOTICE). The
license covers only the original tool and write-up here; it does not extend to
QIDI's or OrcaSlicer's data, which this repo does not redistribute.

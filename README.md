# QIDI X-Plus 5 — OrcaSlicer + LAN-only notes

Field notes from getting a **QIDI X-Plus 5** (Klipper-based, ~Aug 2026) running
LAN-only with OrcaSlicer, no QIDI cloud. Written against QIDIStudio 02.07.02.60
and OrcaSlicer `main` in September 2026.

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
- **The QIDI Box loads the wrong colour by default** over OrcaSlicer/Moonraker:
  Orca imports the box colours but never writes the tool→slot mapping, so prints
  use a stale slot. A four-line `SAVE_VARIABLE` identity map in the machine start
  G-code fixes it (verified on hardware); a matching OrcaSlicer profile PR is
  prepared in `contrib/`. See the box-colour wiki page.

## What's here

- **`NOTES.md`** — the full write-up: profile map, flattened machine params,
  the upstream comparison, and the read-only printer recon (LAN/cloud, SSH,
  closed `.so` modules, QIDILink tunnel + how to disable it). Findings are
  tagged `[VERIFIED]` / `[READ]` / `[UNCONFIRMED]`.
- **`tools/flatten.py`** — resolves QIDIStudio/Orca `inherits` chains into a
  flattened effective config. Usage: `flatten.py <bundle-dir> <preset-name>`.

## Not included (by design)

To keep this shareable, the repo excludes (see `.gitignore`): QIDI's copyrighted
profile bundle, this printer's live config (serial numbers, network IDs, QIDI's
proprietary macros), a GPL cache of Orca's profiles, and QIDI-derived flattened
JSON/G-code. Per-unit identifiers (IP, serials, MAC, the tunnel's private
subdomain) have been redacted from the notes.

The `qidi`/`qiditech` SSH default and the QIDILink server hostname are retained:
both are fleet-wide values already documented publicly by the QIDI community,
not secrets specific to one printer.

## Credits / sources

X-Plus 5 support in OrcaSlicer: the OrcaSlicer project (PR #15163). SSH
credential for this generation: QIDI community (r/QidiTech3D, the Qidi-Max-4
community repos, QIDITECH/QIDI_PLUS4 issue #21). This repo redistributes none of
their code or profile data.

## License

Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). The
license covers only the original tool and write-up here; it does not extend to
QIDI's or OrcaSlicer's data, which this repo does not redistribute.

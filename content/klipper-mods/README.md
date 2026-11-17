# Klipper mods: what you can change, what breaks, and going mainline

The question every Klipper-adjacent owner asks eventually: can I run kiauh,
update Klipper, install ShakeTune/Kalico/Katapult like on a "real" Klipper
machine? Short answer: **not on the stock system without bricking it**, but
the config level is wide open, and full mainline conversions exist for the
sibling printers.

## Why kiauh and the "update" buttons break QIDI machines

The stock system is QIDI's **fork**, not vanilla Klipper:

- The klipper and moonraker trees ship with `.git` and version files
  **stripped** - Klipper and Moonraker report their version as `?`. There is
  no upstream for kiauh or git to pull against; the tooling just fights the
  fork (this is the mechanical reason behind the warning on
  [the SSH page](../ssh-access/README.md)).
- QIDI's klipper carries **closed compiled modules** the printer depends on:
  `box_extras`, `multi_color_controller`, `box485`, `print_stats_manager`,
  `smart_output_pin`, `ai_func_manager` and friends. Source isn't readable;
  the touchscreen, Box flows and print state sync all live in there.
  Vanilla Klipper has none of it.

So when kiauh (or Fluidd's update button, or a Moonraker restart after a
partial update) replaces QIDI's klipper with a clean upstream one, the host
and the MCU firmware disagree and the closed modules vanish: you get
"the system starts abnormally", a dead touchscreen, or a Klipper that won't
start. This is a repeated, well-documented failure across QIDI generations -
Q1 Pro, X-Max 3, Plus 4 owners have all done it
([r/QIDI recovery thread](https://www.reddit.com/r/QIDI/comments/1j4f4co/i_am_new_to_this_whole_process_can_someone_please/),
[Q1 Pro brick + QIDI's own recovery
doc](https://www.reddit.com/r/qiditech/comments/1g1pug8/qidi_1_pro_the_system_starts_abnormally/)).
QIDI's support line is blunt: the printer uses a custom Klipper and only
works with the official firmware updates.

### If you already broke it

- **Config-error halt** (e.g. `Section gcode_arcs is not a valid config
  section` after a firmware update): edit `printer.cfg` over SSH/Fluidd,
  comment the stale section out, restart. That one's recoverable in minutes.
- **Replaced klipper/moonraker folders**: delete both and restore QIDI's
  builds ([QIDITECH/klipper](https://github.com/QIDITECH/klipper) and the
  matching moonraker), then re-flash the official firmware. For the Series-3
  machines there's a scripted version:
  [billkenney/revert_qidi_software](https://github.com/billkenney/revert_qidi_software).
- **Worst case**: pull the eMMC, image it in an adapter, reflash. Owners have
  recovered this way; it took one of them three weeks. Let that inform the
  risk calculus.

## What you *can* mod on stock (config and userspace level)

The good news: almost everything that matters day-to-day is config, and config
is yours. **But do this first:**

### The one mod before any mod: back up the config

Before the first `[include]` or macro edit, pull the printer's config off the
machine. Firmware updates replace `printer.cfg` wholesale (they leave a
`printer-<date>.cfg` copy, but that's the single file — the shipped macros,
Box config, and Moonraker settings change across versions too). A full backup
gives you a baseline for diffs and a recovery path if an edit halts Klipper.

Config lives at `/home/qidi/printer_data/config/`. SSH in (see
[the SSH page](../ssh-access/README.md)), then:

```bash
# Pull it to your local machine
scp -r qidi@<ip>:/home/qidi/printer_data/config/ ./plus5-config-backup/

# Or compress on the printer first
ssh qidi@<ip> "tar czf /tmp/config-backup.tar.gz -C /home/qidi/printer_data config/"
scp qidi@<ip>:/tmp/config-backup.tar.gz ./
```

Routine:
- Full backup **before your first edit** (your baseline).
- Repeat after every firmware update (the tree changes more than
  `printer.cfg`).
- Keep them dated (`plus5-config-2026-11-17.tar.gz`).
- Diff against the baseline when troubleshooting.

For an automated approach, the community-standard
[klipper-backup](https://github.com/Staubgeborener/klipper-backup) script does
incremental backups on the printer itself and pushes to GitHub — it adds a Moonraker
update-manager plugin, so it shows up in Fluidd's update panel. On QIDI firmware
its Moonraker integration needs the system Moonraker to be writable (the stock
one is), but the automatic dependency updates that the script also configures
will fight QIDI's fork — install only the backup half, not the update half.

After a firmware update, re-adding your mods is a single
`[include my-macros.cfg]` in the new `printer.cfg`.

---

- **Config includes**: add your own `.cfg` files and one `[include]` line to
  `printer.cfg` - macros, fan behaviour, whatever Klipper config supports
  (see [the QoL page](../qol-gcode/README.md) and
  [box-internals](../box-internals/README.md)). Firmware updates replace
  `printer.cfg` (old copy kept as `printer-<date>.cfg`) but leave extra files
  alone - re-add the include after updates.
- **KAMP is already in the stock config** - adaptive meshing and purge ship
  enabled (QIDI's own wiki tells you how to *disable* it). Tuning packs
  exist: [tonngodoc/qidi-plus5-kamp](https://github.com/tonngodoc/qidi-plus5-kamp).
- **Input shaper** is stock functionality: `SHAPER_CALIBRATE`, results
  auto-saved to `printer.cfg` (see
  [the print-quality page](../print-quality-tuning/README.md)). Community
  ShakeTune packaging exists for the
  [Plus 4](https://github.com/qidi-community/ShakeTune-For-Plus4); on the
  Plus 5 the stock tooling covers the same ground.
- **UI level**: [HelixScreen via Gromatou/qidi-plus-5-better-ui](https://github.com/Gromatou/qidi-plus-5-better-ui)
  installs an alternative UI plus Klipper fixes in one command - safe because
  it lives above the klipper core.
- **Anything through Moonraker's API** - dashboards, agents, macros
  ([the Fluidd panel page](../qidi-box-fluidd-panel/README.md) collects the
  options).

## Going full mainline (Kalico / Katapult / kiauh on a clean system)

The real answer to "I want vanilla Klipper" is: wipe QIDI's host stack, flash
Katapult bootloaders and mainline Klipper (or
[Kalico](https://docs.kalico.gg/)) on the MCUs, and use kiauh to install
everything on the clean system. Then kiauh works exactly as advertised.

Published precedents, none of them for the Plus 5 yet (as of Nov 2026):

- **Plus 4**: [phrac/plus4_kalico](https://github.com/phrac/plus4_kalico) and
  [DrFate09/qidi_plus4_klipper](https://github.com/DrFate09/qidi_plus4_klipper)
  - full guides: kiauh install, Katapult on the mainboard via the microSD
  (`qd_mcu.bin` + RESET button), **ST-Link programmer for the toolhead**
  (soldering required). Even
  [KlipperFleet](https://github.com/JohnBaumb/KlipperFleet) lists the Plus 4
  mainboard, toolhead and Box v2 in its flashing compatibility table.
- **Q2** (same generation as the Plus 5): [n3oney/qidi-q2-klipper](https://github.com/n3oney/qidi-q2-klipper)
  does mainline Klipper/Kalico + Katapult *without* an ST-Link;
  [cedbossneo/q2-offload](https://github.com/cedbossneo/q2-offload) moves the
  whole stack to a separate Linux host; [pavver/qidi-q2-klipper-config](https://github.com/pavver/qidi-q2-klipper-config)
  keeps a maintained config against QIDI firmware.
- **FreeDi** ([Phil1988/FreeDi](https://github.com/Phil1988/FreeDi)) - the
  interesting middle road for other QIDI models: mainline Klipper that
  *reuses the factory touchscreen*. Not available for the Plus 4; no Plus 5
  support either. Watch this space.

What you lose going mainline, and it's a lot on this machine: **the
touchscreen** (QIDI's screen talks to the closed modules - Plus 4 guides say
so upfront), the **Box flow automation** (cut/load/purge state machine is
QIDI's code), auto-refill, spaghetti detection, and QIDI support (you're off
the supported path entirely). What you gain: real versions, kiauh, upstream
Klipper features, your own recovery story.

## The decision, compressed

| Want | Do |
|---|---|
| Macros, tuning, KAMP tweaks, UI changes | Config level - safe, survives updates with one re-added line |
| ShakeTune-grade input shaper analysis | Stock `SHAPER_CALIBRATE` covers it; deep analysis waits for mainline |
| Vanilla Klipper / Kalico / kiauh | Full conversion - documented for Plus 4 (ST-Link) and Q2 (no ST-Link), nothing published for the Plus 5 yet |
| To keep the touchscreen and Box automation | Stay stock; there is no mainline-with-screen option for this generation yet |

---

*Stock-system findings verified read-only on one unit plus QIDI's shipped
config; the brick/recovery reports and mainline guides are community-sourced
with links. If you've mainlined a Plus 5, this page wants your writeup.*

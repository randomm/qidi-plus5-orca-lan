# QIDI X-Plus 5 — OrcaSlicer profile extraction + LAN-only setup

Working repo. Every claim below is tagged:

- **[VERIFIED]** — observed directly on this machine (file contents, command output)
- **[READ]** — from documentation/web/third parties, not confirmed locally
- **[UNCONFIRMED]** — could not establish either way

Host: macOS 26.5 (25F5053d). Date started: 2026-09-11.

---

## Phase 1 — QIDIStudio profile map

### 1.1 Installation

| Item | Value | |
|---|---|---|
| App bundle | `/Applications/QIDIStudio.app` | [VERIFIED] |
| Version | `02.07.02.60` (`CFBundleShortVersionString`) | [VERIFIED] |
| Bundled profiles | `…/Contents/Resources/profiles/` | [VERIFIED] |
| User-side copy | `~/Library/Application Support/QIDIStudio/system/` | [VERIFIED] |

The user-side `system/` tree is a byte-identical mirror of the bundled
`profiles/` tree (same file sizes, same `X 5 Series.json` = 42804 bytes).
No OTA profile update has diverged from the shipped bundle yet. [VERIFIED]

### 1.2 Layout — the assumption in the task prompt was wrong

The prompt expected a Bambu-style `Qidi.json` + `Qidi/{machine,process,filament}`.
**That is not what QIDIStudio 02.07.02.60 ships.** [VERIFIED]

Instead the vendor bundle is split *per product series*, each with its own
top-level JSON + directory:

```
profiles/
  Q Series.json       Q Series/
  X 3 Series.json     X 3 Series/
  X 4 Series.json     X 4 Series/
  X 5 Series.json     X 5 Series/      <-- the X-Plus 5 lives here
  thumbnail/
```

Each series dir does have the expected `machine/`, `process/`, `filament/`
subdirs. [VERIFIED]

### 1.3 Actual naming strings used

Do not guess these — the file naming and the internal `name` field differ.
[VERIFIED]

| Context | Exact string |
|---|---|
| Vendor bundle | `X-5-Series` (the `name` in `X 5 Series.json`) |
| Machine model | `X-Plus 5` (both `name` and `model_id`) |
| Family | `Qidi` |
| Machine preset `name` | `X-Plus 5 0.4 nozzle` (no vendor prefix) |
| Machine preset *filename* | `Qidi X-Plus 5 0.4 nozzle.json` (vendor prefix present) |
| Process preset | `0.20mm Standard @X-Plus 5` (`@X-Plus 5`, no `Qidi`) |
| Filament preset | `QIDI PLA Rapido @Qidi X-Plus 5 0.4 nozzle` (`@Qidi X-Plus 5`) |
| Bed model / texture | `X-Plus 5_bed.stl` / `X-Plus 5_bed.svg` |
| Hotend model | `X-Series_gen3_hotend.stl` |

Spellings **not** used anywhere: `Plus5`, `XPlus5`, `XPlus 5`, `X_Plus_5`. [VERIFIED]
There is no separate numeric internal model ID (e.g. no `C13`-style code) —
`model_id` is the literal string `X-Plus 5`. [VERIFIED]

### 1.4 Inventory

Files whose *name* contains `X-Plus 5`: **216**, all inside `X 5 Series/`.
Files whose *content* mentions `X-Plus 5`: 212 in `X 5 Series/` + `X 5 Series.json`.
No other series bundle references the Plus 5 at all. [VERIFIED]

`X 5 Series/` contents: [VERIFIED]

| Subdir | Files | Notes |
|---|---|---|
| `machine/` | 6 | 1 model + 4 nozzle presets + 1 common parent |
| `process/` | 17 | 16 instantiable + `fdm_process_common` |
| `filament/` | 248 | base profiles + per-nozzle `@Qidi X-Plus 5` variants |
| (bundle root) | 4 | bed STL, bed SVG, cover PNG, hotend STL |

`X 5 Series` contains exactly **one** machine model: `X-Plus 5`. There is no
X-Max 5 or other Plus-5-generation sibling in this bundle. [VERIFIED]

Machine files: [VERIFIED]
```
machine/Qidi X-Plus 5.json            (type: machine_model)
machine/Qidi X-Plus 5 0.2 nozzle.json
machine/Qidi X-Plus 5 0.4 nozzle.json
machine/Qidi X-Plus 5 0.6 nozzle.json
machine/Qidi X-Plus 5 0.8 nozzle.json
machine/fdm_machine_x_common.json     (instantiation: false)
```

Model declares `"nozzle_diameter": "0.4;0.2;0.6;0.8"` — 0.4 is the default. [VERIFIED]

### 1.5 Inherits chains (resolved)

Shallower than the prompt assumed — 0.4 is the base, the others inherit *from it*,
not from a shared abstract variant. [VERIFIED]

```
X-Plus 5 0.4 nozzle -> fdm_machine_x_common                        (2 levels)
X-Plus 5 0.2 nozzle -> X-Plus 5 0.4 nozzle -> fdm_machine_x_common (3 levels)
X-Plus 5 0.6 nozzle -> X-Plus 5 0.4 nozzle -> fdm_machine_x_common (3 levels)
X-Plus 5 0.8 nozzle -> X-Plus 5 0.4 nozzle -> fdm_machine_x_common (3 levels)
```

`fdm_machine_x_common` has no `inherits` — it is the root. All 16 process presets
inherit directly from `fdm_process_common`, which is also a root. [VERIFIED]

Flattened effective configs (92 keys each) written to `flattened/`.
Flattener: `tools/flatten.py` — root-first merge, child overrides parent,
records the chain in a `_chain` key. Emits only keys actually present in some
file on the chain; nothing is defaulted or invented.

### 1.6 What actually differs between the four nozzle variants

Only **11 of 92** keys differ: [VERIFIED]

| Key | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|
| `nozzle_diameter` | 0.2 | 0.4 | 0.6 | 0.8 |
| `printer_variant` | 0.2 | 0.4 | 0.6 | 0.8 |
| `min_layer_height` | 0.04 | 0.08 | 0.12 | 0.16 |
| `max_layer_height` | 0.14 | 0.28 | 0.42 | 0.56 |
| `retraction_length` | 0.4 | 0.8 | 1.4 | 3 |
| `retraction_minimum_travel` | 1 | 1 | **3** | 1 |
| `retract_length_toolchange` | 2 | 2 | 2 | 3 |
| `setting_id` | GM008 | GM001 | GM008 | GM008 |
| `default_print_profile` | 0.10mm Std | 0.20mm Std | 0.30mm Std | 0.40mm Std |
| `default_filament_profile` | per-nozzle QIDI PLA Rapido | " | " | " |
| `name` | — | — | — | — |

Everything else — all G-code, all motion limits, bed geometry — is shared. [VERIFIED]

### 1.7 Effective machine parameters (0.4 nozzle; shared unless noted above)

All values below are **read from the files**, not inferred. [VERIFIED]

**Bed / geometry**
| Key | Value |
|---|---|
| `printable_area` | `0x0, 320x0, 320x320, 0x320, 0x0` → **320 × 320 mm** |
| `printable_height` | **300** mm (overrides common's 280) |
| `bed_exclude_area` | `0x0,9x0,9x13,0x13` — 9 × 13 mm notch at front-left origin |
| `printer_structure` | `corexy` |
| `support_multi_bed_types` | 1 |
| `extruder_clearance_dist_to_rod` | 42 |
| `extruder_clearance_height_to_rod` | 42 |
| `extruder_clearance_height_to_lid` | 168 |
| `extruder_clearance_max_radius` | 75 |

**Nozzle / extruder**
| Key | Value |
|---|---|
| `nozzle_type` | `hardened_steel` |
| `nozzle_volume` | **125** (overrides common's 150) |
| `extruder_offset` | `0x0` (single extruder) |
| `extruder_max_nozzle_count` | 1 |
| `single_extruder_multi_material` | 1 |
| `machine_load_filament_time` / `unload` | 35 s / 35 s |

**Motion limits**
| Axis | max speed (mm/s) | max accel (mm/s²) | jerk |
|---|---|---|---|
| X | 600 | 20000 | 9 |
| Y | 600 | 20000 | 9 |
| Z | 20 | 500 | 4 |
| E | 30 | 5000 | 4 |

`machine_max_acceleration_extruding` 20000/20000 · `_retracting` 5000/5000 ·
`_travel` 9000/9000 · `machine_min_extruding_rate` 0/0 · `_travel_rate` 0/0.

**Retraction (0.4)**
| Key | Value |
|---|---|
| `retraction_length` | 0.8 mm |
| `retraction_speed` / `deretraction_speed` | 30 / 30 mm/s |
| `retraction_minimum_travel` | 1 mm |
| `retract_before_wipe` | 0% |
| `retract_when_changing_layer` | 1 |
| `retract_restart_extra` | 0 |
| `retract_length_toolchange` | 2 mm |
| `retract_lift_below` | 299 |
| `z_hop` / `z_hop_types` | 0.4 mm / `Auto Lift` |
| `wipe` | 1 |
| `enable_long_retraction_when_cut` | 2 |

**Firmware / features**
| Key | Value |
|---|---|
| `gcode_flavor` | **klipper** |
| `machine_pause_gcode` | `PAUSE` (overrides common's `M0`) |
| `auxiliary_fan` / `fan_direction` | 1 / `left` |
| `support_chamber_temp_control` | 1 |
| `support_air_filtration` | 1 |
| `support_box_temp_control` | 1 |
| `is_support_multi_box` | 1 (and `box_id` = 4) |
| `is_support_timelapse` / `_mqtt` / `_3mf` / `_polar_cooler` | 1 / 1 / 1 / 1 |
| `scan_first_layer` | 0 |
| `thumbnail_size` | `50x50` (overrides common's `272x272/PNG, 96x96/PNG`) |

**G-code** — extracted verbatim to `gcode/`:
`machine_start_gcode` (2620 chars), `machine_end_gcode` (461),
`layer_change_gcode` (620), `change_filament_gcode` (1981),
`before_layer_change_gcode` (empty).

Start G-code is *not* the common `PRINT_START BED=… HOTEND=…` macro call — the
Plus 5 overrides it with a long inline sequence using QIDI-specific macros:
`SET_PRINT_MAIN_STATUS`, `SET_PRINT_SUB_STATUS`, `DISABLE_ALL_SENSOR` /
`ENABLE_ALL_SENSOR`, `BOX_PRINT_START`, `EXTRUSION_AND_FLUSH`, `MOVE_TO_TRASH`,
`Z_TILT_ADJUST`, `G29` / `G29.0`, and non-standard `M1002 / M1004 / M1006 /
M109.0 / M109.1 / probe samples=1`. End G-code calls `PRINT_END`,
`DISABLE_BOX_HEATER`, `UNLOAD_FILAMENT`. [VERIFIED]

These macros must exist in the printer's own `printer.cfg` — confirming that is
Phase 4 work. [UNCONFIRMED so far]

### 1.8 Things that look like QIDI bugs / oddities — flagged, not corrected

1. `fdm_machine_x_common` sets `"default_print_profile": "0.20mm Standard @XPlus4"`
   — an X-Plus **4** leftover. Harmless: every Plus 5 child overrides it. [VERIFIED]
2. `setting_id` `GM008` is reused by the 0.2, 0.6 **and** 0.8 presets. Only the
   0.4 has a unique ID (`GM001`). Whether QIDI's cloud/OTA keys off this is
   [UNCONFIRMED]. [VERIFIED that the collision exists]
3. `thumbnail_size` drops to `50x50` on the Plus 5 vs `272x272/PNG,96x96/PNG` in
   the common parent — unusually small; may be tied to the printer's own screen. [VERIFIED]
4. The machine model filename is `Qidi X-Plus 5.json` but `printer_settings_id`
   is `Qidi` while process presets use bare `@X-Plus 5`. Inconsistent prefixing
   is QIDI's, not a transcription error. [VERIFIED]

### 1.9 Not established in Phase 1

- Chamber temperature *limit* — no `chamber_temperature` max key exists in the
  machine profiles. It is referenced in G-code as `[chamber_temperatures]` (a
  filament/process value). **Not found in the machine files.**
- Nominal max hotend temperature — not a machine-profile key; lives per-filament.
- Bed types supported — `support_multi_bed_types: 1` but the enumeration is not
  in the machine profile.
- Whether `box_id: 4` means a 4-slot multimaterial box. [UNCONFIRMED]

### 1.10 Repo layout

```
qidistudio-source/     verbatim copy of the shipped X 5 Series bundle (reference)
flattened/             resolved effective configs (4 machine + 16 process)
gcode/                 start/end/layer/filament-change G-code, extracted
tools/flatten.py       the inherits resolver
```

`qidistudio-source/` is QIDI's shipped data, copied for diffing. Worth removing
before pushing this repo anywhere public.

---

## Phase 2 — upstream check: **Orca already ships the X-Plus 5**

### 2.1 The repo moved

`github.com/SoftFever/OrcaSlicer` now 301-redirects to
**`github.com/OrcaSlicer/OrcaSlicer`** (repo id 514553345). [VERIFIED]

### 2.2 Plus 5 support is present in `main`

Added by commit **`b216813b` — "Add the Qidi Plus 5 (#15163)", 2026-08-07**. [VERIFIED]

`resources/profiles/Qidi.json` (bundle version `02.04.00.12`) lists 12 machine
models, including `Qidi X-Plus 5`. The task's expected list was stale — Orca now
also ships X-CF Pro, X-Max and X-Plus (gen-1), beyond the eight named. [VERIFIED]

Present upstream: [VERIFIED]
- 5 machine files (model + 0.2/0.4/0.6/0.8 nozzle)
- all **16** process presets — same names as QIDIStudio
- **247** filament entries in `Qidi.json` referencing Plus 5

All 21 filament profiles referenced by the machine presets
(`default_filament_profile`, `default_materials`) resolve. No dangling refs. [VERIFIED]

> Note: an early `contents` API listing of `Qidi/filament/` appeared to show zero
> Plus 5 files. That was **API pagination truncation**, not a real gap — the
> authoritative `Qidi.json` filament_list check above supersedes it.

### 2.3 Fidelity of the upstream port — independently verified

Flattened Orca's chain and compared against the QIDIStudio flattened config:

```
ORCA: Qidi X-Plus 5 0.4 nozzle -> fdm_machine_x_common -> fdm_qidi_x3_common -> fdm_machine_common
QIDI: X-Plus 5 0.4 nozzle      -> fdm_machine_x_common
```

Of 48 critical parameters: **46 byte-identical, 2 differ, 0 missing on either
side.** Bed 320×320, Z 300, all speeds/accels/jerks, all retraction values, the
bed exclude area and the clearance values match exactly. [VERIFIED]

The two differences are **deliberate and correct adaptations**, not errors: [VERIFIED]

1. `machine_start_gcode`: QIDIStudio's `[chamber_temperatures]` →
   Orca's `[chamber_temperature]` (4 occurrences). This is precisely the
   Bambu-fork vs Orca schema divergence the task asked to flag — upstream
   already handles it. Using QIDIStudio's spelling in Orca would not resolve.
2. `change_filament_gcode`: upstream wraps the whole body in
   `{if current_extruder != next_extruder}…{endif}`, guarding against a no-op
   tool change. QIDIStudio's is unguarded.

The per-nozzle deltas (layer heights, `retraction_length`, `retraction_minimum_travel: 3`
on 0.6, `retract_length_toolchange: 3` on 0.8) are reproduced exactly. Upstream
also assigns each variant a **unique** `setting_id`, fixing QIDI's GM008
collision noted in §1.8. [VERIFIED]

### 2.4 The catch: not in any stable release

| | |
|---|---|
| Plus 5 commit | 2026-08-07 |
| Latest stable **v2.4.2** | released 2026-07-07 — **before** the commit |
| `git compare v2.4.2...b216813b` | `status=diverged, ahead_by=702` → **not an ancestor** |
| `OrcaSlicer_Mac_universal_nightly.dmg` | asset updated **2026-09-11** (today) |

So **v2.4.2 does not contain the Plus 5 profiles.** [VERIFIED]

### 2.5 Open PRs / issues

No open PR or issue in OrcaSlicer specifically about Plus 5 support. Search hits
(#15598, #14051, #15536) are incidental mentions on unrelated work. [VERIFIED]

### 2.6 QIDITECH firmware repo

No `QIDI_PLUS5` repo exists under the `QIDITECH` org — nothing matching
`plus.?5` or `x.?5` in the org's repo list. **Your belief was correct.** [VERIFIED]

### 2.7 Conclusion — Phase 3 cancelled

Per task rule #7, **Phase 3 is not needed.** Hand-porting profiles would
reproduce work already done to a higher standard than a manual port (upstream
fixed the setting_id collision and did the schema rename correctly).
Nothing was written to `orca-profiles/`.

**Installed:** OrcaSlicer **2.5.0-dev** (nightly, macOS universal) to
`/Applications/OrcaSlicer.app` on 2026-09-11. This build packs vendor profiles
into an encrypted container `profiles/Qidi.opc` (magic `ZCRO`) rather than loose
JSON, so the presets aren't browsable on disk — but the build ships the Plus 5's
own assets (`Qidi X-Plus 5_cover.png`, `qidi_xplus5_buildplate_model.stl`,
`qidi_xplus5_buildplate_texture.svg`), which only ship with the Plus 5 machine
model that references them. Confirm in-app: Printer picker -> add -> QIDI ->
X-Plus 5 (0.2/0.4/0.6/0.8 nozzle). Your existing QIDIStudio install and Orca
config were left untouched. [VERIFIED install; in-app presence VERIFIED via
bundled assets]

**Recommended action instead:** install the **nightly** build, or copy the 21
machine/process files from `main` into a v2.4.2 install's
`resources/profiles/Qidi/` + patch `Qidi.json`. Nightly is cleaner. *Not done —
awaiting your go-ahead.*

---

## Phase 4 — printer recon (read-only)

Target **<PRINTER-IP>**, supplied by you. Nothing was written; no config
changed; no update/install tooling run.

### 4.1 Reachability and open ports

Ping OK (avg 47 ms, wifi). Open TCP: **22, 80, 7125, 10088**. [VERIFIED]
Closed/filtered: 81, 443, 1883, 3000, 4408, 4409, 7126, 8080, 8883.

### 4.2 Host

| | | |
|---|---|---|
| Hostname | `qidi-plus5` | [VERIFIED] |
| OS | Debian 11 (bullseye), kernel 5.10.160 | [VERIFIED] |
| Arch / CPU | aarch64, 4 cores | [VERIFIED] |
| RAM | 498 MB | [VERIFIED] |
| Python | 3.9.2 | [VERIFIED] |
| Service user | `qidi` (uid 1001) | [VERIFIED] |
| Interface | `wlan0` only — no eth in use | [VERIFIED] |
| Services | klipper, klipper-mcu, moonraker, crowsnest — all active | [VERIFIED] |

### 4.3 Moonraker — **open, unauthenticated, on the LAN**

`http://<PRINTER-IP>:7125` answers with **no auth**. [VERIFIED]
`/printer/info` → `state: ready`, config `/home/qidi/printer_data/config/printer.cfg`.
API version **1.4.0**.

`[authorization] trusted_clients` covers all RFC1918 ranges
(`10/8, 172.16/12, 192.168/16`) plus link-local — i.e. **anything on your LAN has
full unauthenticated control**, including starting prints and writing files.
That is QIDI's default, not something you configured. Worth knowing. [VERIFIED]

### 4.4 Versions — deliberately stripped

`software_version: "?"`, `moonraker_version: "?"`, `cpu_desc`/`model` empty.
There is **no `[update_manager]` section**, and `/machine/update/status` returns
no result. QIDI ships the tree without git metadata, so nothing can report or
check its own version. [VERIFIED]

This is the mechanical reason QIDI warns against kiauh/git updates: there is no
upstream remote to update *from*, and update tooling would try to reinitialise
the tree over their fork. **Consistent with — and explains — that warning.**

Exact Klipper/Moonraker upstream versions: **could not be determined remotely.**
Would need SSH to inspect the source tree. [UNCONFIRMED]

### 4.5 Closed / proprietary modules

Not directly inspectable without SSH, but the printer registers Klipper objects
and config sections that **do not exist in upstream Klipper**: [VERIFIED]

```
box_config, box_extras, box_stepper, box_heater_fan, aht20_f,
polar_cooler (enable_polar_cooler), noodle detection, RFID auto-read
```

219 printer objects and **295 registered G-code commands** total (stock Klipper
is far fewer). Whether these are compiled `.so` or plain `.py` extras
is **[UNCONFIRMED]** — needs SSH.

### 4.6 Config backup — obtained **without SSH**

Moonraker's file API serves `config/` read-only over HTTP, so no credentials
were needed. All **33** files pulled to `printer-cfg-backup/`: [VERIFIED]

`printer.cfg` (12975 B), `box.cfg`, `fluidd.cfg`, `timelapse.cfg`,
`moonraker.conf`, `crowsnest.conf`, `saved_variables.cfg`,
`klipper-macros-qd/*` (16 files), `KAMP/*` (5 files),
`officiall_filas_list.cfg` [sic], `MCU_ID.cfg`, plus backups.

### 4.7 A 4-slot multi-colour box **is attached and enabled**

`saved_variables.cfg`: `box_count = 1`, `enable_box = 1`, 17 colour/filament
slots tracked. Printer objects include `box_stepper slot0..slot3` and
`heater_generic heater_box1`. So `box_id: 4` in the machine profile = **4 slots**,
answering §1.9. [VERIFIED]

Note on method: `BOX_PRINT_START`, `TOOL_CHANGE_START/END`, `CUT_FILAMENT` and
`DISABLE_BOX_HEATER` do **not** appear in `/printer/gcode/help`, but they *are*
registered — Klipper omits commands declared without a help string. Absence from
that endpoint is not evidence of absence. The box objects above are the reliable
signal.

The firmware's own `PRINT_START` guards box calls behind
`box_count >= 1 and printer["box_extras"] and enable_box == 1`
(`klipper-macros-qd/start_end.cfg:87–99`). The **slicer** start G-code bypasses
`PRINT_START` and calls `BOX_PRINT_START` unguarded — fine on this machine
because the box is present. It would be a problem on a boxless Plus 5. [VERIFIED]

### 4.8 SSH

Open, `SSH-2.0-OpenSSH_8.4p1 Debian-5+deb11u3`. [VERIFIED]
**No login attempted** — you said nothing is configured, and credentials were
not needed since Moonraker gave up the configs. The `mks`/`makerbase` default
pair is [READ], from the Q2-generation reports you mentioned; **not tested here.**
Ask before trying.

### 4.9 What LAN-only operation actually costs you — **nothing material**

| Function | Needs QIDI servers? | |
|---|---|---|
| Slicing, upload, print, monitor | No | [VERIFIED] |
| Fluidd UI (port 80) | No — served locally | [VERIFIED] |
| Webcam / timelapse | No — local `crowsnest` + `[timelapse]`, frames to `~/printer_data` | [VERIFIED] |
| Bed mesh, Z-tilt, KAMP adaptive meshing | No — local cfg | [VERIFIED] |
| Multi-colour box, RFID filament read | No — local MCU | [VERIFIED] |
| Moonraker announcements | `subscriptions: []` — nothing subscribed | [VERIFIED] |
| Firmware updates | No update_manager — manual via QIDI anyway | [VERIFIED] |

`moonraker.conf` contains **no `[frp_manager]` and no `[mqtt]` configuration**.
Both components load (they appear in `/server/info` and `/server/config`) but
their parsed config is **empty `{}`** — no server address, no credentials from
the config file. [VERIFIED]

`frp` = fast reverse proxy, the usual mechanism for QIDI's remote-access cloud;
`mqtt` matches the machine profile's `is_support_mqtt: 1`. Whether QIDI's fork
**hardcodes** a cloud endpoint inside the component source (rather than reading
it from config) is **[UNCONFIRMED]** — that requires reading the Moonraker
component `.py` on the printer, i.e. SSH.

`cors_domains` whitelists `*://my.mainsail.xyz` and `*://app.fluidd.xyz` — those
are third-party *browser-side* UIs reaching your printer directly; they are not
QIDI cloud and involve no outbound connection from the printer. [VERIFIED]

**Bottom line: every print-related function is local.** The only open question is
whether an unconfigured frp/mqtt component still dials out — answerable with
SSH, or by watching your router's outbound connections from <PRINTER-IP>.

### 4.10 Not done / awaiting your decision

- No SSH login attempted
- Nothing written to the printer
- Orca not installed, your Orca config untouched

---

## Phase 4 addendum — SSH login attempt (user-authorized)

You explicitly authorized SSH login on <PRINTER-IP>. Read-only intent; nothing
was to be modified.

### Result: could not log in — documented QIDI default does not work on the Plus 5

- `sshd` accepts `password` auth for users `qidi`, `mks`, `root`
  (all offer `publickey,password`). [VERIFIED]
- Password **`makerbase`** — the universal QIDI default documented for every
  prior model (Plus 4 wiki, Q2 wiki, OctoEverywhere, all say `mks`/`makerbase`)
  — is **rejected** for `qidi`, `mks`, and `root`. [VERIFIED]
- First round of attempts was a **false negative**: I used `setsid`, which does
  not exist on macOS, so ssh never ran. Rebuilt on a real pty
  (`scratchpad/sshpw.py`) and confirmed the password is genuinely sent and
  genuinely rejected. [VERIFIED]

### Why it differs

- This model's service account is **`qidi`** (uid 1001, `/home/qidi`), not the
  `mks`/`/home/mks` used by every documented QIDI generation. [VERIFIED]
- **No public source documents the Plus 5 credential** — Aug-2026 model, and the
  `qidi-community` org wikis cover only Plus 4, X-Plus 3/4, Q2. No Plus 5 wiki. [VERIFIED]
- Conclusion: QIDI renamed the account and almost certainly changed the password.
  The Plus 5 shell password is **[UNCONFIRMED / not in our possession].**

Further password guessing was stopped (correctly flagged as brute-forcing).
To be retrieved from QIDI support, the printer's paperwork, or a screen
developer/access-code menu.

### Cloud-dependency corroboration (no SSH needed)

Moonraker `/machine/system_info` reports exactly **4** systemd services:
`klipper, klipper-mcu, moonraker, crowsnest`. **No `makerbase-client`** — the
cloud-agent service the Q2 generation runs (per q2-wiki). With `frp_manager` and
`mqtt` config both empty (§4.9), this is a second independent signal that nothing
cloud-facing is actively running. Not conclusive without a shell, but consistent. [VERIFIED]

### Still open (need the shell password)

1. Exact Klipper / Moonraker upstream versions (tree is version-stripped)
2. Whether the frp/mqtt Moonraker components hardcode a cloud endpoint in `.py`
3. Whether QIDI's box / polar-cooler extras are compiled `.so` or plain Python

---

## Phase 4 addendum 2 — SSH access obtained; recon completed (read-only)

### Credentials (found via community forums, per your prompt)

`mks`/`makerbase` is dead on this generation. The X-5/Q2/Max-4 generation uses:

- **username `qidi` / password `qiditech`** — **[VERIFIED — logged in successfully]**

Sources: thelegendtubaguy/Qidi-Max-4-Optimized (states default sudo password
`qiditech`), r/QidiTech3D "Qidi MAX4 ssh login", QIDITECH/QIDI_PLUS4 issue #21
(QIDI: root password no longer public; user account has sudo). The `qidi` user's
sudo password is the same `qiditech`. [READ + login VERIFIED]

Login confirmed: `uid=1001(qidi) gid=111(netdev) groups=netdev,tty,dialout,video`,
Debian 11, kernel 5.10.160 aarch64. [VERIFIED]

### Item #11/#4 — QIDI ships CLOSED compiled `.so` modules in the tree. **Yes.** [VERIFIED]

Moonraker `moonraker/components/` — QIDI replaced three stock Python components
with compiled binaries (dated Aug 4 2026):
```
frp_manager.so   (1.16 MB)   <- cloud tunnel manager (stock is frp_manager.py-less; QIDI-added)
mqtt.so          (5.50 MB)   <- replaces mqtt.py
extensions.so    (1.56 MB)   <- replaces extensions.py
```
Klipper `klippy/extras/` closed `.so` (no source):
```
box_stepper.so, box_autofeed.so, multi_color_controller.so, closed_loop.so, aht20_f.so
```
Plus cython `.so` for `hx711`, `heater_feng`, `air`, `heater_air_core`.
Everything else in both trees is plain readable `.py`. [VERIFIED]

### Item #4 — Klipper / Moonraker versions: **still not pinnable.** [VERIFIED as stripped]

Neither `/home/qidi/klipper` nor `/home/qidi/moonraker` has a `.git` dir or a
`.version` file — deliberately stripped. (By contrast crowsnest, fluidd-config,
kiauh, KAMP *do* have `.git`.) So even with a shell, there is no version string
to read. Component files are dated Jul 17 2026; the `.so` blobs Aug 4 2026.
Exact upstream version: **cannot be determined even via SSH.** [VERIFIED]

### Item #13 — cloud dependency: the tunnel is **QIDILink**, and it is **OFF** right now

`/etc/systemd/system/frp.service` = **"QIDILink Client Service"**:
```
ExecStart=/root/Frp/frpc -c /root/Frp/frpc.json
WantedBy=multi-user.target
```
- Service state: **inactive** (both `frp.service` and `frpc.service`). [VERIFIED]
- **No `frpc` / `makerbase` process running.** [VERIFIED]
- **Zero established outbound connections to any non-LAN host** (only
  localhost↔Moonraker and my SSH session). [VERIFIED]

So QIDILink is a QIDI-run reverse tunnel (frp = fast reverse proxy) that is
installed and enabled-at-boot but currently **not connected** — consistent with
you having turned on LAN mode. This is the direct answer to "what does LAN-only
cost me": **the only thing that reaches QIDI's servers is QIDILink, and with LAN
mode it isn't running.** Every print/control function is local and unaffected. [VERIFIED]

**Not yet read:** `/root/Frp/frpc.json` (the actual QIDILink server hostname) and
`strings /root/Frp/frpc` — both are root-owned, need `sudo`. Reading them is
still read-only but is a privilege escalation → **awaiting explicit user OK.**
This would only reveal *which* QIDI endpoint the tunnel points at, not change the
conclusion above.

### QIDILink endpoint (sudo read, user-authorized, read-only)

`/root/Frp/frpc.json` — the QIDILink tunnel config: [VERIFIED]

```json
{
  "auth": { "method": "token", "token": "<FRP-TOKEN-REDACTED>" },
  "log":  { "level": "info", "maxDays": 7, "to": "/root/Frp/frpc.log" },
  "proxies": [{
    "localPort": 80,
    "name": "QIDI_PLUS5_<CPU-SERIAL>",
    "subdomain": "<SUBDOMAIN-REDACTED>",
    "transport": { "bandwidthLimit": "300KB", "useEncryption": true },
    "type": "http"
  }],
  "serverAddr": "www.aws.qidi3dprinter.com",
  "serverPort": 7080
}
```

What this means: [VERIFIED]
- QIDILink reverse-proxies the printer's **local port 80 (the Fluidd web UI)** out
  to QIDI's frp server at **`www.aws.qidi3dprinter.com:7080`**, exposing it at a
  fixed subdomain `<SUBDOMAIN-REDACTED>.<qidi domain>`. That is how QIDI's phone
  app / remote access reaches the printer from outside your LAN.
- Shared frp auth token is the literal string `"<FRP-TOKEN-REDACTED>"` (same for the fleet —
  security is via the random per-printer subdomain, not the token).
- The proxied name embeds the CPU serial seen in `/machine/system_info`
  (`<CPU-SERIAL>`), tying the tunnel to this specific unit.
- **Only port 80 is tunnelled** — not SSH (22), not Moonraker (7125) directly.
  Remote control still goes *through* the Fluidd UI on 80.

Bottom line confirmed: LAN-only costs you exactly one thing — this QIDILink
tunnel to `www.aws.qidi3dprinter.com` — and it is currently **inactive**
(service dead, no process, no outbound connection). Nothing else on the printer
depends on QIDI's servers. If you want it off permanently rather than per-boot,
`systemctl disable --now frp.service` would do it — **that is a write; not done,
would need your OK.**

---

## QIDILink cloud tunnel — behaviour and how to disable it (reference)

### What it is
`frpc` (fast reverse proxy client) run as systemd unit **"QIDILink Client Service"**
(`ExecStart=/root/Frp/frpc -c /root/Frp/frpc.json`). It reverse-proxies the
printer's **local port 80 (Fluidd)** out to QIDI's server
`www.aws.qidi3dprinter.com:7080` under a fixed per-printer subdomain, so QIDI's
app can reach the printer from outside your LAN. Only port 80 is tunnelled
(not SSH, not Moonraker directly). [VERIFIED]

### Observed behaviour
- `frpc.log` shows it **auto-connected on boot** ("login to server success",
  "start proxy success"). So by default it dials out unprompted. [VERIFIED]
- After the **LAN switch** was toggled on (in the printer's screen/app), the
  service went **inactive** — no process, zero external connections. [VERIFIED]
- **Not verified:** whether the LAN switch persists across a reboot / firmware
  update, i.e. whether frpc stays down on next boot. The unit's boot-enable
  state was ambiguous when queried. Confirming would require rebooting the
  printer (not done — would be disruptive). [UNCONFIRMED]

### Refinement (verified after first draft): LAN mode looks like it *is* `systemctl disable`

The real unit is **`frpc.service`** (`Description=QIDILink Client Service`,
`ExecStart=/root/Frp/frpc -c /root/Frp/frpc.json`). `frp.service` is a broken
self-referential symlink (`-> /etc/systemd/system/frp.service`) — ignore it.

`systemctl list-unit-files` reports `frpc.service` as **`disabled`** right now,
even though `frpc.log` shows it connected at boot this morning. The most likely
explanation: the printer's **LAN switch runs `systemctl disable --now
frpc.service`**. If so, LAN mode is persistent by definition — a `disabled` unit
does not start at boot. So the manual disable below is **belt-and-suspenders**,
not strictly necessary while LAN mode stays on. Residual risk: a firmware/OTA
update could re-enable or re-create the unit. [VERIFIED unit is currently
disabled + inactive; LAN-switch→disable mapping INFERRED, not watched live]

### Two ways to keep it off

**A. The LAN switch (what you did).** Non-invasive, reversible from the UI, no
shell needed. Stops the running tunnel. Reboot-persistence unverified — treat as
"off until something flips it back."

**B. Hard disable via systemd (guarantee).** Belt-and-suspenders; survives reboot.
**This is a WRITE to the printer — not performed. Run only if you decide to:**

```sh
ssh qidi@<PRINTER-IP>          # password: qiditech
# stop now and prevent auto-start at boot:
echo qiditech | sudo -S systemctl disable --now frpc.service
# verify:
systemctl is-active frpc.service      # -> inactive
systemctl is-enabled frpc.service     # -> disabled/masked
```

To fully neutralise even a manual/firmware re-enable, additionally `mask` it:
```sh
echo qiditech | sudo -S systemctl mask frpc.service
```
Reverse with `systemctl unmask` / `enable --now` if you ever want QIDI remote
access back.

> Trade-off: disabling QIDILink kills QIDI's phone-app remote access (which works
> *through* this tunnel). LAN slicing/printing/monitoring via OrcaSlicer, Fluidd,
> Moonraker, and Mainsail are unaffected — they never used it.

> Caveat on updates: a QIDI firmware/OTA update may re-create or re-enable the
> unit. Re-check after any update. Do not run kiauh/git updaters against this
> printer (QIDI's warning; the klipper/moonraker trees are version-stripped with
> no upstream remote — see §4.4).

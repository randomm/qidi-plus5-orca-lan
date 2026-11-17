# Box and printer internals: commands, variables, and traps

A working reference to what the firmware actually exposes - gathered from
[jcazares76's machine notes](https://github.com/jcazares76/Qidi-Plus-5-Mods/blob/main/docs/machine-notes.md)
(verified on his unit; the best single source for this), plus this wiki's own
poking. Useful if you script against Moonraker, write macros, or just want to
know what `?` means before panicking.

## The save_variables schema (where slot data lives)

Slot data is in Klipper's `save_variables` (`saved_variables.cfg`). **Slots are
0-based here** - `slot0` is the box's slot 1; the box label and slicers use
1-based. Index **16 is the external spool**, and `slot16` also means "nothing
loaded".

| Variable | Meaning | Example |
|---|---|---|
| `filament_slot<N>` | QIDI filament ID (string) | `'QFA00'` = PLA Basic |
| `color_slot<N>` | colour, one-item hex list | `['FAFAFA']` |
| `slot<N>` | state: 0 empty, 1 spool present/parked, 2 loaded in toolhead, 3 in tube post-eject | `1` |
| `value_t<T>` | tool -> slot mapping used when printing | `'slot2'` |
| `enable_box` | 1 = print from box, 0 = external spool | `1` |
| `last_load_slot`, `last_load_filament_id` | last loaded slot + its ID | `'slot16'` |

Writing these with `SAVE_VARIABLE` updates the box **live** - `box_extras`
reflects the new name/vendor/temps/colour immediately, no refresh command.
(Runout remapping relies on `value_t<T>`; stamping it in start G-code has the
trade-offs on [the colour page](../qidi-box-colour-mapping/README.md).)

Filament IDs match QIDI Studio's profiles: QFA = PLA, QFB = ABS/ASA, QFC = PC,
QFG = PETG, QFL = third-party brands, QFN = nylon, QFP = PPS, QFS = support,
QFT = PET, QFU = TPU; `xx90`+ = Generic.

## Load / unload / eject

```
UNLOAD_FILAMENT_CONTROL SLOT=<i>   ; pull filament back to the tube (ready to reload)
EJECT_FILAMENT_CONTROL SLOT=<i>    ; pull filament fully out of the feeder
LOAD_FILAMENT_CONTROL SLOT=<i>     ; feed from slot to toolhead
```

`SLOT` is the **0-based** box slot index. Measured on one unit: load takes
~100 s and heats the nozzle to **280 C even for PLA** (inferred: hottest
filament in the box); unload ~75 s at the slot's own `max_temp`.

> **`SLOT` is not validated.** `EJECT_FILAMENT_CONTROL SLOT=99` shut Klipper
> down with `Unknown config object 'box_stepper slot99'` - a plain `RESTART`
> wasn't enough; `FIRMWARE_RESTART` recovered it in ~20 s. Only ever send real
> box indexes, never 16.

## Dryer commands

```
BOX_START_DRYING BOX=1 TEMP=45 TIME=2     ; TIME is hours; end_time reads minutes left
BOX_STOP_DRYING BOX=1
SET_HEATER_TEMPERATURE HEATER="heater_box1" TARGET=40   ; direct heater set, works over the console
```

`SET_HEATER_TEMPERATURE` is the console escape hatch when Fluidd refuses
([why](../qidi-box-drying/README.md)) - note that `DISABLE_BOX_HEATER` does
**not** clear a target set this way. There's also `EX_START_DRYING` /
`EX_STOP_DRYING`: in-printer spool drying with presets in `drying.conf`
(PLA 70 C bed / 55 C chamber / 720 min; PETG and ABS 90/60/720).

## Useful Moonraker endpoints (no SSH needed)

- `/printer/objects/query?...` - everything below, live
- `/printer/gcode/script?script=...` - run commands
- `/server/gcode_store?count=N` - read a command's reply. **QIDI commands
  often return OK while printing an error to the console** - always read this
  back instead of trusting the return code.
- `/server/files/upload` (`root=config`) - config upload; `/printer/info` for
  readiness after `RESTART`

Moonraker trusts the whole LAN (`[authorization]` private ranges, no API key).
Handy, and worth a thought on shared networks.

## Traps that cost someone a recovery

- **`M106 P3 S>0` also zeroes the chamber heater target.** QIDI's `M106`
  macro (`klipper-macros-qd/fans.cfg`): running the chamber exhaust fan kills
  chamber heating. QIDI's own start G-code only enables that fan when the
  chamber target is 0 - now you know why.
- **`#` starts a comment in Klipper config, even inside macro code**, and is
  also stripped from G-code parameters - pass hex colours without `#`.
- **`RESTART` vs `FIRMWARE_RESTART`**: host restart is the normal
  config-reload; once a board is shut down ("Can not update MCU 'mcu' config
  as it is shutdown"), only `FIRMWARE_RESTART` recovers it.
- Console `!!` errors pop up on the touchscreen (`QDC_100_005_000_001`
  info box). Harmless, but startling.
- QIDI's config files are UTF-8 with Chinese comments; download/upload them
  as **bytes** (curl -o / -F), or PowerShell 5's ISO-8859-1 default will
  garble every comment on write-back.
- Fan/object map for the curious: part fan `M106 P0` (there's no `[fan]`
  object), aux `M106 P2`, chamber exhaust `M106 P3`, polar cooler `M106 P4`;
  `SET_FAN_SPEED FAN=<name> SPEED=0..1` works for all `fan_generic`s.

## Testing rules (from someone who crashed his learning this)

1. Only test with the printer idle (`print_stats.state` = `standby`) - and
   check right before each command, not once per session.
2. Probe unknown commands without arguments first - they usually name the
   missing parameter.
3. Don't probe motor/filament commands with out-of-range values (see the
   eject crash above).
4. Heaters: low temps, short times, verify target 0 and power 0 after.
5. Back up config as raw bytes before uploading a change; verify the upload
   byte for byte.

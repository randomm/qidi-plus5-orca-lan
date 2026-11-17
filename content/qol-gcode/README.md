# Quality-of-life G-code and macro changes

Small slicer- and config-side edits that make the machine nicer to live with.
Each one is independent - take what you want. Two are verified on my unit
(noted), the rest are community-documented with sources.

## Skip the end-of-print unload (verified)

The stock Orca **"Qidi X-Plus 5"** machine end G-code calls
`UNLOAD_FILAMENT T=[current_extruder]` before `PRINT_END` - so after every
print the printer pulls the filament all the way back out of the toolhead.
Annoying if you print the same material back to back. The printer-side
`print_end` macro doesn't require it (it handles offsets, heaters, fans,
steppers - not filament), so the fix is one line in the slicer:

Printer Settings -> Machine G-code -> **Machine end G-code**, comment out:

```gcode
; UNLOAD_FILAMENT T=[current_extruder]
```

The small `G1 E-3 F1800` retract before it still runs; park and heater-off are
unaffected. Safe for the next print: every start runs a purge
(`EXTRUSION_AND_FLUSH`) anyway, and a different Box slot triggers the
cut-and-load flow itself. Unload on demand via the touchscreen or
`UNLOAD_FILAMENT` in the console (it accepts `LENGTH=`). QIDI Studio's profile
carries the same line - edit it there too if you print from Studio.

## Timelapse at 1080p instead of 640x480

The camera is 1080p native but timelapses save at 640x480 by default. In
Fluidd: Configuration -> `crowsnest.conf`:

```
resolution: 1920x1080
max_fps: 10
```

Save & restart. If Full HD lags the UI, drop to 1280x720. Don't change the
head park position - QIDI warns it causes timelapse errors. (The Chinese
wiki uses `webcam.txt` for this; check which file exists on your unit.)
Source: [printer-hub.ru known issues](https://printer-hub.ru/en/posts/qidi-plus5-known-issues).

## Cut the start-of-print purge from 200+ mm to ~30 mm

The stock `CLEAR_NOZZLE` block purges 200+ mm before every print. Replace it
with:

```gcode
;===== CLEAR_NOZZLE =====
M109 S[nozzle_temperature_initial_layer]
G92 E0
M83
G1 E5 F80
G1 E25 F300
M400
M106 S255
G1 E-3 F1000
M104 S140
```

Fine for same-filament prints; after a material change (PETG -> PLA) even
200 mm may not be enough - keep the stock macro for those, and load the next
filament at the *previous* filament's temperature for cleaner transitions.
Source: [printer-hub.ru](https://printer-hub.ru/en/posts/qidi-plus5-known-issues).

## UPS-safe sequential heating

All heaters at once draws ~1445 W (bed ~500, chamber ~550, nozzle ~150, Box
dryer ~245 - measured figures from a community unit). If you're on a UPS or a
shared circuit, heat sequentially - bed (wait) -> chamber (wait) -> nozzle -
and the start peak stays under ~1000 W. The
[jcazares76 repo](https://github.com/jcazares76/Qidi-Plus-5-Mods) ships an
Orca profile with exactly this start G-code.

## Heat the Box during Orca prints (AUTO_BOX_TEMP)

QIDI Studio writes `BOX_TEMP_SET VT<n>=...` into every print; **OrcaSlicer
never does**, so the Box never heats during an Orca print - filament sits at
room humidity while you print ABS. The same
[jcazares76 repo](https://github.com/jcazares76/Qidi-Plus-5-Mods) fixes it
with an `AUTO_BOX_TEMP` macro in its `box_slots.cfg`: one line in your start
G-code (after the nozzle reaches temp) heats the Box to the lowest
`box_max_temp` of the spools physically inside it (a no-limit spool like PLA
counts as 40 C by default), and a watcher turns the heater off about a minute
after the print ends. Options: `SLOTS=1,2`, `MAX=40`, `OFF=1`.

## Flip the Box on/off for external-spool prints

The known Orca gap ([#17227](https://github.com/OrcaSlicer/OrcaSlicer/issues/17227)):
Orca never writes `enable_box`, so an external-spool print right after a Box
print can fail with "filament missing 1D". Console workaround:

```gcode
SAVE_VARIABLE VARIABLE=enable_box VALUE=0    ; print from the external spool
SAVE_VARIABLE VARIABLE=enable_box VALUE=1    ; print from the box
```

## Cooler stepper drivers (optional)

`driver_SLOPE_CONTROL: 2` on `[tmc2240 stepper_x]` / `[stepper_y]` (stock
ships it commented out). Klipper's default `0` is the hottest current-rise
slope; `2` measurably cools the driver chips for a small high-speed torque
cost ([Klipper PR #6771](https://github.com/Klipper3d/klipper/pull/6771)), `3`
coolest. Worth it if your machine lives somewhere warm.

---

*The two "verified" items were checked against firmware v01.01.02.01's shipped
macros and the Orca profile; the rest are community-sourced with links. Every
`printer.cfg` edit here survives only until the next firmware update replaces
the file - re-apply, and keep the `printer-<date>.cfg` backups QIDI leaves
behind.*

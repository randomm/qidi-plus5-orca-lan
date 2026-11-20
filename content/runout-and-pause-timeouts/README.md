# Runout, pause timeouts, and the real spool-refill window

The `[idle_timeout]` section in `printer.cfg` ships as `timeout: 43200` - 12
hours - and it is natural to assume that's the window you have to swap a spool
when filament runs out mid-print. It isn't. Traced through the shipped macros
(QIDI rewrites them on firmware updates - re-check after any update; verified
against firmware v01.01.02.01's shipped config and Klipper's `idle_timeout.py`):

## What actually happens on runout

1. The runout sensor (`[filament_switch_sensor]`, `pause_on_runout: True`)
   fires and Klipper runs QIDI's PAUSE macro.
2. The PAUSE macro (`klipper-macros-qd/pause_resume_cancel.cfg`):
   - saves the current nozzle target,
   - runs `M104 S0` - **hotend off immediately** ("prevents filament
     degradation"; bed, chamber and Box dryer stay hot),
   - disables the extruder stepper,
   - runs `SET_IDLE_TIMEOUT TIMEOUT=259200` - a **runtime override to 72
     hours**, in RAM. The 12 h config value is simply not in charge here.
3. Depending on the Box state, either `AUTO_RELOAD_FILAMENT` runs (auto-swap
   to another slot with identical filament properties) or
   `SET_PRINT_SUB_STATUS box_filament_exhausted` leaves it waiting for you.
4. Refill + Retry on the screen (or `RESUME`) runs `RESUME_PRINT`: it
   re-heats to the saved temperature (`M109`), purges 250 mm, wipes, and
   restores position.

Mid-print auto-swap is unaffected by any of this - active printing never
trips idle_timeout (the toolhead has to fully drain first).

## After 72 hours paused

The idle gcode eventually kills the bed, chamber and Box heaters. The print
job itself survives (the Plus 5's idle gcode has `PRINT_END` commented out -
Plus 4 stock wasn't so lucky), **but** `_KM_IDLE_TIMEOUT`'s paused branch
zeroes the saved reheat temperature, so a generic resume skips reheating:
part, bed and chamber are all cold. For ABS/ASA, treat a print that sat past
the window as lost - re-run it rather than resume.

## Why you can't just change it

Editing `[idle_timeout]` in `printer.cfg` cannot change the paused window:
the macro's runtime override wins until Klipper restarts, and a restart
re-reads the config value (which then only governs non-paused idle - e.g. a
botched cancel holding a hot nozzle). The window is a firmware policy, not a
config setting.

`[box485] serial_timeout` / `extrude_timeout` (shipped `0.0`) are Box
serial-protocol timeouts, unrelated to runout refill - QIDI marks them
"don't change".

## Practical rules

- **72 hours, not 12**, is your refill window - and only with the bed and
  chamber still hot. PLA tolerance for a cold resume is your call; ABS/ASA,
  don't.
- The hotend is off within seconds of runout - you are not burning filament
  while you walk to the printer.
- Auto-refill (`AUTO_RELOAD_FILAMENT`) only picks a spool with **identical
  filament properties** - same brand/type/colour configured box-side. If you
  want it to work, configure the pairing candidate properly.
- If a print dies partway through a Box load/unload sequence, the state
  machine can leave flags behind (`retry_step`, `load_retry_num`) - see
  [the drying page](../qidi-box-drying/README.md)'s state-machine section for
  what healthy values look like.

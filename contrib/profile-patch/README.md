# Profile PR artifact — X-Plus 5 box tool→slot mapping

Submission-ready content for the OrcaSlicer profile PR (see
`../orcaslicer-xplus5-box-mapping.md` for the issue + PR text).

## Files

- `Qidi X-Plus 5 0.4 nozzle.json` — a copy of the upstream profile
  (`resources/profiles/Qidi/machine/Qidi X-Plus 5 0.4 nozzle.json` on `main`) with a
  **single-line** edit: four `SAVE_VARIABLE value_t{n} → slot{n}` lines prepended to
  `machine_start_gcode`, inside `;===== BOX_PREPAR =====`, immediately before
  `BOX_PRINT_START`. Verified: valid JSON, 1-line diff vs upstream, and the mapping lines
  decode to `SAVE_VARIABLE VARIABLE=value_t0 VALUE="'slot0'"` (correct Klipper literal).

## Also required in the PR (not a file here)

- Bump `version` in `resources/profiles/Qidi.json`: `02.04.00.12` → `02.04.00.13`.

## Applying (Phase D, on the fork)

1. Fork OrcaSlicer, branch off `main`.
2. Overwrite `resources/profiles/Qidi/machine/Qidi X-Plus 5 0.4 nozzle.json` with this file
   (or apply the same one-line insertion to the then-current upstream file, in case it moved).
3. Bump `Qidi.json` version.
4. `scripts/check_profile.sh` (whole tree) → all 5 checks green.
5. Open PR per the checklist in `../orcaslicer-xplus5-box-mapping.md`.

The 0.2/0.6/0.8 nozzle profiles inherit this `machine_start_gcode`, so this one edit covers
all four variants. Values are literal (no gcode placeholders), so `validate_slice` is safe.

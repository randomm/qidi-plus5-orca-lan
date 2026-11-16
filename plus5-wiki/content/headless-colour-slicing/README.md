# Slicing multi-colour jobs completely headless (CLI lane, no GUI)

**Use case note:** everything on this page is a *different lane* from the rest of
this wiki. The other pages assume you click around OrcaSlicer or QIDIStudio on a
desktop. This one is for driving the whole job from a script: `orca-slicer` CLI
(2.5.1) slicing on a Linux box over SSH, upload and start via Moonraker HTTP,
QIDI Box colour swaps, zero GUI anywhere. If you just want colour prints from the
slicer on your desktop, read
[the box-colour page](../qidi-box-colour-mapping/README.md) and stop here.

This is how I print the two-colour Voronoi lampshade panels (black ribs,
alternating red/pink cells) that a script generates as three STLs: frame +
red-cell slab + pink-cell slab. Verified end-to-end on hardware 2026-11-16
with OrcaSlicer 2.5.1, 0.4 nozzle, 0.2 mm layers, 3 of 4 box slots loaded
(slot 3 jammed, unused).

## The only path that works: one composed object via `--load-assemble-list`

Assigning one filament per STL object (`--load-filament-ids "1,2,3"`) does **not**
work for parts that sit in the same footprint at different heights: Orca's
G-code path-conflict check rejects them
(`gcode path conflicts found between ...`, CLI exit -101/-50) and there is no
clean z-gap escape — coplanar, 1 µm and 40 µm gaps all still flag, and pulling
the slabs apart further (≥50 µm) makes them vanish entirely
("No layers were detected", exit -100). There is a documented bypass flag,
`--no-check`, but the real fix is to slice the colour regions as **one object
with per-volume filament assignment**, which is exactly what the assemble list
does:

```json
{
  "plates": [{
    "plate_index": 1,
    "plate_name": "plate_1",
    "need_arrange": false,
    "objects": [
      { "path": "/abs/path/panel_frame.stl",   "count": 1, "filaments": [1], "assemble_index": [1] },
      { "path": "/abs/path/panel_cells_red.stl","count": 1, "filaments": [2], "assemble_index": [1] },
      { "path": "/abs/path/panel_cells_pink.stl","count": 1, "filaments": [3], "assemble_index": [1] }
    ]
  }]
}
```

Same `assemble_index` on every entry merges them into a single composed model,
so the conflict check has nothing between which to complain, and

```bash
orca-slicer --datadir /path/to/datadir \
  --load-settings "printer-job.json;process-job.json" \
  --load-filaments "fil-black.json;fil-red.json;fil-pink.json" \
  --load-assemble-list assemble-list.json \
  --no-check --slice 1 --outputdir out --export-3mf job.3mf
```

produces a correct 3-swap gcode (verified: tool changes land exactly at layer
boundaries, each colour extrudes in its own region).

CLI gotchas, all of them cost me a cycle:

- `--load-assemble-list` refuses positional model files **and** `--arrange`
  (even `--arrange 0`): `run found error, return -2`. Bake XY placement into
  the STLs; omit `pos_*` and the STL's own coordinates are used.
- `--load-filament-ids` cannot be combined with 3MF input.
- `flush_volumes_matrix` in the printer JSON must be exactly N×N of the number
  of *loaded* filaments or the slice aborts (`Flush volumes matrix do not match
  to the correct size!`). Cleanest: delete the key — the Qidi change-filament
  macro already purges onto the right-side waste pad, and with ≤3 swaps a wipe
  tower is not needed.
- OBJ `usemtl` face colours are **silently ignored** on the plain-positional
  path (everything prints in tool 0). The face-colour→filament mapping only
  exists on the assemble-list code path.

## The `auto_drop` trap (the quiet one)

With separate objects, Orca drops **each object independently to z=0**. My
0.2 mm membrane slabs live at z 0.401–0.599 by design — and Orca dragged them
down onto layer 1, printing the colour film into the first layer, silently,
with a clean `return_code: 0`. The composed-object assemble-list path fixes
this too (drop uses the union's min z), but check for it whenever objects
float: open the gcode and count extrusion per tool per layer block. The
per-layer `;Z:` comments delimit blocks; `T\d` lines switch tools — you can
audit colour placement without any GUI. Same trick tells you which *role*
Orca gave each region: the `;TYPE:` tags (`Bridge`, `Inner wall`,
`Internal solid infill`...). Watch out: most extrusion lines carry no `F`
word — feedrate is inherited from the last `G0/G1` that did, so track
last-seen-F per block or the numbers lie.

## `value_t` bindings are per-job, not per-printer

The box-colour page covers why Orca never writes `value_tN`. On the CLI lane
you control them from the machine-start-gcode text in the job JSON, which means
you can bind them *per job*: T-index n (i.e. the n-th `--load-filaments`
entry) loads from the slot named in `value_tn`. Bind them to your actual
physical spool layout — my layout is slot1=red, slot2=pink, slot4=black, so a
frame=fil1/red=fil2/pink=fil3 job needs

```
SAVE_VARIABLE VARIABLE=value_t0 VALUE="'slot3'"   ; frame  -> phys 4 (black)
SAVE_VARIABLE VARIABLE=value_t1 VALUE="'slot0'"   ; red    -> phys 1
SAVE_VARIABLE VARIABLE=value_t2 VALUE="'slot1'"   ; pink   -> phys 2
SAVE_VARIABLE VARIABLE=value_t3 VALUE="'slot0'"   ; unused, keep off jammed slot3
```

Always verify against the slice output rather than the intent:
`grep value_t plate_1.gcode` plus checking `UNLOAD_T*` order matches the
colour sequence you expect.

## Thin horizontal films: the settings that matter are the bridge ones

For a single-layer (0.2 mm) colour film spanning ~9.5 mm cell openings, I
chased the wrong setting first. Evidence, from byte-comparing slices:
`sparse_infill_density` 15% vs 100% produced **identical** membrane material —
the film is not sparse-infill classified. The `;TYPE:` tags showed it as
`Bridge`: dense paths, but at `bridge_speed=50` mm/s with `bridge_flow=1` a
PLA strand spanning 9.5 mm of nothing sags into a stringy web. Bridging wants
the opposite of what you'd guess: fast and thin. Current (pending print
verification) patch: `bridge_speed=120`, `bridge_flow=0.9`,
`internal_bridge_speed=100%`, monotonic internal solid infill,
`infill_wall_overlap=25%`, part fan 100%. The dense-but-sagged print and the
gcode proof of the classification are both in the photo record; the fixed
settings' print result is to be confirmed.

## Uploading and starting over Moonraker

`POST /printer/print/start?filename=...` is the natural move, but some HTTP
proxies between you and the printer choke on query-string POSTs while allowing
upload POSTs. The reliable one-shot: multipart upload with the start flag as a
**form field**:

```bash
curl -F "file=@job.gcode" -F "print=true" http://<printer-ip>/server/files/upload
# -> {"print_started": true, ...}
```

and poll `/printer/objects/query?print_stats` with **one object per query** —
comma-separated multi-object queries silently returned empty through my proxy.

## Never chain prints

A finished job reports `standby` and says **nothing** about whether last
print's part is still on the bed. I queued the follow-up slice straight after
the previous print finished; only the fact that I happened to be standing at
the printer saved the second print from starting on top of the first. If your
lane is unattended: after any completion, stop, announce, and have a human
confirm the plate is clear before the next start. Treat "approved print"
approval as single-use.

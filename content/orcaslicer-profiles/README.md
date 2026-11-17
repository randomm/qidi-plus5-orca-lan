# X-Plus 5 profiles in OrcaSlicer

Good news first: you don't need to build these by hand. OrcaSlicer already ships
X-Plus 5 profiles. They landed in `main` on 2026-08-07,
[PR #15163](https://github.com/OrcaSlicer/OrcaSlicer/pull/15163).

The catch: that merge is newer than the last stable release (v2.4.2, 2026-07-07).
So a stable build won't have them yet.

## Getting them

Use a nightly. Grab `OrcaSlicer_..._nightly` from the
[nightly-builds release](https://github.com/OrcaSlicer/OrcaSlicer/releases/tag/nightly-builds).
First run: add printer, QIDI, X-Plus 5, pick your nozzle (0.2 / 0.4 / 0.6 / 0.8,
0.4 is the default). That's it.

Once a stable ships after August 2026 it'll fold these in and this stops being a
nightly-only thing.

Staying on stable for now? You can copy the X-Plus 5 files from
`resources/profiles/Qidi/` on OrcaSlicer's `main` into your install and add the
model to `Qidi.json`. Doable, but fiddlier than just running the nightly.

## Are the shipped profiles any good?

I actually checked instead of assuming. Flattened OrcaSlicer's 0.4-nozzle machine
profile and compared it against QIDIStudio's own: 46 of 48 core machine
parameters match exactly. Bed 320 x 320, 300 tall. CoreXY. Speeds, accelerations,
jerk, retraction, the bed exclude area, all of it.

The two that differ are deliberate and correct, not sloppiness:

- OrcaSlicer uses `chamber_temperature` where QIDIStudio's Bambu-fork uses
  `chamber_temperatures`. Different naming between the forks. Using QIDIStudio's
  spelling in Orca would just silently do nothing, so this had to be translated.
- The filament-change G-code is wrapped in `{if current_extruder != next_extruder}`
  so a same-tool "change" becomes a no-op.

Per-nozzle deltas (layer-height range, retraction length, the 0.8's longer
tool-change retract) are all carried across. So: faithful port. No reason to
hand-roll your own, and I say that as someone who was about to.

## Connecting Orca to the printer over the LAN

No QIDI cloud needed for this. Orca talks straight to Moonraker.

In Orca, edit the printer and open the physical-printer / connection dialog.
Then:

- **Host Type:** `Moonraker (Klipper)`. It's at the bottom of the list. There's
  also an `Octo/Klipper` option that works via Moonraker's OctoPrint shim, but
  native Moonraker is the fuller one.
- **Hostname, IP or URL:** just the printer's IP, e.g. `192.168.8.xxx`. No port.
  The stock image runs an nginx on port 80 that proxies the Moonraker API, so the
  bare IP is enough.
- **Device UI:** `http://<printer-ip>` if you want the "open web UI" button to
  land on Fluidd. Optional.
- **API Key / Password:** leave it blank. On the stock image Moonraker trusts the
  whole LAN with no key (`login_required: false`, and the trusted_clients list
  covers the private ranges). Handy, and also worth a thought: anyone on your
  network can drive the printer. Fine at home, maybe less fine on a shared or
  office network.

Hit Test. Green? Good.

### macOS gotcha

If you're on macOS Sequoia or newer (I'm on 26.x): the **first** Test will fail,
and at the same moment macOS pops its "OrcaSlicer wants to find devices on your
local network" prompt. That's the actual reason it failed - the request never
left the machine. Grant it, hit Test again, connected. If you dismissed the
prompt, it's under System Settings, Privacy & Security, Local Network. Cost me a
confused minute before the penny dropped...

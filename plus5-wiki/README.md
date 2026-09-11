# QIDI Community X-Plus 5 Wiki

Notes and fixes for the QIDI X-Plus 5, in the same spirit as the community
[Plus 4](https://github.com/qidi-community/Plus4-Wiki) and
[Q2](https://github.com/qidi-community/q2-wiki) wikis.

The Plus 5 sits close to the Q2/Max-4 generation, so a lot of their pages carry
over. But a couple of things did change - the SSH account, the cloud tunnel - and
that's mostly what these pages are here to catch.

## Official QIDI wiki

[QIDI X-Plus 5 support page](https://wiki.qidi3d.com/en/Plus5)

---

## Getting in and set up

### [SSH access](./content/ssh-access/README.md)
`qidi` / `qiditech`. The old `mks` / `makerbase` doesn't work anymore.

### [X-Plus 5 profiles in OrcaSlicer](./content/orcaslicer-profiles/README.md)
Already shipped in OrcaSlicer. Use a nightly until the next stable, and yes, they
turned out to be a faithful port.

### [LAN mode and the QIDILink cloud tunnel](./content/lan-mode-and-qidilink/README.md)
What LAN mode actually does under the hood, and how to shut the cloud tunnel off
properly. The Plus 5 uses `frp` now, not the Plus 4's `udp_server`, so the disable
steps are different.

### [Getting the QIDI Box to print the right colour from OrcaSlicer](./content/qidi-box-colour-mapping/README.md)
Out of the box it loads the wrong slot every time. Why (a stale `value_t0`
variable Orca never writes), and the four-line start-gcode fix that makes colour
selection actually work.

---

*All of this started from poking at one X-Plus 5 read-only over SSH. Verified vs
inferred is called out where it matters. Corrections and additions very welcome -
that's the whole point of a community wiki...*

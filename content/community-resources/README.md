# Community resources for the Plus 5

Where the rest of the Plus 5 knowledge lives. The `qidi-community` GitHub org
(Plus 4 and Q2 wikis) has **no Plus 5 wiki yet** - this wiki is, as far as
anyone can tell, the only dedicated one. Checked November 2026.

## This wiki's close relatives

- [randomm/qidi-plus5-orca-lan](https://github.com/randomm/qidi-plus5-orca-lan) -
  the repo this wiki was born from: LAN-only Orca field notes plus the wiki
  itself. The [NOTES.md](../../lan-only/NOTES.md) full write-up lives here too.
- [qidi-community/Plus4-Wiki](https://github.com/qidi-community/Plus4-Wiki) -
  the Plus 4 wiki (282 stars). Config tweaks, SSH security, cartographer
  probe, cooling. Much carries over conceptually.
- [qidi-community/q2-wiki](https://github.com/qidi-community/q2-wiki) - the Q2
  wiki; the Q2 shares this generation (Box, SSH, QIDILink).
- [thelegendtubaguy/QidiMax4CommunityWiki](https://github.com/thelegendtubaguy/QidiMax4CommunityWiki) -
  the Max 4 wiki, very active: FAQ, error messages, fan assignments, SSH/OS
  internals, power usage, and the
  [heated bed screws](https://github.com/thelegendtubaguy/QidiMax4CommunityWiki/blob/main/docs/heated_bed_screws.md)
  page that the bed-tramming section leans on.

## Reference and fix repos

- [thelegendtubaguy/Qidi-Plus5-Defaults](https://github.com/thelegendtubaguy/Qidi-Plus5-Defaults) -
  **firmware tracker**: the full stock Klipper/Moonraker config dump, hourly
  checks of QIDI's firmware endpoint, and tags to diff package revisions.
  The reference for "what did this firmware change" - including the macros
  these pages quote.
- [Jonathall/qidi-plus5-fluidd-box-fix](https://github.com/Jonathall/qidi-plus5-fluidd-box-fix) -
  the patched Fluidd bundle ([details](../qidi-box-fluidd-panel/README.md)).
- [jcazares76/Qidi-Plus-5-Mods](https://github.com/jcazares76/Qidi-Plus-5-Mods) -
  box-slot macros, PC dashboard, and the
  [machine-notes](https://github.com/jcazares76/Qidi-Plus-5-Mods/blob/main/docs/machine-notes.md)
  internals doc the box-internals page draws from.
- OrcaSlicer's **printer agent** ([PR #16723](https://github.com/OrcaSlicer/OrcaSlicer/pull/16723),
  in 2.5.0+) - per-filament Box slot picking at print start.

## Tools

- [Gromatou/qidi-plus-5-better-ui](https://github.com/Gromatou/qidi-plus-5-better-ui) -
  HelixScreen UI + Klipper fixes, one-command installer.
- [tonngodoc/qidi-plus5-kamp](https://github.com/tonngodoc/qidi-plus5-kamp) -
  KAMP setup with a 1-click installer (docs in Vietnamese).
- [mihaits/qidi-smart-purge](https://github.com/mihaits/qidi-smart-purge) -
  skip the start-of-print purge when the same filament is already loaded.
- [borgels/mcp-server-qidi](https://github.com/borgels/mcp-server-qidi) - MCP
  server for the X-Plus5 over Moonraker (for the AI-assisted among us).

## Official

- [QIDI Plus 5 wiki](https://wiki.qidi3d.com/en/Plus5) - quick start,
  maintenance manual, replacement videos, firmware history.
  [Firmware release notes](https://wiki.qidi3d.com/en/Plus5/firmware-release-history)
  are worth reading before updating: they occasionally admit what changed.
- Support: Plus5support@qidi3d.com / Plus5support02@qidi3d.com

## Where the discussion happens

- [r/QidiTech3D](https://www.reddit.com/r/QidiTech3D/) - the active hub; most
  of the field reports on these pages started there.
- [printer-hub.ru's 40 Plus 5 known issues](https://printer-hub.ru/en/posts/qidi-plus5-known-issues) -
  the best indexed roundup of community-reported problems, with sources.

---

*This page is the one most likely to go stale - PRs and new repos welcome.
Verified links November 2026.*

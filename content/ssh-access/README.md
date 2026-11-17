# SSH access on the X-Plus 5

Soo... the `mks` / `makerbase` login everyone knows from the Plus 4 and the X-3
generation? Dead on the X-Plus 5. QIDI renamed the account on this generation and
it caught me out for a while.

It's now:

**Username:** `qidi`
**Password:** `qiditech`

Grab the printer's IP from the front-panel network tab, then:

```
ssh qidi@x.x.x.x
```

Password is `qiditech`. Config lives in `/home/qidi/printer_data/config` (note
`/home/qidi`, not `/home/mks`). SFTP works too: FileZilla with
`sftp://IP_ADDRESS`, same login.

## Root

The `qidi` account has sudo: `sudo -i`, same `qiditech` password. QIDI stopped
publishing the root password on recent models, so if you want one you set it
yourself:

```
sudo passwd root
```

## Notes

- Verified on my own X-Plus 5. Firmware image mid-2026: Debian 11, kernel
  5.10.160, aarch64.
- `qiditech` is the same password Max 4 owners reported, and the Max 4 runs the
  same image. New account, same idea. If yours doesn't take it, check the paper
  that came with the unit.
- Don't point kiauh or any git-based updater at this printer. QIDI ships the
  klipper and moonraker trees with the `.git` and version files stripped out:
  there's no upstream to pull from, so the tooling just fights the fork. QIDI
  warns about this too, and now you can see why.

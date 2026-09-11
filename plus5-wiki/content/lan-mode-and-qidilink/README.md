# LAN mode and the QIDILink cloud tunnel

QIDILink is the remote-access feature: it's what lets QIDI's phone app reach your
printer from outside your own network. Handy if you want it, a standing outbound
door to a vendor cloud if you don't.

On the Plus 4 it was a custom `udp_server` binary (see the
[Plus 4 guide](https://github.com/qidi-community/Plus4-Wiki/tree/main/content/disable%20QIDILink-client)).
The Plus 5 changed it. It's now plain [frp](https://github.com/fatedier/frp) (the
`frpc` client), so the Plus 4 steps don't line up anymore. Here's what's actually
running on the Plus 5.

## What it does

A systemd unit `frpc.service` ("QIDILink Client Service") runs
`/root/Frp/frpc -c /root/Frp/frpc.json`. That config reverse-proxies one thing:
your printer's local port 80, the Fluidd web UI, out to QIDI's server at
`www.aws.qidi3dprinter.com:7080`, published under a fixed per-printer subdomain.

Only port 80 goes through the tunnel. Not SSH, not Moonraker directly. Remote
control still happens through the Fluidd UI.

Is it encrypted? Yes, the frp transport is. Is that the whole story? Not quite:
the only thing gating access is the obscure subdomain. Anyone who has that URL can
reach your printer's UI while the tunnel is up. Same warning as the earlier
models, and `/root/Frp/frpc.log` shows it dials out on boot by default.

## Turning it off

### The LAN switch on the screen

Toggling LAN mode on the printer stops the tunnel. And here's the nice part: on my
unit `frpc.service` was left in the `disabled` state afterwards, so it won't come
back on the next boot either. So I'd say the screen toggle is very likely enough
on its own, and it's fully reversible from the UI. Check it:

```
systemctl is-enabled frpc.service   # disabled = won't start at boot
systemctl is-active  frpc.service   # inactive = not running now
```

One honest caveat: I saw the unit sitting `disabled`, I didn't watch the toggle
flip it. So I'm inferring the LAN switch runs `systemctl disable`. The end state
is what matters and that I did verify.

### Hard lock (optional)

Want it locked even against something turning it back on? Mask the unit over SSH:

```
sudo systemctl mask frpc.service
```

`mask` points the unit at `/dev/null`, so even `systemctl enable` or `start`
can't wake it until you `sudo systemctl unmask frpc.service`.

> `/etc/systemd/system/frp.service` is a broken symlink pointing at itself. It's
> not a real unit, ignore it. The one that matters is `frpc.service`.

## What you actually lose

QIDI's phone-app remote access, which rides on this tunnel. That's it. Local
slicing, printing and monitoring over your LAN - OrcaSlicer, Fluidd, Moonraker,
Mainsail - never touched QIDILink and keep working exactly as before.

## After a firmware update

Re-check `systemctl is-enabled frpc.service`. An update can re-create or re-enable
the unit, and you won't get told.

---

*Mechanism verified read-only over SSH on one X-Plus 5. The mask command is the
standard systemd move but I didn't run it on my unit, only read the state. Adapt
at your own risk, and correct this page if your printer disagrees.*

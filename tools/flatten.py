#!/usr/bin/env python3
"""Resolve QIDIStudio 'inherits' chains into flattened effective configs.

Usage: flatten.py <bundle-dir> <subdir> <preset-name> [...]
Only keys actually present in some file on the chain are emitted; nothing
is invented. Emits a "_chain" key recording the resolution order.
"""
import json, os, sys

def load(bundle, name):
    """Find a preset JSON by its 'name' anywhere in the bundle."""
    for sub in ("machine", "process", "filament"):
        d = os.path.join(bundle, sub)
        if not os.path.isdir(d):
            continue
        p = os.path.join(d, name + ".json")
        if os.path.exists(p):
            with open(p) as fh:
                return json.load(fh), p
        # fall back to scanning for a matching "name" field
        for fn in os.listdir(d):
            if not fn.endswith(".json"):
                continue
            fp = os.path.join(d, fn)
            try:
                with open(fp) as fh:
                    j = json.load(fh)
            except Exception:
                continue
            if j.get("name") == name:
                return j, fp
    raise SystemExit("NOT FOUND: %s" % name)

def flatten(bundle, name):
    chain, cur = [], name
    layers = []
    while cur:
        j, path = load(bundle, cur)
        chain.append({"name": cur, "file": os.path.relpath(path, bundle)})
        layers.append(j)
        cur = j.get("inherits") or None
    out = {}
    for j in reversed(layers):          # root first, child overrides
        for k, v in j.items():
            if k == "inherits":
                continue
            out[k] = v
    out["_chain"] = chain
    return out

if __name__ == "__main__":
    bundle, names = sys.argv[1], sys.argv[2:]
    for n in names:
        print(json.dumps(flatten(bundle, n), indent=2, ensure_ascii=False))

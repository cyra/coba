#!/usr/bin/env python3
"""Install the coba themes into an Octarine workspace.

Octarine keeps custom themes per workspace in <workspace>/.octarine/themes.json
and injects them as [data-theme="<id>"] blocks. This merges the coba entries in,
so themes made in the Theme Creator survive a re-run.

Octarine reads that file when it opens the workspace, so restart it afterwards.

  ./install-octarine.py [workspace]

With no argument the workspace is read from Octarine's own settings, which only
works when exactly one is registered.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.expanduser("~/Library/Application Support/Octarine/.store.dat")


def octarine_running():
    """Full process listing rather than pgrep, which does not report the calling
    process's own ancestors and so misses an app the script was launched from."""
    try:
        out = subprocess.run(["ps", "-Ao", "comm="], capture_output=True,
                             text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return False       # cannot tell, do not block on it
    return "Octarine.app/Contents/MacOS/" in out


def sole_workspace():
    try:
        with open(STORE) as f:
            ws = json.load(f)["store"]["workspace"]
        paths = [w["path"] for w in ws.values()]
    except (OSError, ValueError, KeyError, AttributeError, TypeError) as e:
        sys.exit(f"cannot read Octarine settings ({STORE}): {e}")
    if len(paths) != 1:
        sys.exit(f"{len(paths)} workspaces registered, name one: {paths}")
    return paths[0]


def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    if octarine_running() and "--force" not in sys.argv:
        sys.exit("quit Octarine first: it rewrites themes.json from memory and "
                 "would drop this merge. Pass --force to write anyway.")

    ws = args[0] if args else sole_workspace()
    target = os.path.join(ws, ".octarine", "themes.json")
    if not os.path.isdir(os.path.dirname(target)):
        sys.exit(f"not an Octarine workspace: {ws}")

    with open(os.path.join(HERE, "octarine", "themes.json")) as f:
        coba = json.load(f)

    existing = []
    if os.path.exists(target):
        # Once only. Re-running would otherwise back up the merged file over the
        # one copy of the user's original.
        bak = target + ".bak"
        if not os.path.exists(bak):
            shutil.copy(target, bak)
        try:
            with open(target) as f:
                existing = json.load(f)
            if not isinstance(existing, list):
                raise ValueError("expected a list of themes")
        except (ValueError, OSError) as e:
            sys.exit(f"{target} is not readable as a theme list ({e}); "
                     f"the original is at {bak}")

    # Match on name, not id: a theme pasted into the Theme Creator by hand has
    # a cuid2 the generator cannot know. Keep the id that is already there, the
    # active-theme setting points at it, and only refresh the colours.
    by_name = {t.get("name", "").lower(): t for t in existing if isinstance(t, dict)}
    merged, ours = list(existing), []
    for t in coba:
        old = by_name.get(t["name"].lower())
        if old:
            old.update({k: v for k, v in t.items() if k not in ("id", "created")})
            old["modified"] = t["modified"]
        else:
            merged.append(t)
        ours.append(t["name"])

    # Write via a temp file in the same directory: a crash or a full disk leaves
    # the old themes.json intact rather than a truncated one Octarine cannot parse.
    tmp = target + ".tmp"
    with open(tmp, "w") as f:
        json.dump(merged, f, indent=2)
        f.write("\n")
    os.replace(tmp, target)

    print(f"wrote {target} ({len(ours)} coba themes, {len(merged)} total)")
    print("restart Octarine, then Settings > Preferences > Theme.")


if __name__ == "__main__":
    main()

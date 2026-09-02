#!/usr/bin/env python3
"""Generate the coba themes for iTerm2, VS Code and Octarine from one palette.

Four schemes, all rooted in Le Corbusier's Polychromie Architecturale (Salubra,
1931 + 1959) and taken further where it did not reach. coba wax is the warm one
and stays closest to the Salubra set. coba pine is a green ground. coba dawn and
coba dusk are a cool slate pair, light and dark, built to invert each other.

Each entry is (hex, id, name). The id is a Salubra number where the tone is one
of the 63, or "*" where it is shaded off them because no member of the set
worked at that contrast.
"""
import json, math, os, plistlib, sys

WAX = {
    #  slot            hex        id       name
    "background":   ("f5f0e8", "*",     "warm ground, on the yellow axis"),
    "foreground":   ("2b3642", "*",     "cool slate ink"),
    "bold":         ("1b232c", "*",     "cool slate ink, deepened"),
    "cursor":       ("c95750", "*",    "red accent"),
    "cursor_text":  ("f5f0e8", "*",     "warm ground, on the yellow axis"),
    "selection":    ("e3dcd0", "*",     "sunken, de-pinked"),
    "selected_text":("2b3642", "*",     "cool slate ink"),
    "link":         ("395a8e", "4320K", "bleu outremer 59"),
    "badge":        ("a33a29", "4320A", "rouge vermillon 59"),
    "tab":          ("ebe4d9", "*",     "panel, de-pinked"),
    "guide":        ("e3dcd0", "*",     "sunken, de-pinked"),
    "comment":      ("65686f", "*",     "cool neutral, darkened to read"),
    "panel":        ("ebe4d9", "*",     "panel, de-pinked"),
    "line":         ("f0eae0", "*",     "panel, lightened and de-pinked"),

    "ansi0":  ("49443b", "32140", "ombre naturelle 31"),
    "ansi1":  ("a33a29", "4320A", "rouge vermillon 59"),
    "ansi2":  ("57633c", "*",     "olive"),
    "ansi3":  ("826417", "*",     "ocre fonce"),
    "ansi4":  ("0e2d58", "4320T", "bleu outremer fonce"),
    "ansi5":  ("6c2b3b", "4320M", "le rubis"),
    "ansi6":  ("2e747f", "*",     "teal, off the blue it collided with"),
    "ansi7":  ("7a7c81", "*",     "cool neutral, darkened to read"),
    "ansi8":  ("65686f", "*",     "cool neutral, darkened to read"),
    "ansi9":  ("b8493a", "*",     "vermillon lightened toward the red accent"),
    "ansi10": ("6e764d", "*",     "olive, lightened"),
    "ansi11": ("a4832a", "*",     "amber-ochre"),
    "ansi12": ("395a8e", "4320K", "bleu outremer 59"),
    "ansi13": ("811c35", "32100", "rouge carmin"),
    "ansi14": ("5a8a93", "32031", "ceruleen vif"),
    "ansi15": ("8d8888", "*",     "cool neutral, darkened to read"),
}

PINE = {
    "background":   ("21302c", "*",     "g0 lifted to L* 18, chroma 7"),
    "foreground":   ("bfd7ce", "*",     "txt, chroma pulled toward the ground"),
    "bold":         ("eafff4", "*",    "hot white"),
    "cursor":       ("8fe6c0", "*",    "mint"),
    "cursor_text":  ("21302c", "*",     "g0 lifted to L* 18, chroma 7"),
    "selection":    ("404f4b", "*",     "surface lifted"),
    "selected_text":("eafff4", "*",    "hot white"),
    "link":         ("8fe6c0", "*",    "mint"),
    "badge":        ("e8a08a", "*",    "err salmon"),
    "tab":          ("101e1b", "*",     "g0 shaded"),
    "guide":        ("404f4b", "*",     "surface lifted"),
    "comment":      ("8ba296", "*",     "txt-dim lifted"),
    "panel":        ("101e1b", "*",     "g0 shaded"),
    "line":         ("2e3d3a", "*",     "surface tint"),

    "ansi0":  ("303f3b", "*",     "surface shaded"),
    "ansi1":  ("e8a08a", "*",    "err salmon"),
    "ansi2":  ("8fe6c0", "*",    "mint"),
    "ansi3":  ("f2b573", "4320L", "ocre jaune clair"),
    "ansi4":  ("7facc6", "4320N", "bleu ceruleen 59"),
    "ansi5":  ("de8da0", "4320C", "rose vif"),
    "ansi6":  ("6db3ad", "*",     "teal, ceruleen moyen shifted off the blue"),
    "ansi7":  ("bfd7ce", "*",     "txt, chroma pulled toward the ground"),
    "ansi8":  ("8ba296", "*",     "txt-dim lifted"),
    "ansi9":  ("f0bcac", "*",     "err salmon lightened"),
    "ansi10": ("d6ffee", "*",    "hot mint"),
    "ansi11": ("f4bd48", "4320W", "le jaune vif"),
    "ansi12": ("96b4c9", "32021", "outremer moyen"),
    "ansi13": ("eba9bb", "*",     "rose vif lightened"),
    "ansi14": ("99bdb8", "32033", "ceruleen clair"),
    "ansi15": ("eafff4", "*",    "hot white"),
}

DUSK = {
    #  slot            hex        id        name
    # This started as a near-black ground under a warm cream, an 81 point L*
    # span at 13.5:1, which glares. The ground is lifted to a L* 19 slate and
    # the ink eased to a 67 point span, where coba pine sits. Everything that
    # was a lift off the near-black is rebuilt upward onto the ground's own
    # hue. The warm-on-cold tension is the point and is kept.
    "background":   ("243037", "*",      "ground lifted to L* 19, slate"),
    "foreground":   ("c1b8b0", "*",      "cream, eased off a 13.5 ratio"),
    "bold":         ("e3ddd7", "*",      "hot cream, eased with the body"),
    "cursor":       ("7bbac7", "*",      "cyan"),
    "cursor_text":  ("243037", "*",      "ground lifted to L* 19, slate"),
    "selection":    ("3d4b54", "*",      "slate lifted to L* 31"),
    "selected_text":("e3ddd7", "*",      "hot cream, eased with the body"),
    "link":         ("7bbac7", "*",      "cyan"),
    "badge":        ("ff5879", "*",      "magenta"),
    "tab":          ("151f25", "*",      "slate shaded to L* 11"),
    "guide":        ("3d4b54", "*",      "slate lifted to L* 31"),
    "comment":      ("9ba5ae", "*",      "slate grey, on the ground's own hue"),
    "panel":        ("151f25", "*",      "slate shaded to L* 11"),
    "line":         ("2e3a41", "*",      "slate lifted one step"),

    "ansi0":  ("303d46", "*",      "shadow slot, slate at L* 25"),
    # This red arrived at 3.6 against its original ground. Lifting it alone slid
    # it into the magenta, so it is rotated 11 degrees toward orange as well.
    "ansi1":  ("e67665", "*",      "red, lifted and rotated off the magenta"),
    "ansi2":  ("7cbf9e", "*",      "green"),
    "ansi3":  ("a4947c", "*",      "yellow, lifted to clear 4.5"),
    # The source ran one hex in both the blue and cyan slots. coba needs them
    # apart, so the cyan keeps it and the blue is pulled off.
    "ansi4":  ("7fa8d8", "*",      "blue, split off the cyan it shared a hex with"),
    "ansi5":  ("ff5c7c", "*",      "magenta, a hair up to clear 4.5"),
    "ansi6":  ("7bbac7", "*",      "cyan"),
    "ansi7":  ("c1b8b0", "*",      "cream, eased off a 13.5 ratio"),
    "ansi8":  ("9ba5ae", "*",      "slate grey, on the ground's own hue"),
    "ansi9":  ("ef5847", "*",      "bright red"),
    "ansi10": ("a2d9b1", "*",      "bright green"),
    "ansi11": ("bbae82", "*",      "bright yellow, off the eased body text"),
    "ansi12": ("a8c4e8", "*",      "blue lightened"),
    "ansi13": ("ff99a1", "*",      "bright magenta"),
    "ansi14": ("dff0eb", "*",      "bright cyan"),
    "ansi15": ("e3ddd7", "*",      "hot cream, eased with the body"),
}

DAWN = {
    #  slot            hex        id   name
    # coba dawn is coba dusk inverted: the same hues, darkened onto a cool
    # ground, so the two work as a light/dark pair. Only the hue family carries
    # over, every tone here is mixed for this ground.
    "background":   ("ebf2f7", "*", "cool ground at L* 95 on the slate axis"),
    "foreground":   ("303e47", "*", "slate ink"),
    "bold":         ("1a242a", "*", "slate ink, deepened"),
    "cursor":       ("00788b", "*", "deep teal accent"),
    "cursor_text":  ("ebf2f7", "*", "cool ground at L* 95 on the slate axis"),
    "selection":    ("ced7dd", "*", "ground sunk to L* 86"),
    "selected_text":("1a242a", "*", "slate ink, deepened"),
    "link":         ("0064a0", "*", "dusk blue, darkened for a light ground"),
    "badge":        ("a93a2f", "*", "dusk red, darkened for a light ground"),
    "tab":          ("dae2e8", "*", "panel at L* 90"),
    "guide":        ("ced7dd", "*", "ground sunk to L* 86"),
    "comment":      ("5f6a72", "*", "slate neutral, darkened to read"),
    "panel":        ("dae2e8", "*", "panel at L* 90"),
    "line":         ("e4eaf0", "*", "panel, lightened"),

    "ansi0":  ("45545f", "*", "slate, near black"),
    "ansi1":  ("a93a2f", "*", "dusk red, darkened"),
    "ansi2":  ("006e47", "*", "dusk green, darkened"),
    "ansi3":  ("795b16", "*", "dusk yellow, darkened"),
    "ansi4":  ("0064a0", "*", "dusk blue, darkened"),
    # On a light ground the red and magenta both darken toward the same
    # crimson, so this one is rotated 24 degrees off the pink dusk uses.
    "ansi5":  ("a2386f", "*", "dusk magenta, darkened and rotated off the red"),
    "ansi6":  ("00697d", "*", "dusk cyan, darkened"),
    "ansi7":  ("738089", "*", "slate neutral"),
    "ansi8":  ("5f6a72", "*", "slate neutral, darkened to read"),
    "ansi9":  ("d35141", "*", "dusk bright red, darkened"),
    "ansi10": ("308c54", "*", "dusk bright green, darkened"),
    "ansi11": ("8c7c24", "*", "dusk bright yellow, darkened"),
    "ansi12": ("0082ca", "*", "dusk bright blue, darkened"),
    "ansi13": ("cc4e89", "*", "dusk bright magenta, darkened and rotated"),
    "ansi14": ("238b77", "*", "dusk bright cyan, darkened"),
    "ansi15": ("808a92", "*", "slate neutral, lightened"),
}

SCHEMES = {"coba wax": WAX, "coba pine": PINE,
           "coba dawn": DAWN, "coba dusk": DUSK}
COBA_GUID = "1A0DEE71-1E00-4B0A-9E51-1B0EC1F0A1DE"
COOL_GUID = "5D05C0DE-2B1B-4D0F-9C21-7E1D0B5A4C33"
HERE = os.path.dirname(os.path.abspath(__file__))


def hx(scheme, slot):
    return scheme[slot][0]


def sharp(scheme, slot):
    return "#" + scheme[slot][0]


# --- contrast -------------------------------------------------------------
def _lin(c):
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(h):
    r, g, b = (_lin(int(h[i:i + 2], 16) / 255.0) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)))
    return (lb + 0.05) / (la + 0.05)


def delta_e(c1, c2):
    """CIEDE2000. Below about 12 two terminal colours start reading as one."""
    def _lab(x):
        r, g, b = (_lin(int(x[i:i + 2], 16) / 255.0) for i in (0, 2, 4))
        X = (0.4124*r + 0.3576*g + 0.1805*b) / 0.95047
        Y = 0.2126*r + 0.7152*g + 0.0722*b
        Z = (0.0193*r + 0.1192*g + 0.9505*b) / 1.08883
        f = lambda t: t ** (1/3) if t > 0.008856 else 7.787*t + 16/116
        fx, fy, fz = f(X), f(Y), f(Z)
        return 116*fy - 16, 500*(fx - fy), 200*(fy - fz)
    L1, a1, b1 = _lab(c1); L2, a2, b2 = _lab(c2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb**7 / (Cb**7 + 25**7))) if Cb else 0
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dhp = 0 if C1p * C2p == 0 else ((h2p - h1p + 180) % 360) - 180
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lb, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:          hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180: hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:       hbp = (h1p + h2p + 360) / 2
    else:                       hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17*math.cos(math.radians(hbp - 30)) + 0.24*math.cos(math.radians(2*hbp))
         + 0.32*math.cos(math.radians(3*hbp + 6)) - 0.20*math.cos(math.radians(4*hbp - 63)))
    Sl = 1 + (0.015 * (Lb - 50)**2) / math.sqrt(20 + (Lb - 50)**2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = (-2 * math.sqrt(Cbp**7 / (Cbp**7 + 25**7))
          * math.sin(math.radians(60 * math.exp(-(((hbp - 275) / 25) ** 2))))) if Cbp else 0
    return math.sqrt((dLp/Sl)**2 + (dCp/Sc)**2 + (dHp/Sh)**2 + Rt * (dCp/Sc) * (dHp/Sh))


# One source of truth for the gate. check() enforces these and build_contrast()
# publishes them; writing the numbers twice would let the table drift from what
# is actually enforced.
#
# ansi0 is the shadow slot, meant to sit near the ground, so it has no floor.
# Everything else, 7 and 15 included, is a colour programs emit as text.
FLOORS = ([("foreground", 4.5), ("comment", 4.5)]
          + [(f"ansi{i}", 4.5) for i in range(1, 7)]
          + [(f"ansi{i}", 3.0) for i in (7, 8, 9, 10, 11, 12, 13, 14, 15)])

# Body text and comments must not read as one of the colours they sit next to.
# Looser for the brights: a pale ink near a pale bright is normal in a
# near-monochrome scheme, a comment the same colour as a string is not.
INK_DE = [(i, 10.0) for i in range(1, 7)] + [(i, 7.5) for i in (9, 10, 11, 12, 13, 14)]

# Slots carrying different meanings. Same-hue normal/bright pairs are skipped:
# looking alike is the point of a bright.
PAIRS, PAIR_DE = ((1, 3), (1, 5), (2, 3), (2, 6), (4, 6), (6, 12), (1, 13), (2, 14)), 12.0


def measure(s):
    """Every gated number for one scheme, as (label, value, floor) triples."""
    bg = hx(s, "background")
    out = [(slot, contrast(hx(s, slot), bg), floor) for slot, floor in FLOORS]
    out += [(f"{base}/ansi{i}", delta_e(hx(s, base), hx(s, f"ansi{i}")), floor)
            for base in ("foreground", "comment") for i, floor in INK_DE]
    out += [(f"ansi{i}/ansi{j}", delta_e(hx(s, f"ansi{i}"), hx(s, f"ansi{j}")), PAIR_DE)
            for i, j in PAIRS]
    return out


def check(strict=False):
    """Contrast floors, plus the pairs that must not read as one colour."""
    bad = []
    for name, s in SCHEMES.items():
        for label, value, floor in measure(s):
            if value < floor:
                bad.append(f"{name} {label} {value:.2f} < {floor}")
    for line in bad:
        print("CONTRAST:", line, file=sys.stderr)
    if strict and bad:
        sys.exit(1)
    return not bad


# --- iTerm2 ---------------------------------------------------------------
ITERM_SLOTS = {
    "Background": "background", "Foreground": "foreground", "Bold": "bold",
    "Link": "link", "Cursor": "cursor", "Cursor Text": "cursor_text",
    "Selection": "selection", "Selected Text": "selected_text",
    "Badge": "badge", "Tab": "tab", "Cursor Guide": "guide",
    **{f"Ansi {i}": f"ansi{i}" for i in range(16)},
}


def comp(h, alpha=True):
    d = {"Color Space": "sRGB"}
    for k, i in (("Red Component", 0), ("Green Component", 2), ("Blue Component", 4)):
        d[k] = int(h[i:i + 2], 16) / 255.0
    if alpha:
        d["Alpha Component"] = 1.0
    return d


# Everything both profiles share. Colours and the light/dark split are not here.
# No font: it inherits whatever Default already has.
PROFILE_BASE = {
    "Dynamic Profile Parent Name": "Default",
    "Use Non-ASCII Font": False,
    "ASCII Anti Aliased": True,
    "Non-ASCII Anti Aliased": True,
    "Horizontal Spacing": 1.0,
    "Vertical Spacing": 1.0,
    "Use Bold Font": True,
    "Use Bright Bold": False,
    "Minimum Contrast": 0,
    "Show Mark Indicators": False,
}


def build_iterm():
    out = os.path.join(HERE, "iterm")
    os.makedirs(out, exist_ok=True)
    for fname, s in (("coba-wax", WAX), ("coba-pine", PINE),
                     ("coba-dawn", DAWN), ("coba-dusk", DUSK)):
        with open(os.path.join(out, fname + ".itermcolors"), "wb") as f:
            plistlib.dump({f"{k} Color": comp(hx(s, v)) for k, v in ITERM_SLOTS.items()}, f)

    profiles = [{
        # The switching profile: light by day, pine by night.
        "Name": "coba",
        "Guid": COBA_GUID,
        **PROFILE_BASE,
        "Use Separate Colors for Light and Dark Mode": True,
        **{f"{k} Color (Light)": comp(hx(WAX, v), alpha=False) for k, v in ITERM_SLOTS.items()},
        **{f"{k} Color (Dark)": comp(hx(PINE, v), alpha=False) for k, v in ITERM_SLOTS.items()},
    }, {
        # The cool pair: dawn by day, dusk by night. Same hue family either way.
        "Name": "coba cool",
        "Guid": COOL_GUID,
        **PROFILE_BASE,
        "Use Separate Colors for Light and Dark Mode": True,
        **{f"{k} Color (Light)": comp(hx(DAWN, v), alpha=False) for k, v in ITERM_SLOTS.items()},
        **{f"{k} Color (Dark)": comp(hx(DUSK, v), alpha=False) for k, v in ITERM_SLOTS.items()},
    }]
    with open(os.path.join(out, "coba.json"), "w") as f:
        json.dump({"Profiles": profiles}, f, indent=2)
        f.write("\n")


# --- VS Code --------------------------------------------------------------
def vscode_theme(name, s, kind):
    g, a = (lambda k: sharp(s, k)), (lambda i: sharp(s, f"ansi{i}"))
    bg, fg, panel, line = g("background"), g("foreground"), g("panel"), g("line")
    accent, muted = g("cursor"), g("comment")
    return {
        "name": name,
        "type": kind,
        "semanticHighlighting": True,
        "colors": {
            "editor.background": bg,
            "editor.foreground": fg,
            "editor.lineHighlightBackground": line,
            "editor.selectionBackground": g("selection"),
            "editor.selectionHighlightBackground": g("guide"),
            "editor.findMatchBackground": g("guide"),
            "editor.findMatchHighlightBackground": line,
            "editorCursor.foreground": g("cursor"),
            "editorLineNumber.foreground": a(8),
            "editorLineNumber.activeForeground": fg,
            "editorIndentGuide.background1": line,
            "editorIndentGuide.activeBackground1": a(8),
            "editorWhitespace.foreground": line,
            "editorBracketMatch.background": g("selection"),
            "editorBracketMatch.border": accent,
            "editorGutter.addedBackground": a(2),
            "editorGutter.modifiedBackground": a(4),
            "editorGutter.deletedBackground": a(1),
            "editorError.foreground": a(1),
            "editorWarning.foreground": a(3),
            "editorInfo.foreground": a(4),
            "editorWidget.background": panel,
            "editorWidget.border": line,
            "editorSuggestWidget.selectedBackground": g("selection"),
            "editorHoverWidget.background": panel,
            "editorHoverWidget.border": line,
            "sideBar.background": panel,
            "sideBar.foreground": fg,
            "sideBar.border": line,
            "sideBarSectionHeader.background": panel,
            "sideBarTitle.foreground": muted,
            "activityBar.background": panel,
            "activityBar.foreground": fg,
            "activityBar.inactiveForeground": muted,
            "activityBar.border": line,
            "activityBarBadge.background": accent,
            "activityBarBadge.foreground": g("cursor_text"),
            "statusBar.background": panel,
            "statusBar.foreground": muted,
            "statusBar.border": line,
            "statusBar.noFolderBackground": panel,
            "statusBar.debuggingBackground": accent,
            "statusBar.debuggingForeground": g("cursor_text"),
            "statusBarItem.remoteBackground": a(4),
            "statusBarItem.remoteForeground": g("background"),
            "titleBar.activeBackground": panel,
            "titleBar.activeForeground": fg,
            "titleBar.inactiveBackground": panel,
            "titleBar.inactiveForeground": muted,
            "titleBar.border": line,
            "tab.activeBackground": bg,
            "tab.activeForeground": fg,
            "tab.activeBorderTop": accent,
            "tab.inactiveBackground": panel,
            "tab.inactiveForeground": muted,
            "tab.border": line,
            "editorGroupHeader.tabsBackground": panel,
            "editorGroupHeader.tabsBorder": line,
            "breadcrumb.background": bg,
            "breadcrumb.foreground": muted,
            "breadcrumb.focusForeground": fg,
            "panel.background": bg,
            "panel.border": line,
            "panelTitle.activeForeground": fg,
            "panelTitle.inactiveForeground": muted,
            "terminal.background": bg,
            "terminal.foreground": fg,
            "terminalCursor.foreground": g("cursor"),
            "terminal.selectionBackground": g("selection"),
            **{f"terminal.ansi{k}": a(i) for k, i in (
                ("Black", 0), ("Red", 1), ("Green", 2), ("Yellow", 3),
                ("Blue", 4), ("Magenta", 5), ("Cyan", 6), ("White", 7),
                ("BrightBlack", 8), ("BrightRed", 9), ("BrightGreen", 10),
                ("BrightYellow", 11), ("BrightBlue", 12), ("BrightMagenta", 13),
                ("BrightCyan", 14), ("BrightWhite", 15))},
            "list.activeSelectionBackground": g("selection"),
            "list.activeSelectionForeground": fg,
            "list.inactiveSelectionBackground": line,
            "list.hoverBackground": line,
            "list.highlightForeground": accent,
            "input.background": bg,
            "input.foreground": fg,
            "input.border": line,
            "inputOption.activeBorder": accent,
            "dropdown.background": panel,
            "dropdown.border": line,
            "button.background": accent,
            "button.foreground": g("cursor_text"),
            "badge.background": g("badge"),
            "badge.foreground": g("background"),
            "focusBorder": accent,
            "foreground": fg,
            "widget.shadow": "#00000022",
            "scrollbarSlider.background": g("selection") + "99",
            "scrollbarSlider.hoverBackground": g("selection"),
            "scrollbarSlider.activeBackground": a(8),
            "minimap.selectionHighlight": g("selection"),
            "gitDecoration.modifiedResourceForeground": a(4),
            "gitDecoration.addedResourceForeground": a(2),
            "gitDecoration.deletedResourceForeground": a(1),
            "gitDecoration.untrackedResourceForeground": a(2),
            "gitDecoration.ignoredResourceForeground": muted,
            "textLink.foreground": g("link"),
            "textLink.activeForeground": accent,
            "peekViewEditor.background": panel,
            "peekViewResult.background": panel,
            "notificationCenterHeader.background": panel,
            "notifications.background": panel,
            "notifications.border": line,
        },
        "tokenColors": [
            {"scope": ["comment", "punctuation.definition.comment"],
             "settings": {"foreground": muted, "fontStyle": "italic"}},
            {"scope": ["string", "constant.other.symbol", "meta.embedded.assembly"],
             "settings": {"foreground": a(2)}},
            {"scope": ["constant.numeric", "constant.language", "constant.character",
                       "keyword.other.unit"],
             "settings": {"foreground": a(5)}},
            {"scope": ["keyword", "storage", "storage.type", "keyword.control"],
             "settings": {"foreground": a(1)}},
            {"scope": ["keyword.operator", "punctuation.separator", "punctuation.terminator"],
             "settings": {"foreground": a(8) if kind == "light" else a(7)}},
            {"scope": ["entity.name.function", "support.function", "meta.function-call"],
             "settings": {"foreground": a(4)}},
            {"scope": ["entity.name.type", "entity.name.class", "support.type",
                       "support.class", "entity.other.inherited-class"],
             "settings": {"foreground": a(6)}},
            {"scope": ["variable", "variable.other", "meta.definition.variable"],
             "settings": {"foreground": fg}},
            {"scope": ["variable.parameter", "variable.other.property",
                       "support.variable.property"],
             "settings": {"foreground": a(12)}},
            {"scope": ["entity.name.tag", "punctuation.definition.tag"],
             "settings": {"foreground": a(1)}},
            {"scope": ["entity.other.attribute-name"],
             "settings": {"foreground": a(3), "fontStyle": "italic"}},
            {"scope": ["support.type.property-name.json", "support.type.property-name.css",
                       "meta.object-literal.key"],
             "settings": {"foreground": a(4)}},
            {"scope": ["markup.heading", "entity.name.section"],
             "settings": {"foreground": a(1), "fontStyle": "bold"}},
            {"scope": ["markup.bold"], "settings": {"fontStyle": "bold"}},
            {"scope": ["markup.italic"], "settings": {"fontStyle": "italic"}},
            {"scope": ["markup.inline.raw", "markup.fenced_code"],
             "settings": {"foreground": a(3)}},
            {"scope": ["markup.underline.link"],
             "settings": {"foreground": g("link"), "fontStyle": "underline"}},
            {"scope": ["markup.inserted"], "settings": {"foreground": a(2)}},
            {"scope": ["markup.deleted"], "settings": {"foreground": a(1)}},
            {"scope": ["markup.changed"], "settings": {"foreground": a(3)}},
            {"scope": ["invalid", "invalid.illegal"], "settings": {"foreground": a(9)}},
        ],
    }


def build_vscode():
    out = os.path.join(HERE, "vscode", "themes")
    os.makedirs(out, exist_ok=True)
    for slug, label, s, kind in (("coba-wax", "coba wax", WAX, "light"),
                                 ("coba-pine", "coba pine", PINE, "dark"),
                                 ("coba-dawn", "coba dawn", DAWN, "light"),
                                 ("coba-dusk", "coba dusk", DUSK, "dark")):
        with open(os.path.join(out, f"{slug}-color-theme.json"), "w") as f:
            json.dump(vscode_theme(label, s, kind), f, indent=2)
            f.write("\n")


def build_preview(name, s, path):
    """One SVG per scheme: a terminal specimen over the 16 slots.

    A bare colour strip shows the palette but not the theme. This renders real
    output in it, which is what the README is for. Only the first tspan of each
    line is positioned; the rest flow, so nothing depends on guessing the glyph
    advance of whichever monospace font the renderer happens to resolve. No
    window chrome: coba is a colour scheme, not a window, so the specimen is
    just the background and padding, the same shape it takes over a real
    terminal's own content area.
    """
    g, a = (lambda k: sharp(s, k)), (lambda i: sharp(s, f"ansi{i}"))
    FS, LH, W, PAD = 13, 21, 720, 18
    TOP = PAD + FS

    def line(y, segs):
        out = []
        for i, (text, fill) in enumerate(segs):
            esc = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            pos = f' x="{PAD}" y="{y}"' if i == 0 else ""
            out.append(f'<tspan{pos} fill="{fill}">{esc}</tspan>')
        return "".join(out)

    fg, dim = g("foreground"), g("comment")
    rows = [
        [("~/dev/coba", dim)],
        [("base ", dim), ("\u276f ", a(5)), ("python3", a(2)), (" build.py ", fg), ("--strict", a(6))],
        [("built iterm/, vscode/, octarine/ ", fg), ("(contrast ok)", dim)],
        [("base ", dim), ("\u276f ", a(5)), ("git", a(2)), (" status ", fg), ("--short", a(6))],
        [(" M", a(3)), (" build.py", fg)],
        [("??", a(2)), (" octarine/", fg)],
        [("base ", dim), ("\u276f ", a(5)), ("\u2588", g("cursor"))],
    ]
    body_h = TOP + LH * len(rows) + 10
    sw_y, SW = body_h + 6, 26
    H = sw_y + SW + PAD

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" role="img" aria-label="{name} colour scheme preview">',
             f'<rect width="{W}" height="{H}" rx="6" fill="{g("background")}"/>']
    parts.append(f'<text font-size="{FS}" xml:space="preserve" '
                 f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace">')
    for i, segs in enumerate(rows):
        parts.append(line(TOP + i * LH, segs))
    parts.append("</text>")
    cw = (W - PAD * 2) / 16
    for i in range(16):
        parts.append(f'<rect x="{PAD + i * cw:.1f}" y="{sw_y}" width="{cw - 3:.1f}" '
                     f'height="{SW}" rx="2" fill="{a(i)}"/>')
    parts.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(parts) + "\n")


def build_previews():
    out = os.path.join(HERE, "assets")
    os.makedirs(out, exist_ok=True)
    for slug, name in (("coba-wax", "coba wax"), ("coba-pine", "coba pine"),
                       ("coba-dawn", "coba dawn"), ("coba-dusk", "coba dusk")):
        build_preview(name, SCHEMES[name], os.path.join(out, slug + ".svg"))


# --- Octarine -------------------------------------------------------------
# Octarine themes are a flat block of CSS custom properties, imported through
# Settings > Theme Creator. Missing variables are filled from the base theme,
# so every variable it reads is set here rather than left to inherit.
#
# The surface ladder differs by scheme: coba wax stacks upward off the ground
# (panel is lighter), coba pine stacks the sidebar darker than the ground and
# lifts the inline surfaces instead. So the ladder is per-scheme, not a formula.
LADDER = {
    "coba wax": ("line", "panel", "selection"),
    "coba pine":  ("line", "ansi0", "selection"),
    "coba dusk":  ("line", "ansi0", "selection"),
    "coba dawn":  ("line", "panel", "selection"),
}


def mix(a, b, t):
    """Blend two hexes in sRGB. Used for the tints Octarine wants where the
    palette has no slot: mark, error ground, hover. Opaque on purpose, an
    alpha would sit differently over the sidebar than over the editor."""
    return "".join(f"{round(int(a[i:i+2],16)*(1-t) + int(b[i:i+2],16)*t):02x}"
                   for i in (0, 2, 4))


def octarine_vars(name, s):
    g, a = (lambda k: sharp(s, k)), (lambda i: sharp(s, f"ansi{i}"))
    bg = hx(s, "background")
    inter, second, third = (sharp(s, k) for k in LADDER[name])
    return {
        "--color-text-primary":     g("foreground"),
        "--color-text-secondary":   g("comment"),
        # A real ladder: comment, then two steps sunk toward the ground. ansi8
        # is not used here, it is the same hex as comment in coba pine.
        "--color-text-tertiary":    "#" + mix(bg, hx(s, "comment"), 0.80),
        "--color-text-placeholder": "#" + mix(bg, hx(s, "comment"), 0.55),
        "--color-text-link":        g("link"),
        "--color-text-accent":      g("cursor"),
        "--color-text-error":       a(1),
        "--color-editor-body":      g("foreground"),
        "--color-editor-heading":   g("bold"),

        "--color-bg-primary":      g("background"),
        "--color-bg-intermediate": inter,
        "--color-bg-secondary":    second,
        "--color-bg-tertiary":     third,
        "--color-bg-hover":        inter,
        "--color-bg-accent":       g("cursor"),
        "--color-bg-doc-link":     "#" + mix(bg, hx(s, "link"), 0.22),
        "--color-bg-mark":         "#" + mix(bg, hx(s, "ansi11"), 0.30),
        "--color-bg-error":        "#" + mix(bg, hx(s, "ansi1"), 0.22),
        "--color-bg-kbd":          second,
        "--color-bg-tooltip":      g("tab"),
        "--color-app-sidebar":     g("panel"),

        "--color-border-primary":   g("guide"),
        "--color-border-secondary": inter,
        "--color-border-accent":    g("cursor"),
        "--color-border-error":     a(1),
        "--color-icon":             g("comment"),
        "--color-outline-primary":  g("cursor"),
    }


# Fixed so a rebuild does not churn the file. Octarine only displays these.
OCTARINE_STAMP = 1755950000000

# Octarine forks a custom theme off a built-in and keeps the parent recorded.
# It never reads back through it: all 27 variables are set, and the app has no
# :root fallback, so nothing here actually inherits.
OCTARINE_BASE = {"coba wax": "default-light", "coba pine": "default-dark",
                 "coba dawn": "default-light", "coba dusk": "default-dark"}


def build_octarine():
    out = os.path.join(HERE, "octarine")
    os.makedirs(out, exist_ok=True)
    themes = []
    for slug, name in (("coba-wax", "coba wax"), ("coba-pine", "coba pine"),
                       ("coba-dawn", "coba dawn"), ("coba-dusk", "coba dusk")):
        v = octarine_vars(name, SCHEMES[name])
        # Comments are rejected by the Theme Creator's paste import, so the
        # file is variable lines only.
        body = "\n".join(f"{k}: {val};" for k, val in v.items()) + "\n"
        with open(os.path.join(out, slug + ".css"), "w") as f:
            f.write(body)
        themes.append({
            "id": slug,
            "name": name,
            "variables": v,
            "dark": OCTARINE_BASE[name] == "default-dark",
            "baseTheme": OCTARINE_BASE[name],
            "created": OCTARINE_STAMP,
            "modified": OCTARINE_STAMP,
        })
    # Drops into <workspace>/.octarine/themes.json. install-octarine.sh merges
    # it rather than copying, so themes made in the app are not lost.
    with open(os.path.join(out, "themes.json"), "w") as f:
        json.dump(themes, f, indent=2)
        f.write("\n")


def build_contrast():
    """CONTRAST.md: every number the gate checks, with its margin.

    The gate says pass or fail. This publishes the actual figures, which is the
    part worth reading: where a scheme sits comfortably and where it is a
    rounding error from the floor.
    """
    lines = ["# Contrast", "",
             "Generated by `build.py`. Every figure is measured from",
             "`palette.json`, not asserted. `python3 build.py --strict` refuses to",
             "write if any of them falls below its floor.", "",
             "Ratios are WCAG 2.x contrast against the scheme's own ground.",
             "Separations are CIEDE2000, which is roughly perceptual: below about",
             "12, two terminal colours start reading as one.", ""]

    tight = []
    for name, s in SCHEMES.items():
        rows = measure(s)
        worst = min(rows, key=lambda r: r[1] - r[2])
        tight.append((worst[1] - worst[2], name, worst))
        ratios = [r for r in rows if "/" not in r[0]]
        seps = [r for r in rows if "/" in r[0]]

        lines += [f"## {name}", "",
                  f"Ground `{sharp(s, 'background')}`, ink `{sharp(s, 'foreground')}`.", "",
                  "| slot | hex | ratio | floor | margin |",
                  "| --- | --- | --: | --: | --: |"]
        for slot, val, floor in ratios:
            lines.append(f"| {slot} | `{sharp(s, slot)}` | {val:.2f} | {floor} | "
                         f"{val - floor:+.2f} |")
        lines += ["", "| separation | dE | floor | margin |", "| --- | --: | --: | --: |"]
        for label, val, floor in seps:
            lines.append(f"| {label} | {val:.1f} | {floor} | {val - floor:+.1f} |")
        lines += ["", f"`ansi0` (`{sharp(s, 'ansi0')}`) is the shadow slot and has no "
                      f"floor; it is meant to sit near the ground.", ""]

    tight.sort()
    lines += ["## Tightest margins", "",
              "The closest call in each scheme. These are what to watch when",
              "editing a palette.", "",
              "| scheme | measure | value | floor | margin |",
              "| --- | --- | --: | --: | --: |"]
    for margin, name, (label, val, floor) in tight:
        lines.append(f"| {name} | {label} | {val:.2f} | {floor} | {margin:+.2f} |")
    lines.append("")

    with open(os.path.join(HERE, "CONTRAST.md"), "w") as f:
        f.write("\n".join(lines))


def build_palette_json():
    with open(os.path.join(HERE, "palette.json"), "w") as f:
        json.dump({n: {k: {"hex": "#" + v[0], "salubra": v[1], "name": v[2]}
                       for k, v in s.items()} for n, s in SCHEMES.items()}, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    ok = check(strict="--strict" in sys.argv)
    build_iterm()
    build_vscode()
    build_octarine()
    build_previews()
    build_palette_json()
    build_contrast()
    print("built iterm/, vscode/themes/, octarine/, assets/, palette.json, CONTRAST.md", "(contrast ok)" if ok else "(see warnings)")

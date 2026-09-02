#!/usr/bin/env python3
"""Checks for the colour maths in build.py. Run: python3 test_build.py

check() guards the palettes. This guards check(): if contrast() or delta_e()
were wrong, every scheme would pass a gate that means nothing.
"""
import build as b


def close(a, x, tol=0.5):
    assert abs(a - x) <= tol, f"{a} != {x} (tol {tol})"


def test_contrast():
    # The two fixed points of the WCAG ratio.
    close(b.contrast("ffffff", "000000"), 21.0, 0.01)
    close(b.contrast("808080", "808080"), 1.0, 0.01)
    # Symmetric: the formula sorts its inputs.
    close(b.contrast("ff0000", "00ff00"), b.contrast("00ff00", "ff0000"), 0.001)
    # A published value: #767676 is the darkest grey passing 4.5 on white.
    assert b.contrast("767676", "ffffff") >= 4.5
    assert b.contrast("777777", "ffffff") < 4.5


def test_delta_e():
    assert b.delta_e("abcdef", "abcdef") == 0.0
    # White to black is analytically exact: dL* is 100, both chromas are 0, so
    # every weighting term collapses to 1 and dE is just dL*.
    close(b.delta_e("ffffff", "000000"), 100.0, 0.01)
    # Symmetric, and monotone in the obvious direction.
    close(b.delta_e("c0392b", "2980b9"), b.delta_e("2980b9", "c0392b"), 0.001)
    assert b.delta_e("ffffff", "000000") > b.delta_e("ff0000", "fe0000")
    # The gate's own threshold: two slots at dE 12 are the borderline case it
    # is written around, so a pair well inside it must score below.
    assert b.delta_e("7bbac7", "7cbbc8") < 12


def test_mix():
    assert b.mix("000000", "ffffff", 0.0) == "000000"
    assert b.mix("000000", "ffffff", 1.0) == "ffffff"
    assert b.mix("000000", "ffffff", 0.5) == "808080"


def test_schemes_pass_their_own_gate():
    assert b.check(), "a shipped scheme fails check()"


def test_every_scheme_is_complete():
    slots = set(b.WAX)
    for name, s in b.SCHEMES.items():
        assert set(s) == slots, f"{name} slot set differs from coba wax"
        for slot, (hexv, _id, _n) in s.items():
            assert len(hexv) == 6 and all(c in "0123456789abcdef" for c in hexv), \
                f"{name} {slot} is not a 6-digit lowercase hex: {hexv}"


def test_octarine_sets_every_variable():
    # Octarine has no :root fallback, so an omitted variable renders as nothing.
    keys = None
    for name in b.SCHEMES:
        v = b.octarine_vars(name, b.SCHEMES[name])
        assert len(v) == 27, f"{name} emits {len(v)} variables, expected 27"
        keys = keys or set(v)
        assert set(v) == keys, f"{name} emits a different variable set"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")

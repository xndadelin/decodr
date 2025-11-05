_names = (
    "hill",
    "homophonic",
    "rot47",
    "bacon",
    "gronsfeld",
    "caesar",
    "affine",
    "atbash",
    "substitution",
    "rot13"
)

for _n in _names:
    try:
        mod = __import__(f"{__name__}.{_n}", fromlist=[_n])
        globals()[_n] = mod
    except Exception:
        pass

__all__ = [n for n in _names if n in globals()]
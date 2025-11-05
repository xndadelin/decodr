_names = (
    "polybius",
    "bazeries",
    "bifid",
    "four_square",
    "nihilist",
    "trifid",
    "adfgx"
)

for _n in _names:
    try:
        mod = __import__(f"{__name__}.{_n}", fromlist=[_n])
        globals()[_n] = mod
    except Exception:
        pass

__all__ = [n for n in _names if n in globals()]
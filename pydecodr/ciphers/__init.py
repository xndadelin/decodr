for _name in ("classical", "fractionation", "modern", "polyalphabetic", "stream", "rotor"):
    try:
        mod = __import__(f"{__name__}.{_name}", fromlist=[_name])
        globals()[_name] = mod
    except Exception:
        pass

__all__ = [k for k in ("classical", "fractionation", "modern", "polyalphabetic", "stream", "rotor") if k in globals]
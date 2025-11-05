"""pydecodr - core package."""

from importlib.metadata import version, PackageNotFoundError

__all__ = [
    "__version__",
    "__description__",
    "encode",
    "decode",
    "encrypt",
    "decrypt",
    "detect"
]

__description__ = "pydecodr - a modular CTF/crypto CLI toolkit for encodings, classic ciphers, and autodetection."

try:
    __version__ = version("pydecodr")
except PackageNotFoundError:
    __version__ = "0.1.0"

try:
    from .api import encode, decode, detect, encrypt, decrypt
except ImportError as e:
    raise ImportError(
        "pydecodr.api not found. Make sure 'src/pydecodr/api.py' exists."
    ) from e

for _name in ("ciphers", "encodings"):
    try:
        mod = __import__(f"{__name__}.{_name}", fromlist=[_name])
        globals()[_name] = mod
    except Exception:
        pass
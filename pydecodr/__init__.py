"""decodr - core package."""

from importlib.metadata import version, PackageNotFoundError

__all__ = [
    "__version__",
    "__description__",
    "encode",
    "decode",
    "detect"
]

__description__ = "decodr - a modular CTF/crypto CLI toolkit for encodings, classic ciphers, and autodetection."

try:
    __version__ = version("decodr")
except PackageNotFoundError:
    __version__ = "0.1.0"

try:
    from .api import encode, decode, detect
except ImportError as e:
    raise ImportError(
        "decodr.api not found. Make sure 'src/decodr/api.py' exists."
    ) from e
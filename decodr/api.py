"""
decodr.api - high-level interface.

This module provides a unified interface for encoding, decoding, and
autodetection across all submodules of the decodr package.
"""

from __future__ import annotations

from typing import Any, Optional
from importlib import import_module

ENCODING_MAP = {
    "base64": "decodr.encodings.base64_mod",
    "base32": "decodr.encodings.base32_mod",
    "hex": "decodr.encodings.hex_mod",
    "caesar": "decodr.ciphers.classical.caesar",
    "rot13": "decodr.ciphers.classical.rot13",
    "atbash": "decodr.ciphers.classical.atbash",
    "vignere": "decodr.ciphers.polyalphabetic.vignere"
    # im gonna add more as they are implemented one by one
}

def __load_module(scheme: str):
    if scheme not in ENCODING_MAP:
        raise ValueError(f"Unsupported scheme: {scheme}")
    module_path = ENCODING_MAP[scheme]
    return import_module(module_path)

def encode(scheme: str, text: str, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "encode", getattr(mod, "encrypt", None))
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no encode/encrypt function.")
    return fn(text, **kwargs)

def decode(scheme: str, text: str, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "decode", getattr(mod, "decrypt", None))
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no decode/decrypt function.")
    return fn(text, **kwargs)

def detect(text: str, limit: int = 5) -> list[dict[str, str]]:
    from decodr.detectors.autodetect import try_decode_candidates
    candidates = try_decode_candidates(text, limit=limit)
    return [
        {
            "scheme": name,
            "result": decoded,
            "score": f"{score:.2f}"
        } for name, decoded, score in candidates
    ]

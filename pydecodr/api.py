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
    "url": "decodr.encodings.url_mod",

    "caesar": "decodr.ciphers.classical.caesar",
    "atbash": "decodr.ciphers.classical.atbhas",
    "affine": "decodr.ciphers.classical.affine",
    "rot13": "decodr.ciphers.classical.rot13",
    "substitution": "decodr.ciphers.classical.substitution",

    "vigenere": "decodr.ciphers.polyalphabetic.vignere",
    "autokey_vignere": "decodr.ciphers.polyalphabetic.autokey_vigenere",
    "beaufort": "decodr.ciphers.polyalphabetic.beaufort",
    "playfair": "decodr.ciphers.polyalphabetic.playfair",

    "bifid": "decodr.ciphers.fractionation.bifid",
    "adfgx": "decodr.ciphers.fractionation.adfgx",

    "railfence": "decodr.ciphers.transposition.railfence",
    "columnar": "decodr.ciphers.transposition.columnar",

    "xor": "decodr.ciphers.stream.xor",
    "repeating_xor": "decodr.ciphers.stream.repeating_xor",
    "rc4": "decodr.ciphers.stream.rc4",

    "enigma": "decodr.ciphers.rotor.enigma",

    "aes": "decodr.ciphers.modern.aes",
    "rsa": "decodr.ciphers.modern.rsa",
    "hashes": "decodr.ciphers.modern.hashes",

    "fmt": "decodr.utils.fmt",
    "ioutils": "decodr.utils.ioutils"
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
    from pydecodr.detectors.autodetect import try_decode_candidates
    candidates = try_decode_candidates(text, limit=limit)
    return [
        {
            "scheme": name,
            "result": decoded,
            "score": f"{score:.2f}"
        } for name, decoded, score in candidates
    ]

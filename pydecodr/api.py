"""
pydecodr.api - high-level interface.

This module provides a unified interface for encoding, decoding, and
autodetection across all submodules of the pydecodr package.
"""

from __future__ import annotations

from typing import Any
from importlib import import_module

ENCODING_MAP = {
    "base64": "pydecodr.encodings.base64_mod",
    "base32": "pydecodr.encodings.base32_mod",
    "hex": "pydecodr.encodings.hex_mod",
    "url": "pydecodr.encodings.url_mod",

    "caesar": "pydecodr.ciphers.classical.caesar",
    "atbash": "pydecodr.ciphers.classical.atbash",
    "affine": "pydecodr.ciphers.classical.affine",
    "rot13": "pydecodr.ciphers.classical.rot13",
    "substitution": "pydecodr.ciphers.classical.substitution",

    "vigenere": "pydecodr.ciphers.polyalphabetic.vigenere",
    "autokey_vignere": "pydecodr.ciphers.polyalphabetic.autokey_vigenere",
    "beaufort": "pydecodr.ciphers.polyalphabetic.beaufort",
    "playfair": "pydecodr.ciphers.polyalphabetic.playfair",

    "bifid": "pydecodr.ciphers.fractionation.bifid",
    "adfgx": "pydecodr.ciphers.fractionation.adfgx",

    "railfence": "pydecodr.ciphers.transposition.railfence",
    "columnar": "pydecodr.ciphers.transposition.columnar",

    "xor": "pydecodr.ciphers.stream.xor",
    "repeating_xor": "pydecodr.ciphers.stream.repeating_xor",
    "rc4": "pydecodr.ciphers.stream.rc4",

    "enigma": "pydecodr.ciphers.rotor.enigma",

    "aes": "pydecodr.ciphers.modern.aes",
    "rsa": "pydecodr.ciphers.modern.rsa",
    "hashes": "pydecodr.ciphers.modern.hashes",

    "fmt": "pydecodr.utils.fmt",
    "ioutils": "pydecodr.utils.ioutils"
}

def __load_module(scheme: str):
    if scheme not in ENCODING_MAP:
        raise ValueError(f"Unsupported scheme: {scheme}")
    module_path = ENCODING_MAP[scheme]
    return import_module(module_path)

def encode(scheme: str, text: str, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "encode")
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no encode function.")
    return fn(text, **kwargs)

def decode(scheme: str, text: str, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "decode")
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no decode function.")
    return fn(text, **kwargs)

def encrypt(scheme: str, text: str, /, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "encrypt")
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no encrypt function.")
    return fn(text, **kwargs)
    

def decrypt(scheme: str, text: str, /, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "decrypt")
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no decrypt function.")
    return fn(text, **kwargs)

def crack(scheme: str, text: str, /, **kwargs: Any) -> str:
    mod = __load_module(scheme)
    fn = getattr(mod, "crack")
    if fn is None:
        raise AttributeError(f"Module '{mod.__name__}' has no crack function.")
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

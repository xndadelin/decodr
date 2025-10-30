"""
decodr.detectors.autodetect - heuristic detector for encodings
"""

from __future__ import annotations
import base64 
import binascii
import re
from typing import Optional, List, Dict
from pydecodr.utils.fmt import _printable_ratio

def is_hex(s: str) -> bool:
    return bool(re.fullmatch(r"[0-9A-Fa-f]+", s)) and len(s) % 2 == 0

def is_base_64(s: str) -> bool:
    if len(s) % 4 != 0:
        return False
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False
    
def is_base32(s: str) -> bool:
    try:
        base64.b32decode(s)
        return True
    except Exception:
        return False

def is_url_encoded(s: str) -> bool:
    return "%" in s and re.search(r"%[0-9A-Fa-f]{2}", s) is not None

def detect_type(data: str) -> Dict[str, Optional[str]]:
    data = data.strip()
    if not data:
        return {
            "type": "None",
            "confidence": 0.0
        }
    
    if is_hex(data):
        return {
            "type": "hex",
            "confidence": 0.95
        }
    
    if is_base_64(data):
        return {
            "type": "base64",
            "confidence": 0.9
        } 
    if is_base32(data):
        return {
            "type": "base_32",
            "confidence": 0.85
        }
    if is_url_encoded(data): 
        return {
            "type": "url-encoded",
            "confidence": 0.8
        }
    
    try:
        ratio = _printable_ratio(data.encode("utf-8", "ignore"))
    except Exception:
        ratio = 0.0
    
    if ratio > 0.9:
        return {
            "type": "plaintext",
            "confidence": "ratio"
        }
    elif ratio < 0.3:
        return {
            "type": "ciphertext",
            "confidence": 0.5
        }
    else: 
        return {
            "type": "unknown",
            "confidence": ratio
        }
    
if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.detectors.autodetect <string>\n"
    )

    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    s = sys.argv[1]
    try:
        result = detect_type(s)
        print(f"Detected: {result['type']} (confidence {result['confidence']:.2f})")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

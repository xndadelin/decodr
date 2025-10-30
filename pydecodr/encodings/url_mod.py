"""
decodr.encodings.url_mod - URL encoding helpers.

This module just implements encode/decode for URL-safe percent-encoding.
https://datatracker.ietf.org/doc/html/rfc3986
"""

from __future__ import annotations
from urllib.parse import quote, unquote

def encode(text: str, safe: str = '/') -> str:
    return quote(text, safe=safe)

def decode(text: str) -> str:
    return unquote(text)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 -m decodr.encodings.url_mode <encode|decode> <text>")
        sys.exit(1)

    cmd, text = sys.argv[1], sys.argv[2]

    try:
        if cmd == 'encode':
            print(encode(text))
        elif cmd == "decode":
            print(decode(text))
        else:
            print("Error: Unknown command. Use 'encode' or 'decode'.")
    except Exception as e:
        print(f"Error: {e}")


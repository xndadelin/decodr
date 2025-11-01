"""
pydecodr.encodings.url_mod - URL encoding helpers.

This module just implements encode/decode for URL-safe percent-encoding.
https://datatracker.ietf.org/doc/html/rfc3986
"""

from __future__ import annotations
from urllib.parse import quote, unquote
import sys
import argparse

def encode(text: str, safe: str = '/') -> str:
    return quote(text, safe=safe)

def decode(text: str) -> str:
    return unquote(text)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.encodings.url_mod",
        description="URL encoding/decoding utility"
    )

    p.add_argument("action", choices=["encode", "decode"], help="action to perform")
    p.add_argument("text", help="text to encode or decode (quote if contains spaces)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text

    try:
        if action == "encode":
            print(encode(text))
            sys.exit(0)
        elif action == "decode":
            print(decode(text))
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


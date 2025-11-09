"""
pydecodr.encodings.base85 - Base85 encoder and decodr
"""

from __future__ import annotations
import sys
import argparse
import base64

def encode(text: str) -> str:
    return base64.a85encode(text.encode()).decode()

def decode(text: str) -> str:
    return base64.a85decode(text.encode()).decode()

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.encodings.base85",
        description="Base 85 encoder and decoder"
    )

    p.add_argument("action", choices=["encode", "decode"], help="action to perform")
    p.add_argument("text", help="text to encode/decode (quote if contains spaces)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.action == "encode":
            print(encode(args.text))
        elif args.action == "decode":
            print(decode(args.text))
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
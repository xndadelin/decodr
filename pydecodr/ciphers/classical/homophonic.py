"""
pydecodr.ciphers.classical.homophonic - homophonic substitution cipher
"""

from __future__ import annotations
import sys
import argparse
import json
import random
from typing import Dict, List

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DEFAULT_MAPPING: Dict[str, List[int]] = {
    ch: list(range(100 + i * 3, 100 + i * 3 + 3)) for i, ch in enumerate(ALPHABET)
}

def encrypt(plaintext: str, mapping: Dict[str, List[int]] = DEFAULT_MAPPING, sep: str = " ") -> str:
    plaintext = plaintext.upper()
    out = []
    for ch in plaintext:
        if ch in mapping:
            out.append(str(random.choice(mapping[ch])))
        elif ch == " ":
            out.append("/")
    return sep.join(out)

def decrypt(ciphertext: str, mapping: Dict[str, List[int]] = DEFAULT_MAPPING, sep: str = " ") -> str:
    inverse: Dict[str, str] = {}
    for letter, nums in mapping.items():
        for n in nums:
            inverse[str(n)] = letter
    
    parts = ciphertext.replace("/", " / ").split(sep)
    out = []
    for part in parts:
        if part == "/":
            out.append(" ")
        elif part in inverse:
            out.append(inverse[part])
        else:
            continue

    return "".join(out)

def load_mapping_from_json(path: str) -> Dict[str, List[int]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = {}
    for k, v in data.items():
        mapping[k.upper()] = [int(x) for x in v]
    return mapping

def _build_argparse() -> argparse.ArgumentParser:
    example_json = """Example mapping JSON:
{
    "A": [11, 12, 13],
    "B": [21, 22],
    "C": [23],
    "D": [24, 25],
    ...
}
"""
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.classical.homophonic",
        description="Homophonic substitution cipher.\n"
                    "Each letter can map to multiple numeric codes\n"
                    f"{example_json}",
        formatter_class=argparse.RawTextHelpFormatter
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext")
    p.add_argument("--map-file", default=None, help="path to custom mapping JSON file")
    p.add_argument("--sep", default=" ", help="separator between symbols")
    p.add_argument("--seed", type=int, default=None, help="random seed for deterministic encryption output")

    return p

if __name__ == "__main__":
    parser = _build_argparse()
    args = parser.parse_args(sys.argv[1:])
    try:
        mapping = load_mapping_from_json(args.map_file) if args.map_file else DEFAULT_MAPPING
        if args.seed is not None:
            random.seed(args.seed)
        
        if args.action == "encrypt":
            print(encrypt(args.text, mapping=mapping, sep=args.sep))
        elif args.action == "decrypt":
            print(decrypt(args.text, mapping=mapping, sep=args.sep))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
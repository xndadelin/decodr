"""
pydecodr.ciphers.fractionation.polybius - polybius square cipher (5x5)
"""

from __future__ import annotations

import argparse
import sys
import re
from typing import List, Tuple, Dict, Optional

ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
ALPHABET_FULL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _clean_plaintext(s: str, j_as_i: bool) -> str:
    s = s.upper()
    letters = []
    for ch in s:
        if ch.isalpha():
            if j_as_i and ch == "J":
                letters.append("I")
            else:
                letters.append(ch)
    return "".join(letters)

def _build_square(keyword: Optional[str], j_as_i: bool) -> List[List[str]]:
    used: List[str] = []
    if keyword:
        for ch in keyword.upper():
            if not ch.isalpha():
                continue
            if j_as_i and ch == "J":
                ch = "I"
            if ch not in used:
                used.append(ch)

    base = ALPHABET if j_as_i else ALPHABET_FULL
    for ch in base:
        if j_as_i and ch == "J":
            continue
        if ch not in used:
            used.append(ch)

    if len(used) > 25:
        if "J" in used:
            used.remove("J")
        else:
            used = used[:25]

    square: List[List[str]] = []
    for i in range(5):
        row = used[i * 5 : (i + 1) * 5]
        square.append(row)

    return square

def _square_mappings(
        square: List[List[str]]
) -> Tuple[Dict[str, Tuple[int, int]], Dict[Tuple[int, int], str]]:
    letter_to_cord: Dict[str, Tuple[int, int]] = {}
    coord_to_letter: Dict[Tuple[int, int], str] = {}
    for r in range(5):
        for c in range(5):
            letter = square[r][c]
            coord = (r + 1, c + 1)
            letter_to_cord[letter] = coord
            coord_to_letter[coord] = letter
    return letter_to_cord, coord_to_letter

def encrypt(plaintext: str, j_as_i: bool = True, numeric_output: bool = True, separator: str = " ", keyword: Optional[str] = None) -> str:
    clean = _clean_plaintext(plaintext, j_as_i)
    square = _build_square(keyword, j_as_i)
    l2c, _ = _square_mappings(square)

    out: List[str] = []
    for ch in clean:
        if ch not in l2c:
            if ch == "J" and j_as_i:
                coord = l2c.get("I")
                if coord is None:
                    continue
            else:
                continue
        else:
            coord = l2c[ch]
        if numeric_output:
            out.append(f"{coord[0]}{coord[1]}")
        else:
            out.append(square[coord[0]- 1][coord[1] - 1])
    
    return " ".join(out) 

def _parse_numeric_pairs(s: str) -> List[Tuple[int, int]]:
    pairs = re.findall(r"([1-5])\s*([1-5])", s)
    if pairs:
        return [(int(a), int(b)) for a, b in pairs]
    compact = re.sub(r"\D", "", s)
    if len(compact) % 2 != 0:
        compact = compact[:-1]
    res: List[Tuple[int, int]] = []
    for i in range(0, len(compact), 2):
        a = int(compact[i])
        b = int(compact[i + 1])
        if 1 <= a <= 5 and 1 <= b <= 5:
            res.append((a, b))
    return res

def decrypt(ciphertext: str, j_as_i: bool = True, numeric_input: bool = True, separator: str = " ", keyword: Optional[str] = None) -> str:
    square = _build_square(keyword, j_as_i)
    _, c2l = _square_mappings(square)

    if numeric_input:
        pairs = _parse_numeric_pairs(ciphertext)
        letters: List[str] = []
        for coord in pairs:
            letter = c2l.get(coord)
            if letter:
                letters.append(letter)
        return "".join(letters)
    else:
        return _clean_plaintext(ciphertext, j_as_i)
    
def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.fractionation.polybius",
        description="Polybius 5x5 cipher",
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action")
    p.add_argument("text", help="text (quote if contains spaces)")
    p.add_argument("--no-j-as-i", dest="j_as_i", action="store_false", help="do not MERGE J into I")
    p.add_argument("--no-numeric", dest="numeric", action="store_false", help="encrypt: output letters; decrypt: treat input as letters")
    p.add_argument("--sep", default=" ", help="separator for numeric pairs (default: space)")
    p.add_argument("--keyword", default=None, help="optional keyword for keyed square")

    return p

    
if __name__ == "__main__":

    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    j_as_i = bool(args.j_as_i)
    numeric = bool(args.numeric)
    sep = args.sep
    keyword = args.keyword

    if action == "encrypt":
        print(encrypt(text, j_as_i=j_as_i, numeric_output=numeric, separator=sep, keyword=keyword))
        sys.exit(0)
    
    if action == "decrypt":
        print(decrypt(text, j_as_i=j_as_i, numeric_input=numeric, separator=sep, keyword=keyword))
        sys.exit(0)

    parser.print_help()
    sys.exit(1)
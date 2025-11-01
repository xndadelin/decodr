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
            used.remove(25)
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

def encript(plaintext: str, j_as_i: bool = True, numeric_output: bool = True, separator: str = " ", keyword: Optional[str] = None) -> str:
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

def _parse_numeric_pairs(s: str) -> List[Tuple[int, int]]:
    pairs = re.findall(r"([1-5]\s*([1-5]))", s)
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
        return "".join(letter)
    else:
        return _clean_plaintext(ciphertext, j_as_i)
"""
pydecodr.ciphers.fractionation.bifid - bifid cipher (polybius + fractionation)
"""

from __future__ import annotations
from typing import List, Tuple
import sys
import argparse

ALPHABET_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def _normalize_text(s: str) -> List[Tuple[int, str]]:
    letters: List[str] = []
    mask: List[Tuple[int, str]] = []
    li = 0

    for ch in s:
        if ch.isalpha():
            up = ch.upper()
            if up == "J":
                up = "I"
            letters.append(up)
            mask.append((li, ""))
            li += 1
        else:
            mask.append((-1, ch))
    return letters, mask

def _reinsert_nonletters(proc_letters: List[str], mask: List[Tuple[int, str]]) -> str:
    out: List[str] = []
    for idx, ch in mask:
        if idx == -1:
            out.append(ch)
        else:
            out.append(proc_letters[idx])
    
    return "".join(out)

def _build_square(key: str | None) -> List[List[str]]:
    seen = set()
    seq = []
    if key:
        for ch in key.upper():
            if ch.isalpha():
                ch = "I" if ch == "J" else ch
                if ch not in seen and ch in ALPHABET_25:
                    seen.add(ch)
                    seq.append(ch)
    
    for ch in ALPHABET_25:
        if ch not in seen:
            seq.append(ch)
    
    return [seq[i: i + 5] for i in range(0, 25, 5)]

def _coord_map(square: List[List[str]]):
    pos = {}
    for r in range(5):
        for c in range(5):
            pos[square[r][c]] = (r + 1, c + 1)
    return pos

def _letter_from_coords(square: List[List[str]], r: int, c: int) -> str:
    return square[r - 1][c - 1]

def _fractionate(rows: List[int], cols: List[int], period: int) -> Tuple[List[int], List[int]]:
    out_rows: List[int] = []
    out_cols: List[int] = []
    n = len(rows)
    i = 0
    while i < n:
        block_r = rows[i: i + period]
        block_c = cols[i: i + period]
        combined = block_r + block_c

        out_rows.extend(combined[: len(block_r)])
        out_cols.extend(combined[len(block_r) :])
        i += period

    return out_rows, out_cols

def encrypt(plaintext: str, key: str | None = None, period: int = 5) -> str:
    if period <= 0:
        raise ValueError("period must be >=1")
    
    letters, mask = _normalize_text(plaintext)
    if not letters:
        return plaintext

    square = _build_square(key)
    pos = _coord_map(square)

    rows: List[int] = []
    cols: List[int] = []
    for ch in letters:
        r, c = pos[ch]
        rows.append(r)
        cols.append(c)

    out_letters: List[str] = []
    n = len(letters)
    i = 0
    while i < n:
        blk_len = min(period, n - i)
        r_block = rows[i: i + blk_len]
        c_block = cols[i: i + blk_len]
        combined = r_block + c_block
        for j in range(0, 2 * blk_len, 2):
            rr = combined[j]
            cc = combined[j + 1]
            out_letters.append(_letter_from_coords(square, rr, cc))
        i += blk_len

    return _reinsert_nonletters(out_letters, mask)

def decrypt(ciphertext: str, key: str | None = None, period: int = 5) -> str:
    if period <= 0:
        raise ValueError("period must be >=1")
    
    letters, mask = _normalize_text(ciphertext)
    if not letters:
        return ciphertext

    square = _build_square(key)
    pos = _coord_map(square)

    rows: List[int] = []
    cols: List[int] = []
    for ch in letters:
        r, c = pos[ch]
        rows.append(r)
        cols.append(c)

    seq: List[int] = []
    for ch in letters:
        r, c = pos[ch]
        seq.extend([r, c])

    out_letters: List[str] = []
    n = len(letters)
    i = 0
    p = 0
    while i < n:
        blk_len = min(period, n - i)
        block = seq[p : p + 2 * blk_len]
        r_block = block[:blk_len]
        c_block = block[blk_len:]
        for j in range(blk_len):
            out_letters.append(_letter_from_coords(square, r_block[j], c_block[j]))
        
        p += 2 * blk_len
        i += blk_len

    return _reinsert_nonletters(out_letters, mask)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.fractionation.bifid",
        description="Bifid cipher"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or cipher text (quote if contains spaces)")
    p.add_argument('--key', default=None, help="optional Polybius key (default: None)")
    p.add_argument("--period", type=int, default=5, help="period for fractionation (default: 5)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    key = args.key
    period = args.period 

    try:
        if action == "encrypt":
            print(encrypt(text, key=key, period=period))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, key=key, period=period))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
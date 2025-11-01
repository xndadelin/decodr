"""
pydecodr.ciphers.fractionation.adfgx - ADFGX cipher
"""

from __future__ import annotations
from typing import Dict, List, Tuple
import sys
import argparse

ADFGX = "ADFGX"
ALPHABET_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def _normalize_letters(s: str) -> List[str]:
    out: List[str] = []
    for ch in s.upper():
        if ch.isalpha():
            out.append("I" if ch == "J" else ch) 
    return out

def _build_square(key: str | None) -> List[List[str]]:
    seen = set()
    seq: List[str] = []
    if key:
        for ch in _normalize_letters(key):
            if ch not in seen and ch in ALPHABET_25:
                seen.add(ch)
                seq.append(ch)
    for ch in ALPHABET_25:
        if ch not in seen:
            seq.append(ch)
    
    return [seq[i: i + 5] for i in range(0, 25, 5)]

def _coords_map(square: List[List[str]]) -> tuple[Dict[str, Tuple[int, int]], Dict[Tuple[int, int], str]]:
    pos: Dict[str, Tuple[int, int]] = {}
    rev: Dict[Tuple[int, int], str] = {}
    for r in range(5):
        for c in range(5):
            ch = square[r][c]
            pos[ch] = (r, c)
            rev[(r, c)] = ch
    return pos, rev

def _polybius_encode(letters: List[str], square_key: str | None) -> str:
    square = _build_square(square_key)
    pos, _ = _coords_map(square)
    out: List[str] = []
    for ch in letters:
        r, c = pos[ch]
        out.append(ADFGX[r])
        out.append(ADFGX[c])

    return "".join(out)

def _polybius_decode(digrams: str, square_key: str | None) -> List[str]:
    if len(digrams) % 2 != 0:
        raise ValueError("ADFGX stream length must be even")
    square = _build_square(square_key)
    _, rev = _coords_map(square)
    sym_index = {
        sym: i for i, sym in enumerate(ADFGX)
    }
    out: List[str] = []
    for i in range(0, len(digrams), 2):
        r = sym_index[digrams[i]]
        c = sym_index[digrams[i + 1]]
        out.append(rev[(r, c)])
    return out

def _key_order(key: str) -> List[int]:
    indexed = list(enumerate(key))
    sorted_cols = sorted(indexed, key=lambda t:(t[1].upper(), t[0]))
    return [i for i, _ in sorted_cols]

def _chunks(s: str, n: int) -> List[str]:
    return [s[i: i + n] for i in range(0, len(s), n)]

def _columnar_encrypt(stream: str, key: str, pad: str | None = "X") -> str:
    if not key:
        raise ValueError("Transposition key cannot be empty.")
    ncols = len(key)
    rows = _chunks(stream, ncols)
    if pad is not None and rows and len(rows[-1]) < ncols:
        rows[-1] = rows[-1] + pad[0] * (ncols - len(rows[-1]))
    order = _key_order(key)
    out: List[str] = []
    for col in order:
        for r in rows:
            if col < len(r): 
                out.append(r[col])
    return "".join(out)

def _columnar_decypt(stream: str, key: str, pad: str | None = "X") -> str:
    if not key:
        raise ValueError("Transposition key cannot be empty.")
    n = len(stream)
    ncols = len(key)
    if ncols == 0:
        return stream
    order = _key_order(key)
    nrows = (n + ncols - 1) // ncols

    if pad is not None:
        col_lengths = [nrows] * ncols
    else:
        full_in_last_row = n % col_lengths
        if full_in_last_row == 0 and n > 0:
            full_in_last_row = ncols
        col_lengths: List[int] = []
        for idx_in_order in range(ncols):
            length = nrows if idx_in_order < full_in_last_row else max(nrows - 1, 0)
            col_lengths.append(length)

    cols: List[str] = []
    p = 0
    for length in col_lengths:
        cols.append(stream[p: p + length])
        p += length

    col_map ={
        order[i]: cols[i] for i in range(ncols)
    }

    rows: List[List[str]] = [[""] * ncols for _ in range(nrows)]
    ptr = {
        c: 0 for c in range(ncols)
    }
    for r in range(nrows):
        for c in range(ncols):
            col_str = col_map.get(c, "")
            q = ptr[c]
            if q < len(col_str):
                rows[r][c] = col_str[q]
                ptr[c] = q + 1

    return "".join(ch for row in rows for ch in row if ch)

def encrypt(plaintext: str, square_key: str | None, trans_key: str, pad: str | None = "X") -> str:
    letters = _normalize_letters(plaintext)
    if not letters:
        return ""
    adfgx_stream = _polybius_encode(letters, square_key)
    return _columnar_encrypt(adfgx_stream, trans_key, pad=pad)

def decrypt(ciphertext: str, square_key: str | None, trans_key: str, pad: str | None = "X") -> str:
    if not ciphertext:
        return ""
    adfgx_only = "".join(ch for ch in ciphertext.upper() if ch in ADFGX)
    inter = _columnar_decypt(adfgx_only, trans_key, pad=pad)
    letters = _polybius_decode(inter, square_key)
    return "".join(letters)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='pydecodr.ciphers.fractionation.adfgx',
        description="ADFGX cipher"
    )

    p.add_argument('action', choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument('text', help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument("square_key", help='Polybius square keyword (use "-" for default)')
    p.add_argument('trans_key', help="transposition key")
    p.add_argument('--pad', default="X", help="padding character (default: X)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    square_key = None if args.square_key == "-" else args.square_key
    trans_key = args.trans_key
    pad = args.pad[0].upper() if args.pad else "X"

    try:
        if action == "encrypt":
            print(encrypt(text, square_key, trans_key, pad=pad))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, square_key, trans_key, pad=pad))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
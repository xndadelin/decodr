"""
pydecodr.ciphers.fractionation.adfgvx - ADFGVX cipher (6x6)
"""

from __future__ import annotations
from typing import Dict, List, Tuple
import sys
import argparse

ADFGVX = "ADFGVX"
ALPHABET_36 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def _normalize_alnum_36(s: str) -> List[str]:
    out: List[str] = []
    for ch in s.upper():
        if ch.isalnum():
            out.append(ch)
    return out

def _build_square(key: str | None) -> List[List[str]]:
    seen = set()
    seq: List[str] = []
    if key:
        for ch in _normalize_alnum_36(key):
            if ch not in seen and ch in ALPHABET_36:
                seen.add(ch)
                seq.append(ch)
    for ch in ALPHABET_36:
        if ch not in seen:
            seen.add(ch)
            seq.append(ch)
    return [seq[i: i + 6] for i in range(0, 36, 6)]

def _coords(square: List[List[str]]) -> tuple[Dict[str, Tuple[int, int]], Dict[Tuple[int, int], str]]:
    pos: Dict[str, Tuple[int, int]] = {}
    rev: Dict[Tuple[int, int], str] = {}
    for r in range(6):
        for c in range(6):
            ch = square[r][c]
            pos[ch] = (r, c)
            rev[(r, c)] = ch
    return pos, rev

def _polybius_encode(chars: List[str], square_key: str | None) -> str:
    square = _build_square(square_key)
    pos, _ = _coords(square)
    out: List[str] = []
    for ch in chars:
        r, c = pos[ch]
        out.append(ADFGVX[r])
        out.append(ADFGVX[c])
    return "".join(out)

def _polybius_decode(digrams: str, square_key: str | None) -> List[str]:
    if len(digrams) % 2 != 0:
        raise ValueError("ADFGVX stream lenght must be even.")
    square = _build_square(square_key)
    _, rev = _coords(square)
    sym_index = {
        sym: i for i, sym in enumerate(ADFGVX)
    }
    out: List[str] = []
    for i in range(0, len(digrams), 2):
        r = sym_index[digrams[i]]
        c = sym_index[digrams[i+1]]
        out.append(rev[(r, c)])
    return out

def _key_order(key: str) -> List[int]:
    if not key:
        raise ValueError("Transposition key cannot be empty.")
    indexed = list(enumerate(key))
    sorted_cols = sorted(indexed, key=lambda t: (t[1].upper(), t[0]))
    return [i for i, _ in sorted_cols]

def _chunks(s: str, n: int) -> List[str]:
    return [s[i: i + n] for i in range(0, len(s), n)]

def _columnar_encrypt(stream: str, key: str, pad: str | None = "X") -> str:
    if not key:
        raise ValueError("Transposition key cannot be empty.")
    ncols = len(key)
    rows = _chunks(stream, ncols)

    if pad is not None and rows:
        pads_needed = (ncols - len(rows[-1])) % ncols
        if pads_needed:
            rows[-1] = rows[-1] + pad[0] * pads_needed
    
    order = _key_order(key)
    out: List[str] = []
    for col in order:
        for r in rows:
            if col < len(r):
                out.append(r[col])
    return "".join(out)

def _columnar_decrypt(stream: str, key: str, pad: str | None = "X") -> str:
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
        full_in_last_rows = n % ncols
        if full_in_last_rows == 0 and n > 0:
            full_in_last_rows = ncols
        col_lengths: List[int] = []
        for idx_in_order in range(ncols):
            length = nrows if idx_in_order < full_in_last_rows else max(nrows - 1, 0)
            col_lengths.append(length)
    
    cols: List[str] = []
    p = 0
    for length in col_lengths:
        cols.append(stream[p: p + length])
        p += length

    col_map = {
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
    out = "".join(ch for row in rows for ch in row if ch)
    if pad is not None and out:
        pch = pad[0]
        i = len(out) - 1
        while i >= 0 and out[i] == pch:
            i -= 1
        out = out[:i+1]

    return out

def encrypt(plaintext: str, square_key: str | None, trans_key: str, pad: str | None = "X") -> str:
    chars = _normalize_alnum_36(plaintext)
    if not chars:
        return ""
    adfgvx_stream = _polybius_encode(chars, square_key)
    ct =  _columnar_encrypt(adfgvx_stream, trans_key, pad=pad)
    return ct

def decrypt(ciphertext: str, square_key: str | None, trans_key: str, pad: str | None = "X") -> str:
    if not ciphertext:
        return ""
    adfgvx_only = "".join(ch for ch in ciphertext.upper() if ch in ADFGVX)
    inter = _columnar_decrypt(adfgvx_only, trans_key, pad=pad)
    letters = _polybius_decode(inter, square_key)
    return "".join(letters)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.fractionation.adfgvx",
        description="ADFGVX cipher (6x6)"
    )

    p.add_argument('action', choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument("square_key", help='6x6 square keyword (use "-" for default)')
    p.add_argument("trans_key", help="transposition key")
    p.add_argument("--pad", default="X", help="padding character (default: X)")

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
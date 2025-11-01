"""
pydecodr.ciphers.transposition.columnar - columnar transposition cipher
"""

from __future__ import annotations
from typing import List
import sys
import argparse

def _key_order(key: str) -> List[int]:
    indexed = list(enumerate(key))
    sorted_cols = sorted(indexed, key=lambda t: (t[1].upper(), t[0]))
    return [i for i, _ in sorted_cols]

def _chunks(seq: str, n: int) -> List[str]:
    return [seq[i: i + n] for i in range(0, len(seq), n)]

def encrypt(plaintext: str, key: str, pad: str | None = None) -> str:
    if not key:
        raise ValueError("Key cannot be empty.")
    ncols = len(key)
    rows = _chunks(plaintext, ncols)

    if pad is not None and rows and len(rows[-1]) < ncols:
        rows[-1] = rows[-1] + pad[0] * (ncols - len(rows[-1]))

    order = _key_order(key)

    out_chars: List[str] = []
    for col in order:
        for r in rows:
            if col < len(r):
                out_chars.append(r[col])
    
    return "".join(out_chars)

def decrypt(ciphertext: str, key: str, pad: str | None = None) -> str:
    if not key:
        raise ValueError("Key cannot be empty.")
    ncols = len(key)
    n = len(ciphertext)
    if ncols == 0:
        return ciphertext
    
    order = _key_order(key)
    nrows = (n + ncols - 1) // ncols

    if pad is not None:
        col_lengths = [nrows] * ncols
    else:
        full_in_last_row = n % ncols
        if full_in_last_row == 0 and n > 0:
            full_in_last_row = ncols
        
        col_lengths: list[int] = []
        for idx_in_order in range(ncols):
            orig_col = order[idx_in_order]
            length = nrows if orig_col < full_in_last_row else max(nrows - 1, 0)
            col_lengths.append(length)
            
    cols_data: list[str] = []
    pos = 0
    for length in col_lengths:
        cols_data.append(ciphertext[pos: pos + length])
        pos += length
    
    col_map = {
        order[i]: cols_data[i] for i in range(ncols)
    }

    pointers = {
        c: 0 for c in range(ncols)
    }
    rows: list[list[str]] = [[""] * ncols for _ in range(nrows)]
    for r in range(nrows):
        for c in range (ncols):
            col_str = col_map.get(c, "")
            p = pointers[c]
            if p < len(col_str):
                rows[r][c] = col_str[p]
                pointers[c] = p + 1
            else:
                rows[r][c] = ""


    plaintext = "".join(ch for row in rows for ch in row if ch != "")
    return plaintext

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.transposition.columnar",
        description="Columnar transposition cipher.",
        epilog="If you used padding during encrypt, pass the some one during decrypt."
    )

    p.add_argument('action', choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertex (quote if contains spaces)")
    p.add_argument("key", help="transposition key (string)")
    p.add_argument("--pad", default=None, help="optional padding character (default: none)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    key = args.key
    pad = args.pad

    try:
        if action == "encrypt":
            print(encrypt(text, key, pad=pad))
            sys.exit(0)
        elif action == "decrypt":
            print(decrypt(text, key, pad=pad))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
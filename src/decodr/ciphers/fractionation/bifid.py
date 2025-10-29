"""
decodr.ciphers.fractionation.bifid - bifid cipher (polybius + fractionation)
"""

from __future__ import annotations
from typing import List, Tuple

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

    fr, fc = _fractionate(rows, cols, period)
    out_letters: List[str] = []
    for r, c in zip(fr, fc):
        out_letters.append(_letter_from_coords(square, r, c))

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

    n = len(rows)
    i = 0
    rec_rows: List[int] = []
    rec_cols: List[int] = []
    while i < n :
        blk_len = min(period, n - i)
        r_block = rows[i : i + blk_len]
        c_block = cols[i: i + blk_len]

        rec_rows.extend(r_block)
        rec_cols.extend(c_block)
        i += blk_len

    out_letters: List[str] = []
    for r, c in zip(rec_rows, rec_cols):
        out_letters.append(_letter_from_coords(square, r, c))

    return _reinsert_nonletters(out_letters, mask)

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys
    
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.fractionation.bifid encrypt <text> [key] [period]\n"
        "python3 -m decodr.ciphers.fractionation.bifid decrypt <text> [key] [period]\n"
    )

    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)
    
    cmd, text = sys.argv[1], sys.argv[2]
    key = sys.argv[3] if len(sys.argv) >= 4 else None
    period = int(sys.argv[4]) if len(sys.argv) >= 5 else 5

    try:
        if cmd in ("encrypt, decrypt"):
            print(encrypt(text, key=key, period=period))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, key=key, period=period))
        else:
            print("Unknown command. Use 'encrypt' or 'decrypt'.") 
            print(usage)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
"""
pydecodr.ciphers.fractionation.four_square - four square cipher
"""

from __future__ import annotations
import sys
import argparse

BASE = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def _is_alpha(ch: str) -> bool:
    return ("A" <= ch <= "Z") or ("a" <= ch <= "z")

def _to_I(ch: str) -> str:
    return "I" if ch.upper() == "J" else ch.upper()

def _clean_letter_keep_positions(s: str) -> tuple[str, list[tuple[int, str]]]:
    letters = []
    meta = []
    for i, ch in enumerate(s):
        if _is_alpha(ch):
            letters.append(_to_I(ch))
            meta.append((i, "lower" if ch.islower() else "upper"))
        else:
            meta.append((i, "non"))
    return "".join(letters), meta
 
def _mk_square(keyword: str) -> str:
    k = "".join(_to_I(ch) for ch in keyword if _is_alpha(ch))
    seen = set()
    out = []
    for ch in k + BASE:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)

def _pos(square: str, ch: str) -> tuple[int, int]:
    i = square.index(ch)
    return divmod(i, 5)

def _diagraphs(letters_only: str) -> list[tuple[str, str]]:
    t = letters_only
    if len(t) % 2 == 1:
        t += t[-1]
    return [(t[i], t[i+1]) for i in range(0, len(t), 2)]

def _apply_meta(original: str, letters_result: str, meta: list[tuple[int, str]]) -> str:
    res = list(original)
    it = iter(letters_result)
    for idx, kind in meta:
        if kind == "non":
            continue
        try:
            ch = next(it)
        except StopIteration:
            break
        res[idx] = ch.lower() if kind == "lower" else ch
    return "".join(res)

def encrypt(plaintext: str, key1: str, key2: str) -> str:
    TL = BASE
    BR = BASE
    TR = _mk_square(key1)
    BL = _mk_square(key2)

    letters, meta = _clean_letter_keep_positions(plaintext)
    if not letters:
        return plaintext
    
    pairs = _diagraphs(letters)
    out_letters = []
    for a, b in pairs:
        ra, ca = _pos(TL, a)
        rb, cb = _pos(BR, b)
        out_letters.append(TR[ra*5 + cb])
        out_letters.append(BL[rb*5 + ca])

    if len(letters) % 2 == 1:
        out_letters.pop(-2)

    return _apply_meta(plaintext, "".join(out_letters), meta)

def decrypt(ciphertext: str, key1: str, key2: str) -> str:
    TL = BASE
    BR = BASE
    TR = _mk_square(key1)
    BL = _mk_square(key2)

    letters, meta = _clean_letter_keep_positions(ciphertext)
    if not letters:
        return ciphertext

    pairs = _diagraphs(letters)    

    out_letters = []
    for a, b in pairs:
        ra, cb = _pos(TR, a)
        rb, ca = _pos(BL, b)
        out_letters.append(TL[ra*5 + ca])
        out_letters.append(BR[rb*5 + cb])

    needed = sum(1 for _, k in meta if k != "non")

    return _apply_meta(ciphertext, "".join(out_letters)[:needed], meta)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.fractionation.four_square",
        description="Four-Square cipher"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform"),
    p.add_argument("text", help="plaintext/ciphertext (quote if contains spaces)")
    p.add_argument("key1", help="key for the right-top square")
    p.add_argument("key2", help="key for left-bottom square")
    
    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.key1, args.key2))
        elif args.action == "decrypt":
            print(decrypt(args.text, args.key1, args.key2))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

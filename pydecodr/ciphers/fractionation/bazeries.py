"""
pydecodr.ciphers.fractionation.bazeries - bazeries cipher (polybius 5x5 with pairs inversion)
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

def _pair_for(square: str, ch: str) -> str:
    r, c = _pos(square, ch)
    return f"{r+1}{c+1}"

def _pairs_to_text(square: str, pairs: list[str]) -> str:
    out = []
    for p in pairs:
        if len(p) != 2:
            continue
        r = int(p[0]) - 1
        c = int(p[1]) - 1
        out.append(square[r*5 + c])
    return "".join(out)

def _to_pairs(square: str, letters: str) -> list[str]:
    return [_pair_for(square, ch) for ch in letters]

def _numkey_chuncks(numkey: str) -> list[int]:
    if not numkey or any(ch not in "0123456789" for ch in numkey):
        raise ValueError("The numeric key need to only contain numbers.")
    return [max(1, int(d)) for d in numkey]

def _reverse_by_group_on_pairs(pairs: list[str], chunk_sizes: list[int]) -> list[str]:
    if not pairs:
        return []
    out, i, j = [], 0, 0
    n, m = len(pairs), len(chunk_sizes)
    while i < n:
        size = chunk_sizes[j % m]
        chunk = pairs[i:i+size]
        out.extend(reversed(chunk))
        i += size
        j += 1
    return out

def _process(text: str, alpha_key: str, num_key: str) -> str:
    square = _mk_square(alpha_key)
    letters, meta = _clean_letter_keep_positions(text)
    if not letters:
        return text
    
    pairs = _to_pairs(square, letters)
    sizes = _numkey_chuncks(num_key)
    permuted = _reverse_by_group_on_pairs(pairs, sizes)
    result_letters = _pairs_to_text(square, permuted)

    return _apply_meta(text, result_letters, meta)

def encrypt(plaintext: str, alpha_key: str, num_key: str) -> str:
    return _process(plaintext, alpha_key, num_key)


def decrypt(ciphertext: str, alpha_key: str, num_key: str) -> str:
    return _process(ciphertext, alpha_key, num_key)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='pydecodr.ciphers.fractionation.bazeries',
        description="Bazeries cipher (polybius 5x5 with pairs inversion)"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext/ciphertext (quote if contains spaces)")
    p.add_argument("alpha_key", help="alphanumeric key (A-Z) for the Polybius square")
    p.add_argument("num_key", help="numerical key (0 is treated as 1)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.action == "encrypt":
            print(encrypt(args.text, args.alpha_key, args.num_key))
        elif args.action == "decrypt":
            print(decrypt(args.text, args.alpha_key, args.num_key))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
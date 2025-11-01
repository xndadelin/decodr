"""
pydecodr.ciphers.polyalphabetic.beaufort - classical beaufort cipher
C_i = (K_i - P_i) mod 26
"""

from __future__ import annotations
import sys
import argparse

def _char_to_idx(ch: str) -> int:
    return ord(ch.lower()) - ord("a")

def _shift_letter(pt_ch: str, k_ch: str) -> str:
    if not pt_ch.isalpha():
        return pt_ch
    p = _char_to_idx(pt_ch)
    k = _char_to_idx(k_ch)
    idx = (k - p) % 26 
    base = ord("A") if pt_ch.isupper() else ord("a")
    return chr(base + idx)

def transform(text: str, key: str) -> str:
    if not key:
        raise ValueError("Key cannot be empty")
    kletters = [c for c in key if c.isalpha()]
    if not kletters:
        raise ValueError("Key must contain at least one alphabetic character")
    
    out = []
    j = 0
    klen = len(kletters)
    for ch in text:
        if ch.isalpha():
            out.append(_shift_letter(ch, kletters[j % klen]))
            j += 1
        else:
            out.append(ch)
    
    return "".join(out)

def encrypt(plaintext: str, key: str) -> str:
    return transform(plaintext, key)

def decrypt(ciphertext: str, key: str) -> str:
    return transform(ciphertext, key)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.polyalphabetic.beaufort",
        description="Beaufort cipher"
    )

    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quotes if contains spaces)")
    p.add_argument("key", help="key (string)")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    action = args.action
    text = args.text
    key = args.key

    try:
        if action == "encrypt":
            print(encrypt(text, key))
            sys.exit(0)
        elif action == 'decrypt':
            print(decrypt(text, key))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


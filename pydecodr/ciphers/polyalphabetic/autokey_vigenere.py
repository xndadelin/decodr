"""
pydecodr.ciphers.polyalphabetic.autokey_vigenere - Autokey Vignere cipher

- the key is extended by appending the plaintext (for encryption) 
or the recovered plaintext (for decryption)
"""

from __future__ import annotations
import sys
import argparse

def _shift(ch: str, k: int, decrypt: bool = False) -> str:
    if not ch.isalpha():
        return ch
    base = ord("A") if ch.isupper() else ord("a")
    offset = -k if decrypt else k
    return chr((ord(ch) - base + offset) % 26 + base)

def _char_to_shift(ch: str) -> int:
    return ord(ch.lower()) - ord("a")

def encrypt(plaintext: str, key: str) -> str:
    if not key:
        raise ValueError('Key cannot be empty')
    
    key_stream = key
    result = []
    j = 0

    for ch in plaintext:
        if ch.isalpha():
            k = _char_to_shift(key_stream[j].lower())
            result.append(_shift(ch, k))
            j += 1
            key_stream += ch
        else:
            result.append(ch)

    return "".join(result)

def decrypt(ciphertext: str, key: str) -> str:
    if not key:
        raise ValueError('Key cannot be empty')
    
    key_stream = list(key)
    result = []
    j = 0

    for ch in ciphertext:
        if ch.isalpha():
            k = _char_to_shift(key_stream[j].lower())
            plain_ch = _shift(ch, k, decrypt=True)
            result.append(plain_ch)
            j += 1
            key_stream.append(plain_ch)
        else:
            result.append(ch)
            
    return "".join(result)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.polyalphabetic.autokey_vigenere",
        description="Autokey vigenere cipher"
    )
    p.add_argument("action", choices=["encrypt", "decrypt"], help="action to perform")
    p.add_argument("text", help="plaintext or ciphertext (quote if contains spaces)")
    p.add_argument("key", help="initial key (strings)")

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
        elif action == "decrypt":
            print(decrypt(text, key))
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
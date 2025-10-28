"""
decodr.ciphers.polyalphabetic.vigenere - Autokey Vignere cipher

- the key is extended by appending the plaintext (for encryption) 
or the recovered plaintext (for decryption)
"""

from __future__ import annotations

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
            result.append(_shift(ch, k), decrypt=True)
            j += 1
            key_stream.append(p)
        else:
            result.append(ch)
            
    return "".join(result)

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.polyalphabetic.autokey_vigenere encrypt <text> <key>\n"
        "python3 -m decodr.ciphers.polyalphabetic.autokey_vigenere decrypt <text> <key>\n"
    )

    if len(sys.argv) < 4:
        print(usage)
        sys.exit(1)
    
    cmd, text, key = sys.argv[1:4]

    try:
        if cmd in("encrypt", "encode"):
            print(encrypt(text, key))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, key))
        else:
            print("Unknown command. Use 'decrypt' or 'encrypt'.")
            print(usage)
    except Exception as e:
        print(f"Error {e}")
        sys.exit(1)


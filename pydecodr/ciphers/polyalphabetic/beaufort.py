"""
decodr.ciphers.polyalphabetic.beaufort - classical beaufort cipher
C_i = (K_i - P_i) mod 26
"""

from __future__ import annotations

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

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys
    
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.polyalphabetic.beaufort encrypt <text> <key>\n"
        "python3 -m decodr.ciphers.polyalphabetic.beaufort decrypt <text> <key>\n"
    )

    if len(sys.argv) < 4:
        print(usage)
        sys.exit(1)

    cmd, text, key = sys.argv[1:4]

    try:
        if cmd in ("encrypt", "encode"):
            print(encrypt(text, key))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, key))
        else:
            print("Unknown command. Use 'encrypt' or 'decrypt'.")
            print(usage)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

        
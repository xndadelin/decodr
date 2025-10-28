"""
decodr.ciphers.classical.affine - affine cipher 

Encryption: E(x) = (ax + b) mod 26
Decryption: D(x) = a_inv * (x - b) mod 26
a is the modulare inverse of a mod 26
"""

from __future__ import annotations

def _char_to_num(ch: str) -> int:
    return ord(ch.lower()) - ord('a')

def _num_to_char(n: int, upper: bool) -> str:
    base = ord("A") if upper else ord("a")
    return chr((n % 26) + base)

def _modinv(a: int, m: int) -> int:
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"There is no modular inverse for a={a} mod {m}")

def encrypt(plaintext: str, a: int = 5, b: int = 8) -> str:
    result = []
    for ch in plaintext:
        if ch.isalpha() and ch.isascii():
            upper = ch.isupper()
            x = _char_to_num(ch)
            y = (a * x + b) % 26
            result.append(_num_to_char(y, upper))
        else:
            result.append(ch)
    return "".join(result)

def decrypt(ciphertext: str, a: int = 5, b: int = 8) -> str:
    result = []
    a_inv = _modinv(a, 26)
    for ch in ciphertext:
        if ch.isalpha() and ch.isascii():
            upper = ch.isupper()
            y = _char_to_num(ch)
            x = (a_inv * (y - b) % 26)
            result.append(_num_to_char(x, upper))
        else:
            result.append(ch)
    return "".join(result)

encode = encrypt
decode = decrypt

def crack(ciphertex: str) -> list[tuple[int, int, str]]:
    valid_a = [1,3,5,7,9,11,15,17,19,21,23,25]
    results: list[tuple[int, int, str]] = []
    for a in valid_a:
        for b in range(26):
            try:
                pt = decrypt(ciphertex, a, b)
                results.append((a, b, pt))
            except Exception:
                continue
    return results

if __name__ == "__main__":
    import sys 

    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.classical.affine encrypt <text> [a] [b]\n"
        "python3 -m decodr.ciphers.classical.affine decrypt <text> [a] [b]\n"
        "python3 -m decodr.ciphers.classical.affine crack <ciphertext>\n"
    )

    if(len(sys.argv) < 3):
        print(usage)
        sys.exit(1)

    cmd, text = sys.argv[1], sys.argv[2]
    try:
        a = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
        b = int(sys.argv[4]) if len(sys.argv) >= 4 else 8
    except ValueError:
        print('a and b must be integers')
        sys.exit(1)

    try:
        if cmd in ("encrypt", "encode"):
            print(encrypt(text, a, b))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, a, b))
        elif cmd == "crack":
            for a_val, b_val, pt in crack(text):
                print(f"a={a_val:2d}, b={b_val:2d} -> {pt}")
        else:
            print("Error: Unknown command. Use 'encrypt', 'decrypt' or 'crack'.")
            print(usage)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    



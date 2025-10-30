"""
decodr.ciphers.transposition.railfence - rail fence (zig-zag) ciphers
"""

from __future__ import annotations

def _zigzag_indices(n: int, rails: int) -> list[int]:
    if rails < 2:
        raise ValueError("rails must be >= 2")
    rail = 0
    direction = 1
    rail_of_index: list[int] = []
    for _ in range(n):
        rail_of_index.append(rail)
        rail += direction
        if rail == rails - 1:
            direction = -1
        elif rail == 0:
            direction = 1
    
    indices: list[int] = []
    for r in range(rails):
        indices.extend(i for i, rr in enumerate(rail_of_index) if rr == r)
    return indices

def encrypt(plaintext: str, rails: int = 3) -> str:
    if rails < 2:
        raise ValueError("railst must be >= 2")
    n = len(plaintext)
    order = _zigzag_indices(n, rails)

    return "".join(plaintext[i] for i in order)

def decrypt(ciphertext: str, rails: int = 3) -> str:
    if rails < 2:
        raise ValueError("rails must be >= 2")
    n = len(ciphertext)
    order = _zigzag_indices(n, rails)

    plain = [""] * n
    for k, i in enumerate(order):
        plain[i] = ciphertext[k]

encode = encrypt
decode = decrypt

if __name__ == "__main__":
    import sys
    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.transposition.railfence encrypt <text> [rails]\n"
        "python3 -m decodr.ciphers.transposition.railfence decrypt <text> [rails]\n"
    )
    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)

    cmd, text = sys.argv[1], sys.argv[2]
    rails = int(sys.argv[3]) if len(sys.argv) >= 4 else 3

    try:
        if cmd in("encrypt", "encode"):
            print(encrypt(text, rails))
        elif cmd in ("decrypt", "decode"):
            print(decrypt(text, rails))
        else:
            print("Unknown command. Use 'encrypt' or 'decrypt'.")
            print(usage)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


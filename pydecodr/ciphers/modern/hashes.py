"""
decodr.ciphers.modern.hashes = common has algoritms md5, sha1, sha256/512
"""

from __future__ import annotations
import hashlib
from typing import Literal
import hmac

HashAlgo = Literal[
    "md5",
    "sha1",
    "sha256",
    "sha512"
]

def hash_text(text: str, algo: HashAlgo = "sha256", *, encoding: str = "utf-8") -> str:
    algo = algo.lower()
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported has algoritm: {algo}")
    h = hashlib.new(algo)
    h.update(text.encode(encoding))
    return h.hexdigest()

def verify_hash(text: str, digest: str, algo: HashAlgo = "sha256", *, encoding: str = "utf-8") -> bool:
    return hmac.compare_digest((hash_text(text, algo, encoding=encoding)), digest)

if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.ciphers.modern.hashes hash <text> [algo]\n"
        "python3 -m decodr.ciphers.modern.hashes verify <text> <digest>"
    )

    if len(sys.argv) < 3 :
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "hash":
            text = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            print(hash_text(text, algo))
        elif cmd == "verify":
            if len(sys.argv) < 4:
                print("Usage: verify <text> <digest> [algo]")
                sys.exit(1)
            text, digest = sys.argv[2], sys.argv[3]
            algo = sys.argv[4] if len(sys.argv) >= 5 else "sha256"
            ok = verify_hash(text, digest, algo)
            print("✅ match" if ok else "❌ not a match")
        else:
            print(usage)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
"""
pydecodr.ciphers.modern.hashes = common has algoritms md5, sha1, sha256/512
"""

from __future__ import annotations
import hashlib
from typing import Literal
import hmac
import sys
import argparse

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

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.ciphers.modern.hashes",
        description="Hashing utilities"
    )

    sub = p.add_subparsers(dest="command", required=True)

    p_hash = sub.add_parser("hash", help="compute hash of a text")
    p_hash.add_argument("text", help="text to hash")
    p_hash.add_argument("--algo", default="sha256", help="hash algoritm (default: sha256)", choices=["md5", "sha1", "sha256","sha512"])

    p_verify = sub.add_parser("verify", help="verify if text matches the hash")
    p_verify.add_argument("text", help="original text")
    p_verify.add_argument("digest", help="expected hash digest (hex)")
    p_verify.add_argument("--algo", default="sha256", help="hash algoritm (default: sha256)", choices=["md5", "sha1", "sha256","sha512"])

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.command == "hash":
            print(hash_text(args.text, args.algo))
            sys.exit(0)
        elif args.command == "verify":
            ok = verify_hash(args.text, args.digest, args.algo)
            print("✅ match" if ok else "❌ not a match")
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
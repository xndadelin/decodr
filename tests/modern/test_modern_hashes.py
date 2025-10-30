import hashlib
from pydecodr.ciphers.modern import hashes

def test_hashes():
    s = "HACKCLUB"
    algos = [
        "md5",
        "sha1",
        "sha256",
        "sha512"
    ]
    for algo in algos:
        expected = getattr(hashlib, algo)(s.encode()).hexdigest()
        got = hashes.hash_text(s, algo)
        assert got.lower() == expected, f"{algo} mismatch"
        assert hashes.verify_hash(s, expected, algo), f"{algo} verify failed"
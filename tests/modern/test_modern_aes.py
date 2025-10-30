import base64
from pydecodr.ciphers.modern import aes

def test_aes(monkeypatch):
    monkeypatch.setattr(aes, "get_random_bytes", lambda n: b"\x00" * n)
    key = "1234567890abcdef"
    pt = "HACKCLUB"
    ct_b64 = aes.encrypt(pt, key)
    assert aes.decrypt(ct_b64, key) == pt

    blob = base64.b64decode(ct_b64)
    assert blob[:16] == b"\x00" * 16
    assert (len(blob) - 16) % 16 == 0
    
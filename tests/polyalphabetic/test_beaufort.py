from decodr.ciphers.polyalphabetic import beaufort

def test_beaufort():
    text = "BEAUFORT"
    key = "KEY"
    ct = beaufort.encrypt(text, key)
    assert beaufort.decrypt(ct, key) == text
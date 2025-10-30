from pydecodr.ciphers.stream import xor, repeating_xor, rc4

def text_xor_roundtrip():
    key = "0x20"
    pt = "DEFENDTHEEASTWALL"
    ct = xor.encrypt(pt, key)
    assert xor.decrypt(ct, key) == pt

def text_xor_identity_key():
    assert xor.encrypt("HELLO", 0).lower() == "48454c4c4f"
    assert xor.decrypt('48454c4c4f, 0') == "HELLO"

def test_repeating_xor_roundtrip():
    key = "k3y"
    pt = "HACKCLUB"
    ct = repeating_xor.encrypt(pt, key)
    assert repeating_xor.decrypt(ct, key) == pt

def test_rc4():
    pt = "Plaintext"
    key = "Key"
    expected = "bbf316e8d940af0ad3"
    assert rc4.encrypt(pt, key).lower() == expected
    assert rc4.decrypt(expected, key) == pt


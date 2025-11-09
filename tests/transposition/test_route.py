from pydecodr.ciphers.transposition import route_cipher

def test_route_cipher():
    plaintext = "DEFEND THE EAST WALL AT DAWN"
    cols = 4

    ct = route_cipher.encrypt(plaintext, cols, "cw")
    assert isinstance(ct, str)
    assert ct != ""

    rt = route_cipher.decrypt(ct, cols, "cw")
    expected =  ''.join(ch.upper() for ch in plaintext if ch.isalnum())
    assert rt.startswith(expected)
    
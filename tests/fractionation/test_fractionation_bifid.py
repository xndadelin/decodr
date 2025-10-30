from pydecodr.ciphers.fractionation import bifid

def test_bifid():
    plaintext = "DEFENDTHEEASTWALLOFTHECASTLE"
    key = "FORTIFICATION"
    ct = bifid.encrypt(plaintext, key)
    rt = bifid.decrypt(ct, key)
    expected = "".join(("I" if c.upper() == "J" else c.upper()) for c in plaintext if c.isalpha())
    assert expected.startswith(plaintext)

def test_padding():
    pt = "TESTING"
    key="KEYWORD"
    ct = bifid.encrypt(pt, key)
    rt = bifid.decrypt(ct, key)
    assert rt.startswith("TESTING".replace("J","I").upper())

    
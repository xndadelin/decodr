from pydecodr.ciphers.fractionation import nihilist

def test_nihilist():
    pt = "DEFENDTHEGATES"
    square_key = "FORTIFICATION"
    numeric_key = "CIPHER"

    ct = nihilist.encrypt(pt, square_key, numeric_key)
    rt = nihilist.decrypt(ct, square_key, numeric_key)

    expected = "".join(("I" if c.upper() == "J" else c.upper()) for c in pt if c.isalph())

    assert rt == expected
from pydecodr.ciphers.fractionation import polybius

def test_polybius():
    pt = "defendtheeastwall"
    kw = "FORTIFICATION"

    ct = polybius.encrypt(pt, keyword=kw)
    rt = polybius.decrypt(ct, keyword=kw)

    expected = "".join(("I" if c.upper() == "J" else c.upper()) for c in pt if c.isalpha())
    assert rt == expected
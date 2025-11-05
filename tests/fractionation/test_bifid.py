from pydecodr.ciphers.fractionation import bifid

def test_bidid():
    pt = "Defend the gates"
    key = "FORTIFICATION"
    period = 5
    ct = bifid.encrypt(pt, key=key, period=period)
    rt = bifid.decrypt(ct, key=key, period=period)

    expected = "".join(("I" if c.upper() == "J" else c.upper()) if c.isalpha() else c for c in pt)

    assert rt == expected
from pydecodr.ciphers.fractionation import trifid

def test_trifid():
    pt = "defend the east wall"
    ct = trifid.encrypt(pt)
    rt = trifid.decrypt(ct)

    assert rt == pt
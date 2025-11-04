from pydecodr.ciphers.classical import hill

def test_hill():
    pt = "ATTACKATDAWN"
    key = "3,3,2,5"
    ct = hill.encrypt(pt, key)
    rt = hill.decrypt(ct, key)

    expected = pt.upper()
    assert rt == expected
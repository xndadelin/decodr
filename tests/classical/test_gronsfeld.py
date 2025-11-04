from pydecodr.ciphers.classical import gronsfeld

def test_gronsfeld():
    pt = 'DEFEND THE EAST WALL OF THE CASTLE'
    key = "31415"
    ct = gronsfeld.encrypt(pt, key)
    rt = gronsfeld.decrypt(ct, key)

    expected = pt
    assert rt == expected
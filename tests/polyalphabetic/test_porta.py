from pydecodr.ciphers.polyalphabetic import porta

def test_porta():
    pt = "DEFEND THE EAST WALL"
    key = "FORTIFICATION"

    ct = porta.encrypt(pt, key)
    rt = porta.decrypt(ct, key)

    assert rt == pt
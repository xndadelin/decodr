from pydecodr.ciphers.transposition import double_transposition

def test_double_transposition():
    pt = "DEFEND THE EAST WALL"
    k1 = "FORT"
    k2 = "CIPHER"
    ct = double_transposition.encrypt(pt, k1, k2, pad="X")
    rt = double_transposition.decrypt(ct, k1, k2, pad="X")

    assert rt == pt
    
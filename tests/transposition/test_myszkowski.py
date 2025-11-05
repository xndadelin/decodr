from pydecodr.ciphers.transposition import myszkowski

def test_myszkowski():
    pt = "DEFENDTHEEASTWALL"
    key = "BALLOON"
    ct = myszkowski.encrypt(pt, key, pad="X")
    rt = myszkowski.decrypt(ct, key, pad="X")

    assert rt == pt
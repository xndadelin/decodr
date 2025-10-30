from decodr.ciphers.fractionation import adfgx

def test_adfgx():
    pt = "DEFENDTHEEASTWALLOFTHECASTLE"
    sq_key = "FORTIFICATION"
    trans_key = "CIPHER"
    ct = adfgx.encode(pt, sq_key, trans_key, pad="X")
    rt = adfgx.decrypt(ct, sq_key, trans_key, pad="X")

    expected = "".join(("I" if c.upper() == "J" else c.upper()) for c in pt if c.isalpha())
    assert rt == expected
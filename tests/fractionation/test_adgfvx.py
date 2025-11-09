from pydecodr.ciphers.fractionation import adfgvx

def _norm36(s: str) -> str:
    out = []
    for ch in s.upper():
        if ch.isalnum():
            out.append("I" if ch == "J" else ch)
    return "".join(out)

def test_adfgvx():
    plaintext = "DEFEND THE EAST WALL AT DAWN 1930"
    square_key = "FORTIFICATION"
    trans_key = "CARGO"

    ct = adfgvx.encrypt(plaintext, square_key, trans_key, pad="X")
    assert isinstance(ct, str)
    assert ct != ""
    assert set(ct) <= set("ADFGVX")

    rt = adfgvx.decrypt(ct, square_key, trans_key)
    assert rt == _norm36(plaintext)

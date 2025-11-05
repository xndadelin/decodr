from pydecodr.ciphers.classical import bacon

def test_bacon():
    pt = "HACKCLUB YIHA"
    ct = bacon.encrypt(pt)
    rt = bacon.decrypt(ct)

    expected = "".join(c.upper() for c in pt if c.isalpha() or not c.isspace())
    assert rt == expected
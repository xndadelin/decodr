from pydecodr.ciphers.classical import rot47

def test_rot47():
    pt = "HACKCLUBADVENTURE"
    ct = rot47.encrypt(pt)
    rt = rot47.decrypt(ct)

    expected = pt
    assert rt == expected
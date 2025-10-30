from pydecodr.ciphers.classical import affine

def test_affine():
    text = "BUCHAREST"
    a, b = 5, 8
    ct = affine.encrypt(text, a, b)
    assert affine.decrypt(ct, a, b) == text



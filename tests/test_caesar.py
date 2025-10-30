from decodr.ciphers.classical import caesar

def test_caesar():
    text = "HACKCLUB"
    key = 5
    ct = caesar.encrypt(text, key)
    assert caesar.decrypt(ct, key) == text

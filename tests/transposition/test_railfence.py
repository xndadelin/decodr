from pydecodr.ciphers.transposition import railfence

def test_railfence():
    text = "HELLOFROMTHEMOON"
    key = 3
    ct = railfence.encrypt(text, key)
    assert railfence.decrypt(ct, key) == text
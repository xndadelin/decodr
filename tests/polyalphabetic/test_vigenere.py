from decodr.ciphers.polyalphabetic import vigenere, autokey_vigenere

def test_vigenere():
    text = "ILOVEPYTHON"
    key = "KEY"
    ct = vigenere.encrypt(text, key)
    assert vigenere.decrypt(ct, key) == text

def autokey_test_vigenere():
    text = "ILOVEPYTHON"
    key = "KEY"
    ct = autokey_vigenere.encrypt(text, key)
    assert autokey_vigenere.decrypt(ct, key) == text

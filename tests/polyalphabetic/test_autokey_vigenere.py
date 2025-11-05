from pydecodr.ciphers.polyalphabetic import autokey_vigenere

def test_vigenere_autokey():
    pt = "DEFEND THE EAST WALL"
    key = "FORT"
    ct = autokey_vigenere.encrypt(pt, key)
    rt = autokey_vigenere.decrypt(ct, key)

    assert rt == pt
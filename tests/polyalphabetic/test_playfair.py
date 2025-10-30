from pydecodr.ciphers.polyalphabetic import playfair

def test_playfair():
    text = "HIDETHEGOLD"
    key = "PLAYFAIR"
    ct = playfair.encrypt(text, key)
    rt = playfair.decrypt(ct, key)

    normalized = text.replace("J", "I").upper()
    assert rt.startswith(normalized)


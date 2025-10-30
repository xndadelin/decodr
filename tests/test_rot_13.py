from decodr.ciphers.classical import rot13

def test_rot13():
    text="CAESARSALAD"
    assert rot13.decrypt(rot13.encrypt(text)) == text
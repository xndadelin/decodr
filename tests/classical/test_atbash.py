from decodr.ciphers.classical import atbash

def test_atbash():
    text = "SANFRANCISCO"
    ct = atbash.encrypt(text)
    assert atbash.decrypt(ct) == text
from pydecodr.ciphers.classical import substitution

def test_substitution():
    text = "AVADAKEDAVRA"
    mapping ={chr(i+65): chr(i+65) for i in range(26)}
    ct = substitution.encrypt(text, mapping)
    assert substitution.decrypt(ct, mapping) == text
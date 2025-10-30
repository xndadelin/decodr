from decodr.ciphers.rotor import enigma

def test_engima():
    pt = "HACKCLUB"
    ct = enigma.encrypt(pt)
    assert enigma.decrypt(ct) == pt
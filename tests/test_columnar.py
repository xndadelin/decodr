from decodr.ciphers.transposition import columnar

def test_columnar():
    text = "DEFENDDUCKADAM"
    key = "FORTRESS"
    ct = columnar.encrypt(text, key)
    rt = columnar.decrypt(ct, key)
    assert rt == text or rt.strip("X") == text

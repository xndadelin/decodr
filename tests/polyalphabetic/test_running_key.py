from pydecodr.ciphers.polyalphabetic import running_key

def test_running_key():
    pt = "DEFEND THE EAST WALL"
    key = "THIS SHOULD BE A VERY LONG BOOK PASSAGE USED AS RUNNING KEY"

    ct = running_key.encrypt(pt, key)
    rt = running_key.decrypt(ct, key)

    assert rt == pt
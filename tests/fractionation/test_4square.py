from pydecodr.ciphers.fractionation import four_square

def test_four_square():
    pt = "DEFEND THE EAST WALL"
    key1 = "FORTIFICATION"
    key2 = "CIPHER"
    ct = four_square.encrypt(pt, key1, key2)
    rt = four_square.decrypt(ct, key1, key2)

    expected = "".join("I" if c == "J" else "i" if c == "j" else c for c in pt)

    assert rt == expected
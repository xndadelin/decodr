from pydecodr.ciphers.classical import homophonic
import random 

def test_homophonic():
    random.seed(0)
    pt = "DEFEND THE EAST WALL"
    ct = homophonic.encrypt(pt)
    rt = homophonic.decrypt(ct)

    expected = pt.upper()
    assert rt == expected
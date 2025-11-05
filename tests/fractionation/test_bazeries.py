from pydecodr.ciphers.fractionation import bazeries

def test_bazeries():
    pt = "Defend the East wall of HackClub"
    alpha_key = "FORTIFICATION"
    num_key = "431256"
    ct = bazeries.encrypt(pt, alpha_key, num_key)
    rt = bazeries.decrypt(ct, alpha_key, num_key)

    expected = "".join("I" if c == "J" else "i" if c == "j" else c for c in pt)
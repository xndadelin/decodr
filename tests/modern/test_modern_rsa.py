from pydecodr.ciphers.modern import rsa

def test_rsa():
    pub, priv = rsa._generate_keys(61, 53, 65537)
    n_e, n_d = pub, priv
    n, e = n_e
    n2, d = n_d
    assert n == n2
    pt = "HACKCLUB"
    ct = rsa.encrypt(pt, n, e)
    assert rsa.decrypt(ct, n, d) == pt

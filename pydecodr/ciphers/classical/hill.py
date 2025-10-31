"""
pydecodr.ciphers.classical.hill -  hill cipher (2x2 and 3x3)
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_SET = set(ALPHABET)
MOD = 26

def clean_letters(s):
    return "".join(ch for ch in s.upper() if ch in ALPHABET_SET)

def letters_only_and_positions(s):
    s_up = s.upper()
    letters = []
    pos = []
    for i, ch in enumerate(s_up):
        if ch in ALPHABET_SET:
            letters.append(ch)
            pos.append(i)
    return "".join(letters), pos

def idx(c): return ord(c) - 65
def ch(i): return chr((i % MOD) + 65)

def parse_matrix(key_str):
    if not key_str or not isinstance(key_str, str):
        raise ValueError("Matrix key must be a non empty string.")
    s = key_str.replace("|", ";").replace("\n", ";")
    tmp = []
    current_row = []
    rows = []
    token = ""
    for ch in s:
        if ch in ", \t":
            if token:
                tmp.append(token)
                token = ""
        elif ch == ";":
            if token: 
                tmp.append(token)
                token = ""
            if tmp:
                rows.append(tmp)
                tmp = []
        else:
            token += ch
    if token: 
        tmp.append(token)
    if tmp:
        rows.append(tmp)

    if not rows:
        raise ValueError("Invalid key matrix format.")
    
    if len(rows) == 1:
        flat = rows[0]
        if len(flat) == 4:
            rows = [flat[:2], flat[2:]]
        elif len(flat) == 9:
            rows = [flat[0:3], flat[3:6], flat[6:9]]
        else:
            raise ValueError("Key needs 4 numbers or 9.")
        
    n = len(rows)
    if n not in (2, 3):
        raise ValueError("Only 2x2 and 3x3 matrices are allowed.")
    for r in rows:
        if len(r) != n:
            raise ValueError("Matrix must be square.")
        
    M = []
    for r in rows:
        row = []
        for t in r:
            try:
                row.append(int(t) % MOD)
            except:
                raise ValueError("Key matrix must contain only integers.")
        M.append(row)
    return M, n

def egcd(a, b):
    if b == 0: 
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m=MOD):
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m

def det2(M):
    return (M[0][0] * M[1][1] - M[0][1] * M[1][0]) % MOD

def det3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return (a*(e*i - f*h) - b(d*i - f*g) + c*(d*h - e*g)) % MOD

def mat_inv2(M):
    d = det2(M)
    invd = modinv(d, MOD)
    a, b = M[0]
    c, dv = M[1]
    adj = [[ dv, (-b) % MOD],  [(-c) % MOD, a % MOD]]
    return [[(invd * adj[0][0]) % MOD, (invd * adj[0][1]) % MOD],
            [(invd * adj[1][0]) % MOD, (invd * adj[1][1]) % MOD]]

def minor3(M, r, c):
    minor = []
    for ri in range(3):
        if ri == r:
            continue
        row = M[ri][:c] + M[ri][c+1:]
        minor.append(row)
    return minor

def mat_inv3(M):
    d = det3(M)
    invd = modinv(d, MOD)
    cof = [[0] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            m = minor3(M, r, c)
            dd = (m[0][0]*m[1][1] - m[0][1]*m[1][0]) % MOD

            cof[r][c] = ((-1) ** (r + c) * dd) % MOD

    adj = [[cof[0][0], cof[1][0], cof[2][0]],
             [cof[0][1], cof[1][1], cof[2][1]],
             [cof[0][2], cof[1][2], cof[2][2]]
          ]
    return [[(invd * adj[r][c]) % MOD for c in range(3)] for r in range(3)]

def mat_mul_vec(M, v):
    n = len(M)
    return [sum(M[r][k] * v[k] for k in range(n)) % MOD for r in range(n)]


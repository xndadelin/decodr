<div align="center">
  <a href="https://moonshot.hackclub.com" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/35ad2be8c916670f3e1ac63c1df04d76a4b337d1_moonshot.png" 
         alt="This project is part of Moonshot, a 4-day hackathon in Florida visiting Kennedy Space Center and Universal Studios!" 
         style="width: 100%;">
  </a>
</div>

# pydecodr
> A modular CTF/crypto library toolkit for encodings, classic ciphers, and autodetection. CLI included :3.


`pydecodr` is a Python package that lets you **encode, decode, encrypt or decrypt text** using classical, polyalphabetic, modern, and stream ciphers, all through a **Python API** and a **CLI interface**

---
## Features:
- classical ciphers: (caesar, atbash, affine, rot13, substitution)
- polyalphabetic: (vigenere, autokey_vigenere, beaufort, playfair)
- fractionation: (bifid, ADFGX)
- transpos9ition: (railfence, columnar)
- stream: (xor, repeating xor, rc4)
- modern: (aes, rsa, hash utilities)
- encodings: (b32, b64, hex, URL-safe)
- detection & utils: (file magic detection, I/O helpers)
- cli interface

---

## Installation
```bash
pip install pydecodr
```

--- 

## Usage
### CLI interface
You can use any cipher module directly with Python's `-m` flag:

```python
# caesar cipher
python3 -m pydecodr.ciphers.classical.caesar encrypt "HELLO" 3
# -> KHOOR

python3 -m pydecodr.ciphers.classical.caesar decrypt "KHOOR" 3
# -> HELLO
```

### Python API
```python
from pydecodr.ciphers.classical import caesar
from pydecodr.ciphers.polyalphabetic import vigenere

print(caesar.encrypt("HELLO", 3))
# KHOOR

print(vigenere.encrypt("HELLOWORLD", "KEY"))
# RIJVSUYVJN
```
Or load dynamically using the global registry:
```python
from pydecodr import load_module

mod = load_module("adfgx")
ciphertext = mod.encrypt("DEFEND THE EAST WALL", "FORTIFICATION", "CIPHER")
print(mod.decrypt(ciphertext, "FORTIFICATION", "CIPHER"))
```
Check this for more usage: [usage](https://xndadelin.me/pydecodr/)


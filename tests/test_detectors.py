from pydecodr.detectors import autodetect
from pydecodr.detectors import file_magic

def test_autodetect():
    assert autodetect.detect_type("48656c6c6f")['type'] == 'hex'
    assert autodetect.detect_type("SGVsbG8=")['type'] == 'base64'
    assert autodetect.detect_type("%48%65%6C%6C%6F")['type'] == "url-encoded"
    assert autodetect.detect_type("HELLO")["type"] in ("plaintext", "unknown")

def test_file_magic(tmp_path):
    p = tmp_path / "sample.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"readadadakdjhakdhaskjd")
    assert file_magic.detect_file(str(p)) == "PNG image"


from pydecodr.encodings import morse

def test_morse():
    pt = "SOS WE ATTACK AT 0900"
    ct = morse.encode(pt)
    rt = morse.decode(ct)

    expected = pt.upper()
    assert rt == expected
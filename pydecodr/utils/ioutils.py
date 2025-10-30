"""
decodr.utils.ioutils - input/output helpers.

Provides helper functions for reading input and ofc writing output,
that's it either from strings, files, or stdin/stdout.
"""

from __future__ import annotations
from pathlib import Path
import sys

def read_input(text: str | None = None, infile: str | None = None, binary: bool = False) -> bytes:
    if text is not None:
        return text.encode('utf-8') if not binary else text.encode('utf-8', 'ignore')
    
    if infile:
        path = Path(infile)
        # mode = "rb" if binary else "r"
        data = path.read_bytes() if binary else path.read_text(encoding="utf-8", errors="ignore")
        return data if isinstance(data, bytes) else data.encode('utf-8')
    
    data = sys.stdin.buffer.read()
    return data if isinstance(data, bytes) else data.encode('utf-8', 'ignore') 

def write_output(data: bytes, outFile: str | None = None, binary: bool = False):
    if outFile:
        path = Path(outFile)
        if binary:
            path.write_bytes(data)
        else:
            path.write_text(data.decode('utf-8', 'ignore'), encoding='utf-8')
    else:
        if binary:
            sys.stdout.buffer.write(data)
        else:
            print(data.decode('utf-8', 'ignore'))
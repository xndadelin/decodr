"""
pydecodr.detectors.file_magic - magic number detection
"""

from __future__ import annotations
from typing import Optional, Tuple, Dict

MAGIC_SIGNATURES: Dict[bytes, str] = {
    b"\x89PNG\r\n\x1a\n": "PNG image",
    b"\xFF\xD8\xFF": "JPEG image",
    b"GIF87a": "GIF image",
    b"GIF89a": "GIF image",
    b"%PDF-": "PDF document",
    b"PK\x03\x04": "ZIP archive",
    b"7z\xBC\xAF\x27\x1C": "7-Zip archive",
    b"Rar!\x1A\x07\x00": "RAR archive",
    b"MZ": "Windows executable (PE)",
    b"\x25\x21PS": "PostScript document",
    b"OggS": "Ogg audio stream",
    b"ID3": "MP3 audio (with tag)",
    b"\x1F\x8B": "GZIP compressed file",
    b"\x42\x5A\x68": "BZIP2 compressed file",
    b"\x50\x4B\x03\x04": "ZIP archive",
    b"\x50\x4B\x05\x06": "ZIP empty archive",
}

def detect_magic(data: bytes) -> Optional[str]:
    for sig, name in MAGIC_SIGNATURES.items():
        if data.startswith(sig):
            return name
    return None

def detect_file(path: str) -> Optional[str]:
    try:
        with open(path, "rb") as f:
            head = f.read(16)
        return detect_magic(head)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise RuntimeError(f"Error reading {path}: {e}")
    
if __name__ == "__main__":
    import sys

    usage = (
        "Usage:\n"
        "python3 -m decodr.detectors.file_magic <file>\n"
    )
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    path = sys.argv[1]
    try:
        file_type = detect_file(path)
        if file_type:
            print(f"Detected: {file_type}")
        else:
            print("Unknown file type or unsupported signature.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)    

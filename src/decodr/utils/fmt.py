"""
decodr.utils.fmt - formatting helpers for CLI display.

Small helpers to collapse whitespace, clip strings with ellipsis,
and ofc produce readable previews for text/bytes.
"""

from __future__ import annotations
from typing import Optional

ELLIPSIS = "..."

def collapse_ws(s: str) -> str:
    return " ".join(s.replace("\r", "").replace("\n", " ").replace("\t", " ").split())

def clip(s: str, max_len: int = 80, ellipsis: str = ELLIPSIS) -> str:
    if max_len < 0 or len(s) <= max_len:
        return s
    if max_len <= len(ellipsis):
        return ellipsis[:max_len]
    return s[: max_len - len(ellipsis) ] + ellipsis


def preview_text(s: str, max_len: int = 80) -> str:
    return clip(collapse_ws(s), max_len=max_len)

def _printable_ratio(b: bytes) -> float:
    printable = set(range(32, 127)) | {9, 10, 13}
    if not b:
        return 1.0
    ok = sum(1 for x in b if x in printable)
    return ok / len(b)

def __chunks(s: str, n: int) -> list[str]:
    return [s[i : i + n] for i in range(0, len(s), n)]

def hex_preview(b: bytes, max_len: int = 80, group: int = 2, sep: str = " ") -> str:
    hx = b.hex()
    grouped = sep.join(__chunks(hx, group))
    return clip(grouped, max_len=max_len)

def bytes_to_preview(b: bytes, max_len: int = 80) -> str:
    try:
        s = b.decode("utf-8", "ignore")
    except Exception:
        return hex_preview(b, max_len=max_len)
    
    if _printable_ratio(b) >= 0.85 and s.strip():
        return preview_text(s, max_len=max_len)
    return hex_preview(b, max_len=max_len)

def auto_preview(data: str | bytes, max_len: int = 80) -> str:
    if isinstance(data, bytes):
        return bytes_to_preview(data, max_len)
    return preview_text(str(data), max_len=max_len)

def surround(label: str, value: str, sep: str = ": ") -> str:
    return f"{label}{sep}{preview_text(value)}"

def pad_right(s: str, width: int) -> str:
    if len(s) >= width:
        return s
    return s + " " * (width - len(s))

def align_kv(items: list[tuple[str, str]], gap: int = 2) -> str:
    if not items:
        return ""
    max_key = max(len(k) for k, _ in items)
    lines = []
    for k, v in items:
        kpad = pad_right(k, max_key)
        lines.append(f"{kpad}{' ' * gap}: {v}")
    return "\n".join(lines)


 
"""
pydecodr.encodings.morse - simple morse decoder/encoder
"""

from __future__ import annotations
import sys
import argparse
from typing import Dict

MORSE: Dict[str, str] = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "'": ".----.", "!": "-.-.--",
    "/": "-..-.", "(": "-.--.", ")": "-.--.-", "&": ".-...", ":": "---...",
    ";": "-.-.-.", "=": "-...-", "+": ".-.-.", "-": "-....-", "_": "..--.-",
    "\"": ".-..-.", "$": "...-..-", "@": ".--.-."
}

REV = {v: k for k, v in MORSE.items()}

def encode(text: str, letter_sep: str = " ", word_sep: str = " / ", keep_unknown: bool = False) -> str:
    out_words = []
    for word in text.split():
        codes = []
        for ch in word.upper():
            code = MORSE.get(ch)
            if code is None:
                if keep_unknown:
                    codes.append(ch)
            else:
                codes.append(code)
        out_words.append(letter_sep.join(codes))
    return word_sep.join(out_words)

def decode(code: str, letter_sep: str = " ", word_sep: str = " / ", keep_unknown: bool = False) -> str:
    parts_words = code.split(word_sep) if word_sep else [code]
    out_words = []
    for w in parts_words:
        letters = [t for t in w.strip().split(letter_sep) if t != ""]
        out_letters = []
        for token in letters:
            ch = REV.get(token)
            if ch is None:
                if keep_unknown:
                    out_letters.append(token)
            else:
                out_letters.append(ch)
        out_words.append("".join(out_letters))
    return " ".join(out_words)

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pydecodr.encodings.morse",
        description="Simple morse encoder/decodr"
    )

    p.add_argument("action", choices=["encode", "decode"], help="action to perform")
    p.add_argument("text", help="plaintext (encode) or morse text (decode). quote if contains spaces")
    p.add_argument("--letter-sep", default=" ", help="separator between letters (default: space)")
    p.add_argument("--word-sep", default=" / ", help="separator between words (default: ' / ')")
    p.add_argument("--keep-unknown", action="store_true", help="keep unknown characters/tokens instead of dropping them")

    return p

if __name__ == "__main__":
    parser = _build_argparser()
    args = parser.parse_args(sys.argv[1:])
    try:
        if args.action == "encode":
            print(encode(args.text, letter_sep=args.letter_sep, word_sep=args.word_sep, keep_unknown=args.keep_unknown))
        else:
            print(decode(args.text, letter_sep=args.letter_sep, word_sep=args.word_sep, keep_unknown=args.keep_unknown))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


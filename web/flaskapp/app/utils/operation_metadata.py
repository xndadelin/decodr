from pydecodr.api import ENCODING_MAP

def get_operations_metadata():
    operations = {
        "encodings": [],
        "classical": [],
        "polyalphabetic": [],
        "fractionation": [],
        "transposition": [],
        "stream": [],
        "rotor": [],
        "modern": []
    }

    for name, module_path in ENCODING_MAP.items():
        if "encodings" in module_path:
            category = "encodings"
            actions = ["encode", "decode"]
        elif "classical" in module_path:
            category = "classical"
            actions = ["encrypt", "decrypt"]
            if name in ["caesar", "affine"]:
                actions.append("crack")
        elif "polyalphabetic" in module_path:
            category = "polyalphabetic"
            actions = ["encrypt", "decrypt"]
        elif "transposition" in module_path:
            category = "transposition"
            actions = ["encrypt", "decrypt"]
        elif "stream" in module_path:
            category = "stream"
            actions = ["encrypt", "decrypt"]
        elif "rotor" in module_path:
            category = "rotor"
            actions = ["encrypt", "decrypt"]
        elif "modern" in module_path:
            category = "modern"
            if name == "hashes":
                actions = ['encode']
            else:
                actions = ["encrypt", "decrypt"]
        else:
            category = "utils"
            actions = []


def get_operation_metadata(operation_name):
    params_map = {
        "caesar": [
            {
                "name": "shift",
                "type": "number",
                "default": 3,
                "min": 1,
                "max": 25
            }
        ],
        "affine": [
            {
                "name": "a",
                "type": "number",
                "default": 5
            },
            {
                "name": "b",
                "type": "number",
                "default": 8
            }
        ],
        "vigenere": [
            {
                "name": "key",
                "type": "text",
                "required": True
            }
        ],
        "playfair": [
            {
                "name": "key",
                "type": "text",
                "required": True
            }
        ],
        "railfence": [
            {
                "name": "rails",
                "type": "number",
                "default": 3,
                "min": 2
            }
        ],
        "columnar": [
            {
                "name": "key",
                "type": "text",
                "required": True
            }
        ],
        "xor": [
            {
                "name": "key",
                "type": "text",
                "required": True
            }
        ],
        "repeating_xor": [
            {
                "name": "key",
                "type": "text",
                "required": True
            }
        ],
        "rc4": [
            {
                "name": "key",
                "type": "text",
                "required": True
            }
        ],
        "aes": [
            {
                "name": "key",
                "type": "text",
                "required": True
            },
            {
                "name": "mode",
                "type": "select",
                "options": [
                    "CBC", "ECB", "CTR"
                ],
                "default": "CBC"
            }
        ],
        "rsa": [
            {
                "name": "key_size", "type": "numer", "default": 2048
            }
        ],
        "hashes": [
            {
                "name": "algoritm",
                "type": "select",
                "options": [
                    "md5", "sha1", "sha256", "sha512"
                ],
                "default": "sha256"
            }
        ]
    }

    return params_map.get(operation_name, [])
    
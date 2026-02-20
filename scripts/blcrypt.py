#!/usr/bin/env python3
# written by glacierpiece
# https://github.com/glacierpiece/borderlands-4-save-utlity
# Modified to support Epic ID and general improvements

import argparse, sys, zlib, yaml, struct
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def unknown_constructor(loader, _tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    else:
        return None

yaml.add_multi_constructor('!', unknown_constructor, yaml.SafeLoader)

BASE_KEY = bytes((
    0x35, 0xEC, 0x33, 0x77, 0xF3, 0x5D, 0xB0, 0xEA,
    0xBE, 0x6B, 0x83, 0x11, 0x54, 0x03, 0xEB, 0xFB,
    0x27, 0x25, 0x64, 0x2E, 0xD5, 0x49, 0x06, 0x29,
    0x05, 0x78, 0xBD, 0x60, 0xBA, 0x4A, 0xA7, 0x87
))

def derive_key(user_id: str, platform: str = "steam") -> bytes:
    k = bytearray(BASE_KEY)
    if platform == "steam":
        sid = int("".join(ch for ch in user_id if ch.isdigit()), 10)
        sid_le = sid.to_bytes(8, "little", signed=False)
        for i in range(8):
            k[i] ^= sid_le[i]
    elif platform == "epic":
        # Epic ID is UTF-16LE, XOR'd up to 32 bytes
        uid_bytes = user_id.encode("utf-16le")
        for i in range(min(len(uid_bytes), 32)):
            k[i] ^= uid_bytes[i]
    else:
        raise ValueError(f"Unsupported platform: {platform}")
    return bytes(k)

def decrypt_sav_to_yaml(sav_path: Path, user_id: str, platform: str = "steam") -> bytes:
    ciph = sav_path.read_bytes()
    if len(ciph) % 16 != 0:
        raise ValueError(f"input .sav size {len(ciph)} not multiple of 16")
    key = derive_key(user_id, platform)
    pt_padded = AES.new(key, AES.MODE_ECB).decrypt(ciph)
    try:
        body = unpad(pt_padded, 16, style="pkcs7")
    except ValueError:
        print("PKCS7 unpad failed, returning padded data")
        body = pt_padded
    yaml_data = zlib.decompress(body)
    return yaml_data

def encrypt_yaml_to_sav(yaml_path: Path, user_id: str, platform: str = "steam") -> bytes:
    current_yaml = yaml_path.read_bytes()
    comp = zlib.compress(current_yaml, level=9)
    adler32 = zlib.adler32(current_yaml) & 0xffffffff
    uncompressed_length = len(current_yaml)
    packed = comp + struct.pack('<I', adler32) + struct.pack('<I', uncompressed_length)
    pt_padded = pad(packed, 16, style="pkcs7")
    key = derive_key(user_id, platform)
    ciph = AES.new(key, AES.MODE_ECB).encrypt(pt_padded)
    return ciph

def main():
    parser = argparse.ArgumentParser(
        prog="blcrypt",
        description=(
            "Encrypt/decrypt BL4 saves - decrypt to readable YAML, edit values, then encrypt.\n"
            "I'm not responsible for any damage you do your save file. Backup your save file before using this, and be smart."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_dec = sub.add_parser(
        "decrypt",
        help="Decrypt a .sav to readable YAML.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p_dec.add_argument("-in", "--input", required=True, help="Path to input .sav")
    p_dec.add_argument("-out", "--output", help="Path to output .yaml (default: <input>.yaml)")
    p_dec.add_argument("-id", "--id", required=True, help="User ID (SteamID or Epic ID)")
    p_dec.add_argument("-p", "--platform", choices=["steam", "epic"], default="steam", help="Platform (default: steam)")
    p_dec.epilog = (
        "Examples:\n"
        "  blcrypt decrypt -in 1.sav -out save.yaml -id 7656119XXXXXXXXX\n"
        "  blcrypt decrypt -in 1.sav -out save.yaml -id epic_user -p epic\n"
        "If PKCS7 or zlib errors appear, verify the ID and platform are correct."
    )

    p_enc = sub.add_parser(
        "encrypt",
        help="Encrypt a YAML to .sav to be read by the game.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p_enc.add_argument("-in", "--input", required=True, help="Path to input .yaml")
    p_enc.add_argument("-out", "--output", help="Path to output .sav (default: <input>.sav)")
    p_enc.add_argument("-id", "--id", required=True, help="User ID (SteamID or Epic ID)")
    p_enc.add_argument("-p", "--platform", choices=["steam", "epic"], default="steam", help="Platform (default: steam)")
    p_enc.epilog = (
        "Examples:\n"
        "  blcrypt encrypt -in save.yaml -out 1.sav -id 7656119XXXXXXXXX\n"
        "The game should accept the .sav if the ID matches the save owner."
    )

    args = parser.parse_args()

    try:
        if args.cmd == "decrypt":
            in_path = Path(args.input)
            out_path = Path(args.output) if args.output else in_path.with_suffix(".yaml")
            yaml_bytes = decrypt_sav_to_yaml(in_path, args.id, args.platform)
            out_path.write_bytes(yaml_bytes)
            print(f"wrote {out_path}")
        elif args.cmd == "encrypt":
            in_path = Path(args.input)
            out_path = Path(args.output) if args.output else in_path.with_suffix(".sav")
            sav_bytes = encrypt_yaml_to_sav(in_path, args.id, args.platform)
            out_path.write_bytes(sav_bytes)
            print(f"wrote {out_path}")
        else:
            parser.error("unknown command")
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

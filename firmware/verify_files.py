#!/usr/bin/env python3
"""Offline checksum and AVB-signature check; does not access or flash a phone."""
import hashlib,json,struct,sys
from pathlib import Path

def check(condition,message):
    if not condition:raise ValueError(message)

def avb_signature(data):
    """Check the SHA256_RSA2048 signature against the embedded AVB public key.

    This verifies internal signing consistency, not the phone's trust anchor.
    AVB public keys use exponent 65537; the signed input is header + aux block.
    """
    check(data[:4] == b"AVB0" and len(data) >= 256, "Invalid AVB header")
    auth, aux = struct.unpack_from(">QQ", data, 12)
    check(struct.unpack_from(">I", data, 28)[0] == 1,
          "Expected signed SHA256_RSA2048 AVB metadata")
    check(struct.unpack_from(">I", data, 120)[0] == 0,
          "Stock AVB flags were altered")
    hash_off, hash_size, sig_off, sig_size, key_off, key_size = struct.unpack_from(">6Q", data, 32)
    aux_start = 256 + auth
    check(aux_start + aux <= len(data), "Truncated AVB data")
    check(hash_off + hash_size <= auth and sig_off + sig_size <= auth,
          "AVB authentication fields exceed their block")
    check(key_off + key_size <= aux, "AVB key exceeds auxiliary block")
    key = data[aux_start + key_off:aux_start + key_off + key_size]
    check(len(key) >= 8, "Truncated AVB key")
    bits = struct.unpack_from(">I", key)[0]
    check(bits == 2048 and sig_size == 256 and hash_size == 32,
          "Unexpected AVB RSA field sizes")
    modulus = int.from_bytes(key[8:8 + 256], "big")
    digest = hashlib.sha256(data[:256] + data[aux_start:aux_start + aux]).digest()
    check(digest == data[256 + hash_off:256 + hash_off + hash_size],
          "AVB signed digest mismatch")
    signature = data[256 + sig_off:256 + sig_off + sig_size]
    value = int.from_bytes(signature, "big")
    check(0 < value < modulus, "Invalid RSA signature value")
    decoded = pow(value, 65537, modulus).to_bytes(256, "big")
    digest_info = bytes.fromhex("3031300d060960864801650304020105000420") + digest
    expected = b"\0\1" + b"\xff" * (256 - len(digest_info) - 3) + b"\0" + digest_info
    check(decoded == expected, "AVB RSA signature does not verify")


def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'manifest.json').read_text())
    for name,item in manifest['files'].items():
        p=(root/name).resolve()
        check(p.is_relative_to(root),'Invalid path')
        check(p.is_file() and p.stat().st_size==item['bytes'],'Missing/size mismatch: '+name)
        with p.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
        check(digest==item['sha256'],'SHA256 mismatch: '+name)
        print('SHA256 OK: '+name,flush=True)
    for name in ['vbmeta.img','vbmeta_system.img','vbmeta_vendor.img']:
        avb_signature((root/name).read_bytes())
        print('AVB signature OK: '+name,flush=True)
    d=(root/'vbmeta.img').read_bytes();auth=struct.unpack_from('>Q',d,12)[0];off,size=struct.unpack_from('>QQ',d,64)
    pub=d[256+auth+off:256+auth+off+size]
    check(hashlib.sha1(pub).hexdigest()=='cdbb77177f731920bbe0a0f94f84d9038ae0617d','Root key differs from original ROM')
    check(pub==(root/'verification/root.avbpubkey').read_bytes(),'Root key byte mismatch')
    print('PASS: file hashes, signatures and stock root-key match. Full AVB build report is in verification/.')
    print('On-device boot is not established by this offline check.')

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)

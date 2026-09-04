"""
Week 3 — FIX the misuse here. Fill in the TODOs.
pip install argon2-cffi pycryptodome
"""
import os
import hashlib
import hmac
from argon2 import PasswordHasher
from Crypto.Cipher import AES

ph = PasswordHasher()

def store_password(pw: str) -> str:
    # FIX: argon2id, salted automatically
    return ph.hash(pw)

def verify_password(hash_: str, pw: str) -> bool:
    try:
        return ph.verify(hash_, pw)
    except Exception:
        return False

def verify_and_migrate(stored_hash: str, pw: str) -> tuple[bool, str, bool]:
    if stored_hash.startswith("$argon2"):
        if not verify_password(stored_hash, pw):
            return False, stored_hash, False
        if ph.check_needs_rehash(stored_hash):
            return True, store_password(pw), True
        return True, stored_hash, False

    legacy_md5 = hashlib.md5(pw.encode()).hexdigest()

    if hmac.compare_digest(legacy_md5, stored_hash):
        new_hash = store_password(pw)
        return True, new_hash, True

    return False, stored_hash, False

def encrypt_gcm(data: bytes, key: bytes) -> tuple[bytes, bytes, bytes]:
    # FIX: authenticated encryption (AES-GCM), random nonce, key from env/KMS
    nonce = os.urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(data)
    return nonce, ct, tag

def decrypt_gcm(
    nonce: bytes,
    ciphertext: bytes,
    tag: bytes,
    key: bytes,
) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def reset_token() -> str:
    # FIX: CSPRNG
    import secrets
    return secrets.token_urlsafe(16)

if __name__ == "__main__":
    key = bytes.fromhex(os.environ.get("ENC_KEY_HEX", os.urandom(32).hex()))
    h = store_password("password123")
    print("argon2 ok:", verify_password(h, "password123"))
    print("gcm:", encrypt_gcm(b"secret", key))
    print("token:", reset_token())

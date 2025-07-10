import hashlib


def sha1_bytes(data: bytes) -> str:
    """Calculate SHA1 hash of binary data and return uppercase hex string"""
    return hashlib.sha1(data).hexdigest().upper()

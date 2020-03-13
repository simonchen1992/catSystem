import hashlib

def to_md5_hex(message):
    return hashlib.md5(message.encode()).hexdigest()
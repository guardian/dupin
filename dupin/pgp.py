from pgpy import PGPKey, PGPMessage


def encrypt(contents, key):
    message = PGPMessage.new(contents)
    encrypted = key.encrypt(message)
    return str(encrypted)

def parse_key(key_str):
    key = PGPKey()
    key.parse(key_str)
    return key

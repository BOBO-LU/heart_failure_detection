import gzip
import json
import hashlib

def get_hash(data):
    if not isinstance(data, (str, int, tuple)):
        raise ValueError(f'Wrong type in get_hash() {data.__class__.__name__}')
    if isinstance(data, (str, int)):
        data = [data]
    hasher = hashlib.sha1(''.encode('utf-8'))
    for value in data:
        if not isinstance(value, (str, int)):
            raise ValueError(f'get_hash was called with type {value.__class__.__name__}')
        hasher.update(str(value).encode('utf-8'))
    return hasher.hexdigest()
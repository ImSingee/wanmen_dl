import sys
import time
import hashlib
from config import CONFIG


def get_token():
    time_str = hex(int(time.time()))[2:]

    md5 = hashlib.md5()
    md5.update('5ec029c599f7abec29ebf1c50fcc05a0'.encode(encoding='utf-8'))
    md5.update(time_str.encode(encoding='utf-8'))
    token = md5.hexdigest()

    return time_str, token


def get_headers():
    time_str, token = get_token()

    return {
        'Authorization': CONFIG["Authorization"],
        'User-Agent': CONFIG['UserAgent'],
        'x-sa': '9e2fc61b78106962a1fa5c5ba6874acaaf0cabfecb6f85ae2d4a082b672b9139f1466529572da95c36dd39a7cf9c8444',
        'accept': 'vnd.wanmen.v9+json',
        'x-app': 'uni',
        'x-platform': 'web',
        'x-time': time_str,
        'x-token': token,
    }


def to_name(title):
    title = title.replace('\\', ' ', sys.maxsize)
    title = title.replace('/', ' ', sys.maxsize)
    title = title.replace(':', ' ', sys.maxsize)
    title = title.replace('*', ' ', sys.maxsize)
    title = title.replace('?', ' ', sys.maxsize)
    title = title.replace('"', ' ', sys.maxsize)
    title = title.replace('<', ' ', sys.maxsize)
    title = title.replace('>', ' ', sys.maxsize)
    title = title.replace('|', ' ', sys.maxsize)

    return title

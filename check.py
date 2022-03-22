import os
import sys
import time

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from config import CONFIG
from m3u8 import download
from utils import to_name, get_headers, requests_get


def check_done(course_id: str, course_name: str, base_dir: str):
    course_name = to_name(course_name)
    course_dir = os.path.join(base_dir, course_name)

    done_file = os.path.join(course_dir, ".done")

    if os.path.exists(done_file):
        print(f"{course_id}\tDONE\t{course_name}")
    else:
        print(f"{course_id}\tDOWNLOADING\t{course_name}")


if __name__ == '__main__':
    course_id = sys.argv[1]

    if len(sys.argv) > 2:
        course_name = sys.argv[2]
    else:
        course_name = CONFIG['NameMap'][course_id]

    check_done(course_id, course_name, CONFIG['DownloadTo'])

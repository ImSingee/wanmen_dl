import os
import json

CONFIG = {
    "Authorization": "Bearer xxx",
    'UserAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    "DownloadTo": "/volume1/Courses/万门",
    "NumProcess": 32,
    "NameMap": {},
}

if os.path.exists("config.json"):
    with open("config.json") as f:
        o = json.load(f)
        CONFIG.update(o)

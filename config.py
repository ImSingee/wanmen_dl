import os
import json

CONFIG = {
    "Authorization": "Bearer xxx",
    "DownloadTo": "/volume1/Courses/万门",
    "NameMap": {},
}

if os.path.exists("config.json"):
    with open("config.json") as f:
        o = json.load(f)
        CONFIG.update(o)

import json
import sys
import os
import requests
from config import CONFIG
from utils import get_headers, to_name


def download_documents(course_id: str, course_name: str, base_dir: str):
    course_name = to_name(course_name)
    base_dir = os.path.join(base_dir, course_name)

    print(f"准备下载文档，开始获取 {course_name} 的课程信息")

    r = requests.get(f'https://api.wanmen.org/4.0/content/v2/courses/{course_id}', headers=get_headers())
    r.raise_for_status()

    info = r.json()
    documents = info['documents']

    print(f"共有 {len(documents)} 个资料文档")

    documents_dir = os.path.join(base_dir, "资料")
    os.makedirs(documents_dir, exist_ok=True)

    with open(os.path.join(documents_dir, "meta.json"), "r") as f:
        json.dump(documents, f)

    documents = sorted(documents, key=lambda x: x['order'])
    for i, doc in enumerate(documents, 1):
        name = f"{i} - {doc['name']}.{doc['ext']}"
        to = os.path.join(documents_dir, name)

        if os.path.exists(to):
            print(f"{name} 已经下载过 -> 跳过")
            continue
        else:
            print(f"{name} 开始下载")

        temp_to = to + ".tmp"

        with open(temp_to, "wb") as f:
            with requests.get(doc['url'], stream=True) as r:
                r.raise_for_status()

                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        os.rename(temp_to, to)

        print(f"{name} 下载完成")

    print(f"{course_name} 的所有资料下载完成")


if __name__ == '__main__':
    course_id = sys.argv[1]

    if len(sys.argv) > 2:
        course_name = sys.argv[2]
    else:
        course_name = CONFIG['NameMap'][course_id]

    download_documents(course_id, course_name, CONFIG['DownloadTo'])

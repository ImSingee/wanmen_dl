import os
import time
import hashlib
import requests
from config import CONFIG
from m3u8 import download
from utils import to_name


def get_token():
    time_str = hex(int(time.time()))[2:]

    md5 = hashlib.md5()
    md5.update('5ec029c599f7abec29ebf1c50fcc05a0'.encode(encoding='utf-8'))
    md5.update(time_str.encode(encoding='utf-8'))
    token = md5.hexdigest()

    return time_str, token


def fetch_course(course_id: str, course_name: str, base_dir: str):
    course_name = to_name(course_name)
    base_dir = os.path.join(base_dir, course_name)

    print(f"开始获取 {course_name} 的课程信息")

    time_str, token = get_token()

    r = requests.get(f'https://api.wanmen.org/4.0/content/lectures?courseId={course_id}&debug=1', headers={
        "Authorization": CONFIG["Authorization"],
        "X-Time": time_str,
        "X-Token": token,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.130 Safari/537.36'
    })

    if r.status_code != 200:
        print("错误 - 无法获取课程信息")
        print(r.status_code, r.reason)
        exit(-1)

    chapters = r.json()

    print("获取成功，即将开始下载")
    for i, chapter in enumerate(chapters, 1):
        chapter_name = to_name(chapter['name'])

        print(f"开始下载第 {i} 章：{chapter_name}")
        chapter_dir = os.path.join(base_dir, f"{i} - {chapter_name}")
        os.makedirs(chapter_dir, exist_ok=True)
        for j, lecture in enumerate(chapter['children'], 1):
            fetch_single(f'{i}-{j}', lecture, chapter_dir)
    print(f"{course_name} 下载完成")


def fetch_single(lecture_index: str, lecture_info: dict, base_dir: str):
    lecture_id = lecture_info['_id']
    lecture_name = lecture_index + ' ' + to_name(lecture_info['name'])

    print(f"[{lecture_name}] 正在准备下载")

    save_to = os.path.join(base_dir, lecture_name + '.mp4')

    if os.path.exists(save_to):
        print(save_to, "已存在 -> 跳过")
        return

    time_str, token = get_token()

    r = requests.get(f'https://api.wanmen.org/4.0/content/lectures/{lecture_id}?routeId=main&debug=1', headers={
        "Authorization": CONFIG["Authorization"],
        "X-Time": time_str,
        "X-Token": token,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.130 Safari/537.36'
    })

    if r.status_code != 200:
        print("错误 - 无法获取课程信息")
        print(r.status_code, r.reason)
        exit(-1)

    lecture_info = r.json()

    # print(lecture_info)

    if lecture_info.get('video'):
        video_m3u8_url = lecture_info['video']['hls']['pcHigh']
    else:
        video_m3u8_url = lecture_info['hls']['pcHigh']

    print(f"[{lecture_name}] 开始下载")
    download(video_m3u8_url, save_to)
    print(f"[{lecture_name}] 下载完成")

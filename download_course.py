import os
import sys
import requests
from config import CONFIG
from m3u8 import download
from utils import to_name, get_headers


def fetch_course(course_id: str, course_name: str, base_dir: str, *, lecture_id=None):
    course_name = to_name(course_name)
    base_dir = os.path.join(base_dir, course_name)

    print(f"开始获取 {course_name} 的课程信息")

    r = requests.get(f'https://api.wanmen.org/4.0/content/lectures?courseId={course_id}&debug=1', headers=get_headers())

    if r.status_code != 200:
        print("错误 - 无法获取课程信息")
        print(r.status_code, r.reason)
        exit(-1)

    chapters = r.json()

    print("获取成功，即将开始下载")

    if lecture_id is None:  # 下载全部
        fetch_all_chapters(chapters, base_dir)
        print(f"{course_name} 下载完成")
    else:
        found = False
        for i, chapter in enumerate(chapters, 1):
            chapter_name = to_name(chapter['name'])

            for j, lecture in enumerate(chapter['children'], 1):
                current_lecture_id = lecture['_id']

                if current_lecture_id != lecture_id:
                    continue

                found = True
                chapter_dir = os.path.join(base_dir, f"{i} - {chapter_name}")
                os.makedirs(chapter_dir, exist_ok=True)
                fetch_single(f'{i}-{j}', lecture, chapter_dir)
        if not found:
            print(f"lecture_id = {lecture_id} 的课程不存在")
            return


def fetch_all_chapters(chapters, base_dir: str):
    for i, chapter in enumerate(chapters, 1):
        fetch_chapter(i, chapter, base_dir)


def fetch_chapter(chapter_index: int, chapter: dict, base_dir: str):
    chapter_name = to_name(chapter['name'])

    print(f"开始下载第 {chapter_index} 章：{chapter_name}")
    chapter_dir = os.path.join(base_dir, f"{chapter_index} - {chapter_name}")
    os.makedirs(chapter_dir, exist_ok=True)
    for j, lecture in enumerate(chapter['children'], 1):
        fetch_single(f'{chapter_index}-{j}', lecture, chapter_dir)

    print(f"第 {chapter_index} 章：{chapter_name} 下载完成")


def fetch_single(lecture_index: str, lecture_info: dict, base_dir: str):
    lecture_id = lecture_info['_id']
    lecture_name = lecture_index + ' ' + to_name(lecture_info['name'])

    print(f"[{lecture_name}] 正在准备下载")

    save_to = os.path.join(base_dir, lecture_name + '.mp4')

    if os.path.exists(save_to):
        print(save_to, "已存在 -> 跳过")
        return

    r = requests.get(f'https://api.wanmen.org/4.0/content/lectures/{lecture_id}?routeId=main&debug=1', headers=get_headers())

    if r.status_code != 200:
        print("错误 - 无法获取课程信息")
        print(r.status_code, r.reason)
        exit(-1)

    lecture_info = r.json()

    # print(lecture_info)

    if lecture_info.get('video'):
        video_m3u8_url = lecture_info['video']['hls']['pcHigh']
        video_m3u8_url_mid = lecture_info['video']['hls']['pcMid']
    else:
        video_m3u8_url = lecture_info['hls']['pcHigh']
        video_m3u8_url_mid = lecture_info['hls']['pcMid']

    print(f"[{lecture_name}] 开始下载")
    download(video_m3u8_url, video_m3u8_url_mid, save_to)
    print(f"[{lecture_name}] 下载完成")


if __name__ == '__main__':
    course_id = sys.argv[1]

    if len(sys.argv) > 2:
        course_name = sys.argv[2]
    else:
        course_name = CONFIG['NameMap'][course_id]

    if len(sys.argv) > 3:
        lecture_id = sys.argv[3]
    else:
        lecture_id = None

    fetch_course(course_id, course_name, CONFIG['DownloadTo'], lecture_id=lecture_id)

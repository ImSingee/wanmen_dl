import os
import sys
import time

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from config import CONFIG
from m3u8 import download
from utils import to_name, get_headers, requests_get


def fetch_course(course_id: str, course_name: str, base_dir: str, *, lecture_id=None):
    course_name = to_name(course_name)
    course_dir = os.path.join(base_dir, course_name)

    print(f"开始获取 {course_name} 的课程信息")

    r = requests_get(f'https://api.wanmen.org/4.0/content/lectures?courseId={course_id}&debug=1', headers=get_headers(), timeout=2)

    if r.status_code != 200:
        print("错误 - 无法获取课程信息")
        print(r.status_code, r.reason)
        exit(-1)

    chapters = r.json()

    print("获取成功，即将开始下载")

    if lecture_id is None:  # 下载全部
        fetch_all_chapters(chapters, course_dir)
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
                chapter_dir = os.path.join(course_dir, f"{i} - {chapter_name}")
                os.makedirs(chapter_dir, exist_ok=True)
                fetch_single(f'{i}-{j}', lecture, chapter_dir)
        if not found:
            print(f"lecture_id = {lecture_id} 的课程不存在")
            return


def fetch_all_chapters(chapters, course_dir: str):
    done_file = os.path.join(course_dir, ".done")

    if os.path.exists(done_file):
        print("Already done, auto skip")
        print("If you want to re-download, please run")
        print(f"> rm -i '{done_file}'")
        return

    if CONFIG['NumProcess'] != 1:
        if CONFIG['NumProcess'] == 0:
            CONFIG['NumProcess'] = os.cpu_count()

        fetch_all_chapters_with_multiprocessing(chapters, course_dir)
    else:
        fetch_all_chapters_with_single_thread(chapters, course_dir)

    with open(os.path.join(course_dir, ".done"), 'w') as f:
        f.write(str(time.time()))


def fetch_all_chapters_with_single_thread(chapters, base_dir: str):
    with Session() as session:
        for chapter_index, chapter in enumerate(chapters, 1):
            chapter_name = to_name(chapter['name'])

            print(f"开始下载第 {chapter_index} 章：{chapter_name}")
            chapter_dir = os.path.join(base_dir, f"{chapter_index} - {chapter_name}")
            os.makedirs(chapter_dir, exist_ok=True)

            for j, lecture in enumerate(chapter['children'], 1):
                fetch_single(f'{chapter_index}-{j}', lecture, chapter_dir, session=session)

            print(f"第 {chapter_index} 章：{chapter_name} 下载完成")


def fetch_all_chapters_with_multiprocessing(chapters, base_dir: str):
    # from multiprocessing import Pool
    from multiprocessing.pool import ThreadPool as Pool

    errors = []
    with Pool(CONFIG['NumProcess']) as p:
        for chapter_index, chapter in enumerate(chapters, 1):
            chapter_name = to_name(chapter['name'])
            chapter_dir = os.path.join(base_dir, f"{chapter_index} - {chapter_name}")
            os.makedirs(chapter_dir, exist_ok=True)

            for j, lecture in enumerate(chapter['children'], 1):
                # 预先跳过
                tip = should_skip(f'{chapter_index}-{j}', lecture, chapter_dir)
                if tip is not None:
                    print(tip)
                    continue

                # 加入下载队列
                p.apply_async(fetch_single, (f'{chapter_index}-{j}', lecture, chapter_dir), error_callback=lambda err: errors.append(err))

        p.close()
        p.join()

    if len(errors) != 0:
        for i, e in enumerate(errors, 1):
            print(f"Error {i}: {e}")

        raise errors[0]


def ensure_session(f):
    def inner(*args, **kwargs):
        session = kwargs.get('session')

        if session is None:
            with Session() as session:
                session.mount('https://api.wanmen.org', HTTPAdapter(max_retries=5))
                kwargs['session'] = session
                return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return inner


def should_skip(lecture_index: str, lecture_info: dict, base_dir: str):
    lecture_name = lecture_index + ' ' + to_name(lecture_info['name'])
    save_to = os.path.join(base_dir, lecture_name + '.mp4')

    if os.path.exists(save_to):
        return f"{save_to} 已存在 -> 跳过"


@ensure_session
def fetch_single(lecture_index: str, lecture_info: dict, base_dir: str, *, session):
    lecture_id = lecture_info['_id']
    lecture_name = lecture_index + ' ' + to_name(lecture_info['name'])

    print(f"[{lecture_name}] 正在准备下载")

    save_to = os.path.join(base_dir, lecture_name + '.mp4')

    if os.path.exists(save_to):
        print(save_to, "已存在 -> 跳过")
        return

    r = session.get(f'https://api.wanmen.org/4.0/content/lectures/{lecture_id}?routeId=main&debug=1', headers=get_headers(), timeout=2)

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
    download(session, video_m3u8_url, video_m3u8_url_mid, save_to)
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

import os
from typing import List
import requests
from urllib.parse import urljoin


def fetch(url: str) -> str:
    print("Fetching", url)
    r = requests.get(url)
    if r.status_code != 200:
        print("Fetch fail, status =", r.status_code)
        exit(-2)
    return r.content.decode()


def parse(m3u8: str) -> List[str]:
    lines = m3u8.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            result.append(line)

    return result


def download(url: str, save_to: str, *, full=False):
    m3u8 = parse(fetch(url))

    if full:
        print(f"获取 m3u8 文件成功，该文件共有 {len(m3u8)} 个片段")
    else:
        m3u8 = m3u8[1:-1]  # 忽略第一个和最后一个片段（课程头尾）
        print(f"获取 m3u8 文件成功，该文件共有 {len(m3u8)} 个片段（已经忽略首尾片段）")

    part_file = save_to + '.part'
    with open(part_file, 'wb') as f:
        # m3u8 文件不设定下载缓存
        for i, line in enumerate(m3u8, 1):
            print(f"\r正在下载第 {i}/{len(m3u8)} 个文件片段", end='')
            ts_url = urljoin(url, line)
            times = 3
            while times >= 0:
                try:
                    r = requests.get(ts_url, timeout=5)
                    if r.status_code != 200:
                        raise RuntimeError()

                    f.write(r.content)
                    break
                except Exception as e:
                    print("遇到错误，重试", e)
                    times -= 1
            if times < 0:
                print("遇到错误，多次重试仍失败 -> 终止")
                exit(-1)
    print()

    mp4_part_file = save_to + '.part.mp4'
    ffmpegConvertToMp4(part_file, mp4_part_file)

    os.remove(part_file)
    os.rename(mp4_part_file, save_to)

    print("下载完成！")


def ffmpegConvertToMp4(input_file_path, output_file_path):
    code = os.system(f'ffmpeg -y -loglevel error -i "{input_file_path}" -bsf:a aac_adtstoasc -vcodec copy -acodec copy "{output_file_path}"')
    if code != 0:
        raise RuntimeError("无法转换为 mp4")
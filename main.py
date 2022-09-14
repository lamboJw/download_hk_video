# -*- encoding=utf-8 -*-
import os.path
from urllib.parse import urlparse, parse_qs
from spider import get_video_url
from m3u8 import M3U8
from base_path import BASE_PATH

cur_video_url = None
output_path = None
output_filename = None


def download_video(url):
    global cur_video_url, output_path
    video_url, video_name = get_video_url(url)
    if video_url is None:
        raise AttributeError("获取m3u8链接失败")
    if video_name is None:
        raise AttributeError("获取视频名称失败")
    print(video_name)
    dir_path = os.path.join(output_path, video_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    info = urlparse(video_url)
    query_info = parse_qs(info.query).get("videourl")[0]
    query_url = query_info.split(",")
    next_url = "https://www.gq1000.com" + query_url[0]
    cur_episode = int(query_url[-1]) + 1
    episode_dir_name = os.path.join(dir_path,
                                    video_name + "-" + ("0" if cur_episode < 10 else "") + str(cur_episode))
    for i in range(1, len(query_url) - 3):
        if query_url[i].__len__() > 0:
            m3u8_obj = M3U8(query_url[i], episode_dir_name, i - 1)
            m3u8_obj.download_slice()
            m3u8_obj.combine_video()
    os.rmdir(episode_dir_name)
    if cur_video_url != query_url[0]:
        cur_video_url = query_url[0]
        download_video(next_url)


if __name__ == "__main__":
    try:
        base_url = input("请输入要下载电视剧的第一集链接：")
        while base_url.__len__() == 0 or not base_url.startswith("https://www.gq1000.com"):
            if base_url.__len__() == 0:
                base_url = input("请输入要下载电视剧的第一集链接：")
            else:
                base_url = input("电视剧链接必须是 https://www.gq1000.com 网站中的链接：")

        base_url_info = urlparse(base_url)
        cur_video_url = base_url_info.path
        output_path = os.path.join(BASE_PATH, "output")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        download_video(base_url)
    except Exception as e:
        print("捕获错误：", e)
    finally:
        os.system("pause")

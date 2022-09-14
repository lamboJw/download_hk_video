# -*- encoding=utf-8 -*-
import os.path
from urllib.parse import urlparse, parse_qs
from spider import get_video_url
import getopt
import sys
from m3u8 import M3U8

cur_video_url = None
dir_path = None
output_filename = None


def download_video(url):
    global cur_video_url, dir_path, output_filename
    video_url = get_video_url(url)
    if video_url is None:
        raise AttributeError("获取m3u8链接失败")
    info = urlparse(video_url)
    query_info = parse_qs(info.query).get("videourl")[0]
    query_url = query_info.split(",")
    next_url = "https://www.gq1000.com" + query_url[0]
    cur_episode = int(query_url[-1]) + 1
    episode_dir_name = os.path.join(dir_path,
                                    output_filename + "-" + ("0" if cur_episode < 10 else "") + str(cur_episode))
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
    opts, args = getopt.getopt(sys.argv[1:], "hu:o:", ["help", "url=", "output="])
    base_url = None
    output_filename = None
    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
            print("-u 或--url 传入要下载的剧集，-o 或 --output 传入剧集名称，然后就会自动下载整个剧集到项目目录中的output文件夹")
        elif opt == "-u":
            if arg.startswith("="):
                base_url = arg[1:]
            else:
                base_url = arg
        elif opt == "--url":
            base_url = arg
        elif opt == "-o":
            if arg.startswith("="):
                output_filename = arg[1:]
            else:
                output_filename = arg
        elif opt == "--output":
            output_filename = arg
        else:
            continue

    if base_url is None or output_filename is None:
        raise ValueError("必须传入请求的地址和保存的文件名")

    base_url_info = urlparse(base_url)
    cur_video_url = base_url_info.path
    output_path = os.path.join(os.path.dirname(__file__), "output")
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    dir_path = os.path.join(output_path, output_filename)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    download_video(base_url)

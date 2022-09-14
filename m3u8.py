# -*- encoding=utf-8 -*-
import multiprocessing
import os
import re
import urllib3
from urllib.parse import urlparse
from threading import Thread

# TODO 多进程下载任务，为每个进程单独创建连接池
http = urllib3.PoolManager(timeout=6.0)
download_type = "thread"  # thread 或 normal


class M3U8(object):
    episode_dir_name = None
    index = None
    content = None
    slice_list = []
    dir_path = None
    m3u8_host = None

    def __init__(self, url, episode_dir_name, index):
        url_info = urlparse(url)
        self.m3u8_host = url_info.scheme + "://" + url_info.netloc
        self.episode_dir_name = episode_dir_name
        self.index = index
        r = http.request("get", url, headers={"referer": "https://www.gq1000.com/"})
        self.content = r.data.decode("utf-8")
        result = re.findall(r"#EXT-X-STREAM-INF:.*?BANDWIDTH=(\d*).*?\n(.*?)\n", self.content)
        if result.__len__() > 0:
            max_m3u8_url = ""
            max_bandwidth = ""
            for item in result:
                if item[0] > max_bandwidth:
                    max_m3u8_url = item[1]
            if not max_m3u8_url.startswith("http"):
                max_m3u8_url = self.m3u8_host + max_m3u8_url
            r = http.request("get", max_m3u8_url, headers={"referer": "https://www.gq1000.com/"})
            self.content = r.data.decode("utf-8")
        self.get_slice_url()
        self.get_dir_path()

    def get_slice_url(self):
        self.slice_list = re.findall(r'#EXTINF:\d*\.?\d*?,\n(.*?)\n', self.content)

    def get_dir_path(self):
        if self.dir_path is None:
            if not os.path.exists(self.episode_dir_name):
                os.mkdir(self.episode_dir_name)
            index_path = os.path.join(self.episode_dir_name, str(self.index))
            if not os.path.exists(index_path):
                os.mkdir(index_path)
            self.dir_path = index_path

    def download_slice(self):
        pool = multiprocessing.Pool(4)
        i = 0
        step = 20
        max_index = self.slice_list.__len__() - 1
        while i < self.slice_list.__len__():
            start = i
            end = i + step
            if end > max_index:
                end = -1
            url_list = self.slice_list[start:end]
            pool.apply_async(func=_do_download, args=(start, url_list, self.dir_path, self.m3u8_host))
            i = i + step
        pool.close()
        pool.join()

    def combine_video(self):
        output_name = os.path.split(self.episode_dir_name)[1] + ".mp4"
        with open(os.path.join(self.episode_dir_name, "..", output_name), "ab") as f:
            for i in range(0, self.slice_list.__len__() - 1):
                slice_path = os.path.join(self.dir_path, str(i))
                with open(slice_path, "rb") as f1:
                    f.write(f1.read())

        for i in range(0, self.slice_list.__len__() - 1):
            slice_path = os.path.join(self.dir_path, str(i))
            os.remove(slice_path)
        os.rmdir(self.dir_path)


def _do_download(start, url_list, dir_path, host):
    threads = []
    for i in range(len(url_list)):
        url = url_list[i]
        if not url.startswith("http"):
            url = host + url
        if download_type == "normal":
            with open(os.path.join(dir_path, str(i + start)), 'wb') as f:
                result = http.request('get', url)
                if result.status == 200:
                    f.write(result.data)
        else:
            thread = Thread(target=_thread_download, args=(url, os.path.join(dir_path, str(i + start))))
            threads.append(thread)
    if threads.__len__() > 0:
        for t in threads:
            t.start()
        for t in threads:
            t.join()


def _thread_download(url, dir_path):
    with open(dir_path, 'wb') as f:
        result = http.request('get', url)
        if result.status == 200:
            f.write(result.data)

# -*- encoding=utf-8 -*-
import multiprocessing
import os
import re

import pathlib2
import urllib3

http = urllib3.PoolManager()


class M3U8(object):
    episode_dir_name = None
    index = None
    content = None
    slice_list = []
    dir_path = None

    def __init__(self, url, episode_dir_name, index):
        self.episode_dir_name = episode_dir_name
        self.index = index
        r = http.request("get", url, headers={"referer": "https://www.gq1000.com/"})
        self.content = r.data.decode("utf-8")
        self.get_slice_url()
        self.get_dir_path()

    def get_slice_url(self):
        self.slice_list = re.findall(r'https?:\/\/.*', self.content)

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
        step = 10
        max_index = self.slice_list.__len__() - 1
        while i < self.slice_list.__len__():
            start = i
            end = i + step
            if end > max_index:
                end = -1
            url_list = self.slice_list[start:end]
            pool.apply_async(func=_do_download, args=(start, url_list, self.dir_path))
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


def _do_download(start, url_list, dir_path):
    for i in range(len(url_list)):
        url = url_list[i]
        with open(os.path.join(dir_path, str(i + start)), 'wb') as f:
            result = http.request('get', url)
            if result.status == 200:
                f.write(result.data)

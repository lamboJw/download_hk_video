# -*- encoding=utf-8 -*-
import os
import sys
import shutil

from base_path import get_base_path

BASE_PATH = get_base_path()


def remove_dir(path):
    if not os.path.exists(path):
        return
    for file in os.scandir(path):
        cur_path = os.path.join(path, file)
        if os.path.isfile(cur_path):
            os.remove(cur_path)
        else:
            remove_dir(cur_path)
    os.rmdir(path)


def copy_dir(source, target):
    if sys.platform.startswith('win'):
        os.system(f"xcopy {source} {target} /I/E/Q")
    else:
        os.system(f"cp -R {source} {target}")


if __name__ == "__main__":
    result = os.popen(f"pyinstaller -F {os.path.join(BASE_PATH, 'main.py')}")
    last_line = result.readlines()
    remove_dir(os.path.join(BASE_PATH, "build"))
    dist_dir = os.path.join(BASE_PATH, "dist")
    if not os.path.exists(os.path.join(dist_dir, "config.json")):
        shutil.copy(os.path.join(BASE_PATH, 'config.json'), os.path.join(dist_dir, 'config.json'))
    if not os.path.exists(os.path.join(dist_dir, "lib")):
        copy_dir(os.path.join(BASE_PATH, 'lib'), os.path.join(dist_dir, 'lib'))
    if not os.path.exists(os.path.join(dist_dir, "webDriver")):
        copy_dir(os.path.join(BASE_PATH, 'webDriver'), os.path.join(dist_dir, 'webDriver'))
        remove_dir(os.path.join(dist_dir, 'webDriver', '__pycache__'))
        if os.path.exists(os.path.join(dist_dir, 'webDriver', '__init__.py')):
            os.remove(os.path.join(dist_dir, 'webDriver', '__init__.py'))

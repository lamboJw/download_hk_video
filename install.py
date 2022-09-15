# -*- encoding=utf-8 -*-
import os
from base_path import get_base_path

if __name__ == "__main__":
    result = os.popen(f"cd {get_base_path()} && pyinstaller -F {os.path.join(get_base_path(), 'main.py')}")
    last_line = result.readlines()[-1]
    print(last_line)
    # TODO 删除build文件夹，判断dist是否存在lib、webDriver、config.json文件，无则复制

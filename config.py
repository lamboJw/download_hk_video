import json
import os

from base_path import get_base_path

config_path = os.path.join(get_base_path(), "config.json")
if not os.path.exists(config_path):
    print("配置文件不存在")
    os.system("pause")
    quit()
with open(config_path, encoding='utf-8') as f:
    config = json.load(f)


def get_config(key, default=None):
    return config.get(key, default)

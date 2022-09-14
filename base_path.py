import os
import sys


def get_base_path():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(os.path.realpath(sys.executable))
    else:
        return os.path.dirname(__file__)

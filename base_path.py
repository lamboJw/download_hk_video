import os
import sys

if hasattr(sys, 'frozen'):
    BASE_DIR = os.path.dirname(os.path.realpath(sys.executable))
else:
    BASE_PATH = os.path.dirname(__file__)

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
DATA_DB = os.path.join(DATA_DIR, 'data.json')
EXTS_DIR = os.path.join(DATA_DIR, 'extensions')

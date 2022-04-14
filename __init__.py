from asyncio.log import logger
import traceback
import io
import subprocess 
import os
import json 
import logging 
import sys 
import importlib
from time import time 
from contextlib import redirect_stdout 
from pathlib import Path 
from configparser import BasicInterpolation, ConfigParser
from math import * 
import bpy 
import addon_utils

item_list = [
    'Prism Ares', 'Prism Ghost', 'Prism Knife', 'Prism Phantom', 'Prism Operator', 'Prism Spectre'
]

Selected_item = ''


_TEXTURE_FORMAT = ".png" #Can have DDS, TGA, PNG
_SAVE_JSON = False
_APPEND = True
_DEBUG = False
_FOR_UPLOAD = True
_PROP_CHECK = False

stdout = io.StringIO()
os.system("cls")
sys.dont_write_bytecode = True

CWD = Path(bpy.context.space_data.text.filepath).parent
VAL_EXPORT_FOLDER = os.path.join(CWD, "export")
JSON_FOLDER = Path(os.path.join(CWD, "export", "JSONs"))
JSON_FOLDER.mkdir(parents=True, exist_ok=True)

config = ConfigParser(interpolation=BasicInterpolation())
config.read(os.path.join(CWD.__str__(), 'settings.ini'))

VAL_KEY = config["VALORANT"]["UE_AES"]
VAL_PAKS_PATH = config["VALORANT"]["PATH"]
WHITE_RGB = (1, 1, 1, 1)
BLACK_RGB = (0, 0, 0, 0)

LOGFILE = os.path.join(CWD, 'yo.log')

if Path(LOGFILE).exists():
    with open(LOGFILE, "r+") as f:
        f.truncate(0)

try:
    logger
except NameError:
    logger = logging.getLogger("yo")
    logger.setLevel(logging.info)
    
    fh = logging.FileHandler(LOGFILE)
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    if logger.handlers.__len__() == 0:
        logger.addHandler(fh)
        logger.addHandler(ch)

try:
    sys.path.append(os.path.join(CWD.__str__()))
    sys.path.append(os.path.join(CWD.__str__(), "utils"))

    from utils import _umaplist
    from utils import blenderUtils
    from utils import common
    from utils.UE4Parse.Objects.EUEVersion import EUEVersion
    from utils.UE4Parse.provider.Provider import Provier, FGame

    importlib.reload(_umaplist)
    importlib.reload(blenderUtils)
    importlib.reload(common)
except Exception:
    traceback.print_exc()

def timer(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        logger.info(f'Function {func.__name__!r} executed in {(t2-t1):.3f}s')
        return result
    return wrap_func

def shorten_path(file_path, length):
    return f'..\{Path(*Path(file_path).parts[-length:])}'

def save_json(p: str, d):
    with open(p, 'w') as jsonfile:
        pass
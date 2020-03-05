import os
from settings import FILEPREFIX,FILESUFFIX,DATA_DIRNAME

LogPath = DATA_DIRNAME

def gen_logfile(name,txt):
    PREFIX = name + "." + FILEPREFIX
    SUFFIX = FILESUFFIX
    LOGS = DATA_DIRNAME
    name = ".".join([PREFIX,txt,SUFFIX])
    path = os.path.join(LOGS,name)
    return path

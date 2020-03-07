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

def oldest_files(files):
    old_json,old_pickle,op,oj = None,None,None,None
    for fp in files:
        path = fp.parent
        parts = fp.name.split(".")
        age = sum([int(i) for i in parts if i.isnumeric()])
        if "pickle" in parts:
            if not old_pickle or age > op:
                old_pickle = path / fp
                op = age
        elif "json" in parts:
            if not old_json or age > oj:
                old_json = path / fp
                oj = age
    return old_json,old_pickle

import os
from os.path import realpath
from pathlib import Path

FILEPREFIX = "torrent"
PICKLESUFFIX = "pickle.bin"
JSONSUFFIX = "log.json"

def log_filename(name,txt,ext): # -> {pathlib.Path()}
    """ ::


        \CR
    Returns --> {pathlib.Path()}
        name {str} - session name
               txt {str} - text for finle number
               ext {str} - "json" | "pickle"
    """
    PREFIX = name + "." + FILEPREFIX
    SUFFIX = PICKLESUFFIX if "pickle" in ext else JSONSUFFIX
    logPath = Path(__file__).resolve().parent.parent / "data"
    name = ".".join([PREFIX,txt,SUFFIX])
    path = os.path.join(logPath,name)
    return path

def latest_log(files,ext):
    """ Returns --> {pathlib.Path}
        Parses list of files or path onjects for
        the last latest logfile.\n
    Args:--> \t \t \n \n
        files {Path|str} - files in log directory
        ext {str} - "json" or "pickle"
    """
    latest = num = path = None
    for fp in files:
        if isinstance(fp,str):
            fp = Path(fp)
        path = fp.parent
        parts = fp.name.split(".")
        if not ext in parts:
            continue
        age = sum([int(i) for i in parts if i.isnumeric()])
        if not latest or age > num:
            latest = path / fp
            num = age
    return path / latest

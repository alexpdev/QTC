import os
import sys
import json
from src.mixins import SessionMixin
from conf import FILESUFFIX,FILEPREFIX,DATA_DIRNAME
from pathlib import Path
from datetime import datetime


def logfile(name,txt):
    PREFIX = name + FILEPREFIX
    SUFFIX = FILESUFFIX
    LOGS = DATA_DIRNAME
    name = "".join([PREFIX,txt,SUFFIX])
    path = os.path.join(LOGS,name)
    return path

class Session(SessionMixin):
    logs = DATA_DIRNAME

    def __init__(self,name=None,**kwargs):
        self.name = name
        self.url = kwargs["url"]
        self.credentials = kwargs["credentials"]
        self.response = None
        self.cookies = None
        self.logfile = self._logfile

    def _logfile(self,text):
        return logfile(self.name,text)

    def log(self,data):
        stamp = datetime.isoformat(datetime.now())
        files = [i for i in self.logs.iterdir() if self.name in i.name]
        if files:
            logdata,logpath = self.log_vars({stamp:data},files[-1])
        else:
            logdata = {stamp:data}
            logpath = self.logfile("1")
        json.dump(logdata,open(logpath,"wt"))
        return

    def log_vars(self,data,path):
        if self.is_full(path):
            logdata = json.load(open(path,"rt")).update(data)
            logpath = path
        else:
            logdata = data
            logpath = next_log_path(path)
        return logdata,logpath

    def is_full(self,path):
        size = path.stat().st_size
        if size < 1000000:
            return True
        return False

    def next_log_path(self,path):
        parts = path.name.split(".")
        num = int(parts[-3])
        if num < 9:
            name = ".".join(parts[1:-3] + [str(num+1)])
        else:
            name = ".".join(parts[1:-2] + ["1"])
        return self.logfile(name)

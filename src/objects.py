import os
import sys
import json
import src
from pathlib import Path
from datetime import datetime

PREFIX = src._vars["prefix"]
SUFFIX = src._vars["suffix"]
LOGS = src._vars["data"]

def logfile(txt):
    name = "".join([PREFIX,txt,SUFFIX])
    path = os.path.join(LOGS,name)
    return path


class RequestError(Exception):
    pass

class Session:
    logs = LOGS

    def __init__(self,*args,**kwargs):
        if not args:
            self.credentials = kwargs["credentials"]
            self.url = kwargs["base_url"]
            self.cookies = kwargs["cookies"]
            self.response = kwargs["response"]
        else:
            self.url = args[0]
            self.credentials = args[1]
            self.response = args[2]
            self.cookies = self.response.cookies
        self.timestamp = datetime.isoformat()
        self.logfile = logfile
        self.session_id = None

    def log(self,data):
        stamp = datetime.isoformat(datetime.now())
        files = sorted(list(self.logs.iterdir()))
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

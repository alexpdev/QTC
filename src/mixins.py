import os
import sys
import json
import requests
from datetime import datetime

from src.utils import gen_logfile,LogPath


class RequestError(Exception):
    pass


class RequestMixin:

    def login(self,credentials=None,url=None):
        url = self.url + "auth/login"
        response = requests.get(url,params=self.credentials)
        self.check_response(response)
        self.response = response
        self.cookies = response.cookies
        return response

    def check_response(self,response):
        if response.status_code == 200:
            return True
        else:
            raise RequestError

    def get_info(self):
        url = self.url + "torrents/info"
        response = requests.get(url,cookies=self.cookies)
        self.check_response(response)
        data = response.json()
        return data



class LoggerMixin:

    def get_logfile(self,txt):
        return gen_logfile(self.name,txt)

    def log(self,data):
        stamp = datetime.isoformat(datetime.now())
        files = [i for i in self.logs.iterdir() if self.name in i.name]
        files = sorted(files,key=lambda x: x.name)
        if files:
            logdata,logpath = self.log_vars({stamp:data},files[-1])
        else:
            logdata = {stamp:data}
            logpath = self.get_logfile("1")
        json.dump(logdata,open(logpath,"wt"))
        return

    def log_vars(self,data,path):
        if not self.is_full(path):
            logdata = json.load(open(path,"rt"))
            if logdata: logdata.update(data)
            logpath = path
        else:
            logdata = data
            logpath = self.next_log_path(path)
        return logdata,logpath

    def is_full(self,path):
        size = path.stat().st_size
        if size < 1000000:
            return False
        return True

    def next_log_path(self,path):
        parts = path.name.split(".")
        num = int(parts[-3])
        if num < 9:
            name = ".".join(parts[2:-3] + [str(num+1)])
        else:
            name = ".".join(parts[2:-2] + ["1"])
        return self.get_logfile(name)

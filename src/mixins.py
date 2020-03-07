"""
Backend for Logging with pickle
This is the default logging backend.
"""
# pickle log structure example:
#     PickleFile = {
#         torrent hash : {
#             "name" : example.torrent.name,
#             "magnent_uri" : magnet?=http://example.torrent.url,
#             "data" : {
#                 "ul" : 4385893493,
#                 "ratio" : 2.546,
#                 "timestamp" : "2020-03-05T01:44:39.367658"
#             }
#         }
#     }
#! /bin/python3
import os
import sys
import json
import pickle
import requests
from datetime import datetime

from src.utils import latest_log,log_filename


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


class BaseLogMixin:
    ignore_fields = ["max_ratio",
                     "seq_dl",
                     "dl_limit",
                     "up_limit",
                     "auto_tmm",
                     "force_start",
                     "seeding_time_limit",
                     "max_seeding_time",
                     "f_l_peice_prio"]

    def get_logfile(self,txt,ext):
        return log_filename(self.name,txt,ext)

    def is_full(self,path):
        max_data = 1000000 if "json" in path.name else 10000000
        size = path.stat().st_size
        if size < max_data:
            return False
        return True

    def nextPath(self,path,ext):
        parts = path.name.split(".")
        num = int(parts[-3])
        if num < 9:
            name = ".".join(parts[2:-3] + [str(num+1)])
        else:
            name = ".".join(parts[2:-2] + ["1"])
        return self.log_filename(name,ext)


class PickleLogMixin(BaseLogMixin):
    def log(self,data):
        stamp = datetime.isoformat(datetime.now())
        files = [i for i in self.logs.iterdir() if (self.name in i.name)
                                                and ("pickle" in i.name)]
        fp = latest_log(files,"pickle")
        logdata = self.filterData(stamp,data,pickle.load(open(fp,"rb")))
        pickle.dump(logdata,open(fp,"wb"))
        return

    def filterData(self,stamp,data,logdata):
        for item in data:
            int_data,str_data = self.pickle_data(stamp,item)
            if item["hash"] not in logdata:
                str_data["data"] = [int_data]
                logdata[item["hash"]] = str_data
            else:
                logdata[item["hash"]]["data"].append(int_data)
        return logdata

    def pickle_data(self,stamp,log_item):
        int_data,str_data = {"timestamp":stamp},{"session":self.name}
        for k,v in log_item.items():
            if k in self.ignore_fields: continue
            elif isinstance(v,str):
                str_data[k] = v
            else:
                int_data[k] = v
        return int_data,str_data


class JsonLogMixin(BaseLogMixin):
    def log(self,data):
        stamp = datetime.isoformat(datetime.now())
        files = [i for i in self.logs.iterdir() if
                (self.name in i.name) and ("json" in i.name)]
        js = latest_log(files,"json")
        logdata,logpath = self.log_vars_json(stamp,data,js)
        json.dump(logdata,open(logpath,"wt"))
        return

    def log_vars_json(self,stamp,data,path):
        if not self.is_full(path):
            logdata = json.load(open(path,"rt"))
            if logdata: logdata.update({stamp:data})
            logpath = path
        else:
            logdata = {stamp:data}
            logpath = self.next_log_path(path,"json")
        return logdata,logpath

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
from src.mixins import RequestMixin, JsonLogMixin, PickleLogMixin
from src.models import DataModel
from src.utils import log_filename
from settings import DATA_DIRNAME



# Pickle Backend Logging
""" Pickle log structure example
    ---
    File = {
        torrent_hash : {
            "hash" : torrent_hash,
            "name" : example.torrent.name,
            "data" : [{
                "timestamp" : "2020-03-05T01:44:39.367658"
                "ratio" : 2.546, ...
                },
                {
                "ul" : 4521548,
                "ratio" : .012, ...
                }, ...
            ]}
        },...
    }
"""

# Json backend Logging
""" Json file log format example:
    ---
    File = {
        timestamp : {
            [{
                "hash": "845743939FDSF",
                "name" : "some.example.torrent",
                "dl" : 4534564364,
                "ul" : 2345435,
                "ratio" : 0.0978
            }]
        }
    }
"""



class BaseSession(RequestMixin):
    logs = DATA_DIRNAME

    def __init__(self,name=None,url=None,credentials=None):
        self.name = name
        self.url = url
        self.credentials = credentials


class JsonSession(BaseSession,JsonLogMixin):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.models = dict()

    def load_models(self):
        if not self.models:
            for log in self.parse_logs():
                self.load_data(log)
        return self.models

    def find_torrent_models(self,torrent_hash):
        if torrent_hash in self.models:
            return self.models[torrent_hash]

    def parse_logs(self):
        for log in self.logs.iterdir():
            if self.name in log.name and "json" in log.name:
                yield log

    def load_data(self,path):
        data = json.load(open(path,"rt"))
        for stamp in data:
            lst = data[stamp]
            logtime = datetime.fromisoformat(stamp)
            self.add_models(lst,logtime)
        return

    def add_models(self,lst,logtime):
        for kwargs in lst:
            model = DataModel(self.name,logtime,**kwargs)
            h = model.hash
            if h in self.models:
                self.models[h].append(model)
            else:
                self.models[h] = [model]
        return

class Session(BaseSession,PickleLogMixin):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.models = dict()

    def find_models(self,model_hash):
        return self.models[model_hash]

    def get_models(self):
        if not self.models:
            self.load_models()
        return self.models

    def load_models(self):
        for log in self.logs.iterdir():
            if self.name in log.name and "pickle" in log.name:
                self.load_data(log)
        return

    def load_data(self,path):
        data = pickle.load(open(path,"rb"))
        for t_hash in data:
            self.models[t_hash] = []
            model = self.create_model(data[t_hash],t_hash)
        return

    def create_model(self,data,thash):
        kwargs = data.copy()
        for item in data["data"]:
            kwargs.update(item)
            if "client" not in kwargs:
                kwargs["client"] = self.name
            model = DataModel(**kwargs)
            self.models[thash].append(model)


class SessionManager:
    def __init__(self,**kwargs):
        self.name = "manager"
        self.sessions = {}

    def set_window(self,win):
        self.window = win
        return

    def add_session(self,session):
        if session.name not in self.sessions:
            self.sessions[session.name] = session
        return

    def search_models(self,model_hash):
        for name,session in self.sessions.items():
            if model_hash in session.models:
                models = session.models[model_hash]
                return models

    def get_models(self,session_name,model_hash):
        session = self.sessions[session_name]
        return session.find_models(model_hash)

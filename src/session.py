import os
import sys
import json
from pathlib import Path
from datetime import datetime
from src.mixins import RequestMixin, JsonLogMixin, PickleLogMixin
from src.models import DataModel
from src.utils import LogPath,gen_logfile




class BaseSession(RequestMixin):

    def __init__(self,name=None,url=None,credentials=None):
        self.name = name
        self.url = url
        self.credentials = credentials


class JsonSession(BaseMixin,JsonLogMixin):
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
    logs = LogPath

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

class Session(RequestMixin,PickleLogMixin):
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
    logs = LogPath

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._models = None

    @property
    def models(self):
        if self._models:
            return self._models
        self.load_models()

    @models.setter
    def models(self,models):
        pass

    def load_models(self):
        for log in self.logs.iterdir():
            if self.name in log.name and "pickle" in log.name:
                self.load_data(log)

    def load_data(self,path):
        data = pickle.load(open(path,"rb"))
        for thash in data:
            self.add_models(data,thash)
        return

    def add_models(self,data,thash):
        kwargs = {}
        for k,v in data.items():
            if k == "data":
                kwargs.update(v)
                continue
            kwargs[k] = v
        model = DataModel(**kwargs)

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

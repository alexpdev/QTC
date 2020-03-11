import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
from .mixins import RequestMixin,JsonBackend,PickleBackend
from .models import DataModel
from .utils import log_filename
from .backends import SqlBackend
from settings import DATA_DIRNAME


class BaseSession(RequestMixin):
    logs = DATA_DIRNAME

    def __init__(self,name=None,url=None,credentials=None):
        self.name = name
        self.url = url
        self.credentials = credentials


class SqlSession(BaseSession,SqlBackend):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._cursor = None
        self._connection = None
        self._models = {}
        self.get_db()

    @property
    def models(self):
        return self._models

    def get_session_torrents(self):
        self.select_where("static","client",self.name)
        for row in self.cur:
            print(row)



class JsonSession(BaseSession,JsonBackend):
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

class PickleSession(BaseSession,PickleBackend):
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
            session.get_session_torrents()
        return

    def search_models(self,model_hash):
        for name,session in self.sessions.items():
            if model_hash in session.models:
                models = session.models[model_hash]
                return models

    def get_models(self,session_name,model_hash):
        session = self.sessions[session_name]
        return session.find_models(model_hash)

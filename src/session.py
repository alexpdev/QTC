import os
import sys
import json
from pathlib import Path
from datetime import datetime
from src.mixins import RequestMixin,LoggerMixin
from src.models import DataModel
from src.utils import LogPath,gen_logfile


class Session(RequestMixin,LoggerMixin):
    logs = LogPath

    def __init__(self,name=None,url=None,credentials=None):
        self.name = name
        self.url = url
        self.credentials = credentials
        self.models = {}

    def parse_logs(self):
        for log in self.logs.iterdir():
            if self.name in log.name:
                yield log

    def load_models(self):
        if not self.models:
            for log in self.parse_logs():
                self.load_data(log)
        return self.models

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

    def find_models(self,model_hash):
        for name,session in self.sessions.items():
            if model_hash in session.models:
                models = session.models[model_hash]
                return models

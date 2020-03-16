import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
from src.mixins import QueryMixin
from src.window import Win
from src.serialize import Converter as Conv
from PyQt5.QtWidgets import QApplication

class BaseSession:
    def __init__(self,path,clients,*args,**kwargs):
        self.path = path
        self.clients = clients
        self.models = {}
        self.static_fields = ("hash", "client", "name",
                              "tracker", "magnet_uri",
                              "save_path", "total_size",
                              "added_on", "completion_on",
                              "state", "category", "tags")

        self.data_fields = ("hash", "client", "timestamp",
                            "ratio", "uploaded", "time_active",
                            "completed", "size", "downloaded",
                            "num_seeds", "num_leechs", "last_activity",
                            "seen_complete", "dlspeed", "upspeed",
                            "num_complete", "num_incomplete",
                            "downloaded_session", "uploaded_session")


class SqlSession(QueryMixin,BaseSession):
    def __init__(self,path,clients,*args,**kwargs):
        super().__init__(path,clients)
        self.path = path
        self.clients = clients

    def get_client_names(self):
        names = [i for i in self.clients]
        return names

    def get_torrent_names(self,client):
        table = "static"
        field = "client"
        rows = self.select_where(table,field,client)
        values = []
        for row in rows:
            v = (row["name"],row["hash"],row["client"])
            yield v

    def get_data_rows(self,torrent_hash,client):
        args = ("data","hash",torrent_hash)
        rows = self.select_where(*args)
        return Conv.convert_values(rows)


    def get_static_rows(self,torrent_hash,client):
        args = ("static","hash",torrent_hash)
        rows = self.select_where(*args)
        return Conv.convert_values(rows)


    def mainloop(self):
        app = QApplication(sys.argv)
        win = Win()
        win.assign_session(self)
        win.show()
        sys.exit(app.exec_())


## class JsonSession(BaseSession,JsonBackend):
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)
#         self.models = dict()

#     def load_models(self):
#         if not self.models:
#             for log in self.parse_logs():
#                 self.load_data(log)
#         return self.models

#     def find_torrent_models(self,torrent_hash):
#         if torrent_hash in self.models:
#             return self.models[torrent_hash]

#     def parse_logs(self):
#         for log in self.logs.iterdir():
#             if self.name in log.name and "json" in log.name:
#                 yield log

#     def load_data(self,path):
#         data = json.load(open(path,"rt"))
#         for stamp in data:
#             lst = data[stamp]
#             logtime = datetime.fromisoformat(stamp)
#             self.add_models(lst,logtime)
#         return

#     def add_models(self,lst,logtime):
#         for kwargs in lst:
#             model = DataModel(self.name,logtime,**kwargs)
#             h = model.hash
#             if h in self.models:
#                 self.models[h].append(model)
#             else:
#                 self.models[h] = [model]
#         return

# class PickleSession(BaseSession,PickleBackend):
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)
#         self.models = dict()

#     def find_models(self,model_hash):
#         return self.models[model_hash]

#     def get_models(self):
#         if not self.models:
#             self.load_models()
#         return self.models

#     def load_models(self):
#         for log in self.logs.iterdir():
#             if self.name in log.name and "pickle" in log.name:
#                 self.load_data(log)
#         return

#     def load_data(self,path):
#         data = pickle.load(open(path,"rb"))
#         for t_hash in data:
#             self.models[t_hash] = []
#             model = self.create_model(data[t_hash],t_hash)
#         return

#     def create_model(self,data,thash):
#         kwargs = data.copy()
#         for item in data["data"]:
#             kwargs.update(item)
#             if "client" not in kwargs:
#                 kwargs["client"] = self.name
#             model = DataModel(**kwargs)
#             self.models[thash].append(model)



import os
from datetime import datetime
import sqlite3

from src.mixins import QueryMixin, RequestMixin
from src.serialize import Converter as Conv



class DatabaseError(Exception):
    pass

class DatabasePathError(DatabaseError):
    pass

class LessThanAnHour(DatabaseError):
    pass

class BaseStorage(RequestMixin):
    def __init__(self,path,clients,*args,**kwargs):
        self.path = path

        self.clients = clients

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

    def make_client_requests(self, client):
        client_details = self.clients[client]
        url = client_details["url"]
        credentials = client_details["credentials"]
        resp = self.login(url=url, credentials=credentials)
        data = self.get_info(resp, url=url)
        return data

    def filter_static_fields(self, torrent):
        info = torrent.copy()
        for k in torrent:
            if k not in self.static_fields:
                del info[k]
        return info

    def filter_data_fields(self, torrent):
        info = torrent.copy()
        for k in torrent:
            if k not in self.data_fields:
                del info[k]
        return info


class SqlStorage(BaseStorage, QueryMixin):
    def __init__(self, path, clients, *args, **kwargs):
        super().__init__(path, clients)
        self.path = path
        self.clients = clients
        self.conn = None

    def log(self):
        if not self.check_path():
            CreatorScript(self.path,self.clients)
            self.get_connection()
        if not self.check_timelog():
            return "Not Now"
        data = []
        for client in self.clients:
            response = self.make_client_requests(client)
            for item in response:
                item["timestamp"] = self.timestamp
                item["client"] = client
                data.append(item)
        self.format_data(data)

    def check_timelog(self):
        timestamp = datetime.now()
        self.timestamp = datetime.isoformat(timestamp)
        rows = self.select_rows("stamps")
        for item in rows:
            print(tuple(item),item["timestamp"])
            row_stamp = datetime.fromisoformat(item["timestamp"])
            if (timestamp - row_stamp).seconds < 86400:
                return False
        self.log_timestamp(str(self.timestamp))
        return True

    def check_path(self):
        if os.path.isfile(self.path):
            self.get_connection()
            return True
        return False

    def format_data(self, data):
        vals = []
        for torrent in self.filter_new(data):
            columns, values, params = self.get_save_values(torrent)
            vals.append(tuple(values))
        if not vals: return
        return self.save_many_to_db(columns, vals, params, "data")

    def filter_new(self, data):
        for torrent in data:
            if self.torrent_exists("static", "hash", torrent["hash"]):
                yield self.filter_data_fields(torrent)
            else:
                self.create_new_torrent(torrent)

    def get_save_values(self,torrent):
        column,values,params = [],[],[]
        for k,v in torrent.items():
                column.append(k)
                values.append(v)
                params.append("?")
        return ", ".join(column), values, ", ".join(params)

    def create_new_torrent(self, torrent):
        staticFields = self.filter_static_fields(torrent)
        dataFields = self.filter_data_fields(torrent)
        self.save_to_db(staticFields, "static")
        self.save_to_db(dataFields, "data")
        return


class CreatorScript(SqlStorage):
    def __init__(self,path,clients,*args,**kwargs):
        super().__init__(path,clients,*args,**kwargs)
        self.path = path
        self.clients = clients
        self.datatypes = Conv.datatypes
        self.first_run_script()

    def first_run_script(self):
        self.conn = sqlite3.connect(self.path)
        stIn = [f'{i} {self.datatypes[i]["type"]}' for i in self.static_fields]
        dtIn = [f'{i} {self.datatypes[i]["type"]}' for i in self.data_fields]
        self.create_db_table(", ".join(stIn), "static")
        self.create_db_table(", ".join(dtIn), "data")
        self.create_db_table("timestamp TEXT","stamps")
        return True

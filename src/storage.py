import os
from datetime import datetime

from src.mixins import QueryMixin, RequestMixin
from src.serialize import Converter as Conv


class DatabaseError(Exception):
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

    def log(self):
        for client in self.clients:
            data = self.make_client_requests(client)
            self.log_data(client, data)


class SqlStorage(BaseStorage, QueryMixin):
    def __init__(self, path, clients, *args, **kwargs):
        super().__init__(path, clients)
        self.path = path
        self.clients = clients
        self.conn = None

    def check_path(self):
        if os.path.isfile(self.path):
            self.get_connection()
            return True
        return False

    def log_data(self, client, data):
        if not self.check_path():
            self.get_connection()
            sample = data[0]
            self.first_run_script(client, sample)
            del data[0]
        self.format_data(client, data)
        self.conn.close()

    def format_data(self, client, data):
        cols, vals = None, []
        for torrent in self.filter_new(client, data):
            data = self.filter_data_fields(torrent)
            columns, values, params = self.get_save_values(data)
            if cols and columns != cols:
                raise DatabaseError
            cols = columns
            vals.append(tuple(values))
        if vals: self.save_many_to_db(cols, vals, params, "data")
        return

    def filter_new(self, client, data):
        timestamp = datetime.isoformat(datetime.now())
        for torrent in data:
            torrent["client"] = client
            torrent["timestamp"] = timestamp
            if self.torrent_exists("static", "hash", torrent["hash"]):
                yield torrent
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

    def first_run_script(self, client, sample):
        timestamp = str(datetime.isoformat(datetime.now()))
        sample["client"] = client
        sample["timestamp"] = timestamp
        d_headers, s_headers = Conv.table_details(sample)
        static_headers = ", ".join(s_headers)
        self.create_db_table(static_headers, "static")
        data_headers = ", ".join(d_headers)
        self.create_db_table(data_headers, "data")
        staticFields = self.filter_static_fields(sample)
        self.save_to_db(staticFields, "static")
        dataFields = self.filter_data_fields(sample)
        self.save_to_db(dataFields, "data")
        return

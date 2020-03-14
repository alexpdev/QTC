import os
from datetime import datetime
# from settings import DB_PATH,DATA_DIR,CLIENTS
from src.serializer import table_details
from src.mixins import RequestMixin,QueryMixin

class BaseStorage(RequestMixin):
    def __init__(self,path,clients,*args,**kwargs):
        self.data_dir = path

        self.clients = clients

        self.static_fields = ("hash", "client", "name",
                              "tracker", "magnet_uri", "save_path",
                              "total_size", "added_on", "completion_on",
                              "state", "category", "tags")

        self.data_fields = ("hash", "client", "timestamp","ratio","uploaded",
        "time_active","completed","size","downloaded","num_seeds","num_leechs","last_activity", "seen_complete","dlspeed","upspeed","num_complete","num_incomplete","downloaded_session","uploaded_session")

    def make_client_requests(self,client):
        client_details = self.clients[client]
        url = client_details["url"]
        credentials = client_details["credentials"]
        resp = self.login(url=url,credentials=credentials)
        data = self.get_info(resp,url=url)
        return data

    def filter_static_fields(self,torrent):
        info = torrent.copy()
        for k in torrent:
            if k not in self.static_fields:
                del info[k]
        return info

    def filter_data_fields(self,torrent):
        info = torrent.copy()
        for k in torrent:
            if k not in self.data_fields:
                del info[k]
        return info

    def log(self):
        for client in self.clients:
            data = self.make_client_requests(client)
            self.log_data(client,data)


class SqlStorage(BaseStorage,QueryMixin):
    def __init__(self,path,clients,db_name,*args,**kwargs):
        super().__init__(path,clients)
        self.data_dir = path
        self.name = db_name
        self.clients = clients
        self.connect = None
        self.cursor = None

    @property
    def path(self):
        path = self.data_dir / self.name
        return path

    def check_path(self):
        if os.path.isfile(self.path):
            return True
        return False

    def log_data(self,client,data):
        if not self.check_path():
            sample = data[0]
            self.first_run_script(client,sample)
            del data[0]
        self.format_data(client,data)

    def format_data(self,client,data):
        timestamp = datetime.isoformat(datetime.now())
        many_seq = []
        for torrent in data:
            torrent["client"] = client
            torrent["timestamp"] = timestamp
            if not self.torrent_exists("static","hash",torrent["hash"]):
                self.create_new_torrent(torrent)
            else: many_seq.append(torrent)
        self.format_many(many_seq)

    def format_many(self,many_seq):
        db_columns = None
        db_values = []
        for torrent in many_seq:
            data = self.filter_data_fields(torrent)
            result = self.get_save_values(data)
            columns, values, params = result
            if db_columns and columns != db_columns:
                self.save_many_to_db(db_columns,db_values,params,"data")
                db_values = []
            db_columns = columns
            db_values.append(tuple(values))
        self.save_many_to_db(db_columns,db_values,params,"data")
        return

    def create_new_torrent(self,torrent):
        staticFields = self.filter_static_fields(torrent)
        dataFields = self.filter_data_fields(torrent)
        self.save_to_db(staticFields,"static")
        self.save_to_db(dataFields,"data")
        return

    def first_run_script(self,client,sample):
        self.cursor = self.get_cursor(self.path)
        timestamp = str(datetime.isoformat(datetime.now()))
        sample["client"] = client
        sample["timestamp"] = timestamp
        d_headers,s_headers = table_details(sample)
        static_headers = ", ".join(s_headers)
        self.create_db_table(static_headers,"static")
        data_headers = ", ".join(d_headers)
        self.create_db_table(data_headers,"data")
        staticFields = self.filter_static_fields(sample)
        self.save_to_db(staticFields,"static")
        dataFields = self.filter_data_fields(sample)
        self.save_to_db(dataFields,"data")
        return

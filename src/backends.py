import os
import sys
from pathlib import Path
from datetime import datetime
from .mixins import QueryMixin
from .serializer import ItemSerializer
from .models import DataModel
from .utils import log_filename, latest_log
from settings import DB_PATH,DATA_DIRNAME,CLIENTS

class BaseBackend:
    data_dir = DATA_DIRNAME
    fields = {
        "ignore" : ("auto_tmm",
                    "dl_limit",
                    "f_l_piece_prio",
                    "force_start",
                    "max_ratio",
                    "max_seeding_time",
                    "progress",
                    "ratio_limit",
                    "seeding_time_limit",
                    "super_seeding",
                    "up_limit",
                    "seq_dl",
                    "priority"),
        "static" : ("hash",
                    "client",
                    "name",
                    "tracker",
                    "magnet_uri",
                    "save_path",
                    "total_size",
                    "added_on",
                    "completion_on",
                    "state",
                    "category",
                    "tags",),
        "data" :   ("hash",
                    "timestamp",
                    "ratio",
                    "uploaded",
                    "time_active",
                    "completed",
                    "size",
                    "downloaded",
                    "num_seeds",
                    "num_leechs",
                    "last_activity",
                    "seen_complete",
                    "dlspeed",
                    "upspeed",
                    "completion_on",
                    "num_complete",
                    "num_incomplete",
                    "downloaded_session",
                    "uploaded_session",)}


class SqlBackend(BaseBackend,QueryMixin):
    serializer = ItemSerializer()
    db_path = DB_PATH
    clients = CLIENTS

    def check_path(self):
        if os.path.exists(self.db_path):
            return True
        return False

    def get_db(self):
        if self.check_path():
            self.connect(self.db_path)
        else:
            self.create_new_database()
        return

    def create_new_database(self):
        self.connect(self.db_path)
        self.create_static_table()
        self.create_data_table()
        return

    def create_data_table(self):
        data = self.fields["data"]
        kwargs = self.serializer.get_types(*data)
        self.create_table("data",foreign_key="hash",**kwargs)
        return

    def create_static_table(self):
        static = self.fields["static"]
        kwargs = self.serializer.get_types(*static)
        self.create_table("static",**kwargs)
        return

    def log(self,torrents):
        for torrent in torrents:
            timestamp = datetime.isoformat(datetime.now())
            torrent["timestamp"] = str(timestamp)
            torrent["client"] = self.name
            self.log_data(torrent,"static")
            self.log_data(torrent,"data")

    def log_data(self,data,table_name):
        fields = self.fields[table_name]
        kw1 = {}
        for label in fields:
            if label not in data:
                kw1[label] = None
            else:
                kw1[label] = data[label]
        self.insert_row(table_name,**kw1)
        return


class LogBackend(BaseBackend):

    def log_data(self,data):
        """ ```
            In -> (data{dict}) # pulled from WebAPI Request
            Out -> (None) # Begins the file storage logging process
        """
        for torrent_data in data:
            self.log(torrent_data)
        return

    def get_logfile(self,ext,name):
        """ ```
            IN -> (ext{str},name{str})
            OUT -> (fp{Path})
        """
        logdir = self.data_dir / ext
        largest_num,path = None,None
        for fp in logdir.iterdir():
            if name not in fp.name:
                continue
            if fp.stat().st_size < 1_500_000:
                return fp
            num = int(fp.name.split(".")[2])
            if not largest_num or num > largest_num:
                largest_num,path = num,fp
        if not path:
            filename = ".".join(name,"torrents",1,self.fp_ext)
            path = logdir / filename
        return path

    def copy_fields(self,data,fields):
        kw = {}
        for field in fields:
            if field in data:
                kw[field] = data[field]
            else:
                kw[field] = None
        return kw

    def format_data(self,data):
        static = self.copy_fields(data,self.fields["static"])
        field_data = self.copy_fields(data,self.fields["data"])
        if "hash" in field_data:
            del  field_data["hash"]
        static["data"] = {data["timestamp"]:field_data}
        final = { data["hash"] : static }
        return static

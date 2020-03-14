import os
import sys
from pathlib import Path
from datetime import datetime
from src.mixins import QueryMixin
from src.serializer import Serializer
from settings import DB_PATH,DATA_DIR,CLIENTS

class BaseBackend:
    data_dir = DATA_DIR
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

    def get_models(self,client):
        return self.query_models(client)

    def query_models(self,client):
        self.select_where("static","client",client)
        static_fields = self.fields["static"]
        for row in self.cur:
            yield dict(zip(static_fields,row))

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
        """ Creates a new database \n
            In --> None  \n
            Out -> None """
        self.connect(self.db_path)
        self.create_static_table()
        self.create_data_table()
        return

    def create_data_table(self):
        """ Creates a table in the database \n
            -------
            In -> None \n
            Out -> None                     """
        data = self.fields["data"]
        kwargs = self.serializer.get_types(*data)
        self.create_table("data",foreign_key="hash",**kwargs)
        return

    def create_static_table(self):
        """ Creates a table in the database \n
            -------
            In -> None \n
            Out -> None                     """
        static = self.fields["static"]
        kwargs = self.serializer.get_types(*static)
        self.create_table("static",**kwargs)
        return

    def log(self,torrents):
        for torrent in torrents:
            timestamp = datetime.isoformat(datetime.now())
            torrent["timestamp"] = str(timestamp)
            torrent["client"] = self.name
            if not self.hash_in_db(torrent["hash"]):
                self.log_data(torrent,"static")
            self.log_data(torrent,"data")
        return

    def hash_in_db(self,torrent_hash):
        """ Checks if torrent already exists in database \n
            In -> {torrent_hash}(string) \n
            Out -> {Bool} """
        self.select_where("static","hash",torrent_hash)
        if self.cur.fetchone():
            return True
        return False

    def log_data(self,data,table_name):
        """ Formats data to store in the database \n
            In -> `(data {list[]} , table_name {str})` \n
            Out -> None """
        fields = self.fields[table_name]
        kw1 = {}
        for label in fields:
            if label not in data:
                kw1[label] = None
            else:
                kw1[label] = data[label]
        self.insert_row(table_name,**kw1)
        return


class FileStorageBackend(BaseBackend):

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


class PickleBackend(FileStorageBackend):

    def log(self, data):
        data["timestamp"] = datetime.isoformat(datetime.now())
        data["client"] = self.name
        data_ready = self.format_data(data)
        path = self.get_logfile()
        final = {data["hash"]:data_ready}
        if not os.path.exists(path):
            pickle.dump(final,open(path,"wb"))
        else:
            self.compare_logs(final,path,data["hash"])

    def compare_logs(self,final,path,tor_hash):
        fp = pickle.load(open(path,"rb"))
        if tor_hash not in fp:
            return fp.update(final)
        fp[tor_hash]["data"].update(final[tor_hash]["data"])
        return pickle.dump(fp,open(path,"wb"))

    def get_logfile(self):
        """ ```
            IN -> (name{str})
            OUT -> (fp{Path})
        """
        logdir = self.data_dir / "pickle"
        if not os.path.exists(logdir):
            os.mkdir(logdir) # create log directory on first run

        # stat Existing files for room too append data
        largest_num,path = None,None
        for fp in logdir.iterdir():

            """ each client listed in the settings
                file will make their own log files with
                the client name as part of the file_name
                to easily ID them
            """
            if self.name not in fp.name:
                continue

            # for pickle 5MB is the limit
            if fp.stat().st_size < 5_000_000:
                return fp

            num = int(fp.name.split(".")[2])
            if not largest_num or num > largest_num:
                largest_num,path = num,fp

        if not path:
            filename = ".".join(self.name,
                                "torrents",
                                1,
                                "pickle.bin")
        else:
            filename = ".".join(self.name,
                                "torrents",
                                largest_num + 1,
                                "pickle.bin")
        return path


class JsonBackend(FileStorageBackend):

    def log(self, data):
        data["timestamp"] = datetime.isoformat(datetime.now())
        data["client"] = self.name
        data_ready = self.format_data(data)
        path = self.get_logfile()
        final = {data["hash"]:data_ready}
        if not os.path.exists(path):
            json.dump(final,open(path,"wt"))
        else:
            self.compare_logs(final,path,data["hash"])

    def compare_logs(self,final,path,tor_hash):
        fp = json.load(open(path,"rt"))
        if tor_hash not in fp:
            return fp.update(final)
        fp[tor_hash]["data"].update(final[tor_hash]["data"])
        return json.dump(fp,open(path,"wt"))


    def get_logfile(self):
        """ ```
            IN -> (name{str})
            OUT -> (fp{Path})
        """
        logdir = self.data_dir / "json"
        if not os.path.exists(logdir):
            os.mkdir(logdir) # create log directory on first run

        # stat Existing files for room too append data
        largest_num,path = None,None
        for fp in logdir.iterdir():

            """ each client listed in the settings
                file will make their own log files with
                the client name as part of the file_name
                to easily ID them
            """
            if self.name not in fp.name:
                continue

            # for JSON 1MB is the limit
            if fp.stat().st_size < 1_000_000: return fp
            num = int(fp.name.split(".")[2])
            if not largest_num or num > largest_num:
                largest_num,path = num,fp

        if not path:
            filename = ".".join(self.name,
                                "torrents",
                                1,
                                "log.json")
        else:
            filename = ".".join(self.name,
                                "torrents",
                                largest_num + 1,
                                "log.json")
        return path

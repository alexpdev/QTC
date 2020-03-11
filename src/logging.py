import os
import pickle
import json
import itertools
from pathlib import Path
from .backends import LogBackend


class PickleBackend(LogBackend):

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


class JsonBackend(LogBackend):

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
            if fp.stat().st_size < 1_000_000:
                return fp

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

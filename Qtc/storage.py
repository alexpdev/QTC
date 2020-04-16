#! /usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
### Qtc v0.2
### a.k.a. QTorrentCompanion
### This code written for the "Qtc" program
###
### This project is licensed with:
### GNU AFFERO GENERAL PUBLIC LICENSE
###
### Please refer to the LICENSE file locate in the root directory of this
### project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
### information.
###
### THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
### KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
### IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
### THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
### YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
### NECESSARY SERVICING, REPAIR OR CORRECTION.
###
### IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
### CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
### INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
### OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import os
from datetime import datetime

from qtc.mixins import QueryMixin, RequestMixin, SqlConnect

class ConfigurationError(Exception):
    pass

class BaseStorage(RequestMixin):

    def __init__(self, path=None, clients=None, debug=False, *args, **kwargs):
        self.path = path
        self.clients = clients
        self.debug = debug
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
        cookies = resp.cookies
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

    def dbug_out(self,msg):
        if self.debug:
            with open(self.dbug_path,"at") as fd:
                fd.write(msg + "\n")
                print(msg)
        return

    def dbug_first(self,msg):
        if not self.debug: return
        self.dbug_path = self.path.parent / "debug.log"
        with open(self.dbug_path,"at") as fd:
            ts = datetime.isoformat(datetime.now())
            ts_len, output = len(ts), "Debug Log - " + ts
            fd.write(output + "\n")
            fd.write("-"*(ts_len + 9) + "\n")
        self.dbug_out(msg)

class SqlStorage(BaseStorage, QueryMixin):
    def __init__(self, path=None, clients=None, debug=False, *args, **kwargs):
        super().__init__(path=path, clients=clients, debug=debug)
        self.path = path
        self.clients = clients
        self.connection = SqlConnect(self.path)
        self.dbug_first("First Output: Storage Initialized")

    def log(self):
        self.dbug_out("Data retreival and storage process initialized.")
        if not self.check_path():
            self.dbug_out("Error: No database discovered. Beginning \
                                                Clean Install Script")
            self.installation_script()
        self.timestamp = datetime.isoformat(datetime.now())
        self.log_timestamp(self.timestamp)
        data = self.get_data()
        self.format_data(data)
        return

    def get_data(self,data=[]):
        if not self.clients:
            self.dbug_out("Error: Client details ommited from config file. Waiting for user to provide address and login information.")
            raise ConfigurationError

        for client in self.clients:
            last_rows = self.query_last_rows(client)
            response = self.make_client_requests(client)
            self.dbug_out(f"{client} request successfull")
            for item in response:
                item["timestamp"] = self.timestamp
                item["client"] = client
                data.append(item)
        return data

    def query_last_rows(self,client,d={}):
        db_info = self.select_where("data","client",client)
        for row in db_info:
            h,t = row["hash"],row["timestamp"]
            if h not in d or d[h]["timestamp"] < t:
                d[h] = row
        return d

    def compare(self,item,last_rows):
        if item["hash"] not in last_rows: return False
        for field in ["ratio", "uploaded", "downloaded", "completed", "size"]:
            if item[field] != last_rows[item["hash"]][field]:
                return False
        return True


    def query_data(self,**kwargs):
        query = tuple(self.select_where_and("data",**kwargs))
        timestamps = [i["timestamp"] for i in query]
        if not timestamps: return False
        idx = timestamps.index(max(timestamps))
        return query[idx]

    def check_path(self):
        if os.path.isfile(self.path):
            return True
        return False

    def format_data(self, data,vals=[]):
        self.dbug_out("Saving filtered data to Database.")
        for torrent in self.filter_new(data):
            columns, values, params = self.get_save_values(torrent)
            vals.append(tuple(values))
        if not vals:
            return
        return self.save_many_to_db(columns, vals, params, "data")

    def filter_new(self, data):
        # if self.compare(item,last_rows): continue
        for torrent in data:
            if self.torrent_exists(torrent):
                yield self.filter_data_fields(torrent)
            else:
                self.create_new_torrent(torrent)


    def torrent_exists(self,torrent):
        kwargs = {"client" : torrent["client"] , "hash" : torrent["hash"]}
        rows = tuple(self.select_where_and("static",**kwargs))
        if not rows: return False
        if len([i for i in rows[0].keys() if torrent[i] != rows[0][i]]) >= 2:
            self.delete_row("static",**kwargs)
            return False
        return True

    def get_save_values(self, torrent):
        column, values, params = [], [], []
        for k, v in torrent.items():
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

    def installation_script(self):
        stypes = {
            "TEXT": {"client", "tracker", "hash",
                    "category", "magnet_uri", "name",
                    "save_path", "state", "tags"},
            "INTEGER": {"completion_on", "added_on","total_size"}}
        dtypes = {
            "TEXT": {"client", "hash", "timestamp"},
            "REAL": {"ratio"},
            "INTEGER": {"completed", "downloaded",
                        "last_activity", "downloaded_session", "size",
                        "num_complete", "uploaded", "uploaded_session",
                        "upspeed", "num_incomplete", "num_leechs", "num_seeds",
                        "dlspeed", "seen_complete", "time_active"}}

        def loop_types(typ,lst):
            for k,v in typ.items():
                lst += [i + " " + k for i in v]
            return lst

        slst = loop_types(stypes,[])
        self.create_db_table(", ".join(slst), "static")
        dlst = loop_types(dtypes,[])
        self.create_db_table(", ".join(dlst), "data")
        self.create_db_table("timestamp TEXT", "stamps")
        return True

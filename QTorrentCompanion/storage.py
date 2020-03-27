#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## QTorrentCompanion v0.2
##
## This code written for the "QTorrentCompanion" program
##
## This project is licensed with:
## GNU AFFERO GENERAL PUBLIC LICENSE
##
## Please refer to the LICENSE file locate in the root directory of this
## project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
## information.
##
## THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
## KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
## THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
## YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
## NECESSARY SERVICING, REPAIR OR CORRECTION.
##
## IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
## CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
## INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
## OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
## PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import os
from datetime import datetime

from QTorrentCompanion.mixins import QueryMixin, RequestMixin, SqlConnect

class BaseStorage(RequestMixin):

    def __init__(self, path=None, clients=None, *args, **kwargs):
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

class SqlStorage(BaseStorage, QueryMixin):
    def __init__(self, path=None, clients=None, *args, **kwargs):
        super().__init__(path=path, clients=clients)
        self.path = path
        self.clients = clients
        self.connection = SqlConnect(self.path)


    def log(self):
        if not self.check_path():
            self.installation_script()
        if not self.check_timelog():
            print("not enough time between logs")
            return False
        data = []
        for client in self.clients:
            response = self.make_client_requests(client)
            for item in response:
                item["timestamp"] = self.timestamp
                item["client"] = client
                data.append(item)
        self.format_data(data)
        return True


    def check_timelog(self):
        timestamp = datetime.now()
        self.timestamp = datetime.isoformat(timestamp)
        rows = self.select_rows("stamps")
        for item in rows:
            row_stamp = datetime.fromisoformat(item["timestamp"])
            if (timestamp - row_stamp).seconds < 600:
                return False
        self.log_timestamp(self.timestamp)
        return True


    def check_path(self):
        if os.path.isfile(self.path):
            return True
        return False


    def format_data(self, data):
        vals = []
        for torrent in self.filter_new(data):
            columns, values, params = self.get_save_values(torrent)
            vals.append(tuple(values))
        if not vals:
            return
        return self.save_many_to_db(columns, vals, params, "data")


    def filter_new(self, data):
        for torrent in data:
            row = self.torrent_exists("static", "hash", torrent["hash"])
            if not row:
                self.create_new_torrent(torrent)
                continue
            fields = [i for i in row.keys() if torrent[i] != row[i]]
            if len(fields) <= 2:
                yield self.filter_data_fields(torrent)
            else:
                self.delete_row("static","hash",row["hash"])


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

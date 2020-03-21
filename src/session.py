#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qbt Companion v0.1
##
## This code written for the "Qbt Companion" program
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
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime
from src.mixins import QueryMixin, SqlConnect
from src.window import Win
from src.models import StaticModel,DataModel
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
        self.connection = SqlConnect(self.path)

    def get_client_names(self):
        names = [i for i in self.clients]
        return names

    def get_torrent_names(self,client):
        table = "static"
        field = "client"
        rows = self.select_where(table,field,client)
        for row in rows:
            model = StaticModel(row)
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

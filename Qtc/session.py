#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qtc v0.2
##
## This code written for the "Qtc" program
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
###
######
################################################################################

import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from Qtc.mixins import QueryMixin, SqlConnect
from Qtc.factory import ItemFactory
from Qtc.window import Win


class BaseSession:
    def __init__(self,path,clients,*args,**kwargs):
        self.path = path
        self.clients = clients
        self.static_fields = ("name", "client", "total_size",
                              "tracker", "added_on", "hash",
                              "save_path", "category", "completion_on",
                              "state", "magnet_uri", "tags")

        self.data_fields = ("timestamp", "uploaded", "downloaded",
                            "ratio", "size", "time_active",
                            "seen_complete", "last_activity", "hash",
                            "client", "downloaded_session", "uploaded_session",
                            "upspeed", "dlspeed", "completed",
                            "num_complete", "num_seeds", "num_incomplete",
                            "num_leechs",)


class SqlSession(QueryMixin,BaseSession):
    def __init__(self,path,clients,*args,**kwargs):
        super().__init__(path,clients)
        self.path = path
        self.clients = clients
        self.connection = SqlConnect(self.path)
        self.factory = ItemFactory()

    def gen_items(self,field,data):
        item = self.factory.gen_item(field,data)
        return item

    def get_headers(self,fields):
        headers = [self.factory.get_label(i) for i in fields]
        return headers

    def get_client_names(self):
        names = [i for i in self.clients]
        return names

    def get_torrent_names(self,client):
        table = "static"
        field = "client"
        rows = self.select_where(table,field,client)
        rows = sorted(rows,key=lambda x: x["name"])
        for row in rows:
            v = (row["name"],row["hash"],row["client"])
            yield v

    def get_data_rows(self,torrent_hash,client):
        args = ("data","hash",torrent_hash)
        rows = self.select_where(*args)
        return rows

    def get_static_rows(self,torrent_hash,client):
        args = ("static","hash",torrent_hash)
        rows = self.select_where(*args)
        return rows

    def end_session(self):
        sys.exit(self.app.exec_())

    def get_client_data(self,client):
        data = self.select_where("data","client",client)
        ul_chart,ratio_chart = self.factory.compiledata(data)
        return ul_chart,ratio_chart

    def get_active_hashes(self):
        """ Query Database for latest timestamp and return related hashes """
        stamps = self.select_rows("stamps")
        now,min_time,timestamp = datetime.now(),None,None
        for row in stamps:
            logged = datetime.fromisoformat(row["timestamp"])

            if not timestamp or now - logged < min_time:
                timestamp = row["timestamp"]
                min_time = now - logged

        rows = self.select_where("data","timestamp",timestamp)
        return [i["hash"] for i in rows]

    def check_log(self):
        span = datetime.now() - self.logger[1]
        if span.seconds > 600:
            self.logger = (self.logger[0],datetime.now())
            return self.logger[0].start()
        return

    def mainloop(self,log_thread,BASE_DIR):
        self.Base_Dir = BASE_DIR
        self.logger = (log_thread, datetime.now())
        self.app = QApplication(sys.argv)
        self.win = Win()
        self.win.assign_session(self)
        self.app.setWindowIcon(QIcon(BASE_DIR / "icons" / "WinIcon.png"))
        self.win.show()
        sys.exit(self.app.exec_())


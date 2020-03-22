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
###
######
################################################################################

from datetime import datetime,timedelta
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt

class ItemFactory:

    labels = { "completed":"Completed","time_active":"Time Active",
            "downloaded":"Downloaded","downloaded_session":"Downloaded Session",
            "num_complete":"Total Complete","uploaded":"Uploaded",
            "uploaded_session":"Uploaded Session","ratio":"Ratio",
            "category":"Category", "tags":"Tags", "magnet_uri":"Magnet",
            "total_size":"Total Size","save_path":"Save Path","client":"Client",
            "num_incomplete":"Total Leeches","num_leechs":"Leechs Connected",
            "timestamp":"Timestamp","num_seeds":"Total Seeds", "size":"Size",
            "upspeed":"Upload Speed","dlspeed":"Download Speed", "hash":"Hash",
            "last_activity":"Last Activity", "seen_complete":"Seen Complete",
            "name":"Name", "state":"State", "tracker":"Tracker",
            "added_on":"Added On", "completion_on" : "Completion On"}

    funcs = {("completed", "num_complete", "num_incomplete", "num_leechs",
              "num_seeds", "hash", "client", "name", "tracker", "magnet_uri",
              "save_path", "state", "category", "tags"): 1,
             ("downloaded", "uploaded", "uploaded_session", "downloaded_session", "size", "total_size"): 2,
             ("last_activity", "seen_complete"): 3,
             ("ulspeed", "dlspeed"): 4,
             ('added_on',"completion_on") : 5,
             ("timestamp",): 6,
             ("ratio",): 7,
             ("time_active",): 8}


    def gen_item(self,field,data):
        label = self.get_label(field)
        for item in self.funcs:
            if field in item: break
        converted_data = self.convert_data(data,self.funcs[item]-1)
        label_item = map(self.transform,[label,converted_data])
        return tuple(label_item)

    def transform(self,data):
        item = QStandardItem(data)
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        return item


    def convert_data(self,data,idx):
        func_lst = [self.convert_const, self.convert_bytes,
                    self.convert_duration, self.convert_bps,
                    self.convert_time, self.convert_isotime,
                    self.convert_ratio, self.convert_delta]
        return func_lst[idx-1](data)

    def get_label(self,field):
        return self.labels[field]

    def convert_duration(self,data):
        now = datetime.now()
        d = datetime.fromtimestamp(data)
        return str(abs(now - d))

    def convert_bytes(self,data):
        val = data
        if val > 1_000_000_000:
            nval = str(round(val / 1_000_000_000,2))+"GB"
        elif val > 1_000_000:
            nval = str(round(val / 1_000_000,2))+"MB"
        elif val > 1000:
            nval = str(round(val / 1000,2))+"KB"
        else:
            nval = str(val)+" B"
        return nval

    def convert_bps(self,data):
        val = self.convert_bytes(data)
        val += "/s"
        return val

    def convert_const(self,data):
        return str(data)

    def convert_time(self,data):
        return str(datetime.fromtimestamp(data))

    def convert_ratio(self,data):
        return str(round(data,5))

    def convert_delta(self,data):
        d = timedelta(seconds=data)
        return str(d)

    def convert_isotime(self,data):
        return str(datetime.fromisoformat(data))

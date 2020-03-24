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

import os
import json
from datetime import datetime,timedelta
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt

class ItemFactory:

    """ Factory Class for generating items for GUI tables. """

    def __init__(self):
        """ Calls `self.load_fields()` immediately and returns. """
        self.load_fields()


    def load_fields(self):
        """ loads field data from `fields.json` in the same directory. """
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(path,"fields.json")
        fields = json.load(open(json_file))
        self.fields = fields
        self.funcs = {0 : self.convert_const,    1 : self.convert_bytes,
                      2 : self.convert_duration, 3 : self.convert_bps,
                      4 : self.convert_time,     5 : self.convert_isotime,
                      6 : self.convert_ratio,    7 : self.convert_delta}

    def gen_item(self,field,data):
        label_item = self.get_label(field)
        data_item = self.convert_data(field,data)
        return (label_item, data_item)

    def transform(self,data):
        item = QStandardItem(data)
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        return item

    def convert_data(self,field,data):
        idx = self.fields[field]["conv"]
        func = self.funcs[idx]
        serialized_data = func(data)
        data_item = self.transform(serialized_data)
        return data_item

    def get_label(self,field):
        label = self.fields[field]["label"]
        label_item = self.transform(label)
        return label_item

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
        data = int(data)
        d = timedelta(seconds=data)
        return str(d)

    def convert_isotime(self,data):
        return str(datetime.fromisoformat(data))

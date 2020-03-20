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

from datetime import datetime,timedelta



class BaseModel:
    def __init__(self,*args,**kwargs):
        self.name = "BaseModel Class"

    def __str__(self):
        return self.name

    def convert_duration(self,data):
        now = datetime.now()
        d = datetime.fromtimestamp(data)
        return abs(now - d)

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


class DataModel(BaseModel):
    fields = ("hash", "client", "timestamp",
                "ratio", "uploaded", "time_active",
                "completed", "size", "downloaded",
                "num_seeds", "num_leechs", "last_activity",
                "seen_complete", "dlspeed", "upspeed",
                "num_complete", "num_incomplete",
                "downloaded_session", "uploaded_session")

    def __init__(self,row):
        self.hashe = row["hash"]
        self.client = row["client"]
        self.timestamp = row["timestamp"]
        self.ratio = row["ratio"]
        self.uploaded = row["uploaded"]
        self.downloaded = row["downloaded"]
        self.time_active = row["timeactive"]
        self.completed = row["completed"]
        self.size = row["size"]
        self.num_leechs = row["num_leechs"]
        self.last_activity = row["last_activity"]
        self.seen_complete = row["seen_complete"]
        self.dlspeed = row["dlspeed"]
        self.upspeed = row["upspeed"]
        self.num_complete = row["num_complete"]
        self.num_incomplete = row["num_incomplete"]
        self.downloaded_session = row["downloaded_session"]
        self.uploaded_session = row["uploaded_session"]



    def __getitem__(self,item):
        if item == "hash":
            return self.hashe
        return self.__getattribute__(item)


    def convert_value(self,value,header):
        converts = {"completed": {
                        "label": "Completed",
                        "conv" : self.convert_const},
                    "downloaded": {
                        "label": "Downloaded",
                        "conv" : self.convert_bytes},
                    "downloaded_session":{
                        "label": "Downloaded Session",
                        "conv" : self.convert_bytes},
                    "num_complete": {
                        "label": "Total Complete",
                        "conv" : self.convert_const},
                    "uploaded": {
                        "label": "Uploaded",
                        "conv" : self.convert_bytes},
                    "uploaded_session": {
                        "label": "Uploaded Session",
                        "conv" : self.convert_bytes},
                    "num_incomplete": {
                        "label": "Total Leeches",
                        "conv" : self.convert_const},
                    "num_leechs": {
                        "label": "Leechs Connected",
                        "conv" : self.convert_const},
                    "timestamp": {
                        "label": "Timestamp",
                        "conv" : self.convert_isotime},
                    "num_seeds": {
                        "label": "Total Seeds",
                        "conv" : self.convert_const},
                    "size": {
                        "label": "Size",
                        "conv" : self.convert_bytes},
                    "upspeed": {
                        "label": "Upload Speed",
                        "conv" : self.convert_bps},
                    "dlspeed": {
                        "label": "Download Speed",
                        "conv" : self.convert_bps},
                    "last_activity": {
                        "label": "Last Activity",
                        "conv" : self.convert_duration},
                    "seen_complete": {
                        "label": "Seen Complete",
                        "conv" : self.convert_duration},
                    "time_active": {
                        "label": "Time Active",
                        "conv" : self.convert_delta},
                    "ratio": {
                        "label": "Ratio",
                        "conv" : self.convert_ratio}
            }
        converter = converts[header]["conv"]
        label = converts[header]["label"]
        val = converter(value)
        return (label,val)


class StaticModel(BaseModel):
    fields = ("hash", "client", "name",
              "tracker", "magnet_uri",
              "save_path", "total_size",
              "added_on", "completion_on",
              "state", "category", "tags")

    def __init__(self,data):
        self.hashe = data["hash"]
        self.client = data["client"]
        self.name = data["name"]
        self.tracker = data["tracker"]
        self.magnet_uri = data["magnet_uri"]
        self.save_path = data["save_path"]
        self.total_size = data["total_size"]
        self.added_on = data["added_on"]
        self.completion_on = data["completion_on"]
        self.state = data["state"]
        self.category = data["category"]
        self.tags = data["tags"]
        self.data_models = []

    def __getitem__(self,item):
        if item == "hash":
            return self.hashe
        return self.__getattribute__(item)

    def add_model(self,model):
        self.data_models.append(model)
        return

    def iter_models(self):
        for model in self.data_models:
            yield model


    def converter_value(self,data,header):
        converts = {"client": {"label": "Client","conv" : 4},
                    "tracker": {"label": "Tracker","conv" : 4},
                    "category": {"label": "Category","conv" : 4},
                    "hash": {"label": "Hash","conv" : 4},
                    "magnet_uri": {"label": "Magnet Link","conv" : 4},
                    "tags": {"label": "Tags","conv" : 4},
                    "save_path": {"label": "Save Path","conv" : 4},
                    "state": {"label": "State","conv" : 4},
                    "name": {"label": "Name","conv" : 4},
                    "total_size": {"label": "Total Size","conv" : 2}}
        converter = converts[header]["conv"]
        label = converts[header]["label"]
        func = self.convert_const if converter == 4 else self.convert_bytes
        val = func(data)
        return (label,val)



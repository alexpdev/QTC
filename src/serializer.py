from datetime import datetime,timedelta

class ItemSerializer:
    def __init__(self):
        self.info = {
            "client":{
                "type":"text",
                "label":"Client",
                "converter": self.convert_str
                },
            "tracker":{
                "type":"text",
                "label":"Tracker",
                "converter": self.convert_str
                },
            "category":{
                "type":"text",
                "label":"Category",
                "converter": self.convert_str
                },
            "hash":{
                "type":"text",
                "label":"Hash",
                "converter": self.convert_str
                },
            "magnet_uri":{
                "type":"text",
                "label":"Magnet Link",
                "converter": self.convert_str
                },
            "tags":{
                "type":"text",
                "label":"Tags",
                "converter": self.convert_str
                },
            "save_path":{
                "type":"text",
                "label":"Save Path",
                "converter": self.convert_str
                },
            "state":{
                "type":"text",
                "label":"State",
                "converter": self.convert_str
                },
            "name":{
                "type":"text",
                "label":"Name",
                "converter": self.convert_str
                },
            "total_size": {
                "type":"integer",
                "label":"Total Size",
                "converter": self.convert_bytes
                },
            "completed": {
                "type":"integer",
                "label":"Completed",
                "converter": self.convert_bytes
                },
            "downloaded": {
                "type":"integer",
                "label":"Downloaded",
                "converter": self.convert_bytes
                },
            "downloaded_session": {
                "type":"integer",
                "label":"Downloaded Session",
                "converter": self.convert_bytes
                },
            "num_complete": {
                "type":"integer",
                "label":"Num Complete",
                "converter": self.convert_int
                },
            "uploaded": {
                "type":"integer",
                "label":"Uploaded",
                "converter": self.convert_bytes
                },
            "uploaded_session": {
                "type":"integer",
                "label":"Uploaded Session",
                "converter": self.convert_bytes
                },
            "num_incomplete": {
                "type":"integer",
                "label":"Num Incomplete",
                "converter": self.convert_int
                },
            "num_leechs": {
                "type":"integer",
                "label":"Leechs Count",
                "converter": self.convert_int
                },
            "timestamp": {
                "type":"integer",
                "label":"Timestamp",
                "converter": self.convert_str
                },
            "num_seeds": {
                "type":"integer",
                "label":"Seeds Count",
                "converter": self.convert_int
                },
            "size": {
                "type":"integer",
                "label":"Size",
                "converter": self.convert_bytes
                },
            "upspeed": {
                "type":"integer",
                "label":"Up Speed",
                "converter": self.convert_bps
                },
            "dlspeed": {
                "type":"integer",
                "label":"Down Speed",
                "converter": self.convert_bps
                },
            "last_activity":{
                "type":"integer",
                "label":"Last Activity",
                "converter": self.convert_duration
                },
            "added_on":{
                "type":"integer",
                "label":"Added On",
                "converter": self.convert_date
                },
            "completion_on":{
                "type":"integer",
                "label":"Completion On",
                "converter": self.convert_date
                },
            "seen_complete":{
                "type":"integer",
                "label":"Seen Complete",
                "converter": self.convert_date
                },
            "time_active":{
                "type":"integer",
                "label":"Time Active",
                "converter": self.convert_duration
                },
            "ratio":{
                "type":"real",
                "label":"Ratio",
                "converter": self.convert_ratio
                }
            }

    def get_types(self,*args):
        types = {}
        for arg in args:
            types[arg] = self.info[arg]["type"]
        return types

    def convert_ratio(self,data):
        return round(data,3)

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
        val = convert_bytes(data)
        val += "/s"
        return val

    def convert_str(self,data):
        return data

    def convert_int(self,data):
        return data

    def convert_date(self,data):
        return datetime.fromtimestamp(data)



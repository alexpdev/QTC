from datetime import datetime,timedelta

class DataModel:

    def __init__(self,**kwargs):
        self.client = kwargs["client"]
        self.timestamp = datetime.fromisoformat(kwargs["timestamp"])
        self.category = kwargs["category"]
        self.added_on = datetime.fromtimestamp(kwargs["added_on"])
        self.dlspeed = kwargs["dlspeed"]
        self.downloaded = kwargs["downloaded"]
        self.downloaded_session = kwargs["downloaded_session"]
        self.last_activity = datetime.fromtimestamp(kwargs["last_activity"])
        self.hash = kwargs["hash"]
        self.completed = kwargs["completed"]
        self.completion_on = datetime.fromtimestamp(kwargs["completion_on"])
        self.magnet_uri = kwargs["magnet_uri"]
        self.name = kwargs["name"]
        self.num_complete = kwargs["num_complete"]
        self.num_incomplete = kwargs["num_incomplete"]
        self.num_leechs = kwargs["num_leechs"]
        self.time_active = timedelta(seconds = kwargs["time_active"])
        self.num_seeds = kwargs["num_seeds"]
        self.ratio = kwargs["ratio"]
        self.progress = kwargs["progress"]
        self.save_path = kwargs["save_path"]
        self.size = kwargs["size"]
        self.state = kwargs["state"]
        self.tags = kwargs["tags"]
        self.total_size = kwargs["total_size"]
        self.tracker = kwargs["tracker"]
        self.uploaded = kwargs["uploaded"]
        self.uploaded_session = kwargs["uploaded_session"]
        self.upspeed = kwargs["upspeed"]

    def tableFields(self):
        fields = {"DL Session":self.downloaded_session,
            "Timestamp" : self.timestamp,
            "DL Speed":self.dlspeed,
            "Ratio" : self.ratio,
            "Leechs" : self.num_leechs,
            "Seeds":self.num_seeds,
            "Size" : self.size,
            "Uploaded" : self.uploaded,
            "Time Active" : self.time_active,
            "Last Activity": self.last_activity,
            "Uploaded Session" : self.uploaded_session,
            "Upload Speed":self.upspeed}
        for k,v in fields.items():
            fields[k] = self.denom(v)
        return fields


    def static_fields(self):
        fields = {"Client" : self.client,
            "Hash":self.hash,
            "Torrent Name":self.name,
            "Total Size":self.total_size,
            "Downloaded":self.downloaded,
            "Tracker":self.tracker,
            "Date Added":self.added_on,
            "Magnet Link":self.magnet_uri,
            "Date Completed":self.completion_on,
            "Category" : self.category,
            "Tags" : self.tags,
            "State":self.state}
        for k,v in fields.items():
            fields[k] = self.denom(v)
        return fields

    def time_fields(self):
        fields = {self.added_on :"Added On",
        self.timestamp :"Time Stamp",
        self.time_active :"Time Active",
        self.completion_on :"Completion On",
        self.last_activity :"Last Activity"}

    def denom(self,field):
        if not isinstance(field,int):
            return field
        val = field
        if val > 1_000_000_000:
            nval = str(round(val / 1_000_000_000,2))+"GB"
        elif val > 1_000_000:
            nval = str(round(val / 1_000_000,2))+"MB"
        elif val > 1000:
            nval = str(round(val / 1000,2))+"KB"
        else:
            nval = str(val)+" B"
        return nval

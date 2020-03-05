class DataModel:

    def __init__(self,title,logtime,**kwargs):
        self.session = title
        self.logtime = logtime
        self.added_on = kwargs["added_on"]
        self.amount_left = kwargs["amount_left"]
        self.category = kwargs["category"]
        self.completed = kwargs["completed"]
        self.completion_on = kwargs["completion_on"]
        self.dlspeed = kwargs["dlspeed"]
        self.downloaded = kwargs["downloaded"]
        self.downloaded_session = kwargs["downloaded_session"]
        self.eta = kwargs["eta"]
        self.hash = kwargs["hash"]
        self.last_activity = kwargs["last_activity"]
        self.magnet_uri = kwargs["magnet_uri"]
        self.max_ratio = kwargs["max_ratio"]
        self.max_seeding_time = kwargs["max_seeding_time"]
        self.name = kwargs["name"]
        self.num_complete = kwargs["num_complete"]
        self.num_incomplete = kwargs["num_incomplete"]
        self.num_leechs = kwargs["num_leechs"]
        self.num_seeds = kwargs["num_seeds"]
        self.progress = kwargs["progress"]
        self.ratio = kwargs["ratio"]
        self.save_path = kwargs["save_path"]
        self.size = kwargs["size"]
        self.state = kwargs["state"]
        self.tags = kwargs["tags"]
        self.time_active = kwargs["time_active"]
        self.total_size = kwargs["total_size"]
        self.tracker = kwargs["tracker"]
        self.uploaded = kwargs["uploaded"]
        self.uploaded_session = kwargs["uploaded_session"]
        self.upspeed = kwargs["upspeed"]

    def display_fields(self):
        fields = [  ("name",self.name),
                    ("downloaded",self.downloaded),
                    ("logtime",self.logtime),
                    ("max_ratio",self.max_ratio),
                    ("max_seeding_time",self.max_seeding_time),
                    ("num_leechs",self.num_leechs),
                    ("num_seeds",self.num_seeds),
                    ("ratio",self.ratio),
                    ("size",self.size),
                    ("uploaded",self.uploaded),
                    ("uploaded_session",self.uploaded_session),
                    ("upspeed",self.upspeed),]
        return fields


class DataModel:
    def __init__(self,parent=None,**kwargs):
        self.parent = parent
        self.timestamp = kwargs["timestamp"]
        self.dlspeed = kwargs["dlspeed"]
        self.downloaded = kwargs["downloaded"]
        self.downloaded_session = kwargs["downloaded_session"]
        self.last_activity = kwargs["last_activity"]
        self.completed = kwargs["completed"]
        self.completion_on = kwargs["completion_on"]
        self.num_complete = kwargs["num_complete"]
        self.num_incomplete = kwargs["num_incomplete"]
        self.num_leechs = kwargs["num_leechs"]
        self.time_active = ["time_active"]
        self.num_seeds = kwargs["num_seeds"]
        self.ratio = kwargs["ratio"]
        self.size = kwargs["size"]
        self.uploaded = kwargs["uploaded"]
        self.uploaded_session = kwargs["uploaded_session"]
        self.upspeed = kwargs["upspeed"]

class StaticModel:

    def __init__(self,*args,**kwargs):
        self.torrent_hash = kwargs["hash"]
        self.client = kwargs["client"]
        self.magnet_uri = kwargs["magnet_uri"]
        self.save_path = kwargs["save_path"]
        self.state = kwargs["state"]
        self.tracker = kwargs["tracker"]
        self.name = kwargs["name"]
        self.added_on = kwargs["added_on"]
        self.total_size = kwargs["total_size"]
        self.category = kwargs["category"]
        self.tags = kwargs["tags"]
        self.data_models = []

    def has_items(self):
        if self.data_models:
            return True
        return False



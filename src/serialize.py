from datetime import datetime, timedelta

class Converter:

    datatypes = {
        "client": {
            "type": "TEXT",
            "label": "Client",
            "table": "static",
            "conv" : 4,
        },
        "tracker": {
            "type": "TEXT",
            "label": "Tracker",
            "table": "static",
            "conv" : 4,
        },
        "category": {
            "type": "TEXT",
            "label": "Category",
            "table": "static",
            "conv" : 4,
        },
        "hash": {
            "type": "TEXT",
            "label": "Hash",
            "table": "static",
            "conv" : 4,
        },
        "magnet_uri": {
            "type": "TEXT",
            "label": "Magnet Link",
            "table": "static",
            "conv" : 4,
        },
        "tags": {
            "type": "TEXT",
            "label": "Tags",
            "table": "static",
            "conv" : 4,
        },
        "save_path": {
            "type": "TEXT",
            "label": "Save Path",
            "table": "static",
            "conv" : 4,
        },
        "state": {
            "type": "TEXT",
            "label": "State",
            "table": "static",
            "conv" : 4,
        },
        "name": {
            "type": "TEXT",
            "label": "Name",
            "table": "static",
            "conv" : 4,
        },
        "total_size": {
            "type": "INTEGER",
            "label": "Total Size",
            "table": "static",
            "conv" : 2,
        },
        "completed": {
            "type": "INTEGER",
            "label": "Completed",
            "table": "data",
            "conv" : 2,
        },
        "downloaded": {
            "type": "INTEGER",
            "label": "Downloaded",
            "table": "data",
            "conv" : 2,
        },
        "downloaded_session": {
            "type": "INTEGER",
            "label": "Downloaded Session",
            "table": "data",
            "conv" : 2,
        },
        "num_complete": {
            "type": "INTEGER",
            "label": "Total Complete",
            "table": "data",
            "conv" : 4,
        },
        "uploaded": {
            "type": "INTEGER",
            "label": "Uploaded",
            "table": "data",
            "conv" : 2,
        },
        "uploaded_session": {
            "type": "INTEGER",
            "label": "Uploaded Session",
            "table": "data",
            "conv" : 2,
        },
        "num_incomplete": {
            "type": "INTEGER",
            "label": "Total Incomplete",
            "table": "data",
            "conv" : 4,
        },
        "num_leechs": {
            "type": "INTEGER",
            "label": "Total Leechs",
            "table": "data",
            "conv" : 4,
        },
        "timestamp": {
            "type": "INTEGER",
            "label": "Timestamp",
            "table": "data",
            "conv" : 4,
        },
        "num_seeds": {
            "type": "INTEGER",
            "label": "Total Seeds",
            "table": "data",
            "conv" : 4,
        },
        "size": {
            "type": "INTEGER",
            "label": "Size",
            "table": "data",
            "conv" : 2,
        },
        "upspeed": {
            "type": "INTEGER",
            "label": "Upload Speed",
            "table": "data",
            "conv" : 3,
        },
        "dlspeed": {
            "type": "INTEGER",
            "label": "Download Speed",
            "table": "data",
            "conv" : 3,
        },
        "last_activity": {
            "type": "INTEGER",
            "label": "Last Activity",
            "table": "data",
            "conv" : 1,
        },
        "added_on": {
            "type": "INTEGER",
            "label": "Added On",
            "table": "static",
            "conv" : 5,
        },
        "completion_on": {
            "type": "INTEGER",
            "label": "Completion On",
            "table": "static",
            "conv" : 5,
        },
        "seen_complete": {
            "type": "INTEGER",
            "label": "Seen Complete",
            "table": "data",
            "conv" : 5,
        },
        "time_active": {
            "type": "INTEGER",
            "label": "Time Active",
            "table": "data",
            "conv" : 1,
        },
        "ratio": {
            "type": "REAL",
            "label": "Ratio",
            "table": "data",
            "conv" : 6,
        },
    }

    @classmethod
    def table_details(cls,data):
        data_types, static_types = [], []
        hash_type = "hash " + cls.datatypes["hash"]["type"]
        client_type = "client " + cls.datatypes["client"]["type"]
        for t in [hash_type, client_type]:
            static_types.append(t)
            data_types.append(t)
        for k, v in data.items():
            if k in ["hash", "client"] or k not in cls.datatypes:
                continue
            value = k + " " + cls.datatypes[k]["type"]
            if cls.datatypes[k]["table"] == "static":
                static_types.append(value)
            elif cls.datatypes[k]["table"] == "data":
                data_types.append(value)
        return data_types, static_types

    @classmethod
    def convert_values(cls,rows):
        final = []
        for row in rows:
            row_vals = []
            for k,v in zip(row.keys(),tuple(row)):
                info = cls.datatypes[k]
                label = info["label"]
                cdig = info["conv"]
                value = cls.convert(cdig,v)
                row_vals.append((label,value))
            final.append(row_vals)
        return final

    @classmethod
    def convert(cls,num,val):
        converter_lst = [
            lambda x: cls.convert_duration(x),
            lambda x: cls.convert_bytes(x) ,
            lambda x: cls.convert_bps(x) ,
            lambda x: cls.convert_const(x) ,
            lambda x: cls.convert_time(x) ,
            lambda x: cls.convert_ratio(x)
        ]
        result = converter_lst[num - 1](val)
        return result



    # converter 1
    @classmethod
    def convert_duration(cls,data):
        now = datetime.now()
        d = datetime.fromtimestamp(data)
        return abs(now - d)

    # converter 2
    @classmethod
    def convert_bytes(cls,data):
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

    # converter 3
    @classmethod
    def convert_bps(cls,data):
        val = cls.convert_bytes(data)
        val += "/s"
        return val

    # converter 4
    @classmethod
    def convert_const(cls,data):
        return data

    # converter 5
    @classmethod
    def convert_time(cls,data):
        return datetime.fromtimestamp(data)

    # converter 6
    @classmethod
    def convert_ratio(cls,data):
        return round(data,3)



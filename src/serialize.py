from datetime import datetime, timedelta

class Converter:
    datatypes = None

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
                value = cls.info["conv"](v)
                row_vals.append((label,value))
            final.append(row_vals)
        return final

    @classmethod
    def convert_duration(cls,data):
        now = datetime.now()
        d = datetime.fromtimestamp(data)
        return abs(now - d)

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

    @classmethod
    def convert_bps(cls,data):
        val = convert_bytes(data)
        val += "/s"
        return val

    @classmethod
    def convert_str(cls,data):
        return data

    @classmethod
    def convert_date(cls,data):
        return datetime.fromtimestamp(data)

    @classmethod
    def convert_ratio(cls,data):
        return round(data,3)


    convert_int = convert_str

    datatypes = {
        "client": {
            "type": "TEXT",
            "label": "Client",
            "table": "static",
            "conv" : convert_str,
        },
        "tracker": {
            "type": "TEXT",
            "label": "Tracker",
            "table": "static",
            "conv" : convert_str,
        },
        "category": {
            "type": "TEXT",
            "label": "Category",
            "table": "static",
            "conv" : convert_str,
        },
        "hash": {
            "type": "TEXT",
            "label": "Hash",
            "table": "static",
            "conv" : convert_str,
        },
        "magnet_uri": {
            "type": "TEXT",
            "label": "Magnet Link",
            "table": "static",
            "conv" : convert_str,
        },
        "tags": {
            "type": "TEXT",
            "label": "Tags",
            "table": "static",
            "conv" : convert_str,
        },
        "save_path": {
            "type": "TEXT",
            "label": "Save Path",
            "table": "static",
            "conv" : convert_str,
        },
        "state": {
            "type": "TEXT",
            "label": "State",
            "table": "static",
            "conv" : convert_str,
        },
        "name": {
            "type": "TEXT",
            "label": "Name",
            "table": "static",
            "conv" : convert_str,
        },
        "total_size": {
            "type": "INTEGER",
            "label": "Total Size",
            "table": "static",
            "conv" : convert_bytes,
        },
        "completed": {
            "type": "INTEGER",
            "label": "Completed",
            "table": "data",
            "conv" : convert_bytes,
        },
        "downloaded": {
            "type": "INTEGER",
            "label": "Downloaded",
            "table": "data",
            "conv" : convert_bytes,
        },
        "downloaded_session": {
            "type": "INTEGER",
            "label": "Downloaded Session",
            "table": "data",
            "conv" : convert_bytes,
        },
        "num_complete": {
            "type": "INTEGER",
            "label": "Total Complete",
            "table": "data",
            "conv" : convert_int,
        },
        "uploaded": {
            "type": "INTEGER",
            "label": "Uploaded",
            "table": "data",
            "conv" : convert_bytes,
        },
        "uploaded_session": {
            "type": "INTEGER",
            "label": "Uploaded Session",
            "table": "data",
            "conv" : convert_bytes,
        },
        "num_incomplete": {
            "type": "INTEGER",
            "label": "Total Incomplete",
            "table": "data",
            "conv" : convert_int,
        },
        "num_leechs": {
            "type": "INTEGER",
            "label": "Total Leechs",
            "table": "data",
            "conv" : convert_int,
        },
        "timestamp": {
            "type": "INTEGER",
            "label": "Timestamp",
            "table": "data",
            "conv" : convert_str,
        },
        "num_seeds": {
            "type": "INTEGER",
            "label": "Total Seeds",
            "table": "data",
            "conv" : convert_int,
        },
        "size": {
            "type": "INTEGER",
            "label": "Size",
            "table": "data",
            "conv" : convert_bytes,
        },
        "upspeed": {
            "type": "INTEGER",
            "label": "Upload Speed",
            "table": "data",
            "conv" : convert_bps,
        },
        "dlspeed": {
            "type": "INTEGER",
            "label": "Download Speed",
            "table": "data",
            "conv" : convert_bps,
        },
        "last_activity": {
            "type": "INTEGER",
            "label": "Last Activity",
            "table": "data",
            "conv" : convert_duration,
        },
        "added_on": {
            "type": "INTEGER",
            "label": "Added On",
            "table": "static",
            "conv" : convert_date,
        },
        "completion_on": {
            "type": "INTEGER",
            "label": "Completion On",
            "table": "static",
            "conv" : convert_date,
        },
        "seen_complete": {
            "type": "INTEGER",
            "label": "Seen Complete",
            "table": "data",
            "conv" : convert_date,
        },
        "time_active": {
            "type": "INTEGER",
            "label": "Time Active",
            "table": "data",
            "conv" : convert_duration,
        },
        "ratio": {
            "type": "REAL",
            "label": "Ratio",
            "table": "data",
            "conv" : convert_ratio,
        },
    }


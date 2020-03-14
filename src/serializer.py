from datetime import datetime,timedelta


def table_details(data):
    from src.datatypes import datatypes
    data_types,static_types = [],[]
    hash_type = "hash " + datatypes["hash"]["type"]
    client_type = "client " + datatypes["client"]["type"]
    for t in [hash_type,client_type]:
        static_types.append(t)
        data_types.append(t)
    for k,v in data.items():
        if k in ["hash","client"] or k not in datatypes:
            continue
        value = k + " " + datatypes[k]["type"]
        if datatypes[k]["table"] == "static":
            static_types.append(value)
        elif datatypes[k]["table"] == "data":
            data_types.append(value)
    return data_types,static_types

def convert_duration(data):
    now = datetime.now()
    d = datetime.fromtimestamp(data)
    return abs(now - d)

def convert_bytes(data):
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

def convert_bps(data):
    val = convert_bytes(data)
    val += "/s"
    return val

def convert_str(data):
    return data

def convert_int(data):
    return data

def convert_date(data):
    return datetime.fromtimestamp(data)

def convert_ratio(data):
    return round(data,3)

def convert(column,data):
    types = {"str","bytes","int","float","duration","date"}
    info = {"client":convert_str,
        "tracker": convert_str,
        "category": convert_str,
        "hash": convert_str,
        "magnet_uri": convert_str,
        "tags": convert_str,
        "save_path": convert_str,
        "state": convert_str,
        "name": convert_str,
        "total_size": convert_bytes,
        "completed": convert_bytes,
        "downloaded": convert_bytes,
        "downloaded_session": convert_bytes,
        "num_complete": convert_int,
        "uploaded": convert_bytes,
        "uploaded_session": convert_bytes,
        "num_incomplete": convert_int,
        "num_leechs": convert_int,
        "timestamp": convert_str,
        "num_seeds": convert_int,
        "size": convert_bytes,
        "upspeed": convert_bps,
        "dlspeed": convert_bps,
        "last_activity": convert_duration,
        "added_on": convert_date,
        "completion_on": convert_date,
        "seen_complete": convert_date,
        "time_active": convert_duration,
        "ratio": convert_ratio}
    converter = info[column]
    return str(converter(data))

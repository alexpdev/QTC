import os
from pathlib import Path
ROOT = (i.parent.parent for i in [Path(__file__).resolve()])
USER = os.environ["USERNAME"]
PASS = os.environ["PASSWORD"]
SEED_PASS = os.environ["SEEDBOXPASS"]
SEED_URL = os.environ["SEEDBOXURL"]
SEED_USER = os.environ["SEED_USER"]
DATA_DIR = next(ROOT) / "temp" / "db"
DB_NAME = "qbtdata.db"
LOCAL1 = os.environ["LOCAL1"]
LOCAL2 = os.environ["LOCAL2"]
LOCAL1_CLIENT = os.environ["LOCAL1_CLIENT"]
LOCAL2_CLIENT = os.environ["LOCAL2_CLIENT"]
CLIENTS = [LOCAL1_CLIENT,LOCAL2_CLIENT,"seedbox"]
DETAILS = {
    # LOCAL1_CLIENT:{
    #     "url": LOCAL1,
    #     "credentials":{
    #         "username" : USER,
    #         "password" : PASS
    #     }
    # },
    LOCAL2_CLIENT :{
        "url": LOCAL2,
        "credentials":{
            "username": USER,
            "password": PASS,
        }
    },
    "seedbox" : {
        "url" : SEED_URL,
        "credentials":{
            "username": SEED_USER,
            "password": SEED_PASS,
        }
    }
}

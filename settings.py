# Default and Custom Configuration Data Go Here
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.resolve()

USER = os.environ["USERNAME"]
PASS = os.environ["PASSWORD"]

SEED_PASS = os.environ["SEEDBOXPASS"]
SEED_URL = os.environ["SEEDBOXURL"]

DATA_DIRNAME = ROOT / "data"

items = {
    "asp001":{
        "url": "http://asp001:8765/api/v2/",
        "credentials":{
            "username" : USER,
            "password" : PASS
        }
    },
    "asp002" :{
        "url": "http://127.0.0.1:8080/api/v2/",
        "credentials":{
            "username": USER,
            "password": PASS,
        }
    },
    "seedbox" : {
        "url" : SEED_URL,
        "credentials":{
            "username": USER,
            "password": SEED_PASS,
        }
    }
}

FILEPREFIX = "torrent"

FILESUFFIX = "log.json"

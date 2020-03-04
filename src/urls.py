import os
import sys
from dotenv import load_dotenv

load_dotenv()

user = os.environ["USERNAME"]
pw = os.environ["PASSWORD"]
pwSeedbox = os.environ["SEEDBOXPASS"]
items = {
    "asp001":{
        "url": "http://asp001:8765/api/v2/",
        "credentials":{
            "username" : user,
            "password" : pw
        }
    },
    "asp002" :{
        "url": "http://127.0.0.1:8080/api/v2/",
        "credentials":{
            "username":user,
            "password":pw,
        }
    },
    "seedbox" : {
        "url" : "http://51.254.241.117:8080/api/v2/",
        "credentials":{
            "username":user,
            "password":pwSeedbox,
        }
    }
}

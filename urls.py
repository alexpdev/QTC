import os
import sys
from dotenv import load_dotenv

load_dotenv()

user = os.environ["USERNAME"]
pw = os.environ["PASSWORD"]
pwSeedbox = os.environ["SEEDBOXPASS"]
seedboxurl = os.environ["SEEDBOXURL"]
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
        "url" : seedboxurl,
        "credentials":{
            "username":user,
            "password":pwSeedbox,
        }
    }
}

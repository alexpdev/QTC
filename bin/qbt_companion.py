#! /bin/python3
"""






    Just in case














"""

import sys
import os
from pathlib import Path
fp = os.path.abspath(__file__)
path_fp = Path(fp).resolve()
BASE_DIR = path_fp.parent.parent
BD = os.path.abspath(BASE_DIR)
from dotenv import load_dotenv as lde
sys.path.append(BD)
lde()
from src.settings import DATA_DIR,DB_NAME,DETAILS,DEBUG
from src.storage import SqlStorage
from src.session import SqlSession
from threading import Thread

kwargs = {
    "dbg" : False,
    "backend" : "Sqlite3",

}

def main(**kwargs):
    if DEBUG:
        kwargs["dbg"] = True
        print("Program Started")
    database_path = BASE_DIR / DATA_DIR / DB_NAME
    clients = DETAILS
    storage = SqlStorage(database_path,clients)
    if DEBUG:
        print("SQL Storage Object Created")
    session = SqlSession(database_path,clients)
    if DEBUG:
        print("SQL Session Object Created")
    args = storage,session
    log_thread = Thread(target=log,args=args)
    main_thread = Thread(target=mainloop,args=args)
    storage.log()
    if DEBUG:
        print("Current Client Stats Logged")
    session.mainloop()
    if DEBUG:
        print("Window Created")

def mainloop(session):
    session.mainloop()

def log(storage):
    storage.log()

if __name__ == "__main__":
    main(**kwargs)



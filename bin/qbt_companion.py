#! /bin/python3
"""






    Just in case














"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv as lde
BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(BASE_DIR)
lde()
from src.settings import DATA_DIR,DB_NAME,DETAILS
from src.storage import SqlStorage
from threading import Thread


def main():
    db_dir = BASE_DIR / DATA_DIR
    clients = DETAILS
    db_name = DB_NAME
    storage = SqlStorage(db_dir,clients,db_name)
    log_thread = Thread(log,(storage,))



def log(storage):
    storage.log()






import os
import sys
import json
from pathlib import Path
BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(BASE_DIR)
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()
from test.testsettings import DETAILS,DB_NAME,DATA_DIR
from src.serialize import Converter as Conv
from src.session import SqlSession
from src.widgets import *
from src.storage import SqlStorage,BaseStorage

class TestOthers(TestCase):
    @classmethod
    def setUpClass(cls):
        class_clients = DETAILS
        class_db = DATA_DIR / DB_NAME
        sql_storage = SqlStorage(class_db,class_clients)
        for i in range(3):
            sql_storage.log()


    def setUp(self):
        self.clients = DETAILS
        self.path = DATA_DIR / DB_NAME

    def tearDown(self):
        pass

    def test_session_queries(self):
        storage = SqlStorage(self.path,self.clients)
        session = SqlSession(self.path,self.clients)
        for client in session.clients:
            info = session.get_torrent_names(client)
            self.assertTrue(info)
            hashes,names,client = [],[],[]
            for i in info:
                hashes.append(i[1])
                names.append(i[0])
                client.append(i[2])
            for t_hash in hashes:
                rows = session.get_static_rows(t_hash,client)
                self.assertTrue(rows)
                for row in rows:
                    self.assertIn(("Hash",t_hash),row)


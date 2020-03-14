import os
import sys
import json
from pathlib import Path
sys.path.append(Path(os.path.abspath(__file__)).parent.parent)
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()
from test.testsettings import DETAILS,DB_NAME,DATA_DIR
from src.storage import SqlStorage,BaseStorage

class TestStorage(TestCase):
    def setUp(self):
        self.clients = DETAILS
        self.path = DATA_DIR
        self.name = DB_NAME

    def tearDown(self):
        db = self.path / self.name
        if os.path.isfile(db):
            os.remove(db)

    def test_storage_constructors(self):
        base_storage = BaseStorage(self.path,self.clients)
        sql_storage = SqlStorage(self.path,self.clients,self.name)
        for storage in [base_storage,sql_storage]:
            self.assertTrue(storage)
            self.assertIn("hash",storage.static_fields)
            self.assertIn("uploaded",storage.data_fields)
            self.assertEqual(storage.data_dir,self.path)
            self.assertEqual(storage.clients,self.clients)

    def test_sql_methods(self):
        sql_storage = SqlStorage(self.path,self.clients,self.name)
        clients = (i for i in self.clients)
        client = next(clients)
        data = sql_storage.make_client_requests(client)
        self.assertTrue(data)
        self.assertIsInstance(data,list)
        torrent = data[0]
        torrent["client"] = client
        torrent["timestamp"] = "timestamp"
        self.assertIsInstance(torrent,dict)
        for i in sql_storage.static_fields:
            self.assertIn(i,torrent)
        for i in sql_storage.data_fields:
            self.assertIn(i,torrent)

    def test_success(self):
        storage = SqlStorage(self.path,self.clients,self.name)
        storage.log()
        self.assertTrue(os.path.isfile(self.path / self.name))









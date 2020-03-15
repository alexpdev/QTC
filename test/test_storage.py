import json
import os
import sys
from pathlib import Path
from unittest import TestCase

from dotenv import load_dotenv

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
sys.path.append(BASE_DIR)
load_dotenv()

from test.testsettings import DATA_DIR, DB_NAME, DETAILS


from src.storage import BaseStorage, SqlStorage


class TestStorage(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.path = DATA_DIR / DB_NAME
        self.clients = DETAILS
        if os.path.isfile(self.path):
            os.remove(self.path)

    def tearDown(self):
        db = self.path
        if os.path.isfile(db):
            os.remove(db)

    def test_storage_constructors(self):
        base_storage = BaseStorage(self.path,self.clients)
        sql_storage = SqlStorage(self.path,self.clients)
        for storage in [base_storage,sql_storage]:
            self.assertTrue(storage)
            self.assertIn("hash",storage.static_fields)
            self.assertIn("uploaded",storage.data_fields)
            self.assertEqual(storage.path,self.path)
            self.assertEqual(storage.clients,self.clients)

    def test_sql_methods(self):
        sql_storage = SqlStorage(self.path,self.clients)
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
        storage = SqlStorage(self.path,self.clients)
        storage.log()
        self.assertTrue(os.path.isfile(self.path))
        storage.log()
        for row in storage.select_rows("static"):
            self.assertTrue(len(row) > 5)

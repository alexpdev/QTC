import os
import sys
import json
from pathlib import Path
sys.path.append(Path(os.path.abspath(__file__)).parent.parent)
from unittest import TestCase
from dotenv import load_dotenv
load_dotenv()
from test.testsettings import DETAILS,DB_NAME,DATA_DIR
from src.session import BaseSession,SqlSession
from src.storage import SqlStorage


class TestSession(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.clients = DETAILS
        self.path = DATA_DIR / DB_NAME
        db = self.path
        if os.path.isfile(db):
            os.remove(db)

    def tearDown(self):
        db = self.path
        if os.path.isfile(db):
            os.remove(db)

    def test_session_init(self):
        base = BaseSession(self.path,self.clients)
        sql = SqlSession(self.path,self.clients)
        self.assertTrue(base)
        self.assertTrue(sql)
        self.assertEqual(base.path,self.path)
        self.assertEqual(sql.path,self.path)

    def test_session_methods(self):
        session = SqlSession(self.path,self.clients)
        storage = SqlStorage(self.path,self.clients)
        storage.log()
        names = [i for i in self.clients]
        client_names = session.get_client_names()
        self.assertEqual(names,client_names)

    def test_get_torrent_names(self):
        session = SqlSession(self.path,self.clients)
        storage = SqlStorage(self.path,self.clients)
        storage.log()
        for client in session.clients:
            names = session.get_torrent_names(client)
            self.assertTrue(names)
            for name in names:
                self.assertEqual(len(name),3)
                self.assertIn(client,name)
                tr_name,tr_hash,tr_client = name
                self.assertIsInstance(tr_name,str)
                self.assertIsInstance(tr_hash,str)
                self.assertIsInstance(tr_client,str)










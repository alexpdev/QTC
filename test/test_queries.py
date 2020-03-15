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

class TestQueries(TestCase):
    def setUp(self):
        self.clients = DETAILS
        self.path = DATA_DIR / DB_NAME

    def tearDown(self):
        db = self.path
        if os.path.isfile(db):
            os.remove(db)


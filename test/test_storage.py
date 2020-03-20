#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qbt Companion v0.1
##
## This code written for the "Qbt Companion" program
##
## This project is licensed with:
## GNU AFFERO GENERAL PUBLIC LICENSE
##
## Please refer to the LICENSE file locate in the root directory of this
## project or visit <https://www.gnu.org/licenses/agpl-3.0 for more
## information.
##
## THE COPYRIGHT HOLDERS PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY
## KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
## THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH
## YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL
## NECESSARY SERVICING, REPAIR OR CORRECTION.
##
## IN NO EVENT ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR
## CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
## INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
## OUT OF THE USE OR INABILITY TO USE THE PROGRAM EVEN IF SUCH HOLDER OR OTHER
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import os
import sys
import json
import sqlite3
from pathlib import Path
from unittest import TestCase

from dotenv import load_dotenv

# BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
# sys.path.append(BASE_DIR)
load_dotenv()

from test.testsettings import DATA_DIR, DB_NAME, DETAILS


from src.storage import BaseStorage, SqlStorage


class TestStorage(TestCase):

    @classmethod
    def setUpClass(cls):
        path = DATA_DIR / DB_NAME
        if os.path.isfile(path):
            os.remove(path)
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.path = DATA_DIR / DB_NAME
        self.clients = DETAILS
        self.storage = SqlStorage(self.path,self.clients)

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

    def test_request_mixin(self):
        for client in self.clients:
            data = self.storage.make_client_requests(client)
            self.assertTrue(data)
            self.assertIsInstance(data,list)
            torrent = data[0]
            torrent["client"] = client
            torrent["timestamp"] = "timestamp"
            self.assertIsInstance(torrent,dict)
            for i in self.storage.static_fields:
                self.assertIn(i,torrent)
            for i in self.storage.data_fields:
                self.assertIn(i,torrent)

    def test_log_function(self):
        self.assertTrue(self.storage.log())
        self.assertTrue(os.path.isfile(self.path))
        self.assertFalse(self.storage.log())
        for row in self.storage.select_rows("static"):
            self.assertTrue(len(row) > 5)

    def test_create_database_table(self):
        db_name = "names"
        db_headers = ("name TEXT, address TEXT, number INTEGER, age REAL")
        self.storage.create_db_table(db_headers,db_name)
        con = sqlite3.connect(self.path)
        c = con.execute("SELECT * from names")
        self.assertEqual(c.fetchone(),None)
        data = {"name":"dursley","address":"Privet Drive","number":4,"age":44.5}
        self.storage.save_to_db(data,db_name)
        con = sqlite3.connect(self.path)
        c = con.execute("SELECT * from names")
        for row in c:
            for i in tuple(row):
                self.assertIn(i,data.values())
        con.close()


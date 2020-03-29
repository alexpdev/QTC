#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qtc v0.2
##
## This code written for the "Qtc" program
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
## PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import os
import sys
import sqlite3
from pathlib import Path
from unittest import TestCase
sys.path.append(os.getcwd())
try:
    from tests.test_pydenv import pydenv
    pydenv()
    from tests._testsettings import DETAILS,DB_NAME,DATA_DIR
except:
    from tests.testsettings import DETAILS,DB_NAME,DATA_DIR

from qtc.storage import BaseStorage, SqlStorage


class TestStorage(TestCase):

    @classmethod
    def setUpClass(cls):
        path = DATA_DIR / DB_NAME
        if os.path.isfile(path):
            os.remove(path)
        storage = SqlStorage(path,DETAILS)
        storage.log()

    @classmethod
    def tearDownClass(cls):
        db = DATA_DIR / DB_NAME
        if os.path.isfile(db):
            os.remove(db)

    def setUp(self):
        self.path = DATA_DIR / DB_NAME
        self.clients = DETAILS
        self.storage = SqlStorage(self.path,self.clients)


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
        self.assertFalse(self.storage.log())
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


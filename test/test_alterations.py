#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## QTorrentCompanion v0.2
##
## This code written for the "QTorrentCompanion" program
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
from unittest import TestCase
sys.path.append(os.getcwd())
try:
    from test._testsettings import DETAILS,DB_NAME,DATA_DIR
except:
    from test.testsettings import DETAILS,DB_NAME,DATA_DIR

from QTorrentCompanion.session import SqlSession

from QTorrentCompanion.storage import SqlStorage,BaseStorage

class TestOthers(TestCase):
    @classmethod
    def setUpClass(cls):
        class_clients = DETAILS
        class_db = DATA_DIR / DB_NAME
        sql_storage = SqlStorage(class_db,class_clients)
        sql_storage.log()

    def setUp(self):
        self.clients = DETAILS
        self.path = DATA_DIR / DB_NAME

    @classmethod
    def tearDownClass(cls):
        db = DATA_DIR / DB_NAME
        if os.path.isfile(db):
            os.remove(db)

    def test_session_queries(self):
        session = SqlSession(self.path,self.clients)
        self.assertTrue(session)
        for client in session.clients:
            info = session.get_torrent_names(client)
            with self.subTest(i=client):
                self.assertTrue(info)
                self.assertIn(client,self.clients)
            hashes,names,client = [],[],[]
            for i in info:
                hashes.append(i[1])
                names.append(i[0])
                client.append(i[2])
            for t_hash in hashes:
                rows = session.get_static_rows(t_hash,client)
                self.assertTrue(rows)
                for row in rows:
                    with self.subTest(i=t_hash):
                        self.assertIn(("Hash",t_hash),row)

    def test_db_data_changes(self):
        storage = SqlStorage(self.path,self.clients)
        storage.log()
        hashes = set()
        for client in self.clients:
            data = storage.make_client_requests(client)
            for torrent in data:
                hashes.add(torrent["hash"])
                torrent["tags"] = "Books"
                self.assertEqual(torrent["tags"], "Books")
                torrent["category"] = "software"
                torrent["client"] = client
                self.assertEqual(torrent["category"], "software")
                torrent["state"] = "uploadingAllDayLong"
            with self.subTest("filter_new"):
                self.assertFalse(list(storage.filter_new(data)))
        for row in storage.select_rows("static"):
            if row["hash"] in hashes:
                self.assertEqual(row["category"], "software")
                self.assertEqual(row["tags"],"Books")
                self.assertEqual(row["state"],"uploadingAllDayLong")





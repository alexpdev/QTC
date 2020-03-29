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
from unittest import TestCase
sys.path.append(os.getcwd())
try:
    from tests.test_pydenv import pydenv
    pydenv()
    from tests._testsettings import DETAILS,DB_NAME,DATA_DIR
except:
    from tests.testsettings import DETAILS,DB_NAME,DATA_DIR

from qtc.session import SqlSession

from qtc.storage import SqlStorage,BaseStorage

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





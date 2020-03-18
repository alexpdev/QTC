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
from pathlib import Path
# BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
# sys.path.append(BASE_DIR)
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


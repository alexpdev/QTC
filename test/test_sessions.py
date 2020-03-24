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

from src.session import BaseSession,SqlSession
from src.storage import SqlStorage


class TestSession(TestCase):

    @classmethod
    def setUpClass(cls):
        db = DATA_DIR / DB_NAME
        if os.path.isfile(db):
            os.remove(db)

    def setUp(self):
        self.clients = DETAILS
        self.path = DATA_DIR / DB_NAME

    @classmethod
    def tearDownClass(cls):
        db =DATA_DIR / DB_NAME
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

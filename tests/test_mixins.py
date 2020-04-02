#! /usr/bin/python
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
from datetime import datetime
from unittest import TestCase
sys.path.append(os.getcwd())
try:
    from tests.test_pydenv import pydenv
    pydenv()
    from tests._testsettings import DETAILS,DB_NAME,DATA_DIR,DEBUG
except:
    from tests.testsettings import DETAILS,DB_NAME,DATA_DIR,DEBUG
    from tests.test_data import data

from qtc.mixins import QueryMixin, SqlConnect
from tests.test_data import a

class TestMixin(TestCase):
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
        db = DATA_DIR / DB_NAME
        if os.path.isfile(db):
            os.remove(db)

    def test_sqlconnect(self):
        connection = SqlConnect(self.path)
        with connection as cursor:
            self.assertTrue(cursor)
        return True

    def test_create_table(self):
        mixin = QueryMixin()
        mixin.path = self.path
        mixin.clients = self.clients
        connection = SqlConnect(self.path)
        mixin.connection = connection
        self.assertTrue(mixin)
        self.assertEqual(mixin.path,self.path)
        mixin.create_db_table("timestamp","stamps")
        stamp = datetime.timestamp(datetime.now())
        mixin.log_timestamp(stamp)
        with connection as curs:
            r = tuple(curs.execute("SELECT * FROM stamps"))
            self.assertTrue(r)
            self.assertIsInstance(r[0]["timestamp"],float)
            self.assertEqual(r[0]["timestamp"],stamp)

    def test_save_to_db(self):
        mixin = QueryMixin()
        mixin.path = self.path
        mixin.clients = self.clients
        mixin.connection = SqlConnect(self.path)
        columns = tuple(a[0].keys())
        params = tuple(["?" for i in range(len(columns))])
        mixin.create_db_table(",".join(columns),"torrents")
        all_vals = []
        for i in a:
            values = []
            for k, v in i.items():
                values.append(v)
            all_vals.append(tuple(values))
        cols,vals,params = ", ".join(columns), values, ", ".join(params)
        mixin.save_many_to_db(cols,all_vals,params,"torrents")
        rows = mixin.select_rows("torrents")
        self.assertEqual(len(rows),len(a))






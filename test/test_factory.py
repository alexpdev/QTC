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
from pathlib import Path
from unittest import TestCase
from datetime import datetime,timedelta
sys.path.append(os.getcwd())
try:
    from test._testsettings import DETAILS,DB_NAME,DATA_DIR
except:
    from test.testsettings import DETAILS,DB_NAME,DATA_DIR

from Qtc.factory import ItemFactory

from PyQt5.QtGui import QStandardItem


class TestFactory(TestCase):

    def test_factory_init(self):
        factory = ItemFactory()
        self.assertTrue(factory)
        self.assertTrue(factory.fields)
        self.assertTrue(factory.funcs)

    def test_factory_labels(self):
        factory = ItemFactory()
        for field in factory.fields.keys():
            item = factory.get_label(field)
            self.assertIsInstance(item,str)
            self.assertEqual(item,factory.fields[field]["label"])
            self.assertNotEqual(item,field)

    def test_factory_converters(self):
        factory = ItemFactory()
        samples = {
            "uploaded" : 5466326,
            "ratio" : 1.5634325,
            "timestamp" : datetime.isoformat(datetime.now()),
            "completed" : 455,
            "seen_complete" : datetime.timestamp(datetime.now()),
            "time_active" : datetime.timestamp(datetime.now()),
            "name" : "hoolahoops",
            "hash" : "abcd1234"
        }
        for k,v in samples.items():
            item = factory.gen_item(k,v)
            self.assertTrue(item)
            self.assertIsInstance(item,QStandardItem)
            self.assertEqual(item.field,k)
            self.assertEqual(item.value,v)









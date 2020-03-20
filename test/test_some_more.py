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



class TestMore(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = DATA_DIR / DB_NAME
        if os.path.isfile(path):
            os.remove(path)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.path):
            os.remove(cls.path)

    def setUp(self):
        self.path = DATA_DIR / DB_NAME
        self.clients = DETAILS
        self.storage = SqlStorage(self.path,self.clients)

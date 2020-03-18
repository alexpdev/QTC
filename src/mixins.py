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


import json
import os
import pickle
import sqlite3
import sys
from datetime import datetime

import requests


class RequestError(Exception):
    pass


class DbAlreadyConnected(Exception):
    pass


class NoDatabaseConnected(Exception):
    pass


class RequestMixin:
    def login(self,url=None,credentials=None):
        url += "auth/login"
        response = requests.get(url, params=credentials)
        self.check_response(response)
        return response

    def check_response(self, response):
        if response.status_code == 200:
            return True
        else:
            raise RequestError

    def get_info(self,resp,url=None):
        if not url:
            url = self.url
        url += "torrents/info"
        cookies = resp.cookies
        response = requests.get(url, cookies=cookies)
        self.check_response(response)
        data = response.json()
        return data


class QueryMixin:

    def db_disconnect(self):
        self.conn.commit()
        self.curs.close()
        self.conn.close()

    def db_connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.curs = self.conn.cursor()
        return self.curs

    def torrent_exists(self,table,field,value):
        row = self.select_where(table,field,value)
        if row: return True
        return False

    def log_timestamp(self,stamp):
        cur = self.db_connect()
        statement = f"INSERT INTO stamps VALUES (?)"
        cur.execute(statement,(stamp,))
        self.db_disconnect()
        return

    def save_to_db(self,torrent,table_name):
        cur = self.db_connect()
        columns, values, params = self.get_save_values(torrent)
        stat = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        cur.execute(stat,tuple(values))
        self.db_disconnect()
        return

    def save_many_to_db(self,columns,commit_values,params,table_name):
        cur = self.db_connect()
        statement = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        cur.executemany(statement,commit_values)
        self.db_disconnect()
        return

    def select_rows(self,table):
        cur = self.db_connect()
        statement = f"SELECT * FROM {table}"
        r = cur.execute(statement)
        rows = r.fetchall()
        self.db_disconnect()
        return rows

    def select_where(self,table,field,value):
        cur = self.db_connect()
        stmnt = f"SELECT * FROM {table} WHERE {field} == ?"
        r = cur.execute(stmnt,(value,))
        rows = r.fetchall()
        self.db_disconnect()
        return rows

    def create_db_table(self,headers,table_name):
        cur = self.db_connect()
        statement = f"CREATE TABLE {table_name} ({headers})"
        cur.execute(statement)
        self.db_disconnect()
        return

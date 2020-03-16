import json
import os
import pickle
import sqlite3 as sql
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

    def get_connection(self):
        self.conn = sql.connect(self.path)
        return self.conn

    def get_cursor(self):
        conn = sql.connect(self.path)
        conn.row_factory = sql.Row
        cur = conn.cursor()
        return cur

    def torrent_exists(self,table,field,value):
        row = self.select_where(table,field,value)
        try:
            r = next(row)
            return True
        except StopIteration:
            return False

    def log_timestamp(self,stamp):
        cur = self.conn.cursor()
        statement = f"INSERT INTO logtime VALUES (?)"
        cur.execute(statement,tuple(stamp))
        cur.close()

    def save_to_db(self,torrent,table_name):
        cur = self.conn.cursor()
        columns, values, params = self.get_save_values(torrent)
        stat = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        cur.execute(stat,tuple(values))
        self.conn.commit()
        cur.close()
        return

    def save_many_to_db(self,columns,commit_values,params,table_name):
        cur = self.conn.cursor()
        statement = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        cur.executemany(statement,commit_values)
        self.conn.commit()
        cur.close()
        return

    def select_rows(self,table,*args):
        cur = self.get_cursor()
        args = "*" if not args else args
        statement = f"SELECT {args} FROM {table}"
        rows = cur.execute(statement)
        return rows

    def select_where(self,table,field,value):
        cur = self.get_cursor()
        stmnt = f"SELECT * FROM {table} WHERE {field} == ?"
        rows = cur.execute(stmnt,(value,))
        return rows

    def create_db_table(self,headers,table_name):
        cur = self.conn.cursor()
        statement = f"CREATE TABLE {table_name} ({headers})"
        cur.execute(statement)
        self.conn.commit()
        cur.close()
        return

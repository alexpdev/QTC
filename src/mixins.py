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
        self.get_connection()
        self.conn.row_factory = sql.Row
        self.cur = self.conn.cursor()
        return self.cur

    def torrent_exists(self,table,field,value):
        row = self.select_where(table,field,value)
        if row: return True
        return False

    def log_timestamp(self,stamp):
        cur =  self.conn.cursor()
        statement = f"INSERT INTO stamps VALUES (?)"
        cur.execute(statement,(stamp,))
        self.conn.commit()
        cur.close()
        return

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

    def select_rows(self,table):
        self.cur = self.get_cursor()
        statement = f"SELECT * FROM {table}"
        r = self.cur.execute(statement)
        rows = r.fetchall()
        self.cur.close()
        return rows

    def select_where(self,table,field,value):
        self.cur = self.get_cursor()
        stmnt = f"SELECT * FROM {table} WHERE {field} == ?"
        r = self.cur.execute(stmnt,(value,))
        rows = r.fetchall()
        self.cur.close()
        return rows

    def create_db_table(self,headers,table_name):
        cur = self.conn.cursor()
        statement = f"CREATE TABLE {table_name} ({headers})"
        cur.execute(statement)
        self.conn.commit()
        cur.close()
        return

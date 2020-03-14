import os
import sys
import json
import pickle
import requests
import sqlite3 as sql
from datetime import datetime


class RequestError(Exception):
    pass


class DbAlreadyConnected(Exception):
    pass


class NoDatabaseConnected(Exception):
    pass


class RequestMixin:
    def login(self,url=None,credentials=None):
        if not url:
            url = self.url
            credentials = self.credentials
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

    def get_cursor(self,path=None):
        if not path:
            path = self.path
        if self.connect:
            return self.cursor
        self.connect = sql.connect(path)
        self.cursor = self.connect.cursor()
        return self.cursor

    def create_db_table(self,headers,table_name):
        statement = f"CREATE TABLE {table_name} ({headers})"
        self.cursor.execute(statement)
        self.connect.commit()
        return

    def save_to_db(self,torrent,table_name):
        columns, values, params = self.get_save_values(torrent)
        stat = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        self.cursor.execute(stat,tuple(values))
        self.connect.commit()

    def save_many_to_db(self,columns,commit_values,params,table_name):
        statement = f"INSERT INTO {table_name} ({columns}) VALUES ({params})"
        cursor = self.get_cursor(self.path)
        cursor.executemany(statement,commit_values)
        self.connect.commit()

    def create_table(self,table_name,fields):
        fields = ", ".join(fields)
        statement = f"CREATE TABLE {table_name} ({fields})"
        self.cursor.execute(statement)
        self.connect.commit()
        return

    def torrent_exists(self,table,field,value):
        row = self.select_where(table,field,value)
        if not row: return False
        return True

    def select_rows(self,table,*args):
        statement = f"SELECT {args} FROM {table}"
        self.cursor.execute(statement)
        return self.cursor

    def select_where(self,table,field,value):
        stmnt = f"SELECT * FROM {table} WHERE ({field} = ?)"
        self.cursor.execute(stmnt,(value,))
        return self.cursor

    def get_save_values(self,torrent):
        column,values,params = [],[],[]
        for k,v in torrent.items():
            column.append(k)
            values.append(v)
            params.append("?")
        return ", ".join(column), values, ", ".join(params)

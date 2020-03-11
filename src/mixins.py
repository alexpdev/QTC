import os
import sys
import json
import pickle
import requests
import sqlite3 as sql
from datetime import datetime
from .utils import latest_log, log_filename


class RequestError(Exception):
    pass


class DbAlreadyConnected(Exception):
    pass


class NoDatabaseConnected(Exception):
    pass


class RequestMixin:
    def login(self, credentials=None, url=None):
        url = self.url + "auth/login"
        response = requests.get(url, params=self.credentials)
        self.check_response(response)
        self.response = response
        self.cookies = response.cookies
        return response

    def check_response(self, response):
        if response.status_code == 200:
            return True
        else:
            raise RequestError

    def get_info(self):
        url = self.url + "torrents/info"
        response = requests.get(url, cookies=self.cookies)
        self.check_response(response)
        data = response.json()
        return data


class QueryMixin:

    @property
    def con(self):
        return self._connection

    @property
    def cur(self):
        return self._cursor

    def connect(self,path):
        if self.con:
            raise DbAlreadyConnected
        self._connection = sql.connect(path)
        self._cursor = self._connection.cursor()
        return self.cur

    def create_table(self,table_name,foreign_key=None,**kwargs):
        statmnt = "CREATE TABLE " + table_name + "("
        columns = [" ".join([str(i),str(j)]) for i,j in kwargs.items()]
        params = ", ".join(columns)
        if foreign_key:
            params += ", FOREIGN KEY(hash) REFERENCES static(hash)"
        statmnt = "".join([statmnt,params,")"])
        self.cur.execute(statmnt)
        self.con.commit()
        return

    def insert_row(self,table_name,**kwargs):
        stmnt = f"INSERT INTO {table_name} "
        columns,values = [],[]
        for k,v in kwargs.items():
            columns.append(k)
            values.append(v)
        columns = "(" + ",".join(columns) + ")"
        params = "(" + ",".join(["?" for i in range(len(values))]) + ")"
        statement = "".join([stmnt,columns," VALUES ", params])
        self.cur.execute(statement,tuple(values))
        self.con.commit()
        return

    def select_rows(self,table,*args):
        if args:
            statement = f"SELECT {args} FROM {table}"
        else:
            statement = f"SELECT * FROM {table}"
        self.cur.execute(statement)
        lst = []
        for row in self.cur:
            print(row)
            lst.append(row)
        return row

    def select_where(self,table,field,value):
        stmnt = f"SELECT * FROM {table} WHERE ({field} = ?)"
        self.cur.execute(stmnt,(value,))


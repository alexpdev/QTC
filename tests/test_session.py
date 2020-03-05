from unittest import TestCase
import requests
import src
from datetime import datetime
from time import time,sleep
from src.objects import Session

class SessionTest(TestCase):

    def setUp(self):
        self.credentials = {"username":"password"}
        self.url = "http://127.0.0.1:8080/api/v2"
        self.response = requests.get(self.url + "/torrents/list")
        self.cookies = self.response.cookies
        self.kwargs = {
            "credentials" : self.credentials,
            "base_url" : self.url,
            "cookies" : self.cookies,
            "response" : self.response
        }
        self.args = (self.url,self.credentials,self.response)
        self.ul,self.dl = 0,0
        self.data = {
                "hash" : "1234567890POIOU",
                "name" : "MyTorrent1080P",
                "ul" : "0",
                "dl" : "0"
            }
        self.logs = src._vars["data"] / "test"

    def test_kwargs_init(self):
        session = Session(**self.kwargs)
        self.assertEqual(session.url,self.url)
        self.assertEqual(self.cookies,session.cookies)
        self.assertEquals(self.credentials,session.credentials)

    def test_args_init(self):
        session = Session(*self.args)
        self.assertEqual(session.url,self.url)
        self.assertEqual(self.cookies,session.cookies)
        self.assertEquals(self.credentials,session.credentials)

    def test_log(self):
        Session.logs = self.logs
        session = Session(**self.kwargs)
        print(self.logs)
        self.assertEqual(session.logs,self.logs)
        lst = list(self.logs.iterdir())
        session.log(self.data)
        for i in range(60):
            self.data["ul"] = str(self.ul+(13453*i))
            self.data["dl"] = str(self.dl+(89765*i))
            session.log(self.data)
            sleep(1.0)
        nlst = list(self.logs.iterdir())
        self.assertNotEqual(lst,nlst)

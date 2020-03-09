

import os
from unittest import TestCase
import testingconf
from src.session import BaseSession,Session

USER = os.environ["USERNAME"]
PASS = os.environ["PASSWORD"]

SEED_PASS = os.environ["SEEDBOXPASS"]
SEED_USER = os.environ["SEED_USER"]
SEED_URL = os.environ["SEEDBOXURL"]
LOCAL1 = os.environ["LOCAL1"]
LOCAL2 = os.environ["LOCAL2"]


class SessionTest(TestCase):

    def setUp(self):
        self.credentials = {"username":USER,"password":PASS}
        self.urls = [LOCAL1,LOCAL2]
        self.seed = {
            "name" : "SEEDBOX",
            "url":SEED_URL,
            "credentials":{
                "username":SEED_USER,
                "password":SEED_PASS
                }}

    def test_create_session(self):
        for url in self.urls:
            session = BaseSession(credentials=self.credentials,url=url)
            self.assertEqual(session.credentials , self.credentials)
            # self.assertTrue(session.name,None)
            self.assertEqual(session.url,url)

    def test_http_requests(self):
        for url in self.urls:
            session = BaseSession(credentials=self.credentials,url=url)
            response = session.login()
            self.assertTrue(response)
            self.assertEqual(response.status_code,200)
            info = session.get_info()
            self.assertTrue(info)

    def test_with_kwargs(self):
        session = BaseSession(**self.seed)
        response = session.login()
        self.assertTrue(session.name,self.seed["name"])
        self.assertEqual(response.status_code,200)
        info = session.get_info()
        self.assertTrue(info)








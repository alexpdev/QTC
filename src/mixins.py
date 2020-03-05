import os
import sys
import json
import requests
from datetime import datetime

class RequestError(Exception):
    pass

class SessionMixin:

    def login(self):
        url = self.url + "auth/login"
        response = requests.get(url,params=self.credentials)
        self.check_response(response)
        self.response = response
        self.cookies = response.cookies
        return response

    def check_response(self,response):
        if response.status_code == 200:
            return True
        else:
            raise RequestError

    def get_info(self):
        url = self.url + "torrents/info"
        cookie = self.cookies
        response = requests.get(url,cookies=cookie)
        self.check_response(response)
        js = response.json()
        return js

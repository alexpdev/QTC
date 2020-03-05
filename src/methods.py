import os
import sys
import json
import requests
from datetime import datetime
from src.objects import RequestError,Session

def login(*args,**kwargs):
    try:
        respnse = _login_with_args(*args)
    except:
        response = _login_with_kwargs(**kwargs)
    return response

def _login_with_kwargs(**kwargs):
    url = kwargs["url"] + "auth/login"
    response = requests.get(url,params=kwargs["credentials"])
    if response.status_code != 200:
        raise RequestError
    kwargs["response"] = response
    kwargs["cookies"] = response.cookies
    session = Session(**kwargs)
    return session

def _login_with_args(*args):
    url,username,password = args
    credentials = {"username":username,"password":password}
    response = requests.get(url+"auth/login",params=credentials)
    if response.status_code != 200:
        raise RequestError
    args = (url,credentials,response)
    session = Session(*args)
    return session

def check_response(response):
    if response.status_code == 200:
        return True
    else:
        raise RequestError

def get_info(base,response):
    url = base + "torrents/info"
    cookie = response.cookies
    response = requests.get(url,cookie=cookie)
    check_response(response)
    js = response.json()
    return js

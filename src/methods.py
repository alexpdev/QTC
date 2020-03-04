import os
import sys
import json
import requests
from src.urls import items
from src.objects import RequestError


def login(*args,**kwargs):
    try:
        respnse = _login_with_args(*args)
    except:
        response = _login_with_kwargs(**kwargs)
    return response

def _login_with_kwargs(**kwargs):
    url = kwargs["url"] + "auth/login"
    params = kwargs["credentials"]
    response = requests.get(url,params=params)
    if response.status_code == 200:
        return response
    raise RequestError


def _login_with_args(url,username,password):
    params = {"username":username,"password":password}
    response = requests.get(url+"auth/login",params=params)
    if response.status_code == 200:
        return response
    raise RequestError

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

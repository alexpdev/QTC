#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## QTorrentCompanion v0.2
##
## This code written for the "QTorrentCompanion" program
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
## PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
###
######
################################################################################
# Default and Custom Configuration Data Go Here

import os
from pathlib import Path

"""
    User specific details should be filled in below. TODO will be to create a GUI menu within app for filling this information in... eventually.
"""

## Local or remote client information should be entered below.

## Client name can be any name you want e.g. "home computer", "seedbox" ...
LOCAL_CLIENT = "home"

## The absolute URL to the client's Web UI.
LOCAL_URL = "http://127.0.0.1:8080/api/v2" # Default for most clients

## Username and password if security options are enable for the client.
USER = "admin" # default on most clients if applicable
PASS = ""
## If Web UI security features are not enabled then assign user and pass to
## empty strings.


## If you would like to track more than one client then repeat the same 4 items
## from above and make sure to add the variables to the DETAILS map at the
## bottom of this file.
LOCAL_CLIENT2 = "optional_client_#2"
LOCAL_URL2 = ""

REMOTE_CLIENT = "seedbox"
REMOTE_URL = "http://remote.url/api/v2"
REMOTE_USER = "remote_user"
REMOTE_PASS = "remote_password"



## The name of the database file.
DB_NAME = "qbtdata.db"

## The directory where the database file will live relative to the application's
## root directory. Default is "./data". Directory must already exist prior to
## starting the application.
DATA_DIR = "data"

## Setting this to true currently does nothing.
DEBUG = False  # TODO #


## Variable map read in by the application.
DETAILS = {
    LOCAL_CLIENT :{
        "url": LOCAL_URL,
        "credentials":{
            "username": USER,
            "password": PASS,
        }
    },
    LOCAL_CLIENT2 :{
        "url": LOCAL_URL2,
        "credentials":{
            "username": USER,
            "password": PASS,
        }
    },
    REMOTE_CLIENT : {
        "url" : REMOTE_URL,
        "credentials":{
            "username": REMOTE_USER,
            "password": REMOTE_PASS,
        }
    }
}

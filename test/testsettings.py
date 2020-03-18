#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qbt Companion v0.1
##
## This code written for the "Qbt Companion" program
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
### PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
######
################################################################################

import os
import sys
from pathlib import Path
SETTINGS_FILE = Path(__file__).resolve()
BASE_DIR = SETTINGS_FILE.parents[1]
sys.path.append(BASE_DIR)
USER = os.environ["USERNAME"]
PASS = os.environ["PASSWORD"]
SEED_PASS = os.environ["SEEDBOXPASS"]
SEED_URL = os.environ["SEEDBOXURL"]
SEED_USER = os.environ["SEED_USER"]
DATA_DIR = BASE_DIR / "temp" / "db"
DB_NAME = "qbtdata.db"
DB_PATH = DATA_DIR / DB_NAME
LOCAL1 = os.environ["LOCAL1"]
LOCAL2 = os.environ["LOCAL2"]
LOCAL1_CLIENT = os.environ["LOCAL1_CLIENT"]
LOCAL2_CLIENT = os.environ["LOCAL2_CLIENT"]
CLIENTS = [LOCAL1_CLIENT,LOCAL2_CLIENT,"seedbox"]
DETAILS = {
    # LOCAL1_CLIENT:{
    #     "url": LOCAL1,
    #     "credentials":{
    #         "username" : USER,
    #         "password" : PASS
    #     }
    # },
    LOCAL2_CLIENT :{
        "url": LOCAL2,
        "credentials":{
            "username": USER,
            "password": PASS,
        }
    },
    "seedbox" : {
        "url" : SEED_URL,
        "credentials":{
            "username": SEED_USER,
            "password": SEED_PASS,
        }
    }
}

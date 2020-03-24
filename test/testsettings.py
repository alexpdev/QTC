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
######
################################################################################

from pathlib import Path

# No editing should be necessary
SETTINGS_FILE = Path(__file__).resolve() #  This File Path

# Application Root Directory
BASE_DIR = SETTINGS_FILE.parents[1]

# path to data directory for testing purposes
# This should not be the same as the main applications data_dir
DATA_DIR = BASE_DIR / "temp" / "db"

# Name of database file
DB_NAME = "qbtdata.db"

# testing data dir and db_file name concatenated
# there shouldn't be any reason to edit this so leave as is
DB_PATH = DATA_DIR / DB_NAME

# Torrent Client Login Credentials If Applicable
USER = "admin"
PASS = "admin"

# client identifiers
LOCAL_CLIENT = "local"


# client urls for web api
LOCAL = "http://127.0.0.1:8080/api/v2"  #Default url for most clients


# for application use, leave as is
DETAILS = {
    LOCAL_CLIENT :{
        "url": LOCAL,
        "credentials":{
            "username": USER,
            "password": PASS,
        }
    }
}

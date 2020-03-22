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

import sys
import os
from pathlib import Path
from threading import Thread

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
BASE_DIR = Path(BASE_DIR)
try:
    from src._settings import (DATA_DIR, DB_NAME, DETAILS, DEBUG)
except:
    from src.settings import (DATA_DIR, DB_NAME, DETAILS, DEBUG)


from src.storage import SqlStorage
from src.session import SqlSession


def main():
    """ Esecute main program.

    Returns:
        int -- returns 0 on program exit.
    """
    database_path = BASE_DIR / DATA_DIR / DB_NAME
    clients = DETAILS
    storage = SqlStorage(database_path,clients)
    session = SqlSession(database_path,clients)
    log_thread = Thread(target=storage.log)
    log_thread.start()
    session.mainloop()
    return 0

if __name__ == "__main__":
    main()

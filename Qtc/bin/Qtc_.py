#!/usr/bin/python
#! -*- coding: utf-8 -*-

################################################################################
######
###
## Qtc v0.2
##
## This code written for the "Qtc" program
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

dirname = lambda x: os.path.dirname(x)
here = dirname(os.path.abspath(__file__))
BASE_DIR = dirname(dirname(here))
sys.path.append(BASE_DIR)
BASE_DIR = Path(BASE_DIR)

try:
    from qtc.bin.pydenv import pydenv
    pydenv()
    from qtc.__settings import (DATA_DIR, DB_NAME, DETAILS, DEBUG)
except:
    from qtc.settings import (DATA_DIR, DB_NAME, DETAILS, DEBUG)


from qtc.storage import SqlStorage
from qtc.session import SqlSession


def main():
    """ Execute main program.

    Returns:
        int -- returns 0 on program exit.
    """
    database_path = BASE_DIR / "Qtc" /  DATA_DIR / DB_NAME
    clients = DETAILS
    storage = SqlStorage(database_path,clients)
    session = SqlSession(database_path,clients)
    log_thread = Thread(target=storage.log)
    log_thread.start()
    session.mainloop(log_thread,BASE_DIR)
    return 0

if __name__ == "__main__":
    main()

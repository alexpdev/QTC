import os
import sys
from time import sleep
from pathlib import Path
from etc.conf import FILEPREFIX,FILESUFFIX,DATA_DIRNAME
import urls
from urls import items
from src.session import Session

path = Path(__file__).resolve()
ROOT = path.parent.parent
sys.path.append(str(ROOT))


_vars = {
    "prefix" : FILEPREFIX,
    "suffix" : FILESUFFIX,
    "data" : ROOT / DATA_DIRNAME,
    "urls" : urls
}


def main(k,v):
    session = Session(name=k,**v)
    a = session.login()
    b = session.get_info()
    session.log(b)
    print(b)







if __name__ == "__main__":
    for k,v in items.items():
        main(k,v)

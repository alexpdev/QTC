import os
import sys
from time import sleep
from pathlib import Path

path = Path(__file__).resolve()
ROOT = path.parent.parent
sys.path.append(str(ROOT))

import urls
from urls import items
from src.session import Session

def main(k,v):
    session = Session(name=k,**v)
    a = session.login()
    b = session.get_info()
    session.log(b)
    print(b)

if __name__ == "__main__":
    for k,v in items.items():
        main(k,v)
